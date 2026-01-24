from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import reduce
from random import random, shuffle
import shutil
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import json
import os
import re
import sys
import unicodedata

from langtext import LangText


WORD_PREFIX = "word"
SCORE_PREFIX = "score"
TYPE_PREFIX = "<type>"


class Kit(Enum):
    """Defines the available language kit configurations."""

    LATIN = "kits/kit_latin.json"

    def load_config(
        self,
        *,
        base_dir: Optional[str] = None,
        fallback_dir: Optional[str] = None,
        copy_to_base_dir: bool = True,
    ) -> dict:
        """Load kit configuration.

        Preference order:
        1) base_dir/<kit path> (user-editable)
        2) fallback_dir/<kit path> (bundled with the app)

        If we end up using the bundled copy and copy_to_base_dir is True, we try
        to copy it into base_dir so users can edit it.
        """

        def _try_load(path: str) -> Optional[dict]:
            if not path or not os.path.exists(path):
                return None
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(
                    f"ERROR: Kit file {path} has invalid JSON.",
                    file=sys.stderr,
                )
                return None

        base_path = os.path.join(base_dir, self.value) if base_dir else ""
        # Bundled resources live under app_dir/assets/...
        fb_path = (
            os.path.join(fallback_dir, "assets", self.value) if fallback_dir else ""
        )

        cfg = _try_load(base_path)
        if cfg is not None:
            return cfg

        cfg = _try_load(fb_path)
        if cfg is not None:
            if copy_to_base_dir and base_dir and fb_path and os.path.exists(fb_path):
                try:
                    os.makedirs(os.path.dirname(base_path), exist_ok=True)
                    if base_path and not os.path.exists(base_path):
                        shutil.copy2(fb_path, base_path)
                except Exception:
                    # Best-effort only.
                    pass
            return cfg

        print(
            f"ERROR: Kit file {self.value} not found. Using empty kit.",
            file=sys.stderr,
        )
        return {}


# ----------------------
# Kit prompt tree


@dataclass(frozen=True)
class InputNode:
    key: str
    label: str


@dataclass(frozen=True)
class GroupNode:
    label: str
    children: Tuple["PromptNode", ...]


@dataclass(frozen=True)
class ChoiceNode:
    label: str
    options: Tuple[str, ...]
    default: str
    option_children: Dict[str, Tuple["PromptNode", ...]]
    showtype_here: bool = False


PromptNode = Union[InputNode, GroupNode, ChoiceNode]


def _is_meta_key(key: str) -> bool:
    return key.startswith("<") and key.endswith(">")


def build_prompt_tree(
    kit: Any, *, label: Optional[str] = None, showtype: Optional[str] = None
) -> Tuple[PromptNode, ...]:
    """Builds a UI-friendly prompt tree from the kit definition.

    The returned nodes describe either:
    - free text inputs (InputNode)
    - purely visual grouping (GroupNode)
    - a choice selection (ChoiceNode) that changes which sub-prompts appear

    The produced data, when collected, matches the CLI's `add_kit_properties` behavior.
    """

    if kit is None or not isinstance(kit, dict):
        return tuple()

    mode = kit.get("<mode>")
    if not mode:
        return tuple()

    if mode == "and":
        children: List[PromptNode] = []

        # If <showtype> is set, the selected type from the parent choice is stored in <type>.
        if kit.get("<showtype>") and showtype:
            # Hidden output; no UI field needed. We'll store it when collecting.
            children.append(GroupNode(label=TYPE_PREFIX, children=tuple()))

        for key, val in kit.items():
            if _is_meta_key(key):
                continue
            if val is None:
                children.append(InputNode(key=key, label=key))
            else:
                sub = build_prompt_tree(val, label=key, showtype=showtype)
                if sub:
                    children.append(GroupNode(label=key, children=sub))
        return tuple(children)

    if mode == "or":
        options = tuple(k for k in kit.keys() if not _is_meta_key(k))
        if not options:
            return tuple()
        default = options[-1]

        option_children: Dict[str, Tuple[PromptNode, ...]] = {}
        for opt in options:
            opt_val = kit.get(opt)
            if opt_val is None:
                option_children[opt] = tuple()
            else:
                option_children[opt] = build_prompt_tree(
                    opt_val, label=opt, showtype=opt
                )

        node = ChoiceNode(
            label=label or "choose",
            options=options,
            default=default,
            option_children=option_children,
            showtype_here=bool(kit.get("<showtype>")),
        )
        return (node,)

    if mode in ("apart", "both"):
        # Handled at higher level (per-language).
        return tuple()

    return tuple()


