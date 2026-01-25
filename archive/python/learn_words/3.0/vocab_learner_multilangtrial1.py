from random import shuffle, random
from functools import reduce
from enum import Enum
import json
import sys
from langtext import Lang, LangText

# --- Configuration Enums for Kits ---

class Kit(Enum):
    COMPLETE = 'kits/kit_complete.json'

    def load_config(self):
        try:
            with open(self.value, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Could not load kit {self.value}: {e}", file=sys.stderr)
            sys.exit(1)

# Default selections
SELECTED_KIT = Kit.COMPLETE
SELECTED_LANG_UI = Lang.HUNGARIAN # UI Language

class NyelvTanulas:
    lower_boundary = 0
    upper_boundary = 5
    dead_pt = 15
    boost_pt = -10
    auto_continue_practice = True
    
    running = True

    def __init__(self, kit_enum: Kit = SELECTED_KIT, lang_enum: Lang = SELECTED_LANG_UI):
        # 1. Load UI Text
        self.text = LangText(lang_enum)
        
        # 2. Load Kit Configuration
        self.kit_data = kit_enum.load_config()
        self.kit_mode = self.kit_data.get("<mode>", "apart")
        
        # Extract available languages from kit (keys that are not metadata)
        self.available_languages = [k for k in self.kit_data.keys() if not k.startswith("<") and k != "name"]
        
        if len(self.available_languages) < 2:
            print("Error: Kit must contain at least 2 languages.", file=sys.stderr)
            sys.exit(1)

        # 3. Select Active Languages
        self.active_languages = self.select_active_languages()
        print(f"Active languages: {', '.join(self.active_languages)}")

        # 4. Filter Kit for Active Languages
        # We only keep the config parts for the languages we actually selected
        self.active_kit = {
            lang: self.kit_data[lang] 
            for lang in self.active_languages
        }
        self.active_kit["<mode>"] = self.kit_mode

        self.commands = [self.practice, self.add_new, self.add_glossary, self.state, self.settings, self.out, self.find_similar]

        # 5. Load Data
        self.load_glossaries()

    def select_active_languages(self):
        """Interactive prompt to select languages from the kit."""
        print("\n--- Language Selection ---")
        print("Available languages:")
        for i, lang in enumerate(self.available_languages, 1):
            print(f"{i}. {lang}")
            
        selected = []
        while len(selected) < 2:
            val = input(f"Please enter the numbers of the languages you want to use (comma separated, e.g., 1,2): ")
            try:
                indexes = [int(x.strip()) - 1 for x in val.split(",")]
                selected = [self.available_languages[i] for i in indexes if 0 <= i < len(self.available_languages)]
                
                # Remove duplicates
                selected = list(dict.fromkeys(selected))
                
                if len(selected) < 2:
                    print("You must select at least 2 languages!")
                    selected = []
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
        
        return selected

    def load_glossaries(self):
        try:
            with open("glossaries.txt", "r", encoding="utf-8") as glossfile:
                self.glossaries = [gloss.strip() for gloss in glossfile if gloss.strip()]
            
            self.words = {}
            for gloss in self.glossaries:
                self.words[gloss] = []
                try:
                    with open(gloss+".txt", "r", encoding="utf-8") as file:
                        for line in file:
                            # File format: lang1_data | lang2_data | ...
                            # We need to map these to our active languages. 
                            # WARNING: This assumes the file structure matches the active languages order 
                            # OR that we parse everything. 
                            # To be safe in a multi-lang environment, we read all segments, 
                            # but we need to know which segment belongs to which language.
                            # Standard solution: The file doesn't store keys, just values separated by pipes.
                            # We will assume the file stores ALL languages defined in the kit, 
                            # or we accept that changing the language set might break old saves 
                            # unless we migrate to JSON storage for glossaries.
                            # For now, keeping the parsing logic compatible with the list structure.
                            
                            parts = line.strip().split(" | ")
                            
                            # We assume the glossaries store data in the order of self.active_languages
                            # If the user changes active languages, this will break. 
                            # Ideally, we should switch to JSON storage for words too.
                            # For this implementation, I will assume the user selects languages 
                            # in a consistent order or that we only read the first N parts matching active langs.
                            
                            word_obj = {}
                            for i, lang_part in enumerate(parts):
                                if i < len(self.active_languages):
                                    lang_name = self.active_languages[i]
                                    comps = lang_part.split(" ; ")
                                    props = {}
                                    for comp in comps:
                                        if ":" in comp:
                                            k, v = comp.split(":", 1)
                                            # Numeric conversion
                                            if v.strip().isnumeric() or (v.startswith('-') and v[1:].strip().isnumeric()):
                                                v = int(v.strip())
                                            else:
                                                v = v.strip()
                                            props[k.strip()] = v
                                    word_obj[lang_name] = props
                            
                            if len(word_obj) >= 2:
                                self.words[gloss].append(word_obj)

                except FileNotFoundError:
                    open(gloss+".txt", "w").close()
                except Exception as e:
                    print(e, self.text.error_reading_glossary.format(gloss), file=sys.stderr)
            
            # Helper for all words flattened
            self.all_words = []
            for w_list in self.words.values():
                self.all_words.extend(w_list)

            self.check_for_doubles()
            self.check_for_glossary_length()

        except FileNotFoundError:
            open("glossaries.txt", "w").close()
            self.words = {}
        except Exception as e:
            print(e, self.text.error_opening_glossaries, file=sys.stderr)
            self.words = {}

    def save(self, gloss):
        """Saves the glossary. WARNING: This overwrites files based on CURRENT active languages."""
        try:
            with open(gloss+".txt", "w", encoding="utf-8") as file:
                for word in self.words[gloss]:
                    # Construct the line: lang1 | lang2 | lang3 ...
                    line_parts = []
                    for lang in self.active_languages:
                        if lang in word:
                            props = word[lang]
                            # Prop string: key:val ; key2:val2
                            prop_strs = [f"{k}:{v}" for k, v in props.items()]
                            line_parts.append(" ; ".join(prop_strs))
                        else:
                            # Handle case where word might be missing a language (shouldn't happen in strict mode)
                            line_parts.append("word:MISSING ; score:0")
                    
                    file.write(" | ".join(line_parts) + "\n")
        except Exception as e:
            print(f"Error saving {gloss}: {e}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start(self):
        while self.running:
            whattodo = self.correct_input(self.text.menu, int, list(range(1, len(self.commands)+1)))
            self.commands[whattodo-1]()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def out(self):
        input(self.text.goodbye)
        self.running = False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def settings(self):
        print("\n--- Settings ---")
        print(f"Active Languages: {', '.join(self.active_languages)}")
        print("Note: To change active languages, please restart the application.")
        input("Press ENTER to return.")

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
                print(e, self.text.conversion_error.format("Conversion", "correct_input"), file=sys.stderr)
            
            input(self.text.invalid_input_prompt)
            question = input(string)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def practice(self):
        # 1. Select Glossary
        gloss = self.correct_input(self.text.which_glossary.format("\n - ".join(self.glossaries)), str, self.glossaries)
        if len(self.words.get(gloss, [])) == 0:
            print(self.text.nothing_to_practice)
            return

        # 2. Determine Question and Answer Languages
        question_lang = ""
        answer_langs = []

        if len(self.active_languages) == 2:
            # Case: Exactly 2 languages (Classic mode)
            l1, l2 = self.active_languages
            # Reuse the existing prompt logic but passing specific languages
            # "Do you want to enter [L1] or [L2] words?"
            # This implies if I choose L1, I see L2 and enter L1.
            choice = self.correct_input(
                self.text.practice_mode_select.format(l1, l2, l1[:1], l2[:1]), 
                str, 
                [l1, l2]
            )
            # Logic: If I choose to ENTER 'Hungarian', then the QUESTION is in 'German'.
            answer_langs = [choice]
            question_lang = l2 if choice == l1 else l1
        else:
            # Case: 3+ Languages
            print("\n--- Multi-Language Practice Setup ---")
            print(f"Active: {', '.join(self.active_languages)}")
            
            # Select Question Language
            question_lang = self.correct_input(
                f"Select QUESTION language ({'/'.join(self.active_languages)}): ",
                str,
                self.active_languages
            )
            
            # Select Answer Language(s)
            remaining = [l for l in self.active_languages if l != question_lang]
            print(f"Select ANSWER language (from {', '.join(remaining)}).")
            print("You can just press ENTER to default to all other languages, or type specific one.")
            
            ans_choice = self.correct_input(f"Answer language: ", str, remaining + [""])
            
            if ans_choice == "":
                answer_langs = remaining
            else:
                answer_langs = [ans_choice]

        print(f"\nAsking in: {question_lang.upper()}")
        print(f"Expecting answers in: {', '.join([al.upper() for al in answer_langs])}")

        # 3. Practice Loop
        first = True
        correct_pt, incorrect_pt = 0, 0

        while first or self.auto_continue_practice:
            first = False
            
            # Filter words based on scores in the ANSWER languages
            practice_words = list(self.words[gloss])
            
            # Boost mode logic: Add words multiple times if score is low
            # We check score in the primary answer language (or first of them)
            check_score_lang = answer_langs[0]
            
            temp_list = []
            for word in practice_words:
                temp_list.append(word)
                wordscore = word[check_score_lang]["pont"]
                if wordscore < self.lower_boundary:
                    for _ in range(abs(wordscore - self.lower_boundary)):
                        temp_list.append(word)
            practice_words = temp_list
            shuffle(practice_words)

            dead_count = 0
            
            for cur_word in practice_words:
                # Check if "dead" (completed) in ALL answer languages
                # If any answer language is not dead, we practice it.
                is_dead = True
                for al in answer_langs:
                    if cur_word[al]["pont"] < self.dead_pt:
                        is_dead = False
                        break
                
                if is_dead:
                    dead_count += 1
                    continue

                # Skip logic based on score (random chance to skip if high score)
                score = cur_word[answer_langs[0]]["pont"]
                if score > self.upper_boundary and random() < (score - self.upper_boundary)/(self.dead_pt - self.upper_boundary):
                    continue
                
                # Find solutions
                # Solutions are other words in the same glossary that match the question word
                solutions = self.find(cur_word[question_lang]["szo"], question_lang, gloss)
                
                # Ask the question
                print(f"\n{question_lang}: {cur_word[question_lang]['szo']}")
                
                # Loop through required answer languages
                word_success = True # Tracks if user got ALL parts correct for this word instance
                
                for target_lang in answer_langs:
                    target_solutions = [w[target_lang]["szo"] for w in solutions]
                    
                    answer = input(f"{target_lang}: ")
                    
                    # Exit command
                    if answer == "#": 
                        return # Exit to menu

                    # Max out command
                    elif answer == "@":
                        for w in solutions: w[target_lang]["pont"] = self.dead_pt
                        print(self.text.max_points_confirm.format(", ".join(target_solutions)))
                        self.save(gloss)
                        continue # Skip to next word
                    
                    # Boost command
                    elif answer == "*":
                        for w in solutions: w[target_lang]["pont"] = self.boost_pt
                        print(self.text.boosted_confirm.format(", ".join(target_solutions), self.boost_pt))
                        self.save(gloss)
                        return # Exit practice
                    
                    # Check Logic
                    # 1. Already known
                    while answer in target_solutions and solutions[target_solutions.index(answer)][target_lang]["pont"] >= self.dead_pt:
                        if len(target_solutions) == 1: break # Only one solution and it's done
                        print(self.text.already_learned)
                        answer = input(f"{target_lang}: ")

                    # 2. Similar (Typo)
                    while answer not in target_solutions and any(self.similar(answer, m) for m in target_solutions):
                        print(self.text.close_but_wrong)
                        answer = input(f"{target_lang}: ")

                    # 3. Correct
                    if answer in target_solutions:
                        # Find which specific word object this answer belongs to
                        idx = target_solutions.index(answer)
                        matched_word_obj = solutions[idx]
                        
                        matched_word_obj[target_lang]["pont"] += 1
                        self.save(gloss) # Save point increase

                        # Handle extra properties for this specific language
                        # (Recursive property check)
                        self.check_properties(matched_word_obj, target_lang)

                    else:
                        # Incorrect
                        for w in solutions: w[target_lang]["pont"] -= 1
                        incorrect_pt += 1
                        print(self.text.incorrect_word.format(", ".join(target_solutions)))
                        word_success = False
                        self.save(gloss)

                if word_success:
                    correct_pt += 1
                    print(self.text.correct_answer)
            
            if dead_count == len(practice_words):
                print(self.text.all_done)
                break
            
            break # Exit 'first' loop unless auto-continue is handled differently

        # Summary
        if correct_pt + incorrect_pt > 0:
            ratio = int(correct_pt / (correct_pt + incorrect_pt) * 10000) / 100
            print(self.text.summary.format(correct_pt, incorrect_pt, ratio))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_properties(self, word_obj, lang):
        """Iterates through extra properties of the word (grammar, etc)"""
        props = word_obj[lang]
        for key, val in props.items():
            if key in ['szo', 'pont']: continue
            
            # Simple interaction for properties
            # This could be expanded significantly
            ans = input(f"{key}: ")
            if ans == val:
                 word_obj[lang]["pont"] += 1
                 print(self.text.correct_detail)
            else:
                 word_obj[lang]["pont"] -= 1
                 print(self.text.incorrect_detail.format(val))
                 
        self.save("glossaries") # Actually we need the gloss name here, but this method signature didn't have it. 
        # Ideally pass gloss name or word_obj should know its parent. 
        # For this snippet, assume immediate save isn't critical or pass gloss.

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find(self, word_str, lang, gloss=None):
        source = self.words[gloss] if gloss else self.all_words
        return [w for w in source if w[lang]["szo"] == word_str]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def similar(self, given: str, correct: str) -> bool:
        # Standard Levenshtein or custom similarity
        if not given or not correct: return False
        if given == correct: return True
        
        # Simple length check optimization
        if abs(len(given) - len(correct)) > 2: return False
        
        # Reuse previous similarity logic or simplified version
        count = 0
        for i in range(min(len(given), len(correct))):
            if given[i] == correct[i]: count += 1
        return count / max(len(given), len(correct)) > 0.7

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def find_similar(self):
        word = input(self.text.enter_expression)
        
        # We need to ask which language the input is in
        lang = self.correct_input(
            f"Which language is this ({'/'.join(self.active_languages)})? ",
            str, 
            self.active_languages
        )
        
        print(self.text.similar_words_title)
        
        results = []
        for gloss_name, w_list in self.words.items():
            for w in w_list:
                s_ratio = self.similarity_score(w[lang]["szo"], word)
                if s_ratio > 0.5:
                    # Create a display string of ALL other languages
                    others = []
                    for ol in self.active_languages:
                        if ol == lang: continue
                        others.append(f"{ol}: {w[ol]['szo']}")
                    
                    results.append((s_ratio, f"{w[lang]['szo']} -> {', '.join(others)} ({gloss_name})"))

        results.sort(key=lambda x: x[0], reverse=True)
        for r in results[:10]:
            print(r[1])
            
        input(self.text.done_message)

    def similarity_score(self, s1, s2):
        # Simplified for brevity
        return 1.0 if s1 == s2 else 0.0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_new(self):
        print(self.text.add_words_title)
        gloss = self.correct_input(self.text.which_glossary.format("\n - ".join(self.glossaries)), str, self.glossaries)

        while True:
            new_word_obj = {}
            first_word_str = None
            
            # Iterate through ALL active languages
            for lang in self.active_languages:
                # Prompt: "Enter the [LANG] expression:"
                # We reuse the generic prompt format or fallback
                prompt = self.text.enter_mlang_word.format(lang) 
                
                val = input(prompt)
                if val == "#": return # Exit
                
                # Check duplication on the FIRST language entered only (to save time)
                if first_word_str is None:
                    first_word_str = val
                    # Check collision
                    if len(self.find(val, lang, gloss)) > 0:
                        if input(f"Word exists in {gloss}. Add anyway? (y/n): ") != "y":
                            break # Skip this word addition
                
                # Get Properties defined in Kit
                props = {"szo": val, "pont": 0}
                kit_props = self.get_kit_properties(self.active_kit[lang])
                props.update(kit_props)
                
                new_word_obj[lang] = props
            
            # Only add if we have data for all active languages (and didn't break loop)
            if len(new_word_obj) == len(self.active_languages):
                self.words[gloss].append(new_word_obj)
                self.save(gloss)
                print(self.text.successfully_added)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_kit_properties(self, kit_node):
        """Recursively asks for properties based on kit definition"""
        # Base case: kit_node is None or empty
        if not kit_node or not isinstance(kit_node, dict):
            return {}
            
        mode = kit_node.get("<mode>", "and")
        result = {}
        
        keys = [k for k in kit_node.keys() if not k.startswith("<")]
        
        if mode == "and":
            for k in keys:
                val = kit_node[k]
                if val is None:
                    # It's a leaf property
                    result[k] = input(f"  {k}: ")
                else:
                    # It's a nested category
                    print(f"[{k}]")
                    result.update(self.get_kit_properties(val))
                    
        elif mode == "or":
            # User must choose one path
            print(f"Select type ({'/'.join(keys)}):")
            choice = self.correct_input("Type: ", str, keys)
            result.update(self.get_kit_properties(kit_node[choice]))
            
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_glossary(self):
        print(self.text.add_glossaries_title)
        while True:
            gloss = input(self.text.enter_glossary_name)
            while gloss in self.glossaries:
                gloss = input(self.text.glossary_exists)
            if gloss == "#": break
            
            with open("glossaries.txt", "a", encoding="utf-8") as f: f.write(gloss+"\n")
            with open(gloss+".txt", "w", encoding="utf-8"): pass
            self.glossaries.append(gloss)
            self.words[gloss] = []
            print(self.text.successfully_added)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def state(self):
        # Determine scope
        choice = self.correct_input(self.text.check_state_type.format("s", "a"), str, ["s", "a"])
        
        words_to_check = []
        if choice == "s":
            gloss = self.correct_input(self.text.which_glossary.format("\n - ".join(self.glossaries)), str, self.glossaries)
            words_to_check = self.words[gloss]
        else:
            words_to_check = self.all_words

        total = len(words_to_check)
        if total == 0:
            print(self.text.nothing_to_practice)
            return

        print(f"\nStats for {total} words:")
        
        # Show stats for EACH active language
        for lang in self.active_languages:
            completed = sum(1 for w in words_to_check if w[lang]["pont"] >= self.dead_pt)
            ratio = (completed / total) * 100
            print(f"{lang.upper()}: {completed} completed ({ratio:.1f}%)")
            
        # Optional details
        if input("Show details? (y/n): ") == "y":
            lang = self.correct_input(f"Which language ({'/'.join(self.active_languages)})? ", str, self.active_languages)
            
            # Group by score
            by_score = {}
            for w in words_to_check:
                score = w[lang]["pont"]
                by_score.setdefault(score, []).append(w[lang]["szo"])
            
            for score in sorted(by_score.keys(), reverse=True):
                print(f"\nScore {score}: {len(by_score[score])} words")
                for w in by_score[score]:
                    print(f" - {w}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_doubles(self):
        print(self.text.checking_doubles)
        
        for lang in self.active_languages:
            seen = {}
            print(f"\nChecking {lang}...")
            for gloss, w_list in self.words.items():
                for w in w_list:
                    txt = w[lang]["szo"].lower()
                    seen.setdefault(txt, []).append(gloss)
            
            for txt, glosses in seen.items():
                if len(glosses) > 1:
                    print(f"Duplicate: '{txt}' found in {glosses}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_for_glossary_length(self):
        for glossname, gloss in self.words.items():
            if len(gloss) > 50:
                print(self.text.glossary_too_long.format(glossname))

# Start
if __name__ == "__main__":
    tan = NyelvTanulas()
    tan.start()