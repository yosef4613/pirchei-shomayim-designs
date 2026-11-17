# -*- coding: utf-8 -*-
"""4.11 · סבב 9מ של מפת הדרכים — C2 לפי הציור שאושר (הבעלים 21:03, גרסה 2: Turbo_City_C2_Design_v2.html; המספרים — make_c2v2.py / c2v2_page.js).
 · המגרשים C2-01 … C2-04, ‏C2-F1 ו-C2-F2 → מגרש אחד, C2-01: ‏97 × 62 מ׳ (x 2628–3600, ‏y 828–1448) — מהמדרכה של שדרת המרכז עד הגבול עם D2,
   ומדרך השדות עד שדרת השדה. השימוש: הקניון, הסופר "שיבולת" והחניון המשותף; שתי הווילות יוצאות מ-C2; הבנק ובית המרקחת — חנויות בקניון.
 · בתוך המגרש (הפריטים של סבב 7, לפי הציור): הבניין 81.2 × 17.2 מ׳ (x 2713–3525, ‏y 886–1058), החניון המשותף — 96 חניות (x 2653–3585, ‏y 1094–1438),
   ונתיב השירות של משאית הארגז, בכיוון אחד מזרחה (y 846–886). שורת החנויות הישנה יוצאת.
 · הפתחים — כניסות למגרש (לא צמתים), ברשימת הכניסות של המפה, כך שהמפרצים של התחנות עוקפים אותם:
   DW-C2-01 ‏(x 2843) כניסת שירות ו-DW-C2-02 ‏(x 3480, זז מ-3404) יציאת שירות — מדרך השדות; DW-C2-03 ‏(x 2769) כניסה בלבד, ימינה משדרת השדה;
   DW-C2-04 ‏(x 3469) יציאה בלבד, ימינה, מערבה; DW-C2-06 — חדש, משדרת המרכז ב-y 1240, ימינה פנימה וימינה החוצה;
   DW-C2-05 — חדש, מרחוב הקניון (CL-MALL/1) ב-y 1240 — נבנה עם D2, ובמפה מסומן "עם D2".
    python3 plan7b_r9m.py → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק ל-W/_to_delete/roads_before_r9m)"""
import json, os, sys, textwrap, html, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
E = html.escape
import plan7b_r9l as R9L        # round 9ל (and through it 9כ … 9) — its patches and wrappers run on import; its __main__ does not
import plan7b_r9k as R9K
import plan7b_r9j as R9J
import plan7b_r9i as R9I
import plan7b_r9g as R9G
import plan7b_r8x as R8X
import plan7b_r7 as R7
import plan7b_sites as ST
import plan7b_svg as SV

