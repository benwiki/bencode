from random import shuffle, random
from functools import reduce
from enum import Enum
import json
import os
import sys
from langtext import Lang, LangText  # Import all language text classes
from langgen import generate_language_setup

# -------------------------------
KIT_GERMAN = {
    "<mode>": "apart",  # mode: apart / both (should the points be counted for both languages or separately)
    "magyar": {
        "<type>": "mothertongue",
    },
    "német": {
        "<type>": "learninglang",
        "<mode>": "and",
        "szófaj": {
            "<mode>": "or",
            "főnév": {
                "<mode>": "and",
                "névelő": None,
                "tbsz": None,
                "gyenge": None,
            },
            "ige": {
                "<mode>": "and",
                "präteritum": None,
                "pp_időbeli_segédige": None,
                "pp": None,
            },
            "melléknév": {
                "<mode>": "and",
                "közép": None,
                "felső": None,
            },
            "névmás": {
                "<mode>": "and",
                "nőnem": None,
                "semleges nem": None,
            },
            "kifejezés": None,
        },
    },
}


########################################################
def main():
    generate_language_setup()
    tan = NyelvTanulas(Kit.LATIN)
    tan.start()


########################################################


class Kit(Enum):
    """Defines the available language kit configurations."""

    # We now only need one entry pointing to the new multi-language kit
    LATIN = "assets/kits/kit_latin.json"

    def load_config(self):
        """Loads the configuration dictionary from the associated JSON file."""
        try:
            path = self.value
            if not os.path.isabs(path):
                path = os.path.join(os.path.dirname(__file__), path)
            with open(path, "r", encoding="utf-8") as f:
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


