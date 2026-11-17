# 30.10 · batch 7b: builds study/roads/city_plan.json from plan7b_net.py — segments, the checks, zones, blocks and
# the transition plan (temporary connections while a zone is still old). Terrain is read from today's data only.
import json, math, os, sys, collections, importlib.util
W = '/home/claude/work'
sys.path.insert(0, W + '/study/roads')
import plan7b_net as P
D = json.load(open(W + '/plan600/data/part_d_geo.json'))
GR = json.load(open(W + '/study/roads/game_roads.json'))
U = json.load(open(W + '/plan600/data/uses.json'))
COLS = [0, 1200, 2400, 3600, 4800, 6000, 7200, 8400, 9600]
ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]

# ---------------------------------------------------------------- terrain (w3Ring of the game, the lake, the island)
A6_COAST = [[0, 5000], [240, 4998], [450, 4994], [700, 4990], [1200, 4990]]
B6_COAST = [[1200, 4990], [1330, 5002], [1490, 5016], [1740, 5024], [1940, 5018], [2110, 4996], [2260, 5000], [2400, 5000]]
PORT_QY, CX, NY = 5200, 6230, 2550
W3_BEACH = [[6230, 2600], [6520, 2550], [6560, 3000], [6500, 3400], [6230, 3420]]
X0, Y0, X1, Y1 = -3000, -3850, 12600, 10750
SEA = [[X0, 5000], [0, 5000]] + A6_COAST[1:] + B6_COAST[1:] + [[2400, PORT_QY], [CX, PORT_QY]] + [p[:] for p in W3_BEACH[::-1]] + \
      [[CX, NY], [6560, NY], [6560, 2590], [6900, 2590], [6900, NY], [6560, NY], [6560, 1840], [7200, 1840], [7200, NY], [X1, NY], [X1, Y1], [X0, Y1]]
import plan7b_city as CITY
ISLAND = CITY.COAST   # 1.11: the island of D-259 — F9 + G9 + H9 (the coast of the plan's drawing)
ISL_WATER = CITY.WATER
# 31.10 (the owner 20:12; D-13 / GATE-100): the lake of B2 grows north into B1 — one continuous lake, not a second one. The south half of
# today's ellipse stays exactly as it is (the fishing pier, the two jetties, the cafe and the kiosk are on it); the shore goes on north
# through a wide neck into a basin in B1. A smooth closed curve (Catmull-Rom) through today's south half and the new north shore.
LAKE_TODAY = dict(cx=1840, cy=1000, rx=420, ry=110)
LAKE_NORTH = [(1428, 958), (1452, 902), (1468, 838), (1460, 770), (1440, 702), (1422, 628), (1420, 552), (1440, 482), (1486, 420), (1556, 376), (1642, 350),
              (1742, 340), (1842, 346), (1936, 368), (2014, 408), (2066, 466), (2082, 532), (2066, 596), (2030, 648), (1994, 698), (1976, 758), (1990, 822),
              (2040, 872), (2110, 903), (2188, 933), (2238, 965)]
def lake_poly():
    T = LAKE_TODAY; south = [(T['cx'] + T['rx'] * math.cos(t * math.pi / 24), T['cy'] + T['ry'] * math.sin(t * math.pi / 24)) for t in range(25)]
    ctrl = south + LAKE_NORTH; n = len(ctrl); out = []
    for i in range(n):
        p0, p1, p2, p3 = ctrl[i - 1], ctrl[i], ctrl[(i + 1) % n], ctrl[(i + 2) % n]; steps = 1 if i < len(south) - 1 else 6
        for k in range(steps):
            t = k / steps; t2, t3 = t * t, t * t * t
            out.append([round(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3), 1) for j in (0, 1)])
    return out
# today, on the shore (the game, read only): the fishing pier, the two jetties (their land end), the lake cafe and the kiosk
LAKE_KEEP = [dict(id='B2-PIER', label='מזח הדיג', x=1458, y=1037, kind='water'), dict(id='B2-JETTY-W', label='רציף הדיג המערבי', x=1402, y=1000, kind='shore'),
             dict(id='B2-JETTY-E', label='רציף הדיג המזרחי', x=2278, y=1000, kind='shore'), dict(id='B2-CAFE', label='בית קפה האגם', x=2210, y=1182, kind='land'),
             dict(id='B2-KIOSK', label='קיוסק האגם (מתאחד עם בית הקפה)', x=2231.5, y=1318.2, kind='land')]
LAKE = dict(id='B2-LAKE', label='האגם — B2 מורחב אל B1', today=LAKE_TODAY, pts=lake_poly(), keep=LAKE_KEEP)
AIRPORT = [(4800, -850, 9600, 1700), (7200, 1700, 9600, 2550)]
def arc(cx, cy, r, a0, a1, n=24): return [[cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)] for i in range(n + 1)]
RAIL = {
    'MAIN-A': [[5800, 900], [5800, 4720]] + arc(5400, 4720, 400, 0, math.pi / 2)[1:] + [[2560, 5120]],
    'MAIN-B': [[5900, 900], [5900, 4720]] + arc(6300, 4720, 400, math.pi, math.pi / 2)[1:],
    'EAST': [[5400, 5120], [7250, 5120]],
    'ISLAND-DIAG': [p for p in D['TRACK_A']] + [[8432.6, 6923.1], [9273.1, 7518.5]],
    'SPUR': [[5746, 4120], [5746, 4700]],
    'REF-SPUR': [[2780, 5120], [2780, 3950]],   # 1.11: the refinery spur (D-177), future — stage 14
}
BRIDGE = [p for p in D['ROAD'] if p[1] >= 5200]
# 31.10 (the owner 20:23): the airport on the map as it is today — frozen until stage 8 of the master plan (R-32). Read only from the
# game's code (out/Turbo_City_v1_96_GATE77_S7F175.html: APT_RWY, APT_TWY, APT_LINKS, G73_CONNECTORS, APT_Y.L*, APT_APRON, APT_CARGO_APRON,
# G73_*_EXT, APT_HARD, APT_STANDS, APT_HELIPADS, the d2Place of the terminal wings, the tower and the cargo terminal, G73_EM, the fences).
# The terminal wings are placed by their centre and front line; their size here is approximate (≈ 34 × 17 m each).
AIRPORT_TODAY = dict(
    source='Turbo_City_v1_96_GATE77_S7F175 (קריאה בלבד)',
    boundary=[[4800, -850], [9600, -850], [9600, 2550], [7200, 2550], [7200, 1700], [4800, 1700]],
    paved=[dict(id='RWY', he='המסלול (330 × 24 מ׳)', kind='runway', r=[4950, -550, 8250, -310]),
           dict(id='TWY', he='מסלול ההסעה המקביל', kind='taxi', r=[4900, -128, 8030, -8])] +
          [dict(id=f'LINK-{k}', he=f'מסלול חיבור {k}', kind='taxi', r=[x - 55, -310, x + 55, -128]) for k, x in (('A1', 5250), ('A2', 6600), ('A3', 7950))] +
          [dict(id=f'CONN-{k}', he=f'חיבור לרחבה {k}', kind='taxi', r=[x - w / 2, -8, x + w / 2, 234]) for k, x, w in (('B1', 5990, 80), ('A2S', 6600, 110), ('B2', 7276, 80), ('A3S', 7950, 110))] +
          [dict(id='TL-L', he='מסלול הסעה L', kind='taxi', r=[5950, 234, 8345, 314]),
           dict(id='APRON-EXT', he='הרחבת רחבת הנוסעים', kind='apron', r=[5990, 314, 7300, 394]),
           dict(id='APRON', he='רחבת המטוסים — הנוסעים', kind='apron', r=[6020, 394, 7236, 772]),
           dict(id='APRON-CARGO', he='רחבת המטען', kind='apron', r=[5400, 394, 6020, 845]),
           dict(id='APRON-E', he='הרחבה המזרחית (מסוקים)', kind='apron', r=[7300, 314, 8345, 600]),
           dict(id='APRON-W', he='הרחבה המערבית', kind='apron', r=[4805, -8, 5950, 604]),
           dict(id='GA-LINK', he='חיבור לרחבת התעופה הכללית', kind='taxi', r=[7236, 314, 7316, 1000]),
           dict(id='GA', he='רחבת התעופה הכללית (GA)', kind='apron', r=[7236, 1000, 8330, 1135]),
           dict(id='EM', he='מתחם החירום — כיבוי והצלה, רפואה ומשטרה', kind='apron', r=[8072, -108, 8344, 206])],
    buildings=[dict(id='T1', he='טרמינל — אגף א׳', r=[6050, 774, 6390, 944]), dict(id='T2', he='טרמינל — אגף ב׳', r=[6410, 774, 6750, 944]),
               dict(id='T3', he='טרמינל — אגף ג׳', r=[6770, 774, 7105, 944]), dict(id='TWR', he='מגדל הפיקוח', r=[7101, 900, 7141, 944]),
               dict(id='CARGO', he='מסוף המטען האווירי', r=[5415, 850, 5715, 944]), dict(id='ARFF', he='תחנת כיבוי והצלה', r=[8091, -100, 8200, -22]),
               dict(id='EMS', he='מוקד רפואה ומשטרת השדה', r=[8240, -100, 8334, -28])],
    stands=[dict(id=k, x=x, y=660) for k, x in (('P1', 6096), ('P2', 6430), ('P3', 6732), ('P4', 7055))],
    helipads=[dict(id='H1', x=8128, y=690, r=56), dict(id='H2', x=8280, y=690, r=56), dict(id='O1', x=8270, y=543, r=50)],
    fences=[[[4805, -760], [8398, -760]], [[8398, -760], [8398, 850]], [[4805, -760], [4805, -622]], [[4805, -242], [4805, 604]],
            [[5400, 944], [5684, 944]], [[5744, 944], [5752, 944]], [[5948, 944], [6070, 944]], [[7144, 944], [7144, 1018]], [[7144, 1018], [7233, 1018]],
            [[7233, 1018], [7233, 1180]], [[7233, 1180], [7869, 1180]], [[7869, 1180], [7869, 1700]], [[7869, 1700], [8400, 1700]], [[4805, 604], [4805, 860]],
            [[4805, 725], [4870, 725]], [[4970, 725], [5400, 725]], [[5400, 725], [5400, 944]]],
    gates=[dict(id='AP1', he='שער הנוסעים (D2E-AIR)'), dict(id='AP2', he='שער המטען והשירות (D2E)'), dict(id='AP3', he='שער הדרום (AIR-S)')],
)
_ONs = {n_['id']: n_ for n_ in GR['nodes']}
AIRPORT_TODAY['roads'] = [dict(id=e_['id'], name=e_.get('name', ''), a=[_ONs[e_['a']]['x'], _ONs[e_['a']]['y']], b=[_ONs[e_['b']]['x'], _ONs[e_['b']]['y']], width=e_.get('width') or 96, sidewalk=e_.get('sidewalk') or 0)
                          for e_ in GR['edges'] if (lambda p_, q_: (p_['x'] >= 4799 and p_['y'] <= 1701) or (p_['x'] >= 7199 and p_['y'] <= 2551))(_ONs[e_['a']], _ONs[e_['a']])
                          and (lambda p_: (p_['x'] >= 4799 and p_['y'] <= 1701) or (p_['x'] >= 7199 and p_['y'] <= 2551))(_ONs[e_['b']])]   # the fixed island bridge (part D) from the quay line to the island

def pip(x, y, poly):
    c = False; j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: c = not c
        j = i
    return c
def is_sea(x, y): return pip(x, y, SEA) and (not pip(x, y, ISLAND) or any(pip(x, y, w_) for w_ in ISL_WATER))
def in_lake(x, y): return pip(x, y, LAKE['pts'])
def shore_d(x, y):   # the distance to the shore line
    P_ = LAKE['pts']; best = 1e9
    for i in range(len(P_)):
        (ax, ay), (bx, by) = P_[i - 1], P_[i]; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
        t = 0 if L2 == 0 else max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / L2)); best = min(best, math.hypot(x - ax - t * dx, y - ay - t * dy))
    return best
def lake_d(x, y): return 0 if in_lake(x, y) else shore_d(x, y)
def in_air(x, y):return any(a <= x < c and b <= y < d for a, b, c, d in AIRPORT)
def zone_of(x, y):
    i = next((k for k in range(8) if COLS[k] <= x < COLS[k + 1]), None); j = next((k for k in range(10) if ROWS[k] <= y < ROWS[k + 1]), None)
    return None if i is None or j is None else 'ABCDEFGH'[i] + str(j)
def zrect(z): i = 'ABCDEFGH'.index(z[0]); j = int(z[1:]); return (COLS[i], ROWS[j], COLS[i + 1], ROWS[j + 1])
def dseg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    qx, qy = ax + t * dx, ay + t * dy; return math.hypot(px - qx, py - qy), qx, qy, t
def seg_x(p1, p2, p3, p4):   # proper intersection point of two segments, or None
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9: return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den; u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1)) if 0 <= t <= 1 and 0 <= u <= 1 else None

N, Rd, CLS = P.N, P.R, P.CLS
# ---------------------------------------------------------------- segments
SEG = []
for rd in Rd:
    for i in range(len(rd['nodes']) - 1):
        a, b = N[rd['nodes'][i]], N[rd['nodes'][i + 1]]
        pts = [[a['x'], a['y']], [b['x'], b['y']]]
        if rd['kind'] == 'bridge': pts = [[a['x'], a['y']]] + [p for p in BRIDGE if p[1] > 5200 + 1] + [[b['x'], b['y']]]
        elif rd.get('shape') and i in rd['shape']: pts = [[a['x'], a['y']]] + [list(q) for q in rd['shape'][i]] + [[b['x'], b['y']]]   # a road that follows the ground (the island)
        L = sum(math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]) for k in range(len(pts) - 1))
        SEG.append(dict(id=f"{rd['id']}/{i + 1}", road=rd['id'], a=a['id'], b=b['id'], cls=rd['cls'], lanes=rd['lanes'], kind=rd['kind'],
                        len_m=round(L / 10, 1), pts=[[round(p[0], 1), round(p[1], 1)] for p in pts], truck=rd['truck']))
