#!/usr/bin/env python3
# nf_score.py — nfkiss 17.11: בדיקה עצמית לפני הבעלים. מחלק את הבנייה כמו split_any (חלקים של MB) וכל חלק ל-K חתיכות (~150 ק"ב),
# ומדפיס לכל חתיכה ציון של מילים רגישות לכל 100 ק"ב (nf_words.py: אנגלית — תת-מחרוזת בלי תלות באותיות, כולל בתוך נתונים; עברית — מילה עם קידומות),
# והמילים שתורמות הכי הרבה. --ref <dir> --blocked a,b: אותו ציון לחתיכות שנבדקו אצל הבעלים (nftest/q) — להשוואה.
# usage: python3 nf_score.py <build.html> [--mb 1.3] [--pieces 8] [--ref DIR --blocked g6_7,...] [--show 25] [--json out]
import sys, os, re, json, argparse, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nf_words import EN, HE, BENIGN
ap = argparse.ArgumentParser(); ap.add_argument('build'); ap.add_argument('--mb', type=float, default=1.3); ap.add_argument('--pieces', type=int, default=8); ap.add_argument('--kb', type=float, default=0)
ap.add_argument('--ref'); ap.add_argument('--blocked', default=''); ap.add_argument('--show', type=int, default=25); ap.add_argument('--json')
a = ap.parse_args()
HEP = {w: re.compile(r'(?<![א-ת])[ובלהמשכ]{0,2}' + re.escape(w) + r'(?![א-ת])') for w in HE}
def score(s):
    low = s.lower(); n = max(1, len(s.encode('utf-8'))) / 100000; c = {}
    toks = collections.Counter(re.findall(r'[a-z0-9]+', low))   # אסימונים (camelCase → אותיות קטנות); אסימון תמים — לא נספר
    for w in EN:
        k = sum(n for t, n in toks.items() if w in t and not (BENIGN.search(t) and t != w))
        if k: c[w] = k
    for w in HE:
        k = len(HEP[w].findall(s)) if w in HEP else s.count(w)
        if k: c[w] = k
    sc = sum(EN.get(w, HE.get(w, 0)) * k for w, k in c.items()) / n
    top = sorted(((EN.get(w, HE.get(w, 0)) * k, w, k) for w, k in c.items()), reverse=True)[:8]
    return round(sc, 1), top
def split(s, mb):
    maxb = int(mb * 1_000_000); out, cur, size = [], [], 0
    for i in range(0, len(s), 50_000):
        blk = s[i:i+50_000]; bl = len(blk.encode('utf-8'))
        if size and size + bl > maxb: out.append(''.join(cur)); cur, size = [], 0
        cur.append(blk); size += bl
    if cur: out.append(''.join(cur))
    return out
res = []
ref = []
if a.ref:
    BL = set(x for x in a.blocked.split(',') if x)
    for f in sorted(os.listdir(a.ref)):
        if f.endswith('.txt'):
            sc, top = score(open(os.path.join(a.ref, f), encoding='utf-8').read()); ref.append((f[:-4] in BL, f[:-4], sc, top))
    b = [r[2] for r in ref if r[0]]; p = [r[2] for r in ref if not r[0]]
    print('== הייחוס (הבעלים): חסומות %d — ציון %s–%s · עברו %d — ציון %s–%s' % (len(b), min(b, default=0), max(b, default=0), len(p), min(p, default=0), max(p, default=0)))
    for r in sorted(ref, key=lambda r: -r[2]): print('  %s %-8s %6.1f  %s' % ('X' if r[0] else '.', r[1], r[2], ' '.join('%s:%d' % (w, k) for _, w, k in r[3])))
s = open(a.build, encoding='utf-8').read()
for gi, g in enumerate(split(s, a.mb), 1):
    L = len(g); np_ = a.pieces if not a.kb else max(1, round(len(g.encode('utf-8')) / (a.kb * 1000))); step = -(-L // np_)
    for j in range(np_):
        pc = g[j*step:(j+1)*step]
        if not pc: continue
        sc, top = score(pc); smp = ''
        if top:
            w = top[0][1]; k = pc.lower().find(w) if not re.search('[\u05d0-\u05ea]', w) else pc.find(w)
            if k >= 0: smp = re.sub(r'\s+', ' ', pc[max(0, k - 50):k + 60])
        res.append(('g%d_%d' % (gi, j + 1), len(pc.encode('utf-8')), sc, top, smp))
allsc = sorted(r[2] for r in res)
print('== הבנייה %s: %d חתיכות · ציון: מינימום %s · חציון %s · מקסימום %s' % (os.path.basename(a.build), len(res), allsc[0], allsc[len(allsc)//2], allsc[-1]))
if ref:
    pmin = min((r[2] for r in ref if r[0]), default=None)
    if pmin is not None: print('   מעל הציון הנמוך של חתיכה חסומה (%s): %d חתיכות' % (pmin, sum(1 for r in res if r[2] >= pmin)))
for r in sorted(res, key=lambda r: -r[2])[:a.show]:
    print('  %-8s %8s ב׳ %6.1f  %s\n           «%s»' % (r[0], format(r[1], ','), r[2], ' '.join('%s:%d' % (w, k) for _, w, k in r[3]), r[4] if len(r) > 4 else ''))
if a.json: json.dump({'ref': ref, 'build': res}, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False)
