
from random import shuffle, random

class NyelvTanulas:

    def __init__(self):
        self.nyelv = "német"
        self.additional_kit = {'mode':'&&', 'szófaj':{'mode':'||', 'főnév':['névelő', 'tbsz', 'gyenge'], 'melléknév':['-bb', 'leg-bb'], 'ige':{'mode':'&&', 'präteritum':None, 'perfekt':['ist/hat', 'pp forma']}}}
        self.lower_boundary = -1
        self.upper_boundary = 5

        self.auto_continue_practice = True

        try:
            file = open("szavak.txt", "r", encoding="utf-8")
            self.szavak = [line.split(" ") for line in file]
            file.close()
            self.szavak = [ {"magyar":    {"szo": line[0], "pont": int(line[1])},
                              self.nyelv: {"szo": line[2], "pont": int(line[3])} }
                            for line in self.szavak ]
        except Exception as e:
            file = open("szavak.txt", "w")
            file.close()
            self.szavak = []

        self.menu = "\nÜdv a nyelvtanuló programban! Mit szeretnél csinálni?\n"\
                    "1. Gyakorolni\n"\
                    "2. Új szót/szavakat megadni\n"\
                    "3. Megnézni, hogy állok\n"\
                    "4. Beállítások\n"\
                    "5. Kilépni\n"\
                    "Kérlek írd be a számot! (1-4): "
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start(self):
        while 1:
            whattodo = self.correct_input(self.menu, int, [1,2,3,4,5])

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
                confirm = input("Viszlát!:)")
                break
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def settings(self):
        pass
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def correct_input(self, string, mytype, values):
        question = input(string)
        while 1:
            try:
                question = mytype(question)
                if question in values:
                    return question
            except Exception as e:
                pass
            print("Helytelen válasz, próbáld újra!\n")
            question = input(string)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def practice(self):
        if len(self.szavak)==0:
            print("Nincs mit gyakorolni...")
            return

        lang = self.correct_input(f"Auto folytatás módban #-tel tudsz kilépni.\nMagyar vagy {self.nyelv} szavakat akarsz beírni? (magyar/{self.nyelv}): ", str, ["magyar", self.nyelv])

        helyes, helytelen = 0, 0

        first = True
        while first or self.auto_continue_practice:
            first = False

            practice_szavak = list(self.szavak)
            for szo in self.szavak:
                szopont = szo[lang]["pont"]
                if szopont < self.lower_boundary:
                    for i in range(abs(szopont-self.lower_boundary)//2):
                        practice_szavak.append(szo)
            shuffle(practice_szavak)

            dead = 0
            for szo in practice_szavak:
                szopont = szo[lang]["pont"]
                if (szopont-self.upper_boundary)*10 >= 100:
                    dead += 1
                    continue
                if szopont > self.upper_boundary and random()*100 < (szopont-self.upper_boundary)*10:
                    continue

                megoldas = szo[lang]["szo"]
                answer = input(szo["magyar" if lang == self.nyelv else self.nyelv]["szo"]+": ")
                if answer == "#": break

                while answer != megoldas and self.similar(answer, megoldas):
                    confirm = input("Majdnem eltaláltad, próbáld újra!")
                    answer = input(szo["magyar" if lang == self.nyelv else self.nyelv]["szo"]+": ")

                if answer == megoldas:
                    w = self.find(megoldas, lang)
                    w["pont"] += 1
                    helyes += 1
                    self.save()
                    confirm = input("Helyes!")
                else:
                    w = self.find(megoldas, lang)
                    w["pont"] -= 1
                    helytelen += 1
                    self.save()
                    confirm = input(f"Helytelen. A megoldás: {megoldas}")
            else:
                if dead == len(practice_szavak): break
                continue
            break # flag: ha kilépek, vagy ha mind "meghaltak" a szavaim, a while-ból is kilép

        confirm = input(f"A végére értél. Helyes válaszok: {helyes}, helytelen válaszok: {helytelen}, vagyis {int(helyes/helytelen*10000)/100 if helytelen!=0 else 100}%")
        self.save()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find(self, word, lang, word_or_pt=None):
        for w in self.szavak:
            if w[lang]["szo"] == word:
                if word_or_pt is not None: return w[lang][word_or_pt]
                else: return w[lang]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similar(self, w1, w2):
        return ( len(w1)==len(w2) and sum(1 for L in w1  if L in w2) == len(w2)-1 ) or ( len(w1)==len(w2)-1 and all(L in w2 for L in w1) )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_new(self):
        print("Szavak hozzáadása. #-tel lépsz ki.")

        while 1:
            magyar: str = input("Add meg a magyar kifejezést: ")
            if magyar == "#": break
            other: str = input(f"Add meg a {self.nyelv} kifejezést: ")
            if other == "#": break
            
            self.szavak.append( {"magyar": {"szo": magyar, "pont": 0}, self.nyelv: {"szo": other, "pont": 0}} )

        self.save()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save(self):
        file = open("szavak.txt", "w", encoding="utf-8")
        for szo in self.szavak:
            file.write(" ".join(map(str, szo["magyar"].values()))+" "+" ".join(map(str, szo[self.nyelv].values()))+"\n")
        file.close()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def state(self):
        pass

########################################################
tan = NyelvTanulas()
tan.start()
