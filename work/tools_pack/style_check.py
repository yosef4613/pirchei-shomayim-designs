# -*- coding: utf-8 -*-
"""style_check.py — the automatic check of a zone (or of the whole built city) against the city style guide (study/style/city_style.json).
It reads: the guide; the game's runtime facts (study/style/dump_<build>.json, made by tools_pack/style_dump.js through nolock.sh); the zone
files of the built zones (tools/patches/*.json); the game file itself for the building types (floors, doors); and the register of
exceptions (study/style/style_exceptions.json: {"exceptions": [{"key": "<zone>|<check>|<item>", "reason": "...", "by": "...", "at": "..."}]}).
It prints, for every zone, a table — rule · required · found · ok / deviation · reason on record — and a summary line per zone, then the
seams between neighbouring built zones. It only measures; it changes nothing.
usage:
  python3 tools_pack/style_check.py                         # every built zone + the seams
  python3 tools_pack/style_check.py C5 D5 --dump study/style/dump_<build>.json      # a new zone: its rectangle from the grid, its district from zone_spec/<Z>.md
  options: --zone Z (repeat), --json OUT (default study/style/style_check_<build>.json), --quiet (the summary only)"""
import json, math, re, sys, os, argparse
sys.dont_write_bytecode = True   # no cache folder beside the tools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W = '/home/claude/tc/pkg/work'

ap = argparse.ArgumentParser()
ap.add_argument('--guide', default=W + '/study/style/city_style.json')
ap.add_argument('--dump', default=W + '/study/style/dump_s7f193.json')
ap.add_argument('--exceptions', default=W + '/study/style/style_exceptions.json')
ap.add_argument('zones', nargs='*')
ap.add_argument('--zone', action='append')
ap.add_argument('--rect'); ap.add_argument('--district')
ap.add_argument('--json'); ap.add_argument('--quiet', action='store_true')
ap.add_argument('--game')   # 2.11 08:32: קובץ המשחק לבדיקה (ברירת המחדל — זה של המדריך)
A = ap.parse_args()
if A.game: os.environ['TC_STYLE_GAME'] = A.game
GD = json.load(open(A.guide, encoding='utf-8'))
DP = json.load(open(A.dump, encoding='utf-8'))
EXC = {}
if os.path.exists(A.exceptions):
    for e in json.load(open(A.exceptions, encoding='utf-8')).get('exceptions', []): EXC[e['key']] = e
ZONES = {k: dict(v) for k, v in GD['zones_built'].items()}
A.zone = (A.zone or []) + (A.zones or []) or None
ROW_Y = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]   # the game's MAP_ROW_Y, with row 0 at −850
def zone_rect(z):
    m = re.match(r'^([A-H])(\d)$', z)
    if not m: return None
    c = 'ABCDEFGH'.index(m.group(1)); n = int(m.group(2))
    return [c * 1200, ROW_Y[n], c * 1200 + 1200, ROW_Y[n + 1]]
def zone_district(z):
    p = W + '/study/zone_spec/%s.md' % z
    if not os.path.exists(p): return ''
    m = re.search(r'^רובע:\s*([^·(\n]+)', open(p, encoding='utf-8').read(), re.M)
    return m.group(1).strip() if m else ''
for z in (A.zone or []):
    if z not in ZONES:
        r = [float(v) for v in A.rect.split(',')] if A.rect else zone_rect(z)
        if r: ZONES[z] = {'rect': r, 'district': A.district or zone_district(z), 'data': [], 'he': 'אזור חדש'}
RUN = A.zone or list(GD['zones_built'].keys())
PAIRS = [list(p) for p in GD['seams']['pairs']]
def touches(a, b):
    ra, rb = ZONES[a]['rect'], ZONES[b]['rect']
    sx = min(ra[2], rb[2]) - max(ra[0], rb[0]); sy = min(ra[3], rb[3]) - max(ra[1], rb[1])
    return (abs(sx) < 1 and sy > 0) or (abs(sy) < 1 and sx > 0)
for z in RUN:
    for o in ZONES:
        if o != z and touches(z, o) and not any(sorted(p) == sorted([z, o]) for p in PAIRS): PAIRS.append([o, z])
if A.zone: PAIRS = [p for p in PAIRS if set(p) & set(RUN)]
KIT = GD['kit']
GAME = open(W + '/' + (A.game or GD['sources']['G']['file']), encoding='utf-8').read()
import style_build as SB   # the building types of the game (the same parser the guide used)
ZDATA = {}
for k in ('ZA', 'ZB3', 'ZB4', 'ZC3', 'ZD3', 'ZCD'):
    ZDATA[k] = json.load(open(W + '/' + GD['sources'][k]['file'], encoding='utf-8'))
ZD = DP.get('zoneData', {})

# ---------------------------------------------------------------- geometry
def inrect(x, y, r, m=0): return r[0] - m <= x < r[2] + m and r[1] - m <= y < r[3] + m
def zone_of(x, y):
    for z, v in ZONES.items():
        if inrect(x, y, v['rect']): return z
    return None
def built_at(x, y):
    """the zone that is built at (x, y), or the column/row name of an unbuilt one"""
    return zone_of(x, y)
NODE_DEG, NODE_XY, BY_NODE = {}, {}, {}
for e in DP['edges']:
    for n, x, y in ((e['a'], e['ax'], e['ay']), (e['b'], e['bx'], e['by'])):
        NODE_DEG[n] = NODE_DEG.get(n, 0) + 1; NODE_XY[n] = (x, y); BY_NODE.setdefault(n, []).append(e)
SIGNAL_NODES = {s['node'] for s in DP.get('signals', [])}
def geo(e):
    L = math.hypot(e['bx'] - e['ax'], e['by'] - e['ay']) or 1
    ux, uy = (e['bx'] - e['ax']) / L, (e['by'] - e['ay']) / L
    return L, ux, uy, -uy, ux
def proj(e, x, y):
    L, ux, uy, nx, ny = geo(e); dx, dy = x - e['ax'], y - e['ay']
    return dx * ux + dy * uy, dx * nx + dy * ny
def junction_band(e, node):
    others = [o for o in BY_NODE.get(node, []) if o['id'] != e['id']]
    if not others: return 0
    best = 0
    for o in others:
        L1, ux, uy, _, _ = geo(e); L2, vx, vy, _, _ = geo(o)
        if abs(ux * vx + uy * vy) > .95: continue            # the same street going on
        best = max(best, o['w'] / 2 + o['sw'])
    return best
def side_intervals(e, s, zone):
    """the t-intervals along e where the middle of the sidewalk on side s lies in the zone"""
    L, ux, uy, nx, ny = geo(e); off = e['w'] / 2 + e['sw'] / 2; r = ZONES[zone]['rect']; out = []; cur = None
    t = 0.0
    while t <= L + 1e-6:
        x, y = e['ax'] + ux * t + nx * s * off, e['ay'] + uy * t + ny * s * off
        if inrect(x, y, r):
            if cur is None: cur = [t, t]
            cur[1] = t
        elif cur is not None: out.append(cur); cur = None
        t += 2.0
    if cur is not None: out.append(cur)
    return [iv for iv in out if iv[1] - iv[0] >= 30]
def on_boundary(x, y):
    for v in ZONES.values():
        r = v['rect']
        if (abs(x - r[0]) < 1 or abs(x - r[2]) < 1) and r[1] - 1 <= y <= r[3] + 1: return True
        if (abs(y - r[1]) < 1 or abs(y - r[3]) < 1) and r[0] - 1 <= x <= r[2] + 1: return True
    return False

# ---------------------------------------------------------------- the things on the ground
LAMPS = []        # (x, y, asset, roadId or None, source)
for l in DP['lights']: LAMPS.append((l['x'], l['y'], l.get('asset'), l.get('roadId'), l['list']))
for k, v in DP.get('looks', {}).items():
    for a, x, y, tw in v['lamps']: LAMPS.append((x, y, a, None, k))