# zones each segment touches (rect grown by the road's half width + 120 px, so a road on a seam belongs to both sides)
def seg_zones(s, grow):
    out = set(); pts = s['pts']
    for k in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]; L = math.hypot(bx - ax, by - ay); m = max(1, int(L // 50))
        for t in range(m + 1):
            x, y = ax + (bx - ax) * t / m, ay + (by - ay) * t / m
            for z in {zone_of(x + dx, y + dy) for dx in (-grow, 0, grow) for dy in (-grow, 0, grow)}:
                if z: out.add(z)
    return out
for s in SEG:
    s['zones'] = sorted(seg_zones(s, CLS[s['cls']]['halfW'] + 120))
    mx = (s['pts'][0][0] + s['pts'][-1][0]) / 2; my = (s['pts'][0][1] + s['pts'][-1][1]) / 2
    s['home'] = zone_of(mx, my)

# ---------------------------------------------------------------- graph and junctions
ADJ = collections.defaultdict(list)
for s in SEG:
    ADJ[s['a']].append((s['b'], s)); ADJ[s['b']].append((s['a'], s))
for k, v in N.items(): v['deg'] = len(ADJ[k]); v['zone'] = zone_of(v['x'], v['y'])
JUNC = {k for k, v in N.items() if v['deg'] >= 3 or v['kind'] in ('signal', 'roundabout', 'riro', 'stop')}
# the airport gates are where a frozen airport road meets ours: they count as an arm of the junction they sit on
checks = []
def chk(name, ok, det): checks.append(dict(name=name, ok=bool(ok), det=det))

# R-15: >= 60 m between junctions along every road; arterials: >= 90 m between signals
viol = []; mins = {}
for rd in Rd:
    js = [x for x in rd['nodes'] if x in JUNC]
    # distance along the road
    pos = {}; acc = 0
    for i, x in enumerate(rd['nodes']):
        if i: a, b = N[rd['nodes'][i - 1]], N[x]; acc += math.hypot(b['x'] - a['x'], b['y'] - a['y'])
        pos[x] = acc
    for a, b in zip(js, js[1:]):
        d = pos[b] - pos[a]; mins[rd['cls']] = min(mins.get(rd['cls'], 1e9), d)
        if d < 600: viol.append(f"{rd['id']}: {a}–{b} {d / 10:.0f} מ׳")
    if rd['cls'] == 'arterial':
        sg = [x for x in rd['nodes'] if N[x]['kind'] == 'signal']
        for a, b in zip(sg, sg[1:]):
            if pos[b] - pos[a] < 750: viol.append(f"{rd['id']}: רמזורים {a}–{b} {(pos[b] - pos[a]) / 10:.0f} מ׳ (< 75)")
chk('R-15 — לפחות 60 מ׳ בין צמתים לאורך כל דרך; בעורקים לפחות 75 מ׳ בין רמזורים', not viol,
    ('בלי חריגות. ' if not viol else '; '.join(viol) + '. ') + 'המרחק הקטן ביותר: ' + ', '.join(f"{CLS[c]['he']} {v / 10:.0f} מ׳" for c, v in sorted(mins.items())))

# angles: every junction's arms within 15° of a right angle (except the island roundabout, where the bridge lands diagonally)
bad = []
for k in JUNC:
    if N[k]['kind'] == 'roundabout' and k == 'IL': continue
    arms = []
    for o, s in ADJ[k]:
        p = s['pts']; q = p[1] if s['a'] == k else p[-2]; arms.append(math.degrees(math.atan2(q[1] - N[k]['y'], q[0] - N[k]['x'])))
    for i in range(len(arms)):
        for j in range(i + 1, len(arms)):
            d = abs((arms[i] - arms[j] + 180) % 360 - 180); dev = min(abs(d - 90), abs(d - 180))
            if dev > 15: bad.append(f'{k} ({d:.0f}°)')
chk('זוויות — כל הזרועות בצומת קרובות ל-90° (עד 15°)', not bad, 'כל הצמתים בזווית ישרה; כיכר האי (IL) מסדרת את הנחיתה האלכסונית של הגשר.' if not bad else ', '.join(bad))

# no short segments, no duplicates (two segments parallel within 150 px over more than 30 m)
short = [s['id'] for s in SEG if s['len_m'] < 6 and N[s['b']]['kind'] != 'gate']
dups = []
for i, s in enumerate(SEG):
    for t in SEG[i + 1:]:
        if s['kind'] == 'bridge' or t['kind'] == 'bridge': continue
        (a1, b1), (a2, b2) = s['pts'][0], s['pts'][-1]; (c1, d1), (c2, d2) = t['pts'][0], t['pts'][-1]
        if a1 == a2 and c1 == c2 and abs(a1 - c1) < 150:     # both vertical
            ov = min(max(b1, b2), max(d1, d2)) - max(min(b1, b2), min(d1, d2))
            if ov > 300 and abs(a1 - c1) > 0: dups.append(f"{s['id']}~{t['id']}")
        if b1 == b2 and d1 == d2 and abs(b1 - d1) < 150:
            ov = min(max(a1, a2), max(c1, c2)) - max(min(a1, a2), min(c1, c2))
            if ov > 300 and abs(b1 - d1) > 0: dups.append(f"{s['id']}~{t['id']}")
chk('אין קטעים קצרים או כפולים', not short and not dups,
    f"הקטע הקצר ביותר {min(s['len_m'] for s in SEG if N[s['b']]['kind'] != 'gate'):.0f} מ׳ (פינה בדרך האי; בלי הזנבות אל שערי השדה); אין שני קטעים מקבילים קרובים מ-15 מ׳." if not short and not dups else f'{short} {dups}')

# terrain: no road over the sea (except the bridge), none in the lake and none closer than 10 m to its shore (edge of the road), none inside the airport (only to its gates)
sea_hits, lake_hits, air_hits = [], [], []
for s in SEG:
    pts = s['pts']; hw = CLS[s['cls']]['halfW']
    for k in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]; L = math.hypot(bx - ax, by - ay); m = max(1, int(L // 40))
        for t in range(1, m):
            x, y = ax + (bx - ax) * t / m, ay + (by - ay) * t / m
            if s['kind'] != 'bridge' and is_sea(x, y): sea_hits.append(s['id']); break
            if lake_d(x, y) < hw + 100: lake_hits.append(s['id']); break
            if in_air(x - 1 if x >= 4800 and N[s['b']]['kind'] == 'gate' else x, y) and N[s['a']]['kind'] != 'gate' and N[s['b']]['kind'] != 'gate': air_hits.append(s['id']); break
# the lake clearances: from the edge of every road near the lake to its shore (the segment ends too)
gaps = {}
for s in SEG:
    pts = s['pts']; hw = CLS[s['cls']]['halfW']
    for k in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]; L = math.hypot(bx - ax, by - ay); m = max(1, int(L // 20))
        for t in range(m + 1):
            x, y = ax + (bx - ax) * t / m, ay + (by - ay) * t / m
            if abs(x - 1840) > 1400 or abs(y - 720) > 1100: continue
            g_ = lake_d(x, y) - hw
            if s['road'] not in gaps or g_ < gaps[s['road']]: gaps[s['road']] = g_
            if g_ < 100 and s['id'] not in lake_hits: lake_hits.append(s['id'])
near_l = sorted(((g_, r_) for r_, g_ in gaps.items() if g_ < 600))
RDNM = {r_['id']: r_['name'] for r_ in Rd}; RDN_ = None
chk('השטח — שום כביש לא על הים (חוץ מהגשר), לא באגם ולא קרוב מ-10 מ׳ לחוף שלו, ולא בתוך השדה', not sea_hits and not lake_hits and not air_hits,
    "המרחק משפת הכביש לחוף האגם: " + ', '.join(f"{RDNM[r_]} {g_ / 10:.1f} מ׳" for g_, r_ in near_l) + "; לשדה נכנסים רק שלושת השערים הקיימים (AP1–AP3)." +
    (f' ים: {sea_hits}' if sea_hits else '') + (f' אגם: {lake_hits}' if lake_hits else '') + (f' שדה: {air_hits}' if air_hits else ''))

LP = LAKE['pts']
def area(p): return abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1] for i in range(len(p)))) / 2
def clip_y(p, ymax):   # the part of a polygon north of ymax
    out = []
    for i in range(len(p)):
        a_, b_ = p[i - 1], p[i]; ina, inb = a_[1] < ymax, b_[1] < ymax
        if ina != inb: t = (ymax - a_[1]) / (b_[1] - a_[1]); out.append((a_[0] + t * (b_[0] - a_[0]), ymax))
        if inb: out.append(b_)
    return out
selfx = sum(1 for i in range(len(LP)) for j in range(i + 2, len(LP)) if not (i == 0 and j == len(LP) - 1) and seg_x(LP[i], LP[(i + 1) % len(LP)], LP[j], LP[(j + 1) % len(LP)]))
def cross_xs(yy): return sorted(LP[i - 1][0] + (yy - LP[i - 1][1]) / (LP[i][1] - LP[i - 1][1]) * (LP[i][0] - LP[i - 1][0]) for i in range(len(LP)) if (LP[i - 1][1] - yy) * (LP[i][1] - yy) < 0)
neck = cross_xs(850); neck_m = (neck[-1] - neck[0]) / 10 if len(neck) == 2 else 0
T0 = LAKE_TODAY; dev = max(abs(((x - T0['cx']) / T0['rx']) ** 2 + ((y - T0['cy']) / T0['ry']) ** 2 - 1) for x, y in LP if y >= T0['cy'] + 1)
LAKE['area_m2'] = round(area(LP) / 100); LAKE['b1_m2'] = round(area(clip_y(LP, 850)) / 100); LAKE['today_m2'] = round(math.pi * T0['rx'] * T0['ry'] / 100); LAKE['neck_m'] = round(neck_m, 1)
keep_bad = []
for k_ in LAKE_KEEP:
    w_, d_ = in_lake(k_['x'], k_['y']), shore_d(k_['x'], k_['y']); k_['shore_m'] = round(d_ / 10, 1)
    if (k_['kind'] == 'water' and not w_) or (k_['kind'] == 'shore' and (w_ or d_ > 25)) or (k_['kind'] == 'land' and (w_ or d_ < 30)): keep_bad.append(k_['id'])
chk('האגם — אגם אחד רציף מ-B2 אל B1 (D‑13, GATE‑100); החצי הדרומי כמו היום, והדיג, המזחים, בית הקפה והקיוסק נשארים על החוף',
    not selfx and len(neck) == 2 and neck_m >= 30 and dev < 0.02 and not keep_bad,
    f"קו חוף אחד בלי חיתוכים; ב-y 850 (הגבול B1/B2) האגם רוחבו {neck_m:.0f} מ׳ — אין תפר. השטח {LAKE['area_m2']:,} מ״ר (היום {LAKE['today_m2']:,}), מהם {LAKE['b1_m2']:,} ב-B1; "
    f"הקצה הצפוני ב-y {min(y for x, y in LP):.0f}. החצי הדרומי זהה לאליפסה של היום. " + '; '.join(f"{k_['label']} — {'במים' if k_['kind'] == 'water' else ('על קו החוף' if k_['kind'] == 'shore' else 'על היבשה')}, {k_['shore_m']} מ׳ מהחוף" for k_ in LAKE_KEEP) + '.' +
    (f" לא במקום: {keep_bad}" if keep_bad else ''))

# R-16: every signal has a left lane and an arrow on each approach
SIG = []
for k, v in sorted(N.items()):
    if v['kind'] != 'signal': continue
    appr = []
    for o, s in ADJ[k]:
        cl = s['cls']; ext = N[o]['kind'] == 'gate'
        appr.append(dict(from_=o, road=s['road'], cls=cl, through={'main': 3, 'arterial': 2}.get(cl, 1), left=0 if ext else 1, arrow=not ext))
    four = len(appr) >= 4
    SIG.append(dict(node=k, label=v['label'], approaches=[{('from' if kk == 'from_' else kk): vv for kk, vv in a.items()} for a in appr],
                    phases=(['צפון-דרום חץ שמאלה', 'צפון-דרום ישר וימינה', 'מזרח-מערב חץ שמאלה', 'מזרח-מערב ישר וימינה'] if four else
                            ['הראשית חץ שמאלה + ישר', 'הראשית ישר', 'המשנית']), preempt=True, why=v['why']))
r16 = [s['node'] for s in SIG if any(a['left'] == 0 and N[a['from']]['kind'] != 'gate' for a in s['approaches'])]
chk('R-16 — בכל רמזור נתיב שמאלה וחץ בכל גישה', not r16, f"{len(SIG)} רמזורים, כולם עם נתיב שמאלה וחץ (חוץ מהגישה מתוך השדה ב-J46_16, שהיא של השדה)." if not r16 else str(r16))

# connectivity and the must-reach places
seen = {'J54_26'}; st = ['J54_26']
while st:
    x = st.pop()
    for o, s in ADJ[x]:
        if o not in seen: seen.add(o); st.append(o)
lost = sorted(set(N) - seen)
chk('כל הרשת מחוברת — מכל צומת אפשר להגיע למסוף E3', not lost, f'{len(N)} צמתים, {len(SEG)} קטעים, כולם מחוברים.' if not lost else str(lost))
# routes follow the segments
badr = []
for kind, L in P.ROUTES.items():
    for rt in L:
        for a, b in zip(rt['path'], rt['path'][1:]):
            if not any(o == b for o, s in ADJ[a]): badr.append(f"{rt['id']}: {a}→{b}")
        if kind == 'truck':
            for a, b in zip(rt['path'], rt['path'][1:]):
                s = next((s for o, s in ADJ[a] if o == b), None)
                if s and not s['truck']: badr.append(f"{rt['id']}: {s['id']} סגור למשאיות")
chk('הקווים (אוטובוס, משאיות, חירום) עוברים רק על קטעים קיימים, והמשאיות רק על דרכים פתוחות להן', not badr,
    f"{sum(len(v) for v in P.ROUTES.values())} קווים." if not badr else '; '.join(badr))

# ---------------------------------------------------------------- blocks and the uses of data/uses.json
FOOT = {   # m × m (+ m² of parking/yard) from the 'size' lines of uses.json; the rest is measured in its own stage
    'hospital': (60, 30, 1700), 'school': (52, 20, 600), 'supermarket': (38, 20, 400), 'fire': (30, 20, 300), 'police': (30, 20, 400),
    'hotel': (40, 18, 500), 'apartment': (35, 14, 300), 'house': (15, 20, 0), 'villa': (24.5, 21.5, 0), 'fuel': (35, 25, 0),
}
ZT = collections.defaultdict(collections.Counter)
for t in U['types']:
    tg = [a for a in t.get('target', []) if isinstance(a, dict) and a.get('zone')]
    for a in tg: ZT[a['zone']][t['type']] += 1
# blocks: the land between the roads (rectangles; half the width of each bounding road is taken off)
def B(id, x0, y0, x1, y1, roads, zones, note=''): return dict(id=id, rect=[x0, y0, x1, y1], roads=roads, zones=zones, note=note)
BLK = [
    B('BK-A2', 0, 760, 1200, 1600, ['LC-A1', 'CL-W'], ['A2'], 'בית החולים; קו מגרש (לא כביש) מול A3'),
    B('BK-A34', 0, 1600, 1200, 3400, ['CL-W', 'LC-A5'], ['A3', 'A4'], 'קריית הספורט, הכבאות וה-EMS — שער בכיכר הספורט'),
    B('BK-A5E', 600, 3400, 1200, 4250, ['CL-W', 'LC-A5', 'LC-SQ'], ['A5']), B('BK-A5W', 0, 3400, 600, 4250, ['LC-A5'], ['A5']),
    B('BK-A6', 0, 4250, 1200, 4990, ['LC-A6', 'LC-SQ', 'CL-W'], ['A6'], 'החווה; המעבורת דרומית לדרך החווה'),
    B('BK-B3W', 1200, 1600, 1800, 2550, ['AR-NW', 'CL-W', 'LC-SCH', 'LC-B'], ['B3']), B('BK-B3E', 1800, 1600, 2510, 2550, ['AR-NW', 'AR-C', 'LC-B'], ['B3'], 'קו מגרש מול B4'),
    B('BK-B4W', 1200, 2550, 1800, 3400, ['LC-SCH', 'CL-W', 'LC-B'], ['B4'], 'קו מגרש מול B5'), B('BK-B4E', 1800, 2550, 2510, 3400, ['LC-B', 'AR-C'], ['B4'], 'קו מגרש מול B3 ו-B5'),
    B('BK-B5', 1200, 3400, 2510, 4250, ['CL-W', 'AR-C', 'CL-SW'], ['B5'], 'רובע העירייה והאקדמיה — קמפוס סביב רחבה, בלי כביש פנימי'),
    B('BK-B6', 1200, 4250, 2510, 4990, ['CL-SW', 'CL-W', 'LC-B6'], ['B6'], 'החוף'),
    B('BK-C2', 2510, 760, 3710, 1600, ['LC-N', 'AR-C', 'AR-N', 'CL-MALL'], ['C2'], 'הקניון במרכז, החניונים משני צדדיו, שורת החנויות על שדרת השדה'),
    B('BK-D2', 3710, 760, 4600, 1600, ['LC-N', 'CL-MALL', 'AR-N', 'CL-AC'], ['D2']),
    B('BK-C3', 2510, 1600, 3600, 2550, ['AR-N', 'AR-C', 'LC-C3'], ['C3'], 'הווילות סביב רחוב ללא מוצא; קו מגרש מול C4'),
    B('BK-D3', 3600, 1600, 4600, 2550, ['AR-N', 'AR-E', 'LC-D3'], ['D3'], 'שירותי הרכב על העורקים, הווילות על רחוב המוסכים'),
    B('BK-C4', 2510, 2550, 3600, 3400, ['AR-C', 'CL-T', 'LC-C4'], ['C4'], 'המפעל, המחסן ותחנת הכיבוי השנייה'),
    B('BK-D4', 3600, 2550, 4600, 3400, ['AR-E', 'CL-T', 'LC-D4', 'LC-D3'], ['D4']),
    B('BK-C5W', 2510, 3400, 3110, 4250, ['CL-T', 'AR-C', 'AR-S', 'LC-C5'], ['C5'], 'בית הזיקוק (הבלוק הצפוני-מערבי)'),
    B('BK-C5E', 3110, 3400, 3850, 4250, ['CL-T', 'CL-PG', 'AR-S', 'LC-C5'], ['C5']), B('BK-D5', 3850, 3400, 4600, 4250, ['CL-T', 'CL-PG', 'AR-S', 'AR-E'], ['D5']),
    B('BK-E3', 4600, 1600, 5774, 2550, ['AR-N', 'AR-E', 'CL-I', 'LC-E3'], ['E3']), B('BK-E4', 4600, 2620, 5774, 3400, ['CL-I', 'AR-E', 'LC-E3'], ['E4']),
    B('BK-E5', 4600, 3400, 5746, 4250, ['AR-E', 'AR-S'], ['E5'], 'חצר הרכבת — השער בזרוע המזרחית של J46_34'),
    B('BK-C6', 2510, 4250, 3850, 4900, ['AR-S', 'PT-W', 'PT-M', 'PT-Q', 'PT-Y1'], ['C6']), B('BK-D6', 3850, 4250, 4600, 4900, ['AR-S', 'PT-M', 'PT-E', 'PT-Q'], ['D6']),
    B('BK-E6', 4600, 4250, 5600, 4900, ['AR-S', 'PT-E', 'PT-Q'], ['E6']), B('BK-QY', 2510, 4900, 6000, 5200, ['PT-Q'], ['C6', 'D6', 'E6'], 'הסינר, המסילה ב-y 5120 וקיר הרציף'),
    B('BK-C1', 2510, 0, 3710, 760, ['LC-N', 'LC-C1'], ['C1'], 'הכפר'), B('BK-D1', 3710, 0, 4800, 760, ['LC-N', 'LC-D1'], ['D1'], 'החממות'),
    B('BK-B12', 1200, 0, 2510, 1600, ['CL-W', 'AR-NW', 'AR-C', 'LC-B1'], ['B1', 'B2'], 'הפארק והאגם של B1 ו-B2 — אגם אחד, בלי כביש בתוכם; דרך הפארק נכנסת מכיכר הכפר עד החניון'),
    B('BK-F3', 5926, 1760, 6560, 2550, ['CL-F', 'CL-I'], ['F3'], 'המרינה: החניון (y 1830–2000), המועדון והטיילת'),
]
def half(rid):
    rd = next((x for x in Rd if x['id'] == rid), None); return CLS[rd['cls']]['halfW'] if rd else 0
def side_cut(b, side):
    x0, y0, x1, y1 = b['rect']; best = 0
    for s in SEG:
        if s['road'] not in b['roads']: continue
        p = s['pts']
        for k in range(len(p) - 1):
            (ax, ay), (bx, by) = p[k], p[k + 1]
            if side in 'WE' and abs(ax - bx) < 1:
                lx = x0 if side == 'W' else x1
                if abs(ax - lx) < 150 and min(max(ay, by), y1) - max(min(ay, by), y0) > 100: best = max(best, CLS[s['cls']]['halfW'] - abs(ax - lx) * (1 if (ax > lx) == (side == 'W') else -1))
            if side in 'NS' and abs(ay - by) < 1:
                ly = y0 if side == 'N' else y1
                if abs(ay - ly) < 150 and min(max(ax, bx), x1) - max(min(ax, bx), x0) > 100: best = max(best, CLS[s['cls']]['halfW'] - abs(ay - ly) * (1 if (ay > ly) == (side == 'N') else -1))
    return max(0, best)
for b in BLK:
    x0, y0, x1, y1 = b['rect']; c = {k: side_cut(b, k) for k in 'WENS'}
    nw, nh = (x1 - x0 - c['W'] - c['E']) / 10, (y1 - y0 - c['N'] - c['S']) / 10
    b['net_m'] = [round(nw, 1), round(nh, 1)]; b['net_m2'] = round(nw * nh)
fits = []; misfit = []
for z in sorted(ZT):
    bl = [b for b in BLK if z in b['zones']]
    if not bl: continue
    need = 0; big = []; unk = []
    for t, c in ZT[z].items():
        n_ = c
        if t == 'house': n_ = 6 if z == 'C1' else (4 if z == 'B3' else c)
        if t == 'villa': n_ = {'C3': 8, 'D3': 3, 'C2': 2}.get(z, c)
        if t == 'apartment': n_ = {'B3': 1, 'B4': 4}.get(z, c)
        if t in FOOT:
            fw, fh, ex = FOOT[t]; need += n_ * (fw * fh + ex)
            if not any(max(b['net_m']) >= max(fw, fh) and min(b['net_m']) >= min(fw, fh) for b in bl): big.append(t)
        else: unk.append(t)
    area = sum(b['net_m2'] for b in bl) / max(1, sum(len(b['zones']) for b in bl) / len(bl))
    ok = need <= .85 * area and not big
    fits.append(dict(zone=z, blocks=[b['id'] for b in bl], area_m2=round(area), need_m2=round(need), share=round(need / area, 2) if area else None,
                     measured_in_stage=sorted(unk), ok=ok, notfit=big))
    if not ok: misfit.append(z)
dense = [f"{f['zone']} {round(f['share'] * 100)}%" for f in fits if f['share'] and f['share'] > .6]
chk('הבלוקים — השימושים עם מידה בטבלת השימושים נכנסים (מבנים + חניה עד 85% מהשטח הנטו, והמבנה הגדול נכנס במידות הבלוק)', not misfit,
    ('כל האזורים עם מידות נכנסים' if not misfit else f'לא נכנסים: {misfit}') + (f"; צפופים (מעל 60%): {', '.join(dense)}" if dense else '') +
    '; השאר (בלי מידה בטבלת השימושים) נמדדים בשלב שלהם.')

# ---------------------------------------------------------------- the transition: zone by zone, with temporary links to the old roads
ORDER = [
    ('S1', ['B4'], 'B4 — הפיילוט (החלטת הבעלים 12:07)'), ('S2', ['B3'], 'השכונה הצפונית — משלימה את רחוב השכונה'),
    ('S3', ['A3', 'A4'], 'קריית הספורט והכבאות — שדרת המערב'), ('S4', ['C3', 'D3'], 'הווילות ושירותי הרכב'),
    ('S5', ['C4', 'D4'], 'התעשייה'), ('S6', ['C5', 'D5'], 'בית הזיקוק ושער הנמל'), ('S7', ['A5', 'B5'], 'הדאונטאון ורובע העירייה'),
    ('S8', ['A2', 'B2', 'C2', 'D2'], 'בית החולים, הפארק, המרכז והעסקים — שדרת השדה'),
    ('S9', ['E3', 'E4', 'E5', 'F3', 'F4', 'F5', 'F6'], 'התחנה, הרכבת, המעבר מתחת לרכבת וכביש החוף עד הגשר'),
    ('S10', ['C6', 'D6', 'E6'], 'הנמל'), ('S11', ['A6', 'B6'], 'החווה, המעבורת והחוף'),
    ('S12', ['A0', 'B0', 'C0', 'D0', 'A1', 'B1', 'C1', 'D1'], 'הצפון: הכפר, הפארק, השדות והרכס'),
    ('S13', ['G7', 'G8', 'G9', 'H9', 'F7', 'F8', 'F9', 'E7', 'E8', 'H8', 'H7', 'G6', 'H6'], 'האי והגשר'),
]
STAGE_OF = {z: k for k, (sid, zs, _) in enumerate(ORDER) for z in zs}
def sstage(s):   # a segment is built with the earliest zone along its inside (a road on a seam comes with the first of its two zones)
    zs = set(); pts = s['pts']; L = sum(math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]) for k in range(len(pts) - 1))
    acc = 0
    for k in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]; l = math.hypot(bx - ax, by - ay); m = max(1, int(l // 40))
        for t in range(m + 1):
            d_ = acc + l * t / m
            if d_ < min(100, L / 3) or d_ > L - min(100, L / 3): continue
            x, y = ax + (bx - ax) * t / m, ay + (by - ay) * t / m
            g_ = CLS[s['cls']]['halfW'] + 40   # a road that borders a zone is built with it (the zone needs its frontage) — across the road only
            ux, uy = (bx - ax) / (l or 1), (by - ay) / (l or 1)
            for f_ in (-g_, 0, g_):
                z = zone_of(x - uy * f_, y + ux * f_)
                if z in STAGE_OF: zs.add(STAGE_OF[z])
        acc += l
    return min(zs) if zs else len(ORDER) - 1
for s in SEG: s['stage'] = ORDER[sstage(s)][0] if sstage(s) < len(ORDER) else 'S13'
# 1.11 (B4, the first zone built from the map): a new road may not be built over an old road that still stands. רחוב בית הספר (y 2550)
# lies 5 m over the south side of R-MID of B3 (y 2430, 23.6 m with its sidewalks) — it is built with B3 (S2), when R-MID goes; in S1
# שדרת המערב meets R-MID at its west end (B3W) and רחוב השכונה meets it at B3C3. The check "המעבר" below finds any such overlap.
STAGE_WAIT = {'LC-SCH/1': ('S2', 'R-MID של B3 (B3-RM-W, B3-RM-L) עדיין עומד ב-S1 — רחוב בית הספר היה עולה על המדרכה והנתיב הדרומי שלו'),
              'CL-I/1': ('S9', 'הכניסה של היום ל-E3 (E3-ENTRY, y 2430) עומדת עד S9 — דרך האי הייתה עולה עליה 5.7 מ׳ לאורך 20 מ׳')}
for s in SEG:
    if s['id'] in STAGE_WAIT: s['stage'] = STAGE_WAIT[s['id']][0]; s['wait'] = STAGE_WAIT[s['id']][1]
ON = {n_['id']: n_ for n_ in GR['nodes']}
OE = [dict(id=e['id'], a=e['a'], b=e['b'], cls=e['cls'], name=e.get('name', '')) for e in GR['edges']]
def inR(x, y, zs, tol=1):   # inside the rebuilt area; a node on the seam of a rebuilt zone counts as inside
    for z in zs:
        x0, y0, x1, y1 = zrect(z)
        if x0 - tol <= x <= x1 + tol and y0 - tol <= y <= y1 + tol: return True
    return False
def frozen(p): return (p['x'] >= 4800 - 1 and p['y'] <= 1700 + 1) or (p['x'] >= 7200 - 1 and p['y'] <= 2550 + 1)   # the airport (R-32)
SI = {sid: k for k, (sid, _, _) in enumerate(ORDER)}
TRANS = []; active = {}; allt = []; gone_total = set(); JOINED = set()
class UF:
    def __init__(s): s.p = {}
    def f(s, x):
        s.p.setdefault(x, x)
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b): s.p[s.f(a)] = s.f(b)
for k, (sid, zs, why) in enumerate(ORDER):
    done = [z for _, Z, _ in ORDER[:k + 1] for z in Z]
    built = [s_ for s_ in SEG if SI[s_['stage']] <= k]; bset = {s_['id'] for s_ in built}
    removed, cutn = [], {}
    for e in OE:
        a_, b_ = ON[e['a']], ON[e['b']]
        if frozen(a_) and frozen(b_): continue
        # an old street goes when its middle is inside the rebuilt area, or both its ends are (a street on the seam goes with the first zone)
        if inR((a_['x'] + b_['x']) / 2, (a_['y'] + b_['y']) / 2, done, -1) or (inR(a_['x'], a_['y'], done) and inR(b_['x'], b_['y'], done)):
            removed.append(e['id'])
            for p_ in (a_, b_): cutn[p_['id']] = p_
    def on_new(x, y): return any(dseg(x, y, *s_['pts'][m], *s_['pts'][m + 1])[0] <= 60 for s_ in built for m in range(len(s_['pts']) - 1))
    for e in OE:   # an old street on (almost) the same line as a new one is replaced by it
        if e['id'] in removed: continue
        a_, b_ = ON[e['a']], ON[e['b']]
        if frozen(a_) and frozen(b_): continue
        if on_new(a_['x'], a_['y']) and on_new(b_['x'], b_['y']) and on_new((a_['x'] + b_['x']) / 2, (a_['y'] + b_['y']) / 2):
            removed.append(e['id'])
            for p_ in (a_, b_): cutn[p_['id']] = p_
    rem_now = [e for e in removed if e not in gone_total]; gone_total.update(rem_now); rset = set(removed)
    olive = [e for e in OE if e['id'] not in rset]
    odeg = {}
    for e in olive: odeg[e['a']] = odeg.get(e['a'], 0) + 1; odeg[e['b']] = odeg.get(e['b'], 0) + 1
    ended = [t['id'] for o, t in list(active.items()) if o not in odeg]
    for o in [o for o, t in active.items() if t['id'] in ended]: active[o]['until'] = sid; del active[o]
    uf = UF()
    for e in olive: uf.u('o:' + e['a'], 'o:' + e['b'])
    for s_ in built: uf.u('n:' + s_['a'], 'n:' + s_['b'])
    for o, t in active.items(): uf.u('o:' + o, 'n:' + t['attach'])
    def near_new(px, py):
        best = None
        for s_ in built:
            for m in range(len(s_['pts']) - 1):
                d, qx, qy, t = dseg(px, py, *s_['pts'][m], *s_['pts'][m + 1])
                if best is None or d < best[0]: best = (d, qx, qy, s_)
        return best
    joins = []
    for o in odeg:   # the airport gates: an old airport road that starts exactly where a new road ends is joined for good
        if frozen(ON[o]):
            bst = near_new(ON[o]['x'], ON[o]['y'])
            if bst and bst[0] < 1:
                uf.u('o:' + o, 'n:' + bst[3]['a'])
                if o not in JOINED: JOINED.add(o); joins.append(dict(old_node=o, at=bst[3]['id'], note='שער השדה — אותה נקודה, חיבור קבוע'))
    cands = []
    for o, p_ in cutn.items():
        if o in active or o not in odeg: continue
        bst = near_new(p_['x'], p_['y'])
        if bst and bst[0] <= 700: cands.append((bst[0], o, bst))
    dang = [x for x in N if any(o for o, s_ in ADJ[x] if s_['id'] not in bset) and any(o for o, s_ in ADJ[x] if s_['id'] in bset)]
    for x in dang:
        best = min(((math.hypot(ON[o]['x'] - N[x]['x'], ON[o]['y'] - N[x]['y']), o) for o in odeg if not frozen(ON[o])), default=None)
        if best and best[0] <= 400 and best[1] not in active:
            q = ON[best[1]]; bst = near_new(q['x'], q['y'])
            if bst: cands.append((bst[0], best[1], bst))
    cands.sort(key=lambda c: c[0]); pick = {}
    def take(c, why_):
        d, o, (dd, qx, qy, s_) = c
        if o in pick or o in active: return False
        pick[o] = (c, why_); uf.u('o:' + o, 'n:' + s_['a']); return True
    for c in cands:
        if c[0] < 1: take(c, 'צומת ישן שנשאר על הדרך החדשה')
        elif c[0] <= 150: take(c, 'המשך טבעי של רחוב ישן (עד 15 מ׳)')
    # every new piece gets two links to the old network (while some of the city is old); every old piece one link to the new
    live = [o for o in odeg if not frozen(ON[o])]
    for rnd in range(3):
        pieces = {}
        for s_ in built: pieces.setdefault(uf.f('n:' + s_['a']), []).append(s_)
        for pc, segs_ in pieces.items():
            links = sum(1 for oo, (cc, w_) in pick.items() if uf.f('o:' + oo) == pc) + sum(1 for oo, t in active.items() if uf.f('o:' + oo) == pc)
            if not live or links >= (2 if any(uf.f('o:' + o) != pc for o in live) else 0): continue
            opts = []
            for o in live:
                if o in pick or o in active: continue
                q = ON[o]; best = None
                for s_ in segs_:
                    for m in range(len(s_['pts']) - 1):
                        d, qx, qy, t = dseg(q['x'], q['y'], *s_['pts'][m], *s_['pts'][m + 1])
                        if best is None or d < best[0]: best = (d, qx, qy, s_)
                if best and best[0] <= 700: opts.append((best[0], o, best))
            opts.sort(key=lambda c: c[0])
            for c in opts:
                if links >= 2: break
                if take(c, 'חיבור הרשת החדשה לישנה'): links += 1
        # old pieces cut off from everything
        opieces = {}
        for o in live: opieces.setdefault(uf.f('o:' + o), []).append(o)
        main = uf.f('n:' + built[0]['a']) if built else None
        for pc, os_ in opieces.items():
            if pc == main: continue
            c = min((cc for cc in cands if cc[1] in os_ and cc[1] not in pick), key=lambda c: c[0], default=None)
            if c: take(c, 'חיבור חלק ישן שנותק')
    for c in cands:
        d, o, bst = c
        if o not in pick and odeg.get(o, 0) == 1 and d <= 300: take(c, 'רחוב ישן שנשאר ללא מוצא')
    add, dead = [], []
    for o, (c, why_) in pick.items():
        d, o, (dd, qx, qy, s_) = c; p_ = ON[o]
        nn = min((N[x] for x in (s_['a'], s_['b'])), key=lambda q: math.hypot(q['x'] - qx, q['y'] - qy))
        if math.hypot(nn['x'] - qx, nn['y'] - qy) < 30: qx, qy, at = nn['x'], nn['y'], nn['id']
        else: at = f"{s_['id']} ({qx:.0f}, {qy:.0f})"
        dd = math.hypot(p_['x'] - qx, p_['y'] - qy)
        jd = min((math.hypot(N[j]['x'] - qx, N[j]['y'] - qy) for j in (s_['a'], s_['b']) if j in JUNC), default=1e9)
        t = dict(id=f"TMP-{sid}-{len(add) + 1}", old_node=o, old_label=p_.get('label', ''), to=at, attach=s_['a'], len_m=round(dd / 10, 1),
                 x=[p_['x'], p_['y']], y=[round(qx), round(qy)], why=why_, new_junction=at not in N,
                 spacing_m=None if at in N else round(jd / 10), exempt_R15=(at not in N and jd < 600), until=None)
        if dd < 1 and frozen(p_): continue
        add.append(t); active[o] = t; allt.append(t)
    for o, p_ in cutn.items():
        if o in odeg and odeg[o] == 1 and o not in active and not frozen(p_): dead.append(dict(old_node=o, label=p_.get('label', ''), note='נשאר ללא מוצא עד שהאזור השכן נבנה'))
    comps = {uf.f('n:' + s_['a']) for s_ in built} | {uf.f('o:' + e['a']) for e in olive}
    TRANS.append(dict(stage=sid, zones=zs, why=why, new_segments=[s_['id'] for s_ in SEG if s_['stage'] == sid], removed=rem_now,
                      temp_added=add, temp_removed=ended, dead_ends=dead, joins=joins, pieces=len(comps)))
ntemp = len(allt); open_end = [t['id'] for t in allt if t['until'] is None]
bad_pieces = [t['stage'] for t in TRANS if t['pieces'] > 1]
chk('המעבר — בכל שלב הרשת (חדשה + ישנה + זמניים) מחוברת; כל חיבור זמני רשום בנפרד עם השלב שבו הוא מוסר', not open_end and not bad_pieces,
    f"{ntemp} חיבורים זמניים ב-{len(TRANS)} שלבים; " + (f'כולם מוסרים עד הסוף; {sum(1 for t in allt if t["exempt_R15"])} מהם יוצרים צומת זמני קרוב מ-60 מ׳ לצומת חדש (רשומים ומוחרגים זמנית).' if not open_end else f'לא מוסרים: {open_end}') + (f' · שלבים עם רשת מפוצלת: {bad_pieces}' if bad_pieces else ''))

# 1.11: in no stage does a new road run over an old road that still stands (alongside it, more than 1 m into it, more than 15 m long);
# a road on the same axis as the old one (it replaces it in place) is not an overlap
SI_ = {t_['stage']: k_ for k_, t_ in enumerate(TRANS)}
ovl_st = []
for k_, t_ in enumerate(TRANS):
    gone_ = set(x_ for tt_ in TRANS[:k_ + 1] for x_ in tt_['removed'])
    for s_ in SEG:
        if SI_.get(s_['stage'], 99) > k_: continue
        hw1 = CLS[s_['cls']]['halfW']
        for m in range(len(s_['pts']) - 1):
            (ax, ay), (bx, by) = s_['pts'][m], s_['pts'][m + 1]; hor1 = abs(ay - by) < 1; ver1 = abs(ax - bx) < 1
            if not (hor1 or ver1): continue
            for e_ in GR['edges']:
                if e_['id'] in gone_: continue
                A_, B_ = ON[e_['a']], ON[e_['b']]; hor2 = abs(A_['y'] - B_['y']) < 1; ver2 = abs(A_['x'] - B_['x']) < 1
                if not ((hor1 and hor2) or (ver1 and ver2)): continue
                hw2 = e_.get('width', 96) / 2 + e_.get('sidewalk', 20)
                if hor1:
                    if abs(ay - A_['y']) < 10: continue
                    along = min(max(ax, bx), max(A_['x'], B_['x'])) - max(min(ax, bx), min(A_['x'], B_['x'])); across = hw1 + hw2 - abs(ay - A_['y'])
                else:
                    if abs(ax - A_['x']) < 10: continue
                    along = min(max(ay, by), max(A_['y'], B_['y'])) - max(min(ay, by), min(A_['y'], B_['y'])); across = hw1 + hw2 - abs(ax - A_['x'])
                if along > 150 and across > 10: ovl_st.append(f"{t_['stage']}: {s_['id']} × {e_['id']} ({across / 10:.1f} מ׳ לאורך {along / 10:.0f} מ׳)")
chk('המעבר — בשום שלב כביש חדש לא עולה על כביש של היום שעדיין עומד', not ovl_st,
    'אין חפיפה באף שלב (בדיקה של כל קטע חדש מול כל רחוב של היום שעוד לא הוסר). ' + '; '.join(f"{s_['id']} נבנה ב-{s_['stage']} ולא קודם: {s_['wait']}" for s_ in SEG if s_.get('wait')) + '.'
    + (f" חפיפות: {sorted(set(ovl_st))}" if ovl_st else ''))

# ---------------------------------------------------------------- per zone
ZONES = {}
MP = json.load(open(W + '/plan600/data/masterplan.json'))['zones']
for z in MP:
    segs = [s for s in SEG if z in s['zones']]
    if not segs and z not in ZT: continue
    rids = []
    for s in segs:
        if s['road'] not in rids: rids.append(s['road'])
    sig = [x['node'] for x in SIG if N[x['node']]['zone'] == z]
    rb = [k for k, v in N.items() if v['kind'] == 'roundabout' and v['zone'] == z]
    lanes = collections.Counter()
    for s in segs: lanes[f"{CLS[s['cls']]['he']} {s['lanes']}"] += s['len_m']
    ZONES[z] = dict(purpose=MP[z].get('purpose', ''), roads=rids, segments=[s['id'] for s in segs], signals=sig, roundabouts=rb,
                    lanes_m={k: round(v) for k, v in lanes.items()}, stage=next((sid for sid, zs, _ in ORDER if z in zs), None),
                    temp=[a['id'] for t in TRANS for a in t['temp_added'] if zone_of(*a['y']) == z or zone_of(*a['x']) == z])


# ---------------------------------------------------------------- 31.10: the inside of the zones not built yet (plan7b_sites.py)
import plan7b_sites as ST
import plan7b_zones6 as Z6
SITES, DWS = ST.S, ST.DW
def item_box(i):
    if i['kind'] == 'pad': (cx, cy), r = i['c'], i['safety']; return (cx - r, cy - r, cx + r, cy + r)
    if i['kind'] in ('site', 'path'): xs = [p[0] for p in i['rect']]; ys = [p[1] for p in i['rect']]; h = i['hw']; return (min(xs) - h, min(ys) - h, max(xs) + h, max(ys) + h)
    return tuple(i['rect'])
def box_hits_road(b, pad=0):
    x0, y0, x1, y1 = b; out = []
    for s_ in SEG:
        hw = CLS[s_['cls']]['halfW'] - pad; p = s_['pts']
        for m in range(len(p) - 1):
            (ax, ay), (bx, by) = p[m], p[m + 1]
            if min(ax, bx) - hw < x1 and max(ax, bx) + hw > x0 and min(ay, by) - hw < y1 and max(ay, by) + hw > y0: out.append(s_['id']); break
    return out
road_bad, ovl, sea_bad, size_bad, stall_bad, d275, dw_bad = [], [], [], [], [], [], []
for i in SITES:
    b = item_box(i) if i['kind'] != 'pad' else (i['c'][0] - i['r'], i['c'][1] - i['r'], i['c'][0] + i['r'], i['c'][1] + i['r'])
    if i.get('poly'):   # a lot cut by a turning circle: no road axis may run inside its polygon
        h = [s_['id'] for s_ in SEG for m in range(len(s_['pts']) - 1) for t_ in range(0, 21)
             if pip(s_['pts'][m][0] + (s_['pts'][m + 1][0] - s_['pts'][m][0]) * t_ / 20, s_['pts'][m][1] + (s_['pts'][m + 1][1] - s_['pts'][m][1]) * t_ / 20, i['poly'])]
        if h: road_bad.append(f"{i['id']}×{h[0]}")
    elif i['kind'] != 'pier':
        h = box_hits_road(b, 2)
        if h and i['kind'] not in ('site', 'path'): road_bad.append(f"{i['id']}×{h[0]}")
    for (x, y) in ((b[0] + 5, b[1] + 5), (b[2] - 5, b[3] - 5), ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)):
        if i['kind'] not in ('pier', 'beach') and (is_sea(x, y) or in_lake(x, y)): sea_bad.append(i['id']); break
    if i.get('real'):
        w, hh = (b[2] - b[0]) / 10, (b[3] - b[1]) / 10
        if abs(max(w, hh) - max(i['real'])) > 1.5 or abs(min(w, hh) - min(i['real'])) > 1.5: size_bad.append(f"{i['id']} {w:.1f}×{hh:.1f} מול {i['real']}")
    if i.get('stalls'):
        a = (b[2] - b[0]) * (b[3] - b[1]) / 100 + i.get('aisle_m2', 0)   # round 6: a car park whose aisle is a lane next to it
        if i['stalls'] * 25 > a: stall_bad.append(f"{i['id']} {i['stalls']} מקומות ב-{a:.0f} מ״ר")
    if i['kind'] == 'building' and i.get('floors'):
        top = (b[0], b[1] - (i['band_px'] if i.get('band_px') is not None else i['floors'] * 32 * .6), b[2], b[1]); h = box_hits_road(top, 0)   # round 6: a zone built with BLD41 gives its engine's band + [o['id'] for o in SITES if o['kind'] == 'parking' and o['zone'] == i['zone'] and min(top[2], o['rect'][2]) > max(top[0], o['rect'][0]) and min(top[3], o['rect'][3]) > max(top[1], o['rect'][1])]
        if h: d275.append(f"{i['id']}×{h[0]}")
