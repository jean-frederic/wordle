with open('chunk-vendors.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sub = text[97319:97319+2500]
print("Snippet from 97319:")
print(sub[:500])
# find next module pattern like },"key":
matches = list(re.finditer(r'\},["\']?[a-zA-Z0-9_$]+["\']?:function', sub))
for m in matches:
    print("Next module at offset", m.start(), ":", m.group(0))
