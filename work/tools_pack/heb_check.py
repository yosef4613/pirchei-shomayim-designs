# -*- coding: utf-8 -*-
"""R-55 (the review 14:15): a message to the owner is checked before it goes out — no English.
Allowed in a Hebrew sentence: codes with a digit (S7F186, R-55, D‑301, B4, ST-16, p469, 3/4), sha1 hashes, file names (*.html, *.json, *.md),
and code names written as one word with a hyphen or an underscore (J46_16, A3-PITCH, AR-N). Everything else in Latin letters is English and fails.
usage: python3 heb_check.py < message.txt   → exit 0 = clean; exit 1 = the English words, one per line."""
import re, sys
t = sys.stdin.read()
t = re.sub(r'https?://\S+', ' ', t)                                   # links
t = re.sub(r'\b[\w.\-]+\.(?:html|json|md|js|py|png|txt|zip)\b', ' ', t)  # file names
t = re.sub(r'\b[0-9a-f]{12,40}\b', ' ', t)                            # sha1
bad = []
for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-‑/.']*", t):
    w = w.strip('.-‑/\'')
    if not w: continue
    if re.search(r'\d', w): continue                                   # a code with a digit
    if len(w) == 1: continue                                           # a single letter: a coordinate (x, y) or a label (A, L, S)
    if re.search(r'[_\-‑]', w) and w.upper() == w: continue            # a code name: AR-N, A3-PITCH, SVC-E
    bad.append(w)
if bad:
    print('\n'.join(sorted(set(bad)))); sys.exit(1)
print('נקי'); sys.exit(0)
