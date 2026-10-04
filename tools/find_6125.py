for filename in ['app.js', 'chunk-vendors.js']:
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    import re
    matches = [m.start() for m in re.finditer(r'6125', text)]
    print(f"{filename}: {len(matches)} matches for 6125")
    for idx in matches:
        print(text[max(0, idx-100):min(len(text), idx+200)])
        print("-"*30)
