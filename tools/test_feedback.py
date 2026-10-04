import json
import math
from collections import Counter

# Load target words and allowed words
with open('target_words.json', 'r', encoding='utf-8') as f:
    target_words = json.load(f)

with open('all_words.json', 'r', encoding='utf-8') as f:
    all_words = json.load(f)

print(f"Target words: {len(target_words)}, Allowed words: {len(all_words)}")

def get_feedback(guess, target):
    """
    Compute Wordle feedback for guess against target.
    0 = Grey (incorrect)
    1 = Yellow (partial)
    2 = Green (correct)
    Returns integer pattern in [0, 242] (3^5)
    """
    res = [0] * 5
    target_letters = list(target)
    
    # First pass: green
    for i in range(5):
        if guess[i] == target[i]:
            res[i] = 2
            target_letters[i] = None
            
    # Second pass: yellow
    for i in range(5):
        if res[i] == 0 and guess[i] in target_letters:
            res[i] = 1
            target_letters[target_letters.index(guess[i])] = None
            
    # Convert pattern to base-3 integer
    p = 0
    for v in res:
        p = p * 3 + v
    return p

# Test sample feedback
print("Test feedback ALORS vs AVOIR:", get_feedback("ALORS", "AVOIR"))
