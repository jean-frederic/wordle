with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

import re

m = re.search(r'const u="2\.3\.0"', s)
if m:
    idx = m.start()
    print("Found Game component definitions:")
    print(s[idx:idx+4000])
