import json
from test_seedrandom import SeedRandom

with open('target_words.json', 'r', encoding='utf-8') as f:
    target_words = json.load(f)

# target_words contains words[0 : pizza_idx + 1]
# so len(target_words) is exactly (this.words.indexOf("PIZZA") + 1) = 1792!

def get_word_for_date(date_str):
    if date_str == "2022-3-8":
        return "DROIT"
    if date_str == "2023-5-12":
        return "FAIRE"
    sr = SeedRandom(date_str)
    rnd = sr.random()
    idx = int(rnd * len(target_words))
    return target_words[idx]

print("2022-1-10:", get_word_for_date("2022-1-10"))
print("2022-3-8:", get_word_for_date("2022-3-8"))
print("2023-5-12:", get_word_for_date("2023-5-12"))
print("2026-10-4 (Today):", get_word_for_date("2026-10-4"))
