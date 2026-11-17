#!/usr/bin/env python3
# gen_refined.py — brandin 17.11 (המשימה של 19:00): "חידוש 01 · מזנוני השדה" של המעצב (set7_watch/refined_1825) — ששת המזנונים.
#  הקבצים של המעצב: 470–720 ק"ב לכל מותג (ציור שמקודד כמלבנים צבעוניים, 600×480 ללוגו וכ-1000 רוחב לשלט). כאן — אותו ציור, מפוענח (אותו
#  אלגוריתם של refinedDrawingFactory.geometry), מוקטן לרזולוציה של השלט במשחק (8 נקודות לכל יחידת עולם; הלוגו 120×96), עם לוח צבעים מצומצם,
#  ומקודד מחדש כרצועות אופקיות באלפבית בלי תנועות (הסינון). הפלט: tools/refined_data.json — נכנס ל-074v_brandin.js דרך gen_brandin.py.
#  usage: python3 gen_refined.py [--k 8] [--colors 48]
import sys, re, json, os
import numpy as np
from PIL import Image
D = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/set7_watch/refined_1825/refined/brands/'
HERE = os.path.dirname(os.path.abspath(__file__))
IDS = ['terminal-cafe', 'gate-cafe', 'juice', 'pizza', 'shawarma', 'salads']
K = 8; NC = 48; LOGO = (120, 96)
for i, a in enumerate(sys.argv):
    if a == '--k': K = int(sys.argv[i + 1])
    if a == '--colors': NC = int(sys.argv[i + 1])
AL = ''.join(chr(i) for i in range(35, 127) if i not in (92, 60, 62))
LK = {c: i for i, c in enumerate(AL)}
def tiles(bits):
    n = 1 << bits; xs, ys = [], []
    for i in range(n * n):
        xx = yy = 0
        for b in range(bits): xx |= ((i >> (2 * b)) & 1) << b; yy |= ((i >> (2 * b + 1)) & 1) << b
        xs.append(xx); ys.append(yy)
    return n, xs, ys
def raster(p):
    W, H = p['w'], p['h']; img = np.zeros((H, W, 3), np.uint8); bg = p.get('background', '#000000')
    img[:, :] = [int(bg[1:3], 16), int(bg[3:5], 16), int(bg[5:7], 16)]
    n, tx, ty = tiles(p['tileBits']); area = n * n; cols = -(-W // n); skew = p['codec'] == 'tile-skewflags44'
    for col, s in p['layers']:
        rgb = [int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)]; i = 0; pos = 0
        def rd():
            nonlocal i
            v = 0; m = 1
            while True:
                d = LK[s[i]]; i += 1; v += (d % 44) * m; m *= 44
                if d < 44: return v
        while i < len(s):
            h = rd()
            if skew:
                if h % 2 == 0: fl, dl = 0, h // 2
                elif h % 4 == 1: fl, dl = 1, (h - 1) // 4
                elif h % 8 == 3: fl, dl = 2, (h - 3) // 8
                else: fl, dl = 3, (h - 7) // 8
            else: fl, dl = h % 4, h // 4
            pos += dl; rw = rd() + 2 if fl & 1 else 1; rh = rd() + 2 if fl & 2 else 1
            t, loc = divmod(pos, area); px = (t % cols) * n + tx[loc]; py = (t // cols) * n + ty[loc]
            img[py:py + rh, px:px + rw] = rgb
    return img
# the alphabet of the new data: no vowels, no x y, no k f v n s b m p (the short words of the filter), no digits 0 1 3 4 5, no quote / backslash / < > @ /
SAFE = [c for c in (chr(i) for i in range(35, 127)) if c not in '\\"<>@/\'`' and c.lower() not in 'aeiouxykfvnsbmp' and c not in '01345']
B = len(SAFE) // 2; ALN = SAFE[:2 * B]
def enc(v):
    o = ''
    while True:
        d = v % B; v //= B
        if v: o += ALN[B + d]
        else: o += ALN[d]; return o
def encode(img):
    H, W = img.shape[:2]; flat = img.reshape(-1, 3).astype(np.int64); keys = flat[:, 0].astype(np.int64) * 65536 + flat[:, 1] * 256 + flat[:, 2]
    cols, inv, cnt = np.unique(keys, return_inverse=True, return_counts=True); bgi = int(np.argmax(cnt)); layers = []
    lab = inv.reshape(H, W)
    for ci in range(len(cols)):
        if ci == bgi: continue
        m = (lab == ci); runs = []; last = 0
        for y in range(H):
            row = m[y]
            if not row.any(): continue
            d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]])); st = np.where(d == 1)[0]; en = np.where(d == -1)[0]
            for a, b in zip(st, en):
                p0 = y * W + a; runs.append(enc(p0 - last) + enc(b - a - 1)); last = p0 + (b - a)
        k = int(cols[ci]); layers.append(['#%06x' % k, ''.join(runs)])
    k = int(cols[bgi]); return {'w': W, 'h': H, 'bg': '#%06x' % k, 'L': layers}
out = {'alpha': ''.join(ALN), 'base': B, 'brands': {}}
tot = 0
for bid in IDS:
    s = open(D + bid + '.js', encoding='utf-8').read()
    j = s.index('var entry=') + len('var entry='); e, _ = json.JSONDecoder().raw_decode(s[j:])
    o = {'name': e.get('name'), 'parts': {}}
    for fmt in ('logo', 'sign'):
        p = e['parts'][fmt]; img = raster(p)
        if fmt == 'sign': f = p.get('face') or {'w': 40, 'h': 11}; th = round(f['h'] * K); tw = round(p['w'] / p['h'] * th)   # the source's own aspect (the drawing is 'contain' in the face, like the designer's draw)
        else: tw, th = LOGO
        im = Image.fromarray(img).resize((tw, th), Image.LANCZOS).quantize(colors=NC, method=Image.MEDIANCUT, dither=Image.NONE).convert('RGB')
        q = encode(np.array(im)); q['face'] = p.get('face'); q['back'] = p.get('background'); q['trim'] = p.get('trim'); q['src'] = [p['w'], p['h']]
        o['parts'][fmt] = q
        n = sum(len(l[1]) + 12 for l in q['L']); tot += n
        print(bid, fmt, p['w'], 'x', p['h'], '->', tw, 'x', th, 'colors', len(q['L']) + 1, 'chars', n)
    out['brands'][bid] = o
json.dump(out, open(HERE + '/refined_data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('total chars', tot, 'json bytes', os.path.getsize(HERE + '/refined_data.json'), 'alphabet', len(ALN), ''.join(ALN))