for a, x, y, tw in ZD.get('C3LV', {}).get('lamps', []): LAMPS.append((x, y, a, None, 'C3LV'))
TREES = []
for t in DP['trees']: TREES.append((t['x'], t['y'], t.get('asset'), t['list']))
for k, v in DP.get('looks', {}).items():
    for a, x, y, tw in v['trees']: TREES.append((x, y, a, k))
for a, x, y, tw in ZD.get('C3LV', {}).get('trees', []): TREES.append((x, y, a, 'C3LV'))
PROPS = []
for k, v in DP.get('looks', {}).items():
    for a, x, y in v['props']: PROPS.append((x, y, a, k))
OPEN = DP.get('openings', [])
CW = DP.get('crosswalks', [])
STOPS = [s for s in DP.get('stops', []) if not s.get('terminal')]

def lamps_on_side(e, s):
    L, ux, uy, nx, ny = geo(e); off = e['w'] / 2 + e['sw'] / 2; band = e['sw'] / 2 + GD['method']['lamp_band_px']; out = []
    for (x, y, a, rid, src) in LAMPS:
        t, d = proj(e, x, y)
        if rid is not None:
            if rid == e['id'] and d * s > 0 and -10 <= t <= L + 10: out.append((t, a, src, x, y))
        elif abs(d - s * off) <= band and -10 <= t <= L + 10: out.append((t, a, src, x, y))
    return sorted(out)
def trees_on_side(e, s):
    L, ux, uy, nx, ny = geo(e); lo, hi = e['w'] / 2 - 2, e['w'] / 2 + e['sw'] + GD['method']['tree_band_px']; out = []
    for (x, y, a, src) in TREES:
        t, d = proj(e, x, y)
        if lo <= d * s <= hi and -10 <= t <= L + 10: out.append((t, a, src, x, y))
    return sorted(out)
def openings_on_side(e, s):
    L, ux, uy, nx, ny = geo(e); hz = abs(uy) < .01; out = []
    for o in OPEN:
        cx, cy = o['x'] + o['w'] / 2, o['y'] + o['h'] / 2; t, d = proj(e, cx, cy)
        if not (e['w'] / 2 - 25 <= d * s <= e['w'] / 2 + e['sw'] + 90): continue
        ta = proj(e, o.get('ax', cx), o.get('ay', cy))[0] if (hz and o.get('dir') == 'v') or (not hz and o.get('dir') == 'h') else t
        h = max(o.get('half', 40), (o['w'] if hz else o['h']) / 2)
        if -h <= ta <= L + h: out.append((ta - h, ta + h))
    dep = 34 if e['cls'] in ('arterial', 'main') else 30
    for c in CW:
        if c.get('roadId') == e['id']:
            t = proj(e, c['x'], c['y'])[0]; out.append((t - dep / 2 - 10, t + dep / 2 + 10))
    for st in STOPS:
        if st.get('edgeId') == e['id']:
            t, d = proj(e, st['x'], st['y'])
            if d * s > 0: out.append((t - 66 - 40, t + 74 + 40))
    return out
def overlap(a, b, ivs):
    tot, cur = 0, []
    for x0, x1 in sorted(ivs):
        x0, x1 = max(x0, a), min(x1, b)
        if x1 <= x0: continue
        if cur and x0 <= cur[-1][1]: cur[-1][1] = max(cur[-1][1], x1)
        else: cur.append([x0, x1])
    return sum(x1 - x0 for x0, x1 in cur)

# ---------------------------------------------------------------- the rows
ROWS = []
def row(zone, check, item, need, have, ok, rule=None, info=False):
    key = '%s|%s|%s' % (zone, check, item)
    ex = EXC.get(key)
    r = {'zone': zone, 'check': check, 'rule': rule, 'item': item, 'need': need, 'have': have, 'ok': (None if info else bool(ok)), 'key': key,
         'reason': ex['reason'] if (ex and not ok and not info) else None}
    ROWS.append(r); return r
def fmt(v): return ('%d' % round(v)) if isinstance(v, (int, float)) else str(v)
SIDE_HE = {1: 'צד שמאל', -1: 'צד ימין'}
def side_name(e, s):
    L, ux, uy, nx, ny = geo(e)
    if abs(uy) < .01: return 'הצד הדרומי' if ny * s > 0 else 'הצד הצפוני'
    return 'הצד המזרחי' if nx * s > 0 else 'הצד המערבי'
def edges_in(zone):
    out = []
    for e in DP['edges']:
        for s in (1, -1):
            if side_intervals(e, s, zone): out.append(e); break
    return out

# ---------------------------------------------------------------- corridors: chains of straight edges of one type (a street that goes on)
def build_corridors():
    G = {}
    for e in DP['edges']:
        hz = abs(e['ay'] - e['by']) < .5; vt = abs(e['ax'] - e['bx']) < .5
        if not (hz or vt) or e['cls'] not in KIT: continue
        o = 'h' if hz else 'v'; ax = round(e['ay'] if hz else e['ax'])
        c0, c1 = sorted((e['ax'], e['bx']) if hz else (e['ay'], e['by']))
        G.setdefault((o, ax, e['cls']), []).append((c0, c1, e))
    out = []
    for (o, ax, cls), L in G.items():
        L.sort(key=lambda q: q[0]); cur = None
        for c0, c1, e in L:
            if cur and abs(c0 - cur['c1']) < 1: cur['edges'].append(e); cur['c1'] = max(cur['c1'], c1)
            else:
                cur = {'o': o, 'axis': ax, 'cls': cls, 'c0': c0, 'c1': c1, 'edges': [e], 'w': e['w'], 'sw': e['sw']}; out.append(cur)
    return out
CORR = build_corridors()
def edge_side(e, g, o):
    L, ux, uy, nx, ny = geo(e)
    return (1 if ny > 0 else -1) * g if o == 'h' else (1 if nx > 0 else -1) * g
def cof(e, t, o):
    L, ux, uy, nx, ny = geo(e); return (e['ax'] + ux * t) if o == 'h' else (e['ay'] + uy * t)
def corr_items(C, g, what):
    out = []
    for e in C['edges']:
        s = edge_side(e, g, C['o'])
        for q in (lamps_on_side(e, s) if what == 'lamp' else trees_on_side(e, s)):
            out.append((cof(e, q[0], C['o']),) + tuple(q[1:]))
    return sorted(out)
def corr_openings(C, g):
    out = []
    for e in C['edges']:
        for a, b in openings_on_side(e, edge_side(e, g, C['o'])):
            x, y = sorted((cof(e, a, C['o']), cof(e, b, C['o']))); out.append((x, y))
    return out
def corr_nodes(C):
    """the junctions along the corridor: c, the band of the crossing street, and the sides it joins from"""
    ids = {e['id'] for e in C['edges']}; out = {}
    for e in C['edges']:
        for n, x, y in ((e['a'], e['ax'], e['ay']), (e['b'], e['bx'], e['by'])):
            c = x if C['o'] == 'h' else y
            for o in BY_NODE.get(n, []):
                if o['id'] in ids: continue
                L1, ux, uy, _, _ = geo(e); L2, vx, vy, _, _ = geo(o)
                if abs(ux * vx + uy * vy) > .95: continue
                ox, oy = (o['bx'], o['by']) if o['a'] == n else (o['ax'], o['ay'])
                side = (1 if oy > y else -1) if C['o'] == 'h' else (1 if ox > x else -1)
                q = out.setdefault(n, {'c': c, 'band': 0, 'sides': set()}); q['band'] = max(q['band'], o['w'] / 2 + o['sw']); q['sides'].add(side)
    return list(out.values())
def corr_zone_intervals(C, g, zone):
    off = C['w'] / 2 + C['sw'] / 2; r = ZONES[zone]['rect']; out = []; cur = None; c = C['c0']
    while c <= C['c1'] + 1e-6:
        x, y = (c, C['axis'] + g * off) if C['o'] == 'h' else (C['axis'] + g * off, c)
        if inrect(x, y, r):
            if cur is None: cur = [c, c]
            cur[1] = c
        elif cur is not None: out.append(cur); cur = None
        c += 2.0
    if cur is not None: out.append(cur)
    return [iv for iv in out if iv[1] - iv[0] >= 30]