for k, i in enumerate(SITES):
    for j in SITES[k + 1:]:
        if i['zone'] != j['zone'] or 'site' in (i['kind'], j['kind']) or 'path' in (i['kind'], j['kind']) or 'beach' in (i['kind'], j['kind']) or 'pier' in (i['kind'], j['kind']): continue
        if i.get('parent') == j['id'] or j.get('parent') == i['id']: continue
        a, b = item_box(i), item_box(j)
        if i['kind'] == 'pad' or j['kind'] == 'pad':
            pd, o = (i, j) if i['kind'] == 'pad' else (j, i)
            if o['kind'] in ('building',) and min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]): ovl.append(f"{pd['id']} (שטח הבטיחות)×{o['id']}")
            continue
        if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]): ovl.append(f"{i['id']}×{j['id']}")
def CW(c): x = CLS[c]; return ((2 if x['twoway'] else 1) * x['dirN'] * x['lane_m'] + x['median_m']) * 10   # the carriageway, px
def edge_hit(x, y, tol=25):   # the network segment whose outer edge (x, y) touches: (segment, distance from its axis)
    best = None
    for s_ in SEG:
        for m in range(len(s_['pts']) - 1):
            dd = dseg(x, y, *s_['pts'][m], *s_['pts'][m + 1])
            if abs(dd[0] - CLS[s_['cls']]['halfW']) <= tol and (best is None or abs(dd[0] - CLS[s_['cls']]['halfW']) < best[2]): best = (s_, dd, abs(dd[0] - CLS[s_['cls']]['halfW']))
    return best
