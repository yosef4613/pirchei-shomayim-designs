# nf_piece.py — merge4: מדפיס את החלקים החדשים (שלא קיימים בבנייה הישנה) של חתיכה אחת (כמו nf_score, 12 ק"ב), עם המילים הרגישות שבהם.
# usage: python3 nf_piece.py <old.html> <new.html> <gN_M> [--kb 12]
import sys, re, argparse
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/nfkiss/tools')
from nf_words import EN, HE, BENIGN
ap = argparse.ArgumentParser(); ap.add_argument('old'); ap.add_argument('new'); ap.add_argument('piece'); ap.add_argument('--kb', type=float, default=12); a = ap.parse_args()
def split(s, mb=1.3):
    maxb = int(mb * 1_000_000); out, cur, size = [], [], 0
    for i in range(0, len(s), 50_000):
        blk = s[i:i+50_000]; bl = len(blk.encode('utf-8'))
        if size and size + bl > maxb: out.append(''.join(cur)); cur, size = [], 0
        cur.append(blk); size += bl
    if cur: out.append(''.join(cur))
    return out
old = open(a.old, encoding='utf-8').read(); new = open(a.new, encoding='utf-8').read()
gi, j = map(int, a.piece[1:].split('_')); g = split(new)[gi - 1]; L = len(g); np_ = max(1, round(len(g.encode('utf-8')) / (a.kb * 1000))); step = -(-L // np_)
pc = g[(j - 1) * step:j * step]; W = 200; i = 0; runs = []; st = None
while i < len(pc):
    w = pc[i:i + W]; inold = w in old
    if not inold and st is None: st = i
    if inold and st is not None: runs.append((st, i + W)); st = None
    i += W
if st is not None: runs.append((st, len(pc)))
for s0, s1 in runs:
    t = pc[s0:s1]; toks = [x for x in re.findall(r'[a-z0-9]+', t.lower()) if any(w in x for w in EN) and not (BENIGN.search(x))]
    print('== %d–%d (%d תווים) · %s' % (s0, s1, s1 - s0, ' '.join(sorted(set(toks)))[:300])); print(re.sub(r'\s+', ' ', t[:600]))