def gname(C, g): return ('הצד הדרומי' if g > 0 else 'הצד הצפוני') if C['o'] == 'h' else ('הצד המזרחי' if g > 0 else 'הצד המערבי')
def corr_label(C, z0, z1):
    es = [e for e in C['edges'] if min(cof(e, 0, C['o']), cof(e, geo(e)[0], C['o'])) < z1 and max(cof(e, 0, C['o']), cof(e, geo(e)[0], C['o'])) > z0]
    nm = es[0].get('name', es[0]['id']).split(' — ')[0] if es else C['edges'][0]['id']
    return '%s (%s)' % (nm, ' · '.join(e['id'] for e in es))
def gaps_along(P, z0, z1, ends, bands, ops):
    """the gaps of a row of points between z0 and z1: between neighbours, and from a junction or a dead end to the first point;
    a junction band and an opening inside a gap do not count. ends: {'lo': c or None, 'hi': c or None} — where an end gap is measured from"""
    ivs = list(bands) + list(ops); G = []
    def eff(a, b): return (b - a) - overlap(a, b, ivs)
    for a, b in zip(P, P[1:]): G.append(eff(a, b))
    E = []
    if P:
        if ends['lo'] is not None: E.append(max(0, eff(ends['lo'], P[0])))
        if ends['hi'] is not None: E.append(max(0, eff(P[-1], ends['hi'])))
    else:
        lo = ends['lo'] if ends['lo'] is not None else z0; hi = ends['hi'] if ends['hi'] is not None else z1
        E.append(max(0, eff(lo, hi)))
    return G, E
def corr_ends(C, g, z0, z1, nodes):
    """an end gap is measured only where the zone's stretch reaches a junction or a dead end, never at a seam"""
    ends = {'lo': None, 'hi': None}
    for key, cz, cend in (('lo', z0, C['c0']), ('hi', z1, C['c1'])):
        if abs(cz - cend) > 3: continue
        x, y = (cend, C['axis']) if C['o'] == 'h' else (C['axis'], cend)
        if on_boundary(x, y): continue
        nd = [q for q in nodes if abs(q['c'] - cend) < 1]
        band = max([q['band'] for q in nd], default=0)
        ends[key] = cend + band if key == 'lo' else cend - band
    return ends
def check_streets(zone):
    for e in edges_in(zone):
        k = KIT.get(e['cls']); name = e.get('name', e['id']).split(' — ')[0]
        if not k: continue
        need = 'רוחב %d · %d נתיבים · מדרכה %d' % (k['width_px'], k['lanes'], k['sidewalk_px'])
        have = 'רוחב %d · %d נתיבים · מדרכה %d' % (e['w'], e['tl'], e['sw'])
        row(zone, 'C-05', '%s (%s) — החתך' % (name, e['id']), need, have, e['w'] == k['width_px'] and e['tl'] == k['lanes'] and e['sw'] == k['sidewalk_px'], 'K')
    for C in CORR:
        k = KIT[C['cls']]; sp = k['lamp']['spacing_px']; mn = k['lamp'].get('min_gap_px') or 0; nodes = corr_nodes(C)
        for g in (1, -1):
            for z0, z1 in corr_zone_intervals(C, g, zone):
                tag = '%s · %s' % (corr_label(C, z0, z1), gname(C, g))
                bands = [(q['c'] - q['band'], q['c'] + q['band']) for q in nodes if g in q['sides']]
                ends = corr_ends(C, g, z0, z1, nodes)
                Ls = [q for q in corr_items(C, g, 'lamp') if z0 - 4 <= q[0] <= z1 + 4]
                bad = sorted({q[1] for q in Ls if q[1] != k['lamp']['asset']})
                row(zone, 'C-01', tag + ' — סוג הפנס', k['lamp']['asset'], ', '.join(sorted({q[1] for q in Ls})) or 'אין פנסים', not bad, 'K')
                P = [q[0] for q in Ls]; G, E = gaps_along(P, z0, z1, ends, bands, [])
                mx = max(G + E) if (G + E) else 0; hint = ''
                if mx > sp + .5:
                    pts = ([ends['lo']] if ends['lo'] is not None else [z0]) + P + ([ends['hi']] if ends['hi'] is not None else [z1])
                    big = [(a, b) for a, b in zip(pts, pts[1:]) if b - a > sp]
                    ops = corr_openings(C, g)
                    if any(overlap(a, b, ops) > 0 for a, b in big): hint = ' · בפער יש כניסה או מעבר (K‑187)'
                row(zone, 'C-02', tag + ' — המרחק בין הפנסים', 'עד %d' % sp, '%d פנסים · הפער הגדול %d%s' % (len(P), mx, hint), mx <= sp + .5, 'K')
                raw = [b - a for a, b in zip(P, P[1:])]
                if raw: row(zone, 'C-03', tag + ' — המרחק המזערי', 'לפחות %d' % mn, 'הקרוב %d' % min(raw), min(raw) >= mn - .5, 'K')
                Ts = [q for q in corr_items(C, g, 'tree') if z0 - 4 <= q[0] <= z1 + 4]; T = [q[0] for q in Ts]
                if k['trees']['spacing_px']:
                    lo, hi = k['trees']['spacing_px']; G, E = gaps_along(T, z0, z1, ends, bands, corr_openings(C, g))
                    raw = [b - a for a, b in zip(T, T[1:])]
                    big = [x for x in G + E if x > hi + .5]; small = [x for x in raw if x < lo - .5]
                    have = '%d עצים · הפער הגדול %s' % (len(T), fmt(max(G + E)) if (G + E) else '—')
                    if big: have += ' · %d פערים מעל %d' % (len(big), hi)
                    if small: have += ' · %d צפופים מ-%d' % (len(small), lo)
                    row(zone, 'C-04', tag + ' — עצי השדרה', 'עץ כל %d–%d (בלי כניסות, מעברים ומפרצים)' % (lo, hi), have, not big and not small, 'K')
                else:
                    row(zone, 'C-04', tag + ' — עצי הרחוב', 'לא נקבע (ס-3)', '%d עצים' % len(T), True, 'K', info=True)
    # the lanes of B3 (the paved courts): a lamp every 200 px (D‑328)
    for lot in (ZDATA['ZB3'].get('lots', []) if zone == 'B3' else []):
        if not lot['id'].startswith('B3-LN-'): continue
        y = lot['yard']; hz = y['w'] >= y['h']; a, b = (y['x'], y['x'] + y['w']) if hz else (y['y'], y['y'] + y['h'])
        P = sorted([(lx if hz else ly) for (lx, ly, asset, rid, src) in LAMPS if rid is None and y['x'] - 14 <= lx <= y['x'] + y['w'] + 14 and y['y'] - 14 <= ly <= y['y'] + y['h'] + 14])
        g = [q - p for p, q in zip([a] + P, P + [b])]; sp = KIT['lane']['lamp']['spacing_px']
        row(zone, 'C-02', '%s (%s) — פנס כל 20 מ׳' % (lot['label'], lot['id']), 'עד %d' % sp, '%d פנסים · הפער הגדול %d' % (len(P), max(g)), max(g) <= sp + .5, 'K')

# ---------------------------------------------------------------- parking, doors, signs, markings, stops, accesses
NOT_CAR = re.compile(GD['parking']['not_car_lots'])
def stalls_in(zone):
    seen, out = set(), []
    for s in DP['stalls'] + DP.get('stallsZone', []):
        k = (s['x'], s['y'], s['w'], s['h'])
        if k in seen: continue
        seen.add(k)
        if zone_of(s['x'] + s['w'] / 2, s['y'] + s['h'] / 2) == zone: out.append(s)
    return out