LOT = [2628.0, 828.0, 3600.0, 1448.0]                      # the design: from AR-C's sidewalk (the hedge at 2628) to D2, from LC-N's hedge (828) to AR-N's sidewalk (1448)
BLDG = [2713, 886, 3525, 1058]                              # BL of c2v2_page.js: כלבו השדרה 2713–2889, קניון טורבו 2889–3237, שיבולת 3237–3525
PARK = [2653, 1094, 3585, 1438]                             # the four rows and the loop of aisles (AIS, ROWS)
SVC = [[2843, 846], [2843, 866], [3480, 866], [3480, 846]]  # LANE [2813,846,3510,886]: in at DW-C2-01, east along the back, out at DW-C2-02
OLD = ('C2-01', 'C2-02', 'C2-03', 'C2-04', 'C2-F1', 'C2-F2')
OLD_ITEMS = ('C2-MALL-P', 'C2-MALL', 'C2-SHOPS')
WHY = 'הבעלים 4.11 21:03 — C2 גרסה 2 (Turbo_City_C2_Design_v2.html): קניון אחד גדול, הסופר "שיבולת" וחניון אחד משותף; '
LOT_LABEL = 'הקניון, הסופר "שיבולת" והחניון המשותף'
LOT_WHY = (WHY + 'מגרש אחד במקום שישה (C2-01 עד C2-04, ‏C2-F1 ו-C2-F2) — 97 × 62 מ׳. שתי הווילות יוצאות מ-C2; הבנק ובית המרקחת — חנויות בקניון, עם חזית ושלט.')
# the openings — (id, road, at, to, lanes, use, label)
DWS = [('DW-C2-01', 'LC-N', (2843, 814), (2843, 840), '1', 'שירות — כניסה', 'כניסת השירות של הקניון והסופר — משאית הארגז, מדרך השדות'),
       ('DW-C2-02', 'LC-N', (3480, 814), (3480, 840), '1', 'שירות — יציאה', 'יציאת השירות — משאית הארגז אחרי הרציף של "שיבולת"'),
       ('DW-C2-03', 'AR-N', (2769, 1448), (2769, 1440), '1', 'כניסה בלבד — ימינה משדרת השדה', 'הכניסה לחניון המשותף — ימינה משדרת השדה'),
       ('DW-C2-04', 'AR-N', (3469, 1448), (3469, 1440), '1', 'יציאה בלבד — ימינה, מערבה', 'היציאה מהחניון המשותף — ימינה, מערבה, לשדרת השדה'),
       ('DW-C2-06', 'AR-C', (2623, 1240), (2645, 1240), '1+1', 'ימינה פנימה וימינה החוצה', 'הכניסה והיציאה של החניון משדרת המרכז — ימינה פנימה וימינה החוצה'),
       ('DW-C2-05', 'CL-MALL', (3651, 1240), (3592, 1240), '1+1', 'כניסה ויציאה — עם D2', 'הכניסה והיציאה של החניון מרחוב הקניון — עם D2')]
WITH_D2 = 'DW-C2-05'
DW_WHY = {'DW-C2-02': WHY + 'זז מ-x 3404 ל-3480, כדי שהמשאית שיוצאת מהרציף של הסופר תספיק לפנות; 23 מ׳ מ-J37_08.',
          'DW-C2-05': WHY + 'נבנה עם D2, כשרחוב הקניון החדש (CL-MALL/1) נבנה; במפה הוא כבר קיים, מסומן "עם D2".',
          'DW-C2-06': WHY + 'חדש: מהנתיב החיצוני צפונה של שדרת המרכז; החציון רציף — ימינה בלבד.'}
ST.DW[:] = [d for d in ST.DW if d['id'] not in {x[0] for x in DWS}] + [
    dict(zone='C2', id=i, road=r, at=at, to=to, lanes=ln, label=lab + (' — עם D2' if i == WITH_D2 and 'עם D2' not in lab else ''), use9m=u,
         why=DW_WHY.get(i, WHY + 'פתח אמיתי: ריצוף על כל רוחב המדרכה, שפה מונמכת וכנף בכל צד.'), **({'with': 'D2'} if i == WITH_D2 else {}))
    for i, r, at, to, ln, u, lab in DWS]
DONE9M = {}

