import json
import math
import time
from collections import Counter, defaultdict

with open('target_words.json', 'r', encoding='utf-8') as f:
    target_words = json.load(f)

with open('all_words.json', 'r', encoding='utf-8') as f:
    all_words = json.load(f)

TARGET_SET = set(target_words)
ALL_SET = set(all_words)

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

def filter_candidates(candidates, guess, pattern):
    return [c for c in candidates if get_feedback(guess, c) == pattern]

def choose_best_guess(candidates, turn):
    """
    Choose the best guess for the current candidate list.
    If len(candidates) <= 2, just guess the first candidate.
    """
    N = len(candidates)
    if N <= 2:
        return candidates[0]
    
    cand_set = set(candidates)
    
    # We want to search for the word that gives the best partition.
    # To be fast, candidate words are evaluated, plus top general words if needed.
    # When targeting 2 or 3 guesses:
    # On turn 2:
    # 1. If any word in candidates gives max_bucket == 1, pick it! (Guarantees win in <= 3, and chance to win on turn 2!)
    # 2. If any word in all_words gives max_bucket == 1, pick candidate if possible, or sacrifice word.
    
    best_word = None
    best_score = (-1, -1000, False) # (is_guarantee_3, entropy, is_candidate)
    
    # Check candidates first
    cand_eval = []
    for guess in candidates:
        buckets = Counter()
        for target in candidates:
            buckets[get_feedback(guess, target)] += 1
        
        max_bucket = max(buckets.values())
        entropy = -sum((count / N) * math.log2(count / N) for count in buckets.values())
        # Target bias: winning immediately on this turn has probability 1/N
        # When N is small (e.g. <= 6), probability of direct win is huge!
        cand_eval.append((max_bucket, entropy, guess))
        
    cand_eval.sort(key=lambda x: (x[0], -x[1]))
    
    # If best candidate already has max_bucket <= 1, it guarantees win on turn 3 and can win on turn 2!
    if cand_eval[0][0] <= 1:
        return cand_eval[0][2]
        
    # If candidates is relatively small (e.g. <= 30), also consider sacrifice words from all_words
    # that might perfectly separate all candidates (max_bucket = 1)
    if N <= 15:
        # Check if an outside word can achieve max_bucket == 1
        for guess in all_words:
            # Quick check: distinct letters
            buckets = Counter()
            possible_perfect = True
            for target in candidates:
                p = get_feedback(guess, target)
                buckets[p] += 1
                if buckets[p] > 1:
                    possible_perfect = False
                    break
            if possible_perfect:
                # Outside word perfectly separates all candidates!
                # But wait, cand_eval[0][2] might win now with prob 1/N.
                # If cand_eval[0][0] == 2, that means with candidate guess we win in 2 (prob 1/N)
                # or win in 3 (prob (N-1)/N). That's also max 3!
                if cand_eval[0][0] <= 2:
                    return cand_eval[0][2]
                return guess

    # In general, pick highest entropy candidate with tie-breaking for target membership
    cand_eval.sort(key=lambda x: (-x[1], x[0]))
    return cand_eval[0][2]

# Let's test on 100 sample words
first_guess = "RAIES"
results = Counter()
t0 = time.time()
sample_targets = target_words[:200]
print(f"Simulating first {len(sample_targets)} targets with opening '{first_guess}'...")

for target in sample_targets:
    cands = target_words[:]
    turns = 0
    guess = first_guess
    while True:
        turns += 1
        if guess == target:
            results[turns] += 1
            break
        p = get_feedback(guess, target)
        cands = filter_candidates(cands, guess, p)
        guess = choose_best_guess(cands, turns + 1)

t1 = time.time()
print(f"Simulation done in {t1 - t0:.2f}s")
print(f"Distribution: {dict(sorted(results.items()))}")
avg_turns = sum(k*v for k, v in results.items()) / len(sample_targets)
print(f"Average attempts: {avg_turns:.3f}")
pct_2_or_3 = (results[1] + results[2] + results[3]) / len(sample_targets) * 100
print(f"Solved in <= 3 attempts: {pct_2_or_3:.1f}%")