class NyelvTanulas:
    lower_boundary = 0
    upper_boundary = 5
    dead_pt = 15
    boost_pt = -10
    auto_continue_practice = True

    running = True

    def __init__(self, kit: Kit, lang: Lang = Lang.ENGLISH):
        self.kit = kit.load_config()
        self.text = lang.text()
        self.mlang = self.get_lang("mothertongue")
        self.learnlang = self.get_lang("learninglang")
        self.languages = [
            self.mlang,
            self.learnlang,
        ]
        """[
                    self.text.menu_practice,
                    self.text.menu_add_words,
                    self.text.menu_create_dictionaries,
                    self.text.menu_check_progress,
                    self.text.menu_settings,
                    self.text.menu_exit,
                    self.text.menu_word_search,
                ]"""
        self.commands = {
            self.text.menu_practice: self.practice,
            self.text.menu_add_words: self.add_new,
            self.text.menu_create_dictionaries: self.add_glossary,
            self.text.menu_check_progress: self.state,
            self.text.menu_settings: self.settings,
            self.text.menu_exit: self.out,
            self.text.menu_word_search: self.find_similar,
        }

        try:
            with open("glossaries.txt", "r", encoding="utf-8") as glossfile:
                self.glossaries = [gloss.strip() for gloss in glossfile]

            self.words = {}
            for gloss in self.glossaries:
                try:
                    with open(gloss + ".txt", "r", encoding="utf-8") as file:
                        temp = [
                            [
                                [
                                    [
                                        (
                                            int(c.strip())
                                            if c.strip().isnumeric()
                                            or c[1:].strip().isnumeric()
                                            else c.strip()
                                        )
                                        for c in comp.split(":")
                                    ]
                                    for comp in lang.split(" ; ")
                                ]
                                for lang in line.split(" | ")
                            ]
                            for line in file
                        ]

                        self.words[gloss] = [
                            {
                                self.languages[i]: {key: val for key, val in word[i]}
                                for i in range(2)
                            }
                            for word in temp
                        ]
                except FileNotFoundError as e:
                    file = open(gloss + ".txt", "w")
                    file.close()
                    self.words[gloss] = []
                except Exception as e:
                    print(e, self.text.error_reading_glossary.format(gloss))
                    self.words[gloss] = []

            self.all_words = reduce(lambda a, b: a + b, self.words.values())

            self.check_for_doubles()
            self.check_for_glossary_length()

        except FileNotFoundError as e:
            file = open("glossaries.txt", "w")
            file.close()
            self.words = {}
        except Exception as e:
            print(e, self.text.error_opening_glossaries)
            self.words = {}

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_lang(self, langtype: str):
        assert langtype in ["mothertongue", "learninglang"], "Wrong type!"
        for lang, props in self.kit.items():
            if lang == "<mode>":
                continue
            if props.get("<type>") == langtype:
                return lang

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start(self):
        while self.running:
            whattodo = self.correct_input(
                self.text.menu,
                values=list(self.commands),
                numbered=True,
            )
            self.commands[whattodo]()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def out(self):
        confirm = input(self.text.goodbye)
        self.running = False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def settings(self):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def correct_input(
        self,
        string,
        mytype=None,
        values=None,
        segment=True,
        numbered=False,
        default=None,
    ):

        if numbered:
            answer = input(
                f"{string}\n"
                + "\n".join(f"{i+1}. {val}" for i, val in enumerate(values))
                + "\n"
                + self.text.choose_number.format(1, len(values))
            )
            mytype = int
            segment = False
            if default is not None and answer == "":
                assert (
                    isinstance(default, int)
                    and -(len(values) - 1) <= default <= len(values) - 1
                )
                return values[default]
        else:
            answer = input(string)
        while True:
            try:
                answer = mytype(answer)
                if numbered and 1 <= answer <= len(values):
                    return values[answer - 1]
                elif answer in values:
                    return answer
                elif segment:
                    starts = [
                        val
                        for val in values
                        if isinstance(val, str) and val.startswith(answer)
                    ]
                    if len(starts) > 1:
                        print(
                            self.text.multiple_options_error.format(", ".join(starts))
                        )
                    elif len(starts) == 1:
                        return starts[0]
            except Exception as e:
                print(
                    e, self.text.conversion_error.format("Konverziós", "correct_input")
                )
            input(self.text.invalid_input_prompt)
            answer = input(string)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def practice(self):
        gloss = self.correct_input(
            self.text.which_glossary.format("\n - ".join(self.glossaries)),
            str,
            self.glossaries,
        )

        if len(self.words) == 0 or len(self.words[gloss]) == 0:
            print(self.text.nothing_to_practice)
            return
        lang = self.correct_input(
            self.text.practice_mode_select.format(
                self.mlang, self.learnlang, self.mlang, self.learnlang
            ),
            str,
            self.languages,
        )
        questionlang = self.get_questionlang(lang)
        correct_pt, incorrect_pt = 0, 0

        first = True
        while first or self.auto_continue_practice:
            first = False

            dead = 0
            to_break = False
            practice_words = self.get_practice_words(lang, gloss)
            for cur_word in practice_words:
                len_detail = len(
                    [
                        detail
                        for detail in cur_word[lang]
                        if detail not in ("szo", "pont", "<type>")
                    ]
                )
                wordscore = cur_word[lang]["pont"] // max(1, len_detail)
                if wordscore >= self.dead_pt:
                    dead += 1
                    continue
                if wordscore > self.upper_boundary and random() < (
                    wordscore - self.upper_boundary
                ) / (self.dead_pt - self.upper_boundary):
                    continue

                done = False
                solutions = self.find(
                    cur_word[questionlang]["szo"], questionlang, gloss
                )
                solution_words = [word[lang]["szo"] for word in solutions]

                answer = self.ask_word(cur_word, lang)
                if answer == "#":
                    break
                elif answer == "@":
                    for word in solutions:
                        word[lang]["pont"] = self.dead_pt
                    confirm = input(
                        self.text.max_points_confirm.format(", ".join(solution_words))
                    )
                    continue
                elif answer == "*":
                    for word in solutions:
                        word[lang]["pont"] = self.boost_pt
                    confirm = input(
                        self.text.boosted_confirm.format(
                            ", ".join(solution_words), str(self.boost_pt)
                        )
                    )
                    break

                while (
                    answer in solution_words
                    and list(
                        filter(
                            lambda x: x[lang]["szo"] == answer
                            and "<type>" not in x[lang]
                            or x[lang]["<type>"] == cur_word[lang]["<type>"],
                            solutions,
                        )
                    )[0][lang]["pont"]
                    >= self.dead_pt
                ):
                    confirm = input(self.text.already_learned)
                    answer = self.ask_word(cur_word, lang)

                while answer not in solution_words and any(
                    self.similar(answer, m) for m in solution_words
                ):
                    confirm = input(self.text.close_but_wrong)
                    answer = self.ask_word(cur_word, lang)

                if answer in solution_words:
                    to_change = list(
                        filter(
                            lambda x: x[lang]["szo"] == answer
                            and "<type>" not in x[lang]
                            or x[lang]["<type>"] == cur_word[lang]["<type>"],
                            solutions,
                        )
                    )[0][lang]
                    to_change["pont"] += 1
                    correct_pt += 1
                    self.save(gloss)
                    details = ""
                    if len(solutions) > 1:
                        details = " " + self.text.details_separator.format(
                            ", ".join(w for w in solution_words if w != answer)
                        )
                    confirm = input(self.text.correct_answer + details)

                    if to_change["pont"] >= self.dead_pt:
                        confirm = input(self.text.max_points_word_complete)
                        done = True

                    for detail, detail_solution in to_change.items():
                        if detail not in ("pont", "szo", "<type>"):
                            answer = input(f"{detail}: ")
                            if answer == "#":
                                to_break = True
                                break
                            elif answer == "@":
                                for word in solutions:
                                    word[lang]["pont"] = self.dead_pt
                                confirm = input(
                                    self.text.max_points_confirm.format(
                                        ", ".join(solution_words)
                                    )
                                )
                                break
                            elif answer == "*":
                                for word in solutions:
                                    word[lang]["pont"] = self.boost_pt
                                confirm = input(
                                    self.text.boosted_confirm.format(
                                        ", ".join(solution_words), self.boost_pt
                                    )
                                )
                                to_break = True
                                break

                            while answer != detail_solution and self.similar(
                                answer, detail_solution
                            ):
                                confirm = input(self.text.close_but_wrong)
                                answer = input(f"{detail}: ")

                            if answer == detail_solution:
                                to_change["pont"] += 1
                                correct_pt += 1
                                self.save(gloss)
                                confirm = input(self.text.correct_detail)
                                if not done and to_change["pont"] == self.dead_pt:
                                    confirm = input(self.text.max_points_word_complete)
                            else:
                                to_change["pont"] -= 1
                                incorrect_pt += 1
                                self.save(gloss)
                                confirm = input(
                                    self.text.incorrect_detail.format(detail_solution)
                                )
                        if to_break:
                            break
                else:
                    for word in solutions:
                        word[lang]["pont"] -= 1
                    incorrect_pt += 1
                    self.save(gloss)
                    confirm = input(
                        self.text.incorrect_word.format(", ".join(solution_words))
                    )

                self.save(gloss)

            else:
                if dead == len(practice_words):
                    print(self.text.all_done)
                    break
                continue
            break  # flag: ha kilépek, vagy ha mind "meghaltak" a szavaim, a while-ból is kilép

        if correct_pt + incorrect_pt > 0:
            ratio = int(correct_pt / (correct_pt + incorrect_pt) * 10000) / 100
            confirm = input(self.text.summary.format(correct_pt, incorrect_pt, ratio))
        self.save(gloss)

    def ask_word(self, cur_word, lang):
        questionlang = self.get_questionlang(lang)
        q = "\n" + cur_word[questionlang]["szo"] + ": "
        if cur_word[lang].get("<type>"):
            q = f"\n{cur_word[lang]['<type>']}{q}"
        return input(q)

    def get_questionlang(self, lang):
        return self.mlang if lang == self.learnlang else self.learnlang

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_practice_words(self, lang, gloss):
        practice_words = list(self.words[gloss])
        for word in self.words[gloss]:
            wordscore = word[lang]["pont"]
            if wordscore < self.lower_boundary:
                for i in range(
                    abs(wordscore - self.lower_boundary)
                ):  # minden mínuszpont egy további kérdezést jelent. Boost mode.
                    practice_words.append(word)
        shuffle(practice_words)
        return practice_words

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find(self, word, lang, gloss=None, property=None):
        return [
            w if property is None else w[lang][property]
            for w in (self.words[gloss] if gloss is not None else self.all_words)
            if w[lang]["szo"] == word
        ]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similarity(self, given: str, correct: str) -> float:
        ##        given, correct = given.lower(), correct.lower()
        ##        return ( len(given)==len(correct) and sum(1 for L in given  if L in correct) >= len(correct)-strength ) or ( 0 < abs(len(given)-len(correct)) <= strength and all(L in correct for L in given) )
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
                will_g, will_c = -1, -1  # the indexes I want to search
                chan_g, chan_c = g, c  # the indexes I use for that, they CHANge
                while chan_g < glen:
                    try:
                        will_c = correct.index(given[chan_g], c + 1)
                    except ValueError:
                        chan_g += 1
                    except Exception as e:
                        print(e, self.text.conversion_error.format("Saját", "similar"))
                    else:
                        break
                while chan_c < clen:
                    try:
                        will_g = given.index(correct[chan_c], g + 1)
                    except ValueError:
                        chan_c += 1
                    except Exception as e:
                        print(e, self.text.conversion_error.format("Saját", "similar"))
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

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similar(self, given: str, correct: str, strength=1) -> bool:
        glen, clen = len(given), len(correct)
        if glen == 0 and clen > 0 or clen == 0 and glen > 0:
            return False
        elif clen == 0 and glen == 0:
            return True

        score = self.similarity(given, correct)
        result = (score / clen + score / glen) / 2
        return result > 0.8

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find_similar(self):
        word = input(self.text.enter_expression)
        lang = self.correct_input(
            self.text.what_language.format(self.mlang, self.learnlang),
            str,
            [self.mlang, self.learnlang],
        )
        print(self.text.similar_words_title)
        got = False
        otherlang = self.mlang if lang == self.learnlang else self.learnlang
        garage = []
        for glossname, gloss in self.words.items():
            for w in gloss:
                langitems = [
                    f"{key}:{val}"
                    for key, val in w[lang].items()
                    if key != "szo" and key != "pont"
                ]
                otherlangitems = [
                    f"{key}:{val}"
                    for key, val in w[otherlang].items()
                    if key != "szo" and key != "pont"
                ]
                garage.append(
                    [
                        self.similarity(w[lang]["szo"], word),
                        f" - {w[lang]['szo']} ({w[lang]['pont']} pt) {', '.join(langitems)}"
                        f" = {w[otherlang]['szo']} ({w[otherlang]['pont']} pt) {', '.join(otherlangitems)} [a {glossname} szótárban]",
                    ]
                )

        s = list(reversed(sorted(garage, key=lambda k: k[0])))
        for i in range(10):
            print(s[i][1])
        confirm = input(self.text.done_message)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_new(self):
        print(self.text.add_words_title)
        gloss = self.correct_input(
            self.text.which_glossary.format("\n - ".join(self.glossaries)),
            str,
            self.glossaries,
        )

        while True:
            add_mlang = input(self.text.enter_mlang_word.format(self.mlang))
            if add_mlang == "#":
                break

            q_gloss = self.text.word_in_current_glossary.format(
                f"{self.text.yes_char.upper()}/{self.text.no_char}"
            )
            q_any = self.text.word_in_any_glossary.format(
                f"{self.text.yes_char.upper()}/{self.text.no_char}"
            )
            if len(self.find(add_mlang, self.mlang, gloss)) > 0:
                if input(f"{q_gloss}: ").lower() == self.text.no_char:
                    continue
            elif len(self.find(add_mlang, self.mlang)) > 0:  # global search
                if input(f"{q_any}: ").lower() == self.text.no_char:
                    continue

            add_learnlang = input(self.text.enter_learnlang_word.format(self.learnlang))
            if add_learnlang == "#":
                break

            if len(self.find(add_learnlang, self.learnlang, gloss)) > 0:
                if input(f"{q_gloss}: ").lower() == self.text.no_char:
                    continue
            elif len(self.find(add_learnlang, self.learnlang)) > 0:  # global search
                if input(f"{q_any}: ").lower() == self.text.no_char:
                    continue

            mlang_kit, learnlang_kit = self.add_kit_properties(self.kit)

            self.words[gloss].append(
                {
                    self.mlang: {"szo": add_mlang, "pont": 0, **mlang_kit},
                    self.learnlang: {"szo": add_learnlang, "pont": 0, **learnlang_kit},
                }
            )
            self.save(gloss)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_glossary(self):
        print(self.text.add_glossaries_title)

        while True:
            gloss = input(self.text.enter_glossary_name)
            while gloss in self.glossaries:
                gloss = input(self.text.glossary_exists)
            if gloss == "#":
                break
            with open("glossaries.txt", "a", encoding="utf-8") as glossfile:
                glossfile.write(gloss + "\n")
            with open(gloss + ".txt", "w", encoding="utf-8"):
                pass
            self.glossaries.append(gloss)
            self.words[gloss] = []
            confirm = input(self.text.successfully_added)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save(self, gloss):
        file = open(gloss + ".txt", "w", encoding="utf-8")
        for word in self.words[gloss]:
            file.write(
                " | ".join(
                    " ; ".join(f"{key}:{val}" for key, val in lang.items())
                    for lang in word.values()
                )
                + "\n"
            )
        file.close()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def state(self):
        sz_vagy_ossz = self.correct_input(
            self.text.check_state_type.format(
                self.text.state_options[0], self.text.state_options[1]
            ),
            str,
            self.text.state_options,
        )

        if sz_vagy_ossz == self.text.state_options[0]:  # Specific dictionary
            gloss = self.correct_input(
                self.text.which_glossary.format("\n - ".join(self.glossaries)),
                str,
                self.glossaries,
            )
            words_to_check = self.words[gloss]
        else:  # All dictionaries
            words_to_check = self.all_words

        osszes = len(words_to_check)
        if osszes == 0:
            print(self.text.nothing_to_practice)
            return

        telj = sum(
            1
            for sz in words_to_check
            if sz[self.mlang]["pont"] >= self.dead_pt
            or sz[self.learnlang]["pont"] >= self.dead_pt
        )
        ratio = int(telj / osszes * 10000) / 100
        print(self.text.state_summary.format(osszes, telj, ratio))
        details = self.correct_input(
            self.text.state_details_prompt.format(self.text.yes_no_options),
            str,
            self.text.yes_no_options,
        )
        if details == self.text.no_char:
            return
        whichlang = self.correct_input(
            self.text.state_which_lang.format(self.mlang, self.learnlang),
            str,
            (self.mlang, self.learnlang),
        )
        by_score = {}
        for sz in words_to_check:
            score = sz[whichlang]["pont"]
            try:
                by_score[score].append(sz[whichlang]["szo"])
            except:
                by_score[score] = []
                by_score[score].append(sz[whichlang]["szo"])
        for score, words in reversed(sorted(by_score.items(), key=lambda k: k[0])):
            print("\n", end="")
            print(self.text.state_score_group.format(score, len(words)))
            for sz in words:
                print("-", sz)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_kit_properties(self, kit=None, showtype=None):
        if kit is None:
            return ({}, {})
        if len(kit) == 0 or "<mode>" not in kit:
            return {}

        if kit["<mode>"] == "apart":
            return (
                self.add_kit_properties(kit[self.mlang]),
                self.add_kit_properties(kit[self.learnlang]),
            )
        elif kit["<mode>"] == "both":
            pass

        elif kit["<mode>"] == "and":
            data = {"<type>": showtype} if kit.get("<showtype>") else {}
            for key, val in kit.items():
                if not key.startswith("<"):
                    if val is None:
                        data[key] = input("Add meg a " + key + "-t:")
                    else:
                        print(key + ":")
                        data.update(self.add_kit_properties(val))
            return data
        elif kit["<mode>"] == "or":
            keys = [k for k in kit.keys() if not k.startswith("<")]
            which = self.correct_input(
                self.text.choose_word_form, numbered=True, values=keys, default=-1
            )
            if kit[which] is None:
                return {"<type>": which} if kit.get("<showtype>") else {}
            return self.add_kit_properties(kit[which], which)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_doubles(self):
        garage = {self.mlang: {}, self.learnlang: {}}
        for glossname, gloss in self.words.items():
            for w in gloss:
                mword = w[self.mlang]["szo"].lower()
                try:
                    garage[self.mlang][mword].append(glossname)
                except:
                    garage[self.mlang][mword] = []
                    garage[self.mlang][mword].append(glossname)

                lword = w[self.learnlang]["szo"].lower()
                try:
                    garage[self.learnlang][lword].append(glossname)
                except:
                    garage[self.learnlang][lword] = []
                    garage[self.learnlang][lword].append(glossname)
        print(self.text.checking_doubles)
        for lang, ws in garage.items():
            print("\n", lang.upper(), " nyelven:", sep="")
            for word, glossaries in ws.items():
                if len(glossaries) > 1:
                    print(word, ":", glossaries)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_glossary_length(self):
        figy = True
        for glossname, gloss in self.words.items():
            if len(gloss) > 50:
                if figy:
                    print(self.text.warning_title)
                    figy = False
                print(self.text.glossary_too_long.format(glossname))


if __name__ == "__main__":
    main()