# ---------------------------------------------------------------- 1 · the lots and the items of C2 (after the generator, the fill and round 7)
_post9l = R7.post
def post(ctx):
    g = sys._getframe(1).f_globals
    g['__r9m_post'] = _post9l
    items = eval('__r9m_post(__r9m_ctx)', g, {'__r9m_ctx': ctx})
    LOTS = ctx['LOTS']; mine = {x[0] for x in DWS}
    DONE9M['before_lots'] = [dict(id=l['id'], rect=l['rect'], label=l['label']) for l in LOTS if l['id'] in OLD]
    DONE9M['before_items'] = [dict(id=i['id'], kind=i['kind'], rect=i.get('rect'), label=i['label']) for i in items if i['id'] in OLD_ITEMS]
    gen = [d for d in g['LOT_DW'] if d['zone'] == 'C2']                           # the generator's lowered curbs of the old lots
    DONE9M['before_dws'] = [dict(id=d['id'], road=d['road'], at=d['at']) for d in gen]
    g['LOT_DW'][:] = [d for d in g['LOT_DW'] if d['zone'] != 'C2']
    g['SITE_ROADS'][:] = [r for r in g['SITE_ROADS'] if not (r['kind'] == 'driveway' and r.get('hw') == 30 and any(r['id'] == d['id'] for d in gen))]
    assert sum(1 for r in g['SITE_ROADS'] if r['id'] in mine) == len(mine)          # the six openings stay (from the site driveways, hw 19.5 / 39)
    k = next(n for n, l in enumerate(LOTS) if l['id'] == 'C2-01')
    LOTS[:] = [l for l in LOTS if l['id'] not in OLD[:4]]
    LOTS.insert(k, dict(id='C2-01', zone='C2', kind='lot', use='shop', label=LOT_LABEL, rect=list(LOT), future=True, front='AR-N', dw='DW-C2-03', r9m=True, why=LOT_WHY))
    R8X._refill(g, {'C2'})                                                          # C2-F1 and C2-F2 out; the free scan again (nothing is left)
    items[:] = [i for i in items if i['id'] not in OLD_ITEMS]
    items += [dict(zone='C2', id='C2-MALL', kind='building', label='הקניון — "כלבו השדרה", "קניון טורבו" והסופר "שיבולת" — 81.2 × 17.2 מ׳',
                   why=WHY + 'בניין אחד, צמוד לגדר החיה של דרך השדות; החזית לדרום, אל החניון. הבנק, בית המרקחת, חנות הדיג, בית הקפה והמסעדה — חנויות בקניון.',
                   stage=None, rect=list(BLDG), floors=2, parent='C2-01', access=('lot', 'C2-01'), lbl=True,
                   units=['כלבו השדרה', 'קניון טורבו', 'שיבולת', 'בנק המפרץ', 'הגפן', 'קפה טורבו', 'שולחן העיר', 'קרס וחכה']),
              dict(zone='C2', id='C2-MALL-P', kind='parking', label='החניון המשותף — 96 חניות (6 נכים, 6 טעינה)',
                   why=WHY + 'ארבע שורות (26 + 25 + 25 + 20) ולולאה אחת בכיוון אחד; נכנסים ב-DW-C2-03 ו-DW-C2-06, יוצאים ב-DW-C2-04 ו-DW-C2-06 (ועם D2 — ב-DW-C2-05).',
                   stage=None, rect=list(PARK), stalls=96, parent='C2-01', access=('lot', 'C2-01'), lbl=True),
              dict(zone='C2', id='C2-SVC', kind='svc', label='נתיב השירות — משאית הארגז, בכיוון אחד מזרחה, אל הרציפים',
                   why=WHY + 'נכנסים ב-DW-C2-01, נוסעים מזרחה מאחורי הבניין, הרציף מימין, ויוצאים ב-DW-C2-02 — בלי רוורס ובלי לעבור בחניון של הקונים.',
                   stage=None, pts=[list(q) for q in SVC], hw=20, cls='service', parent='C2-01', access=('lot', 'C2-01'))]
    DONE9M['after'] = dict(lot=list(LOT), bldg=list(BLDG), park=list(PARK), svc=SVC, fill_left=[l['id'] for l in LOTS if l['zone'] == 'C2' and l.get('fill')])
    return items
R7.post = post

_chk9l = R7.checks
def checks(ctx, I):
    g = sys._getframe(1).f_globals
    g['__r9m_chk'] = _chk9l
    out = list(eval('__r9m_chk(__r9m_ctx, __r9m_I)', g, {'__r9m_ctx': ctx, '__r9m_I': I}))
    DONE9M['dws'] = [dict(id=d['id'], road=d['road'], at=d['at'], to_junction_m=d.get('to_junction_m'), lanes=d['lanes'], use=d.get('use9m'), label=d['label'])
                     for d in g['DWS'] if d['id'] in {x[0] for x in DWS}]
    st = next((s for s in g['STOPS'] if s.get('name') == 'הקניון'), None)
    DONE9M['st11'] = [dict(dir=b['dir'], y=[min(q[1] for q in b['poly']), max(q[1] for q in b['poly'])], near_m=b['near_m'], far_m=b['far_m'], relaxed=b.get('relaxed'))
                      for b in (st or {}).get('bay_list', [])]
    return out
R7.checks = checks