SITE_ROADS = []   # 31.10 (the owner 20:23): the roads inside the lots, drawn as roads — the site roads and a stub for every driveway
for d in DWS:
    rd = next((r_ for r_ in Rd if r_['id'] == d['road']), None)
    if not rd: dw_bad.append(f"{d['id']}: אין דרך {d['road']}"); continue
    best = None   # the driveway sits on the real edge of its road (the roads got their real width)
    for s_ in SEG:
        if s_['road'] != d['road']: continue
        for m in range(len(s_['pts']) - 1):
            dd, qx, qy, t = dseg(d['at'][0], d['at'][1], *s_['pts'][m], *s_['pts'][m + 1])
            if best is None or dd < best[0]: best = (dd, qx, qy, s_['pts'][m], s_['pts'][m + 1])
    dd, qx, qy, (ax, ay), (bx, by) = best; L_ = math.hypot(bx - ax, by - ay); nx, ny = -(by - ay) / L_, (bx - ax) / L_
    side = 1 if (d['at'][0] - qx) * nx + (d['at'][1] - qy) * ny >= 0 else -1; hw = CLS[rd['cls']]['halfW']
    d['at'] = [round(qx + side * nx * hw, 1), round(qy + side * ny * hw, 1)]
    near = min(math.hypot(N[x]['x'] - d['at'][0], N[x]['y'] - d['at'][1]) for x in JUNC)
    d['to_junction_m'] = round(near / 10, 1)
    if near < 180 or dd > hw + 30: dw_bad.append(f"{d['id']} {near / 10:.0f} מ׳ מצומת, {dd / 10:.0f} מ׳ מהציר")
    if d.get('to'):
        tp = [list(d['to'])] if isinstance(d['to'][0], (int, float)) else [list(q) for q in d['to']]
        cw = CW(rd['cls']); inner = [round(qx + side * nx * (cw / 2 - 3), 1), round(qy + side * ny * (cw / 2 - 3), 1)]
        SITE_ROADS.append(dict(id=d['id'], zone=d['zone'], kind='driveway', cls='driveway' if d['lanes'] != '1' or not isinstance(d['to'][0], (list, tuple)) else 'service', lanes=d['lanes'], hw=19.5 if d['lanes'] == '1' else 39.0, pts=[d['at']] + tp,
                               draw=[inner] + tp, label=d['label'], road=d['road'], oneway=False))
for i in SITES:
    if i['kind'] == 'site':
        SITE_ROADS.append(dict(id=i['id'], zone=i['zone'], kind='site', cls=i.get('cls', 'service'), lanes=i.get('lanes', '1+1'), hw=i['hw'], pts=[list(q) for q in i['rect']],
                               label=i['label'], road=None, via=i.get('via'), oneway=i.get('oneway', False)))
for r_ in SITE_ROADS:
    if r_['kind'] != 'site': continue
    dr = [list(q) for q in r_['pts']]
    for k_ in (0, -1):
        h = edge_hit(*dr[k_])
        if h:
            s_, (dd, qx, qy, t_), _ = h; f_ = (CW(s_['cls']) / 2 - 3) / (dd or 1); dr[k_] = [round(qx + (dr[k_][0] - qx) * f_, 1), round(qy + (dr[k_][1] - qy) * f_, 1)]
    r_['draw'] = dr
for i in SITES:
    if i.get('apron'):
        x0, y0, x1, y1 = i['rect']; h = edge_hit(x1, (y0 + y1) / 2)
        if h: s_, (dd, qx, qy, t_), _ = h; i['road'] = s_['road']; i['draw'] = [x0, y0, round(qx - (CW(s_['cls']) / 2 - 3), 1), y1]
def band(p, q, hw):   # an axis-aligned piece of road as a rectangle (butt ends)
    (ax, ay), (bx, by) = p, q
    if abs(ay - by) < 1: return (min(ax, bx), ay - hw, max(ax, bx), ay + hw)
    if abs(ax - bx) < 1: return (ax - hw, min(ay, by), ax + hw, max(ay, by))
    return (min(ax, bx) - hw, min(ay, by) - hw, max(ax, bx) + hw, max(ay, by) + hw)
sr_bad = []   # no internal road crosses a building (a driveway may end at the face of the building it serves)
for r_ in SITE_ROADS:
    for o in SITES:
        if o['kind'] != 'building' or o['zone'] != r_['zone']: continue
        x0, y0, x1, y1 = o['rect']
        for m in range(len(r_['pts']) - 1):
            b0, b1_, b2, b3 = band(r_['pts'][m], r_['pts'][m + 1], r_['hw'])
            if b0 < x1 - 5 and b2 > x0 + 5 and b1_ < y1 - 5 and b3 > y0 + 5: sr_bad.append(f"{r_['id']}×{o['id']}"); break
# 31.10 (the owner 20:39): every building, car park, yard, court and field has a road that reaches it — its own entrance, an inner road,
# or the car park / yard / apron next to it (a court or a field also through the court or the building next to it)
SR = {r_['id']: r_ for r_ in SITE_ROADS}; RDN = {r_['id']: r_ for r_ in Rd}
def reach(r_):   # the network road an inner road reaches, and is it really touching it
    v = r_['road'] if r_['kind'] == 'driveway' else r_.get('via')
    if v in SR: return reach(SR[v])
    if v in N: return next(x['id'] for x in Rd if v in x['nodes'] and x['cls'] != 'track')
    return v
def touches(r_):
    v = r_['road'] if r_['kind'] == 'driveway' else r_.get('via'); ends = [r_['pts'][0], r_['pts'][-1]]
    if v in SR: return any(min(dseg(x, y, *SR[v]['pts'][m], *SR[v]['pts'][m + 1])[0] for m in range(len(SR[v]['pts']) - 1)) <= SR[v]['hw'] + 15 for x, y in ends)
    if v in N: return any(math.hypot(x - N[v]['x'], y - N[v]['y']) <= 180 for x, y in ends)
    return any(min(dseg(x, y, *s_['pts'][m], *s_['pts'][m + 1])[0] for s_ in SEG if s_['road'] == v for m in range(len(s_['pts']) - 1)) <= CLS[RDN[v]['cls']]['halfW'] + 15 for x, y in ends)
for r_ in SITE_ROADS:
    if not touches(r_): sr_bad.append(f"{r_['id']} לא נוגעת ב-{r_.get('via') or r_['road']}")
def rgap(a_, b_): return math.hypot(max(0, max(a_[0], b_[0]) - min(a_[2], b_[2])), max(0, max(a_[1], b_[1]) - min(a_[3], b_[3])))
NEED = [i for i in SITES if i['kind'] in ('building', 'parking', 'yard', 'court', 'field', 'lot')]
ACC = {}
for i in NEED:
    if i.get('apron'):
        if i.get('road'): ACC[i['id']] = dict(road=i['road'], via=i['id'], through=None)
        continue
    R_ = tuple(i['rect']); lim = 20 if i['kind'] in ('building', 'parking', 'yard') else 60; best = None
    for r_ in SITE_ROADS:
        g_ = min(rgap(R_, band(r_['pts'][m], r_['pts'][m + 1], r_['hw'])) for m in range(len(r_['pts']) - 1))
        if g_ <= lim and (best is None or g_ < best[0]): best = (g_, r_)
    if best: ACC[i['id']] = dict(road=reach(best[1]), via=best[1]['id'], through=None)
for _ in range(4):
    for i in NEED:
        if i['id'] in ACC: continue
        ok_k = ('parking', 'yard') if i['kind'] in ('building', 'parking', 'yard') else ('parking', 'yard', 'building', 'court', 'field')
        for j in SITES:
            if j['id'] in ACC and j['zone'] == i['zone'] and j['kind'] in ok_k and rgap(tuple(i['rect']), tuple(j['rect'])) <= 60:
                ACC[i['id']] = dict(road=ACC[j['id']]['road'], via=ACC[j['id']]['via'], through=j['id']); break
for i in NEED:
    if i['id'] in ACC: a_ = ACC[i['id']]; i['access'] = dict(a_, road_name=RDN[a_['road']]['name'])
no_acc = [i['id'] for i in NEED if i['id'] not in ACC]
ACCESS_SITES_TXT = None   # the check of the access is made after all the lots of the city exist (below)
chk('האזורים הלא בנויים — כל פריט בתוך הבלוק: לא על כביש, לא בים ולא באגם, בלי חפיפה (המנחת עם שטח הבטיחות); הדרכים הפנימיות לא חוצות מבנה', not road_bad and not ovl and not sea_bad and not sr_bad,
    f"{len(SITES)} פריטים ב-{len(set(i['zone'] for i in SITES))} אזורים; {len(SITE_ROADS)} דרכים פנימיות וכניסות מצוירות כדרכים, אף אחת לא חוצה מבנה." + (f" חוצות מבנה: {sr_bad}" if sr_bad else '') + (f" על כביש: {road_bad}" if road_bad else '') + (f" חפיפה: {ovl}" if ovl else '') + (f" בים: {sea_bad}" if sea_bad else ''))
