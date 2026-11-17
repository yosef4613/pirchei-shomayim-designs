# 30.10 · 7b (the owner 13:20: no pictures — the maps in code): the SVG of the road plan.
# 1.11 (R-36, the owner 31.10 23:10): the map of the future — 5 layers (roads, rails, lots, bus, names), one short legend, every kind of road
# its own colour and width, the future marked in one style, Hebrew names that never overlap (each label has its own zoom limit).
# 31.10 (the owner 20:12 + 20:23): one style for every map — every road at its real width (lane 3.9 m, sidewalks), the lanes drawn,
# today's roads thin grey and dashed, the temporary links a third style, every zone with its border, id and short name, the labels at
# a constant size on the screen, buttons for the layers, and the inner roads of the lots drawn as roads. One set of layers in <defs>;
# every map reuses them (<use>), so the page stays light. No PNG.
import math, html, json
COLS = [0, 1200, 2400, 3600, 4800, 6000, 7200, 8400, 9600]; ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]
e = lambda s: html.escape(str(s), quote=True)
def f1(v): return f"{v:.0f}" if abs(v - round(v)) < .05 else f"{v:.1f}"
def pts(p): return ' '.join(f"{f1(x)},{f1(y)}" for x, y in p)
def sid(s): return s.replace('/', '-')
def zrect(z): i = 'ABCDEFGH'.index(z[0]); j = int(z[1:]); return COLS[i], ROWS[j], COLS[i + 1], ROWS[j + 1]

# ---------------------------------------------------------------- the zones: a short name and a kind (the tint) for each of the 80
ZN = {
    'A0': ('יער הררי', 'forest'), 'B0': ('יער', 'forest'), 'C0': ('שדות', 'fields'), 'D0': ('שדות', 'fields'),
    'E0': ('המסלול', 'air'), 'F0': ('המסלול', 'air'), 'G0': ('המסלול · חירום', 'air'), 'H0': ('קצה המסלול', 'air'),
    'A1': ('יער', 'forest'), 'B1': ('פארק צפוני ואגם', 'park'), 'C1': ('הכפר', 'fields'), 'D1': ('החממות', 'fields'),
    'E1': ('צד אווירי', 'air'), 'F1': ('צד אווירי', 'air'), 'G1': ('צד אווירי', 'air'), 'H1': ('צד אווירי', 'air'),
    'A2': ('בית החולים', 'public'), 'B2': ('הפארק והאגם', 'park'), 'C2': ('הקניון', 'shop'), 'D2': ('עסקים ומלונות', 'shop'),
    'E2': ('השדה — צד היבשה', 'air'), 'F2': ('הטרמינל', 'air'), 'G2': ('האנגרים', 'air'), 'H2': ('תחזוקת השדה', 'air'),
    'A3': ('קריית הספורט', 'sport'), 'B3': ('מגורים — צפון', 'home'), 'C3': ('הווילות', 'home'), 'D3': ('וילות ורכב', 'home'),
    'E3': ('תחנת הרכבת והמסוף', 'rail'), 'F3': ('המרינה', 'coast'), 'G3': ('השדה — דרום', 'air'), 'H3': ('השדה — דרום', 'air'),
    'A4': ('ספורט וכבאות', 'sport'), 'B4': ('השכונה', 'home'), 'C4': ('תעשייה קלה', 'work'), 'D4': ('מחסנים', 'work'),
    'E4': ('תחנת הכוח', 'rail'), 'F4': ('החוף המזרחי', 'coast'), 'G4': ('ים', 'sea'), 'H4': ('ים', 'sea'),
    'A5': ('הדאונטאון', 'public'), 'B5': ('האקדמיה והעירייה', 'public'), 'C5': ('בית הזיקוק', 'work'), 'D5': ('שער הנמל', 'port'),
    'E5': ('חצר הרכבות', 'rail'), 'F5': ('נתיב האוניות', 'sea'), 'G5': ('נתיב האוניות', 'sea'), 'H5': ('ים', 'sea'),
    'A6': ('החווה והמעבורת', 'fields'), 'B6': ('החוף', 'coast'), 'C6': ('מסוף המכולות', 'port'), 'D6': ('רציפי הנמל', 'port'),
    'E6': ('הנמל העמוק', 'port'), 'F6': ('ים · הדרך לאי', 'sea'), 'G6': ('ים', 'sea'), 'H6': ('ים', 'sea'),
    'A7': ('ים', 'sea'), 'B7': ('מפרץ הדיג', 'sea'), 'C7': ('מימי הנמל', 'sea'), 'D7': ('מימי הנמל', 'sea'), 'E7': ('מימי הנמל', 'sea'),
    'F7': ('נתיב שיט', 'sea'), 'G7': ('אסדת הגז', 'sea'), 'H7': ('ים', 'sea'),
    'A8': ('ים', 'sea'), 'B8': ('ים', 'sea'), 'C8': ('נתיב מטען', 'sea'), 'D8': ('נתיב מטען', 'sea'), 'E8': ('נתיב מטען', 'sea'),
    'F8': ('ים', 'sea'), 'G8': ('ים', 'sea'), 'H8': ('ים', 'sea'),
    'A9': ('ים', 'sea'), 'B9': ('ים', 'sea'), 'C9': ('ים', 'sea'), 'D9': ('ים', 'sea'), 'E9': ('ים', 'sea'), 'F9': ('ים', 'sea'),
    'G9': ('האי — מערב', 'island'), 'H9': ('האי', 'island'),
}
TINT = {'forest': '#d3e4c0', 'fields': '#eee6c2', 'park': '#d0e9c1', 'home': '#f4ead7', 'shop': '#f5e0d8', 'work': '#e4dfeb',
        'port': '#dde3e9', 'air': '#e8e8e4', 'rail': '#e6e1d8', 'public': '#e0eaf2', 'sport': '#d9eedd', 'coast': '#f3e9cf', 'sea': '#f1ead6',
        'island': '#e6e0c9'}


# ---------------------------------------------------------------- the road styles: one per kind (colour, lane lines, casing) — 1.11: each kind its own colour and width
STY = {'main': ('#9c1c1c', '#ffffff', '#4a1d1a'), 'arterial': ('#d9572f', '#ffffff', '#5a3b33'), 'collector': ('#eda63a', '#ffffff', '#6a5331'),
       'local': ('#ffffff', '#8f8f8f', '#6f6b62'), 'oneway': ('#fff0a8', '#8a7420', '#7a6a3a'), 'track': ('#c69c6b', None, '#7b5c3b'),
       'service': ('#ebebe7', None, '#8a867c'), 'driveway': ('#ebebe7', None, '#8a867c'), 'bridge': ('#a99ad6', '#ffffff', '#4e446d'),
       'airland': ('#eda63a', '#ffffff', '#6a5331'), 'temp': ('#f7cdea', '#b0177f', '#b0177f')}
WALK = '#e2ded3'; MED = '#9cbf86'
def geom(CLS, cls, kind='road', lanes=None):
    """the cross-section in px: carriageway, total width, median, lane lines [(offset, dashed)], arrows (one way) and the style key"""
    if cls in ('service', 'driveway') or cls is None:
        cw = 39 if (lanes == '1' or cls == 'service') else (60 if cls == 'driveway' else 78)
        return dict(cw=cw, tw=cw, med=0, lines=[], arrow=False, st=cls or 'service')
    if cls == 'airland':
        return dict(cw=78, tw=118, med=0, lines=[(0, 1)], arrow=True, st='airland')
    c = CLS[cls]; L = c['lane_m'] * 10; med = c['median_m'] * 10; n = c['dirN']
    cw = (2 if c['twoway'] else 1) * n * L + med; tw = c['halfW'] * 2
    lines = []
    if c['twoway'] and n == 1: lines = [(0, 1)]
    elif c['twoway'] and n >= 2: lines = [(s * (med / 2 + L * k), 1) for k in range(1, n) for s in (-1, 1)]
    return dict(cw=cw, tw=tw, med=med, lines=lines, arrow=(cls == 'oneway'), st='bridge' if kind == 'bridge' else cls)

def road_parts(pid, p, g, cut=(0, 0), caps=()):
    """the three passes of one road: base (casing + sidewalk), top (carriageway), lanes (median, lines and arrows — cut back at the junctions).
    The ends are square; caps = the ends where the road stops or turns a corner, drawn round."""
    st = STY[g['st']]; tw, cw = g['tw'], g['cw']
    cb = ''.join(f"<circle cx='{f1(x)}' cy='{f1(y)}' r='{f1(tw / 2 + 3)}' fill='{st[2]}'/>" + (f"<circle cx='{f1(x)}' cy='{f1(y)}' r='{f1(tw / 2)}' fill='{WALK}'/>" if tw > cw + 1 else '') for x, y in caps)
    cc = ''.join(f"<circle cx='{f1(x)}' cy='{f1(y)}' r='{f1(cw / 2)}' fill='{st[0]}'/>" for x, y in caps)
    base = f"<g id='b-{pid}'><polyline points='{pts(p)}' class='rk' stroke='{st[2]}' stroke-width='{f1(tw + 6)}'/>" + \
           (f"<polyline points='{pts(p)}' class='rk' stroke='{WALK}' stroke-width='{f1(tw)}'/>" if tw > cw + 1 else '') + cb + "</g>"
    top = f"<g id='c-{pid}'><polyline points='{pts(p)}' class='rk' stroke='{st[0]}' stroke-width='{f1(cw)}'/>" + cc + "</g>"
    q = trim(p, *cut) if (cut[0] or cut[1]) else p
    ln = f"<polyline points='{pts(q)}' class='rk' stroke='{MED}' stroke-width='{f1(g['med'])}'/>" if (g['med'] and q) else ''
    if q and st[1]:
        ln += ''.join(f"<polyline points='{pts(offset(q, d) if d else q)}' class='ln' stroke='{st[1]}'/>" for d, dash in g['lines'])
    if q and g.get('arrow'):   # one way: a chevron every 12 m in the direction of travel
        L = plen(q); acc = 0; ch = []
        for i in range(len(q) - 1):
            (ax, ay), (bx, by) = q[i], q[i + 1]; l = math.hypot(bx - ax, by - ay) or 1; ux, uy = (bx - ax) / l, (by - ay) / l
            t = (60 - acc % 120) % 120
            while t < l:
                x, y = ax + ux * t, ay + uy * t; h = min(cw / 2 - 6, 14)
                ch.append(f"M{f1(x - ux * 12 - uy * h)},{f1(y - uy * 12 + ux * h)}L{f1(x + ux * 6)},{f1(y + uy * 6)}L{f1(x - ux * 12 + uy * h)},{f1(y - uy * 12 - ux * h)}")
                t += 120
            acc += l
        if ch: ln += f"<path d='{''.join(ch)}' class='arw' stroke='{st[1] or '#666'}'/>"
    lane = f"<g id='l-{pid}'>{ln}</g>"
    return base, top, lane

# ---------------------------------------------------------------- the shared layers (<defs>)
SITE_FILL = {'building': '#8e9aa8', 'parking': '#d6dade', 'field': '#b9dca0', 'court': '#e8b48a', 'yard': '#e9d7b4', 'plaza': '#eee6cf', 'park': '#a8d59a',
             'beach': '#f3e3b0', 'pier': '#8b6b4a', 'runway': '#55575a', 'taxi': '#9a9b97', 'apron': '#c9cac5', 'stand': '#d7d8d3'}
LOTFILL = {'home': '#f3dfb8', 'shop': '#f2c7b8', 'work': '#d9cfe6', 'port': '#c9d3dd', 'rail': '#d8d1c4', 'forest': '#b9d6a3', 'fields': '#e2d68f',
           'park': '#b8dda6', 'coast': '#f1e2b2', 'public': '#c9dced', 'sport': '#bfe3c6', 'air': '#d6d6d0'}
def rect_el(r, fill, extra=''):
    x0, y0, x1, y1 = r
    return f"<rect x='{f1(x0)}' y='{f1(y0)}' width='{f1(x1 - x0)}' height='{f1(y1 - y0)}' fill='{fill}' {extra}/>"
def fut(r, poly=None):
    """the mark of the future (not built yet): fine diagonal stripes and a dashed edge — one style for everything"""
    if poly: return f"<polygon points='{pts(poly)}' class='fut' vector-effect='non-scaling-stroke'/>"
    x0, y0, x1, y1 = r
    return f"<rect x='{f1(x0)}' y='{f1(y0)}' width='{f1(x1 - x0)}' height='{f1(y1 - y0)}' class='fut' vector-effect='non-scaling-stroke'/>"

