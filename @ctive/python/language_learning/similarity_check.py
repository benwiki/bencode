from vocab_learner_model import VocabLearnerModel, Kit

some_trial_word_pairs = [
    ("cat", "kat"),
    ("dog", "dog"),
    ("erunt", "êrunt"),
    ("house", "ház"),
    ("cucc", "cuccomb"),
    ("veryveryveryveryveryveryveryveryveryveryveryverylongword", "veryveryveryveryveryverylongwrd"),
]

def similarity_legacy(given: str, correct: str) -> float:
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

def main():
    kit = Kit.LATIN
    model = VocabLearnerModel(kit=kit)
    # Are two words similar?
    # while True:
    #     word = input("Enter the first word: ")
    #     other = input("Enter the second word: ")
    #     sim = model.similar(word, other)
    #     print(f"{word} and {other} are similar: {sim}")
    for word1, word2 in some_trial_word_pairs:
        sim = similarity_legacy(word1, word2)
        print(f"'{word1}' and '{word2}' are similar: {sim}")


if __name__ == "__main__":
    main()