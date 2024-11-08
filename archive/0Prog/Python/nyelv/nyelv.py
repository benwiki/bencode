"""A program for learning languages."""

from random import shuffle, random
from functools import reduce
import os

PROGRAM_PATH = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")


def confirm(s: str):
    """Prints the string and waits for the user to press Enter."""
    input(s)


# -------------------------------
ANYANYELV = "magyar"
TANNYELV = "német"
LANGUAGES = (ANYANYELV, TANNYELV)
# -------------------------------
KIT = {
    "mode": "apart",  # mode: apart / both
    "magyar": {},
    "német": {
        "mode": "and",
        "szófaj": {
            "mode": "or",
            "főnév": {
                "mode": "and",
                "névelő": None,
                "tbsz": None,
                "gyenge": None,
            },
            "ige": {
                "mode": "and",
                "präteritum": None,
                "pp_időbeli_segédige": None,
                "pp": None,
            },
            "melléknév": {
                "mode": "and",
                "közép": None,
                "felső": None,
            },
            "névmás": {
                "mode": "and",
                "nőnem": None,
                "semleges nem": None,
            },
            "kifejezés": None,
        },
    },
}


class NyelvTanulas:
    """A program for learning languages."""

    lower_boundary = 0
    upper_boundary = 5
    dead_pt = 15
    boost_pt = -10
    auto_continue_practice = True
    menu = (
        "\nÜdv a nyelvtanuló programban! Mit szeretnél csinálni?\n"
        "1. Gyakorolni\n"
        "2. Új szót/szavakat megadni\n"
        "3. Új szótárakat létrehozni\n"
        "4. Megnézni, hogy állok\n"
        "5. Beállítások\n"
        "6. Kilépni\n"
        "7. Szókeresés\n"
        "Kérlek írd be a számot! (1-7): "
    )

    running = True

    def __init__(self, mlang=None, learnlang=None, kit=None):
        self.mlang = mlang if mlang is not None else "magyar"
        self.learnlang = learnlang if learnlang is not None else "angol"
        self.kit = kit
        self.commands = [
            self.practice,
            self.add_new,
            self.add_glossary,
            self.state,
            self.settings,
            self.out,
            self.find_similar,
        ]

        try:
            with open(
                f"{PROGRAM_PATH}/glossaries.txt", "r", encoding="utf-8"
            ) as glossfile:
                self.glossaries = [gloss.strip() for gloss in glossfile]

            self.words = {}
            for gloss in self.glossaries:
                try:
                    with open(
                        f"{PROGRAM_PATH}/" + gloss + ".txt", "r", encoding="utf-8"
                    ) as file:
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
                                LANGUAGES[i]: {key: val for key, val in word[i]}
                                for i in range(2)
                            }
                            for word in temp
                        ]

                except FileNotFoundError:
                    file = open(
                        f"{PROGRAM_PATH}/" + gloss + ".txt", "w", encoding="utf-8"
                    )
                    file.close()
                    self.words[gloss] = []

                except (IOError, ValueError) as e:
                    print(e, "- by reading", gloss)
                    self.words[gloss] = []

            self.check_for_doubles()
            self.check_for_glossary_length()

        except FileNotFoundError:
            file = open(f"{PROGRAM_PATH}/glossaries.txt", "w", encoding="utf-8")
            file.close()
            self.words = {}
            self.all_words = []

        except (IOError, ValueError) as e:
            print(e, "- by opening glossaries.txt")
            self.words = {}
            self.all_words = []

        self.all_words = reduce(lambda a, b: a + b, self.words.values(), [])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start(self):
        """Starts the program."""
        while self.running:
            whattodo = self.correct_input(
                self.menu, int, [i + 1 for i in range(len(self.commands))]
            )
            self.commands[whattodo - 1]()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def out(self):
        """Exit."""
        print("Viszlát!:)")
        self.running = False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def settings(self):
        """Settings."""

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def correct_input(self, string, mytype, values: list, segment=False):
        """Asks the user for input until the input is correct."""
        question = input(string)
        while True:
            try:
                question = mytype(question)
                if question in values:
                    return question
                elif segment:
                    for val in values:
                        if val.startswith(question):
                            return val
            except ValueError as e:
                print(e, "in correct input")
            print("Helytelen válasz, próbáld újra!\n")
            question = input(string)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def practice(self):
        """Practice the words."""
        gloss = self.correct_input(
            "\nMelyik szótárat használod?\n - {}\nVálassz: ".format(
                "\n - ".join(self.glossaries)
            ),
            str,
            self.glossaries,
        )

        if len(self.words) == 0 or len(self.words[gloss]) == 0:
            print("Itt még nincs mit gyakorolni...")
            return

        lang = self.correct_input(
            "Auto folytatás módban #-tel tudsz kilépni."
            f"\n{self.mlang} vagy {self.learnlang} szavakat akarsz beírni? "
            f"({self.mlang}/{self.learnlang}): ",
            str,
            [self.mlang, self.learnlang],
        )
        questionlang = self.mlang if lang == self.learnlang else self.learnlang
        correct_pt, incorrect_pt = 0, 0

        first = True
        while first or self.auto_continue_practice:
            first = False

            practice_words = list(self.words[gloss])
            for word in self.words[gloss]:
                wordscore = word[lang]["pont"]
                if wordscore < self.lower_boundary:
                    for _ in range(
                        abs(wordscore - self.lower_boundary)
                    ):  # minden mínuszpont egy további kérdezést jelent. Boost mode.
                        practice_words.append(word)
            shuffle(practice_words)

            dead = 0
            to_break = False
            for cur_word in practice_words:
                wordscore = cur_word[lang]["pont"]
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

                answer = input("\n" + cur_word[questionlang]["szo"] + ": ")
                if answer == "#":
                    break
                elif answer == "@":
                    for word in solutions:
                        word[lang]["pont"] = self.dead_pt
                    confirm(f"Pont kimaxolva! {', '.join(solution_words)} teljesítve!")
                    continue
                elif answer == "*":
                    for word in solutions:
                        word[lang]["pont"] = self.boost_pt
                    confirm(
                        f"{', '.join(solution_words)} boostolva: {self.boost_pt} pontra állítva!"
                    )
                    break

                while (
                    answer in solution_words
                    and solutions[solution_words.index(answer)][lang]["pont"]
                    >= self.dead_pt
                ):
                    confirm("Ezt a szót már tudod, erre van egy másik szó is!")
                    answer = input(cur_word[questionlang]["szo"] + ": ")

                while answer not in solution_words and any(
                    self.similar(answer, m) for m in solution_words
                ):
                    confirm("Majdnem eltaláltad, próbáld újra!")
                    answer = input(cur_word[questionlang]["szo"] + ": ")

                if answer in solution_words:
                    to_change = solutions[solution_words.index(answer)][lang]
                    to_change["pont"] += 1
                    correct_pt += 1
                    self.save(gloss)
                    confirm(
                        "Helyes!"
                        + (
                            " További helyes válaszok: "
                            + ", ".join(w for w in solution_words if w != answer)
                            if len(solutions) > 1
                            else ""
                        )
                    )
                    if to_change["pont"] >= self.dead_pt:
                        confirm("Pont kimaxolva! Szó teljesítve!")
                        done = True

                    for detail, detail_solution in to_change.items():
                        if detail not in ("pont", "szo"):
                            answer = input(f"{detail}: ")
                            if answer == "#":
                                to_break = True
                                break
                            elif answer == "@":
                                for word in solutions:
                                    word[lang]["pont"] = self.dead_pt
                                confirm(
                                    f"Pont kimaxolva! {', '.join(solution_words)} teljesítve!"
                                )
                                break
                            elif answer == "*":
                                for word in solutions:
                                    word[lang]["pont"] = self.boost_pt
                                confirm(
                                    f"{', '.join(solution_words)} boostolva: {self.boost_pt} pontra állítva!"
                                )
                                to_break = True
                                break

                            while answer != detail_solution and self.similar(
                                answer, detail_solution
                            ):
                                confirm("Majdnem eltaláltad, próbáld újra!")
                                answer = input(f"{detail}: ")

                            if answer == detail_solution:
                                to_change["pont"] += 1
                                correct_pt += 1
                                self.save(gloss)
                                confirm("Helyes!")
                                if not done and to_change["pont"] == self.dead_pt:
                                    confirm("Pont kimaxolva! Szó teljesítve!")
                            else:
                                to_change["pont"] -= 1
                                incorrect_pt += 1
                                self.save(gloss)
                                confirm(f"Helytelen. A megoldás: {detail_solution}")
                        if to_break:
                            break
                else:
                    for word in solutions:
                        word[lang]["pont"] -= 1
                    incorrect_pt += 1
                    self.save(gloss)
                    confirm(f"Helytelen. A megoldás(ok): {', '.join(solution_words)}")

                self.save(gloss)

            else:
                if dead == len(practice_words):
                    print("Kész! Nincs mit gyakorolni!")
                    break
                continue
            break  # flag: ha kilépek, vagy ha mind "meghaltak" a szavaim, a while-ból is kilép

        if correct_pt + incorrect_pt > 0:
            confirm(
                f"A végére értél. Helyes válaszok: {correct_pt}, "
                f"helytelen válaszok: {incorrect_pt}, vagyis "
                f"{int(correct_pt/(correct_pt+incorrect_pt)*10000)/100}%"
            )
        self.save(gloss)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find(self, word, lang, gloss=None, property_=None):
        """Finds a word in the glossaries."""
        return [
            w if property_ is None else w[lang][property_]
            for w in (self.words[gloss] if gloss is not None else self.all_words)
            if w[lang]["szo"] == word
        ]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similarity(self, given: str, correct: str) -> float:  # , strength=1) -> float:
        """Returns the similarity of two strings."""
        # given, correct = given.lower(), correct.lower()
        # return (
        #     len(given) == len(correct)
        #     and sum(1 for L in given if L in correct) >= len(correct) - strength
        # ) or (
        #     0 < abs(len(given) - len(correct)) <= strength
        #     and all(L in correct for L in given)
        # )

        # glen ~ given length, clen ~ correct length
        glen, clen = len(given), len(correct)
        if glen == 0 and clen > 0:
            return False
        g, c, score = 0, 0, 0
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
                    except IndexError as e:
                        print(e, "- in similar function")
                    else:
                        break
                while chan_c < clen:
                    try:
                        will_g = given.index(correct[chan_c], g + 1)
                    except ValueError:
                        chan_c += 1
                    except IndexError as e:
                        print(e, "- in similar function")
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
    def similar(self, given: str, correct: str) -> bool:
        """Returns whether two strings are similar."""
        glen, clen = len(given), len(correct)
        if glen == 0 and clen > 0:
            return False

        score = self.similarity(given, correct)
        result = (score / clen + score / glen) / 2
        return result > 0.8

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find_similar(self):
        """Finds similar words."""
        word = input("Írd be a kifejezést: ")
        lang = self.correct_input(
            f"Milyen nyelven van? ({self.mlang}/{self.learnlang}): ",
            str,
            [self.mlang, self.learnlang],
            segment=True,
        )
        print("\nHasonló szavak:")
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
                        f" = {w[otherlang]['szo']} ({w[otherlang]['pont']} pt) "
                        f"{', '.join(otherlangitems)} [a {glossname} szótárban]",
                    ]
                )
        s = list(reversed(sorted(garage, key=lambda k: k[0])))
        for i in range(10):
            print(s[i][1])
        confirm("Kész!")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_new(self) -> None:
        """Adds new words to the glossaries."""
        print("Szavak hozzáadása. #-tel lépsz ki.")

        glosses = "\n - ".join(self.glossaries)
        msg = f"Melyik szótárat használod?\n - {glosses}\nVálassz: "
        gloss = self.correct_input(msg, str, self.glossaries)

        while True:
            words_to_add = ["", ""]
            msg = "Ez a szó már szerepel {} szótárban! Biztos hozzáadod? (i/n): "
            for i, lang in enumerate((self.mlang, self.learnlang)):
                word_of_lang = input(f"\nAdd meg a {lang} kifejezést: ")
                words_to_add[i] = word_of_lang
                if word_of_lang == "#":
                    break
                elif len(self.find(word_of_lang, lang, gloss)) > 0:
                    ans = self.correct_input(msg.format("ebben a"), str, ["i", "n"])
                    if ans == "n":
                        continue
                elif len(self.find(word_of_lang, lang)) > 0:  # global search
                    ans = self.correct_input(msg.format("VALAMELYIK"), str, ["i", "n"])
                    if ans == "n":
                        continue

            mlang_kit, learnlang_kit = self.add_kit_properties(self.kit)
            mlang_word, learnlang_word = words_to_add
            self.words[gloss].append(
                {
                    self.mlang: {"szo": mlang_word, "pont": 0, **mlang_kit},
                    self.learnlang: {"szo": learnlang_word, "pont": 0, **learnlang_kit},
                }
            )
            self.save(gloss)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_glossary(self) -> None:
        """Adds new glossaries."""
        print("Szótárak hozzáadása. #-tel lépsz ki.")

        while True:
            gloss = input("\nAdd meg a szótár nevét: ")
            while gloss in self.glossaries:
                gloss = input("Ez a szótár már létezik!\nAdd meg az új szótár nevét: ")
            if gloss == "#":
                break
            with open(
                f"{PROGRAM_PATH}/glossaries.txt", "a", encoding="utf-8"
            ) as glossfile:
                glossfile.write(gloss + "\n")
            with open(f"{PROGRAM_PATH}/" + gloss + ".txt", "w", encoding="utf-8"):
                pass
            self.glossaries.append(gloss)
            self.words[gloss] = []
            confirm("Sikeresen hozzáadva!")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save(self, gloss) -> None:
        """Saves the glossaries."""
        file = open(f"{PROGRAM_PATH}/" + gloss + ".txt", "w", encoding="utf-8")
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
    def state(self) -> None:
        """Shows the state of the glossaries."""
        msg = "\nEgy bizonyos szótár állapotát (sz)\nvagy minden szótár állapotát (m)\nkívánod megtekinteni? (sz/m): "
        sz_vagy_m = self.correct_input(msg, str, ["sz", "m"])
        if sz_vagy_m == "sz":
            glosses = "\n - ".join(self.glossaries)
            msg = f"\nMelyik szótárat használod?\n - {glosses}\nVálassz: "
            gloss = self.correct_input(msg, str, self.glossaries)
            words_to_check = self.words[gloss]
        else:
            words_to_check = self.all_words

        osszes = len(words_to_check)
        telj = sum(
            1
            for sz in words_to_check
            if sz[self.mlang]["pont"] >= self.dead_pt
            or sz[self.learnlang]["pont"] >= self.dead_pt
        )
        print(
            f"\nSzavak száma: {osszes}; teljesített szavak száma: {telj}; "
            f"tehát az arány: {int(telj / osszes * 10000) / 100} %",
        )
        msg = "Meg kívánod tekinteni az egész kócerájt is? (i/n): "
        details = self.correct_input(msg, str, ["i", "n"])
        if details == "n":
            return

        msg = f"Melyik nyelv pontjait akarod megtekinteni? ({self.mlang}/{self.learnlang}): "
        whichlang = self.correct_input(msg, str, [self.mlang, self.learnlang])
        by_score: dict[str, list] = {}
        for sz in words_to_check:
            score = sz[whichlang]["pont"]
            by_score.get(score, []).append(sz[whichlang]["szo"])
        for score, words in reversed(sorted(by_score.items(), key=lambda k: k[0])):
            print(f"\n{score} pontos szavak: {len(words)} db")
            for sz in words:
                print("-", sz)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_kit_properties(self, kit=None):
        """Adds properties to the words."""
        if kit is None:
            return ({}, {})
        if len(kit) == 0:
            return {}

        if kit["mode"] == "apart":
            return (
                self.add_kit_properties(kit[self.mlang]),
                self.add_kit_properties(kit[self.learnlang]),
            )
        elif kit["mode"] == "both":
            pass

        elif kit["mode"] == "and":
            data = {}
            for key, val in kit.items():
                if key != "mode":
                    if val is None:
                        data[key] = input(f"Add meg a(z) {key}-t:")
                    else:
                        print(f"{key}:")
                        data.update(self.add_kit_properties(val))
            return data
        elif kit["mode"] == "or":
            keys = [k for k in kit.keys() if k != "mode"]
            which = self.correct_input(
                f"válassz ({'/'.join(keys)}): ", str, keys, segment=True
            )
            if kit[which] is None:
                return {}
            return self.add_kit_properties(kit[which])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_doubles(
        self,
    ) -> None:
        """Checks for doubles in the glossaries."""
        print("Ismétlődések keresése...")

        garage: dict[str, dict[str, list]] = {self.mlang: {}, self.learnlang: {}}
        for glossname, gloss in self.words.items():
            for word in gloss:
                mword = word[self.mlang]["szo"].lower()
                garage[self.mlang].get(mword, []).append(glossname)
                lword = word[self.learnlang]["szo"].lower()
                garage[self.learnlang].get(lword, []).append(glossname)
        for lang, ws in garage.items():
            print("\n", lang.upper(), " nyelven:", sep="")
            for word, glossaries in ws.items():
                if len(glossaries) > 1:
                    print(word, ":", glossaries)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_glossary_length(self):
        """Checks if any glossary has more than 50 elements."""
        more_than_50 = [
            glossname for glossname, gloss in self.words.items() if len(gloss) > 50
        ]
        if more_than_50:
            message = "\nFigyelem!\nA következő szótárakban több mint 50 elem van: "
            print(message + ", ".join(more_than_50))


########################################################
tan = NyelvTanulas(ANYANYELV, TANNYELV, KIT)
tan.start()
