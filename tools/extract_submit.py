with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

import re

m = re.search(r'this\.wordOfTheDay=this\.words\[', s)
if m:
    idx = m.start()
    print("Found wordOfTheDay assignment:")
    print(s[idx:idx+2000])

m2 = re.search(r'submitAttempt|validateAttempt|checkWord', s)
if m2:
    idx = m2.start()
    print("Found submit/validate:")
    print(s[idx-100:idx+2000])
else:
    print("submitAttempt not found, searching handleKeyClick:")
    m3 = re.search(r'handleKeyClick\(', s)
    if m3:
        idx = m3.start()
        print(s[idx:idx+2500])