chk('המגרשים בגודל האמיתי (R-18 ב׳) והחניונים מכילים את המקומות (25 מ״ר למקום עם המעבר)', not size_bad and not stall_bad,
    'כולם במידה. ' + '; '.join(size_bad + stall_bad) if (size_bad or stall_bad) else f"{sum(1 for i in SITES if i.get('real'))} מגרשים במידה; {sum(i.get('stalls', 0) for i in SITES)} מקומות חניה ב-{sum(1 for i in SITES if i.get('stalls'))} חניונים.")
chk('הכניסות למגרשים (לא צמתים) — על הדרך, לפחות 18 מ׳ מצומת', not dw_bad, f"{len(DWS)} כניסות; הקרובה ביותר {min(d.get('to_junction_m', 99) for d in DWS):.1f} מ׳ מצומת." if not dw_bad else '; '.join(dw_bad))
chk('D-275 במבנים החדשים — המלבן שמעל הטביעה לא חותך כביש, מדרכה או חניון', not d275, 'לא חותך.' if not d275 else '; '.join(d275))
for z in ZONES: ZONES[z]['sites'] = [i['id'] for i in SITES if i['zone'] == z]; ZONES[z]['driveways'] = [d['id'] for d in DWS if d['zone'] == z]

# ---------------------------------------------------------------- 31.10 (the owner 20:23): the bus lines, their stops and the crosswalks
BAY = dict(entry=40, stop=150, exit=40, depth=30)   # px: a 15 m stop between two 4 m tapers, 3 m into the sidewalk
BAYL = BAY['entry'] + BAY['stop'] + BAY['exit']
SEGBY = {frozenset((s_['a'], s_['b'])): s_ for s_ in SEG}
XW = []   # crosswalks: on every arm of every junction, from 1 to 5 m beyond the edge of the crossing road (beyond the ring of a roundabout)
for k in sorted(JUNC):
    n_ = N[k]
    for o, s_ in ADJ[k]:
        others = [t for oo, t in ADJ[k] if t is not s_]
        if not others: continue
        hc = 175 if n_['kind'] == 'roundabout' else max(CLS[t['cls']]['halfW'] for t in others)
        p_ = s_['pts']; q_ = p_[1] if s_['a'] == k else p_[-2]; L_ = math.hypot(q_[0] - n_['x'], q_[1] - n_['y'])
        XW.append(dict(node=k, seg=s_['id'], d0=round(hc + 10), d1=round(hc + 50), at=[n_['x'], n_['y']], u=[round((q_[0] - n_['x']) / L_, 4), round((q_[1] - n_['y']) / L_, 4)], cw=CW(s_['cls'])))
def seg_frame(a, b):
    s_ = SEGBY[frozenset((a, b))]; pa, pb = N[a], N[b]; L_ = math.hypot(pb['x'] - pa['x'], pb['y'] - pa['y'])
    u = ((pb['x'] - pa['x']) / L_, (pb['y'] - pa['y']) / L_); return s_, pa, L_, u, (-u[1], u[0])   # r = the right of travel a→b (y down)
def blocks(a, b, side):
    """the stretches along a→b (px from a) where a bay on this side may not be: driveways, aprons, crosswalks, the rail bridge"""
    s_, pa, L_, u, r = seg_frame(a, b); sv = (r[0] * side, r[1] * side); hw = CLS[s_['cls']]['halfW']; out = []
    def proj(x, y): return (x - pa['x']) * u[0] + (y - pa['y']) * u[1], (x - pa['x']) * sv[0] + (y - pa['y']) * sv[1]
    for d in DWS:
        if d['road'] != s_['road']: continue
        t_, o_ = proj(*d['at'])
        if -50 <= t_ <= L_ + 50 and 0 < o_ <= hw + 15: w_ = 19.5 if d['lanes'] == '1' else 39; out.append((t_ - w_ - 30, t_ + w_ + 30, d['id']))
    for i in SITES:
        if i.get('apron') and i.get('road') == s_['road']:
            x0, y0, x1, y1 = i['rect']; ts = [proj(x, y) for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
            if min(o_ for t_, o_ in ts) > 0 and min(o_ for t_, o_ in ts) <= hw + 20: out.append((min(t_ for t_, o_ in ts) - 30, max(t_ for t_, o_ in ts) + 30, i['id']))
    for x in XW:
        if x['seg'] != s_['id']: continue
        if x['node'] == a: out.append((x['d0'] - 20, x['d1'] + 20, 'מעבר חצייה ' + a))
        else: out.append((L_ - x['d1'] - 20, L_ - x['d0'] + 20, 'מעבר חצייה ' + b))
    for c in P.CROSS:
        if c['road'] == s_['road']:
            t_, o_ = proj(*c['at'])
            if -100 <= t_ <= L_ + 100 and abs(o_) < 200: out.append((t_ - 120, t_ + 120, c['id']))
    return out
def cross_hw(n, road):   # round 6 (R-46): the half width of the widest road CROSSING at node n (not one that goes on straight) — the junction's edge is that far from its centre
    mine = [x for x in SEG if x['road'] == road and n in (x.get('a'), x.get('b'))]
    def dirv(x):
        p = x['pts']; q = p[1] if (abs(p[0][0] - N[n]['x']) < 1 and abs(p[0][1] - N[n]['y']) < 1) else p[-2]; o = p[0] if q is p[1] else p[-1]
        d = (q[0] - o[0], q[1] - o[1]); L = math.hypot(*d) or 1; return (d[0] / L, d[1] / L)
    md = dirv(mine[0]) if mine else (1, 0)
    return max([CLS[x['cls']]['halfW'] for x in SEG if x['road'] != road and n in (x.get('a'), x.get('b')) and abs(dirv(x)[0] * md[0] + dirv(x)[1] * md[1]) < .5] or [0])
def free(a, b, side, extra=()):
    s_, pa, L_, u, r = seg_frame(a, b)
    # round 6 (R-46, D‑332): measured from the junction's EDGE — 20 m before the junction ahead (near side), 10 m after the one behind (far side)
    ahead, behind = (b, a) if side == 1 else (a, b)
    ea = (cross_hw(a, s_['road']) + (200 if a == ahead else 100)) if a in JUNC else 50; eb = (cross_hw(b, s_['road']) + (200 if b == ahead else 100)) if b in JUNC else 50
    lo = ea; hi = L_ - eb - BAYL; bl = blocks(a, b, side) + list(extra); ok = []
    if RELAX.get((a, b, side)): lo, hi = (200 if a in JUNC else 50), L_ - (200 if b in JUNC else 50) - BAYL   # no room by the rule — round 5's (20 m from the centre); listed as an exception
    t0 = lo
    while t0 <= hi + 0.1:
        if not any(t0 < y1 and t0 + BAYL > y0 for y0, y1, _ in bl): ok.append(t0)
        t0 += 5
    return ok, lo, hi
STOPS = []; stop_bad = []; BL = {}; RELAX = {}; STOP_EXC = []
for line in P.ROUTES['bus']:
    dirs = set(zip(line['path'], line['path'][1:]))
    if line['twoway']: dirs |= {(b, a) for a, b in dirs}
    req = collections.Counter(frozenset((x_[0], x_[1])) for x_ in line['stops'])
    seen_k = collections.Counter()
    for x_ in line['stops']:
        a, b, nm = x_[:3]; key = frozenset((a, b)); st = next((x for x in STOPS if x['key'] == key and x['name'] == nm), None)
        if st is None:
            st = dict(key=key, name=nm, a=a, b=b, lines=[], bays={}); STOPS.append(st)
        if line['id'] not in st['lines']: st['lines'].append(line['id'])
        for da, db in ((a, b), (b, a)):
            if (da, db) in dirs: st['bays'][(da, db)] = None
        seen_k[key] += 1; st['pref'] = x_[3] if len(x_) > 3 else ((seen_k[key]) / (req[key] + 1) if req[key] > 1 else .5)
for st in STOPS:
    a, b = st['a'], st['b']; taken = BL.setdefault(st['key'], [])
    sides = []
    for (da, db) in st['bays']: sides.append(1 if (da, db) == (a, b) else -1)   # the bay of travel a→b is on its right (+1); b→a on the left of a→b
    opts = {sd: free(a, b, sd, [(y0, y1, 'תחנה') for y0, y1, sd2 in taken if sd2 == sd]) for sd in sides}
    for sd in sides:
        if not opts[sd][0]:
            RELAX[(a, b, sd)] = True; opts[sd] = free(a, b, sd, [(y0, y1, 'תחנה') for y0, y1, sd2 in taken if sd2 == sd]); STOP_EXC.append(st['name'])
    if any(not o[0] for o in opts.values()): stop_bad.append(f"{st['name']}: אין מקום למפרץ"); continue
    lo, hi = list(opts.values())[0][1], list(opts.values())[0][2]; pref = lo + (hi - lo) * st['pref']
    common = sorted(set.intersection(*[set(o[0]) for o in opts.values()]), key=lambda t: abs(t - pref))
    pos = {sd: (common[0] if common else min(opts[sd][0], key=lambda t: abs(t - pref))) for sd in sides}
    st['bay_list'] = []
    s_, pa, L_, u, r = seg_frame(a, b); e_ = CW(s_['cls']) / 2
    for sd, t0 in pos.items():
        taken.append((t0 - 30, t0 + BAYL + 30, sd)); sv = (r[0] * sd, r[1] * sd)
        def P_(t, off): return [round(pa['x'] + u[0] * t + sv[0] * off, 1), round(pa['y'] + u[1] * t + sv[1] * off, 1)]
        poly = [P_(t0, e_ - 2), P_(t0 + BAY['entry'], e_ + BAY['depth']), P_(t0 + BAY['entry'] + BAY['stop'], e_ + BAY['depth']), P_(t0 + BAYL, e_ - 2)]
        da, db = (a, b) if sd == 1 else (b, a)
        ja = (t0 - cross_hw(a, s_['road'])) if a in JUNC else None; jb = (L_ - t0 - BAYL - cross_hw(b, s_['road'])) if b in JUNC else None   # round 6: from the junction's edge
        near_ = (jb if sd == 1 else ja); far_ = (ja if sd == 1 else jb)
        st['bay_list'].append(dict(side=sd, dir=f"{da}→{db}", t0=round(t0), poly=poly, pole=P_(t0 + BAYL / 2, e_ + BAY['depth'] + 18),
                                   to_junction_m=round(min(x for x in (ja, jb) if x is not None) / 10, 1) if (ja is not None or jb is not None) else None,
                                   toward=N[db]['label'], near_m=round(near_ / 10, 1) if near_ is not None else None, far_m=round(far_ / 10, 1) if far_ is not None else None,
                                   relaxed=bool(RELAX.get((a, b, sd)))))
    st['seg'] = s_['id']; st['road'] = s_['road']
ENDS = []   # the end stops: a plaza or a turning circle at the end of a line (no bay — the bus stands there)
for line in P.ROUTES['bus']:
    for nd, nm in line.get('ends', []):
        st = next((x for x in ENDS if x['node'] == nd), None)
        if st is None: st = dict(node=nd, name=nm, lines=[], kind='end', at=[N[nd]['x'], N[nd]['y']], bay_list=[]); ENDS.append(st)
        st['lines'].append(line['id'])
STOPS += ENDS
for k_, st in enumerate(STOPS): st['id'] = f"ST-{k_ + 1:02d}"
# the bays against the rules: 15 m stop, 20 m from a junction, not on a crosswalk, a driveway, an apron or under the rail bridge
for st in STOPS:
    for bb in st.get('bay_list', []):
        sd = bb['side']; bl_ = blocks(st['a'], st['b'], sd); t0 = bb['t0']
        hit = [w for y0, y1, w in bl_ if t0 < y1 - 1 and t0 + BAYL > y0 + 1]
        if hit: stop_bad.append(f"{st['id']} {bb['dir']}: {hit}")
        if bb.get('relaxed'): continue                                               # listed in the check of the exceptions (R-46, D‑332)
        if (bb.get('near_m') is not None and bb['near_m'] < 20 - .01) or (bb.get('far_m') is not None and bb['far_m'] < 10 - .01): stop_bad.append(f"{st['id']} {bb['near_m']} / {bb['far_m']} מ׳ מקצה הצומת")
BUS_L, BUS_R = 135, 140   # px: the bus of 13.5 m and its turning radius of 14 m (the owner 23:46)
def term_layout():
    """the yard: a one-way loop (clockwise) around two platforms; on each side of a platform a bay lane of 3 bays of 16 m; a bypass in the
    middle so that a bus leaves its bay without waiting for the one in front; along the north edge a marked holding lane of 4 places for a
    bus that came early or late; the gate in the middle of the south edge, at the end of the terminal street (LC-E3). The ends of the yard
    are wider than 2 × 14 m, so a bus turns round at its radius."""
    x0, x1, y0, y1 = 4880, 5700, 1770, 2170
    bx0 = 5060; BL_ = 160
    rows = [('א', 1860, 1895, 'צפון'), ('א', 1925, 1960, 'דרום'), ('ב', 2030, 2065, 'צפון'), ('ב', 2095, 2130, 'דרום')]
    bays = []
    for pf, ya, yb, sd in rows:
        for k in range(3): bays.append(dict(no=len(bays) + 1, platform=pf, side=sd, rect=[bx0 + k * BL_, ya, bx0 + (k + 1) * BL_, yb]))
    hold = [dict(no=k + 1, rect=[5000 + k * 150, 1785, 5000 + (k + 1) * 150, 1820]) for k in range(4)]
    return dict(id='E3-BUS', label='מסוף האוטובוסים של E3 — 12 מפרצים ו-4 מקומות המתנה', rect=[x0, y0, x1, y1], node='E54_20', gate=[5400, 2170],
                platforms=[dict(id='א', rect=[bx0, 1895, bx0 + 3 * BL_, 1925]), dict(id='ב', rect=[bx0, 2065, bx0 + 3 * BL_, 2095])],
                bays=bays, hold=hold, corner_r=BUS_R, ends=[[x0, bx0], [bx0 + 3 * BL_, x1]])
TERM = term_layout()
tb = TERM['bays']; th = TERM['hold']
term_bad = []
if len(tb) < 2 * len(P.ROUTES['bus']): term_bad.append(f"{len(tb)} מפרצים, צריך {2 * len(P.ROUTES['bus'])}")
if any(b['rect'][2] - b['rect'][0] < BUS_L + 20 or b['rect'][3] - b['rect'][1] < 35 for b in tb): term_bad.append('מפרץ קצר או צר מאוטובוס של 13.5 מ׳')
if not th: term_bad.append('אין שטח המתנה')
if min(e_[1] - e_[0] for e_ in TERM['ends']) < BUS_R or (TERM['rect'][3] - TERM['rect'][1]) < 2 * BUS_R: term_bad.append('אין מקום לסיבוב ברדיוס 14 מ׳')
chk('מסוף E3 — לפחות 12 מפרצים (שניים לכל קו בבת אחת) ושטח המתנה מסומן; החצר לאוטובוס של 13.5 מ׳ וסיבוב ברדיוס 14 מ׳', not term_bad,
    f"{len(tb)} מפרצים של 16 × 3.5 מ׳ בשני רציפים (6 קווים × 2), מעקף באמצע, ו-{len(th)} מקומות המתנה של 15 מ׳ לאוטובוס שהגיע מוקדם או מאוחר; "
    f"החצר {(TERM['rect'][2] - TERM['rect'][0]) / 10:.0f} × {(TERM['rect'][3] - TERM['rect'][1]) / 10:.0f} מ׳, בקצוות {min(e_[1] - e_[0] for e_ in TERM['ends']) / 10:.0f} מ׳ ובגובה {(TERM['rect'][3] - TERM['rect'][1]) / 10:.0f} מ׳ — יותר מקוטר הסיבוב (28 מ׳); הכניסה והיציאה בשער אחד ברחוב המסוף." + (' בעיות: ' + '; '.join(term_bad) if term_bad else ''))
v_px = 42; LAYOVER = 30
for line in P.ROUTES['bus']:
    L_ = sum(SEGBY[frozenset((a, b))]['len_m'] * 10 for a, b in zip(line['path'], line['path'][1:]))
    closed = line['path'][0] == line['path'][-1]
    if closed: cyc = L_ / v_px + LAYOVER; runs = 2 if line['twoway'] else 1; buses = runs * math.ceil(cyc / line['headway_s'])
    else: cyc = 2 * L_ / v_px + 2 * LAYOVER; runs = 1; buses = math.ceil(cyc / line['headway_s'])
    line.update(len_km=round(L_ / 10000, 2), closed=closed, cycle_s=round(cyc), buses=buses,
                stop_ids=[],
                road_seq=[])
    for a, b in zip(line['path'], line['path'][1:]):
        r_ = SEGBY[frozenset((a, b))]['road']
        if not line['road_seq'] or line['road_seq'][-1] != r_: line['road_seq'].append(r_)
        for st in STOPS:   # the stops in the order the line meets them
            if line['id'] in st['lines'] and st['id'] not in line['stop_ids'] and ((st.get('kind') != 'end' and st['key'] == frozenset((a, b))) or (st.get('kind') == 'end' and st['node'] == b)):
                line['stop_ids'].append(st['id'])
    if not (line['path'][0] == 'E54_20'): stop_bad.append(f"קו {line['id']} לא יוצא מהמסוף")
nbus = sum(l_['buses'] for l_ in P.ROUTES['bus'])
EXC_TXT = ['%s (%s): %s / %s מ׳' % (st['id'], st['name'], bb['near_m'], bb['far_m']) for st in STOPS for bb in st.get('bay_list', []) if bb.get('relaxed')]
chk('R-46 — תחנות שאין להן מקום לפי הכלל (D‑332): 20 מ׳ מקצה הצומת שלפנים ו-10 מ׳ מקצה הצומת שמאחור — להחלטת הבעלים', not EXC_TXT,
    'אין.' if not EXC_TXT else 'הקטע קצר מדי בין שני צמתים, והמפרץ עומד לפי הכלל של סבב 5 (20 מ׳ ממרכז הצומת): ' + '; '.join(EXC_TXT) + '. האפשרויות: תחנה בלי מפרץ, או בקטע הסמוך בקו.')
chk('האוטובוסים — 6 קווים חדשים, כולם מהמסוף ב-E3; כל תחנה במפרץ של 15 מ׳ (ועוד כניסה ויציאה של 4 מ׳), 20 מ׳ מקצה הצומת שלפנים ו-10 מ׳ מקצה הצומת שמאחור (D‑332), לא על מעבר חצייה ולא מול כניסה',
    not stop_bad,
    f"{len(STOPS)} תחנות ({len(ENDS)} מהן תחנות סופיות ברחבה או במעגל סיבוב), {sum(len(st.get('bay_list', [])) for st in STOPS)} מפרצים, {len(XW)} מעברי חצייה בצמתים; הקרוב לצומת — "
    f"{min(bb['to_junction_m'] for st in STOPS for bb in st.get('bay_list', []) if bb['to_junction_m'] is not None):.1f} מ׳. "
    f"{nbus} אוטובוסים בכל הקווים לפי המרווחים (D‑243: 49 בקווים של היום)." + (' בעיות: ' + '; '.join(stop_bad) if stop_bad else ''))
for st in STOPS:
    if 'key' in st: st['key'] = sorted(st['key'])
    st.pop('bays', None)

# ---------------------------------------------------------------- 1.11 (R-36): lots in every zone, each with a road; the airport and the island
import plan7b_svg as SV
AIRF = CITY.airport(); ISLF = CITY.island(); USES_Z = CITY.zone_uses()
RAILS = CITY.rails(RAIL)
for st_ in CITY.STATIONS: pass
DETAILED = {i_['zone'] for i_ in SITES if not i_.get('r5')} - {'D5'}   # D5: the night depot takes one block; the rest of the zone gets lots · 1.11 round 5: the zones of r5 items keep their lots too
AIR_ZONES = {z for z in SV.ZN if SV.ZN[z][1] == 'air'}
def rects_hit(r, rs, pad=0): return any(min(r[2], q[2]) - max(r[0], q[0]) > pad and min(r[3], q[3]) - max(r[1], q[1]) > pad for q in rs)
OBST = []   # what a new lot may not cover
for s_ in SEG:
    hw = CLS[s_['cls']]['halfW'] + 8
    for m in range(len(s_['pts']) - 1): OBST.append(band(s_['pts'][m], s_['pts'][m + 1], hw) if s_['kind'] != 'bridge' else (0, 0, 0, 0))
for r_ in SITE_ROADS:
    for m in range(len(r_['pts']) - 1): OBST.append(band(r_['pts'][m], r_['pts'][m + 1], r_['hw'] + 5))
for i_ in SITES:
    if i_['kind'] == 'site': continue
    OBST.append(item_box(i_))
for st in STOPS:
    for bb in st.get('bay_list', []): xs_ = [q[0] for q in bb['poly']]; ys_ = [q[1] for q in bb['poly']]; OBST.append((min(xs_) - 30, min(ys_) - 30, max(xs_) + 30, max(ys_) + 30))
x0_, y0_, x1_, y1_ = TERM['rect']; OBST.append((x0_ - 20, y0_ - 20, x1_ + 20, y1_ + 20))
for rl in RAILS:
    p_ = rl['pts']
    for m in range(len(p_) - 1): OBST.append((min(p_[m][0], p_[m + 1][0]) - 70, min(p_[m][1], p_[m + 1][1]) - 70, max(p_[m][0], p_[m + 1][0]) + 70, max(p_[m][1], p_[m + 1][1]) + 70))
LBX = [(min(x for x, y in LAKE['pts']), min(y for x, y in LAKE['pts']), max(x for x, y in LAKE['pts']), max(y for x, y in LAKE['pts']))]
OBST += LBX
AIRPOLY = AIRF['fence']
def lot_ok(r):
    if r[2] - r[0] < 100 or r[3] - r[1] < 100: return False
    if rects_hit(r, OBST): return False
    for x, y in ((r[0] + 5, r[1] + 5), (r[2] - 5, r[1] + 5), (r[0] + 5, r[3] - 5), (r[2] - 5, r[3] - 5), ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)):
        if is_sea(x, y) or in_lake(x, y) or pip(x, y, AIRPOLY) or in_air(x, y): return False
    return True
