import re

with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

# Find occurrences of the word arrays or daily puzzle logic
for m in re.finditer(r'COMME', s):
    idx = m.start()
    print("--- Context around COMME ---")
    print(s[max(0, idx-200):min(len(s), idx+1000)])
    break

# Search for date or day calculations (e.g. Date.now, Math.floor, day offset, etc.)
for m in re.finditer(r'new Date|Date\.now|localStorage', s):
    idx = m.start()
    print("--- Context around Date/Storage ---")
    print(s[max(0, idx-100):min(len(s), idx+200)])
    print("="*40)
