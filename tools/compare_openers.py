import json
from collections import Counter

with open('target_words.json', 'r', encoding='utf-8') as f:
    target_words = json.load(f)

def get_feedback(guess, target):
    res = [0] * 5
    t_letters = list(target)
    for i in range(5):
        if guess[i] == target[i]:
            res[i] = 2
            t_letters[i] = None
    for i in range(5):
        if res[i] == 0 and guess[i] in t_letters:
            res[i] = 1
            t_letters[t_letters.index(guess[i])] = None
    p = 0
    for v in res:
        p = p * 3 + v
    return p

openers = ["RAIES", "AIRES", "TAIRE", "TARES", "CARIE", "TIRES", "SORTE", "AUTRE", "TARIE"]

for op in openers:
    counts = Counter(get_feedback(op, t) for t in target_words)
    max_b = max(counts.values())
    # Expected candidates remaining: sum(c^2) / N
    N = len(target_words)
    exp_cands = sum(c*c for c in counts.values()) / N
    num_buckets = len(counts)
    cands_le_3 = sum(c for c in counts.values() if c <= 3)
    print(f"{op:6s} | buckets: {num_buckets:3d} | max_bucket: {max_b:3d} | exp_remaining: {exp_cands:5.1f} | targets <= 3 left: {cands_le_3:4d} ({cands_le_3/N*100:.1f}%)")
