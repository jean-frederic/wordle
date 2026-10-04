with open('app.js', 'r', encoding='utf-8') as f:
    s = f.read()

import re

# Look for word arrays assigned to variables or component data
matches = [m.start() for m in re.finditer(r'\["COMME"', s)]
for idx in matches:
    print("Found COMME array at", idx)
    print("Preceding 300 chars:")
    print(s[max(0, idx-300):idx])
    print("Following 100 chars after array:")
    # find where array ends
    end = s.find(']', idx)
    print(s[end:end+300])

# Look for where the secret word is chosen (e.g., wordOfTheDay, solution, mot, secret, etc.)
keywords = ["word", "mot", "solution", "target", "day", "today", "diff", "moment", "dayjs"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), s, re.IGNORECASE)]
    print(f"Keyword '{kw}': {len(matches)} matches")

# Let's inspect where Array 0 is referenced
