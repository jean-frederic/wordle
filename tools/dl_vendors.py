import urllib.request

url = 'https://wordle.louan.me/js/chunk-vendors.b133507d.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = resp.read().decode('utf-8')

print(f"Length of chunk-vendors: {len(data)}")
with open('chunk-vendors.js', 'w', encoding='utf-8') as f:
    f.write(data)

idx = data.find('"6125":')
if idx != -1:
    print("Found 6125 in chunk-vendors:")
    print(data[idx:idx+500])
