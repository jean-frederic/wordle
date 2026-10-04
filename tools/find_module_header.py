with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('"56d7":function')
print(text[idx:idx+800])
