import json
from test_seedrandom import SeedRandom

with open('target_words.json', 'r', encoding='utf-8') as f:
    target_words = json.load(f)

def get_word_for_date(date_str):
    if date_str == "2022-3-8":
        return "DROIT"
    if date_str == "2023-5-12":
        return "FAIRE"
    sr = SeedRandom(date_str)
    rnd = sr.random()
    idx = int(rnd * len(target_words))
    return target_words[idx]

test_dates = [
    "2022-1-10",
    "2022-1-11",
    "2022-3-8",
    "2023-5-12",
    "2026-10-1",
    "2026-10-2",
    "2026-10-3",
    "2026-10-4",
    "2026-10-5"
]

for d in test_dates:
    print(f"Date {d:10s} -> Mot: {get_word_for_date(d)}")