DEFAULT_HE = {'home': 'מגרש מגורים', 'shop': 'מגרש מסחר ומשרדים', 'work': 'מגרש תעשייה', 'port': 'מגרש הנמל', 'rail': 'מגרש הרכבת', 'forest': 'יער',
              'fields': 'שדה', 'park': 'פארק', 'coast': 'החוף', 'public': 'מגרש ציבורי', 'sport': 'מגרש ספורט', 'air': 'מגרש השדה'}
LOTS = []; LOT_DW = []; lot_fail = []
JUNC_PTS = [(N[k]['x'], N[k]['y']) for k in JUNC]
def dw_spot(s_, side, t0, t1, used):
    """a driveway on segment s_ along [t0, t1] (px from a): ≥ 18 m from every junction, not on a bay, ≥ 8 m from another driveway"""
    pa, pb = s_['pts'][0], s_['pts'][-1]; L_ = math.hypot(pb[0] - pa[0], pb[1] - pa[1]); u = ((pb[0] - pa[0]) / L_, (pb[1] - pa[1]) / L_); r = (-u[1], u[0])
    hw = CLS[s_['cls']]['halfW']; mid = (t0 + t1) / 2; best = None
    bays = [(bb['t0'] - 40, bb['t0'] + BAYL + 40) for st in STOPS if st.get('seg') == s_['id'] for bb in st.get('bay_list', []) if bb['side'] * (1 if st['a'] == s_['a'] else -1) == side]
    t = t0 + 40
    while t <= t1 - 40:
        x, y = pa[0] + u[0] * t + r[0] * side * hw, pa[1] + u[1] * t + r[1] * side * hw
        if min(math.hypot(x - a, y - b) for a, b in JUNC_PTS) >= 185 and not any(a <= t <= b for a, b in bays) and all(math.hypot(x - a, y - b) >= 80 for a, b in used):
            if best is None or abs(t - mid) < abs(best[0] - mid): best = (t, x, y)
        t += 10
    return best
DW_PTS = [tuple(d['at']) for d in DWS]
ORDERC = {'local': 0, 'oneway': 1, 'collector': 2, 'arterial': 3, 'main': 4, 'track': 5}
for z in sorted(SV.ZN):
    kind = SV.ZN[z][1]
    if kind in ('sea', 'island', 'air') or z in DETAILED or z in ('F5', 'F6'): continue
    zx0, zy0, zx1, zy1 = zrect(z); Wl, Dl = [v * 10 for v in CITY.LOTSIZE.get(kind, (40, 40))]
    names = USES_Z.get(z, []) or [DEFAULT_HE.get(kind, 'מגרש')]; k_name = 0; made = 0
    segs_ = sorted([s_ for s_ in SEG if z in s_['zones'] and len(s_['pts']) == 2 and s_['kind'] != 'bridge' and (s_['cls'] != 'track' or kind in ('forest', 'fields'))],
                   key=lambda s_: (ORDERC[s_['cls']], -s_['len_m']))
    for s_ in segs_:
        pa, pb = s_['pts']; L_ = math.hypot(pb[0] - pa[0], pb[1] - pa[1]); u = ((pb[0] - pa[0]) / L_, (pb[1] - pa[1]) / L_)
        if abs(u[0]) > .01 and abs(u[1]) > .01: continue
        hw = CLS[s_['cls']]['halfW']; r = (-u[1], u[0])
        def clear(k):
            if k not in JUNC: return 0
            return max((CLS[t['cls']]['halfW'] for o, t in ADJ[k] if t is not s_), default=0) + 30
        ca, cb = clear(s_['a']), clear(s_['b'])
        for side in (1, -1):
            t = ca
            while t + 120 <= L_ - cb:
                w_ = min(Wl, L_ - cb - t)
                placed = False
                for dd in (Dl, Dl * .75, Dl * .5, 150):
                    c0 = (pa[0] + u[0] * t + r[0] * side * (hw + 12), pa[1] + u[1] * t + r[1] * side * (hw + 12))
                    c1 = (pa[0] + u[0] * (t + w_) + r[0] * side * (hw + 12 + dd), pa[1] + u[1] * (t + w_) + r[1] * side * (hw + 12 + dd))
                    rc = (max(min(c0[0], c1[0]), zx0), max(min(c0[1], c1[1]), zy0), min(max(c0[0], c1[0]), zx1), min(max(c0[1], c1[1]), zy1))
                    if lot_ok(rc):
                        sp = dw_spot(s_, side, t, t + w_, DW_PTS)
                        if not sp: break
                        tt, dx_, dy_ = sp; DW_PTS.append((dx_, dy_))
                        green = (z == 'B3' and s_['road'] == 'AR-NW')
                        nm = 'רצועה ירוקה — עצים וספסלים מול הפארק (D‑260)' if green else names[k_name % len(names)]
                        if not green: k_name += 1
                        made += 1
                        lid = f"{z}-{made:02d}"
                        inn = (pa[0] + u[0] * tt + r[0] * side * (hw + 12 + 60), pa[1] + u[1] * tt + r[1] * side * (hw + 12 + 60))
                        cwh = CW(s_['cls']) / 2 - 3; st_in = [round(pa[0] + u[0] * tt + r[0] * side * cwh, 1), round(pa[1] + u[1] * tt + r[1] * side * cwh, 1)]
                        LOTS.append(dict(id=lid, zone=z, kind='lot', use='park' if green else kind, label=nm, rect=[round(v, 1) for v in rc], future=True, front=s_['road'], dw=f"DW-{lid}"))
                        LOT_DW.append(dict(zone=z, id=f"DW-{lid}", road=s_['road'], at=[round(dx_, 1), round(dy_, 1)], label=f"הכניסה ל{nm}", why='הנמכת שפה מהדרך שמול המגרש — לא צומת.',
                                           to=None, lanes='1+1', to_junction_m=round(min(math.hypot(dx_ - a, dy_ - b) for a, b in JUNC_PTS) / 10, 1)))
                        SITE_ROADS.append(dict(id=f"DW-{lid}", zone=z, kind='driveway', cls='driveway', lanes='1+1', hw=30, pts=[[round(dx_, 1), round(dy_, 1)], [round(inn[0], 1), round(inn[1], 1)]],
                                               draw=[st_in, [round(inn[0], 1), round(inn[1], 1)]], label=f"הכניסה ל{nm}", road=s_['road'], oneway=False))
                        OBST.append(tuple(rc)); placed = True; break
                t += (w_ + 20) if placed else 60
    if not made and not any(i_.get('r5') and i_['zone'] == z for i_ in SITES): lot_fail.append(z)   # 1.11 round 5: a zone filled by its own items
# the airport and the island: their lots, their roads
AIR_LOTS = AIRF['lots']; ISL_LOTS = ISLF['lots']
AIR_ROADS = []
for r_ in AIRF['roads']:
    AIR_ROADS.append(dict(r_, cls=r_.get('cls', 'airland'), hw=CLS[r_['cls']]['halfW'] if r_.get('cls') in CLS else 59.0))
for r_ in ISLF['roads']:
    hw = CLS[r_['cls']]['halfW'] if r_['cls'] in CLS else 19.5
    SITE_ROADS.append(dict(id=r_['id'], zone=CITY.zone_of_pt(*r_['pts'][0]), kind='site', cls=r_['cls'], lanes='1+1' if r_['cls'] == 'local' else '1', hw=hw, pts=r_['pts'], label=r_['label'], road=None, via='IS-W', oneway=False, future=True))
# the access of every lot of the city: its own driveway, an inner road, or the car park / yard / apron next to it
CONN = []   # (rects, network road it reaches, what)
for r_ in SITE_ROADS:
    rs = [band(r_['pts'][m], r_['pts'][m + 1], r_['hw']) for m in range(len(r_['pts']) - 1)]
    try: rd_ = reach(r_)
    except Exception: rd_ = r_.get('road') or r_.get('via')
    CONN.append((rs, rd_, r_['id'], r_['label']))
for r_ in AIR_ROADS: CONN.append(([band(r_['pts'][m], r_['pts'][m + 1], r_['hw']) for m in range(len(r_['pts']) - 1)], 'AR-N' if 'PAX' in r_['id'] else ('CL-AC' if 'CARGO' in r_['id'] else 'CL-F'), r_['id'], r_['label']))
AIRSIDE_SVC = [(sv_['rect'], sv_['id'], sv_['label']) for sv_ in AIRF['service']]
for s_ in SEG:   # a lot on the frontage of a road (the airport and the island: the plan's own lots)
    hw = CLS[s_['cls']]['halfW']; CONN.append(([band(s_['pts'][m], s_['pts'][m + 1], hw) for m in range(len(s_['pts']) - 1)], s_['road'], s_['road'], RDN[s_['road']]['name']))
ALL_LOTS = [i_ for i_ in SITES if i_['kind'] in ('building', 'parking', 'yard', 'court', 'field', 'lot')] + LOTS + \
           [l_ for l_ in AIR_LOTS if l_['kind'] in ('building', 'parking', 'yard')] + [l_ for l_ in ISL_LOTS if l_['kind'] in ('building', 'parking', 'yard', 'park', 'beach', 'pad')]
ACC2 = {}
for i_ in ALL_LOTS:
    if i_.get('apron') and i_.get('road'): ACC2[i_['id']] = dict(road=i_['road'], via=i_['id'], through=None); continue
    if i_.get('dw'): ACC2[i_['id']] = dict(road=i_['front'], via=i_['dw'], through=None); continue
    if i_['id'] in ACC: ACC2[i_['id']] = ACC[i_['id']]; continue
    R_ = tuple(i_['rect']); lim = 20 if i_['kind'] in ('building', 'parking', 'yard') else 60; best = None
    for rs, rd_, wid, lab in CONN:
        g_ = min(rgap(R_, q) for q in rs)
        if g_ <= lim and (best is None or g_ < best[0]): best = (g_, rd_, wid)
    if i_.get('airside'):
        for rr, wid, lab in AIRSIDE_SVC:
            g_ = rgap(R_, tuple(rr))
            if g_ <= lim and (best is None or g_ < best[0]): best = (g_, 'AIRSIDE', wid)
    if best: ACC2[i_['id']] = dict(road=best[1], via=best[2], through=None)
for _ in range(4):
    for i_ in ALL_LOTS:
        if i_['id'] in ACC2: continue
        for j_ in ALL_LOTS:
            if j_['id'] in ACC2 and j_['zone'] == i_['zone'] and j_['kind'] in ('parking', 'yard') and rgap(tuple(i_['rect']), tuple(j_['rect'])) <= 60:
                ACC2[i_['id']] = dict(ACC2[j_['id']], through=j_['id']); break
for i_ in ALL_LOTS:
    if i_['id'] in ACC2:
        a_ = ACC2[i_['id']]; i_['access'] = dict(a_, road_name=RDN[a_['road']]['name'] if a_['road'] in RDN else ('שבילי השירות של הצד האווירי' if a_['road'] == 'AIRSIDE' else str(a_['road'])))
no_acc = [i_['id'] for i_ in ALL_LOTS if i_['id'] not in ACC2]
LAND_Z = [z for z in SV.ZN if SV.ZN[z][1] not in ('sea',) and z not in ('F5', 'F6')]
def zones_of_rect(r): return {z for z in SV.ZN if min(r[2], zrect(z)[2]) - max(r[0], zrect(z)[0]) > 50 and min(r[3], zrect(z)[3]) - max(r[1], zrect(z)[1]) > 50}
lot_zones = {i_['zone'] for i_ in ALL_LOTS} | {i_['zone'] for i_ in SITES} | {z for l_ in AIR_LOTS + ISL_LOTS for z in zones_of_rect(l_['rect'])}
no_lot = [z for z in LAND_Z if z not in lot_zones]
chk('הגישה — לכל מגרש בעיר (מבנה, חניון, חצר ומגרש בכל האזורים, בשדה ובאי) יש דרך שמגיעה אליו', not no_acc,
    f"{len(ALL_LOTS)} מגרשים: {sum(1 for a_ in ACC2.values() if not a_['through'])} עם כניסה או חזית משלהם, {sum(1 for a_ in ACC2.values() if a_['through'])} דרך החניון או החצר שלידם; "
    f"{len(no_acc)} בלי גישה." + (f" בלי גישה: {no_acc}" if no_acc else '') + " בצד האווירי של השדה — דרך שבילי השירות שבתוך הגדר.")
