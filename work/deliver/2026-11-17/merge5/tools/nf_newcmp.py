# nf_newcmp.py — merge4 (17.11, גל 4): השוואה של ציוני nf_score בין בנייה ישנה לחדשה (חתיכות של 12 ק"ב):
# לכל חתיכה עם ציון ≥ 30 בחדשה — האם הטקסט שלה קיים כמו שהוא בישנה (רק גבולות החיתוך זזו), או שיש בה תוכן חדש; וספירת המילים בכל הבנייה.
# usage: python3 nf_newcmp.py <old.html> <new.html> [--kb 12] [--min 30]
import sys, os, re, json, argparse, collections
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/nfkiss/tools')
from nf_words import EN, HE, BENIGN
ap = argparse.ArgumentParser(); ap.add_argument('old'); ap.add_argument('new'); ap.add_argument('--kb', type=float, default=12); ap.add_argument('--mb', type=float, default=1.3); ap.add_argument('--min', type=float, default=30)
a = ap.parse_args()
src = open(os.path.join('/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/nfkiss/tools', 'nf_score.py'), encoding='utf-8').read()
HEP = {w: re.compile(r'(?<![א-ת])[ובלהמשכ]{0,2}' + re.escape(w) + r'(?![א-ת])') for w in HE}
def counts(s):
    low = s.lower(); toks = collections.Counter(re.findall(r'[a-z0-9]+', low)); c = {}
    for w in EN:
        k = sum(n for t, n in toks.items() if w in t and not (BENIGN.search(t) and t != w))
        if k: c[w] = k
    for w in HE:
        k = len(HEP[w].findall(s))
        if k: c[w] = k
    return c
def score(s):
    n = max(1, len(s.encode('utf-8'))) / 100000; c = counts(s)
    return round(sum(EN.get(w, HE.get(w, 0)) * k for w, k in c.items()) / n, 1), c
def split(s, mb):
    maxb = int(mb * 1_000_000); out, cur, size = [], [], 0
    for i in range(0, len(s), 50_000):
        blk = s[i:i+50_000]; bl = len(blk.encode('utf-8'))
        if size and size + bl > maxb: out.append(''.join(cur)); cur, size = [], 0
        cur.append(blk); size += bl
    if cur: out.append(''.join(cur))
    return out
def pieces(s):
    for gi, g in enumerate(split(s, a.mb), 1):
        L = len(g); np_ = max(1, round(len(g.encode('utf-8')) / (a.kb * 1000))); step = -(-L // np_)
        for j in range(np_):
            pc = g[j*step:(j+1)*step]
            if pc: yield 'g%d_%d' % (gi, j + 1), pc
old = open(a.old, encoding='utf-8').read(); new = open(a.new, encoding='utf-8').read()
oldsc = {}
for nm, pc in pieces(old): oldsc[nm] = score(pc)[0]
hi = []; same = 0; diff = []
for nm, pc in pieces(new):
    sc, c = score(pc)
    if sc < a.min: continue
    hi.append(nm)
    if pc in old: same += 1
    else:
        # כמה מהחתיכה קיים בישנה: חלונות של 400 תווים
        W = 400; tot = 0; hit = 0
        for i in range(0, max(1, len(pc) - W), W):
            tot += 1; hit += pc[i:i+W] in old
        diff.append((sc, nm, round(hit / max(1, tot), 2), ' '.join('%s:%d' % (w, k) for w, k in sorted(c.items(), key=lambda x: -EN.get(x[0], HE.get(x[0], 0)) * x[1])[:5])))
print('חתיכות עם ציון ≥ %s בחדשה: %d · קיימות כמו שהן בישנה: %d · עם תוכן חדש או שונה: %d' % (a.min, len(hi), same, len(diff)))
for d in sorted(diff, reverse=True): print('  %-8s %6.1f  חלק שקיים בישנה %.0f%%  %s' % (d[1], d[0], d[2] * 100, d[3]))
co = counts(old); cn = counts(new)
wt = lambda c: sum(EN.get(w, HE.get(w, 0)) * k for w, k in c.items())
print('סכום משוקלל: ישנה %.1f · חדשה %.1f' % (wt(co), wt(cn)))
inc = sorted(((EN.get(w, HE.get(w, 0)) * (cn.get(w, 0) - co.get(w, 0)), w, co.get(w, 0), cn.get(w, 0)) for w in set(co) | set(cn) if cn.get(w, 0) > co.get(w, 0)), reverse=True)
dec = sorted(((EN.get(w, HE.get(w, 0)) * (co.get(w, 0) - cn.get(w, 0)), w, co.get(w, 0), cn.get(w, 0)) for w in set(co) | set(cn) if cn.get(w, 0) < co.get(w, 0)), reverse=True)
print('עלו: ' + ' '.join('%s:%d→%d(+%.0f)' % (w, o, n, d) for d, w, o, n in inc))
print('ירדו: ' + ' '.join('%s:%d→%d(-%.0f)' % (w, o, n, d) for d, w, o, n in dec))