def all_lamp_xy(): return [(x, y) for (x, y, a, r, s) in LAMPS]
LXY = all_lamp_xy()
def near_lamp(x, y, R): return min((math.hypot(x - a, y - b) for a, b in LXY), default=1e9) <= R
def check_parking(zone):
    S = [s for s in stalls_in(zone) if not NOT_CAR.search(str(s.get('lot', '')) + ' ' + str(s.get('id', '')))]
    W0, H0 = GD['parking']['stall_px']
    bad = [s for s in S if sorted((round(s['w']), round(s['h']))) != sorted((W0, H0))]
    sizes = {}
    for s in bad: sizes['%d × %d' % (s['w'], s['h'])] = sizes.get('%d × %d' % (s['w'], s['h']), 0) + 1
    row(zone, 'C-07', 'מידות החניות', '%d × %d בכל חניה' % (W0, H0), ('%d חניות' % len(S)) + ((' · ' + ', '.join('%s: %d' % kv for kv in sizes.items())) if sizes else ' · כולן בגודל'), not bad, 'P')
    # special stalls per car park
    pos = {s['id']: s for s in DP['stalls'] + DP.get('stallsZone', []) if 'id' in s}
    for L in DP.get('special', {}).get('lots', []):
        s = pos.get(L['first'])
        if not s or zone_of(s['x'] + s['w'] / 2, s['y'] + s['h'] / 2) != zone: continue
        if L['n'] < GD['parking']['min_lot']: continue
        row(zone, 'C-08', 'חניון %s (%d חניות)' % (L['first'], L['n']), 'נכים %d · חשמל %d' % (L['needA'], L['needE']), 'נכים %d · חשמל %d' % (L['acc'], L['ev']), L['acc'] >= L['needA'] and L['ev'] >= L['needE'], 'P')
    # lighting
    R = GD['parking']['lamp_radius_px']; pub = [s for s in S if not s.get('house') and not str(s.get('lot', '')).endswith('-DW')]
    dark = [s for s in pub if not near_lamp(s['x'] + s['w'] / 2, s['y'] + s['h'] / 2, R)]
    if pub: row(zone, 'C-09', 'תאורה בחניונים', 'כל חניה עד %d מפנס' % R, '%d מתוך %d' % (len(pub) - len(dark), len(pub)) + ((' · בחושך: ' + ', '.join(sorted({str(s.get('id'))[:14] for s in dark})[:6])) if dark else ''), not dark, 'P')
def buildings_in(zone):
    return [b for b in DP.get('buildings', []) if b.get('type') and zone_of(b['x'] + b.get('w', 0) / 2, b['y'] + b.get('h', 0) / 2) == zone]
def check_doors(zone):
    R = GD['parking']['door_lamp_radius_px']
    for b in buildings_in(zone):
        if not b.get('ent'): continue
        d = min((math.hypot(b['ent'][0] - a, b['ent'][1] - c) for a, c in LXY), default=1e9)
        row(zone, 'C-10', '%s (%s) — פנס ליד הדלת' % (b['label'], b['id']), 'עד %d' % R, 'הפנס הקרוב %d' % d, d <= R, 'P')
    racks = [(x, y) for (x, y, a, s) in PROPS if a == GD['design']['bike_rack']]
    for b in buildings_in(zone):
        if b.get('kind') not in GD['design']['public_kinds'] or not b.get('ent'): continue
        d = min((math.hypot(b['ent'][0] - a, b['ent'][1] - c) for a, c in racks), default=None)
        row(zone, 'C-22', '%s (%s) — מתקן אופניים' % (b['label'], b['id']), 'עד %d מהדלת' % GD['design']['bike_radius_px'],
            ('הקרוב %d' % d) if d is not None else 'אין מתקן באזור', d is not None and d <= GD['design']['bike_radius_px'], 'D')
def check_signs(zone):
    r = ZONES[zone]['rect']; fam = set(GD['signs']['family'])
    signs = [s for s in DP.get('signs', []) if inrect(s['x'], s['y'], r)] + [{'asset': a, 'x': x, 'y': y} for (x, y, a, src) in PROPS if a.startswith('RF-') and inrect(x, y, r)]
    other = [s for s in signs if s['asset'] not in fam]
    row(zone, 'C-11', 'משפחת התמרורים', 'רק ' + ', '.join(sorted(fam)[:6]) + '…', '%d תמרורים באזור' % len(signs) + ((' · מחוץ למשפחה: %d' % len(other)) if other else ''), not other, 'T')
    yl = [l for l in DP.get('stopLines', []) if l.get('kind') != 'stop' and inrect(l['x'], l['y'], r)]
    have = 0
    for l in yl:
        if any(s['asset'] == GD['signs']['minor_arm'] and math.hypot(s['x'] - l['x'], s['y'] - l['y']) <= 120 for s in signs): have += 1
    if yl: row(zone, 'C-11', 'תמרור עצור או תן זכות בזרוע משנית', '%d (כמו קווי "תן זכות")' % len(yl), '%d' % have, have >= len(yl), 'T')
    names = [n for n in DP.get('names', []) if inrect(n['x'], n['y'], r)]
    badn = [n['t'] for n in names if re.search(r'[A-Za-z]', n['t'])]
    row(zone, 'C-12', 'שמות הרחובות', 'עברית בלבד, בלי קוד של אזור', '%d שמות' % len(names) + ((' · לא בעברית: ' + ', '.join(badn)) if badn else ' · כולם בעברית: ' + ', '.join(sorted({n['t'] for n in names}))), not badn, 'T')
MARK_ARROWS = bool(re.search(r'[Aa]rrow', GAME[GAME.find('function drawMarkings('):GAME.find('function edgeAxis(')]))
def check_marks(zone):
    r = ZONES[zone]['rect']
    for n in sorted(SIGNAL_NODES):
        if n not in NODE_XY or not inrect(*NODE_XY[n], r): continue
        arms = len(BY_NODE.get(n, []))
        sl = [l for l in DP.get('stopLines', []) if l.get('node') == n and l.get('kind') == 'stop']
        row(zone, 'C-13', 'רמזור %s — קווי עצירה' % n, '%d (גישה לכל זרוע)' % arms, '%d' % len(sl), len(sl) >= arms, 'M')
        row(zone, 'C-13', 'רמזור %s — חץ על הנתיב בכל גישה' % n, '%d' % arms, '%d' % (arms if MARK_ARROWS else 0), MARK_ARROWS, 'M')
    for n, es in BY_NODE.items():
        if n in SIGNAL_NODES or len(es) < 3 or not inrect(*NODE_XY[n], r): continue
        yl = [l for l in DP.get('stopLines', []) if l.get('node') == n and l.get('kind') != 'stop']
        row(zone, 'C-13', 'צומת %s — קו "תן זכות" בזרוע המשנית' % n, 'לפחות 1', '%d' % len(yl), len(yl) >= 1, 'M')
    cws = [c for c in CW if inrect(c['x'], c['y'], r)]
    if cws: row(zone, 'C-13', 'מעברי חצייה', 'צייר אחד (פס 5, רווח 6, עומק 30 / 34)', '%d מעברים בצייר האחד' % len(cws), True, 'M')
