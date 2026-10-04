with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('"56d7":function')
idx_end = text.find('"Game"', idx)
snippet = text[idx:idx_end]
# find all occurrences of 's=' or 's =' or similar
import re
print("Matches for s = :")
for m in re.finditer(r'\b[a-zA-Z0-9_$]+\s*=\s*t\([^)]+\)', snippet):
    print(m.group(0))
