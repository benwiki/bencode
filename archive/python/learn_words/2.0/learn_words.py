
from random import shuffle, random

# -------------------------------
MOTHER_TONGUE = "magyar"
LANG_TO_LEARN = "német"
LANGUAGES = (MOTHER_TONGUE, LANG_TO_LEARN)
DICT_FILENAME = "words.txt"

# -------------------------------
KIT = {
    'mode': 'apart',  # mode: apart / both
    "magyar": {},
    "német": {
        'mode': 'and',
        "szófaj": {
            'mode': 'or',
            "főnév": {
                'mode': 'and',
                "névelő": None,
                "tbsz": None,
                "gyenge": None
            },
            "ige": {
                'mode': 'and',
                "präteritum": None,
                "pp_időbeli_segédige": None,
                "pp": None
            },
            "melléknév": {
                'mode': 'and',
                "közép": None,
                "felső": None
            },
            "kifejezés": None
        }
    }
}


class LanguageLearning:
    lower_boundary = -1
    upper_boundary = 5
    auto_continue_practice = True

    def __init__(self, mlang=None, learnlang=None, kit=None):
        self.mlang = mlang if mlang is not None else "magyar"
        self.learnlang = learnlang if learnlang is not None else "angol"
        self.kit = kit

        try:
            with open(DICT_FILENAME, "r", encoding="utf-8") as dict_file:
                _words = [[[[c.strip() for c in comp.split(':')]
                            for comp in lang.split(" ; ")]
                           for lang in line.split(" | ")]
                          for line in dict_file.readlines()]
            self.words = [{
                LANGUAGES[i]: {
                    key: (int(val) if val.isnumeric() else val)
                    for key, val in word[i]}
                for i in range(2)}
                for word in _words]

        except FileNotFoundError as e:
            with open(DICT_FILENAME, "w") as _:
                self.words = []
        except Exception as e:
            print(e)
            self.words = []

        self.menu = ("\nÜdv a nyelvtanuló programban! "
                     "Mit szeretnél csinálni?\n"
                     "1. Gyakorolni\n"
                     "2. Új szót/szavakat megadni\n"
                     "3. Megnézni, hogy állok\n"
                     "4. Beállítások\n"
                     "5. Kilépni\n"
                     "Kérlek írd be a számot! (1-5): ")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start(self):
        while True:
            whattodo = self.correct_input(self.menu, int, range(1, 5+1))

            if whattodo == 1:
                self.practice()
            elif whattodo == 2:
                self.add_new()
            elif whattodo == 3:
                self.state()
            elif whattodo == 4:
                self.settings()
            elif whattodo == 5:
                self.save()
                input("Viszlát!:)")
                break

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def settings(self):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def correct_input(self, string, mytype, values):
        question = input(string)
        while True:
            try:
                question = mytype(question)
                if question in values:
                    return question
            except Exception as e:
                pass
            print("Helytelen válasz, próbáld újra!\n")
            question = input(string)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def practice(self):
        if len(self.words) == 0:
            print("Nincs mit gyakorolni...")
            return

        lang = self.correct_input(
            f"Auto folytatás módban #-tel tudsz kilépni.\n{self.mlang} vagy "
            f"{self.learnlang} szavakat akarsz beírni? "
            f"(magyar/{self.learnlang}): ", str, [self.mlang, self.learnlang])
        questionlang = self.mlang if lang == self.learnlang else self.learnlang
        correct_ans_num, incorrect_ans_num = 0, 0

        first = True
        while first or self.auto_continue_practice:
            first = False

            practice_words = list(self.words)
            for word in self.words:
                word_pt = int(word[lang]["pont"])
                if word_pt < self.lower_boundary:
                    for i in range(abs(word_pt-self.lower_boundary)//2):
                        practice_words.append(word)
            shuffle(practice_words)

            dead = 0
            for word in practice_words:
                word_pt = int(word[lang]["pont"])
                if (word_pt-self.upper_boundary)*10 >= 100:
                    dead += 1
                    continue
                if (word_pt > self.upper_boundary and
                   random()*100 < (word_pt-self.upper_boundary)*10):
                    continue

                question_word = str(word[questionlang]["szo"])
                solution = word[lang]["szo"]
                answer = input(question_word + ": ")
                if answer == "#":
                    break

                while answer != solution and self.similar(answer, solution):
                    input("Majdnem eltaláltad, próbáld újra!")
                    answer = input(question_word + ": ")

                found_word = self.find(solution, lang)

                if answer == solution:
                    found_word["pont"] += 1
                    correct_ans_num += 1
                    self.save()
                    input("Helyes!")
                else:
                    found_word["pont"] -= 1
                    incorrect_ans_num += 1
                    self.save()
                    input(f"Helytelen. A megoldás: {solution}")

                for reszlet, reszlet_megoldas in word[lang].items():
                    if reszlet not in ('pont', 'szo'):
                        answer = input(f"{reszlet}: ")
                        if answer == "#":
                            break

                        while (answer != reszlet_megoldas and
                               self.similar(answer, reszlet_megoldas)):
                            input("Majdnem eltaláltad, próbáld újra!")
                            answer = input(f"{reszlet}: ")

                        found_word = self.find(solution, lang)

                        if answer == reszlet_megoldas:
                            found_word["pont"] += 1
                            correct_ans_num += 1
                            self.save()
                            confirm = input("Helyes!")
                        else:
                            found_word["pont"] -= 1
                            incorrect_ans_num += 1
                            self.save()
                            confirm = input(
                                f"Helytelen. A megoldás: {solution}")

            else:
                if dead == len(practice_words):
                    break
                continue
            break
            # flag: ha kilépek, vagy ha mind "meghaltak" a szavaim,
            # a while-ból is kilép

        rate = correct_ans_num / (correct_ans_num + incorrect_ans_num)
        input(
            f"A végére értél. Helyes válaszok: {correct_ans_num}, "
            f"helytelen válaszok: {incorrect_ans_num}, vagyis " +
            str(int(rate * 10000) / 100) + "%")
        self.save()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def find(self, word, lang, word_or_pt=None):
        for w in self.words:
            if w[lang]["szo"] == word:
                if word_or_pt is not None:
                    return w[lang][word_or_pt]
                else:
                    return w[lang]
        return None
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def similar(self, w1, w2):
        return ((len(w1) == len(w2) and
                 sum(1 for L in w1 if L in w2) == len(w2)-1) or
                (len(w1) == len(w2)-1 and all(L in w2 for L in w1)))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add_new(self):
        print("Szavak hozzáadása. #-tel lépsz ki.")

        while True:
            add_mlang = input(f"\nAdd meg a {self.mlang} kifejezést: ")
            if add_mlang == "#":
                break
            add_learnlang = input(f"Add meg a {self.learnlang} kifejezést: ")
            if add_learnlang == "#":
                break

            mlang_kit, learnlang_kit = self.add_kit_properties(self.kit)

            self.words.append({
                self.mlang: {
                    "szo": add_mlang,
                    "pont": 0, **mlang_kit},
                self.learnlang: {
                    "szo": add_learnlang,
                    "pont": 0, **learnlang_kit}})
            self.save()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save(self):
        file = open(DICT_FILENAME, "w", encoding="utf-8")
        for szo in self.words:
            file.write(" | ".join(" ; ".join(
                f"{key}:{val}" for key, val in lang.items())
                for lang in szo.values()) + "\n")
        file.close()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def state(self):
        pass
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add_kit_properties(self, kit=None) -> dict | tuple:
        if kit is None:
            return ({}, {})
        if len(kit) == 0:
            return {}

        if kit['mode'] == 'apart':
            return (
                self.add_kit_properties(kit[self.mlang]),
                self.add_kit_properties(kit[self.learnlang]))
        elif kit['mode'] == 'both':
            pass

        elif kit['mode'] == 'and':
            data = {}
            for key, val in kit.items():
                if key != 'mode':
                    if val is None:
                        data[key] = input("Add meg a "+key+"-t:")
                    else:
                        print(key+":")
                        data |= self.add_kit_properties(val)
            return data
        elif kit['mode'] == 'or':
            which = self.correct_input(
                "válassz (" +
                "/".join([k for k in kit.keys() if k != 'mode']) +
                "): ", str, kit.keys())
            if kit[which] is None:
                return {}
            return self.add_kit_properties(kit[which])
        raise RuntimeError("Problem in add_kit_properties")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


########################################################
if __name__ == "__main__":
    tan = LanguageLearning(MOTHER_TONGUE, LANG_TO_LEARN, KIT)
    tan.start()
