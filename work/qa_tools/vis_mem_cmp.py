# 8.11 · vis_mem_cmp.py — ההשוואה של ריצות של vis_mem.js (לפני / אחרי): לכל צילום — כמה פיקסלים שונים (הפרש מעל 8 בערוץ) וההפרש הגדול ביותר.
# עם --noise <dirA2> (ריצה שנייה של אותה בנייה "לפני"): רצפת הרעש של הצילום — מה שמשתנה בין שתי ריצות של אותה בנייה (אורות שתלויים
# בטיימרים, תמונות שנוצרות ברקע). "בתוך הרעש": לא יותר מפי 3 מהרעש של אותו צילום ולא יותר מ-3,000 פיקסלים (0.16% מהמסך), או 0.
# python3 qa_tools/vis_mem_cmp.py <dirA> <dirB> [--noise <dirA2>] [--out out.json] [--diff <dir>]   יציאה 1 — יש צילום מעבר לרעש.
import json, os, sys
import numpy as np
from PIL import Image
a = sys.argv[1:]; A, B = a[0], a[1]
opt = lambda k: a[a.index(k) + 1] if k in a else None
NZ, OUT, DD = opt('--noise'), opt('--out'), opt('--diff')
def load(d, f): return np.asarray(Image.open(os.path.join(d, f)).convert('RGBA')).astype(np.int16)
def diff(x, y): d = np.abs(x - y).max(axis=2); return d > 8, int(d.max())
rows, bad = [], 0
for f in sorted(os.listdir(A)):
    if not f.endswith('.png'): continue
    if not os.path.exists(os.path.join(B, f)): rows.append(dict(shot=f[:-4], missing=True)); bad += 1; continue
    x, y = load(A, f), load(B, f); m, mx = diff(x, y); n = int(m.sum()); r = dict(shot=f[:-4], diffPx=n, maxDiff=mx)
    if NZ and os.path.exists(os.path.join(NZ, f)):
        mn, _ = diff(x, load(NZ, f)); r['noisePx'] = int(mn.sum())
    lim = min(3 * r.get('noisePx', 0), 3000) if NZ else 0
    r['ok'] = n == 0 or n <= lim
    if not r['ok']: bad += 1
    if DD and n:
        os.makedirs(DD, exist_ok=True); o = (x[:, :, :3] * .45).astype(np.uint8); o[m] = [255, 0, 0]; Image.fromarray(o).save(os.path.join(DD, f))
    rows.append(r)
for r in rows: print(r['shot'].ljust(22), ('זהה' if r.get('diffPx') == 0 else ('בתוך הרעש' if r.get('ok') else 'שונה')).ljust(10), r.get('diffPx', ''), 'רעש', r.get('noisePx', '-'), 'מקס', r.get('maxDiff', ''))
same = sum(1 for r in rows if r.get('diffPx') == 0); inn = sum(1 for r in rows if r.get('ok') and r.get('diffPx'))
print('סך הכול', len(rows), 'צילומים ·', same, 'זהים ·', inn, 'בתוך הרעש ·', bad, 'שונים')
if OUT: json.dump(dict(a=A, b=B, noise=NZ, rows=rows, same=same, withinNoise=inn, differ=bad), open(OUT, 'w'), ensure_ascii=False, indent=1)
sys.exit(1 if bad else 0)