TITLE = 'תוכנית הדרכים של כל העיר — סבב 9מ'
_lay9l = SV.label_layout
def label_layout(P_):
    o = _lay9l(P_); P_['title'] = TITLE; P_['batch'] = '9מ'; return o
SV.label_layout = label_layout

_lots9l = SV.lots_layer
def lots_layer(P_):
    """the opening that is built with D2: a dashed outline over its mouth"""
    o = _lots9l(P_); d = next((d for d in P_.get('driveways', []) if d['id'] == WITH_D2), None)
    if not d: return o
    x, y = d['at']; add = f"<rect x='{x - 62}' y='{y - 48}' width='72' height='96' fill='none' stroke='#e07b00' stroke-width='6' stroke-dasharray='16 10'/>"
    k = o.rfind('</g>'); return o[:k] + add + o[k:]
SV.lots_layer = lots_layer

# ---------------------------------------------------------------- 2 · the page: the section of 9מ before 9ל (9ל, 9כ, 9י, 9ט, 9ח stay as they were)
def keep():
    P_ = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8'))
    T = open(os.path.join(HERE, 'city_plan.html'), encoding='utf-8').read()
    def sec(a, b): i = T.index(a); j = T.index(b); assert i < j; return T[i:j]
    if P_.get('r9m'): before = P_['r9m']['before']
    else:
        before = dict(lots=[dict(id=l['id'], rect=l['rect'], label=l['label']) for l in P_['lots'] if l['id'] in OLD],
                      items=[dict(id=i['id'], kind=i['kind'], rect=i.get('rect'), label=i['label']) for i in P_['r7']['items'] if i['id'] in OLD_ITEMS],
                      dws=[dict(id=d['id'], road=d['road'], at=d['at'], to_junction_m=d.get('to_junction_m')) for d in P_['driveways'] if d['zone'] == 'C2'])
    return dict(r9j=P_['r9j'], r9k=P_['r9k'], r9l=P_['r9l'], before=before,
                s9l=sec('<h2>סבב 9ל', '<h2>סבב 9כ'), s9k=sec('<h2>סבב 9כ', '<h2>סבב 9י'), s9j=sec('<h2>סבב 9י', '<h2>סבב 9ט'))

USECOL = {'שירות — כניסה': '#ef6c00', 'שירות — יציאה': '#ef6c00', 'כניסה בלבד — ימינה משדרת השדה': '#1565c0', 'יציאה בלבד — ימינה, מערבה': '#c62828',
          'ימינה פנימה וימינה החוצה': '#6a1b9a', 'כניסה ויציאה — עם D2': '#6a1b9a'}
