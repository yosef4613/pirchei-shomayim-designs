# 30.10 · batch 7b: the drawings of city_plan.json — the whole city, one per zone (with "its roads"), and the transition stages.
import json, math, os
from PIL import Image, ImageDraw, ImageFont
W = '/home/claude/work/study/roads'
P = json.load(open(W + '/city_plan.json'))
GR = json.load(open('/home/claude/work/study/roads/game_roads.json'))
T = P['terrain']; CLS = P['classes']; N = {n['id']: n for n in P['nodes']}; SEG = P['segments']
COLS = [0, 1200, 2400, 3600, 4800, 6000, 7200, 8400, 9600]; ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]
FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(sz, b=False): return ImageFont.truetype(FB if b else FN, sz)
KIND = {'A0': 'forest', 'B0': 'forest', 'A1': 'forest', 'C0': 'fields', 'D0': 'fields', 'C1': 'fields', 'D1': 'fields', 'B1': 'park', 'B2': 'park'}
KC = {'forest': '#d3e3c1', 'fields': '#ece4bf', 'park': '#d2e9c4'}
COL = {'arterial': '#c9442c', 'collector': '#e59a2f', 'local': '#ffffff', 'track': '#a27c52', 'temp': '#d11fb4'}
OLD = [(GR['nodes'], GR['edges'])]
ON = {n['id']: n for n in GR['nodes']}

class View:
    def __init__(s, x0, y0, x1, y1, scale, ox=0, oy=0): s.x0, s.y0, s.x1, s.y1, s.k, s.ox, s.oy = x0, y0, x1, y1, scale, ox, oy
    def __call__(s, x, y): return (s.ox + (x - s.x0) * s.k, s.oy + (y - s.y0) * s.k)
    def w(s, px): return max(1, px * s.k)