def defs(P, GR, M):
    T = P['terrain']; CLS = M['CLS']
    o = ["<svg width='0' height='0' style='position:absolute' aria-hidden='true'><defs>",
         "<pattern id='futp' width='26' height='26' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><line x1='0' y1='0' x2='0' y2='26' stroke='#ffffff' stroke-width='7' stroke-opacity='.55'/></pattern>"]
    # the terrain: a tint per zone, the sea, the island, the lake; the zone borders on top
    o.append("<g id='terrain'><rect x='-400' y='-1250' width='10400' height='9400' fill='#f3f0e7'/>")
    for z, (nm, k) in ZN.items():
        x0, y0, x1, y1 = zrect(z); o.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='{TINT[k]}'/>")
    o.append(f"<polygon points='{pts(T['sea'])}' class='sea'/><polygon points='{pts(T['island'])}' class='isl'/>")
    for w in T.get('island_water', []): o.append(f"<polygon points='{pts(w)}' class='sea'/>")
    o.append(lake_svg(T))
    for x in COLS: o.append(f"<line x1='{x}' y1='-850' x2='{x}' y2='7750' class='zb' vector-effect='non-scaling-stroke'/>")
    for y in ROWS: o.append(f"<line x1='0' y1='{y}' x2='9600' y2='{y}' class='zb' vector-effect='non-scaling-stroke'/>")
    o.append("</g>")
    o.append(lots_layer(P))
    o.append(roads_layer(P, M))
    o.append(rails_layer(P))
    o.append(bus_layer(P, M))
    # for the transition maps only: today's roads and the temporary links
    o.append("<g id='old'>")
    for ed in GR['edges']:
        a, b = M['ON'][ed['a']], M['ON'][ed['b']]; stay = ed['id'] not in M['gone']
        o.append(f"<line id='od-{e(ed['id'])}' x1='{f1(a['x'])}' y1='{f1(a['y'])}' x2='{f1(b['x'])}' y2='{f1(b['y'])}' class='{'oldk' if stay else 'old'}' vector-effect='non-scaling-stroke'/>")
    o.append("</g><g id='temps'>")
    for t in P['transition']['stages']:
        for a in t['temp_added']: o.append(temp_svg(a))
    o.append("</g>")
    o.append(icon_defs())
    o.append("</defs></svg>")
    return '\n'.join(o)

def lake_svg(T):
    L = T['lake']
    if 'pts' not in L: return f"<ellipse cx='{L['cx']}' cy='{L['cy']}' rx='{L['rx']}' ry='{L['ry']}' class='lake'/>"
    LT = L['today']
    o = f"<polygon points='{pts(L['pts'])}' class='lake'/><polygon points='{pts(L['pts'])}' fill='url(#futp)'/>"   # the new part of the lake is the future
    o += f"<ellipse cx='{LT['cx']}' cy='{LT['cy']}' rx='{LT['rx']}' ry='{LT['ry']}' class='lake' stroke='none'/>"
    o += f"<polygon points='{pts(L['pts'])}' class='lakef' vector-effect='non-scaling-stroke'/>"
    for k in L.get('keep', []):   # today's things on the shore, kept: the pier and the jetties (brown), the cafe and the kiosk (grey)
        x, y = k['x'], k['y']
        if k['id'] == 'B2-PIER': o += f"<rect x='{x - 30}' y='{y - 14}' width='60' height='28' fill='#8b6b4a' stroke='#5a4330' stroke-width='3'/>"
        elif k['kind'] == 'shore': o += f"<rect x='{x - 40 if x < 1840 else x + 4}' y='{y - 7}' width='36' height='14' fill='#8b6b4a' stroke='#5a4330' stroke-width='3'/>"
        else: o += f"<rect x='{x - 22}' y='{y - 16}' width='44' height='32' fill='#8e9aa8' stroke='#556' stroke-width='4'/>"
    return o

def lots_layer(P):
    """every lot of the city: the zones built in detail, the new lots of every other zone, the airport of stage 8 and the island — future ones marked"""
    o = ["<g id='lots'>"]
    for l in P.get('lots', []):   # the new lots: the parcel in the colour of its use
        o.append(rect_el(l['rect'], LOTFILL.get(l['use'], '#e6e1d6'), "stroke='#6d6a63' stroke-width='4'") + fut(l['rect']))
    for i in P.get('sites', []):   # 1.11: the lots of the villas (with their border) under everything else of the zone
        if i['kind'] == 'lot':
            fill = LOTFILL.get(i.get('use'), '#f3dfb8')
            if i.get('poly'): o.append(f"<polygon points='{pts(i['poly'])}' fill='{fill}' stroke='#6d6a63' stroke-width='6'/>" + fut(None, i['poly']))
            else: o.append(rect_el(i['rect'], fill, "stroke='#6d6a63' stroke-width='6'") + fut(i['rect']))
    for i in P.get('sites', []):
        if i['kind'] in ('site', 'lot') or i.get('apron'): continue
        if i['kind'] == 'path':   # a footpath: light paving with a thin edge
            o.append(f"<polyline points='{pts(i['rect'])}' class='rk' stroke='#9c8f72' stroke-width='{f1(2 * i['hw'] + 4)}'/><polyline points='{pts(i['rect'])}' class='rk' stroke='#fbf6e8' stroke-width='{f1(2 * i['hw'])}'/>"
                     f"<polyline points='{pts(i['rect'])}' class='rk' stroke='#c9b98f' stroke-width='3' stroke-dasharray='8 10'/>")
            continue
        if i['kind'] == 'house':
            o.append(rect_el(i['rect'], '#a3abb5', "stroke='#556' stroke-width='3'")); continue
        if i['kind'] == 'pad':
            (cx, cy), r, sf = i['c'], i['r'], i['safety']
            o.append(f"<g><circle cx='{cx}' cy='{cy}' r='{sf}' fill='none' stroke='#d9534f' stroke-width='6' stroke-dasharray='30 20'/><circle cx='{cx}' cy='{cy}' r='{r}' fill='#f4f4f4' stroke='#555' stroke-width='8'/><text x='{cx}' y='{cy + 45}' class='padh'>H</text></g>")
        else:
            o.append(rect_el(i['rect'], SITE_FILL[i['kind']], "stroke='#556' stroke-width='5'"))
            if i.get('depot'):   # the night depot: drive-through lanes, three buses in each, an aisle at each end
                x0, y0, x1, y1 = i['rect']; dp = i['depot']; n = dp['lanes']; a = dp['aisle']; w = (x1 - x0) / n
                o.append(rect_el([x0, y0, x1, y0 + a], '#5b636e') + rect_el([x0, y1 - a, x1, y1], '#5b636e'))
                for k in range(n + 1): o.append(f"<line x1='{f1(x0 + k * w)}' y1='{y0 + a}' x2='{f1(x0 + k * w)}' y2='{y1 - a}' stroke='#f2c200' stroke-width='3'/>")
                for k in range(n):
                    for m in range(dp['per']):
                        by = y0 + a + 8 + m * 145; o.append(f"<rect x='{f1(x0 + k * w + 5)}' y='{f1(by)}' width='{f1(w - 10)}' height='135' rx='6' fill='#3f6fb5' opacity='.85'/>")
            o.append(fut(i['rect']))
    A = P.get('air')
    if A:   # the airport of stage 8: the paved areas, the stands, the buildings, the fence — all of it future
        order = {'apron': 0, 'taxi': 1, 'runway': 2, 'stand': 3, 'yard': 3, 'parking': 4, 'building': 5, 'pad': 6}
        for l in sorted(A['lots'], key=lambda l: order.get(l['kind'], 3)):
            r = l['rect']
            if l['kind'] == 'runway':
                o.append(rect_el(r, SITE_FILL['runway'])); cy = (r[1] + r[3]) / 2
                o.append(f"<line x1='{r[0] + 60}' y1='{cy}' x2='{r[2] - 60}' y2='{cy}' stroke='#fff' stroke-width='7' stroke-dasharray='90 70'/>")
            elif l['kind'] == 'taxi':
                o.append(rect_el(r, SITE_FILL['taxi']))
                if r[2] - r[0] > r[3] - r[1]: o.append(f"<line x1='{r[0]}' y1='{(r[1] + r[3]) / 2}' x2='{r[2]}' y2='{(r[1] + r[3]) / 2}' stroke='#e2b100' stroke-width='6'/>")
                else: o.append(f"<line x1='{(r[0] + r[2]) / 2}' y1='{r[1]}' x2='{(r[0] + r[2]) / 2}' y2='{r[3]}' stroke='#e2b100' stroke-width='6'/>")
            elif l['kind'] == 'stand':
                o.append(rect_el(r, 'none', "stroke='#e2b100' stroke-width='5'"))
                cx = (r[0] + r[2]) / 2; w = (r[2] - r[0]) * .42; hgt = (r[3] - r[1]) * .7; y0 = r[1] + (r[3] - r[1]) * .15
                o.append(f"<path d='M{f1(cx)},{f1(y0)} l{f1(w * .09)},{f1(hgt * .35)} l{f1(w * .91)},{f1(hgt * .17)} l0,{f1(hgt * .08)} l{f1(-w * .91)},{f1(-hgt * .02)} l{f1(-w * .04)},{f1(hgt * .3)} l{f1(w * .3)},{f1(hgt * .08)} l0,{f1(hgt * .05)} l{f1(-w * .35)},{f1(-hgt * .03)} l{f1(-w * .35)},{f1(hgt * .03)} l0,{f1(-hgt * .05)} l{f1(w * .3)},{f1(-hgt * .08)} l{f1(-w * .04)},{f1(-hgt * .3)} l{f1(-w * .91)},{f1(hgt * .02)} l0,{f1(-hgt * .08)} l{f1(w * .91)},{f1(-hgt * .17)} z' fill='#f7f7f5' stroke='#6d6f73' stroke-width='3'/>")
            elif l['kind'] == 'pad':
                cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2; rr = (r[2] - r[0]) / 2
                o.append(f"<circle cx='{f1(cx)}' cy='{f1(cy)}' r='{f1(rr)}' fill='#e4e4df' stroke='#555' stroke-width='6'/><text x='{f1(cx)}' y='{f1(cy + rr * .35)}' class='padh' style='font-size:{f1(rr)}px'>H</text>")
            else:
                o.append(rect_el(r, SITE_FILL.get(l['kind'], '#c9cac5'), "stroke='#4f5560' stroke-width='5'" if l['kind'] in ('building', 'parking') else ''))
        for sv in A['service']: o.append(rect_el(sv['rect'], '#b4b4ae'))
        o.append(f"<polygon points='{pts(A['fence'])}' fill='url(#futp)' class='afence' vector-effect='non-scaling-stroke'/>")
        o.append(f"<polygon points='{pts(A['fence'])}' class='fut' style='fill:none' vector-effect='non-scaling-stroke'/>")
        for b in A.get('front_bays', []): o.append(rect_el(b['rect'], '#5b636e', "stroke='#f2c200' stroke-width='4' stroke-dasharray='14 10'"))
    I = P.get('island')
    if I:   # the island of D-259: the summit forest, the station plaza, the village, the harbour — future
        sx, sy = I['summit']
        for k, rr in enumerate((330, 250, 170, 90)): o.append(f"<ellipse cx='{sx}' cy='{sy}' rx='{rr * 2.4}' ry='{rr}' fill='none' stroke='#b9a77d' stroke-width='5' opacity='.7'/>")
        for l in I['lots']:
            if l['kind'] == 'pad':
                r = l['rect']; cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
                o.append(f"<circle cx='{f1(cx)}' cy='{f1(cy)}' r='133' fill='none' stroke='#d9534f' stroke-width='6' stroke-dasharray='30 20'/><circle cx='{f1(cx)}' cy='{f1(cy)}' r='100' fill='#f4f4f4' stroke='#555' stroke-width='8'/><text x='{f1(cx)}' y='{f1(cy + 45)}' class='padh'>H</text>")
            else: o.append(rect_el(l['rect'], SITE_FILL.get(l['kind'], '#d6dade'), "stroke='#556' stroke-width='5'" if l['kind'] in ('building', 'parking', 'yard') else "opacity='.85'") + fut(l['rect']))
        c = I['cable']; o.append(f"<polyline points='{pts(c)}' class='cable' vector-effect='non-scaling-stroke'/>")
    o.append("</g>")
    return '\n'.join(o)