def c2_svg(after, rec):
    x0, y0, x1, y1 = 2300, 640, 3880, 1780; rd = '#8d949b'; wk = '#e2ded3'
    o = [f"<svg viewBox='{x0} {y0} {x1 - x0} {y1 - y0}' role='img' aria-label='C2 {'אחרי' if after else 'לפני'}' style='width:100%;height:auto;background:#f4f2ec;border-radius:8px'>"]
    for (a, b, c, d) in ((x0, 706, x1, 814), (2397, y0, 2623, y1), (x0, 1448, x1, 1752), (3651, y0, 3769, y1)):   # LC-N, AR-C, AR-N, CL-MALL — with their sidewalks
        o.append(f"<rect x='{a}' y='{b}' width='{c - a}' height='{d - b}' fill='{wk}'/>")
    for (a, b, c, d) in ((x0, 721, x1, 799), (2422, y0, 2598, y1), (x0, 1473, x1, 1727), (3671, y0, 3749, y1)):
        o.append(f"<rect x='{a}' y='{b}' width='{c - a}' height='{d - b}' fill='{rd}'/>")
    o.append(f"<line x1='3600' y1='{y0}' x2='3600' y2='{y1}' stroke='#1d5fa8' stroke-width='4' stroke-dasharray='18 12'/>")
    o.append("<text x='3200' y='770' font-size='26' text-anchor='middle' fill='#fff'>דרך השדות</text><text x='3200' y='1610' font-size='30' text-anchor='middle' fill='#fff'>שדרת השדה</text>"
             "<text x='2510' y='1700' font-size='24' text-anchor='middle' fill='#fff'>שדרת המרכז</text><text x='3710' y='1700' font-size='22' text-anchor='middle' fill='#fff'>רחוב הקניון</text>"
             "<text x='3635' y='900' font-size='26' text-anchor='middle' fill='#1d5fa8'>D2</text><text x='3540' y='900' font-size='26' text-anchor='middle' fill='#1d5fa8'>C2</text>")
    R = lambda r, f, ex='': f"<rect x='{r[0]}' y='{r[1]}' width='{r[2] - r[0]}' height='{r[3] - r[1]}' fill='{f}' {ex}/>"
    if after:
        o.append(R(LOT, '#f2c7b8', "stroke='#6d6a63' stroke-width='6'"))
        o.append(R(PARK, '#d6dade', "stroke='#556' stroke-width='4'"))
        for yy in (1150, 1210, 1322, 1382):
            o.append(f"<line x1='2653' y1='{yy}' x2='3585' y2='{yy}' stroke='#fff' stroke-width='3'/>")
        o.append(R(BLDG, '#8e9aa8', "stroke='#556' stroke-width='5'"))
        o.append(f"<polyline points='{' '.join(f'{x},{y}' for x, y in SVC)}' fill='none' stroke='#ef6c00' stroke-width='8' stroke-dasharray='20 12'/>")
        o.append("<text x='3119' y='985' font-size='30' text-anchor='middle' fill='#fff'>הקניון ו&quot;שיבולת&quot;</text>"
                 "<text x='3119' y='1280' font-size='28' text-anchor='middle' fill='#333'>החניון המשותף · 96</text>")
        for d in rec.get('dws', []):
            x, y = d['at']; col = USECOL.get(d.get('use'), '#333'); dash = " stroke-dasharray='10 7'" if d['id'] == WITH_D2 else ''
            v = d['road'] in ('AR-C', 'CL-MALL'); w, h = (60, 60) if v else (60, 60)
            o.append(f"<rect x='{x - w / 2}' y='{y - h / 2}' width='{w}' height='{h}' fill='none' stroke='{col}' stroke-width='9'{dash}/>")
            tx, ty = {'LC-N': (x, y - 52), 'AR-N': (x, y + 72), 'AR-C': (x - 70, y + 9), 'CL-MALL': (x + 75, y - 40)}[d['road']]
            o.append(f"<text x='{tx}' y='{ty}' font-size='30' font-weight='700' text-anchor='middle' fill='{col}'>{E(d['id'][-2:])}</text>")
    else:
        for l in rec['before']['lots']:
            o.append(R(l['rect'], '#f3dfb8' if 'ווילות' in l['label'] else '#f2c7b8', "stroke='#6d6a63' stroke-width='5'"))
        for i in rec['before']['items']:
            if i.get('rect'): o.append(R(i['rect'], '#d6dade' if i['kind'] == 'parking' else '#8e9aa8', "stroke='#556' stroke-width='4'"))
        for l in rec['before']['lots']:
            r = l['rect']; o.append(f"<text x='{(r[0] + r[2]) / 2}' y='{(r[1] + r[3]) / 2 + 10}' font-size='26' text-anchor='middle' fill='#333'>{E(l['id'])}</text>")
        for d in rec['before']['dws']:
            x, y = d['at']; o.append(f"<rect x='{x - 30}' y='{y - 30}' width='60' height='60' fill='none' stroke='#333' stroke-width='8'/>")
            o.append(f"<text x='{x}' y='{y - 52 if y < 1000 else y + 72}' font-size='30' font-weight='700' text-anchor='middle' fill='#333'>{E(d['id'][-2:])}</text>")
    o.append("<g transform='translate(3820,1060)'><path d='M0,-46 L18,0 L0,-12 L-18,0 Z' fill='#222'/><text x='0' y='32' font-size='26' text-anchor='middle'>צפון</text></g>")
    o.append("<text x='2349' y='1250' font-size='28' text-anchor='middle' fill='#222'>מערב</text><text x='3825' y='1300' font-size='28' text-anchor='middle' fill='#222'>מזרח</text>")
    o.append('</svg>')
    return ''.join(o)