def terrain(d, v, zones=True, label=True):
    x0, y0 = v(v.x0, v.y0); x1, y1 = v(v.x1, v.y1)
    d.rectangle([x0, y0, x1, y1], fill='#f2efe5')
    for z, k in KIND.items():
        i, j = 'ABCDEFGH'.index(z[0]), int(z[1]); a = v(COLS[i], ROWS[j]); b = v(COLS[i + 1], ROWS[j + 1]); d.rectangle([a, b], fill=KC[k])
    d.polygon([v(*p) for p in T['sea']], fill='#bcd8ee')
    d.polygon([v(*p) for p in T['island']], fill='#e6e0c9', outline='#9fb3c4')
    L = T['lake']; d.ellipse([v(L['cx'] - L['rx'], L['cy'] - L['ry']), v(L['cx'] + L['rx'], L['cy'] + L['ry'])], fill='#9ec7e6')
    for a, b, c, e in T['airport']:
        p, q = v(a, b), v(c, e); d.rectangle([p, q], fill='#dcdcdc')
        step = 14
        for t in range(int(p[0] - (q[1] - p[1])), int(q[0]), step):
            d.line([(max(p[0], t), p[1] + max(0, p[0] - t)), (min(q[0], t + (q[1] - p[1])), p[1] + min(q[1] - p[1], q[0] - t))], fill='#c4c4c4', width=1)
    if zones:
        for x in COLS: d.line([v(x, ROWS[0]), v(x, ROWS[-1])], fill='#d4d0c4', width=1)
        for y in ROWS: d.line([v(COLS[0], y), v(COLS[-1], y)], fill='#d4d0c4', width=1)
        if label:
            f = font(max(9, int(11 * min(1, v.k / .11))))
            for i in range(8):
                for j in range(10):
                    a = v(COLS[i] + 30, ROWS[j] + 20)
                    if v.x0 <= COLS[i] + 30 <= v.x1 and v.y0 <= ROWS[j] + 20 <= v.y1: d.text(a, 'ABCDEFGH'[i] + str(j), fill='#9a968a', font=f)
    for name, pts in T['rail'].items():
        q = [v(*p) for p in pts]
        for k in range(len(q) - 1): d.line([q[k], q[k + 1]], fill='#4c4c4c', width=max(2, int(v.w(30))))
        for k in range(len(q) - 1):
            (ax, ay), (bx, by) = q[k], q[k + 1]; L_ = math.hypot(bx - ax, by - ay); m = int(L_ // 8)
            for t in range(0, m, 2): d.line([(ax + (bx - ax) * t / max(m, 1), ay + (by - ay) * t / max(m, 1)), (ax + (bx - ax) * (t + 1) / max(m, 1), ay + (by - ay) * (t + 1) / max(m, 1))], fill='#f2efe5', width=1)

def clip(d, v):
    a, b = v(v.x0, v.y0), v(v.x1, v.y1)
    for r_ in ([-9999, -9999, a[0] - 1, 99999], [b[0] + 1, -9999, 99999, 99999], [-9999, -9999, 99999, a[1] - 1], [-9999, b[1] + 1, 99999, 99999]): d.rectangle(r_, fill='white')

def old_roads(d, v, col='#b9b4a6', w=1):
    for e in GR['edges']:
        a, b = ON[e['a']], ON[e['b']]; d.line([v(a['x'], a['y']), v(b['x'], b['y'])], fill=col, width=w)

def roads(d, v, segs=None, ids=True, idfont=None, dim=None):
    segs = segs if segs is not None else SEG
    order = {'track': 0, 'local': 1, 'collector': 2, 'arterial': 3}
    for pas in ('casing', 'fill'):
        for s in sorted(segs, key=lambda s: order.get(s['cls'], 0)):
            q = [v(*p) for p in s['pts']]; hw = CLS[s['cls']]['halfW']; wpx = max(2, int(v.w(2 * hw)))
            if s['cls'] == 'track':
                if pas == 'fill':
                    for k in range(len(q) - 1): d.line([q[k], q[k + 1]], fill=COL['track'], width=max(1, wpx // 2))
                continue
            for k in range(len(q) - 1):
                if pas == 'casing': d.line([q[k], q[k + 1]], fill='#6c6c6c' if s['kind'] != 'bridge' else '#5d527a', width=wpx + 2)
                else: d.line([q[k], q[k + 1]], fill=(dim if dim else (COL[s['cls']] if s['kind'] != 'bridge' else '#b6a9d8')), width=wpx)
    if ids:
        f = idfont or font(10, True); done = set()
        for s in segs:
            if s['road'] in done or s['cls'] == 'track': continue
            rs = [x for x in segs if x['road'] == s['road']]; best = max(rs, key=lambda x: x['len_m']); done.add(s['road'])
            p = best['pts'][len(best['pts']) // 2] if len(best['pts']) > 2 else [(best['pts'][0][0] + best['pts'][-1][0]) / 2, (best['pts'][0][1] + best['pts'][-1][1]) / 2]
            x, y = v(*p); tw = d.textlength(s['road'], font=f)
            d.rectangle([x - tw / 2 - 2, y - 7, x + tw / 2 + 2, y + 7], fill='#ffffffd0', outline='#888')
            d.text((x - tw / 2, y - 6), s['road'], fill='#222', font=f)

def nodes(d, v, big=1.0):
    for n in P['nodes']:
        x, y = v(n['x'], n['y']); r = 4 * big; k = n['kind']
        if not (v.x0 - 50 <= n['x'] <= v.x1 + 50 and v.y0 - 50 <= n['y'] <= v.y1 + 50): continue
        if k == 'signal': d.ellipse([x - r - 1, y - r - 1, x + r + 1, y + r + 1], fill='#111'); d.ellipse([x - r / 2, y - r / 2, x + r / 2, y + r / 2], fill='#4cd26a')
        elif k == 'roundabout': d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], outline='#1d5fa8', width=max(2, int(2 * big))); d.ellipse([x - r / 2, y - r / 2, x + r / 2, y + r / 2], fill='#7ab55c')
        elif k == 'riro': d.polygon([(x - r, y + r), (x + r, y + r), (x, y - r)], fill='#7b3fb3')
        elif k == 'stop': d.rectangle([x - r * .7, y - r * .7, x + r * .7, y + r * .7], fill='#d33')
        elif k == 'gate': d.polygon([(x, y - r - 2), (x + r + 2, y), (x, y + r + 2), (x - r - 2, y)], fill='#f08c00', outline='#333')
        elif k in ('bridgehead', 'plaza'): d.ellipse([x - r, y - r, x + r, y + r], outline='#333', fill='#fff')
    for c in P['crossings']:
        x, y = v(*c['at']); f = font(int(9 * big) + 1, True)
        if c['kind'] == 'level': d.line([(x - 5, y - 5), (x + 5, y + 5)], fill='#000', width=2); d.line([(x - 5, y + 5), (x + 5, y - 5)], fill='#000', width=2)
        else: d.rectangle([x - 5, y - 7, x + 5, y + 7], outline='#000', width=2)
        d.text((x + 7, y - 14), c['id'], fill='#000', font=f)

def rtl(d, xy, txt, f, fill='#222'): d.text(xy, txt, font=f, fill=fill, direction='rtl', anchor='ra', features=['-kern'])

def legend(d, x, y, big=False):
    f = font(13); items = [('arterial', 'עורק 2+2 (+ נתיב שמאלה ברמזור)'), ('collector', 'מאסף 1+1 (+ נתיב שמאלה ברמזור)'), ('local', 'רחוב מקומי 1+1'),
                           ('track', 'דרך עפר'), ('bridge', 'גשר האי (קבוע)')]
    for i, (k, t) in enumerate(items):
        yy = y + i * 22
        if k == 'bridge': d.line([(x - 40, yy + 8), (x - 4, yy + 8)], fill='#b6a9d8', width=7)
        else: d.line([(x - 40, yy + 8), (x - 4, yy + 8)], fill='#6c6c6c', width=9 if k == 'arterial' else 7); d.line([(x - 40, yy + 8), (x - 4, yy + 8)], fill=COL[k], width=7 if k == 'arterial' else 5)
        rtl(d, (x - 50, yy), t, f)
    yy = y + len(items) * 22 + 6
    sym = [('signal', 'רמזור עם חץ שמאלה (R-16)'), ('roundabout', 'כיכר'), ('riro', 'ימינה בלבד (רחוב על עורק)'), ('stop', 'עצור / זכות קדימה'), ('gate', 'שער השדה (קפוא, R-32)')]
    v = View(0, 0, 1, 1, 1)
    for i, (k, t) in enumerate(sym):
        cy = yy + i * 22 + 8; cx = x - 22
        nodes_one(d, cx, cy, k)
        rtl(d, (x - 50, yy + i * 22), t, f)
    yy += len(sym) * 22 + 6
    d.rectangle([x - 40, yy + 2, x - 4, yy + 14], fill='#dcdcdc'); rtl(d, (x - 50, yy), 'שדה התעופה — לא נוגעים', f)
    d.line([(x - 40, yy + 30), (x - 4, yy + 30)], fill='#4c4c4c', width=4); rtl(d, (x - 50, yy + 22), 'מסילה; ▭ מעבר תחתי, ✕ מחסום', f)
    d.line([(x - 40, yy + 52), (x - 4, yy + 52)], fill='#b9b4a6', width=1); rtl(d, (x - 50, yy + 44), 'הכבישים של היום (לרקע)', f)
    return yy + 66

def nodes_one(d, x, y, k, r=4):
    if k == 'signal': d.ellipse([x - r - 1, y - r - 1, x + r + 1, y + r + 1], fill='#111'); d.ellipse([x - r / 2, y - r / 2, x + r / 2, y + r / 2], fill='#4cd26a')
    elif k == 'roundabout': d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], outline='#1d5fa8', width=2); d.ellipse([x - r / 2, y - r / 2, x + r / 2, y + r / 2], fill='#7ab55c')
    elif k == 'riro': d.polygon([(x - r, y + r), (x + r, y + r), (x, y - r)], fill='#7b3fb3')
    elif k == 'stop': d.rectangle([x - r * .7, y - r * .7, x + r * .7, y + r * .7], fill='#d33')
    elif k == 'gate': d.polygon([(x, y - r - 2), (x + r + 2, y), (x, y + r + 2), (x - r - 2, y)], fill='#f08c00', outline='#333')