def check_xw_place(zone):
    """C-29 (R-76): every crossing — at a junction of 3 arms or more, at most 1 m (10 px) after its stop line (the stop line: the street it
    crosses + half the depth + 12, as the game builds it)"""
    r = ZONES[zone]['rect']; E = {e['id']: e for e in DP['edges']}
    for c in list(CW) + list(DP.get('zebras', [])):
        if not inrect(c['x'], c['y'], r): continue
        e = E.get(c.get('roadId')); tag = 'מעבר %s (%s)' % ((c.get('label') or '').replace('מעבר חציה — ', '').replace('מעבר חצייה — ', '').split(' · ')[0] or c['id'], c['id'])
        if not e:
            row(zone, 'C-29', tag + ' — בצומת', 'בצומת', 'בלי כביש', False, 'M'); continue
        n = c.get('signalNode') or c.get('node')
        if n not in (e['a'], e['b']):
            n = min((e['a'], e['b']), key=lambda q: math.hypot(c['x'] - NODE_XY[q][0], c['y'] - NODE_XY[q][1]))
        nx, ny = NODE_XY[n]; arms = BY_NODE.get(n, []); L = geo(e)[0]
        ox, oy = (e['bx'], e['by']) if e['a'] == n else (e['ax'], e['ay']); ex_, ey_ = ox - nx, oy - ny; el = math.hypot(ex_, ey_) or 1
        ch = 0
        for q in arms:
            if q['id'] == e['id']: continue
            px, py = (q['bx'], q['by']) if q['a'] == n else (q['ax'], q['ay']); qx, qy = px - nx, py - ny; ql = math.hypot(qx, qy) or 1
            if abs((ex_ * qx + ey_ * qy) / (el * ql)) < .7: ch = max(ch, q['w'] / 2)
        dep = 34 if e['cls'] in ('arterial', 'main') else 30
        exp = min(L - dep / 2, (ch or max(q['w'] / 2 for q in arms)) + dep / 2 + 12); d = math.hypot(c['x'] - nx, c['y'] - ny)
        ok = len(arms) >= 3 and d <= exp + 10
        have = ('%d זרועות' % len(arms)) + (' · %.1f מ׳ אחרי קו העצירה' % ((d - exp) / 10) if d > exp + .5 else ' · צמוד לקו העצירה')
        row(zone, 'C-29', tag + ' — בצומת, צמוד לקו העצירה', 'צומת של 3 זרועות לפחות · עד 1 מ׳ אחרי קו העצירה', have, ok, 'M')
def check_stops(zone):
    r = ZONES[zone]['rect']; E = {e['id']: e for e in DP['edges']}
    for st in STOPS:
        if not inrect(st['x'], st['y'], r): continue
        e = E.get(st.get('edgeId')); tag = '%s (%s)' % (st.get('label', st['id']).split(' · ')[1] if ' · ' in st.get('label', '') else st['id'], st['id'])
        row(zone, 'C-14', tag + ' — מפרץ', 'מפרץ של 150 + 40 + 40', 'יש מפרץ' if st.get('bay') else 'אין מפרץ — עוצר בנתיב', bool(st.get('bay')), 'B')
        if e:
            t = proj(e, st['x'], st['y'])[0]; L = geo(e)[0]; best = None
            for node, tt in ((e['a'], 0), (e['b'], L)):
                if NODE_DEG.get(node, 0) < 2 and node not in SIGNAL_NODES: continue
                pad = 74 if (tt > t) == (st.get('dirSign', 1) > 0) else 66
                d = abs(tt - t) - junction_band(e, node) - pad
                best = d if best is None else min(best, d)
            if best is not None:
                row(zone, 'C-14', tag + ' — המרחק מהצומת', 'לפחות %d' % GD['stop']['min_junction_px'], '%d' % best, best >= GD['stop']['min_junction_px'], 'B')
def check_access(zone):
    r = ZONES[zone]['rect']; need = []; cuts = [a for a in DP.get('access', [])] + [{'x': o['x'], 'y': o['y'], 'w': o['w'], 'h': o['h']} for o in OPEN]
    for zk in ZONES[zone].get('data', []):
        Z = ZDATA[zk]; parts = [Z] if zk != 'ZCD' else [Z['c4'], Z['d4']]
        for P in parts:
            for lot in P.get('lots', []) or []:
                for a in lot.get('acc', []) or []:
                    if inrect(a['x'] + a['w'] / 2, a['y'] + a['h'] / 2, r): need.append((lot['id'], a))
    def hit(a):
        return any(not (c['x'] > a['x'] + a['w'] + 2 or c['x'] + c['w'] < a['x'] - 2 or c['y'] > a['y'] + a['h'] + 2 or c['y'] + c['h'] < a['y'] - 2) for c in cuts)
    miss = [i for i, a in need if not hit(a)]
    if need: row(zone, 'C-15', 'הנמכה בכל כניסה למגרש', '%d כניסות' % len(need), '%d עם הנמכה' % (len(need) - len(miss)) + ((' · בלי: ' + ', '.join(miss)) if miss else ''), not miss, 'P')
    cz = [a for a in DP.get('access', []) if inrect(a['x'] + a['w'] / 2, a['y'] + a['h'] / 2, r)]
    if cz and not need: row(zone, 'C-15', 'הנמכות באזור', 'הנמכה בכל כניסה', '%d הנמכות בצייר האחד' % len(cz), True, 'P')

# ---------------------------------------------------------------- boundaries, palette, heights, doors, variety
def check_bounds(zone):
    B = GD['boundaries']; r = ZONES[zone]['rect']
    if zone in B['hedge_zones']:
        hz = [(h[0], h[1]) for look in ('B3LOOKD', 'C3D', 'D3ND') for h in ZD.get(look, {}).get('hedges', [])]
        lots = []
        for zk in ZONES[zone]['data']: lots += [L for L in ZDATA[zk].get('houselots', []) if SB.BLD.get(L['id'], {}).get('kind') in ('residential', 'villa')]
        nb = 10
        for L in lots:
            x0, y0, x1, y1 = L['lot']
            n = sum(1 for (x, y) in hz if x0 - nb <= x <= x1 + nb and y0 - nb <= y <= y1 + nb and min(abs(x - x0), abs(x - x1), abs(y - y0), abs(y - y1)) <= nb)
            per = 2 * ((x1 - x0) + (y1 - y0))
            row(zone, 'C-16', 'גדר חיה — המגרש של %s' % L['id'], 'גדר חיה בגבול המגרש', '%d שיחים לאורך הגבול (כ-%d%% מההיקף)' % (n, min(100, round(100 * n * 33 / per))), n >= 1, 'E')
    if zone in B['wall_zones']:
        segs = (ZD.get('D4ND', {}).get('fence') or []) if zone == 'D4' else []
        ln = sum(math.hypot(s[2] - s[0], s[3] - s[1]) for s in segs)
        row(zone, 'C-16', 'חומה בגבול של התעשייה', 'חומה (ס-12)', ('גדר אבטחה: %d קטעים, %d פיקס׳' % (len(segs), ln)) if segs else 'אין חומה ואין גדר', False, 'E')
    if zone in B['buffer']:
        q = B['buffer'][zone]; band = GD['method']['buffer_band_px']
        n = sum(1 for (x, y, a, s) in TREES if r[0] <= x < r[2] and r[1] <= y < r[1] + band)
        row(zone, 'C-16', 'חיץ העצים בגבול הצפוני (מול המגורים)', 'לפחות %d עצים ב-%d פיקס׳ מהגבול' % (q['min'], band), '%d' % n, n >= q['min'], 'E')
def look(tid):
    for p in GD['palettes'].values():
        if tid in p['types']: return p['types'][tid]
    L = SB.type_look(tid); return {k: L[k] for k in ('fn', 'mat', 'wall', 'roof', 'roof_kind', 'floors', 'he')}
# 2.11 08:30 (הבונה): הגבהים נקראים מהמנוע עצמו (לא מוקלדים) — הפונקציה, ואז הביטוי; כשהמנוע משתנה, הבדיקה רואה את זה
def _floor_h(fn):
    i = GAME.find('function ' + fn + '('); j = GAME.find('\n  function ', i + 20) if i >= 0 else -1; body = GAME[i:j if j > 0 else i + 12000] if i >= 0 else ''
    def g(pat):
        m = re.search(pat, body); return float(m.group(1)) if m else None
    if fn in ('houseType', 'rowType', 'aptType'): v = [g(r'\bgh = ([\d.]+)'), g(r'\bfh = ([\d.]+)')]
    elif fn == 'aptL2Type': v = [g(r'\bgh: ([\d.]+)'), g(r'\bfh: ([\d.]+)')]
    elif fn == 'schoolType': v = [g(r'\bHS = ([\d.]+) \* NF')]
    elif fn == 'officeType': v = [g(r'\bfh = ([\d.]+)')]
    elif fn == 'clinicType': h = g(r'h: ([\d.]+), main: true'); v = [h / 2 if h else None]
    else: v = []
    return [x for x in v if x is not None]
