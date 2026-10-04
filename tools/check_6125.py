with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('"6125":')
if idx != -1:
    print("Found 6125 in app.js:")
    print(text[idx:idx+400])
else:
    print("6125 not in app.js, must be in chunk-vendors.js")