def roads_layer(P, M):
    """the network in three passes (so that the junctions read as one surface), with the inner roads, the driveways and the aprons between
    the bases and the carriageways (a driveway crosses the sidewalk); the junction surfaces; the airport's landside roads. Ids per segment."""
    CLS = M['CLS']; B, C, Lh, SB = [], [], [], []
    order = {'track': 0, 'oneway': 1, 'local': 1, 'collector': 2, 'arterial': 3, 'main': 4}
    XWS = {}
    for x in P.get('bus', {}).get('crosswalks', []): XWS.setdefault(x['seg'], []).append(x)
    for s in sorted(P['segments'], key=lambda s: order[s['cls']]):
        b, c, l = road_parts(sid(s['id']), s['pts'], M['G'][s['id']], M['cuts'][s['id']], M['caps'][s['id']])
        zw = ''
        for x in XWS.get(s['id'], []):   # a zebra: stripes along the traffic, 4 m wide, across the carriageway
            d = (x['d0'] + x['d1']) / 2; cx, cy = x['at'][0] + x['u'][0] * d, x['at'][1] + x['u'][1] * d; nx, ny = -x['u'][1], x['u'][0]; h = x['cw'] / 2 - 4
            zw += f"<line x1='{f1(cx - nx * h)}' y1='{f1(cy - ny * h)}' x2='{f1(cx + nx * h)}' y2='{f1(cy + ny * h)}' class='zeb' stroke='{'#c4c4c4' if STY[M['G'][s['id']]['st']][0] == '#ffffff' else '#ffffff'}' stroke-width='{x['d1'] - x['d0']}'/>"
        l = l.replace('</g>', zw + '</g>') if zw else l
        B.append(b); C.append(c); Lh.append(l)
    for r in P.get('site_roads', []):
        g = geom(CLS, r.get('cls') if r.get('cls') in CLS or r.get('cls') in ('service', 'driveway') else 'service', lanes=r['lanes'])
        b, c, l = road_parts('s-' + sid(r['id']), r.get('draw') or r['pts'], g, (0, 0))
        SB.append(f"<g id='sx-{e(sid(r['id']))}'>{b}{c}</g>"); Lh.insert(0, l)
    for i in P.get('sites', []):   # the paved aprons (the fire station, the ambulances) are road surface, out to the carriageway
        if i.get('apron'):
            x0, y0, x1, y1 = i.get('draw') or i['rect']
            SB.append(f"<g id='sx-a-{e(i['id'])}'><rect x='{f1(x0 - 3)}' y='{f1(y0 - 3)}' width='{f1(x1 - x0 + 6)}' height='{f1(y1 - y0 + 6)}' fill='#6f6b62'/>"
                      f"<rect x='{f1(x0)}' y='{f1(y0)}' width='{f1(x1 - x0)}' height='{f1(y1 - y0)}' fill='#f4f4f2'/></g>")
    for r in P.get('air', {}).get('roads', []):   # the landside of the airport (stage 8): one way, two lanes
        if r.get('cls') in CLS: g = geom(CLS, r['cls'])   # 1.11 00:44: the road from the gate to the terminal — 2+2, like an arterial
        else:
            g = geom(CLS, 'airland'); g['arrow'] = r['oneway']; g['lines'] = [] if r['oneway'] else [(0, 1)]
            if r['oneway']: g['lines'] = [(0, 1)]
        b, c, l = road_parts('ar-' + r['id'], r['pts'], g, (0, 0), caps=[tuple(r['pts'][0]), tuple(r['pts'][-1])] if not (r['oneway'] or r.get('cls') in CLS) else ())
        tp = r.get('taper')
        if tp:   # the marked taper: the third lane of the avenue ends over 60 m after the gate — a wedge with diagonal hatching and a merge arrow
            y0 = r['pts'][0][1]; hc = g['cw'] / 2; L_ = CLS[r['cls']]['lane_m'] * 10; x0, x1 = tp['x0'], tp['x1']; sg = tp.get('side', 1)
            wedge = [[x0, y0 + sg * hc], [x0, y0 + sg * (hc + L_)], [x1, y0 + sg * hc]]
            c += (f"<polygon points='{pts(wedge)}' fill='{STY[r['cls']][0]}'/>"
                  + ''.join(f"<line x1='{f1(x0 + k * 60)}' y1='{f1(y0 + sg * (hc + L_ * (1 - k * 60 / (x1 - x0)) - 2))}' x2='{f1(x0 + k * 60 + 26)}' y2='{f1(y0 + sg * (hc + 2))}' stroke='#fff' stroke-width='5'/>" for k in range(1, int((x1 - x0) / 60)))
                  + f"<polygon points='{pts([[x0, y0 - sg * hc], [x0, y0 - sg * (hc + L_)], [x0 + 150, y0 - sg * hc]])}' fill='{STY[r['cls']][0]}'/>"
                  + f"<path d='M{x0 + 120},{f1(y0 + sg * (hc + L_ * .55))} L{x0 + 230},{f1(y0 + sg * (hc - L_ * .45))} M{x0 + 230},{f1(y0 + sg * (hc - L_ * .45))} l-34,-4 M{x0 + 230},{f1(y0 + sg * (hc - L_ * .45))} l-12,{f1(sg * 30)}' stroke='#fff' stroke-width='6' fill='none' stroke-linecap='round'/>")
        SB.append(f"<g id='sx-{e(r['id'])}'>{b}{c}</g>"); Lh.append(l)
    jx = []
    N = M['N']
    for n in P['nodes']:   # the roundabouts and the turning circles, drawn at their real size
        x, y, k = n['x'], n['y'], n['kind']
        if k == 'roundabout':
            arms = M['deg'].get(n['id'], []); top = max(arms, key=lambda s: order[s['cls']]) if arms else None
            col = STY[M['G'][top['id']]['st']][0] if top else '#fff'
            jx.append(f"<g><circle cx='{x}' cy='{y}' r='175' fill='#6f6b62'/><circle cx='{x}' cy='{y}' r='170' fill='{col}'/><circle cx='{x}' cy='{y}' r='80' fill='{MED}' stroke='#fff' stroke-width='8'/></g>")
        elif (k == 'end' and 'מעגל הסיבוב' in n['label']) or n.get('turn'):
            arm = max(M['deg'][n['id']], key=lambda t: M['G'][t['id']]['tw']); g = M['G'][arm['id']]; st = STY[g['st']]
            jx.append(f"<g><circle cx='{x}' cy='{y}' r='{f1(g['tw'] / 2 + 70)}' fill='{st[2]}'/><circle cx='{x}' cy='{y}' r='{f1(g['tw'] / 2 + 67)}' fill='{WALK}'/><circle cx='{x}' cy='{y}' r='{f1(g['cw'] / 2 + 67)}' fill='{st[0]}'/></g>")
    return ("<g id='roads'><g id='rdb'>" + ''.join(B) + "</g><g id='rds'>" + ''.join(SB) + "</g><g id='rdc'>" + ''.join(C) + "</g><g id='jx'>" + ''.join(jx) +
            "</g><g id='rdl'>" + ''.join(Lh) + "</g></g>")

RAILK = {'main': ('#3a3a3a', 26), 'port': ('#3a3a3a', 22), 'east': ('#3a3a3a', 26), 'yard': ('#555', 20), 'xover': ('#555', 18),
         'freight': ('#7b4a1e', 26), 'island': ('#3a3a3a', 26), 'siding': ('#555', 20)}
def rails_layer(P):
    """the rails (1.11): every track at its width — today solid, future dashed; the freight lines brown; the passenger line in teal
    over its tracks; the platforms; a bar at every buffer; an arrow where a line leaves the map; every crossing with a road"""
    o = ["<g id='rails'>"]
    rails = P.get('rails', []); isl = {r['id']: r for r in rails}
    if 'ISL-B' in isl and P.get('segments'):   # the shared deck of the bridge: between the road and the two tracks, from where the road joins it
        br = next((s for s in P['segments'] if s['kind'] == 'bridge'), None)
        if br:
            rp = [q for q in br['pts'] if 5920 <= q[1] <= 7090]; tp = [q for q in isl['ISL-B']['pts'] if q[1] >= 6000]
            if len(rp) > 1 and len(tp) > 1:
                poly = rp + tp[::-1]
                o.append(f"<polygon points='{pts(poly)}' fill='#d9d2ec' stroke='#6d628f' stroke-width='6'/>" + fut(None, poly))
        # the bridge of the S (two tracks over the water, from the switch to the deck)
        a, b = isl['ISL-A']['pts'], isl['ISL-B']['pts']
        o.append(f"<polyline points='{pts([q for q in a if q[1] <= 6085])}' class='rk' stroke='#6d628f' stroke-width='96'/>")
        o.append(f"<polyline points='{pts([q for q in a if q[1] <= 6085])}' class='rk' stroke='#e4dff1' stroke-width='86'/>")
    for st in P.get('stations', []):
        for r_ in st.get('rects', []):
            o.append(rect_el(r_, '#efe7d2', "stroke='#5d5d5d' stroke-width='5'") + (fut(r_) if st['state'] == 'future' else ''))
    if 'ISL-ST-A' in isl and 'ISL-ST-B' in isl:   # the island platform (1,000 × 90) between the two tracks
        a, b = isl['ISL-ST-A']['pts'], isl['ISL-ST-B']['pts']; mid = [[(a[0][0] + b[0][0]) / 2, (a[0][1] + b[0][1]) / 2], [(a[-1][0] + b[-1][0]) / 2, (a[-1][1] + b[-1][1]) / 2]]
        o.append(f"<polyline points='{pts(mid)}' stroke='#efe7d2' stroke-width='90' fill='none'/>")
    for r in rails:
        col, w = RAILK.get(r['kind'], ('#3a3a3a', 24)); p = pts(r['pts'])
        dash = " stroke-dasharray='70 34'" if r['state'] == 'future' else ''
        o.append(f"<polyline points='{p}' class='rk' stroke='{col}' stroke-width='{w}'{dash}/>"
                 f"<polyline points='{p}' class='rk' stroke='#f2efe5' stroke-width='{max(4, w // 4)}' stroke-dasharray='26 22'/>")
        for k, (kind, what) in zip((0, -1), r['ends']):
            q = r['pts'][k]; q2 = r['pts'][1] if k == 0 else r['pts'][-2]; dx, dy = q[0] - q2[0], q[1] - q2[1]; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L
            if kind in ('buffer', 'door'):   # a bar across the end
                o.append(f"<line x1='{f1(q[0] - uy * 26)}' y1='{f1(q[1] + ux * 26)}' x2='{f1(q[0] + uy * 26)}' y2='{f1(q[1] - ux * 26)}' stroke='#b3261e' stroke-width='10'/>")
            elif kind == 'edge':
                o.append(f"<path d='M{f1(q[0] - ux * 60 - uy * 40)},{f1(q[1] - uy * 60 + ux * 40)}L{f1(q[0])},{f1(q[1])}L{f1(q[0] - ux * 60 + uy * 40)},{f1(q[1] - uy * 60 - ux * 40)}' fill='none' stroke='#3a3a3a' stroke-width='12'/>")
    px = P.get('pax')
    if px:   # the passenger line (stage 17): teal over its tracks, dashed — future
        for k in ('south', 'north'):
            o.append(f"<polyline points='{pts(px[k])}' class='rk' stroke='#0e8f86' stroke-width='9' stroke-dasharray='40 22' opacity='.95'/>")
    for c in P['crossings']:
        for x, y, rl, rd in (c.get('pts') or [[c['at'][0], c['at'][1], '', '']]):
            if c['kind'] == 'level': o.append(f"<path d='M{x - 30},{y - 30}L{x + 30},{y + 30}M{x - 30},{y + 30}L{x + 30},{y - 30}' stroke='#b3261e' stroke-width='11'/>")
            else: o.append(f"<rect x='{x - 30}' y='{y - 44}' width='60' height='88' fill='none' stroke='#222' stroke-width='9'/>")
    o.append("</g>")
    return '\n'.join(o)
