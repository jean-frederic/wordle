with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

import re

# Look for handleKeyClick inside methods:
matches = [m.start() for m in re.finditer(r'handleKeyClick\(E\)', s)]
for idx in matches:
    print("handleKeyClick(E) found:")
    print(s[idx:idx+2500])
    print("="*40)