# ------------------------------------------------------------------ the whole city
K = .105; v = View(0, -850, 9600, 7750, K, 10, 50)
Wc, Hc = int(9600 * K) + 20 + 470, int(8600 * K) + 70
im = Image.new('RGB', (Wc, Hc), 'white'); d = ImageDraw.Draw(im, 'RGBA')
terrain(d, v); old_roads(d, v); roads(d, v, idfont=font(9, True)); nodes(d, v, 1.0); clip(d, v)
rtl(d, (Wc - 12, 10), 'תוכנית הדרכים של כל העיר — 7ב, טיוטה 1 (30.10)', font(18, True))
rtl(d, (Wc - 12, 36), 'עורקים כל 2–3 אזורים לפי הזרימה: השדה ↔ המרכז ↔ הנמל ↔ האי', font(12))
yy = legend(d, Wc - 12, 70)
tt = P['totals']; f = font(12)
lines = [f"{tt['nodes']} צמתים · {tt['segments']} קטעים", 'ק"מ: ' + ' · '.join(f'{k} {v_}' for k, v_ in tt['km'].items()),
         f"{tt['signals']} רמזורים · {tt['roundabouts']} כיכרות · {tt['riro']} ימינה-בלבד", f"{tt['temp']} חיבורים זמניים במעבר (בדף)"]
