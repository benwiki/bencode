
from random import shuffle, random
from functools import reduce
from langtext import *
#-------------------------------
ANYANYELV = "magyar"
TANNYELV = "német"
LANGUAGES = (ANYANYELV, TANNYELV)
#-------------------------------
KIT_GERMAN = {
    "mode":"apart", # mode: apart / both (should the points be counted for both languages or separately)
    "magyar" : {
        "<type>": "mothertongue",
    },
    "német" : {
        "<mode>":"and",
        "szófaj" : { "mode":"or",
            "főnév" : { "mode":"and",
                "névelő":None,
                "tbsz":None,
                "gyenge":None
            },
            "ige" : { "mode":"and",
                "präteritum":None,
                "pp_időbeli_segédige":None,
                "pp":None
            },
            "melléknév" : { "mode":"and",
                "közép":None,
                "felső":None
            },
            "névmás" : { "mode":"and",
                "nőnem":None,
                "semleges nem":None
            },
            "kifejezés":None
        }
    }
}

KIT = { "mode": "apart",
    "magyar": {},
    "német": { "mode": "and",
        "szófaj": { "mode": "or",
            "főnév": { "mode": "and",
                "deklináció":None,
                "nem":None,
            },
            "ige":None,
            "prepozíció": { "mode": "and",
                "eset":None,
            },
            "egyéb":None,
        },
    },
}

