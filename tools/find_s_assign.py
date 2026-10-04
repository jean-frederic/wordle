with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('"56d7":function')
idx_end = text.find('seedrandom:s', idx)
print("From 56d7 to seedrandom:s :")
# find all occurrences of ',s=' or 'var s=' or 'let s=' or ';s='
import re
for m in re.finditer(r'[,;]s\s*=', text[idx:idx_end]):
    pos = idx + m.start()
    print(text[pos-20:pos+80])
