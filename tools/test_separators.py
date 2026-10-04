import json
import math
import time
from collections import Counter

with open('target_words.json', 'r', encoding='utf-8') as f:
    target_words = json.load(f)

with open('all_words.json', 'r', encoding='utf-8') as f:
    all_words = json.load(f)

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

# Let's test after playing RAIES
first_guess = "RAIES"
# Group target words by their feedback against RAIES
buckets = {}
for t in target_words:
    p = get_feedback(first_guess, t)
    buckets.setdefault(p, []).append(t)

print(f"Total patterns produced by {first_guess}: {len(buckets)}")
sizes = [len(b) for b in buckets.values()]
print(f"Max bucket size: {max(sizes)}, Median: {sorted(sizes)[len(sizes)//2]}, Average: {sum(sizes)/len(sizes):.1f}")

# Check how many buckets have size <= 1 (already won in 2 or known in 2!)
size_1 = sum(1 for s in sizes if s == 1)
size_2_or_3 = sum(1 for s in sizes if 2 <= s <= 3)
print(f"Buckets with exactly 1 target: {size_1} (solved in 2 guaranteed!)")
print(f"Buckets with 2 or 3 targets: {size_2_or_3}")

# Let's test the largest bucket and see if we can find a word in all_words with max_bucket <= 1
largest_p = max(buckets.keys(), key=lambda p: len(buckets[p]))
largest_cands = buckets[largest_p]
print(f"\nLargest bucket (pattern {largest_p}): {len(largest_cands)} candidates: {largest_cands[:10]}...")

# Search for separating word in all_words for this largest bucket
best_w = None
min_max_b = 999
for w in all_words:
    sub_b = Counter(get_feedback(w, c) for c in largest_cands)
    max_b = max(sub_b.values())
    if max_b < min_max_b:
        min_max_b = max_b
        best_w = w
    if min_max_b <= 1:
        break

print(f"Best separator for largest bucket: '{best_w}' with max bucket {min_max_b}")
