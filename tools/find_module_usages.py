with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

import re

# Find occurrences of '32a3'
for m in re.finditer(r'32a3', s):
    idx = m.start()
    print("--- 32a3 occurrence ---")
    print(s[max(0, idx-100):min(len(s), idx+400)])

# Also find where the other array (the 202 words) is exported
m2 = re.search(r'\["AEROS"', s)
if m2:
    idx2 = m2.start()
    print("--- AEROS array context ---")
    print(s[max(0, idx2-100):idx2])
