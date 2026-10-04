with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Look for variable definitions around "data(){return{seedrandom:s"
idx = text.find('seedrandom:s')
print(text[max(0, idx-1000):idx])