for i, t_ in enumerate(lines): rtl(d, (Wc - 12, yy + 6 + i * 18), t_, f)
yy += 6 + len(lines) * 18 + 10
rtl(d, (Wc - 12, yy), 'העורקים והמאספים', font(13, True)); yy += 20
for rd in P['roads']:
    if rd['cls'] not in ('arterial', 'collector'): continue
    rtl(d, (Wc - 12, yy), f"{rd['id']} — {rd['name']} ({CLS[rd['cls']]['he']} {rd['lanes']})", font(11)); yy += 15
im.save(W + '/city_plan.png'); print('city', im.size)

# ------------------------------------------------------------------ one drawing per zone, with the list of its roads
os.makedirs(W + '/zones', exist_ok=True)
for z, Z in P['zones'].items():
    if not Z['roads']: continue
    i, j = 'ABCDEFGH'.index(z[0]), int(z[1:]); zx0, zy0, zx1, zy1 = COLS[i], ROWS[j], COLS[i + 1], ROWS[j + 1]
    m = 450; x0, y0, x1, y1 = zx0 - m, zy0 - m, zx1 + m, zy1 + m
    k = min(620 / (x1 - x0), 560 / (y1 - y0)); v = View(x0, y0, x1, y1, k, 10, 44)
    Wd, Hd = int((x1 - x0) * k) + 20 + 560, max(int((y1 - y0) * k) + 60, 560)
    im = Image.new('RGB', (Wd, Hd), 'white'); d = ImageDraw.Draw(im, 'RGBA')
    terrain(d, v, label=True); old_roads(d, v, '#a8a294', 2)
    a, b = v(zx0, zy0), v(zx1, zy1); d.rectangle([a, b], outline='#1d5fa8', width=3)
    segs = [s for s in SEG if s['id'] in Z['segments']]; other = [s for s in SEG if s['id'] not in Z['segments']]
    roads(d, v, other, ids=False, dim='#e2ddd2'); roads(d, v, segs, idfont=font(11, True)); nodes(d, v, 1.4); clip(d, v)
    d.rectangle([0, 0, Wd, 36], fill='white')
    rtl(d, (Wd - 12, 8), f"{z} — {Z['purpose']}" + (f"  ·  שלב {Z['stage']}" if Z['stage'] else ''), font(16, True))
    X = Wd - 12; y = 46; f = font(12); fb = font(12, True)
    rtl(d, (X, y), 'הכבישים שלו', font(14, True)); y += 22
    for rid in Z['roads']:
        rd = next(r for r in P['roads'] if r['id'] == rid); L = sum(s['len_m'] for s in segs if s['road'] == rid)
        rtl(d, (X, y), f"{rid} — {rd['name']}", fb); y += 16
        rtl(d, (X - 14, y), f"{CLS[rd['cls']]['he']} · {rd['lanes']} נתיבים · {L:.0f} מ׳ כאן" + ('' if rd['truck'] else ' · בלי משאיות עוברות'), f, '#555'); y += 18
    if Z['signals'] or Z['roundabouts']:
        y += 4; rtl(d, (X, y), 'צמתים', font(14, True)); y += 20
        for nid in Z['signals']: rtl(d, (X, y), f"רמזור {nid} — {N[nid]['label']}", f); y += 16
        for nid in Z['roundabouts']: rtl(d, (X, y), f"כיכר {nid} — {N[nid]['label']}", f); y += 16
    tmp = [a_ for t in P['transition']['stages'] for a_ in t['temp_added'] if a_['id'] in Z['temp']]
    if tmp:
        y += 4; rtl(d, (X, y), 'חיבורים זמניים (במעבר)', font(14, True)); y += 20
        for a_ in tmp[:8]: rtl(d, (X, y), f"{a_['id']}: {a_['old_node']} → {a_['to']} · {a_['len_m']:.0f} מ׳ · עד {a_['until']}", f, '#a0137f'); y += 16
    y += 6; rtl(d, (X, y), 'אפור דק — הכבישים של היום; מסגרת כחולה — האזור', font(11), '#777')
    im.save(f"{W}/zones/{z}.png")
