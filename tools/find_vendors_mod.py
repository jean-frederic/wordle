with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = list(re.finditer(r'seedrandom', text, re.IGNORECASE))
print(f"Matches for seedrandom in vendors: {len(matches)}")
for m in matches[:5]:
    idx = m.start()
    print(text[max(0, idx-100):min(len(text), idx+200)])
    print("="*40)
