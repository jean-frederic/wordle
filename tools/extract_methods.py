with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

import re

m = re.search(r'getWordOfTheDay\(\)', s)
if m:
    idx = m.start()
    print("Found getWordOfTheDay:")
    print(s[idx:idx+4000])