class NyelvTanulas:
    lower_boundary = 0
    upper_boundary = 5
    dead_pt = 15
    boost_pt = -10
    auto_continue_practice = True
    
    running = True

    def __init__(self, mlang=None, learnlang=None, kit=None, text: LangText=None):
        self.mlang = mlang or "magyar"
        self.learnlang = learnlang or "angol"
        self.kit = kit
        self.text = text or EnglishText()
        self.commands = [self.practice, self.add_new, self.add_glossary, self.state, self.settings, self.out, self.find_similar]

        try:
            with open("glossaries.txt", "r", encoding="utf-8") as glossfile:
                self.glossaries = [gloss.strip() for gloss in glossfile]
            
            self.words = {}
            for gloss in self.glossaries:
                try:
                    with open(gloss+".txt", "r", encoding="utf-8") as file:
                        temp = [[[[int(c.strip()) if c.strip().isnumeric() or c[1:].strip().isnumeric() else c.strip()
                                          for c in comp.split(":")]
                                         for comp in lang.split(" ; ")]
                                        for lang in line.split(" | ")]
                                       for line in file]
                                       
                        self.words[gloss] = [{LANGUAGES[i] : {key:val for key, val in word[i]}
                                              for i in range(2)}
                                             for word in temp]
                except FileNotFoundError as e:
                    file = open(gloss+".txt", "w")
                    file.close()
                    self.words[gloss]=[]
                except Exception as e:
                    print(e, "- by reading", gloss)
                    self.words[gloss]=[]
            
            self.all_words = reduce(lambda a,b: a+b, self.words.values())

            self.check_for_doubles()
            self.check_for_glossary_length()
                    
        except FileNotFoundError as e:
            file = open("glossaries.txt", "w")
            file.close()
            self.words = {}
        except Exception as e:
            print(e, "- by opening glossaries.txt")
            self.words = {}
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start(self):
        while self.running:
            whattodo = self.correct_input(self.text.menu, int, list(range(1, len(self.commands)+1)))
            self.commands[whattodo-1]()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def out(self):
        confirm = input("Viszlát!:)")
        self.running = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def settings(self):
        pass
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def correct_input(self, string, mytype, values, segment=True):
        
        question = input(string)
        while True:
            try:
                question = mytype(question)
                if question in values:
                    return question
                elif segment:
                    starts = [val for val in values if val.startswith(question)]
                    if len(starts) > 1:
                        print("\nTöbb mint egy lehetőség adott ({})!\nKérlek több karaktert írj be!".format(", ".join(starts)))
                    elif len(starts) == 1:
                        return starts[0]
            except Exception as e:
                print(e, "{} hiba a {} függvényben! Jelentsd a fejlesztőnek kérlek!".format("Konverziós", "correct_input"))
            input("Helytelen válasz, próbáld újra! [ENTER]")
            question = input(string)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def practice(self):
        
        gloss = self.correct_input("\nMelyik szótárat használod?\n - {}\nVálassz: ".format("\n - ".join(self.glossaries)), str, self.glossaries)
        
        if len(self.words)==0 or len(self.words[gloss]) == 0:
            print("Itt még nincs mit gyakorolni...")
            return
        
        lang = self.correct_input(f"Auto folytatás módban #-tel tudsz kilépni.\n{self.mlang} vagy {self.learnlang} szavakat akarsz beírni? (magyar/{self.learnlang}): ", str, [self.mlang, self.learnlang])
        questionlang = self.mlang if lang == self.learnlang else self.learnlang
        correct_pt, incorrect_pt = 0, 0

        first = True
        while first or self.auto_continue_practice:
            first = False

            practice_words = list(self.words[gloss])
            for word in self.words[gloss]:
                wordscore = word[lang]["pont"]
                if wordscore < self.lower_boundary:
                    for i in range(abs(wordscore-self.lower_boundary)): # minden mínuszpont egy további kérdezést jelent. Boost mode.
                        practice_words.append(word)
            shuffle(practice_words)

            dead = 0
            to_break = False
            for cur_word in practice_words:
                wordscore = cur_word[lang]["pont"]
                if wordscore >= self.dead_pt:
                    dead += 1
                    continue
                if wordscore > self.upper_boundary and random() < (wordscore-self.upper_boundary)/(self.dead_pt-self.upper_boundary):
                    continue
                
                done = False
                solutions = self.find(cur_word[questionlang]["szo"], questionlang, gloss)
                solution_words = [word[lang]["szo"] for word in solutions]
                
                answer = input("\n"+cur_word[questionlang]["szo"]+": ")
                if answer == "#": break
                elif answer == "@":
                    for word in solutions: word[lang]["pont"] = self.dead_pt
                    confirm = input("Pont kimaxolva! "+", ".join(solution_words)+" teljesítve!")
                    continue
                elif answer == "*":
                    for word in solutions: word[lang]["pont"] = self.boost_pt
                    confirm = input(", ".join(solution_words)+" boostolva: "+str(self.boost_pt)+" pontra állítva!")
                    break
                
                while answer in solution_words and solutions[solution_words.index(answer)][lang]["pont"] >= self.dead_pt:
                    confirm = input("Ezt a szót már tudod, erre van egy másik szó is!")
                    answer = input(cur_word[questionlang]["szo"]+": ")
                    
                while answer not in solution_words and any(self.similar(answer, m) for m in solution_words):
                    confirm = input("Majdnem eltaláltad, próbáld újra!")
                    answer = input(cur_word[questionlang]["szo"]+": ")
                    
                if answer in solution_words:
                    to_change = solutions[solution_words.index(answer)][lang]
                    to_change["pont"] += 1
                    correct_pt += 1
                    self.save(gloss)
                    confirm = input("Helyes!"+(f" További helyes válaszok: {', '.join(w for w in solution_words if w!=answer)}" if len(solutions)>1 else ''))
                    if to_change["pont"] >= self.dead_pt:
                        confirm = input("Pont kimaxolva! Szó teljesítve!")
                        done = True
                    
                    for detail, detail_solution in to_change.items():
                        if detail not in ('pont', 'szo'):
                            answer = input(f"{detail}: ")
                            if answer == "#":
                                to_break = True
                                break
                            elif answer == "@":
                                for word in solutions: word[lang]["pont"] = self.dead_pt
                                confirm = input("Pont kimaxolva! "+", ".join(solution_words)+" teljesítve!")
                                break
                            elif answer == "*":
                                for word in solutions: word[lang]["pont"] = self.boost_pt
                                confirm = input(", ".join(solution_words)+" boostolva: "+self.boost_pt+" pontra állítva!")
                                to_break = True
                                break
    
                            while answer != detail_solution and self.similar(answer, detail_solution):
                                confirm = input("Majdnem eltaláltad, próbáld újra!")
                                answer = input(f"{detail}: ")
    
                            if answer == detail_solution:
                                to_change["pont"] += 1
                                correct_pt += 1
                                self.save(gloss)
                                confirm = input("Helyes!")
                                if not done and to_change["pont"]==self.dead_pt:
                                    confirm = input("Pont kimaxolva! Szó teljesítve!")
                            else:
                                to_change["pont"] -= 1
                                incorrect_pt += 1
                                self.save(gloss)
                                confirm = input(f"Helytelen. A megoldás: {detail_solution}")
                        if to_break: break
                else:
                    for word in solutions: word[lang]["pont"] -= 1
                    incorrect_pt += 1
                    self.save(gloss)
                    confirm = input(f"Helytelen. A megoldás(ok): {', '.join(solution_words)}")
                    
                self.save(gloss)    
                    
            else:
                if dead == len(practice_words):
                    print("Kész! Nincs mit gyakorolni!")
                    break
                continue
            break # flag: ha kilépek, vagy ha mind "meghaltak" a szavaim, a while-ból is kilép

        if correct_pt+incorrect_pt>0: confirm = input(f"A végére értél. Helyes válaszok: {correct_pt}, helytelen válaszok: {incorrect_pt}, vagyis {int(correct_pt/(correct_pt+incorrect_pt)*10000)/100}%")
        self.save(gloss)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find(self, word, lang, gloss=None, property = None):
        return [w if property is None else w[lang][property]   for w in (self.words[gloss] if gloss is not None else self.all_words) if w[lang]["szo"] == word]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similarity(self, given: str, correct: str) -> float:
