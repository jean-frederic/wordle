import re
import json

with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

# Look for arrays of 5-letter words
matches = list(re.finditer(r'\["[a-z]{5}"(?:,"[a-z]{5}")+\]', s, re.IGNORECASE))
print(f"Found {len(matches)} matching string arrays in app.js")
for i, m in enumerate(matches):
    arr = json.loads(m.group(0))
    print(f"Array {i}: length {len(arr)} words, sample: {arr[:5]}... last: {arr[-5:]}")
