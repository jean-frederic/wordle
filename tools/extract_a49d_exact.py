with open('chunk-vendors.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('a49d:function')
idx_next = text.find('"62e4"', idx)
if idx_next == -1:
    idx_next = text.find('62e4:', idx)

func_code = text[idx:text.find('},', idx) + 1] # wait, a49d has nested functions
# Let's find where a49d ends properly:
# It starts with "a49d:function(e,t,n){"
# and ends right before the next property in chunk-vendors
end_pos = text.find('},"605d"', idx)
if end_pos == -1:
    end_pos = text.find('},62e4', idx)
if end_pos == -1:
    end_pos = text.find(',"62e4"', idx)

print("idx:", idx, "end_pos:", end_pos)
# Let's write the chunk out
with open('extracted_a49d.js', 'w', encoding='utf-8') as f:
    f.write(text[idx:end_pos+1])
print("Written extracted_a49d.js")
