import json
import math
import time
from collections import Counter

with open('target_words.json', 'r', encoding='utf-8') as f:
    target_words = json.load(f)

with open('all_words.json', 'r', encoding='utf-8') as f:
    all_words = json.load(f)

N = len(target_words)

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

print(f"Calculating entropy for candidate words...")
t0 = time.time()

# Precompute or evaluate the target words themselves first
scored_words = []
for guess in target_words:
    pattern_counts = Counter()
    for target in target_words:
        p = get_feedback(guess, target)
        pattern_counts[p] += 1
    
    # Entropy: sum(- (count / N) * log2(count / N))
    # = log2(N) - (1/N) * sum(count * log2(count))
    entropy = 0.0
    for count in pattern_counts.values():
        p = count / N
        entropy -= p * math.log2(p)
        
    scored_words.append((entropy, guess, max(pattern_counts.values())))

scored_words.sort(key=lambda x: x[0], reverse=True)
t1 = time.time()
print(f"Done in {t1 - t0:.2f}s")
print("\nTop 20 opening target words:")
for rank, (ent, word, max_bucket) in enumerate(scored_words[:20], 1):
    avg_left = sum(c*c for c in [N * (2**(-ent))]) # approximate
    print(f"{rank:2d}. {word} : {ent:.3f} bits (max group: {max_bucket})")