def _junc_of(P_, d):
    N = {n['id']: n for n in P_['nodes']}; x, y = d['at']; best = None
    for n in N.values():
        if n['kind'] not in ('signal', 'roundabout', 'riro', 'stop'): continue
        if abs(math.hypot(n['x'] - x, n['y'] - y) / 10 - (d.get('to_junction_m') or -1)) < .06: best = n['id']
    return best or '—'

def page_r9m(K):
    pj = os.path.join(HERE, 'city_plan.json'); P_ = json.load(open(pj, encoding='utf-8'))
    P_['title'] = TITLE; P_['batch'] = '9מ'
    T = P_['bus']['terminal']; T['gates'] = R9K.gates_rec(); T['flow'] = R9K.FLOW
    P_['logi_points'] = [dict(zone=z, what=w, rect=r, state=s) for z, w, r, s in R9J.POINTS]
    P_['r9j'] = K['r9j']; P_['r9k'] = K['r9k']; P_['r9l'] = K['r9l']
    SB = {frozenset((x['a'], x['b'])): x for x in P_['segments']}
    for ln in P_['routes']['bus']:
        if ln.get('back'): ln['len_back_km'] = round(sum(SB[frozenset((a, b))]['len_m'] for a, b in zip(ln['back'], ln['back'][1:])) / 1000, 2)
    nck = len(P_['checks']); nok = sum(1 for c in P_['checks'] if c['ok'])
    dws = DONE9M.get('dws') or []
    for d in dws: d['junction'] = _junc_of(P_, d)
    order = {x[0]: n for n, x in enumerate(DWS)}; dws.sort(key=lambda d: order[d['id']])
    P_['r9m'] = dict(at='4.11.2026', by='הבעלים 21:03 (C2 גרסה 2)', why='סבב 9מ: C2 לפי הציור שאושר — מגרש אחד, הקניון, הסופר "שיבולת", החניון המשותף, והפתחים',
                     lot=dict(id='C2-01', rect=list(LOT), m=[round((LOT[2] - LOT[0]) / 10, 1), round((LOT[3] - LOT[1]) / 10, 1)], label=LOT_LABEL),
                     out_lots=list(OLD[1:]), items=dict(bldg=list(BLDG), park=list(PARK), svc=SVC, out=['C2-SHOPS']), dws=dws, st11=DONE9M.get('st11'),
                     before=K['before'], checks=f'{nok}/{nck}')
    json.dump(P_, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ph = os.path.join(HERE, 'city_plan.html'); H0 = open(ph, encoding='utf-8').read()
    rec = dict(before=K['before'], dws=dws)
    rows = ''.join(f"<tr><td class='id'>{E(d['id'])}</td><td>{E({'LC-N': 'דרך השדות', 'AR-N': 'שדרת השדה', 'AR-C': 'שדרת המרכז', 'CL-MALL': 'רחוב הקניון'}[d['road']])} "
                   f"<span class='small mut'>({E(d['road'])})</span></td><td class='small'>x {d['at'][0]:.0f}, ‏y {d['at'][1]:.0f}</td><td>{E(d['use'])}</td>"
                   f"<td>{d['to_junction_m']} מ׳ <span class='small mut'>({E(d['junction'])})</span></td></tr>" for d in dws)
    mn = min((d['to_junction_m'] for d in dws), default=0)
    st11 = DONE9M.get('st11') or []
    fig = lambda after, cap: f"<figure style='margin:0;flex:1 1 300px;max-width:520px'>{c2_svg(after, rec)}<figcaption class='small'>{cap}</figcaption></figure>"
    S9 = ("<h2>סבב 9מ — מה השתנה (4.11.2026)</h2>"
          "<p class='small'>הבעלים אישר את C2 גרסה 2 (21:03). המגרשים C2-01 עד C2-04, ‏C2-F1 ו-C2-F2 התאחדו למגרש אחד, <b>C2-01</b>: ‏97 × 62 מ׳, מהמדרכה של שדרת המרכז "
          "עד הגבול עם D2, ומדרך השדות עד שדרת השדה. השימוש: הקניון, הסופר &quot;שיבולת&quot; והחניון המשותף. שתי הווילות יצאו מ-C2, והבנק ובית המרקחת הם חנויות בקניון. "
          "בתוך המגרש, לפי הציור: הבניין (81.2 × 17.2 מ׳, צמוד לדרך השדות), החניון המשותף (96 חניות, לולאה אחת בכיוון אחד) ונתיב השירות של משאית הארגז מאחורי הבניין. "
          "שורת החנויות הישנה יצאה.</p>"
          "<div style='display:flex;flex-wrap:wrap;gap:12px;margin:6px 0 10px'>" + fig(False, 'לפני — סבב 9ל: שישה מגרשים, ארבעה פתחים') +
          fig(True, 'אחרי — סבב 9מ: מגרש אחד ושישה פתחים (המספר — סוף המזהה DW-C2-…); כתום — שירות, כחול — כניסה, אדום — יציאה, סגול — כניסה ויציאה; מקווקו — עם D2') + "</div>"
          "<h3>הפתחים — כניסות למגרש, לא צמתים (הכלל: לפחות 18 מ׳ מצומת)</h3><div class='wrap'><table><tr><th>הפתח</th><th>מאיזה רחוב</th><th>איפה</th><th>מה</th><th>המרחק מהצומת הקרוב</th></tr>"
          + rows + "</table></div>"
          f"<p class='small'>כל הפתחים לפי הכלל: הקרוב ביותר {mn} מ׳ מצומת. DW-C2-05 נבנה עם D2 — במפה הוא כבר קיים, מסומן &quot;עם D2&quot; (מסגרת כתומה מקווקוות). "
          "הפתחים נמצאים ברשימת הכניסות של המפה, ולכן המפרצים של התחנות עוקפים אותם"
          + (": בתחנה &quot;הקניון&quot; (ST-11) ברחוב הקניון — " + '; '.join(f"{'דרומה' if b['dir'].startswith('J37_08') else 'צפונה'} y {b['y'][0]:.0f}–{b['y'][1]:.0f}" + (' (חריגה)' if b.get('relaxed') else '') for b in st11) if st11 else '')
          + f". הבדיקות: {nok} מתוך {nck} עוברות.</p>")
    k = H0.index('<h2>סבב 9ט'); H0 = H0[:k] + S9 + K['s9l'] + K['s9k'] + K['s9j'] + H0[k:]
    for old in ('תוכנית הדרכים של כל העיר — סבב 9ט', 'תוכנית הדרכים של כל העיר — סבב 9י', 'תוכנית הדרכים של כל העיר — סבב 9כ', 'תוכנית הדרכים של כל העיר — סבב 9ל'):
        H0 = H0.replace(old, TITLE)
    open(ph, 'w', encoding='utf-8').write(H0)
    print('r9m', dict(dws=[(d['id'], d['at'], d['to_junction_m'], d['junction']) for d in dws], st11=st11, fill_left=DONE9M.get('after', {}).get('fill_left'), checks=f'{nok}/{nck}'))
    assert len(dws) == 6 and all(d['to_junction_m'] >= 18 for d in dws)
    assert all(H0.count('<h2>סבב ' + r) == 1 for r in ('9מ', '9ל', '9כ', '9י', '9ט', '9ח'))
    assert H0.index('<h2>סבב 9מ') < H0.index('<h2>סבב 9ל') < H0.index('<h2>סבב 9כ') < H0.index('<h2>סבב 9י') < H0.index('<h2>סבב 9ט')

if __name__ == '__main__':
    os.chdir(HERE)
    rec9h, prev9i, sec9h = R9I.keep_9h()
    K = keep()
    src = open(os.path.join(HERE, 'plan7b_r9g.py'), encoding='utf-8').read(); body = src[src.index("if __name__ == '__main__':"):].split('\n')[1:]
    exec(compile(textwrap.dedent('\n'.join(body)), 'plan7b_r9g.py:__main__', 'exec'), dict(vars(R9G)))
    R9I.page_r9i(rec9h, sec9h)
    page_r9m(K)