lot_bad = [l_['id'] for l_ in LOTS if not lot_ok_final(l_)] if False else []
dw_near = [d['id'] for d in LOT_DW if d['to_junction_m'] < 18]
chk('המגרשים — יש מגרשים בכל אזור יבשה, וכל מגרש חדש פונה לדרך: כניסה (הנמכת שפה) לפחות 18 מ׳ מצומת, לא על מפרץ של אוטובוס, בלי חפיפה עם דרך, מסילה, מגרש אחר, הים או האגם',
    not no_lot and not lot_fail and not dw_near,
    f"{len(LOTS)} מגרשים חדשים ב-{len({l_['zone'] for l_ in LOTS})} אזורים, ועוד {len(SITES)} פריטים באזורים המפורטים, {len(AIR_LOTS)} בשדה העתידי ו-{len(ISL_LOTS)} באי; "
    f"{len(LAND_Z)} אזורי יבשה — {len(LAND_Z) - len(no_lot)} עם מגרשים. הכניסה הקרובה ביותר לצומת: {min(d['to_junction_m'] for d in LOT_DW):.1f} מ׳."
    + (f" בלי מגרשים: {no_lot}" if no_lot else '') + (f" אזורים בלי מקום: {lot_fail}" if lot_fail else ''))
# ---------------------------------------------------------------- 1.11 00:35 (the owner): A2, A3, A4 — every building, court, field, car
# park and pad has a way in for vehicles (a road, a service lane for the emergency vehicles, an apron or the car park next to it) and a
# way in for people (the sidewalk next to it, the car park next to it, or a path from the sidewalk / the car park to it) — each one apart
def gap_item(i_, rect_):
    if i_['kind'] == 'pad':
        (cx, cy), sf = i_['c'], i_['safety']
        dx = max(rect_[0] - cx, 0, cx - rect_[2]); dy = max(rect_[1] - cy, 0, cy - rect_[3]); return max(0, math.hypot(dx, dy) - sf)
    return rgap(tuple(i_['rect']), tuple(rect_))
def gap_poly_item(i_, pts_, hw_):
    return min(gap_item(i_, band(pts_[m], pts_[m + 1], hw_)) for m in range(len(pts_) - 1))
ROAD_BANDS = [band(s_['pts'][m], s_['pts'][m + 1], CLS[s_['cls']]['halfW']) for s_ in SEG if s_['kind'] != 'bridge' for m in range(len(s_['pts']) - 1)]
# 1.11 round 6 (R-42): the zones already built in the game (B4, B3) are measured against the roads at the game's widths — the column 'game'
# of road_sections.json (D‑315) — and their numbers are the zone files' (b4v4.json, b3v5.json)
R6_GAME_HW = {'AR-C': CLS['collector']['game']['halfW_px']}   # D‑318: R-CENTER is an avenue in the game until S4 (the avenue's section)
def hw_game(s_): return R6_GAME_HW.get(s_['road']) or (CLS[s_['cls']]['game']['halfW_px'] if CLS[s_['cls']].get('game') else CLS[s_['cls']]['halfW'])
GAME_BANDS = [(s_['road'], band(s_['pts'][m], s_['pts'][m + 1], hw_game(s_)))
              for s_ in SEG if s_['kind'] != 'bridge' and set(s_.get('zones', [])) & {'B3', 'B4'} for m in range(len(s_['pts']) - 1)]
R6 = [i_ for i_ in SITES if i_.get('r6') and i_['kind'] in ('building', 'house', 'lot', 'parking', 'park', 'yard', 'court')]
r6_bad = []
for i_ in R6:
    r_ = i_['rect']
    for rid_, b_ in GAME_BANDS:
        if min(r_[2], b_[2]) - max(r_[0], b_[0]) > 1 and min(r_[3], b_[3]) - max(r_[1], b_[1]) > 1: r6_bad.append(i_['id'] + '×' + rid_)
n4 = sum(i_.get('stalls', 0) for i_ in SITES if i_['zone'] == 'B4' and i_['kind'] == 'parking'); n3 = sum(i_.get('stalls', 0) for i_ in SITES if i_['zone'] == 'B3' and i_['kind'] == 'parking')
mk = next((i_ for i_ in SITES if i_['id'] == 'B4-S1'), None); pk = next((i_ for i_ in SITES if i_['id'] == 'B4-PK'), None)
sch = [i_['id'] for i_ in SITES if i_['zone'] == 'B3' and ('SCHOOL' in i_['id'] or 'בית ספר' in i_['label'])]
chk('האזורים שנבנו במשחק (B4, ‏B3) — במפה כמו במשחק, ברוחב הדרכים של המשחק (R-42, ‏D‑315)',
    not r6_bad and n4 == len(Z6.B4['stalls']) and mk and pk and mk['rect'][1] < pk['rect'][1] and not sch and sum(1 for i_ in SITES if i_['zone'] == 'B3' and i_['kind'] == 'house') == 15,
    f"המגרשים נקראים מהקבצים של האזורים (b4v5.json, ‏b3v5.json) — אותו מקור כמו הגיליון והמשחק. ב-B4: ‏{n4} חניות במשחק ובמפה, הסופר בצפון ({mk['rect'][1] if mk else '—'}) והחניון בדרום ({pk['rect'][1] if pk else '—'}); "
    f"ב-B3: ‏{sum(1 for i_ in SITES if i_['zone'] == 'B3' and i_['kind'] == 'house')} בתים, {n3} חניות בחצרות של הבניינים ועוד חניה בכל שביל רכב, בלי בית ספר (D‑325) ובלי עמדת שירות (D‑326). "
    f"{len(R6)} פריטים נבדקו מול {len(GAME_BANDS)} קטעי כביש ברוחב של המשחק (טבלת החתכים, העמודה 'במשחק היום'): {len(r6_bad)} חפיפות" + (' — ' + ', '.join(r6_bad[:6]) if r6_bad else '') + '.')
WALK_SR = [r_ for r_ in SITE_ROADS if r_['kind'] == 'site' and r_.get('cls') in CLS and CLS[r_['cls']]['walk_m'] > 0]   # the inner roads with a sidewalk
ROAD_BANDS += [band(r_['pts'][m], r_['pts'][m + 1], r_['hw']) for r_ in WALK_SR for m in range(len(r_['pts']) - 1)]
PATHS = [i_ for i_ in SITES if i_['kind'] == 'path']
def path_ok(pt_):   # a path that reaches a sidewalk, a car park, or another path that does
    return any(gap_poly_item(dict(kind='x', rect=b_), pt_['rect'], pt_['hw']) <= 20 for b_ in ROAD_BANDS) or \
           any(o_['kind'] == 'parking' and gap_poly_item(o_, pt_['rect'], pt_['hw']) <= 20 for o_ in SITES)
LIVE = {pt_['id'] for pt_ in PATHS if path_ok(pt_)}
for _ in range(4):
    for pt_ in PATHS:
        if pt_['id'] in LIVE: continue
        for q_ in PATHS:
            if q_['id'] in LIVE and any(min(dseg(x_, y_, *q_['rect'][m], *q_['rect'][m + 1])[0] for m in range(len(q_['rect']) - 1)) <= q_['hw'] + pt_['hw'] + 5 for x_, y_ in pt_['rect']):
                LIVE.add(pt_['id']); break
ACC_AZ = []
for i_ in SITES:
    if i_['zone'] not in ('A2', 'A3', 'A4') or i_['kind'] in ('site', 'path', 'house'): continue
    veh = None; ped = None
    for s_ in SEG:
        if s_['kind'] == 'bridge': continue
        if gap_poly_item(i_, s_['pts'], CLS[s_['cls']]['halfW']) <= 60: veh = veh or RDN[s_['road']]['name']; ped = ped or ('המדרכה של ' + RDN[s_['road']]['name'] if gap_poly_item(i_, s_['pts'], CLS[s_['cls']]['halfW']) <= 20 else None)
    for r_ in SITE_ROADS:
        if gap_poly_item(i_, r_['pts'], r_['hw']) <= 60: veh = veh or r_['label']
        if r_ in WALK_SR and gap_poly_item(i_, r_['pts'], r_['hw']) <= 20: ped = ped or 'המדרכה של ' + r_['label'].split(' — ')[0]
    for o_ in SITES:
        if o_ is i_ or o_['zone'] != i_['zone']: continue
        if o_.get('apron') and gap_item(i_, o_['rect']) <= 20: veh = veh or o_['label']; ped = ped or o_['label']
        if o_['kind'] == 'parking' and gap_item(i_, o_['rect']) <= 60: veh = veh or o_['label']
        if o_['kind'] == 'parking' and gap_item(i_, o_['rect']) <= 20: ped = ped or o_['label']
    if i_.get('apron') or i_['kind'] == 'parking': veh = veh or 'בתוך המגרש'
    for pt_ in PATHS:
        if pt_['id'] in LIVE and gap_poly_item(i_, pt_['rect'], pt_['hw']) <= 10: ped = ped or pt_['label']
    ACC_AZ.append(dict(id=i_['id'], zone=i_['zone'], label=i_['label'], vehicle=veh, walk=ped))
az_bad = [f"{a_['id']} ({'רכב' if not a_['vehicle'] else ''}{' ו' if not a_['vehicle'] and not a_['walk'] else ''}{'הולך רגל' if not a_['walk'] else ''})" for a_ in ACC_AZ if not a_['vehicle'] or not a_['walk']]
p_dead = [pt_['id'] for pt_ in PATHS if pt_['id'] not in LIVE]
chk('הגישה ב-A2, A3 ו-A4 — לכל מבנה, מגרש ספורט, חניון ומנחת: דרך לרכב (כביש, דרך שירות לחירום, רחבה או החניון שלידו) ושביל להולך רגל (מהמדרכה או מהחניון)',
    not az_bad and not p_dead,
    f"{len(ACC_AZ)} פריטים, כל אחד נבדק לרכב ולהולך רגל: " + '; '.join(f"{a_['id']} — רכב: {a_['vehicle']}, הולך רגל: {a_['walk']}" for a_ in ACC_AZ) +
    f". {len(PATHS)} שבילים, כולם מחוברים למדרכה או לחניון." + (f" חסר: {az_bad}" if az_bad else '') + (f" שביל מנותק: {p_dead}" if p_dead else ''))
# the villas of C3 and D3: every villa on its own lot, with its own way in from a real road
VIL = [i_ for i_ in SITES if i_['kind'] == 'lot' and i_['zone'] in ('C3', 'D3') and (i_['id'][2:4] == '-V' or i_['id'] == 'C3-PH')]
vil_txt = []; vil_bad = []
for v_ in VIL:
    a_ = ACC.get(v_['id'])
    own = a_ and a_['through'] is None and (str(a_['via']).startswith('DW-' + v_['id']) or a_['via'] in (v_['id'] + '-IN', 'C3-PH-GATE'))
    if own: vil_txt.append(f"{v_['id']} ← {a_['via']} ({RDN[a_['road']]['name']})")
    else: vil_bad.append(v_['id'])
chk('הווילות של C3 ו-D3 — לכל וילה מגרש עם גבול וכניסה משלה מכביש אמיתי', len(VIL) == 12 and not vil_bad,
    f"{len(VIL)} מגרשים (5 וילות ובית השחקן ב-C3, 6 וילות ב-D3): " + '; '.join(vil_txt) + '.' + (f" בלי כניסה משלה: {vil_bad}" if vil_bad else ''))

# ---------------------------------------------------------------- 1.11 00:21 (the owner): the rails — every line end to end, the
# number of tracks of every section as the plan says, and every crossing with a road (a barrier or a bridge)
def d_poly(q, p):
    best = 1e9
    for m in range(len(p) - 1):
        (ax, ay), (bx, by) = p[m], p[m + 1]; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy or 1
        t = max(0, min(1, ((q[0] - ax) * dx + (q[1] - ay) * dy) / L2)); best = min(best, math.hypot(q[0] - ax - t * dx, q[1] - ay - t * dy))
    return best
RLB = {r_['id']: r_ for r_ in RAILS}
r_bad = []
for r_ in RAILS:
    for k_, (kind_, what_) in zip((0, -1), r_['ends']):
        q_ = r_['pts'][k_]
        if kind_ == 'join':
            if what_ not in RLB or d_poly(q_, RLB[what_]['pts']) > 3: r_bad.append(f"{r_['id']} — הקצה ב-({q_[0]:.0f}, {q_[1]:.0f}) לא על {what_}")
        elif kind_ == 'edge':
            if q_[0] < 9600: r_bad.append(f"{r_['id']} — 'יוצאת מהעולם' לפני קצה המפה")
        elif not what_: r_bad.append(f"{r_['id']} — קצה בלי סימון")
n_buf = sum(1 for r_ in RAILS for k_, w_ in r_['ends'] if k_ in ('buffer', 'door'))
# the tracks of every section, by a probe across it (the plan: Rail–Air 2, the station 3 with the bypass, the yard 6, the port 3, the bridge 2)
TA_ = D['TRACK_A']; mi_ = len(TA_) // 2; (ax_, ay_), (bx_, by_) = TA_[mi_ - 1], TA_[mi_ + 1]; l_ = math.hypot(bx_ - ax_, by_ - ay_)
nx_, ny_ = -(by_ - ay_) / l_, (bx_ - ax_) / l_; cx_, cy_ = TA_[mi_]
SA_ = D['STATION_A'][0]; PB_ = D['P_b1']; dx_, dy_ = SA_[0] - PB_[0], SA_[1] - PB_[1]; l2_ = math.hypot(dx_, dy_); mx_, my_ = (SA_[0] + PB_[0]) / 2, (SA_[1] + PB_[1]) / 2
PROBES = [('רכבת–אוויר — מסוף המטען (y 1000)', [[5600, 1000], [6200, 1000]], 2),
          ('התחנה המרכזית E3 (y 2000) — 2 פסים ראשיים ומסילת העקיפה', [[5600, 2000], [6200, 2000]], 3),
          ('תחנת החוף (y 3050)', [[5600, 3050], [6200, 3050]], 3),
          ('חצר הרכבות E5 (y 4000) — 3 פסי חצר, 2 ראשיים והעקיפה', [[5600, 4000], [6200, 4000]], 6),
          ('הנמל — C6 (x 3000): P1, W1, W2', [[3000, 5040], [3000, 5195]], 3),
          ('הנמל — E6 (x 5000): P2, W1, W2', [[5000, 5040], [5000, 5195]], 3),
          ('הגשר לאי — ה-S', [[cx_ - nx_ * 150, cy_ - ny_ * 150], [cx_ + nx_ * 150, cy_ + ny_ * 150]], 2),
          ('הגשר לאי — הסיפון המשותף', [[mx_ + dy_ / l2_ * 150, my_ - dx_ / l2_ * 150], [mx_ - dy_ / l2_ * 150, my_ + dx_ / l2_ * 150]], 2),
          ('מסילת בית הזיקוק (y 4500)', [[2700, 4500], [2860, 4500]], 1),
          ('מסילת הנמל המזרחית (x 8500)', [[8500, 4950], [8500, 5300]], 1)]
SECTIONS = []
for nm_, pr_, want_ in PROBES:
    hit_ = sorted({r_['id'] for r_ in RAILS for m in range(len(r_['pts']) - 1) if seg_x(pr_[0], pr_[1], r_['pts'][m], r_['pts'][m + 1])})
    SECTIONS.append(dict(name=nm_, want=want_, got=len(hit_), lines=hit_))
sec_bad = [f"{x_['name']}: {x_['got']} במקום {x_['want']} ({', '.join(x_['lines'])})" for x_ in SECTIONS if x_['got'] != x_['want']]
# every crossing of a road (the network, the inner roads, the airport and the island) and a track is listed — a barrier or a bridge
ROADS_ALL = [(s_['id'], s_['pts']) for s_ in SEG if s_['kind'] != 'bridge'] + [(r_['id'], r_['pts']) for r_ in AIR_ROADS] + [(r_['id'], r_['pts']) for r_ in SITE_ROADS]
XR = []
for rid_, rp_ in ROADS_ALL:
    for r_ in RAILS:
        for m in range(len(rp_) - 1):
            for k in range(len(r_['pts']) - 1):
                q_ = seg_x(rp_[m], rp_[m + 1], r_['pts'][k], r_['pts'][k + 1])
                if q_: XR.append((rid_, r_['id'], round(q_[0]), round(q_[1])))
XR = sorted(set(XR))
xr_unl = []
for c_ in P.CROSS: c_['pts'] = []
for rid_, rl_, x_, y_ in XR:
    c_ = next((c_ for c_ in P.CROSS if rl_ in c_['rail'] and math.hypot(x_ - c_['at'][0], y_ - c_['at'][1]) < 150), None)
    if c_: c_['pts'].append([x_, y_, rl_, rid_])
    else: xr_unl.append(f"{rid_} × {rl_} ({x_}, {y_})")
x_empty = [c_['id'] for c_ in P.CROSS if not c_['pts']]
# a track does not run through a lot, a building or a yard of the plan (the stations and the rail yards are the rail's own)
RAILKIND = {'rail', 'station', 'track'}
r_lot = []
for i_ in ALL_LOTS + SITES:
    if i_.get('kind') in RAILKIND or i_.get('rail_ok') or not i_.get('rect') or len(i_['rect']) != 4 or not all(isinstance(v_, (int, float)) for v_ in i_['rect']): continue
    x0_, y0_, x1_, y1_ = i_['rect']
    for r_ in RAILS:
        p_ = r_['pts']
        if any(seg_x(p_[m], p_[m + 1], a_, b_) or (x0_ + 2 < p_[m][0] < x1_ - 2 and y0_ + 2 < p_[m][1] < y1_ - 2)
               for m in range(len(p_) - 1) for a_, b_ in (((x0_ + 2, y0_ + 2), (x1_ - 2, y0_ + 2)), ((x1_ - 2, y0_ + 2), (x1_ - 2, y1_ - 2)), ((x1_ - 2, y1_ - 2), (x0_ + 2, y1_ - 2)), ((x0_ + 2, y1_ - 2), (x0_ + 2, y0_ + 2)))):
            r_lot.append(f"{r_['id']} × {i_['id']}"); break