def collect_prompt_data(
    nodes: Iterable[PromptNode],
    *,
    selections: Dict[str, str],
    inputs: Dict[str, str],
    showtype: Optional[str] = None,
) -> Dict[str, Any]:
    """Collects user entries into the flat dict format used by word entries."""

    data: Dict[str, Any] = {}

    for node in nodes:
        if isinstance(node, InputNode):
            if node.key in inputs:
                data[node.key] = inputs[node.key]
        elif isinstance(node, GroupNode):
            if node.label == TYPE_PREFIX and showtype:
                data[TYPE_PREFIX] = showtype
            else:
                data.update(
                    collect_prompt_data(
                        node.children,
                        selections=selections,
                        inputs=inputs,
                        showtype=showtype,
                    )
                )
        elif isinstance(node, ChoiceNode):
            sel = selections.get(node.label, node.default)
            # If this choice node itself stores <type>
            if node.showtype_here:
                data[TYPE_PREFIX] = sel
            data.update(
                collect_prompt_data(
                    node.option_children.get(sel, tuple()),
                    selections=selections,
                    inputs=inputs,
                    showtype=sel,
                )
            )

    return data


# ----------------------
# Core model


class VocabLearnerModel:
    lower_boundary = 0
    upper_boundary = 5
    dead_pt = 15
    boost_pt = -10

    def __init__(
        self,
        kit: Kit,
        *,
        base_dir: Optional[str] = None,
        app_dir: Optional[str] = None,
    ):
        # base_dir: where user data lives (glossaries, kit copy, settings, ...)
        # app_dir: bundled/read-only application directory (fallback resources)
        self.base_dir = base_dir or os.getcwd()
        self.app_dir = app_dir or os.getcwd()

        os.makedirs(self.base_dir, exist_ok=True)

        legacy_glossary_dir = os.path.join(self.base_dir, "glossary")
        self.glossary_dir = os.path.join(self.base_dir, "glossaries")
        if os.path.isdir(legacy_glossary_dir) and not os.path.isdir(self.glossary_dir):
            try:
                os.rename(legacy_glossary_dir, self.glossary_dir)
            except Exception:
                # Best-effort only.
                pass
        os.makedirs(self.glossary_dir, exist_ok=True)

        self._bootstrap_user_data()

        self.kit = kit.load_config(base_dir=self.base_dir, fallback_dir=self.app_dir)
        self.mlang = self.get_lang("mothertongue")
        self.learnlang = self.get_lang("learninglang")
        self.languages = [self.mlang, self.learnlang]

        self.glossaries: List[str] = []
        self.words: Dict[str, List[Dict[str, Dict[str, Any]]]] = {}
        self.all_words: List[Dict[str, Dict[str, Any]]] = []

        self.load_all()

    def get_lang(self, langtype: str) -> str:
        assert langtype in ["mothertongue", "learninglang"], "Wrong type!"
        for lang, props in self.kit.items():
            if lang == "<mode>":
                continue
            if isinstance(props, dict) and props.get(TYPE_PREFIX) == langtype:
                return lang
        raise ValueError(f"No language with <type>={langtype} in kit")

    def _path(self, filename: str) -> str:
        return os.path.join(self.base_dir, filename)

    def _glossary_path(self, gloss: str) -> str:
        return os.path.join(self.glossary_dir, gloss + ".txt")

    def _bootstrap_user_data(self) -> None:
        """Best-effort: populate user data dir from bundled resources."""

        try:
            # Copy glossary/*.txt if the user folder is empty.
            try:
                has_user_gloss = any(
                    name.lower().endswith(".txt")
                    and os.path.isfile(os.path.join(self.glossary_dir, name))
                    for name in os.listdir(self.glossary_dir)
                )
            except Exception:
                has_user_gloss = False

            bundled_gloss_dir = os.path.join(self.app_dir, "assets", "glossaries")
            if (
                (not has_user_gloss)
                and os.path.isdir(bundled_gloss_dir)
                and os.path.isdir(self.glossary_dir)
            ):
                for name in os.listdir(bundled_gloss_dir):
                    if not name.lower().endswith(".txt"):
                        continue
                    src = os.path.join(bundled_gloss_dir, name)
                    dst = os.path.join(self.glossary_dir, name)
                    if os.path.isfile(src) and not os.path.exists(dst):
                        try:
                            shutil.copy2(src, dst)
                        except Exception:
                            pass

            # Ensure kits folder exists in user data (Kit.load_config will copy on demand).
            os.makedirs(os.path.join(self.base_dir, "kits"), exist_ok=True)
        except Exception:
            # Best-effort only.
            pass

    def load_all(self) -> None:
        self.load_glossaries()
        self.load_words()

    def load_glossaries(self) -> None:
        os.makedirs(self.glossary_dir, exist_ok=True)
        names: List[str] = []
        try:
            for fname in os.listdir(self.glossary_dir):
                if not fname.lower().endswith(".txt"):
                    continue
                full = os.path.join(self.glossary_dir, fname)
                if not os.path.isfile(full):
                    continue
                stem, _ = os.path.splitext(fname)
                stem = stem.strip()
                if stem:
                    names.append(stem)
        except Exception:
            names = []

        names.sort(key=lambda s: s.casefold())
        self.glossaries = names

    def _parse_word_file(self, gloss: str) -> List[Dict[str, Dict[str, Any]]]:
        file_path = self._glossary_path(gloss)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8"):
                pass
            return []

        result: List[Dict[str, Dict[str, Any]]] = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip("\n")
                if not line.strip():
                    continue
                # Format: lang1Key:val ; key:val | lang2Key:val ; key:val
                parts = [p.strip() for p in line.split(" | ")]
                if len(parts) < 2:
                    continue

                entry: Dict[str, Dict[str, Any]] = {}
                for i, lang_name in enumerate(self.languages[:2]):
                    lang_part = parts[i]
                    comps = [c.strip() for c in lang_part.split(" ; ") if c.strip()]
                    items: Dict[str, Any] = {}
                    for comp in comps:
                        kv = [x.strip() for x in comp.split(":", 1)]
                        if len(kv) != 2:
                            continue
                        key, raw = kv[0], kv[1]
                        # numeric conversion similar to CLI behavior
                        if raw.isnumeric() or (
                            raw.startswith("-") and raw[1:].isnumeric()
                        ):
                            items[key] = int(raw)
                        else:
                            items[key] = raw
                    entry[lang_name] = items

                # Ensure required keys exist
                for lang_name in self.languages[:2]:
                    entry.setdefault(lang_name, {})
                    entry[lang_name].setdefault(WORD_PREFIX, "")
                    entry[lang_name].setdefault(SCORE_PREFIX, 0)

                result.append(entry)

        return result

    def load_words(self) -> None:
        self.words = {}
        for gloss in self.glossaries:
            try:
                self.words[gloss] = self._parse_word_file(gloss)
            except Exception as e:
                print(e, f"ERROR reading glossary {gloss}", file=sys.stderr)
                self.words[gloss] = []

        self.all_words = reduce(lambda a, b: a + b, self.words.values(), [])

    def save_glossary(self, gloss: str) -> None:
        file_path = self._glossary_path(gloss)
        with open(file_path, "w", encoding="utf-8") as f:
            for word in self.words.get(gloss, []):
                f.write(
                    " | ".join(
                        " ; ".join(f"{k}:{v}" for k, v in lang.items())
                        for lang in word.values()
                    )
                    + "\n"
                )

    def add_glossary(self, gloss: str) -> None:
        gloss = gloss.strip()
        if not gloss:
            raise ValueError("Glossary name empty")
        if any(sep in gloss for sep in ("/", "\\")):
            raise ValueError("Invalid glossary name")
        if gloss in self.glossaries:
            raise ValueError("Glossary already exists")

        os.makedirs(self.glossary_dir, exist_ok=True)
        with open(self._glossary_path(gloss), "w", encoding="utf-8"):
            pass
        self.glossaries.append(gloss)
        self.words[gloss] = []
        self.all_words = reduce(lambda a, b: a + b, self.words.values(), [])

    def find(
        self,
        word: str,
        lang: str,
        gloss: Optional[str] = None,
        prop: Optional[str] = None,
    ):
        source = self.words[gloss] if gloss is not None else self.all_words
        out = []
        for w in source:
            if w.get(lang, {}).get(WORD_PREFIX) == word:
                out.append(w if prop is None else w[lang].get(prop))
        return out

    def similarity(self, s1: str, s2: str, start1: int = 0, start2: int = 0) -> float:
        """Calculate a friendly similarity score between two strings."""
        if start1 >= len(s1) or start2 >= len(s2):
            return 0

        if s1[start1] == s2[start2]:
            return 1 + self.similarity(s1, s2, start1 + 1, start2 + 1)

        skip_s1 = self.similarity(s1, s2, start1 + 1, start2)
        skip_s2 = self.similarity(s1, s2, start1, start2 + 1)

        return max(skip_s1, skip_s2)

    def similarity_legacy(self, given: str, correct: str) -> float:
        glen, clen = len(given), len(correct)
        if glen == 0 and clen > 0:
            return 0
        g = 0
        c = 0
        score = 0
        while g < glen and c < clen:
            if given[g] == correct[c]:
                score += 1
                g += 1
                c += 1
            else:
                will_g, will_c = -1, -1
                chan_g, chan_c = g, c
                while chan_g < glen:
                    try:
                        will_c = correct.index(given[chan_g], c + 1)
                    except ValueError:
                        chan_g += 1
                    else:
                        break
                while chan_c < clen:
                    try:
                        will_g = given.index(correct[chan_c], g + 1)
                    except ValueError:
                        chan_c += 1
                    else:
                        break
                if will_c == -1 < will_g:
                    g = will_g
                    c = chan_c
                elif will_g == -1 < will_c:
                    c = will_c
                    g = chan_g
                elif will_g > -1 and will_c > -1:
                    if will_g < will_c:
                        g = will_g
                        c = chan_c
                    else:
                        c = will_c
                        g = chan_g
                else:
                    break
        return score

    def similar(self, given: str, correct: str) -> bool:
        len_given, len_correct = len(given), len(correct)
        if len_given == 0 and len_correct == 0:
            return True
        if len_given == 0 or len_correct == 0:
            return False
        score = self.similarity(given, correct)
        tolerance = 2
        if len_correct == 1:
            return len_given <= 2 and score == 1
        if len_correct <= tolerance + 1:
            return len_given <= len_correct + 1 and score >= len_correct - 1
        return max(len_correct - score, len_given - score) <= tolerance

    def get_questionlang(self, answer_lang: str) -> str:
        return self.mlang if answer_lang == self.learnlang else self.learnlang

    def get_practice_words(
        self, answer_lang: str, gloss: str
    ) -> List[Dict[str, Dict[str, Any]]]:
        practice_words = list(self.words[gloss])
        for word in self.words[gloss]:
            wordscore = int(word[answer_lang].get(SCORE_PREFIX, 0))
            if wordscore < self.lower_boundary:
                for _ in range(abs(wordscore - self.lower_boundary)):
                    practice_words.append(word)
        shuffle(practice_words)
        return practice_words

    def all_words_dead(self, *, gloss: str, answer_lang: str) -> bool:
        """Return True if every word in the glossary is 'dead' for answer_lang.

        Uses the same effective-score logic as PracticeSession:
        score is divided by the number of detail fields (excluding word/score/type).
        """

        if gloss not in self.words:
            return True

        for w in self.words.get(gloss, []):
            try:
                details = [
                    k
                    for k in w.get(answer_lang, {})
                    if k not in (WORD_PREFIX, SCORE_PREFIX, TYPE_PREFIX)
                ]
                effective = int(w[answer_lang].get(SCORE_PREFIX, 0)) // max(
                    1, len(details)
                )
                if effective < self.dead_pt:
                    return False
            except Exception:
                # If anything is malformed, treat it as not-dead so we don't
                # prematurely stop auto-continue.
                return False

        return True

    def add_word(
        self,
        gloss: str,
        mword: str,
        lword: str,
        *,
        mprops: Optional[Dict[str, Any]] = None,
        lprops: Optional[Dict[str, Any]] = None,
    ) -> None:
        if gloss not in self.words:
            raise ValueError("Unknown glossary")
        mprops = mprops or {}
        lprops = lprops or {}

        self.words[gloss].append(
            {
                self.mlang: {WORD_PREFIX: mword, SCORE_PREFIX: 0, **mprops},
                self.learnlang: {WORD_PREFIX: lword, SCORE_PREFIX: 0, **lprops},
            }
        )
        self.save_glossary(gloss)
        self.all_words = reduce(lambda a, b: a + b, self.words.values(), [])

    def learninglang_prompt_tree(self) -> Tuple[PromptNode, ...]:
        if not self.kit or "<mode>" not in self.kit:
            return tuple()
        if self.kit.get("<mode>") != "apart":
            return tuple()
        lang_kit = self.kit.get(self.learnlang, {})
        return build_prompt_tree(lang_kit, label=self.learnlang)


