with open('chunk-vendors.js', 'r', encoding='utf-8') as f:
    text = f.read()

a49d_code = text[97319:97319+1615]
# Make a runnable JScript script
js_script = f"""
var module = {{ exports: {{}} }};
var fn = {a49d_code.replace('a49d:', '')};
fn(module, module.exports, function(id){{ return null; }});

var seedrandom = module.exports;
var rng = seedrandom("2022-1-10");
WScript.Echo("Seedrandom result: " + rng());
"""

with open('test_sr_cscript.js', 'w', encoding='utf-8') as f:
    f.write(js_script)

print("Created test_sr_cscript.js")