FLOOR_H = {fn: (_floor_h(fn), 'המנוע: ' + fn) for fn in ('houseType', 'rowType', 'aptType', 'aptL2Type', 'schoolType', 'officeType', 'clinicType')}
def door_specs(fn, tp=None):
    i = GAME.find('function ' + fn + '('); j = GAME.find('\n  function ', i + 20) if i >= 0 else -1
    body = GAME[i:j if j > 0 else i + 12000]; out = []
    body = re.sub(r"door\(c, \{[^}]*\},", "door(c, F,", body)
    for m in re.finditer(r"\bdoor\(c, [^,]+, [^,]+, ([^,]+), ([\d.]+)(?:, \{([^}]*)\})?", body):
        wexpr, h, opt = m.group(1), float(m.group(2)), m.group(3) or ''
        tern = re.search(r'o\.(\w+)\s*\?\s*([\d.]+)\s*:\s*([\d.]+)', wexpr)
        if tern and tp is not None: ws = [float(tern.group(2) if tp.get(tern.group(1)) else tern.group(3))]
        else: ws = [float(v) for v in re.findall(r'\d+(?:\.\d+)?', wexpr)] or ([float((re.search(r'\bdw = ([\d.]+)', body) or [0, 11])[1])] if 'dw' in wexpr else [])   # 2.11 08:35: dw נקרא מהמנוע
        lv = re.search(r'leaves:\s*(\d)', opt)
        for w in ws:
            n = int(lv.group(1)) if lv else (2 if w > 14 else 1)
            out.append((round(w / n / 10, 2), h, n))
    return sorted(set(out))
def check_buildings(zone):
    dist = ZONES[zone]['district']; P = GD['palettes'].get(dist)
    BS = buildings_in(zone); H = GD['heights']
    for b in BS:
        L = look(b['type'])
        if P:
            miss = [k for k, key in (('wall', 'walls'), ('roof', 'roofs'), ('mat', 'materials'), ('roof_kind', 'roof_kinds')) if L.get(k) and L[k] not in {v['v'] for v in P[key]}]
            row(zone, 'C-17', '%s (%s)' % (b['label'], b['id']), 'בתוך הפלטה של רובע %s' % dist, 'קיר %s · גג %s · %s · גג %s' % (L['wall'], L['roof'], L['mat'], L['roof_kind']) + ((' · מחוץ: ' + ', '.join(miss)) if miss else ''), not miss, 'D')
        fn = L['fn']; fl = L['floors']; kind = b.get('kind')
        if fn in ('aptType', 'aptL2Type'): lim, what = H['apartment_max'], 'בניין דירות'
        elif fn == 'schoolType': lim, what = H['school_max'], 'בית ספר'
        elif fn == 'marketType' or b['type'].startswith('MARKET'): lim, what = H['market_max'], 'סופר'
        elif fn in ('houseType', 'rowType'): lim, what = H['house_floors'], 'בית / וילה'
        else: lim, what = None, None
        if lim: row(zone, 'C-18', '%s (%s) — %s' % (b['label'], b['id'], what), 'עד %d קומות' % lim, '%d קומות' % fl, fl <= lim, 'H')
    seen = set(); ids_of = {}
    for b in BS: ids_of.setdefault(b['type'], []).append(b['id'])
    for b in BS:
        L = look(b['type']); fn = L['fn']
        if b['type'] in seen: continue
        seen.add(b['type']); tname = 'הדגם של ' + ', '.join(ids_of[b['type']])
        if b.get('kind') in H['kinds_with_floors'] and fn in FLOOR_H:
            hs, s = FLOOR_H[fn]; lo, hi = H['floor_m']
            row(zone, 'C-19', tname + ' — גובה קומה', '%.1f–%.1f מ׳' % (lo, hi), ' · '.join('%.2f' % v for v in hs) + ' מ׳', all(lo - 1e-6 <= v <= hi + 1e-6 for v in hs), 'S')
        ds = door_specs(fn, SB.TYPES.get(b['type'], {}))
        if ds:
            w0, h0 = H['door_m']; tol = H['tol']
            ok = all(abs(w - w0) <= w0 * tol + 1e-6 and abs(h - h0) <= h0 * tol + 1e-6 for w, h, n in ds)
            row(zone, 'C-20', tname + ' — הדלת', 'כנף %.1f × %.1f מ׳' % (w0, h0), ' · '.join('%s%.2f × %.1f' % ('%d כנפיים · ' % n if n > 1 else '', w, h) for w, h, n in ds), ok, 'S')
    # variety
    by = {}
    for b in BS: by.setdefault(b.get('kind'), []).append(b)
    for kind, L in by.items():
        if len(L) >= 3:
            n = len({b['type'] for b in L})
            row(zone, 'C-21', 'מגוון — %s (%d מבנים)' % (KIND_HE.get(kind, 'סוג אחר'), len(L)), 'לפחות %d דגמים' % GD['design']['variety_min'], '%d דגמים' % n, n >= GD['design']['variety_min'], 'D')
    gap = GD['method']['neighbor_gap_px']; pairs = []
    for i, a in enumerate(BS):
        for b in BS[i + 1:]:
            if a['type'] != b['type']: continue
            dx = max(0, max(a['x'], b['x']) - min(a['x'] + a['w'], b['x'] + b['w'])); dy = max(0, max(a['y'], b['y']) - min(a['y'] + a['h'], b['y'] + b['h']))
            if math.hypot(dx, dy) <= gap: pairs.append('%s ו-%s (%s, %d פיקס׳)' % (a['id'], b['id'], a['type'], math.hypot(dx, dy)))
    row(zone, 'C-21', 'שני מבנים זהים זה ליד זה', 'אין (עד %d פיקס׳ זה מזה)' % gap, ' · '.join(pairs) if pairs else 'אין', not pairs, 'D')

KIND_HE = {'residential': 'מגורים', 'villa': 'וילות', 'service': 'שירותי רכב', 'shop': 'חנויות', 'sport': 'ספורט', 'emergency': 'חירום', 'public': 'ציבור',
           'school': 'בית ספר', 'clinic': 'מרפאה', 'office': 'משרדים', 'factory': 'מפעל', 'warehouse': 'מחסן', 'depot': 'מחסן', 'distribution': 'מרכז הפצה',
           'dock-terminal': 'רציפים', 'rail-warehouse': 'מחסן רכבת', 'gatehouse': 'ביתן שער', 'market': 'סופר'}
# ---------------------------------------------------------------- the city standards
def getp(path):
    k, *rest = path.split('.')
    o = ZD.get(k) if k in ZD else ZDATA.get(k)
    for p in rest:
        if o is None: return None
        if p == 'pad' and isinstance(o, list): o = next((l.get('pad') for l in o if l.get('pad')), None)
        else: o = o.get(p) if isinstance(o, dict) else None
    return o