##        given, correct = given.lower(), correct.lower()
##        return ( len(given)==len(correct) and sum(1 for L in given  if L in correct) >= len(correct)-strength ) or ( 0 < abs(len(given)-len(correct)) <= strength and all(L in correct for L in given) )
        glen, clen = len(given), len(correct)
        if glen==0 and clen>0: return 0
        g=0; c=0; score=0
        while g < glen and c < clen:
            if given[g]==correct[c]:
                score+=1; g+=1; c+=1
            else:
                will_g, will_c = -1, -1 # the indexes I want to search
                chan_g, chan_c = g, c # the indexes I use for that, they CHANge
                while chan_g < glen:
                    try: will_c = correct.index(given[chan_g], c+1)
                    except ValueError: chan_g+=1
                    except Exception as e: print(e, "- in similar function")
                    else: break
                while chan_c < clen:
                    try: will_g = given.index(correct[chan_c], g+1)
                    except ValueError: chan_c+=1
                    except Exception as e: print(e, "- in similar function")
                    else: break
                if   will_c == -1 < will_g: g = will_g; c = chan_c
                elif will_g == -1 < will_c: c = will_c; g = chan_g
                elif will_g>-1 and will_c>-1:
                    if will_g < will_c: g = will_g; c = chan_c
                    else:               c = will_c; g = chan_g
                else: break
                    
        return score
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similar(self, given: str, correct: str, strength=1)->bool:
        glen, clen = len(given), len(correct)
        if glen==0 and clen>0 or clen==0 and glen>0:
            return False
        elif clen==0 and glen==0:
            return True
        
        score = self.similarity(given, correct)
        result = (score/clen+score/glen)/2
        return result>0.8
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find_similar(self):
        word = input("Írd be a kifejezést: ")
        lang = self.correct_input(f"Milyen nyelven van? ({self.mlang}/{self.learnlang}): ", str, [self.mlang, self.learnlang], segment=True)
        print("\nHasonló szavak:")
        got = False
        otherlang = self.mlang if lang == self.learnlang else self.learnlang
        garage = []
        for glossname, gloss in self.words.items():
            for w in gloss:
##                if self.similar(w[lang]["szo"], word):
                langitems = [f"{key}:{val}" for key, val in w[lang].items() if key!="szo" and key!="pont"]
                otherlangitems = [f"{key}:{val}" for key, val in w[otherlang].items() if key!="szo" and key!="pont"]
                garage.append( [self.similarity(w[lang]["szo"], word),
                      f" - {w[lang]['szo']} ({w[lang]['pont']} pt) {', '.join(langitems)}" \
                      f" = {w[otherlang]['szo']} ({w[otherlang]['pont']} pt) {', '.join(otherlangitems)} [a {glossname} szótárban]"] )
                