print('zones', len(os.listdir(W + '/zones')))

# ------------------------------------------------------------------ the transition stages (small maps)
st = P['transition']['stages']; cols = 4; tw, th = 330, 330
im = Image.new('RGB', (cols * tw + 10, math.ceil(len(st) / cols) * (th + 30) + 50), 'white'); d = ImageDraw.Draw(im, 'RGBA')
rtl(d, (im.size[0] - 10, 8), 'המעבר — אזור אחרי אזור: חדש (צבע), ישן שנשאר (אפור), חיבור זמני (סגול)', font(15, True))
SI = {t['stage']: k for k, t in enumerate(st)}
for k, t in enumerate(st):
    cx, cy = (k % cols) * tw + 5, (k // cols) * (th + 30) + 40
    ti = Image.new('RGB', (tw, th + 26), 'white'); td = ImageDraw.Draw(ti, 'RGBA')
    v = View(0, -850, 6600, 5400, (tw - 10) / 6600, 5, 26)
    if t['stage'] == 'S13': v = View(0, -850, 9600, 7750, (tw - 10) / 9600, 5, 26)
    terrain(td, v, zones=True, label=False)
    gone = set(e for tt in st[:k + 1] for e in tt['removed'])
    for e in GR['edges']:
        if e['id'] in gone: continue
        a_, b_ = ON[e['a']], ON[e['b']]; td.line([v(a_['x'], a_['y']), v(b_['x'], b_['y'])], fill='#8f8a7e', width=1)
    roads(td, v, [s_ for s_ in SEG if SI[s_['stage']] <= k], ids=False)
    act = 0
    for tt in st[:k + 1]:
        for a_ in tt['temp_added']:
            if a_['until'] and SI[a_['until']] <= k: continue
            act += 1; p0, p1 = v(*a_['x']), v(*a_['y'])
            td.line([p0, p1], fill='#d11fb4', width=3); td.ellipse([p0[0] - 3, p0[1] - 3, p0[0] + 3, p0[1] + 3], fill='#d11fb4')
    for zz in t['zones']:
        i, j = 'ABCDEFGH'.index(zz[0]), int(zz[1:]); td.rectangle([v(COLS[i], ROWS[j]), v(COLS[i + 1], ROWS[j + 1])], outline='#1d5fa8', width=2)
    clip(td, v); td.rectangle([0, 0, tw, 24], fill='white')
    rtl(td, (tw - 6, 4), f"{t['stage']} — {t['why'][:36]} · {act} זמניים", font(11, True))
    im.paste(ti, (cx, cy))
im.save(W + '/transition.png'); print('transition', im.size)