RST = [('ST-E3', 'התחנה המרכזית'), ('ST-COAST', 'תחנת החוף'), ('ST-PORT', 'רציף הנמל'), ('ST-RAILAIR', 'מסוף רכבת–אוויר'), ('ST-ISLAND', 'תחנת האי')]
def station_points(P):
    out = []
    for st in P.get('stations', []):
        if st.get('rects'):
            xs = [v for r_ in st['rects'] for v in (r_[0], r_[2])]; ys = [v for r_ in st['rects'] for v in (r_[1], r_[3])]
            out.append((st, (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
        elif st.get('poly') == 'island':
            a = next((r for r in P.get('rails', []) if r['id'] == 'ISL-ST-A'), None)
            if a: out.append((st, (a['pts'][0][0] + a['pts'][-1][0]) / 2 - 40, (a['pts'][0][1] + a['pts'][-1][1]) / 2 + 60))
    return out
def rail_marks(P, near=None):
    return "<g class='L-rails'>" + ''.join(icon('train' if st['kind'] == 'pax' else 'cargo', x, y) for st, x, y in station_points(P) if inside(near, x, y)) + "</g>"

def plen(p): return sum(math.hypot(p[i + 1][0] - p[i][0], p[i + 1][1] - p[i][1]) for i in range(len(p) - 1))
def trim(p, a, b):
    """cut a px off the start and b px off the end of a polyline"""
    L = plen(p)
    if a + b >= L - 1: return None
    def at(d):
        acc = 0
        for i in range(len(p) - 1):
            l = math.hypot(p[i + 1][0] - p[i][0], p[i + 1][1] - p[i][1])
            if acc + l >= d: t = (d - acc) / (l or 1); return i, [p[i][0] + (p[i + 1][0] - p[i][0]) * t, p[i][1] + (p[i + 1][1] - p[i][1]) * t]
            acc += l
        return len(p) - 2, list(p[-1])
    i0, q0 = at(a); i1, q1 = at(L - b)
    return [q0] + [list(x) for x in p[i0 + 1:i1 + 1]] + [q1]
def offset(p, d):
    """a parallel polyline at distance d (to the left of the direction of travel), mitred"""
    out = []
    for i in range(len(p)):
        ns = []
        for j in (i - 1, i):
            if 0 <= j < len(p) - 1:
                dx, dy = p[j + 1][0] - p[j][0], p[j + 1][1] - p[j][1]; l = math.hypot(dx, dy) or 1; ns.append((dy / l, -dx / l))
        nx, ny = sum(n[0] for n in ns), sum(n[1] for n in ns); l = math.hypot(nx, ny) or 1; nx, ny = nx / l, ny / l
        c = max(.5, sum(n[0] * nx + n[1] * ny for n in ns) / len(ns)); out.append([p[i][0] + nx * d / c, p[i][1] + ny * d / c])
    return out


def est(txt, px):
    """rough width of a label in screen px"""
    w = 0
    for ch in str(txt):
        if '֐' <= ch <= '׿': w += .58
        elif ch in ' ·—-.,()׳': w += .32
        elif ch.isupper() or ch.isdigit(): w += .64
        else: w += .52
    return w * px


def model(P, GR=None):
    """everything the layers, the labels and the hover need, computed once"""
    CLS = P['classes']; N = {n['id']: n for n in P['nodes']}; RD = {r['id']: r for r in P['roads']}
    deg = {}
    for s in P['segments']:
        for k in (s['a'], s['b']): deg.setdefault(k, []).append(s)
    G = {s['id']: geom(CLS, s['cls'], s['kind']) for s in P['segments']}
    def cut_at(s, k):   # how far the lane lines stop before the node k
        n = N[k]; others = [t for t in deg.get(k, []) if t is not s]
        if n['kind'] == 'roundabout': return 235
        if not others: return 0
        if len(others) == 1 and others[0]['road'] == s['road']: return 0
        return max(G[t['id']]['tw'] / 2 for t in others) + 60
    cuts = {s['id']: (cut_at(s, s['a']), cut_at(s, s['b'])) for s in P['segments']}
    def capped(s, k):   # a dead end, or a corner where the road turns
        arms = deg.get(k, [])
        if N[k]['kind'] == 'roundabout': return False
        if len(arms) == 1: return True
        if len(arms) == 2:
            v = []
            for t in arms:
                p = t['pts']; q = p[1] if t['a'] == k else p[-2]; v.append((q[0] - N[k]['x'], q[1] - N[k]['y']))
            (ax, ay), (bx, by) = v; c = (ax * bx + ay * by) / ((math.hypot(ax, ay) * math.hypot(bx, by)) or 1)
            return c > -0.97
        return False
    caps = {s['id']: [(N[k]['x'], N[k]['y']) for k in (s['a'], s['b']) if capped(s, k)] for s in P['segments']}
    gone = {}
    for t in P['transition']['stages']:
        for r in t['removed']: gone.setdefault(r, t['stage'])
    return dict(CLS=CLS, N=N, RD=RD, deg=deg, G=G, cuts=cuts, caps=caps, gone=gone, ON={n['id']: n for n in GR['nodes']} if GR else {})


# ---------------------------------------------------------------- the zone labels: a spot in each zone that covers the least road
FOOT_K = 11   # the zoom (world px per screen px) the zone labels are placed for
def bands(P, M):
    out = []
    for s in P['segments']:
        hw = M['G'][s['id']]['tw'] / 2; p = s['pts']
        for i in range(len(p) - 1):
            (ax, ay), (bx, by) = p[i], p[i + 1]; out.append((min(ax, bx) - hw, min(ay, by) - hw, max(ax, bx) + hw, max(ay, by) + hw))
    for r in P.get('site_roads', []):
        for i in range(len(r['pts']) - 1):
            (ax, ay), (bx, by) = r['pts'][i], r['pts'][i + 1]; hw = r['hw']; out.append((min(ax, bx) - hw, min(ay, by) - hw, max(ax, bx) + hw, max(ay, by) + hw))
    return out
def ov(a, b): return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
def zone_spots(P, M):
    """for every zone, the spot for its label: the place inside the zone that covers the least road (scored at the zoom FOOT_K)"""
    BD = bands(P, M); BL = [tuple(i['rect']) for i in P.get('sites', []) if i['kind'] == 'building']; out = {}
    BL += [tuple(l['rect']) for l in P.get('island', {}).get('lots', []) + P.get('air', {}).get('lots', []) if l['kind'] in ('pad', 'building', 'stand')] * 2
    L = P['terrain']['lake']
    if P.get('bus'): BL += [tuple(P['bus']['terminal']['rect'])] * 4
    if 'pts' in L:   # the lake (and its label) is an obstacle too: its bounding boxes north and south of y 850
        for part in ([q for q in L['pts'] if q[1] < 850], [q for q in L['pts'] if q[1] >= 850]):
            if part: BL += [(min(x for x, y in part), min(y for x, y in part), max(x for x, y in part), max(y for x, y in part))] * 3
    for z, (nm, k) in ZN.items():
        x0, y0, x1, y1 = zrect(z); w = max(est(z, 13), est(nm, 11)) * FOOT_K + 80; h = 30 * FOOT_K
        best = None
        for fx in (.82, .7, .58, .5, .42, .3, .18):
            for fy in (.24, .38, .52, .66, .8):
                cx = x0 + (x1 - x0) * fx; cy = y0 + (y1 - y0) * fy
                cx = min(max(cx, x0 + w / 2 + 30), x1 - w / 2 - 30); cy = min(max(cy, y0 + h / 2 + 20), y1 - h / 2 - 20)
                r = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
                sc = sum(ov(r, b) for b in BD) + .4 * sum(ov(r, b) for b in BL) + 60 * math.hypot(fx - .82, fy - .24) * w
                if best is None or sc < best[0]: best = (sc, cx, cy)
        out[z] = (best[1], best[2])
    return out

OCT = ' '.join(f"{7.6 * math.cos(math.pi / 8 + i * math.pi / 4):.2f},{7.6 * math.sin(math.pi / 8 + i * math.pi / 4):.2f}" for i in range(8))
ICON = {
    'signal': "<circle r='8.6' fill='#16181b' stroke='#fff' stroke-width='1.6'/><path d='M4.2,0H-3.6M-0.6,-3.1L-3.7,0L-0.6,3.1' fill='none' stroke='#4ee07a' stroke-width='2.1' stroke-linecap='round' stroke-linejoin='round'/>",
    'roundabout': "<circle r='8.2' fill='#fff' stroke='#1d5fa8' stroke-width='2.6'/><circle r='3' fill='#1d5fa8'/>",
    'stop': f"<polygon points='{OCT}' fill='#d42a2a' stroke='#fff' stroke-width='1.5'/><rect x='-4.2' y='-1.2' width='8.4' height='2.4' fill='#fff'/>",
    'riro': "<rect x='-7.6' y='-7.6' width='15.2' height='15.2' rx='3' fill='#7b3fb3' stroke='#fff' stroke-width='1.5'/><path d='M-2.8,4.6V-1.2H3.4M0.8,-3.8L3.5,-1.2L0.8,1.4' fill='none' stroke='#fff' stroke-width='1.9' stroke-linecap='round' stroke-linejoin='round'/>",
    'gate': "<polygon points='0,-8.5 8.5,0 0,8.5 -8.5,0' fill='#f08c00' stroke='#222' stroke-width='1.4'/>",
    'temp': "<rect x='-4.4' y='-4.4' width='8.8' height='8.8' transform='rotate(45)' fill='#fff' stroke='#b0177f' stroke-width='2.2'/>",
    'plaza': "<circle r='5' fill='#fff' stroke='#333' stroke-width='1.8'/>",
    'train': "<rect x='-6.8' y='-6.8' width='13.6' height='13.6' rx='3' fill='#0e8f86' stroke='#fff' stroke-width='1.4'/><rect x='-3.6' y='-4.4' width='7.2' height='6' rx='1.6' fill='#fff'/><path d='M-3.2,4.6L-1.6,2.6M3.2,4.6L1.6,2.6' stroke='#fff' stroke-width='1.3'/>",
    'cargo': "<rect x='-6.8' y='-6.8' width='13.6' height='13.6' rx='3' fill='#7b4a1e' stroke='#fff' stroke-width='1.4'/><rect x='-4.4' y='-3' width='8.8' height='5.4' fill='#fff'/><circle cx='-2.4' cy='3.8' r='1' fill='#fff'/><circle cx='2.4' cy='3.8' r='1' fill='#fff'/>",
    'bus': "<rect x='-6.6' y='-6.6' width='13.2' height='13.2' rx='2.6' fill='#1f4fa8' stroke='#fff' stroke-width='1.4'/><rect x='-3.9' y='-3.8' width='7.8' height='5.6' rx='1.2' fill='#fff'/><circle cx='-2.2' cy='3.3' r='1.15' fill='#fff'/><circle cx='2.2' cy='3.3' r='1.15' fill='#fff'/>",
}

JKIND = {'signal': 'signal', 'roundabout': 'roundabout', 'stop': 'stop', 'riro': 'riro', 'gate': 'gate', 'bridgehead': 'plaza', 'plaza': 'plaza'}
def icon(kind, x, y, cls='ji'):
    return f"<g class='{cls}' transform='translate({f1(x)} {f1(y)})'><g class='s'><use href='#ic-{kind}'/></g></g>"
def icon_defs(): return ''.join(f"<g id='ic-{k}'>{v}</g>" for k, v in ICON.items())
def inside(near, x, y): return (not near) or (near[0] <= x <= near[2] and near[1] <= y <= near[3])

# ---------------------------------------------------------------- the icons (a constant size on the screen) — they are also obstacles of the labels
def bus_badges(P):
    """the badge with the number of each line, twice along it, on the segment where it is most alone"""
    if not P.get('bus'): return []
    SEGBY = {frozenset((s['a'], s['b'])): s for s in P['segments']}; use = {}
    for ln in P['routes']['bus']:
        for a, b in zip(ln['path'], ln['path'][1:]): use.setdefault(frozenset((a, b)), set()).add(ln['id'])
    out = []
    for ln in P['routes']['bus']:
        cand = sorted({frozenset((a, b)) for a, b in zip(ln['path'], ln['path'][1:])}, key=lambda k: (len(use[k]), -SEGBY[k]['len_m']))
        picked = []
        for k in cand:
            s = SEGBY[k]; p = s['pts']; mx, my = (p[0][0] + p[-1][0]) / 2, (p[0][1] + p[-1][1]) / 2
            if s['len_m'] < 50 or any(math.hypot(mx - a, my - b) < 2500 for a, b in picked): continue
            ids = sorted(use[k], key=int); i = ids.index(ln['id']); off = (i - (len(ids) - 1) / 2) * 18
            dx, dy = p[-1][0] - p[0][0], p[-1][1] - p[0][1]; L = math.hypot(dx, dy) or 1; mx += dy / L * off; my -= dx / L * off
            picked.append((mx, my)); out.append((ln, mx, my))
            if len(picked) == 2: break
    return out
def icon_points(P):
    """every icon on the map: (x, y, size in screen px, layer)"""
    out = [(n['x'], n['y'], 18, 'roads') for n in P['nodes'] if JKIND.get(n['kind'])]
    B = P.get('bus')
    if B:
        for st in B['stops']:
            for bb in st.get('bay_list', []): out.append((bb['pole'][0], bb['pole'][1], 15, 'bus'))
            if st.get('kind') == 'end': out.append((st['at'][0] + 40, st['at'][1] - 40, 15, 'bus'))
        x0, y0, x1, y1 = B['terminal']['rect']; out.append(((x0 + x1) / 2, (y0 + y1) / 2, 15, 'bus'))
        for ln, x, y in bus_badges(P): out.append((x, y, 17, 'bus'))
    for st, x, y in station_points(P): out.append((x, y, 15, 'rails'))
    return out
def junction_icons(P, nodes=None, near=None):
    return "<g class='L-roads'>" + ''.join(icon(JKIND[n['kind']], n['x'], n['y']) for n in P['nodes'] if JKIND.get(n['kind']) and (nodes is None or n['id'] in nodes) and inside(near, n['x'], n['y'])) + "</g>"
def bus_marks(P, near=None):
    B = P.get('bus')
    if not B: return ''
    o = []
    for st in B['stops']:
        for bb in st.get('bay_list', []):
            if inside(near, *bb['pole']): o.append(icon('bus', *bb['pole']))
        if st.get('kind') == 'end' and inside(near, *st['at']): o.append(icon('bus', st['at'][0] + 40, st['at'][1] - 40))
    x0, y0, x1, y1 = B['terminal']['rect']
    if inside(near, (x0 + x1) / 2, (y0 + y1) / 2): o.append(icon('bus', (x0 + x1) / 2, (y0 + y1) / 2))
    for ln, x, y in bus_badges(P):
        if inside(near, x, y): o.append(f"<g class='ji' transform='translate({f1(x)} {f1(y)})'><g class='s'><circle r='7.5' fill='{ln['color']}' stroke='#fff' stroke-width='1.6'/><text class='bn' y='3.4'>{e(ln['id'])}</text></g></g>")
    return "<g class='L-bus'>" + ''.join(o) + "</g>"
def temp_icons(P, ids=None, near=None):
    o = []
    for t in P['transition']['stages']:
        for a in t['temp_added']:
            if (ids is None or a['id'] in ids) and inside(near, *a['y']): o.append(icon('temp', *a['y']))
    return "<g class='L-tmp'>" + ''.join(o) + "</g>"

# ---------------------------------------------------------------- the labels: Hebrew names, a constant size on the screen, never on top of each other
# Each label gets the largest zoom (kmax, world px per screen px) at which it is shown: placed by priority at a ladder of zooms,
# a label is shown at k only while nothing of a higher priority (and no icon) is in its box at that zoom. The build checks the result.
LEVELS = [1.5, 2, 3, 4, 5, 6.5, 8, 10, 12.5, 15, 19, 24, 30]
def short(t): return str(t).split(' — ')[0].split(' (')[0].strip()
def label_specs(P, M):
    """every label of the city: (id, x, y, angle, css class, text, box w, box h, box centre offset in screen px, priority, k fit, zone)"""
    L = []; ZS = zone_spots(P, M)
    for z, (nm, k) in ZN.items():
        x, y = ZS[z]
        L.append(dict(id='z-' + z, x=x, y=y, a=0, cls='zid', t=z, w=est(z, 13) + 8, h=14, oy=-5, pr=0, kfit=99, zone=z))
        L.append(dict(id='zn-' + z, x=x, y=y, a=0, cls='znm', t=nm, w=est(nm, 11) + 8, h=13, oy=9, pr=2 if k != 'sea' else 8, kfit=99, zone=z))
    PR = {'main': 1, 'arterial': 1, 'collector': 3, 'local': 5, 'oneway': 5}
    def runs(rd):   # the straight runs of a road: a label may span its junctions — the icons decide where it fits
        sg = [next(s for s in P['segments'] if s['road'] == rd['id'] and {s['a'], s['b']} == {a, b}) for a, b in zip(rd['nodes'], rd['nodes'][1:])]
        out = {}; cur = 0; prev = None
        for s in sg:
            p = s['pts']; d = (round(math.atan2(p[-1][1] - p[0][1], p[-1][0] - p[0][0]), 2) % 3.14) if len(p) == 2 else None
            if prev is not None and (d is None or d != prev): cur += 1
            prev = d; out[s['id']] = cur
        tot = {}
        for s in sg: tot[out[s['id']]] = tot.get(out[s['id']], 0) + plen(s['pts'])
        return {k: tot[v] for k, v in out.items()}
    for rd in P['roads']:
        if rd['cls'] == 'track': continue
        RUN = runs(rd)
        segs = sorted([s for s in P['segments'] if s['road'] == rd['id']], key=lambda s: -s['len_m']); chosen = []
        for s in segs:
            if s['len_m'] < 30: continue
            p = s['pts']; Ls = plen(p); acc = 0
            for i in range(len(p) - 1):
                l = math.hypot(p[i + 1][0] - p[i][0], p[i + 1][1] - p[i][1])
                if acc + l >= Ls / 2:
                    t = (Ls / 2 - acc) / (l or 1); mx = p[i][0] + (p[i + 1][0] - p[i][0]) * t; my = p[i][1] + (p[i + 1][1] - p[i][1]) * t
                    ang = math.degrees(math.atan2(p[i + 1][1] - p[i][1], p[i + 1][0] - p[i][0])); seg_l = l; break
                acc += l
            if any(math.hypot(mx - c[0], my - c[1]) < 1500 for c in chosen): continue
            if ang >= 90: ang -= 180
            if ang < -90: ang += 180
            chosen.append((mx, my)); w = est(rd['name'], 10.5) + 8
            L.append(dict(id=f"r-{sid(s['id'])}", x=mx, y=my, a=ang, cls='rlt', t=rd['name'], w=w, h=13, oy=0, pr=PR.get(rd['cls'], 5), kfit=(min(Ls, seg_l * 2) if s['kind'] == 'bridge' else RUN.get(s['id'], Ls)) / (w + 30), zone=s.get('home')))
    def lot_label(l, pr=7):
        r = l['rect']; t = short(l['label']); w = est(t, 9.5) + 6; h = 12
        L.append(dict(id='l-' + l['id'], x=(r[0] + r[2]) / 2, y=(r[1] + r[3]) / 2, a=0, cls='blt', t=t, w=w, h=h, oy=0, pr=pr, kfit=min((r[2] - r[0]) / w, (r[3] - r[1]) / h), zone=l.get('zone')))
    for i in P.get('sites', []):
        if i['kind'] in ('building', 'court', 'field', 'parking', 'yard', 'park', 'beach', 'plaza', 'lot'): lot_label(i)
    for l in P.get('lots', []): lot_label(l)
    A = P.get('air')
    if A:
        for l in A['lots']:
            if l['kind'] in ('runway', 'taxi', 'building', 'parking', 'yard') or l['id'] in ('AIR-APRON',): lot_label(l, 6)
        L.append(dict(id='air-title', x=7400, y=-430, a=0, cls='aft', t=A['label'], w=est(A['label'], 12.5) + 10, h=16, oy=0, pr=4, kfit=99, zone='G0'))
    I = P.get('island')
    if I:
        for l in I['lots']: lot_label(l, 6)
        L.append(dict(id='isl-title', x=7700, y=7020, a=0, cls='aft', t=I['label'], w=est(I['label'], 12.5) + 10, h=16, oy=0, pr=4, kfit=99, zone='G9'))
    Lk = P['terrain']['lake']
    if 'pts' in Lk:
        t = 'האגם — מורחב אל B1'; L.append(dict(id='lake', x=1755, y=545, a=0, cls='lkt', t=t, w=est(t, 11) + 8, h=14, oy=0, pr=4, kfit=99, zone='B1'))
    if P.get('bus'):
        x0, y0, x1, y1 = P['bus']['terminal']['rect']; t = 'מסוף E3'
        L.append(dict(id='term', x=(x0 + x1) / 2, y=(y0 + y1) / 2, a=0, cls='bt', t=t, w=est(t, 10) + 6, h=13, oy=18, pr=4, kfit=99, zone='E3'))
    RL = {'REF-SPUR': ('מסילת בית הזיקוק', 60, 0), 'SIDING': ('מסילת ההיפוך', 0, -70), 'BYPASS': ('מסילת העקיפה למשא', 0, 0),
          'EAST': ('מסילת הנמל המזרחית', 0, -60), 'W1': ('3 מסילות הרציף', 0, -120), 'ISL-A': ('המסילה לאי — 2 פסים', 120, -40),
          'MAIN-A': ('הקו הראשי — 2 פסים', -95, 0)}
    for r in P.get('rails', []):
        if r['id'] in RL:
            t, dx, dy = RL[r['id']]; p = r['pts']
            m = {'W1': [3100, 5120], 'EAST': [8100, 5120], 'BYPASS': [6000, 3900], 'MAIN-A': [5800, 3150], 'SIDING': [7200, 5085]}.get(r['id'], p[len(p) // 2])
            L.append(dict(id='rl-' + r['id'], x=m[0] + dx, y=m[1] + dy, a=0, cls='blt', t=t, w=est(t, 9.5) + 6, h=12, oy=0, pr=6, kfit=99, zone=None))
    for st, x, y in station_points(P):
        t = dict(RST).get(st['id'], short(st['label']))
        L.append(dict(id='st-' + st['id'], x=x, y=y, a=0, cls='blt', t=t, w=est(t, 9.5) + 6, h=12, oy=17, pr=5, kfit=99, zone=None))
    return L
def box_at(l, k):
    """the label's box in world coordinates at zoom k"""
    w, h = l['w'] * k, l['h'] * k; cx, cy = l['x'], l['y'] + l['oy'] * k
    a = math.radians(l['a'])
    if abs(math.sin(a)) < 1e-6: return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    if abs(math.cos(a)) < 1e-6: return (cx - h / 2, cy - w / 2, cx + h / 2, cy + w / 2)
    ex = abs(math.cos(a)) * w / 2 + abs(math.sin(a)) * h / 2; ey = abs(math.sin(a)) * w / 2 + abs(math.cos(a)) * h / 2
    return (cx - ex, cy - ey, cx + ex, cy + ey)
def hit(a, b, pad=0): return a[0] < b[2] - pad and b[0] < a[2] - pad and a[1] < b[3] - pad and b[1] < a[3] - pad
def label_layout(P):
    """place every label and give it its zoom limit; then count the overlaps at every zoom of the ladder (the check: 0)"""
    M = model(P); L = label_specs(P, M); IC = icon_points(P)
    order = sorted(range(len(L)), key=lambda i: (L[i]['pr'], -L[i]['kfit'] if L[i]['kfit'] < 99 else 0, L[i]['id']))
    placed = {}
    for k in LEVELS:
        G = {}; cell = 220 * k
        def cells(b): return [(i, j) for i in range(int(b[0] // cell), int(b[2] // cell) + 1) for j in range(int(b[1] // cell), int(b[3] // cell) + 1)]
        for x, y, sz, lay in IC:
            b = (x - sz * k / 2, y - sz * k / 2, x + sz * k / 2, y + sz * k / 2)
            for c in cells(b): G.setdefault(c, []).append(b)
        ok = set()
        for i in order:
            l = L[i]
            if k > l['kfit']: continue
            b = box_at(l, k); cs = cells(b)
            if any(hit(b, q) for c in cs for q in G.get(c, [])): continue
            ok.add(i)
            for c in cs: G.setdefault(c, []).append(b)
        placed[k] = ok
    for i, l in enumerate(L):
        km = 0
        for k in LEVELS:
            if i in placed[k]: km = k
            else: break
        l['kmax'] = km
    # the check: at every zoom of the ladder, the labels shown do not overlap each other or an icon
    over = 0; shown = {}
    for k in LEVELS:
        S = [i for i, l in enumerate(L) if l['kmax'] >= k]; shown[k] = len(S)
        boxes = [box_at(L[i], k) for i in S]
        icb = [(x - sz * k / 2, y - sz * k / 2, x + sz * k / 2, y + sz * k / 2) for x, y, sz, lay in IC]
        for a in range(len(boxes)):
            for b in range(a + 1, len(boxes)):
                if hit(boxes[a], boxes[b]): over += 1
            if any(hit(boxes[a], q) for q in icb): over += 1
    out = [dict(id=l['id'], x=round(l['x'], 1), y=round(l['y'], 1), a=round(l['a']), cls=l['cls'], t=l['t'], oy=l['oy'], kmax=l['kmax'], zone=l['zone']) for l in L]
    return dict(labels=out, overlaps=over, n=len(L), never=sum(1 for l in L if not l['kmax']), shown={str(k): v for k, v in shown.items()}, levels=LEVELS)
BASE = {'zid': 4.5, 'znm': 3.9, 'rlt': 3.7, 'blt': 3.3, 'aft': 4.4, 'lkt': 3.9, 'bt': 3.5}   # the baseline under the centre of the box, by the font size
def labels_svg(P, near=None, keep=None):
    """the label layer of one map (the names layer): the labels inside its view, each with its zoom limit"""
    o = []
    for l in P.get('labels', {}).get('labels', []):
        if not l['kmax'] or not inside(near, l['x'], l['y']) or (keep and not keep(l)): continue
        tr = f"translate({f1(l['x'])} {f1(l['y'])})" + (f" rotate({l['a']})" if l['a'] else '')
        o.append(f"<g class='lb' data-k='{l['kmax']}' transform='{tr}'><g class='s'><text class='{l['cls']}' y='{f1(l['oy'] + BASE.get(l['cls'], 3.5))}'>{e(l['t'])}</text></g></g>")
    return "<g class='L-names'>" + ''.join(o) + "</g>"

# ---------------------------------------------------------------- the maps
TOGGLES = [('roads', 'כבישים'), ('rails', 'מסילות'), ('lots', 'מגרשים'), ('bus', 'קווי אוטובוס'), ('names', 'שמות')]
def city_svg(P, M):
    tools = ''.join(f"<button type='button' class='lt' data-l='{k}' aria-pressed='true'><span class='sw sw-{k}'></span>{e(t)}</button>" for k, t in TOGGLES)
    return ("<div class='maptools' role='group' aria-label='שכבות המפה'>" + tools + "</div>"
            "<div class='mapbox' id='cityMap'><div class='mapctl'><button type='button' data-z='in' aria-label='הגדלה'>+</button><button type='button' data-z='out' aria-label='הקטנה'>−</button>"
            "<button type='button' data-z='home' aria-label='כל העיר'>⌂</button></div>"
            "<svg class='m city' viewBox='-200 -950 9900 8800' preserveAspectRatio='xMidYMid meet' role='img' aria-label='מפת העתיד של העיר'>"
            "<use href='#terrain'/><use class='L-lots' href='#lots'/><use class='L-roads' href='#roads'/><use class='L-rails' href='#rails'/><use class='L-bus' href='#bus'/>"
            + junction_icons(P) + bus_marks(P) + rail_marks(P) + labels_svg(P) + "</svg><div class='tip' hidden></div></div>")
def segs_use(ids, sx=()):
    """the network segments (three passes) and the inner roads / aprons sx between the bases and the carriageways"""
    return (''.join(f"<use href='#b-{i}'/>" for i in ids) + ''.join(f"<use href='#sx-{i}'/>" for i in sx) + ''.join(f"<use href='#c-{i}'/>" for i in ids)
            + ''.join(f"<use href='#l-{i}'/>" for i in ids) + ''.join(f"<use href='#l-s-{i}'/>" for i in sx if not i.startswith('a-')))
def sx_of(P, zones):
    return [sid(r['id']) for r in P.get('site_roads', []) if r['zone'] in zones] + ['a-' + i['id'] for i in P.get('sites', []) if i.get('apron') and i['zone'] in zones]
def zone_svg(P, M, z, Z):
    x0, y0, x1, y1 = zrect(z); m = 450; vb = (x0 - m, y0 - m, x1 + m, y1 + m)
    own = [sid(s) for s in Z['segments']]; srd = sx_of(P, {z})
    return (f"<svg class='m' viewBox='{vb[0]} {vb[1]} {vb[2] - vb[0]} {vb[3] - vb[1]}' role='img' aria-label='{e(z)} — {e(ZN[z][0])}'>"
            f"<use href='#terrain'/><use class='L-lots' href='#lots'/><g class='L-roads'><g opacity='.35'><use href='#roads'/></g>{segs_use(own, srd)}<use href='#jx'/></g>"
            f"<use class='L-rails' href='#rails'/><use class='L-bus' href='#bus'/>"
            f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' class='zone' vector-effect='non-scaling-stroke'/>"
            + junction_icons(P, near=vb) + bus_marks(P, near=vb) + rail_marks(P, near=vb) + labels_svg(P, near=vb) + "</svg>")
def site_svg(P, M, z):
    x0, y0, x1, y1 = zrect(z); m = 160; vb = (x0 - m, y0 - m, x1 + m, y1 + m)
    return (f"<svg class='m' viewBox='{vb[0]} {vb[1]} {vb[2] - vb[0]} {vb[3] - vb[1]}' role='img' aria-label='{e(z)} מבפנים'>"
            f"<use href='#terrain'/><use class='L-lots' href='#lots'/><use class='L-roads' href='#roads'/><use class='L-rails' href='#rails'/><use class='L-bus' href='#bus'/>"
            f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' class='zone' vector-effect='non-scaling-stroke'/>"
            + junction_icons(P, near=vb) + bus_marks(P, near=vb) + rail_marks(P, near=vb) + labels_svg(P, near=vb) + "</svg>")
def view_svg(P, M, vb, label):
    """a close view of a part of the map (the airport, the island, the port) — the same layers as the main map"""
    return (f"<svg class='m' viewBox='{vb[0]} {vb[1]} {vb[2] - vb[0]} {vb[3] - vb[1]}' role='img' aria-label='{e(label)}'>"
            f"<use href='#terrain'/><use class='L-lots' href='#lots'/><use class='L-roads' href='#roads'/><use class='L-rails' href='#rails'/><use class='L-bus' href='#bus'/>"
            + junction_icons(P, near=vb) + bus_marks(P, near=vb) + rail_marks(P, near=vb) + labels_svg(P, near=vb) + "</svg>")
def stage_svg(P, M, k):
    st = P['transition']['stages']; SI = {t['stage']: i for i, t in enumerate(st)}; t = st[k]
    gone = set(x for tt in st[:k + 1] for x in tt['removed'])
    built = [sid(s['id']) for s in P['segments'] if SI[s['stage']] <= k]
    done = set(z for tt in st[:k + 1] for z in tt['zones'])
    srd = [x for x in sx_of(P, done) if not x.startswith('DW-') or any(l['id'] == x[3:] and l['zone'] in done for l in P.get('lots', [])) or any(d['id'] == x for d in P['driveways'] if d['zone'] in done)]
    vb = "-100 -950 9800 8800" if t['stage'] == 'S13' else "-100 -950 6800 6350"
    o = [f"<svg class='m' viewBox='{vb}' role='img' aria-label='{e(t['stage'])}'><use href='#terrain'/>"]
    o.append("<g class='L-roads'>" + segs_use(built, srd) + "</g>")
    o.append("<use class='L-rails' href='#rails'/>")
    o.append("<g class='L-roads'>" + ''.join(f"<use href='#od-{e(ed)}'/>" for ed in P['_old_ids'] if ed not in gone) + "</g>")
    tl = []; live = set()
    for tt in st[:k + 1]:
        for a in tt['temp_added']:
            if a['until'] and SI[a['until']] <= k: continue
            tl.append(f"<use href='#tp-{e(a['id'])}'/>"); live.add(a['id'])
    o.append("<g class='L-roads'>" + ''.join(tl) + "</g>")
    bn = {x for s in P['segments'] if SI[s['stage']] <= k for x in (s['a'], s['b'])}
    for zz in t['zones']:
        x0, y0, x1, y1 = zrect(zz); o.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' class='zone zst' vector-effect='non-scaling-stroke'/>")
    o.append(temp_icons(P, ids=live).replace("L-tmp", "L-roads") + junction_icons(P, nodes=bn))
    o.append(labels_svg(P, keep=lambda l: l['id'] in {'z-' + z for z in t['zones']}))
    o.append("</svg>")
    return ''.join(o)

# ---------------------------------------------------------------- the legend: one, short
def xsec(CLS, key, label, dims):
    g = geom(CLS, key)
    b, c, l = road_parts('lg-' + key, [[0, 0], [900, 0]], g)
    strip = (b + c + l).replace(" id='", " data-id='")
    return (f"<div class='lgx'><svg viewBox='0 -160 900 320' class='lgs' aria-hidden='true'>{strip}</svg>"
            f"<div><b>{e(label)}</b><div class='small mut'>{e(dims)}</div></div></div>")
def legend_html(P, M):
    CLS = P['classes']
    def dims(c):
        x = CLS[c]; ln = {1: 'נתיב', 2: '2 נתיבים', 3: '3 נתיבים'}[x['dirN']] + f" של {x['lane_m']}"; parts = []
        if x['walk_m']: parts.append(f"מדרכה {x['walk_m']}")
        parts.append(ln)
        if x['median_m']: parts.append(f"חציון {x['median_m']}")
        if x['twoway']: parts.append(ln)
        if x['walk_m']: parts.append(f"מדרכה {x['walk_m']}")
        return ' · '.join(parts)
    rows = [('main', f"עורק ראשי 3+3 — {CLS['main']['width_m']} מ׳"), ('arterial', f"עורק 2+2 — {CLS['arterial']['width_m']} מ׳"),
            ('collector', f"מאסף 1+1 — {CLS['collector']['width_m']} מ׳"), ('local', f"מקומי 1+1 — {CLS['local']['width_m']} מ׳"),
            ('oneway', f"חד-סטרי, נתיב אחד — {CLS['oneway']['width_m']} מ׳"), ('track', f"דרך עפר — {CLS['track']['width_m']} מ׳")]
    lines = ''.join(f"<span class='lgc'><svg viewBox='0 0 40 14'><line x1='2' y1='7' x2='38' y2='7' stroke='#fff' stroke-width='5'/><line x1='2' y1='7' x2='38' y2='7' stroke='{l['color']}' stroke-width='3'/></svg>{e(l['id'])}</span>" for l in P['routes']['bus'])
    o = ["<div class='legend'><div class='lgh'>מקרא</div><div class='lgrid'>"]
    o += [xsec(CLS, k, t, dims(k)) for k, t in rows]
    o.append("</div><div class='lgrid lg2'>")
    o.append("<div class='lgi'><span class='lgic3'>" + ''.join(f"<svg viewBox='-10 -10 20 20' class='lgic'>{ICON[k]}</svg>" for k in ('signal', 'roundabout', 'stop', 'riro')) + "</span>"
             "<span><b>צמתים:</b> רמזור עם חץ שמאלה · כיכר · עצור / זכות קדימה · ימינה בלבד</span></div>")
    o.append(f"<div class='lgi'><svg viewBox='-10 -10 20 20' class='lgic'>{ICON['bus']}</svg><span><b>תחנת אוטובוס</b> במפרץ · קווים {lines}</span></div>")
    o.append("<div class='lgi'><svg viewBox='0 0 60 26' class='lgo' style='height:26px'><polyline points='2,4 58,4' stroke='#3a3a3a' stroke-width='5'/><polyline points='2,4 58,4' stroke='#f2efe5' stroke-width='1.2' stroke-dasharray='4 3'/>"
             "<polyline points='2,13 58,13' stroke='#7b4a1e' stroke-width='5' stroke-dasharray='9 4'/><polyline points='2,22 58,22' stroke='#3a3a3a' stroke-width='5'/><polyline points='2,22 58,22' stroke='#0e8f86' stroke-width='2.4' stroke-dasharray='6 3'/></svg>"
             f"<svg viewBox='-10 -10 20 20' class='lgic'>{ICON['train']}</svg>"
             "<span><b>מסילה</b> — קיימת · מסילת משא (חום; מקווקו — עתידית) · קו הנוסעים (טורקיז) · תחנה; פס אדום — בולמים, X — מחסום, מסגרת — גשר רכבת</span></div>")
    o.append("<div class='lgi'><svg viewBox='0 0 60 20' class='lgo'><rect x='2' y='3' width='17' height='14' fill='#8e9aa8' stroke='#556'/><rect x='22' y='3' width='17' height='14' fill='#f3dfb8' stroke='#6d6a63'/>"
             "<rect x='42' y='3' width='16' height='14' fill='#d6dade' stroke='#556'/><rect x='2' y='3' width='56' height='14' fill='url(#futp)' class='fut' style='stroke-width:1'/></svg>"
             "<span><b>מגרש</b> — מבנה · מגרש לפי השימוש · חניון; <b>פסים ומקווקו — עתידי, עוד לא בנוי</b> (כל הרשת החדשה עתידית)</span></div>")
    o.append("<div class='lgi'><svg viewBox='0 0 60 20' class='lgo'><rect x='4' y='3' width='52' height='14' fill='#e0eaf2' stroke='#55657a' stroke-width='1.2'/><text x='30' y='14' class='lgt'>A2</text></svg>"
             "<span><b>אזור</b> — גבול, מזהה ושם</span></div>")
    o.append("</div></div>")
    return ''.join(o)

def temp_svg(a):
    x0, y0 = a['x']; x1, y1 = a['y']; tid = e(a['id'])
    if math.hypot(x1 - x0, y1 - y0) < 20:
        return f"<g id='tp-{tid}'><circle cx='{f1(x0)}' cy='{f1(y0)}' r='22' class='tmpd'/></g>"
    p = f"{f1(x0)},{f1(y0)} {f1(x1)},{f1(y1)}"
    return (f"<g id='tp-{tid}'><polyline points='{p}' class='rk' stroke='#b0177f' stroke-width='134'/><polyline points='{p}' class='rk' stroke='#f7cdea' stroke-width='128'/>"
            f"<polyline points='{p}' class='tmpl' vector-effect='non-scaling-stroke'/><circle cx='{f1(x0)}' cy='{f1(y0)}' r='26' class='tmpd'/></g>")


def bus_layer(P, M):
    B = P.get('bus'); lines = P['routes']['bus']
    if not B: return ''
    SEGBY = {frozenset((s['a'], s['b'])): s for s in P['segments']}
    use = {}
    for ln in lines:
        for a, b in zip(ln['path'], ln['path'][1:]):
            k = frozenset((a, b))
            if ln['id'] not in use.setdefault(k, []): use[k].append(ln['id'])
    o = ["<g id='bus'>"]
    T = B['terminal']; x0, y0, x1, y1 = T['rect']; R = T['corner_r']   # the terminal: the yard, the platforms, 12 bays, the holding lane
    o.append(f"<rect x='{x0 - 3}' y='{y0 - 3}' width='{x1 - x0 + 6}' height='{y1 - y0 + 6}' rx='{R}' fill='#6f6b62'/><rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' rx='{R}' fill='#5b636e'/>")
    for pf in T['platforms']: o.append(rect_el(pf['rect'], '#e9e2cf', "stroke='#fff' stroke-width='4'"))
    for b in T['bays']:
        bx0, by0, bx1, by1 = b['rect']
        o.append(f"<rect x='{bx0 + 8}' y='{by0 + 3}' width='{bx1 - bx0 - 16}' height='{by1 - by0 - 6}' fill='none' stroke='#f2c200' stroke-width='4'/><text x='{(bx0 + bx1) / 2}' y='{(by0 + by1) / 2 + 9}' class='bayn'>{b['no']}</text>")
    for h in T['hold']:
        hx0, hy0, hx1, hy1 = h['rect']
        o.append(f"<rect x='{hx0 + 6}' y='{hy0}' width='{hx1 - hx0 - 12}' height='{hy1 - hy0}' fill='#f2c200' fill-opacity='.35' stroke='#f2c200' stroke-width='4' stroke-dasharray='16 10'/>")
    o.append(f"<text x='{(T['hold'][0]['rect'][0] + T['hold'][-1]['rect'][2]) / 2}' y='{T['hold'][0]['rect'][3] - 8}' class='bayn'>המתנה</text>")
    gx, gy = T['gate']; o.append(f"<rect x='{gx - 45}' y='{gy - 4}' width='90' height='14' fill='#5b636e'/>")
    for st in B['stops']:
        for bb in st.get('bay_list', []):
            o.append(f"<polygon points='{pts(bb['poly'])}' class='bay'/>")
    for ln in lines:
        for a, b in zip(ln['path'], ln['path'][1:]):
            k = frozenset((a, b)); s = SEGBY[k]; ids = sorted(use[k], key=lambda x: int(x)); n = len(ids); i = ids.index(ln['id'])
            p = s['pts']
            off = (i - (n - 1) / 2) * 18
            q = offset(p, off) if off else p
            o.append(f"<polyline points='{pts(q)}' class='busc' vector-effect='non-scaling-stroke'/><polyline points='{pts(q)}' class='busl' stroke='{ln['color']}' vector-effect='non-scaling-stroke'/>")
    o.append("</g>")
    return ''.join(o)


STYLE = """
.sea{fill:#bcd8ee}.isl{fill:#e7e0c6;stroke:#9fb3c4;stroke-width:10}.lake{fill:#9ec7e6;stroke:#6f9fc4;stroke-width:6}.lakef{fill:none;stroke:#2f6ea8;stroke-width:1.4;stroke-dasharray:5 3}
.zb{stroke:#4f5f74;stroke-width:1.15;opacity:.55}.rail{fill:none;stroke:#3f3f3f;stroke-width:34}.rail2{fill:none;stroke:#f2efe5;stroke-width:8;stroke-dasharray:40 40}
.railf{fill:none;stroke:#6a6a6a;stroke-width:34;stroke-dasharray:90 45;opacity:.85}
.rk{fill:none;stroke-linecap:butt;stroke-linejoin:round}.zeb{stroke-dasharray:6 6;opacity:.95}.ln{fill:none;stroke-width:3.5;stroke-dasharray:30 45;stroke-linecap:butt}
.arw{fill:none;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.fut{fill:url(#futp);stroke:#5b5346;stroke-width:1.3;stroke-dasharray:5 3}
.old{stroke:#6f6a62;stroke-width:1.5;stroke-dasharray:6 4;fill:none}.oldk{stroke:#2e2e2e;stroke-width:1.7;stroke-dasharray:2 2.5;fill:none}
.tmpl{stroke:#b0177f;stroke-width:1.6;stroke-dasharray:5 3;fill:none}.tmpd{fill:#b0177f}
.padh{font:700 120px system-ui;text-anchor:middle;fill:#333}.afence{stroke:#3d3d3d;stroke-width:1.2;stroke-dasharray:1.5 2.5}.cable{fill:none;stroke:#2f6fd0;stroke-width:2;stroke-dasharray:6 3}
.bay{fill:#5b636e;stroke:#f2c200;stroke-width:4;stroke-dasharray:14 10}
.busc{fill:none;stroke:#fff;stroke-width:5.2;stroke-linecap:round;stroke-linejoin:round;opacity:.9}.busl{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.zone{fill:none;stroke:#1d5fa8;stroke-width:3}.zst{fill:#1d5fa8;fill-opacity:.07}
.m .s{transform:scale(var(--k,10))}.m text{direction:rtl}
.zid{font:700 13px ui-monospace,Menlo,Consolas,monospace;fill:#183a6b;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:3.4px;stroke-linejoin:round;direction:ltr}
.znm{font:600 11px system-ui,"Segoe UI",Arial,sans-serif;fill:#25292e;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:3.2px;stroke-linejoin:round}
.rlt{font:600 10.5px system-ui,"Segoe UI",Arial,sans-serif;fill:#141414;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round}
.blt{font:600 9.5px system-ui,sans-serif;fill:#1b1f24;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:2.6px;stroke-linejoin:round}
.aft{font:700 12.5px system-ui,sans-serif;fill:#7a3b00;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:3.4px}
.lkt{font:italic 700 11px system-ui,sans-serif;fill:#1d5a93;text-anchor:middle;paint-order:stroke;stroke:#eaf3fb;stroke-width:3px}
.bayn{font:700 26px system-ui,sans-serif;fill:#fff;text-anchor:middle;direction:rtl}.bn{font:700 9.5px system-ui,sans-serif;fill:#fff;text-anchor:middle;direction:ltr}.bt{font:700 10px system-ui,sans-serif;fill:#1f4fa8;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:3px}
.lb.hid{display:none}.m .lb,.m .ji{pointer-events:none}
.mapbox{position:relative;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#f3f0e7;touch-action:none;height:clamp(420px,80vh,920px)}
.mapbox svg{display:block;width:100%;height:100%;cursor:grab}.mapbox svg:active{cursor:grabbing}
.mapctl{position:absolute;top:8px;left:8px;display:flex;gap:6px;direction:ltr;z-index:2}
.mapctl button{font:600 18px system-ui;width:38px;height:38px;border-radius:8px;border:1px solid #888;background:#fff;color:#222;cursor:pointer}
.maptools{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}
.lt{display:inline-flex;align-items:center;gap:6px;font:600 13px system-ui,sans-serif;padding:6px 10px;border-radius:18px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer;min-height:34px}
.lt[aria-pressed='false']{opacity:.5;text-decoration:line-through}.lt .sw{width:18px;height:10px;border-radius:2px;display:inline-block}
.sw-roads{background:linear-gradient(#9c1c1c 0 33%,#d9572f 33% 66%,#eda63a 66%)}.sw-rails{background:repeating-linear-gradient(90deg,#3f3f3f 0 6px,#f2efe5 6px 9px);height:6px!important}
.sw-lots{background:#f3dfb8;border:1px solid #6d6a63}.sw-bus{background:linear-gradient(90deg,#1f5fd1 0 33%,#0f8f8a 33% 66%,#2e9e3e 66%)}.sw-names{background:#fff;border:1px solid #555}
.off-roads .L-roads,.off-rails .L-rails,.off-lots .L-lots,.off-bus .L-bus,.off-names .L-names{display:none}
.tip{position:absolute;z-index:3;max-width:min(340px,80%);background:#fff;color:#1f2328;border:1px solid #888;border-radius:8px;padding:7px 9px;font:13px/1.45 system-ui,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.18);pointer-events:none}
.tip b{font-weight:700}.tip .tl{color:#5a6068;font-size:12px}.tip hr{border:0;border-top:1px solid #ddd;margin:5px 0}
.zc svg,.sm svg,.vw svg{display:block;width:100%;height:auto;border-radius:6px;background:#f3f0e7}
.legend{background:#fbfaf6;color:#1f2328;border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:10px 0}
.lgh{font-weight:700;margin-bottom:6px}.lgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:8px 14px}.lg2{margin-top:10px;border-top:1px solid #e3dfd4;padding-top:10px}
.lgx{display:flex;gap:10px;align-items:center}.lgs{width:120px;height:43px;flex:none;background:#f3f0e7;border-radius:4px}
.lgi{display:flex;gap:8px;align-items:center;font-size:13px}.lgo{width:60px;height:20px;flex:none}.lgic{width:20px;height:20px;flex:none}.lgic3{display:inline-flex;gap:3px;flex:none}
.lgc{display:inline-flex;align-items:center;gap:2px;margin-inline-start:6px;font-weight:700}.lgc svg{width:26px;height:10px}
.lgt{font:700 9px ui-monospace,monospace;text-anchor:middle;fill:#183a6b;direction:ltr}.legend .mut{color:#5d646c}
"""

def hover_data(P, GR, M):
    """the hover card: line pieces [x1,y1,x2,y2,half width,info], points, rectangles; each text once"""
    CLS = M['CLS']; RD = M['RD']; info = []; idx = {}
    def I(h):
        if h not in idx: idx[h] = len(info); info.append(h)
        return idx[h]
    def r1(v): return round(v, 1)
    segs = []
    for s in P['segments']:
        rd = RD[s['road']]; c = CLS[s['cls']]; g = M['G'][s['id']]
        t = I(f"<b>{e(rd['name'])}</b> <span class='tl'>({e(rd['id'])})</span><div>{e(c['he'])}{' (גשר)' if s['kind'] == 'bridge' else ''} · {e(c['lanes'])} — {e(c['lanesHe'])}</div>"
              f"<div class='tl'>רוחב {c['width_m']} מ׳ · קטע {e(s['id'])}, {s['len_m']:.0f} מ׳ · נבנה בשלב {e(s['stage'])}</div>")
        for i in range(len(s['pts']) - 1): segs.append([r1(s['pts'][i][0]), r1(s['pts'][i][1]), r1(s['pts'][i + 1][0]), r1(s['pts'][i + 1][1]), g['tw'] / 2, t])
    for r in P.get('site_roads', []):
        cl = r.get('cls'); kind = CLS[cl]['he'] + ' · ' + CLS[cl]['lanes'] if cl in CLS else ('כניסה למגרש — הנמכת שפה' if cl == 'driveway' else 'שביל שירות בתוך מגרש — נתיב אחד')
        t = I(f"<b>{e(r['label'])}</b><div>{e(kind)}</div><div class='tl'>{'אל ' + e(RD[r['road']]['name']) + ' — לא צומת' if r['kind'] == 'driveway' and r.get('road') in RD else e(r['zone'] or '')}</div>")
        for i in range(len(r['pts']) - 1): segs.append([r1(r['pts'][i][0]), r1(r['pts'][i][1]), r1(r['pts'][i + 1][0]), r1(r['pts'][i + 1][1]), r['hw'], t])
    for r in P.get('air', {}).get('roads', []):
        t = I(f"<b>{e(r['label'])}</b><div>השדה העתידי (שלב 8) · {'חד-סטרי, 2 נתיבים' if r['oneway'] else '2 נתיבים'}</div>")
        for i in range(len(r['pts']) - 1): segs.append([r['pts'][i][0], r['pts'][i][1], r['pts'][i + 1][0], r['pts'][i + 1][1], 59, t])
    KH = {'signal': 'רמזור עם חץ שמאלה', 'roundabout': 'כיכר', 'riro': 'ימינה בלבד', 'stop': 'עצור / זכות קדימה', 'gate': 'שער השדה',
          'bridgehead': 'ראש הגשר', 'plaza': 'רחבה', 'end': 'קצה', 'corner': 'פינה'}
    nodes = []; SG = {x['node']: x for x in P['signals']}
    for n in P['nodes']:
        if n['kind'] == 'corner': continue
        roads = sorted({RD[x['road']]['name'] for x in M['deg'].get(n['id'], [])})
        t = f"<b>{e(n['label'])}</b> <span class='tl'>({e(n['id'])})</span><div>{e(KH.get(n['kind'], n['kind']))}{' · ' + e(' × '.join(roads)) if len(roads) > 1 else ''}</div>"
        if n['id'] in SG:
            sg = SG[n['id']]
            t += "<div class='tl'>" + ''.join(f"<div>• מ<b>{e(RD[a['road']]['name'])}</b> (<bdi>{e(a['from'])}</bdi>): {a['through']} ישר" + (' + נתיב שמאלה עם חץ' if a['left'] else ' (הגישה של השדה)') + "</div>" for a in sg['approaches']) + "</div>"
            t += "<div class='tl'>מופעים: " + e(' → '.join(sg['phases'])) + " · עדיפות לחירום</div>"
        if n.get('why'): t += f"<div class='tl'>{e(n['why'])}</div>"
        nodes.append([n['x'], n['y'], 175 if n['kind'] == 'roundabout' else 60, I(t)])
    LN = {l['id']: l for l in P['routes']['bus']}; stops = []; bus = []
    def chips(ids): return ' '.join(f"<span style='display:inline-block;min-width:16px;padding:0 4px;border-radius:8px;background:{LN[i]['color']};color:#fff;font-weight:700;text-align:center'>{e(i)}</span>" for i in ids)
    for st in P.get('bus', {}).get('stops', []):
        for bb in st.get('bay_list', []):
            stops.append([bb['pole'][0], bb['pole'][1], 60, I(f"<b>תחנה: {e(st['name'])}</b> <span class='tl'>({e(st['id'])})</span><div>קווים {chips(sorted(st['lines'], key=int))}</div>"
                                                            f"<div class='tl'>{e(RD[st['road']]['name'])} · לכיוון {e(bb['toward'])} · מפרץ 15 מ׳, {bb['to_junction_m']} מ׳ ממרכז הצומת</div>")])
        if st.get('kind') == 'end':
            stops.append([st['at'][0] + 40, st['at'][1] - 40, 80, I(f"<b>תחנה סופית: {e(st['name'])}</b><div>קווים {chips(sorted(st['lines'], key=int))}</div>")])
    if P.get('bus'):
        x0, y0, x1, y1 = P['bus']['terminal']['rect']; stops.append([(x0 + x1) / 2, (y0 + y1) / 2, 170, I(f"<b>{e(P['bus']['terminal']['label'])}</b><div>כל הקווים: {chips([l['id'] for l in P['routes']['bus']])}</div>")])
    SEGBY = {frozenset((s['a'], s['b'])): s for s in P['segments']}
    for ln in P['routes']['bus']:
        t = I(f"<b>קו {e(ln['id'])} — {e(ln['name'])}</b><div>{'בשני הכיוונים' if ln['twoway'] else 'לולאה בכיוון אחד'} · {ln['len_km']} ק״מ · כל {ln['headway_s']} שנ׳ · {ln['buses']} אוטובוסים</div><div class='tl'>{e(ln['why'])}</div>")
        for a, b in zip(ln['path'], ln['path'][1:]):
            sg = SEGBY[frozenset((a, b))]['pts']
            for i in range(len(sg) - 1): bus.append([r1(sg[i][0]), r1(sg[i][1]), r1(sg[i + 1][0]), r1(sg[i + 1][1]), 30, t])
    rails = []
    for r in P.get('rails', []):
        t = I(f"<b>{e(r['label'])}</b><div class='tl'>{'קיימת היום' if r['state'] == 'today' else 'עתידית — שלב ' + e(r.get('stage', ''))}</div>")
        for i in range(len(r['pts']) - 1): rails.append([r['pts'][i][0], r['pts'][i][1], r['pts'][i + 1][0], r['pts'][i + 1][1], 20, t])
    lots = []
    def lot_info(l, extra=''):
        ac = l.get('access'); at = ''
        if ac: at = f"<div>הגישה מ<b>{e(ac['road_name'])}</b>" + (f" — דרך {e(ac['through'])}" if ac.get('through') else '') + "</div>"
        st = "עתידי — שלב " + e(l.get('stage') or ZSTAGE.get(l.get('zone'), '')) if l.get('future', True) else 'קיים'
        return I(f"<b>{e(l['label'])}</b>{at}<div class='tl'>{e(l['id'])} · {e(l.get('zone') or '')} · {st}{extra}</div>")
    ZSTAGE = {z: Z.get('stage') or '' for z, Z in P['zones'].items()}
    for i in sorted(P.get('sites', []), key=lambda i: 0 if i['kind'] in ('house', 'pad') else 1):
        if i['kind'] in ('site', 'path') or i.get('apron'): continue
        rc = (i['c'][0] - i['safety'], i['c'][1] - i['safety'], i['c'][0] + i['safety'], i['c'][1] + i['safety']) if i['kind'] == 'pad' else tuple(i['rect'])
        lots.append(list(rc) + [lot_info(i if i['kind'] != 'house' else dict(i, label='הבית של ' + i['parent'], access=next((q.get('access') for q in P['sites'] if q['id'] == i['parent']), None)))])
    for l in P.get('lots', []): lots.append(list(l['rect']) + [lot_info(l)])
    for l in P.get('island', {}).get('lots', []): lots.append(list(l['rect']) + [lot_info(l)])
    for l in sorted(P.get('air', {}).get('lots', []), key=lambda l: (l['rect'][2] - l['rect'][0]) * (l['rect'][3] - l['rect'][1])): lots.append(list(l['rect']) + [lot_info(l, ' · השדה העתידי, חלק ו')])
    lake = None; L = P['terrain']['lake']
    if 'pts' in L:
        lake = dict(pts=[[r1(x), r1(y)] for x, y in L['pts']], info=I(f"<b>האגם — אגם אחד מ-B2 אל B1</b><div>{L['area_m2']:,} מ״ר (היום {L['today_m2']:,}), מהם {L['b1_m2']:,} ב-B1</div><div class='tl'>D‑13, GATE‑100 · החלק המפוספס — ההרחבה העתידית</div>"))
    zones = []
    for z, (nm, k) in ZN.items():
        x0, y0, x1, y1 = zrect(z); Z = P['zones'].get(z, {})
        zones.append([x0, y0, x1, y1, I(f"<b>{e(z)} — {e(nm)}</b><div class='tl'>{e(Z.get('purpose', ''))}{' · שלב ' + e(Z['stage']) if Z.get('stage') else ''}</div>")])
    D = dict(info=info, segs=segs, nodes=nodes, stops=stops, bus=bus, rails=rails, lots=lots, lake=lake, zones=zones)
    return "<script>window.__MAP=" + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ";</script>"

ZOOM_JS = """
<script>
(function(){
function K(svg){const vb=svg.viewBox.baseVal,w=svg.getBoundingClientRect().width||1,k=vb.width/w;svg.style.setProperty('--k',k.toFixed(3));
 svg.querySelectorAll('.lb').forEach(g=>g.classList.toggle('hid',k>+g.dataset.k));return k}
const all=[...document.querySelectorAll('svg.m')];
function kAll(){all.forEach(K)}
if('ResizeObserver' in window){const ro=new ResizeObserver(es=>es.forEach(x=>K(x.target)));all.forEach(s=>ro.observe(s))}else{addEventListener('resize',kAll)}
kAll();
// the layer buttons — for every map on the page
document.querySelectorAll('.lt').forEach(b=>b.addEventListener('click',()=>{const on=b.getAttribute('aria-pressed')!=='false';b.setAttribute('aria-pressed',on?'false':'true');document.body.classList.toggle('off-'+b.dataset.l,on)}));
// the city map: wheel, drag and pinch to zoom and pan, the buttons, and the hover (or tap) card
const box=document.getElementById('cityMap');if(!box)return;const svg=box.querySelector('svg'),tip=box.querySelector('.tip');
const HOME=[-200,-950,9900,8800],CORE=[-150,-900,7450,6200];let v=HOME.slice();
function asp(){const r=svg.getBoundingClientRect();return (r.height||1)/(r.width||1)}
function fit(x){let [a,b,w,h]=x;const s=asp();if(h/w>s){const nw=h/s;a-=(nw-w)/2;w=nw}else{const nh=w*s;b-=(nh-h)/2;h=nh}return [a,b,w,h]}
function set(){svg.setAttribute('viewBox',v.map(n=>n.toFixed(1)).join(' '));K(svg)}
function zoom(f,cx,cy){const nw=Math.min(HOME[2]*1.8,Math.max(450,v[2]*f)),s=nw/v[2];v=[cx-(cx-v[0])*s,cy-(cy-v[1])*s,nw,v[3]*s];set()}
function home(){v=fit(HOME);set()}
function first(){v=fit(CORE);set();const W=svg.getBoundingClientRect().width||1;if(v[2]/W>9.5){const w=8*W;v=[2700-w/2,1900-w*asp()/2,w,w*asp()];set()}}
first();let lastW=svg.getBoundingClientRect().width;
addEventListener('resize',()=>{const w=svg.getBoundingClientRect().width;if(Math.abs(w-lastW)<2)return;const cx=v[0]+v[2]/2,cy=v[1]+v[3]/2,k=v[2]/lastW;lastW=w;const nw=k*w;v=[cx-nw/2,cy-nw*asp()/2,nw,nw*asp()];set()});
function pt(x,y){const r=svg.getBoundingClientRect();return[v[0]+(x-r.left)/r.width*v[2],v[1]+(y-r.top)/r.height*v[3]]}
svg.addEventListener('wheel',ev=>{ev.preventDefault();const p=pt(ev.clientX,ev.clientY);zoom(ev.deltaY>0?1.2:1/1.2,p[0],p[1])},{passive:false});
const ptr=new Map();let drag=null,pinch=null,moved=0;
svg.addEventListener('pointerdown',ev=>{svg.setPointerCapture(ev.pointerId);ptr.set(ev.pointerId,[ev.clientX,ev.clientY]);moved=0;
 if(ptr.size===1)drag=[ev.clientX,ev.clientY,v[0],v[1]];else if(ptr.size===2){const [a,b]=[...ptr.values()];pinch=[Math.hypot(a[0]-b[0],a[1]-b[1]),v.slice(),pt((a[0]+b[0])/2,(a[1]+b[1])/2)];drag=null}});
svg.addEventListener('pointermove',ev=>{if(ptr.has(ev.pointerId))ptr.set(ev.pointerId,[ev.clientX,ev.clientY]);
 if(pinch&&ptr.size===2){const [a,b]=[...ptr.values()],d=Math.hypot(a[0]-b[0],a[1]-b[1])||1,f=pinch[0]/d,o=pinch[1],c=pinch[2];const nw=Math.min(HOME[2]*1.8,Math.max(450,o[2]*f)),s=nw/o[2];v=[c[0]-(c[0]-o[0])*s,c[1]-(c[1]-o[1])*s,nw,o[3]*s];set();moved=99;return}
 if(drag){const r=svg.getBoundingClientRect();const dx=ev.clientX-drag[0],dy=ev.clientY-drag[1];moved=Math.max(moved,Math.abs(dx)+Math.abs(dy));v[0]=drag[2]-dx/r.width*v[2];v[1]=drag[3]-dy/r.height*v[3];set();if(moved>4)tip.hidden=true;return}
 if(ev.pointerType==='mouse')hover(ev.clientX,ev.clientY)});
function up(ev){ptr.delete(ev.pointerId);if(ptr.size<2)pinch=null;if(ptr.size===0){if(drag&&moved<5&&ev.pointerType!=='mouse')hover(ev.clientX,ev.clientY);drag=null}}
svg.addEventListener('pointerup',up);svg.addEventListener('pointercancel',up);svg.addEventListener('pointerleave',ev=>{if(ev.pointerType==='mouse')tip.hidden=true});
box.querySelectorAll('.mapctl button').forEach(b=>b.addEventListener('click',()=>{const z=b.dataset.z;if(z==='home'){home();return}zoom(z==='in'?1/1.6:1.6,v[0]+v[2]/2,v[1]+v[3]/2)}));
// the hover: the nearest thing under the pointer, layer by layer (only the layers that are shown)
const D=window.__MAP||{};
function dseg(px,py,a){const dx=a[2]-a[0],dy=a[3]-a[1],L=dx*dx+dy*dy;let t=L?((px-a[0])*dx+(py-a[1])*dy)/L:0;t=Math.max(0,Math.min(1,t));return Math.hypot(px-a[0]-t*dx,py-a[1]-t*dy)}
function near(list,x,y,tol){let best=null;for(const a of list){const d=dseg(x,y,a)-a[4];if(d<=tol&&(!best||d<best[0]))best=[d,a[5]]}return best}
function on(l){return !document.body.classList.contains('off-'+l)}
function hover(cx,cy){const p=pt(cx,cy),k=v[2]/svg.getBoundingClientRect().width,tol=6*k,out=[];
 if(on('roads')){let n=null;for(const a of D.nodes||[]){const d=Math.hypot(p[0]-a[0],p[1]-a[1])-a[2];if(d<=tol&&(!n||d<n[0]))n=[d,a[3]]}if(n)out.push(n[1]);else{const s=near(D.segs||[],p[0],p[1],tol);if(s)out.push(s[1])}}
 if(on('bus')){let st=null;for(const a of D.stops||[]){const d=Math.hypot(p[0]-a[0],p[1]-a[1])-a[2];if(d<=tol&&(!st||d<st[0]))st=[d,a[3]]}if(st)out.unshift(st[1]);else{const b=near(D.bus||[],p[0],p[1],tol);if(b)out.push(b[1])}}
 if(on('rails')){const t=near(D.rails||[],p[0],p[1],tol);if(t)out.push(t[1])}
 if(on('lots')&&!out.length){for(const r of D.lots||[]){if(p[0]>=r[0]&&p[0]<=r[2]&&p[1]>=r[1]&&p[1]<=r[3]){out.push(r[4]);break}}}
 if(!out.length&&D.lake){const q=D.lake.pts;let c=false;for(let i=0,j=q.length-1;i<q.length;j=i++){if((q[i][1]>p[1])!==(q[j][1]>p[1])&&p[0]<(q[j][0]-q[i][0])*(p[1]-q[i][1])/(q[j][1]-q[i][1])+q[i][0])c=!c}if(c)out.push(D.lake.info)}
 if(!out.length){for(const z of D.zones||[]){if(p[0]>=z[0]&&p[0]<z[2]&&p[1]>=z[1]&&p[1]<z[3]){out.push(z[4]);break}}}
 if(!out.length){tip.hidden=true;return}
 tip.innerHTML=out.map(i=>D.info[i]).join('<hr>');tip.hidden=false;const r=box.getBoundingClientRect();let x=cx-r.left+14,y=cy-r.top+14;
 const tw=tip.offsetWidth,th=tip.offsetHeight;if(x+tw>r.width-6)x=Math.max(6,cx-r.left-tw-14);if(y+th>r.height-6)y=Math.max(6,cy-r.top-th-14);tip.style.left=x+'px';tip.style.top=y+'px'}
})();
</script>"""

