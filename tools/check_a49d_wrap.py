with open('chunk-vendors.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('a49d:')
print(text[idx:idx+300])
idx2 = text.find('})(', idx)
print(text[idx2:idx2+200])
