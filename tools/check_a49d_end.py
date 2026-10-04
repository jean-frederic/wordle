with open('chunk-vendors.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('a49d:function')
print("Total length from a49d:")
sub = text[idx:idx+3500]
print(sub[-500:])
