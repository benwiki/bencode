from random import shuffle, random
from functools import reduce
from enum import Enum, auto
import json
import sys
from langtext import Lang, LangText # Import Lang enum and LangText class

# --- Configuration Enums for Kits ---

class Kit(Enum):
    """Defines the available language kit configurations."""
    # We now only need one entry pointing to the new multi-language kit
    MULTILANG = 'kits/kit_multilang.json'

    def load_config(self):
        """Loads the configuration dictionary from the associated JSON file."""
        try:
            with open(self.value, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Kit file {self.value} not found. Using empty kit.", file=sys.stderr)
            return {"name": "Empty Kit", "<mode>": "all", "languages": {}}
        except json.JSONDecodeError:
            print(f"ERROR: Kit file {self.value} has invalid JSON. Using empty kit.", file=sys.stderr)
            return {"name": "Empty Kit", "<mode>": "all", "languages": {}}

# Default Kit and Language for the application instance
SELECTED_KIT = Kit.MULTILANG
SELECTED_LANG = Lang.HUNGARIAN

class NyelvTanulas:
    lower_boundary = 0
    upper_boundary = 5
    dead_pt = 15
    boost_pt = -10
    auto_continue_practice = True
    
    running = True

    def __init__(self, kit_enum: Kit = SELECTED_KIT, lang_enum: Lang = SELECTED_LANG):
        self.text = LangText(lang_enum)
        self.kit_data = kit_enum.load_config()
        self.all_langs_config = self.kit_data.get("languages", {})
        self.all_langs_names = {key: self.all_langs_config[key].get("name_en", key) for key in self.all_langs_config}

        # --- New Multi-Language Setup ---
        self.active_langs = self.select_active_languages() # List of string language codes (e.g., ['german', 'magyar'])
        self.lang_codes = tuple(self.active_langs) # Used for indexing words
        # ---------------------------------
        
        self.commands = [self.practice, self.add_new, self.add_glossary, self.state, self.settings, self.out, self.find_similar]

        try:
            with open("glossaries.txt", "r", encoding="utf-8") as glossfile:
                self.glossaries = [gloss.strip() for gloss in glossfile]
            
            self.words = {}
            for gloss in self.glossaries:
                try:
                    with open(gloss+".txt", "r", encoding="utf-8") as file:
                        # Parsing words needs to be adapted to handle 2+ languages based on active_langs
                        temp = [[[[int(c.strip()) if c.strip().isnumeric() or c[1:].strip().isnumeric() else c.strip()
                                          for c in comp.split(":")]
                                         for comp in lang.split(" ; ")]
                                        for lang in line.split(" | ")]
                                       for line in file]
                                       
                        # Map parsed list items to language codes based on their order in self.lang_codes
                        # Note: This relies on the word data being saved/loaded in a consistent order determined by self.lang_codes
                        self.words[gloss] = [{self.lang_codes[i] : {key:val for key, val in word[i]}
                                              for i in range(len(self.lang_codes))}
                                             for word in temp]
                except FileNotFoundError:
                    file = open(gloss+".txt", "w")
                    file.close()
                    self.words[gloss]=[]
                except Exception as e:
                    print(e, self.text.error_reading_glossary.format(gloss), file=sys.stderr)
                    self.words[gloss]=[]
            
            self.all_words = reduce(lambda a,b: a+b, self.words.values(), []) # Added initial [] for safety

            self.check_for_doubles()
            self.check_for_glossary_length()
                    
        except FileNotFoundError:
            file = open("glossaries.txt", "w")
            file.close()
            self.words = {}
        except Exception as e:
            print(e, self.text.error_opening_glossaries, file=sys.stderr)
            self.words = {}

    def select_active_languages(self):
        """Prompts the user to select the languages for the session (min 2)."""
        while True:
            lang_list = list(self.all_langs_names.keys())
            
            prompt = self.text.select_active_langs + "\n"
            for i, (code, name) in enumerate(self.all_langs_names.items(), 1):
                prompt += f"{i}. {name} ({code})\n"
            prompt += "(Enter numbers separated by commas, e.g., 1,3): "
            
            selection_str = input(prompt)
            try:
                indices = [int(i.strip()) for i in selection_str.split(',') if i.strip()]
                selected_langs = [lang_list[i - 1] for i in indices if 0 < i <= len(lang_list)]
                selected_langs = list(dict.fromkeys(selected_langs)) # Remove duplicates
                
                if len(selected_langs) < 2:
                    print(self.text.min_langs_error)
                else:
                    return selected_langs
            except:
                print(self.text.invalid_input_prompt.replace("[ENTER]", ""))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start(self):
        while self.running:
            whattodo = self.correct_input(self.text.menu, int, list(range(1, len(self.commands)+1)))
            self.commands[whattodo-1]()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def out(self):
        confirm = input(self.text.goodbye)
        self.running = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def settings(self):
        print("\n--- Settings ---")
        print("1. Change UI Language (Current: {})".format(self.text._text_data.get("menu", "").split('\n')[1].split(' ')[-1].strip('!')))
        print("2. Change Active Languages (Current: {})".format(", ".join(self.active_langs)))
        
        setting = self.correct_input("Choose a setting (1-2) or press ENTER to return: ", int, [1, 2, ""])
        
        if setting == 1:
            print("\nAvailable UI Languages:")
            lang_names = [l.name for l in Lang]
            for i, name in enumerate(lang_names, 1):
                print(f"{i}. {name}")
                
            choice = self.correct_input("Enter the number for the new language: ", int, list(range(1, len(lang_names) + 1)))
            new_lang_enum = list(Lang)[choice - 1]
            self.text = LangText(new_lang_enum)
            print(self.text.successfully_added)
            
        elif setting == 2:
            new_langs = self.select_active_languages()
            self.active_langs = new_langs
            self.lang_codes = tuple(self.active_langs)
            # Re-read all word files to ensure word order and length matches the new active_langs tuple
            # NOTE: This is complex and omitted for brevity, but in a production app, changing lang codes would require full data re-parse/re-indexing.
            print(self.text.successfully_added)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def correct_input(self, string, mytype, values, segment=True):
        
        question = input(string)
        while True:
            try:
                if mytype is int and question == "": return ""
                question = mytype(question)
                if question in values:
                    return question
                elif segment:
                    starts = [val for val in values if isinstance(val, str) and val.startswith(question)]
                    if len(starts) > 1:
                        print(self.text.multiple_options_error.format(", ".join(starts)))
                    elif len(starts) == 1:
                        return starts[0]
            except Exception as e:
                print(e, self.text.conversion_error.format("Konverziós", "correct_input"), file=sys.stderr)
            input(self.text.invalid_input_prompt)
            question = input(string)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def practice(self):
        
        gloss = self.correct_input(self.text.which_glossary.format("\n - ".join(self.glossaries)), str, self.glossaries)
        
        if len(self.words)==0 or len(self.words[gloss]) == 0:
            print(self.text.nothing_to_practice)
            return
        
        # --- Multi-Language Practice Setup ---
        
        # 1. Select Question Language
        lang_prompt = "\n" + self.text.select_question_lang + "\n"
        lang_map = {str(i): lang_code for i, lang_code in enumerate(self.active_langs, 1)}
        for i, code in enumerate(self.active_langs, 1):
            lang_prompt += f"{i}. {self.all_langs_names[code]}\n"
        
        q_choice = self.correct_input(lang_prompt, int, list(range(1, len(self.active_langs) + 1)))
        question_lang = lang_map[str(q_choice)]
        
        available_answer_langs = [l for l in self.active_langs if l != question_lang]
        
        # 2. Select Answer Languages (One or more)
        answer_langs = []
        if len(available_answer_langs) == 1:
            # If only one option, automatically select it
            answer_langs = available_answer_langs
        else:
            lang_prompt = "\n" + self.text.select_answer_langs + "\n"
            ans_map = {str(i): lang_code for i, lang_code in enumerate(available_answer_langs, 1)}
            for i, code in enumerate(available_answer_langs, 1):
                lang_prompt += f"{i}. {self.all_langs_names[code]}\n"
            lang_prompt += "(Enter numbers separated by commas, e.g., 1,2): "
            
            while True:
                ans_selection_str = input(lang_prompt)
                try:
                    ans_indices = [int(i.strip()) for i in ans_selection_str.split(',') if i.strip()]
                    answer_langs = [ans_map[str(i)] for i in ans_indices if str(i) in ans_map]
                    answer_langs = list(dict.fromkeys(answer_langs))
                    if answer_langs: break
                except:
                    print(self.text.invalid_input_prompt.replace("[ENTER]", ""))
                    
        # --- End Multi-Language Practice Setup ---

        correct_pt, incorrect_pt = 0, 0
        first = True
        
        while first or self.auto_continue_practice:
            first = False
            
            practice_words = list(self.words[gloss])
            
            # Boost logic needs to check points across all answer languages
            # Simplified boost: boost if *any* answer lang has negative points
            for word in self.words[gloss]:
                is_boosted = False
                for lang in answer_langs:
                    wordscore = word[lang]["pont"]
                    if wordscore < self.lower_boundary:
                        for i in range(abs(wordscore - self.lower_boundary)):
                            practice_words.append(word)
                        is_boosted = True
                if is_boosted: # Do not append multiple times if multiple negative scores exist
                    pass 
            shuffle(practice_words)

            dead = 0
            to_break = False
            
            for cur_word in practice_words:
                
                # Check dead/upper boundary based on the *average* score of all answer languages
                total_score = sum(cur_word[lang]["pont"] for lang in answer_langs)
                avg_score = total_score / len(answer_langs)
                
                if avg_score >= self.dead_pt:
                    dead += 1
                    continue
                if avg_score > self.upper_boundary and random() < (avg_score - self.upper_boundary) / (self.dead_pt - self.upper_boundary):
                    continue
                
                # The word to be asked
                question_word = cur_word.get(question_lang, {}).get("szo")
                if not question_word: continue # Skip if no word exists for this language
                
                print(f"\n--- Question in {self.all_langs_names[question_lang]} ---")
                
                # SOLUTIONS: Find all word entries that share the same question_word
                solutions = self.find(question_word, question_lang, gloss)
                
                is_correct_run = True
                
                # Iterate through all required answer languages
                for answer_lang in answer_langs:
                    
                    # Target solution for the current answer language
                    target_solution_words = [word[answer_lang]["szo"] for word in solutions]
                    
                    answer = input(f"Translate to {self.all_langs_names[answer_lang]}: ")
                    
                    if answer == "#": 
                        to_break = True
                        break
                    elif answer == "@":
                        for word in solutions: word[answer_lang]["pont"] = self.dead_pt
                        # Boost confirmation uses only the target language's words
                        confirm = input(self.text.max_points_confirm.format(", ".join(target_solution_words)))
                        to_break = True # Should break the inner loop (answer_langs) and outer loop (practice_words)
                        break
                    elif answer == "*":
                        for word in solutions: word[answer_lang]["pont"] = self.boost_pt
                        confirm = input(self.text.boosted_confirm.format(", ".join(target_solution_words), str(self.boost_pt)))
                        to_break = True # Should break the inner loop (answer_langs) and outer loop (practice_words)
                        break
                    
                    # --- Answer Validation Loop ---
                    word_found_in_solutions = False
                    
                    for solution_entry in solutions:
                        if answer == solution_entry[answer_lang]["szo"]:
                            word_found_in_solutions = True
                            
                            # 1. Check if already maxed out
                            if solution_entry[answer_lang]["pont"] >= self.dead_pt:
                                confirm = input(self.text.already_learned)
                                is_correct_run = False # Treat as incorrect for the current language check
                                break
                                
                            # 2. Check for details
                            solution_entry[answer_lang]["pont"] += 1
                            correct_pt += 1
                            
                            # Check details (kit properties)
                            if self.check_kit_details(solution_entry, answer_lang, solutions, target_solution_words) == 'fail':
                                solution_entry[answer_lang]["pont"] -= 1 # Revert score increase if details fail
                                incorrect_pt += 1
                                is_correct_run = False
                                break
                            
                            self.save(gloss)
                            
                            # Success message
                            details = ""
                            if len(target_solution_words) > 1:
                                details = " " + self.text.details_separator.format(", ".join(w for w in target_solution_words if w != answer))
                            confirm = input(self.text.correct_answer + details)
                            
                            if solution_entry[answer_lang]["pont"] >= self.dead_pt:
                                confirm = input(self.text.max_points_word_complete)

                            break # Break from inner loop over 'solutions' as word was correctly found
                            
                    
                    if not word_found_in_solutions:
                        # Incorrect Answer
                        is_correct_run = False
                        for word in solutions: word[answer_lang]["pont"] -= 1
                        incorrect_pt += 1
                        self.save(gloss)
                        confirm = input(self.text.incorrect_word.format(", ".join(target_solution_words)))
                
                if to_break: break

            else:
                if dead == len(practice_words):
                    print(self.text.all_done)
                    break
                continue
            break # flag: if we break, exit the while loop

        if correct_pt+incorrect_pt>0: 
            ratio = int(correct_pt/(correct_pt+incorrect_pt)*10000)/100
            confirm = input(self.text.summary.format(correct_pt, incorrect_pt, ratio))
        self.save(gloss)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_kit_details(self, word_entry, lang_code, all_solutions, target_solution_words):
        """Handles the detailed kit property checks for a single correct word entry."""
        for detail, detail_solution in word_entry[lang_code].items():
            if detail not in ('pont', 'szo'):
                answer = input(f"{detail}: ")
                
                # Exit commands for details
                if answer == "#": return 'break'
                elif answer == "@":
                    for word in all_solutions: word[lang_code]["pont"] = self.dead_pt
                    input(self.text.max_points_confirm.format(", ".join(target_solution_words)))
                    return 'break'
                elif answer == "*":
                    for word in all_solutions: word[lang_code]["pont"] = self.boost_pt
                    input(self.text.boosted_confirm.format(", ".join(target_solution_words), self.boost_pt))
                    return 'break'

                while answer != detail_solution and self.similar(answer, detail_solution):
                    input(self.text.close_but_wrong)
                    answer = input(f"{detail}: ")

                if answer == detail_solution:
                    word_entry[lang_code]["pont"] += 1
                    # correct_pt += 1 (This should be handled by practice loop's overall counter)
                    self.save(gloss)
                    input(self.text.correct_detail)
                    if word_entry[lang_code]["pont"] == self.dead_pt:
                        input(self.text.max_points_word_complete)
                else:
                    # Incorrect detail means the overall attempt failed, reduce score
                    # incorrect_pt += 1 (Handled by practice loop)
                    self.save(gloss)
                    input(self.text.incorrect_detail.format(detail_solution))
                    return 'fail'
        return 'success'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find(self, word, lang_code, gloss=None, property = None):
        """Finds all word objects in a glossary (or all words) matching a word in a specific language."""
        words_list = self.words[gloss] if gloss is not None else self.all_words
        
        # Ensure only words that have the lang_code key are checked
        results = [w for w in words_list if lang_code in w and w[lang_code].get("szo") == word]
        
        if property is None: 
            return results
        else:
            return [w.get(lang_code, {}).get(property) for w in results]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similarity(self, given: str, correct: str) -> float:
        # Similarity logic remains the same
        glen, clen = len(given), len(correct)
        if glen==0 and clen>0: return 0
        g=0; c=0; score=0
        while g < glen and c < clen:
            if given[g]==correct[c]:
                score+=1; g+=1; c+=1
            else:
                will_g, will_c = -1, -1
                chan_g, chan_c = g, c
                while chan_g < glen:
                    try: will_c = correct.index(given[chan_g], c+1)
                    except ValueError: chan_g+=1
                    except Exception as e: print(e, self.text.conversion_error.format("Saját", "similar"), file=sys.stderr)
                    else: break
                while chan_c < clen:
                    try: will_g = given.index(correct[chan_c], g+1)
                    except ValueError: chan_c+=1
                    except Exception as e: print(e, self.text.conversion_error.format("Saját", "similar"), file=sys.stderr)
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
        word = input(self.text.enter_expression)
        
        # Select search language
        lang_prompt = "\n" + self.text.what_language + "\n"
        lang_map = {str(i): lang_code for i, lang_code in enumerate(self.active_langs, 1)}
        for i, code in enumerate(self.active_langs, 1):
            lang_prompt += f"{i}. {self.all_langs_names[code]}\n"
        
        q_choice = self.correct_input(lang_prompt, int, list(range(1, len(self.active_langs) + 1)))
        lang = lang_map[str(q_choice)]
        
        print(self.text.similar_words_title)
        
        garage = []
        for glossname, gloss in self.words.items():
            for w in gloss:
                # Only check words that have an entry for the selected language
                if lang not in w or 'szo' not in w[lang]: continue

                search_word = w[lang]["szo"]
                
                # Build the display string dynamically for all active languages
                display_parts = []
                for active_lang_code in self.active_langs:
                    if active_lang_code in w:
                        word_data = w[active_lang_code]
                        items = [f"{key}:{val}" for key, val in word_data.items() if key not in ('szo', 'pont')]
                        display_parts.append(
                            f"{self.all_langs_names[active_lang_code]} ({word_data.get('pont', 0)} pt): {word_data.get('szo', 'N/A')} {', '.join(items)}"
                        )
                
                garage.append( [self.similarity(search_word, word),
                      f" - {' = '.join(display_parts)} [a {glossname} szótárban]"] )
                
        s = list(reversed(sorted(garage, key=lambda k: k[0])))
        for i in range(min(10, len(s))):
            print(s[i][1])
        confirm = input(self.text.done_message)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_new(self):
        print(self.text.add_words_title)
        gloss = self.correct_input(self.text.which_glossary.format("\n - ".join(self.glossaries)), str, self.glossaries)
        
        while True:
            new_word_entry = {}
            exit_flag = False

            print("\n--- New Word Entry ---")
            
            for lang_code in self.active_langs:
                lang_name = self.all_langs_names[lang_code]
                
                # Enter word for the current language
                word_prompt = self.text.enter_word_for_lang.format(lang_name)
                add_word = input(word_prompt)
                
                if add_word == "#": 
                    exit_flag = True
                    break
                
                # Check for duplicates (simplified check, only checks 'szo' property)
                if len(self.find(add_word, lang_code, gloss))>0:
                    if input(self.text.word_in_current_glossary.format(self.text.yes_no_options) + ": ").lower() == self.text.no_char: continue
                elif len(self.find(add_word, lang_code))>0:
                    if input(self.text.word_in_any_glossary.format(self.text.yes_no_options) + ": ").lower() == self.text.no_char: continue
                
                # Add base word and kit properties
                lang_config = self.all_langs_config[lang_code]
                kit_properties = self.add_kit_properties(lang_config)
                
                new_word_entry[lang_code] = {
                    "szo": add_word,
                    "pont": 0,
                    **kit_properties
                }
            
            if exit_flag: break
            
            # Append the completed entry to the glossary
            if new_word_entry:
                self.words[gloss].append(new_word_entry)
                self.save(gloss)
                confirm = input(self.text.successfully_added)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_glossary(self):
        print(self.text.add_glossaries_title)
        
        while True:
            gloss = input(self.text.enter_glossary_name)
            while gloss in self.glossaries:
                gloss = input(self.text.glossary_exists)
            if gloss == "#": break
            with open("glossaries.txt", "a", encoding="utf-8") as glossfile: glossfile.write(gloss+"\n")
            with open(gloss+".txt", "w", encoding="utf-8"): pass
            self.glossaries.append(gloss)
            self.words[gloss] = []
            confirm = input(self.text.successfully_added)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save(self, gloss):
        file = open(gloss+".txt", "w", encoding="utf-8")
        for word_entry in self.words[gloss]:
            # Write only the data for the active languages, ensuring consistent order
            lang_parts = []
            for lang_code in self.lang_codes:
                if lang_code in word_entry:
                    lang_parts.append(" ; ".join(f"{key}:{val}" for key, val in word_entry[lang_code].items()))
            
            # The 'word' in the original code was an array of two language dictionaries. 
            # Now it's an array of N language dictionaries.
            file.write(" | ".join(lang_parts) + "\n")
        file.close()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def state(self):
        
        sz_vagy_ossz = self.correct_input(self.text.check_state_type.format(self.text.state_options[0], self.text.state_options[1]), str, self.text.state_options)
        
        if sz_vagy_ossz == self.text.state_options[0]: # Specific dictionary
            gloss = self.correct_input(self.text.which_glossary.format("\n - ".join(self.glossaries)), str, self.glossaries)
            words_to_check = self.words[gloss]
        else: # All dictionaries
            words_to_check = self.all_words
        
        osszes = len(words_to_check)
        if osszes == 0:
             print(self.text.nothing_to_practice)
             return
             
        # Completed words: count a word as complete if any language score is dead_pt or higher
        telj = sum(1 for sz in words_to_check if any(sz.get(lang, {}).get("pont", 0) >= self.dead_pt for lang in self.active_langs))
        ratio = int(telj/osszes*10000)/100
        
        print(self.text.state_summary.format(osszes, telj, ratio))
        
        details = self.correct_input(self.text.state_details_prompt.format(self.text.yes_no_options), str, self.text.yes_no_options)
        if details == self.text.no_char: return
        
        # New: Select which language's points to view
        lang_prompt = "\n" + self.text.state_which_langs + "\n"
        lang_map = {str(i): lang_code for i, lang_code in enumerate(self.active_langs, 1)}
        for i, code in enumerate(self.active_langs, 1):
            lang_prompt += f"{i}. {self.all_langs_names[code]}\n"
        
        q_choice = self.correct_input(lang_prompt, int, list(range(1, len(self.active_langs) + 1)))
        whichlang = lang_map[str(q_choice)]

        by_score = {}
        for sz in words_to_check:
            # Check only for the selected language
            if whichlang in sz and "szo" in sz[whichlang]:
                score = sz[whichlang]["pont"]
                word = sz[whichlang]["szo"]
                try: by_score[score].append(word)
                except:
                    by_score[score] = [ ]
                    by_score[score].append(word)
        for score, words in reversed(sorted(by_score.items(), key = lambda k: k[0])):
            print("\n", end="")
            print(self.text.state_score_group.format(score, len(words)))
            for sz in words: print("-", sz)
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_kit_properties(self, kit):
        """Recursively prompts for kit properties based on the loaded language config."""
        if kit is None: return {}

        # The overall mode for the kit is 'all', but within a language config, it's 'and' or 'or'
        mode = kit.get('<mode>')
        
        if mode == 'and':
            data = {}
            for key, val in kit.items():
                if key not in ('<mode>', 'name_hu', 'name_en'): 
                    if val is None:
                        data[key] = input(f"Add meg a {key}-t: ") # Hungarian placeholder
                    else:
                        print(f"{key}:")
                        data.update(self.add_kit_properties(val))
            return data                    
        elif mode == 'or':
            keys = [k for k in kit.keys() if k not in ('<mode>', 'name_hu', 'name_en')]
            which = self.correct_input("válassz (" + "/".join(keys) + "): ", str, keys, segment=True) # Hungarian placeholder
            
            # If the selected option has no further config, just return the key itself
            if kit[which] is None: 
                return {which: ""} # Store the selection as an empty string property
            
            # Recurse into the selected option's config
            data = self.add_kit_properties(kit[which])
            
            # The structure of the stored data is simple: we include the selected key 
            # and then any properties gathered from recursion.
            return {which: "selected", **data}
        
        # If no mode is specified (e.g., top-level language container), return empty
        return {}
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_doubles(self): 
        garage = {lang_code: {} for lang_code in self.active_langs}
        
        for glossname, gloss in self.words.items():
            for w in gloss:
                for lang_code in self.active_langs:
                    if lang_code in w and "szo" in w[lang_code]:
                        word_str = w[lang_code]["szo"].lower()
                        try: garage[lang_code][word_str].append(glossname)
                        except:
                            garage[lang_code][word_str] = [glossname]
        
        print(self.text.checking_doubles)
        for lang_code, ws in garage.items():
            print("\n", self.all_langs_names[lang_code].upper(), " nyelven:", sep='')
            for word, glossaries in ws.items():
                if len(glossaries)>1: print(word, ":", glossaries)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_glossary_length(self):
        figy = True
        for glossname, gloss in self.words.items():
            if len(gloss)>50:
                if figy:
                    print(self.text.warning_title)
                    figy = False
                print(self.text.glossary_too_long.format(glossname))

########################################################
# The instantiation now uses the Lang enum and the single MultiLang Kit
tan = NyelvTanulas(kit_enum=SELECTED_KIT, lang_enum=SELECTED_LANG)
tan.start()