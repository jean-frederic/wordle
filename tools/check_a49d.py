with open('chunk-vendors.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('a49d:')
if idx == -1:
    idx = text.find('"a49d":')
print(f"a49d found at {idx}:")
print(text[idx:idx+1500])
