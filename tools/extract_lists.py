import json
import re

with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

# Extract 32a3 (words)
idx1 = s.find('["COMME"')
idx1_end = s.find(']', idx1)
words = json.loads(s[idx1:idx1_end+1])

# Extract second array
idx2 = s.find('["AEROS"')
idx2_end = s.find(']', idx2)
allowed_extra = json.loads(s[idx2:idx2_end+1])

pizza_idx = words.index('PIZZA')
print(f"Total words in main list: {len(words)}")
print(f"Total words in extra list: {len(allowed_extra)}")
print(f"Total allowed guesses: {len(words) + len(allowed_extra)}")
print(f"Index of 'PIZZA': {pizza_idx}")
print(f"Candidate pool size (words[0 : {pizza_idx + 1}]): {pizza_idx + 1}")

with open('target_words.json', 'w', encoding='utf-8') as f:
    json.dump(words[:pizza_idx + 1], f, ensure_ascii=False, indent=2)

with open('all_words.json', 'w', encoding='utf-8') as f:
    json.dump(words + allowed_extra, f, ensure_ascii=False, indent=2)

print("Saved target_words.json and all_words.json successfully.")