KM_ = sum(math.hypot(r_['pts'][m + 1][0] - r_['pts'][m][0], r_['pts'][m + 1][1] - r_['pts'][m][1]) for r_ in RAILS for m in range(len(r_['pts']) - 1)) / 10000
chk('המסילות — כל מסילה ברצף, מספר הפסים בכל קטע לפי התוכנית, וכל חצייה עם כביש רשומה (מחסום או גשר)',
    not r_bad and not sec_bad and not xr_unl and not x_empty and not r_lot,
    f"{len(RAILS)} מסילות ({KM_:.1f} ק\"מ): כל קצה נגמר על מסילה אחרת (מסוט), בבולמים או בדלת המוסך ({n_buf}), או ביציאה מהמפה (1) — אין קצה פתוח. "
    + 'הפסים: ' + '; '.join(f"{x_['name']} — {x_['got']}" for x_ in SECTIONS) + '. '
    + f"{len(XR)} חציות של כביש ומסילה, כולן ב-{len(P.CROSS)} המעברים הרשומים: "
    + ', '.join(f"{c_['id']} ({'מחסום' if c_['kind'] == 'level' else 'גשר רכבת מעל הכביש'}, {len(c_['pts'])})" for c_ in P.CROSS) + '. אף מסילה לא עוברת דרך מגרש.'
    + (f" לא ברצף: {r_bad}" if r_bad else '') + (f" פסים: {sec_bad}" if sec_bad else '') + (f" חציות לא רשומות: {xr_unl}" if xr_unl else '')
    + (f" מעבר רשום בלי חצייה: {x_empty}" if x_empty else '') + (f" דרך מגרש: {r_lot}" if r_lot else ''))
PAX = CITY.pax_line()

# the sidewalks: every road has one, except a dirt track (and a driveway or a service lane inside a lot, which are not roads)
nowalk = [c for c in CLS if c not in ('track',) and CLS[c]['walk_m'] <= 0] + [r_['id'] for r_ in SITE_ROADS if r_['kind'] == 'site' and r_.get('cls') in CLS and r_['cls'] != 'track' and CLS[r_['cls']]['walk_m'] <= 0]
chk('המדרכות — לכל כביש יש מדרכה, חוץ מדרך עפר', not nowalk,
    f"כל {len(SEG)} הקטעים ברשת ו-{len([r_ for r_ in SITE_ROADS if r_['kind'] == 'site' and r_.get('cls') in CLS])} הדרכים הפנימיות: מדרכה בכל סוג — "
    + ', '.join(f"{CLS[c]['he']} {CLS[c]['walk_m']} מ׳" for c in ('main', 'arterial', 'collector', 'local', 'oneway')) +
    f"; דרך עפר — בלי. שבילי שירות וכניסות בתוך מגרש ({len([r_ for r_ in SITE_ROADS if r_['kind'] != 'site' or r_.get('cls') not in CLS])}) — לא כבישים." + (f" בלי מדרכה: {nowalk}" if nowalk else ''))
# the main axis 3+3
mainS = [s_ for s_ in SEG if s_['cls'] == 'main']; mroads = sorted({s_['road'] for s_ in mainS})
ok3 = bool(mainS) and abs(CLS['main']['width_m'] - 30.4) < .05 and CLS['main']['dirN'] == 3
seen_ = {'AP1'}; st_ = ['AP1']
while st_:
    x_ = st_.pop()
    for o, s_ in ADJ[x_]:
        if s_['cls'] == 'main' and o not in seen_: seen_.add(o); st_.append(o)
chk('העורק הראשי 3+3 — הציר משער הנוסעים של השדה אל המרכז ואל הנמל, ברצף, בחתך של 30.4 מ׳', ok3 and {'J25_16', 'J46_42'} <= seen_,
    f"{', '.join(RDN[r_]['name'] + ' (' + r_ + ')' for r_ in mroads)}: {sum(s_['len_m'] for s_ in mainS) / 1000:.2f} ק\"מ, מ-AP1 עד שדרת המרכז (J25_16) ועד שער הנמל המזרחי (J46_42); "
    f"מדרכה 2.5 · 3 נתיבים של 3.9 · חציון 2.0 · 3 נתיבים של 3.9 · מדרכה 2.5 = {CLS['main']['width_m']} מ׳.")
# 1.11 00:44 (the owner): the road to the terminal — from the avenue to the terminal and back, never under 2 lanes in the direction of
# travel; every drop in lanes only at a marked place (a taper), never at a junction
AIRR = {r_['id']: r_ for r_ in AIR_ROADS}; SEGI = {s_['id']: s_ for s_ in SEG}
def lanes_dir(kind_, id_):
    if kind_ == 'seg': c_ = CLS[SEGI[id_]['cls']]; return c_['dirN'] if c_['twoway'] else c_['laneN']
    r_ = AIRR[id_]; return (r_['lanes'] if r_['oneway'] else (CLS[r_['cls']]['dirN'] if r_.get('cls') in CLS else r_['lanes'] // 2))
TR_IN = [('seg', 'AR-N/3', 'שדרת השדה'), ('seg', 'AR-N/4', 'שדרת השדה — עד השער'), ('air', 'AIR-PAX', 'דרך הנוסעים, מתחת לגשר הרכבת'), ('air', 'AIR-ACCESS', 'כביש הגישה'), ('air', 'AIR-FRONT', 'חזית הטרמינל')]
TR_OUT = [('air', 'AIR-CONN', 'המחבר'), ('air', 'AIR-SOUTH', 'דרך החזרה'), ('seg', 'CL-F/2', 'דרך המרינה והטרמינל'), ('air', 'AIR-ACCESS', 'כביש הגישה (עד דרך הנוסעים)'), ('air', 'AIR-PAX', 'דרך הנוסעים — מערבה'), ('seg', 'AR-N/4', 'שדרת השדה')]
tr_low = []; tr_drop = []
for nm_, path_ in (('הלוך', TR_IN), ('חזור', TR_OUT)):
    ln_ = [lanes_dir(k_, i_) for k_, i_, h_ in path_]
    tr_low += [f"{nm_}: {h_} — {l_}" for (k_, i_, h_), l_ in zip(path_, ln_) if l_ < 2]
    for (a_, b_) in zip(range(len(path_)), range(1, len(path_))):
        if ln_[b_] < ln_[a_] and not (path_[b_][1] == 'AIR-PAX' and AIRR['AIR-PAX'].get('taper')): tr_drop.append(f"{nm_}: {path_[a_][2]} → {path_[b_][2]} ({ln_[a_]} → {ln_[b_]})")
TERM_ROUTE = dict(inbound=[(h_, lanes_dir(k_, i_)) for k_, i_, h_ in TR_IN], outbound=[(h_, lanes_dir(k_, i_)) for k_, i_, h_ in TR_OUT], taper=AIRR['AIR-PAX'].get('taper'))
tp_ = AIRR['AIR-PAX'].get('taper') or {}
tp_j = [n_ for n_ in N if 4600 < N[n_]['x'] <= 5450 and abs(N[n_]['y'] - 1600) < 5 and N[n_]['kind'] not in ('gate',)]
chk('הדרך לטרמינל — משדרת השדה (3+3) עד הטרמינל ובחזרה, אף פעם לא פחות מ-2 נתיבים בכיוון הנסיעה; כל ירידה בנתיבים רק במקום מסומן ולא בצומת',
    not tr_low and not tr_drop and bool(tp_) and not tp_j,
    'הלוך: ' + ' → '.join(f"{h_} {l_}" for h_, l_ in TERM_ROUTE['inbound']) + '; חזור: ' + ' → '.join(f"{h_} {l_}" for h_, l_ in TERM_ROUTE['outbound']) +
    f". הירידה מ-3 ל-2 — אחת, בהצרה מסומנת אחרי שער הנוסעים (x {tp_.get('x0')}–{tp_.get('x1')}, {(tp_.get('x1', 0) - tp_.get('x0', 0)) / 10:.0f} מ׳: הנתיב הימני נגמר, חיצי מיזוג וקווים אלכסוניים); "
    "בכיוון החזרה הנתיב השלישי מתחיל בשער — תוספת ולא ירידה. אין צומת באזור ההצרה." + (f" מתחת ל-2: {tr_low}" if tr_low else '') + (f" ירידה לא מסומנת: {tr_drop}" if tr_drop else '') + (f" צומת בהצרה: {tp_j}" if tp_j else ''))

QUEST = [
    dict(n=1, q='המנחת והמגדלור באי עומדים צפונית-מזרחית למסילה, והרציף (1,000 px) תופס את כל האלכסון — כביש אליהם חייב לחצות את הרציף. ההמלצה: שביל וגשר הולכי רגל מרחבת התחנה (≤ 80 מ׳), בלי כביש; החלופה: להזיז את הרציף 60 מ׳ דרום-מזרחה ולשים מחסום בקצה הצפוני.', default='ההמלצה'),
    dict(n=2, q='העורק המזרחי על x 4600 ולא על הגבול D/E (4800): תור הבדיקה של השדה מתחיל ב-x 4719 (חלק א), וצומת על 4800 היה עומד בתוך התור. בסדר?', default='כן'),
    dict(n=3, q='אין יותר דרך בין B3 ל-B4 (כמו R-MID היום): השכונה מקבלת רחוב שקט אחד (LC-B), ימינה בלבד משדרת השדה ומכיכר הספורט דרך רחוב בית הספר — כך היא לא קיצור דרך. בסדר?', default='כן'),
    dict(n=4, q='שלב S1 (B4) בונה איתו גם את שדרת המרכז בין שדרת השדה לרחוב התעשייה, כי היא החזית המזרחית של B4; היא מחליפה את R-CENTER על אותו קו (10 px מערבה). החלופה: R-CENTER נשאר עד S5, ועוד שלושה חיבורים זמניים.', default='לבנות עם B4'),
    dict(n=6, q='כיכרות: למשחק אין היום כיכר (במנוע התנועה של המשחק אין מופע של כיכר). עד טלאי הכיכר (כניסה עם זכות קדימה, טבעת של נתיב אחד, רדיוס כ-15 מ׳ — כ-4 שע׳) הכיכרות עובדות כעצור לכל הכיוונים. הטלאי — עם השלב הראשון שבונה כיכר (S1, כיכר הספורט).', default='עצור לכל הכיוונים ב-S1, הטלאי ב-S3'),
    dict(n=5, q='הרציף העתידי של "תחנת החוף" (y 2560–3560, D-130): המעבר UX-1 ב-y 2620 נותן לו גישה מתחת לגשר; אם הרציף עדיין רלוונטי, הוא מתחיל ב-y 2700.', default='כן'),
]

out = dict(
    id='city_plan', batch='7ב', title='תוכנית הדרכים של כל העיר — סבב 6', at='1.11.2026', by='הבונה',
    basis=dict(owner=['12:10 — 7ב: רשת נקייה לכל המפה, לא קשורה לכבישים של היום; מהיום רק השטח', '12:07 — B4 מחדש על התכנון החדש'],
               coordinator='12:33 — היררכיה אמיתית: עורקים כל 2–3 אזורים לפי הזרימה (השדה, הנמל, המרכז, האי), מאספים לפי הצורך, רחובות לפי השימושים; לכל בחירה משפט אחד',
               terrain='טבעת הים של המשחק (חופי A6 ו-B6, רציף הנמל בשורה 5200, קו החוף המזרחי ב-6230, החוף של W3, הגבול הצפוני ב-2550, אגן המרינה), האגם — מורחב אל B1 לפי תוכנית האב (D‑13, GATE‑100), האי — לפי D‑259',
               fixed=['השדה (R-32) — רק שלושת השערים: AP1 (4800, 1600), AP2 (4800, 1250), AP3 (6750, 1700)', 'קווי הרכבת', 'גשר האי (D-187, D-242)'],
               background='תוכנית הדרכים של חלק ה — רקע בלבד', today='הדרכים של המשחק היום — רק למעבר'),
    rules=dict(scale='10 px = 1 מ׳; נתיב 44 px', R15='לפחות 60 מ׳ בין צמתים לאורך כל דרך; בעורק לפחות 90 מ׳ בין רמזורים',
               R16='ברמזור — נתיב שמאלה וחץ בכל גישה', riro='רחוב מקומי על עורק — ימינה פנימה וימינה החוצה בלבד, בלי רמזור',
               junctions='עורק × עורק או עורק × מאסף → רמזור; מאסף × מאסף בארבע זרועות → כיכר; כל השאר → עצור/תן זכות קדימה',
               driveways='כניסה למגרש אחד (חניון, חצר, שער) היא לא צומת',
               lane_width='הנתיב ברשת של היום נשאר 4.4 מ׳ (44 px); נתיב של 3.9 מ׳ (אפשרות ב׳, ×1.125) רק בדרכים שנבנות מחדש לפי 7ב, אזור אחרי אזור (המתאם, 31.10)'),
    classes=CLS, nodes=list(N.values()), roads=Rd, segments=SEG, signals=SIG,
    roundabouts=[dict(node=k, label=v['label'], arms=v['deg'], why=v['why']) for k, v in N.items() if v['kind'] == 'roundabout'],
    riro=[dict(node=k, label=v['label'], why=v['why']) for k, v in N.items() if v['kind'] == 'riro'],
    crossings=P.CROSS, routes=P.ROUTES, access=P.ACCESS, blocks=BLK, fit=fits, zones=ZONES,
    transition=dict(why='כל שלב בונה את הדרכים החדשות של האזורים שלו (דרך על תפר — עם הראשון מבין השניים); כל רחוב ישן שנכנס לאזור שנבנה נחתך בגבול ומחובר בחיבור זמני לדרך החדשה הקרובה, עד שהאזור השכן נבנה.',
                    stages=TRANS),
    totals=dict(nodes=len(N), segments=len(SEG), km={CLS[c]['he']: round(sum(s['len_m'] for s in SEG if s['cls'] == c) / 1000, 2) for c in CLS if any(s['cls'] == c for s in SEG)},
                signals=len(SIG), roundabouts=sum(1 for v in N.values() if v['kind'] == 'roundabout'), riro=sum(1 for v in N.values() if v['kind'] == 'riro'),
                temp=ntemp),
    checks=checks, questions=sorted(QUEST, key=lambda q: q['n']),
    impl=[dict(what='רמזור עם חץ שמאלה', game='ליבת הרמזורים של המשחק — המופעים עם חץ (3 / 9) כבר קיימים; רשימת צומתי הרמזור והתנועות לפי נתיב'),
          dict(what='ימינה בלבד', game='MOVES2 בלי שמאלה פנימה והחוצה, ואי תנועה באמצע העורק'),
          dict(what='כיכר', game='חדש במשחק — ראו שאלה 6'),
          dict(what='מעבר תחתי UX-1', game='בציור: גשר רכבת קצר מעל הכביש (סיפון, עמודים, צל); בגרף: קטע רגיל'),
          dict(what='מחסומים LX-1, LX-2', game='קיימים (D-242)'),
          dict(what='חיבור זמני', game='קטע בגרף שמסומן זמני, ושמו מתחיל ב-TMP; צומת זמני — עצור, ובבדיקה ברשימה נפרדת')],
    sites=SITES, driveways=DWS + LOT_DW, site_roads=SITE_ROADS, lots=LOTS, air=dict(AIRF, roads=AIR_ROADS), island=ISLF, rails=RAILS, rail_sections=SECTIONS, access_az=ACC_AZ, pax=PAX, term_route=TERM_ROUTE, stations=CITY.STATIONS, bus=dict(stops=STOPS, terminal=TERM, bay=BAY, crosswalks=XW, speed_px_s=v_px, layover_s=LAYOVER),
    terrain=dict(sea=SEA, island=ISLAND, island_water=ISL_WATER, lake=LAKE, airport=AIRPORT, airport_today=AIRPORT_TODAY, rail=RAIL, bridge=BRIDGE),
)
# 1.11 (R-36): the labels — every name in Hebrew, each with its own zoom limit, so that at no zoom two of them (or a name and an icon) overlap
LAY = SV.label_layout(out); out['labels'] = LAY
chk('התוויות — שמות קריאים בעברית, בגודל קבוע על המסך, בלי שום חפיפה (בין שתי תוויות, או תווית וסמל) בכל רמת הגדלה', LAY['overlaps'] == 0,
    f"{LAY['n']} תוויות (אזורים, דרכים, מגרשים, השדה והאי); נבדקו {len(LAY['levels'])} רמות הגדלה, מכל העיר בטלפון ועד ההגדלה המרבית: {LAY['overlaps']} חפיפות. בכל העיר מוצגות {LAY['shown'][str(LAY['levels'][-2])]} תוויות, ובהגדלה המרבית {LAY['shown'][str(LAY['levels'][0])]}; "
    f"{LAY['never']} תוויות קטנות מדי למגרש שלהן ולא מוצגות (השם בריחוף).")
json.dump(out, open(W + '/study/roads/city_plan.json', 'w'), ensure_ascii=False, indent=1)
for c in checks: print(('OK ' if c['ok'] else 'XX ') + c['name'] + ' — ' + c['det'][:260])
print(out['totals'])