# ----------------------
# Practice session


class PracticeSession:
    """State machine for practice.

    UI drives it by calling `current_prompt()` and `submit(text)`.
    """

    def __init__(
        self,
        model: VocabLearnerModel,
        *,
        gloss: str,
        answer_lang: str,
        text: LangText,
        shared_total_history_items: Optional[List[Dict[str, Any]]] = None,
        shared_stats: Optional[Dict[str, int]] = None,
    ):
        self.model = model
        self.gloss = gloss
        self.answer_lang = answer_lang
        self.question_lang = model.get_questionlang(answer_lang)
        self.text: LangText = text

        self.practice_words = model.get_practice_words(answer_lang, gloss)
        self.index = 0

        self.correct_pt = 0
        self.incorrect_pt = 0

        # current word context
        self.cur_word: Optional[Dict[str, Dict[str, Any]]] = None
        self.solutions: List[Dict[str, Dict[str, Any]]] = []
        self.solution_words: List[str] = []

        # detail flow
        self.detail_items: List[Tuple[str, Any]] = []
        self.detail_i = 0
        self.to_change: Optional[Dict[str, Any]] = None

        # feedback / OK gating
        self.awaiting_ok = False
        self.ok_text = ""
        self._ok_action: Optional[str] = None  # 'next_word' | 'next_detail'

        # Per-word history for UI
        # Each item: {"label": str, "given": str, "expected": str, "correct": bool}
        self.history_items: List[Dict[str, Any]] = []
        # Total history across the whole session (words + details). When auto-continue
        # is enabled we share this list across sessions.
        self.total_history_items: List[Dict[str, Any]] = (
            shared_total_history_items if shared_total_history_items is not None else []
        )

        # Mutable stats shared across sessions when auto-continue is enabled.
        # Currently: words_practiced counts word-stage attempts only (not details).
        self._stats: Dict[str, int] = shared_stats if shared_stats is not None else {}
        self._stats.setdefault("words_practiced", 0)
        self.last_word_given: Optional[str] = None
        self.last_was_close = False

        self.done = False
        self.ended_by_user = False
        self.message = ""

        self._advance_to_next_word()

    @property
    def words_practiced(self) -> int:
        try:
            return int(self._stats.get("words_practiced", 0))
        except Exception:
            return 0

    def shared_stats(self) -> Dict[str, int]:
        return self._stats

    def _append_total_history(
        self, *, label: str, given: str, expected: str, correct: bool
    ) -> None:
        self.total_history_items.append(
            {
                "label": label,
                "given": given,
                "expected": expected,
                "correct": bool(correct),
            }
        )

    def total_history_markup(self) -> str:
        """Returns Kivy markup for the session-wide history."""

        if not self.total_history_items:
            return ""
        lines: List[str] = []
        for item in self.total_history_items:
            ok = bool(item.get("correct"))
            mark = "[color=2E7D32]OK[/color]" if ok else "[color=C62828]NO[/color]"
            label = str(item.get("label", ""))
            given = str(item.get("given", ""))
            expected = str(item.get("expected", ""))
            if ok:
                lines.append(f"{mark} {label}: {given}")
            else:
                lines.append(
                    f"{mark} {label}: {given}  [color=888888](Correct: {expected})[/color]"
                )
        return "\n".join(lines)

    def _advance_to_next_word(self) -> None:
        self.to_change = None
        self.detail_items = []
        self.detail_i = 0
        self.awaiting_ok = False
        self.ok_text = ""
        self._ok_action = None
        self.history_items = []
        self.last_word_given = None

        while self.index < len(self.practice_words):
            w = self.practice_words[self.index]
            self.index += 1

            # compute effective score like CLI (score divided by detail count)
            len_detail = len(
                [
                    k
                    for k in w[self.answer_lang]
                    if k not in (WORD_PREFIX, SCORE_PREFIX, TYPE_PREFIX)
                ]
            )
            wordscore = int(w[self.answer_lang].get(SCORE_PREFIX, 0)) // max(
                1, len_detail
            )

            if wordscore >= self.model.dead_pt:
                continue
            if wordscore > self.model.upper_boundary and random() < (
                (wordscore - self.model.upper_boundary)
                / (self.model.dead_pt - self.model.upper_boundary)
            ):
                continue

            self.cur_word = w
            self.solutions = self.model.find(
                w[self.question_lang][WORD_PREFIX], self.question_lang, self.gloss
            )
            self.solution_words = [
                s[self.answer_lang][WORD_PREFIX] for s in self.solutions
            ]
            self.message = ""
            return

        self.done = True
        self.message = "Practice finished"

    def current_prompt(self) -> Tuple[str, str]:
        """Returns (kind, text). kind is 'word' or 'detail' or 'done'."""

        if self.done or not self.cur_word:
            return ("done", self.summary())

        if self.detail_items and self.to_change is not None:
            detail_key, _ = self.detail_items[self.detail_i]
            return ("detail", detail_key)

        q = self.cur_word[self.question_lang][WORD_PREFIX]
        t = self.cur_word[self.answer_lang].get(TYPE_PREFIX)
        if t:
            q = f"{t}\n{q}"
        return ("word", q)

    def current_type(self) -> str:
        if not self.cur_word:
            return ""
        return str(self.cur_word[self.answer_lang].get(TYPE_PREFIX) or "")

    def needs_ok(self) -> bool:
        return self.awaiting_ok and bool(self.ok_text)

    def acknowledge_ok(self) -> None:
        """Call after showing ok_text to the user and they tapped OK."""
        if not self.awaiting_ok:
            return
        action = self._ok_action
        self.awaiting_ok = False
        self.ok_text = ""
        self._ok_action = None

        if action == "next_word":
            self._advance_to_next_word()
        elif action == "next_detail":
            # Advance within the detail prompts
            if self.detail_items and self.to_change is not None:
                if self.detail_i + 1 < len(self.detail_items):
                    self.detail_i += 1
                else:
                    self.detail_items = []
                    self.detail_i = 0
                    self.to_change = None
                    self._advance_to_next_word()

    def summary(self) -> str:
        total = self.correct_pt + self.incorrect_pt
        if total == 0:
            return "No answers yet."
        ratio = int(self.correct_pt / total * 10000) / 100
        return f"Correct: {self.correct_pt} | Incorrect: {self.incorrect_pt} | {ratio}%"

    def command_max_points(self) -> None:
        if not self.solutions:
            return
        for w in self.solutions:
            w[self.answer_lang][SCORE_PREFIX] = self.model.dead_pt
        self.model.save_glossary(self.gloss)
        self.message = "Set max points."
        self._advance_to_next_word()

    def command_boost(self) -> None:
        if not self.solutions:
            return
        for w in self.solutions:
            w[self.answer_lang][SCORE_PREFIX] = self.model.boost_pt
        self.model.save_glossary(self.gloss)
        self.message = f"Boosted to {self.model.boost_pt}."
        self.done = True

    def stop(self) -> None:
        self.done = True
        self.ended_by_user = True
        self.message = "Stopped."

    def submit(self, text: str) -> None:
        if self.done or not self.cur_word:
            return

        if self.awaiting_ok:
            # UI must call acknowledge_ok()
            return

        text = (text or "").strip()
        self.last_was_close = False

        def _normalize_for_compare(s: str) -> str:
            # Prevent false negatives from NFC/NFD differences (common on mobile keyboards)
            # and from spacing around separators like commas.
            s = unicodedata.normalize("NFC", s)
            s = s.casefold()
            s = re.sub(r"\s+", " ", s).strip()
            s = re.sub(r"\s*([,;/])\s*", r"\1", s)
            return s

        def _variants(answer: str) -> List[str]:
            ans = str(answer or "")
            norm_full = _normalize_for_compare(ans)
            out: List[str] = [norm_full]
            # If the stored answer contains multiple alternatives separated by comma/;/,
            # accept any individual alternative as correct.
            parts = [p.strip() for p in re.split(r"[,;/]", ans) if p.strip()]
            if len(parts) > 1:
                out.extend(_normalize_for_compare(p) for p in parts)
            # Deduplicate while preserving order
            seen = set()
            uniq: List[str] = []
            for v in out:
                if v not in seen:
                    seen.add(v)
                    uniq.append(v)
            return uniq

        given_norm = _normalize_for_compare(text)

        # handle special commands from UI if user typed them
        if text == "#":
            self.stop()
            return
        if text == "@":
            self.command_max_points()
            return
        if text == "*":
            self.command_boost()
            return

        # Detail stage
        if self.detail_items and self.to_change is not None:
            detail_key, detail_solution = self.detail_items[self.detail_i]
            ctx_q = self.cur_word[self.question_lang].get(WORD_PREFIX, "")
            ctx_t = str(self.cur_word[self.answer_lang].get(TYPE_PREFIX) or "")
            ctx_prefix = f"{ctx_t} {ctx_q}".strip()
            detail_label = (
                f"{ctx_prefix} · {detail_key}" if ctx_prefix else str(detail_key)
            )

            expected_str = str(detail_solution)
            if given_norm in _variants(expected_str):
                self.to_change[SCORE_PREFIX] = (
                    int(self.to_change.get(SCORE_PREFIX, 0)) + 1
                )
                self.correct_pt += 1
                self.model.save_glossary(self.gloss)
                self.message = "Correct detail."
                self.history_items.append(
                    {
                        "label": detail_key,
                        "given": text,
                        "expected": expected_str,
                        "correct": True,
                    }
                )
                self._append_total_history(
                    label=detail_label,
                    given=text,
                    expected=expected_str,
                    correct=True,
                )
            else:
                # Close-but-wrong: don't penalize, let the user try again.
                # This matches the legacy CLI behavior.
                for expected_norm in _variants(expected_str):
                    if self.model.similar(given_norm, expected_norm):
                        self.message = self.text.close_but_wrong
                        self.last_was_close = True
                        return
                self.to_change[SCORE_PREFIX] = (
                    int(self.to_change.get(SCORE_PREFIX, 0)) - 1
                )
                self.incorrect_pt += 1
                self.model.save_glossary(self.gloss)
                self.message = "Incorrect detail."
                self.history_items.append(
                    {
                        "label": detail_key,
                        "given": text,
                        "expected": expected_str,
                        "correct": False,
                    }
                )
                self._append_total_history(
                    label=detail_label,
                    given=text,
                    expected=expected_str,
                    correct=False,
                )

                # If this word comes from a <showtype>: true branch (stored as <type>),
                # then failing the FIRST detail should immediately skip the rest.
                if (
                    self.detail_i == 0
                    and self.cur_word
                    and (TYPE_PREFIX in self.cur_word.get(self.answer_lang, {}))
                ):
                    self.detail_items = []
                    self.detail_i = 0
                    self.to_change = None
                    preserve = self.message
                    self._advance_to_next_word()
                    if not self.done:
                        self.message = preserve
                    return

            # next detail or next word
            if self.detail_i + 1 < len(self.detail_items):
                self.detail_i += 1
                return

            self.detail_items = []
            self.detail_i = 0
            self.to_change = None
            self._advance_to_next_word()
            return

        # Word stage
        match = None
        type_mismatch = False
        for sol in self.solutions:
            expected_word = str(sol[self.answer_lang].get(WORD_PREFIX, ""))
            if given_norm not in _variants(expected_word):
                continue
            # type matching like CLI
            cur_type = self.cur_word[self.answer_lang].get(TYPE_PREFIX)
            sol_type = sol[self.answer_lang].get(TYPE_PREFIX)
            if (TYPE_PREFIX not in sol[self.answer_lang]) or (sol_type == cur_type):
                match = sol
                break
            type_mismatch = True

        if match is not None:
            try:
                self._stats["words_practiced"] = (
                    int(self._stats.get("words_practiced", 0)) + 1
                )
            except Exception:
                pass
            self.to_change = match[self.answer_lang]
            self.to_change[SCORE_PREFIX] = int(self.to_change.get(SCORE_PREFIX, 0)) + 1
            self.correct_pt += 1
            self.model.save_glossary(self.gloss)

            self.last_word_given = text
            self.history_items = [
                {
                    "label": f"{self.cur_word[self.question_lang][WORD_PREFIX]} → {self.answer_lang}",
                    "given": text,
                    "expected": text,
                    "correct": True,
                }
            ]

            ctx_q = self.cur_word[self.question_lang].get(WORD_PREFIX, "")
            ctx_t = str(self.cur_word[self.answer_lang].get(TYPE_PREFIX) or "")
            word_label = f"{ctx_t} {ctx_q}".strip()
            word_label = (
                f"{word_label} – {self.answer_lang}"
                if word_label
                else f"{ctx_q} – {self.answer_lang}"
            )

            self._append_total_history(
                label=word_label,
                given=text,
                expected=text,
                correct=True,
            )

            # Prepare detail prompts
            self.detail_items = [
                (k, v)
                for k, v in self.to_change.items()
                if k not in (SCORE_PREFIX, WORD_PREFIX, TYPE_PREFIX)
            ]
            self.detail_i = 0

            if not self.detail_items:
                self._advance_to_next_word()
            else:
                self.message = "Correct. Enter details."
            return

        # Close-but-wrong word: don't penalize, don't advance.
        for sol in self.solutions:
            expected_word = str(sol[self.answer_lang].get(WORD_PREFIX, ""))
            for expected_norm in _variants(expected_word):
                if self.model.similar(given_norm, expected_norm):
                    self.message = self.text.close_but_wrong
                    self.last_was_close = True
                    return

        if type_mismatch:
            try:
                self._stats["words_practiced"] = (
                    int(self._stats.get("words_practiced", 0)) + 1
                )
            except Exception:
                pass
            # Treat as incorrect (type mismatch) and move on.
            for sol in self.solutions:
                sol[self.answer_lang][SCORE_PREFIX] = (
                    int(sol[self.answer_lang].get(SCORE_PREFIX, 0)) - 1
                )
            self.incorrect_pt += 1
            self.model.save_glossary(self.gloss)
            self.message = "Incorrect word (type mismatch)."

            ctx_q = self.cur_word[self.question_lang].get(WORD_PREFIX, "")
            ctx_t = str(self.cur_word[self.answer_lang].get(TYPE_PREFIX) or "")
            word_label = f"{ctx_t} {ctx_q}".strip()
            word_label = (
                f"{word_label} → {self.answer_lang}"
                if word_label
                else f"{ctx_q} → {self.answer_lang}"
            )
            self._append_total_history(
                label=word_label,
                given=text,
                expected=", ".join(self.solution_words),
                correct=False,
            )

            self._advance_to_next_word()
            return

        # wrong (or close-but-wrong) word
        try:
            self._stats["words_practiced"] = (
                int(self._stats.get("words_practiced", 0)) + 1
            )
        except Exception:
            pass
        for sol in self.solutions:
            sol[self.answer_lang][SCORE_PREFIX] = (
                int(sol[self.answer_lang].get(SCORE_PREFIX, 0)) - 1
            )
        self.incorrect_pt += 1
        self.model.save_glossary(self.gloss)
        self.message = "Incorrect word."

        ctx_q = self.cur_word[self.question_lang].get(WORD_PREFIX, "")
        ctx_t = str(self.cur_word[self.answer_lang].get(TYPE_PREFIX) or "")
        word_label = f"{ctx_t} {ctx_q}".strip()
        word_label = (
            f"{word_label} – {self.answer_lang}"
            if word_label
            else f"{ctx_q} – {self.answer_lang}"
        )

        self._append_total_history(
            label=word_label,
            given=text,
            expected=", ".join(self.solution_words),
            correct=False,
        )

        # Immediately move on (history shows the correct solution).
        self._advance_to_next_word()
