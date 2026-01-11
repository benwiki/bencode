from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import reduce
from random import random, shuffle
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import json
import os
import sys


class Kit(Enum):
    """Defines the available language kit configurations."""

    LATIN = "kits/kit_latin.json"

    def load_config(self) -> dict:
        try:
            with open(self.value, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(
                f"ERROR: Kit file {self.value} not found. Using empty kit.",
                file=sys.stderr,
            )
            return {}
        except json.JSONDecodeError:
            print(
                f"ERROR: Kit file {self.value} has invalid JSON. Using empty kit.",
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


def build_prompt_tree(kit: Any, *, label: Optional[str] = None, showtype: Optional[str] = None) -> Tuple[PromptNode, ...]:
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

        # If <showtype> is set, the selected type from the parent choice is stored in "<type>"
        if kit.get("<showtype>") and showtype:
            # Hidden output; no UI field needed. We'll store it when collecting.
            children.append(GroupNode(label="<type>", children=tuple()))

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
                option_children[opt] = build_prompt_tree(opt_val, label=opt, showtype=opt)

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


def collect_prompt_data(nodes: Iterable[PromptNode], *, selections: Dict[str, str], inputs: Dict[str, str], showtype: Optional[str] = None) -> Dict[str, Any]:
    """Collects user entries into the flat dict format used by word entries."""

    data: Dict[str, Any] = {}

    for node in nodes:
        if isinstance(node, InputNode):
            if node.key in inputs:
                data[node.key] = inputs[node.key]
        elif isinstance(node, GroupNode):
            if node.label == "<type>" and showtype:
                data["<type>"] = showtype
            else:
                data.update(collect_prompt_data(node.children, selections=selections, inputs=inputs, showtype=showtype))
        elif isinstance(node, ChoiceNode):
            sel = selections.get(node.label, node.default)
            # If this choice node itself stores <type>
            if node.showtype_here:
                data["<type>"] = sel
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

    def __init__(self, kit: Kit, *, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.getcwd()

        self.kit = kit.load_config()
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
            if isinstance(props, dict) and props.get("<type>") == langtype:
                return lang
        raise ValueError(f"No language with <type>={langtype} in kit")

    def _path(self, filename: str) -> str:
        return os.path.join(self.base_dir, filename)

    def load_all(self) -> None:
        self.load_glossaries()
        self.load_words()

    def load_glossaries(self) -> None:
        path = self._path("glossaries.txt")
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8"):
                pass
        with open(path, "r", encoding="utf-8") as f:
            self.glossaries = [line.strip() for line in f if line.strip()]

    def _parse_word_file(self, gloss: str) -> List[Dict[str, Dict[str, Any]]]:
        file_path = self._path(gloss + ".txt")
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
                        if raw.isnumeric() or (raw.startswith("-") and raw[1:].isnumeric()):
                            items[key] = int(raw)
                        else:
                            items[key] = raw
                    entry[lang_name] = items

                # Ensure required keys exist
                for lang_name in self.languages[:2]:
                    entry.setdefault(lang_name, {})
                    entry[lang_name].setdefault("szo", "")
                    entry[lang_name].setdefault("pont", 0)

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
        file_path = self._path(gloss + ".txt")
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
        if gloss in self.glossaries:
            raise ValueError("Glossary already exists")

        with open(self._path("glossaries.txt"), "a", encoding="utf-8") as f:
            f.write(gloss + "\n")
        with open(self._path(gloss + ".txt"), "w", encoding="utf-8"):
            pass
        self.glossaries.append(gloss)
        self.words[gloss] = []
        self.all_words = reduce(lambda a, b: a + b, self.words.values(), [])

    def find(self, word: str, lang: str, gloss: Optional[str] = None, prop: Optional[str] = None):
        source = self.words[gloss] if gloss is not None else self.all_words
        out = []
        for w in source:
            if w.get(lang, {}).get("szo") == word:
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

    def similar(self, s1: str, s2: str) -> bool:
        len1, len2 = len(s1), len(s2)
        if len2 == 0 and len1 == 0:
            return True
        if len1 == 0 or len2 == 0:
            return False
        score = self.similarity(s1, s2)
        print(f"Similarity score: {score} (given length: {len1}, correct length: {len2})")
        return max(len2 - score, len1 - score) <= 2

    def get_questionlang(self, answer_lang: str) -> str:
        return self.mlang if answer_lang == self.learnlang else self.learnlang

    def get_practice_words(self, answer_lang: str, gloss: str) -> List[Dict[str, Dict[str, Any]]]:
        practice_words = list(self.words[gloss])
        for word in self.words[gloss]:
            wordscore = int(word[answer_lang].get("pont", 0))
            if wordscore < self.lower_boundary:
                for _ in range(abs(wordscore - self.lower_boundary)):
                    practice_words.append(word)
        shuffle(practice_words)
        return practice_words

    def add_word(self, gloss: str, mword: str, lword: str, *, mprops: Optional[Dict[str, Any]] = None, lprops: Optional[Dict[str, Any]] = None) -> None:
        if gloss not in self.words:
            raise ValueError("Unknown glossary")
        mprops = mprops or {}
        lprops = lprops or {}

        self.words[gloss].append(
            {
                self.mlang: {"szo": mword, "pont": 0, **mprops},
                self.learnlang: {"szo": lword, "pont": 0, **lprops},
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

    def __init__(self, model: VocabLearnerModel, *, gloss: str, answer_lang: str):
        self.model = model
        self.gloss = gloss
        self.answer_lang = answer_lang
        self.question_lang = model.get_questionlang(answer_lang)

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
        # Total history across the whole session (words + details)
        self.total_history_items: List[Dict[str, Any]] = []
        self.last_word_given: Optional[str] = None

        self.done = False
        self.ended_by_user = False
        self.message = ""

        self._advance_to_next_word()

    def _append_total_history(self, *, label: str, given: str, expected: str, correct: bool) -> None:
        self.total_history_items.append(
            {"label": label, "given": given, "expected": expected, "correct": bool(correct)}
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
                lines.append(f"{mark} {label}: {given}  [color=888888](Correct: {expected})[/color]")
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

            # compute effective score like CLI (pont divided by detail count)
            len_detail = len([k for k in w[self.answer_lang] if k not in ("szo", "pont", "<type>")])
            wordscore = int(w[self.answer_lang].get("pont", 0)) // max(1, len_detail)

            if wordscore >= self.model.dead_pt:
                continue
            if wordscore > self.model.upper_boundary and random() < (
                (wordscore - self.model.upper_boundary) / (self.model.dead_pt - self.model.upper_boundary)
            ):
                continue

            self.cur_word = w
            self.solutions = self.model.find(w[self.question_lang]["szo"], self.question_lang, self.gloss)
            self.solution_words = [s[self.answer_lang]["szo"] for s in self.solutions]
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

        q = self.cur_word[self.question_lang]["szo"]
        t = self.cur_word[self.answer_lang].get("<type>")
        if t:
            q = f"{t}\n{q}"
        return ("word", q)

    def current_type(self) -> str:
        if not self.cur_word:
            return ""
        return str(self.cur_word[self.answer_lang].get("<type>") or "")

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
            w[self.answer_lang]["pont"] = self.model.dead_pt
        self.model.save_glossary(self.gloss)
        self.message = "Set max points."
        self._advance_to_next_word()

    def command_boost(self) -> None:
        if not self.solutions:
            return
        for w in self.solutions:
            w[self.answer_lang]["pont"] = self.model.boost_pt
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
            ctx_q = self.cur_word[self.question_lang].get("szo", "")
            ctx_t = str(self.cur_word[self.answer_lang].get("<type>") or "")
            ctx_prefix = f"{ctx_t} {ctx_q}".strip()
            detail_label = f"{ctx_prefix} · {detail_key}" if ctx_prefix else str(detail_key)

            if text == detail_solution:
                self.to_change["pont"] = int(self.to_change.get("pont", 0)) + 1
                self.correct_pt += 1
                self.model.save_glossary(self.gloss)
                self.message = "Correct detail."
                self.history_items.append(
                    {
                        "label": detail_key,
                        "given": text,
                        "expected": detail_solution,
                        "correct": True,
                    }
                )
                self._append_total_history(
                    label=detail_label,
                    given=text,
                    expected=str(detail_solution),
                    correct=True,
                )
            else:
                self.to_change["pont"] = int(self.to_change.get("pont", 0)) - 1
                self.incorrect_pt += 1
                self.model.save_glossary(self.gloss)
                self.message = "Incorrect detail."
                self.history_items.append(
                    {
                        "label": detail_key,
                        "given": text,
                        "expected": detail_solution,
                        "correct": False,
                    }
                )
                self._append_total_history(
                    label=detail_label,
                    given=text,
                    expected=str(detail_solution),
                    correct=False,
                )

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
        if text in self.solution_words:
            # Find the exact solution entry to modify
            match = None
            for sol in self.solutions:
                if sol[self.answer_lang]["szo"] == text:
                    # type matching like CLI
                    cur_type = self.cur_word[self.answer_lang].get("<type>")
                    sol_type = sol[self.answer_lang].get("<type>")
                    if ("<type>" not in sol[self.answer_lang]) or (sol_type == cur_type):
                        match = sol
                        break

            if match is None:
                # Treat as incorrect (type mismatch) and move on.
                for sol in self.solutions:
                    sol[self.answer_lang]["pont"] = int(sol[self.answer_lang].get("pont", 0)) - 1
                self.incorrect_pt += 1
                self.model.save_glossary(self.gloss)
                self.message = "Incorrect word (type mismatch)."

                ctx_q = self.cur_word[self.question_lang].get("szo", "")
                ctx_t = str(self.cur_word[self.answer_lang].get("<type>") or "")
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

            self.to_change = match[self.answer_lang]
            self.to_change["pont"] = int(self.to_change.get("pont", 0)) + 1
            self.correct_pt += 1
            self.model.save_glossary(self.gloss)

            self.last_word_given = text
            self.history_items = [
                {
                    "label": f"{self.cur_word[self.question_lang]['szo']} → {self.answer_lang}",
                    "given": text,
                    "expected": text,
                    "correct": True,
                }
            ]

            ctx_q = self.cur_word[self.question_lang].get("szo", "")
            ctx_t = str(self.cur_word[self.answer_lang].get("<type>") or "")
            word_label = f"{ctx_t} {ctx_q}".strip()
            word_label = f"{word_label} – {self.answer_lang}" if word_label else f"{ctx_q} – {self.answer_lang}"

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
                if k not in ("pont", "szo", "<type>")
            ]
            self.detail_i = 0

            if not self.detail_items:
                self._advance_to_next_word()
            else:
                self.message = "Correct. Enter details."
            return

        # wrong (or close-but-wrong) word
        for sol in self.solutions:
            sol[self.answer_lang]["pont"] = int(sol[self.answer_lang].get("pont", 0)) - 1
        self.incorrect_pt += 1
        self.model.save_glossary(self.gloss)
        self.message = "Incorrect word."

        ctx_q = self.cur_word[self.question_lang].get("szo", "")
        ctx_t = str(self.cur_word[self.answer_lang].get("<type>") or "")
        word_label = f"{ctx_t} {ctx_q}".strip()
        word_label = f"{word_label} – {self.answer_lang}" if word_label else f"{ctx_q} – {self.answer_lang}"

        self._append_total_history(
            label=word_label,
            given=text,
            expected=", ".join(self.solution_words),
            correct=False,
        )

        # Immediately move on (history shows the correct solution).
        self._advance_to_next_word()