def check_std(zone):
    T = GD['helipads']['table']
    for p in GD['helipads']['pads']:
        if p['zone'] != zone: continue
        o = getp(p['path'])
        if not o: continue
        need = T[p['heli']]; d, ring = 2 * o[p['r']] / 10, 2 * o[p['safe']] / 10
        row(zone, 'C-23', 'המנחת %s — %s' % (p['id'], need['he']), 'מנחת %g מ׳ · טבעת %g מ׳' % (need['pad_m'], need['ring_m']), 'מנחת %g מ׳ · טבעת %g מ׳' % (d, ring), abs(d - need['pad_m']) < .5 and abs(ring - need['ring_m']) < .6, 'N')
        a, win, rx = p['probe']; i = GAME.find(a); has = i >= 0 and rx in GAME[i:i + win]
        row(zone, 'C-23', 'המנחת %s — מסוק על המנחת' % p['id'], 'מסוק', 'יש מסוק בציור' if has else 'אין מסוק בציור של המנחת', has, 'N')
    for k, q in GD['emergency'].items():
        if q['zone'] != zone: continue
        if 'path' in q: n = len(getp(q['path']) or [])
        else: n = int(SB.TYPES.get(q['type'], {}).get('n', 0))
        row(zone, 'C-24', 'תאי החירום — %s' % k, '%d' % q['need'], '%d' % n, n >= q['need'], 'N')
    if zone in ('A3', 'A4'):
        for name, c in GD['sports']['courts'].items():
            r = getp(c['path'])
            if not r: continue
            cx = (r[0] + r[2]) / 2; cy = (r[1] + r[3]) / 2
            if zone_of(cx, cy) != zone: continue
            m = sorted([(r[2] - r[0]) / 10, (r[3] - r[1]) / 10], reverse=True); need = sorted(c['m'], reverse=True)
            ok = m[0] >= need[0] - .3 and m[1] >= need[1] - .3
            row(zone, 'C-25', name, '%g × %g מ׳' % tuple(need), '%g × %g מ׳' % tuple(m), ok, 'N')
    # people and vehicles: every parked car of the zone is a city type that the sizes table measures at its size
    ok_ref = {r['key'] for r in DP.get('sizes', {}).get('table', []) if r.get('group') == 'city' and r.get('ok')}
    r = ZONES[zone]['rect']; cars = [c for c in DP.get('parked', []) if inrect(c['x'], c['y'], r)]
    bad = [c for c in cars if c.get('ref') and c['ref'] not in ok_ref]
    pers = next((x for x in DP.get('sizes', {}).get('table', []) if x.get('group') == 'person'), None)
    row(zone, 'C-27', 'הרכבים החונים באזור', 'כל רכב בגודל הטבלה (×1.125)', '%d רכבים' % len(cars) + ((' · לא בטבלה: %d' % len(bad)) if bad else ' · כולם בגודל'), not bad, 'N')
    if pers: row(zone, 'C-27', 'האדם', '%.1f פיקס׳' % pers['tL'], '%.1f פיקס׳' % pers['L'], pers['ok'], 'N')

def check_city():
    """the code of the city — one painter for the night light, the arrows"""
    i = GAME.find("'SL-RES':{H:20"); heads = set(re.findall(r"lc=N\?'(#[0-9a-f]+)'", GAME)) | set(re.findall(r"ci\(c,hx,hy,2,N\?'(#[0-9a-f]+)'", GAME))
    kit = set(re.findall(r"c\.fillStyle = lt \? '(rgba\([^']+\))'", GAME)); bld = set(re.findall(r"rg\(c, x - 1, y - 27, 14, \['(rgba\([^']+\))'", GAME))
    pool = set(re.findall(r"createRadialGradient\(hx,by,2,hx,by,m\.lr\*pl\);g\.addColorStop\(0,'(rgba\([^']+\))'", GAME))
    cols0 = sorted(heads | kit | bld | pool)
    def rgb(c):   # 2.11 08:40 (הבונה): הצבע נבדק לפי ה-RGB; העוצמה — לפי סוג (ראש / אלומה), בשורה הבאה
        if c.startswith('#'): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
        m = re.match(r'rgba\(([^)]*)\)', c); v = [x.strip() for x in m.group(1).split(',')]; return tuple(int(float(x)) for x in v[:3])
    cols = sorted({'#%02x%02x%02x' % rgb(c) for c in cols0})
    alph = lambda S: sorted({re.match(r'rgba\(([^)]*)\)', c).group(1).split(',')[3].strip() for c in S if c.startswith('rgba')})
    def he_col(c):
        m = re.match(r'rgba\(([^)]*)\)', c)
        if not m: return c
        v = [x.strip() for x in m.group(1).split(',')]; return 'צבע %s שקיפות %s' % (','.join(v[:3]), v[3])
    row('העיר', 'C-26', 'צבע האור בלילה — כל הפנסים', 'צבע אחד: %s' % GD['night']['head'], '%d צבעים: %s' % (len(cols), ' · '.join(cols)), len(cols) <= 1 and (not cols or cols[0] == GD['night']['head'].lower()), 'N')
    row('העיר', 'C-26', 'עוצמת האור — הראש של הפנס ואלומת האור', 'עוצמה אחת לכל סוג', 'הראש: %s · האלומה: %s' % (', '.join(alph(kit)) or '—', ', '.join(alph(bld | pool)) or '—'), len(alph(kit)) <= 1 and len(alph(bld | pool)) <= 1, 'N')
    j = GAME.find('const SLD={'); lrs = sorted({int(v) for v in re.findall(r'lr:(\d+)', GAME[j:j + 2500])})
    k = GAME.find("lamp({ he: 'פנס שכונה'"); kit_pool = bool(re.search(r'createRadialGradient|pool', GAME[GAME.rfind('function lamp(p)', 0, k):k])) or ('function drawLampPools()' in GAME and 'drawLampPools();for(const o of __allPoles)' in GAME)   # 2.11 (p485): שכבה אחת לכל הפנסים
    have = 'בערכת ה-3/4, שמציירת את הפנסים של העיר — %s; בנכסים הישנים — אלומה ברדיוס %d–%d פיקס׳ לפי סוג הפנס' % ('יש' if kit_pool else 'אין אלומה', lrs[0], lrs[-1])
    row('העיר', 'C-26', 'אלומת אור על הקרקע לכל פנס, באותה עוצמה', 'בכל פנס, באותה עוצמה', have, kit_pool, 'N')
    def _arrow_painters():   # 2.11 (p487): a function that delegates to cityArrow is not a painter of its own
        out = set()
        for m in re.finditer(r'function (\w*[Aa]rrow\w*)\(', GAME):
            body = GAME[m.end():m.end() + 900]
            own = body.split('\nfunction ')[0][:600]
            if m.group(1) == 'cityArrow' or ('cityArrow(' not in own and re.search(r'lineTo|fillRect|moveTo', own)): out.add(m.group(1))
        return out
    arrows = len(_arrow_painters()) if 'function cityArrow(' in GAME else len(set(re.findall(r'function (\w*[Aa]rrow\w*)\(', GAME)))
    row('העיר', 'C-13', 'צייר אחד לחצים', 'אחד', '%d ציירים שונים, ואף אחד לא על הכבישים' % arrows, arrows <= 1 and MARK_ARROWS, 'M')
    off = [r for r in DP.get('sizes', {}).get('table', []) if not r.get('ok')]
    row('העיר', 'C-27', 'טבלת הגדלים — כל הסוגים', '%d סוגים בגודל' % len(DP.get('sizes', {}).get('table', [])),
        '%d בגודל · %d עוד לא (קרונות הרכבת והשדה, בשלבים 8–9 ו-14–17)' % (len(DP['sizes']['table']) - len(off), len(off)), not off, 'N')

# ---------------------------------------------------------------- the seams
SEAMS = []
def pair_of(z1, z2):
    for p in PAIRS:
        if sorted(p) == sorted([z1, z2]): return p
    return None
