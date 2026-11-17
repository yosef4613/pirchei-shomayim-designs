# mf_check.py — בודק שכל חלק חדש של ענף יושב ב-int305 אחרי החלק שלפניו בענף ולפני החלק שאחריו; ושכל קובץ ב-parts/ ברשימה.
import json, subprocess, sys, os
S = sys.argv[1]; commits = sys.argv[2:]
def man(rev): return [p['name'] for p in json.loads(subprocess.check_output(['git', '-C', S, 'show', rev + ':manifest.json']))['parts']]
cur = [p['name'] for p in json.load(open(os.path.join(S, 'manifest.json')))['parts']]; idx = {n: i for i, n in enumerate(cur)}
base = set(man("master")); bad = 0; n = 0
for c in commits:
    tn = man(c)
    for i, x in enumerate(tn):
        if x in base: continue
        n += 1
        if x not in idx: print('חסר', c, x); bad += 1; continue
        prev = next((tn[j] for j in range(i - 1, -1, -1) if tn[j] in idx), None); nxt = next((tn[j] for j in range(i + 1, len(tn)) if tn[j] in idx), None)
        ok = (prev is None or idx[prev] < idx[x]) and (nxt is None or idx[nxt] > idx[x])
        if not ok: print('סדר', c, x, prev, nxt); bad += 1
files = set(f for f in os.listdir(os.path.join(S, 'parts'))); extra = files - set(cur); miss = set(cur) - files
print('חלקים', len(cur), '· חדשים', n, '· לא תקינים', bad, '· קבצים בלי רשימה', sorted(extra)[:10], '· ברשימה בלי קובץ', sorted(miss)[:10])