##                    got = True
##        if not got: print("Egyet se találtam...")
        s = list(reversed(sorted(garage, key=lambda k: k[0])))
        for i in range(10):
            print(s[i][1])
        confirm = input("Kész!")
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_new(self):
        print("Szavak hozzáadása. #-tel lépsz ki.")
        gloss = self.correct_input("\nMelyik szótárat használod?\n - {}\nVálassz: ".format("\n - ".join(self.glossaries)), str, self.glossaries)

        while True:
            add_mlang = input(f"\nAdd meg a {self.mlang} kifejezést: ")
            if add_mlang == "#": break
            elif len(self.find(add_mlang, self.mlang, gloss))>0:
                if input("Ez a szó már szerepel ebben a szótárban! Biztos hozzáadod? (i/n): ").lower() == "n": continue
            elif len(self.find(add_mlang, self.mlang))>0: # global search
                if input("Ez a szó már szerepel VALAMELYIK szótárban! Biztos hozzáadod? (i/n): ").lower() == "n": continue
                
            add_learnlang = input(f"Add meg a {self.learnlang} kifejezést: ")
            if add_learnlang == "#": break
            elif len(self.find(add_learnlang, self.learnlang, gloss))>0:
                if input("Ez a szó már szerepel ebben a szótárban! Biztos hozzáadod? (i/n): ").lower() == "n": continue
            elif len(self.find(add_learnlang, self.learnlang))>0: # global search
                if input("Ez a szó már szerepel VALAMELYIK szótárban! Biztos hozzáadod? (i/n): ").lower() == "n": continue
            
            mlang_kit, learnlang_kit = self.add_kit_properties(self.kit)
            
            self.words[gloss].append( {self.mlang:     {"szo": add_mlang,     "pont": 0, **mlang_kit},
                                                             self.learnlang: {"szo": add_learnlang, "pont": 0, **learnlang_kit}} )
            self.save(gloss)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_glossary(self):
        print("Szótárak hozzáadása. #-tel lépsz ki.")
        
        while True:
            gloss = input("\nAdd meg a szótár nevét: ")
            while gloss in self.glossaries:
                gloss = input("Ez a szótár már létezik!\nAdd meg az új szótár nevét: ")
            if gloss == "#": break
            with open("glossaries.txt", "a", encoding="utf-8") as glossfile: glossfile.write(gloss+"\n")
            with open(gloss+".txt", "w", encoding="utf-8"): pass
            self.glossaries.append(gloss)
            self.words[gloss] = []
            confirm = input("Sikeresen hozzáadva!")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save(self, gloss):
        file = open(gloss+".txt", "w", encoding="utf-8")
        for word in self.words[gloss]:
            file.write(" | ".join( " ; ".join(f"{key}:{val}" for key, val in lang.items()) for lang in word.values() )+"\n")
        file.close()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def state(self):
        sz_vagy_ossz = self.correct_input("\nEgy bizonyos szótár állapotát (sz)\nvagy minden szótár állapotát (m)\nkívánod megtekinteni? (sz/m): ", str, ["sz", "m"])
        if sz_vagy_ossz=="sz":
            gloss = self.correct_input("\nMelyik szótárat használod?\n - {}\nVálassz: ".format("\n - ".join(self.glossaries)), str, self.glossaries)
            words_to_check = self.words[gloss]
        else: words_to_check = self.all_words
        
        osszes = len(words_to_check)
        telj =sum(1 for sz in words_to_check if sz[self.mlang]["pont"]>=self.dead_pt or sz[self.learnlang]["pont"]>=self.dead_pt)
        print("\nSzavak száma:", osszes, "; teljesített szavak száma:", telj, "; tehát az arány:", int(telj/osszes*10000)/100, "%")
        
        details = self.correct_input("Meg kívánod tekinteni az egész kócerájt is? (i/n): ", str, ["i", "n"])
        if details =="n": return
        whichlang = self.correct_input("Melyik nyelv pontjait akarod megtekinteni? ("+self.mlang+"/"+self.learnlang+"): ", str, (self.mlang, self.learnlang))
        by_score = {}
        for sz in words_to_check:
            score = sz[whichlang]["pont"]
            try: by_score[score].append(sz[whichlang]["szo"])
            except:
                by_score[score] = [ ]
                by_score[score].append(sz[whichlang]["szo"])
        for score, words in reversed(sorted(by_score.items(), key = lambda k: k[0])):
            print("\n", end="")
            print(score,"pontos szavak:",len(words),"db")
            for sz in words: print("-", sz)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_kit_properties(self, kit=None):
        if kit is None: return ({}, {})
        if len(kit)==0: return {}
        
        if kit['mode'] == 'apart':
            return ( self.add_kit_properties(kit[self.mlang]), self.add_kit_properties(kit[self.learnlang]) )
        elif kit['mode'] == 'both':
            pass
         
        elif kit['mode'] == 'and':
            data = {}
            for key, val in kit.items():
                if key!='mode':
                    if val is None:
                        data[key] = input("Add meg a "+key+"-t:")
                    else:
                        print(key+":")
                        data.update(self.add_kit_properties(val))
            return data                    
        elif kit['mode'] == 'or':
            keys = [k for k in kit.keys() if k!='mode']
            which = self.correct_input("válassz (" + "/".join(keys) + "): ", str, keys, segment=True)
            if kit[which] is None: return {}
            return self.add_kit_properties(kit[which])
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_doubles(self): # ERŐS JAVÍTÁSRA SZORUL!!!!!!!!!!!!!!!! EZ ÍGY RATYI!!!!!!!!!!!!!
        garage = {self.mlang:{}, self.learnlang:{}}
        for glossname, gloss in self.words.items():
            for w in gloss:
                mword = w[self.mlang]["szo"].lower()
                try: garage[self.mlang][mword].append(glossname)
                except:
                    garage[self.mlang][mword] = []
                    garage[self.mlang][mword].append(glossname)

                lword = w[self.learnlang]["szo"].lower()
                try: garage[self.learnlang][lword].append(glossname)
                except:
                    garage[self.learnlang][lword] = []
                    garage[self.learnlang][lword].append(glossname)
        print("Ismétlődések keresése...")
        for lang, ws in garage.items():
            print("\n", lang.upper(), " nyelven:", sep='')
            for word, glossaries in ws.items():
                if len(glossaries)>1: print(word, ":", glossaries)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_glossary_length(self):
        figy = True
        for glossname, gloss in self.words.items():
            if len(gloss)>50:
                if figy:
                    print("\nFigyelem!")
                    figy = False
                print("A", glossname, "nevű szótárban több mint 50 elem van!")

########################################################
tan = NyelvTanulas(ANYANYELV, TANNYELV, KIT)
tan.start()