def seam_add(pr, item, need, have, ok): SEAMS.append({'pair': '%s · %s' % tuple(pr), 'item': item, 'need': need, 'have': have, 'ok': bool(ok)})
def check_seams():
    tolA, tolR = GD['seams']['axis_tol_px'], GD['seams']['row_tol_px']; done = set()
    for C in CORR:
        k = KIT[C['cls']]; sp = k['lamp']['spacing_px']; nodes = corr_nodes(C); off = C['w'] / 2 + C['sw'] / 2
        for g in (1, -1):
            prev = None; c = C['c0']
            while c <= C['c1'] + 1e-6:
                x, y = (c, C['axis'] + g * off) if C['o'] == 'h' else (C['axis'] + g * off, c); z = zone_of(x, y)
                if prev and z != prev[0] and z and prev[0] and c <= C['c1'] - 10:
                    x2, y2 = (c + 10, C['axis'] + g * off) if C['o'] == 'h' else (C['axis'] + g * off, c + 10)
                    pr = pair_of(prev[0], z) if zone_of(x2, y2) == z and c - prev[1] >= 10 else None
                    if pr: seam_corr(C, g, c, pr, k, nodes)
                if prev is None or z != prev[0]: prev = (z, c)
                c += 2.0
    # a street that changes its type on a seam, or goes on beside itself (a jump in the axis)
    for C in CORR:
        for cend in (C['c0'], C['c1']):
            x, y = (cend, C['axis']) if C['o'] == 'h' else (C['axis'], cend)
            if not on_boundary(x, y): continue
            for D in CORR:
                if D is C or D['o'] != C['o']: continue
                for dend in (D['c0'], D['c1']):
                    if abs(dend - cend) > 3 or (dend == D['c0']) == (cend == C['c0']): continue
                    dd = abs(D['axis'] - C['axis'])
                    if dd > 60: continue
                    step = 6 if cend == C['c1'] else -6
                    pa = (cend - step, C['axis']) if C['o'] == 'h' else (C['axis'], cend - step); pb = (cend + step, D['axis']) if C['o'] == 'h' else (D['axis'], cend + step)
                    za, zb = zone_of(*pa), zone_of(*pb); pr = pair_of(za, zb) if za and zb else None
                    key = tuple(sorted([id(C), id(D)]))
                    if not pr or key in done: continue
                    done.add(key); nmC = C['edges'][0]['id']; nmD = D['edges'][0]['id']
                    if dd > tolA: seam_add(pr, '%s ↔ %s — קפיצה בציר' % (nmC, nmD), 'עד %d' % tolA, '%d' % dd, False)
                    if D['cls'] != C['cls']: seam_add(pr, '%s ↔ %s — סוג הדרך' % (nmC, nmD), 'אותו סוג משני הצדדים', '%s / %s' % (KIT[C['cls']]['he'], KIT[D['cls']]['he']), False)
def seam_corr(C, g, cs, pr, k, nodes):
    tag = '%s · %s' % (corr_label(C, cs - 60, cs + 60), gname(C, g)); sp = k['lamp']['spacing_px']; tolR = GD['seams']['row_tol_px']
    seam_add(pr, tag + ' — הכביש והמדרכה', 'אותו סוג, רוחב, ציר ומדרכה', '%s · רוחב %d · מדרכה %d — רחוב אחד, בלי קפיצה' % (k['he'], C['w'], C['sw']), True)
    bands = [(q['c'] - q['band'], q['c'] + q['band']) for q in nodes if g in q['sides']]
    def lat(q): return abs((q[4] if C['o'] == 'h' else q[3]) - C['axis'])
    for what, lim, ops, win in (('lamp', sp, [], sp * 1.5), ('tree', (k['trees']['spacing_px'] or [0, 0])[1], corr_openings(C, g), 200)):
        if what == 'tree' and not k['trees']['spacing_px']: continue
        Q = [q for q in corr_items(C, g, what) if cs - win <= q[0] <= cs + win]; a = [q for q in Q if q[0] < cs]; b = [q for q in Q if q[0] >= cs]
        he = 'שורת הפנסים' if what == 'lamp' else 'שורת העצים'
        if a and b:
            oa = sorted(lat(q) for q in a)[len(a) // 2]; ob = sorted(lat(q) for q in b)[len(b) // 2]
            gap = (b[0][0] - a[-1][0]) - overlap(a[-1][0], b[0][0], bands + ops)
            seam_add(pr, tag + ' — ' + he, 'אותו קו (עד %d) ופער עד %d' % (tolR, lim), 'הקו %d / %d · הפער %d' % (oa, ob, gap), abs(oa - ob) <= tolR and gap <= lim + .5)
        else:
            seam_add(pr, tag + ' — ' + he, 'השורה ממשיכה משני צדי התפר (עד %d)' % win, ('רק בצד אחד (%d / %d)' % (len(a), len(b))) if (a or b) else 'אין משני הצדדים', False)

# ---------------------------------------------------------------- run
for z in RUN:
    if z not in ZONES: print('אזור לא מוכר:', z, '(צריך ‎--rect ו-‎--district)'); sys.exit(2)
    check_streets(z); check_parking(z); check_doors(z); check_signs(z); check_marks(z); check_xw_place(z); check_stops(z); check_access(z); check_bounds(z); check_buildings(z); check_std(z)
check_city()
check_seams()
for s in SEAMS:
    s['key'] = 'תפר %s|C-28|%s' % (s['pair'], s['item']); ex = EXC.get(s['key']); s['reason'] = ex['reason'] if (ex and not s['ok']) else None
SUM = {}
for z in RUN + ['העיר']:
    R = [r for r in ROWS if r['zone'] == z and r['ok'] is not None]
    dev = [r for r in R if not r['ok']]
    SUM[z] = {'rows': len(R), 'ok': len(R) - len(dev), 'dev': len(dev), 'dev_reason': sum(1 for r in dev if r['reason']), 'by_check': {}}
    for r in dev: SUM[z]['by_check'][r['check']] = SUM[z]['by_check'].get(r['check'], 0) + 1
SP = {}
for s in SEAMS:
    q = SP.setdefault(s['pair'], {'rows': 0, 'dev': 0, 'dev_reason': 0}); q['rows'] += 1; q['dev'] += (not s['ok']); q['dev_reason'] += bool(s['reason'])
build = DP['meta'].get('build', '')
tagb = (re.search(r's7f\d+', build or '') or re.search('.*', 'run')).group(0)
out = A.json or (W + '/study/style/style_check_%s%s.json' % (tagb, ('_' + '_'.join(RUN)) if A.zone else ''))
json.dump({'build': build, 'guide': os.path.relpath(A.guide, W), 'dump': os.path.relpath(A.dump, W), 'zones': RUN, 'rows': ROWS, 'seams': SEAMS, 'summary': SUM, 'seam_summary': SP,
           'checks': sorted({r['check'] for r in ROWS} | ({'C-28'} if SEAMS else set()))}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

def cell(s, n): s = str(s); return s if len(s) <= n else s[:n - 1] + '…'
if not A.quiet:
    for z in RUN + ['העיר']:
        print('\n══ %s — %s' % (z, ZONES.get(z, {}).get('he', 'כל העיר')))
        print('כלל | נדרש | יש | תקין / חריגה | סיבה רשומה')
        for r in ROWS:
            if r['zone'] != z: continue
            st = 'מידע' if r['ok'] is None else ('תקין' if r['ok'] else 'חריגה')
            print('%s %s | %s | %s | %s | %s' % (r['check'], cell(r['item'], 70), cell(r['need'], 40), cell(r['have'], 70), st, (r['reason'] or ('—' if r['ok'] is not False else 'אין'))))
    print('\n══ התפרים')
    print('תפר | כלל | נדרש | יש | תקין / חריגה | סיבה רשומה')
    for s in SEAMS: print('%s | %s | %s | %s | %s | %s' % (s['pair'], cell(s['item'], 70), cell(s['need'], 40), cell(s['have'], 60), 'תקין' if s['ok'] else 'חריגה', s['reason'] or ('—' if s['ok'] else 'אין')))
print('\n══ סיכום')
for z in RUN + ['העיר']:
    q = SUM[z]; top = ', '.join('%s: %d' % kv for kv in sorted(q['by_check'].items(), key=lambda kv: -kv[1])[:5])
    print('%s: %d בדיקות · %d תקין · %d חריגות (%d עם סיבה רשומה) %s' % (z, q['rows'], q['ok'], q['dev'], q['dev_reason'], ('· ' + top) if top else ''))
for p, q in SP.items(): print('תפר %s: %d בדיקות · %d חריגות (%d עם סיבה רשומה)' % (p, q['rows'], q['dev'], q['dev_reason']))
print('הקובץ:', os.path.basename(out))
