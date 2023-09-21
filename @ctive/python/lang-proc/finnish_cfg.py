rules = {
    "sentence": [
        "noun_phrase| |verb_phrase",
        "verb_phrase| |noun_phrase_acc",
        "verb_phrase"
    ],
    # "noun_verb_phrase": [
    #     "noun_phrase verb_phrase"
    # ],
    "noun_phrase": [
        "noun_ending_in_long_a|a",
        "noun_ending_in_long_e|e",
        "noun_ending_in_long_i|i",
        "noun_ending_in_long_o|o",
        "noun_ending_in_long_u|u",
        "noun_ending_in_long_y|y",
        "noun_ending_in_long_ä|ä",
        "noun_ending_in_long_ö|ö",

        "noun_ending_in_long_a|i|noun_case",
        "noun_ending_in_long_e|i|noun_case",
        "noun_ending_in_long_i|i|noun_case",
        "noun_ending_in_long_o|i|noun_case",
        "noun_ending_in_long_u|i|noun_case",
        "noun_ending_in_long_y|i|noun_case",
        "noun_ending_in_long_ä|i|noun_case",
        "noun_ending_in_long_ö|i|noun_case",

        "monosyllabic_noun",

        "noun"
    ],
    "noun_phrase_acc": [
        "noun|noun_acc"
    ],
    "verb_phrase": [
        ["verb|verb_conjugation"]
    ],
    "verb_conjugation": [
        ""
    ],
    "adjective": [
        
    ],
    "adjective_acc": [
        
    ]
}
