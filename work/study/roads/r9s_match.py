# -*- coding: utf-8 -*-
"""8.11 · סבב 9ס — טבלת ההתאמה מפה↔משחק (R-86, ‏R-83 סעיף ט, ‏R-87 סעיף ה).
לכל מגרש, קטע דרך, צומת (כולל סוג השליטה), מעבר חצייה ומפרץ תחנה באזורים שנבנו — בשני הכיוונים, עם מרחק במטרים.
מרחק של יותר מ-4.5 מ׳ — לא תואם, עם הסבר ועם "מי מתקן".
    from r9s_match import match; T = match(P, G)        P — city_plan.json (אחרי סבב 9ס), ‏G — game_s7f265.json (probe_s7f265.js)"""
import math, re

COLS = [0, 1200, 2400, 3600, 4800, 6000, 7200, 8400, 9600]; ROWS = [-850, 0, 850, 1700, 2550, 3400, 4250, 5200, 6050, 6900, 7750]
TOL = 45                     # 4.5 מ׳ (10 פיקסלים למטר)
BUILT_STAGES = [f'S{i}' for i in range(1, 9)]
S9A_SEGS = ['LC-E3/1', 'LC-E3/2', 'LC-E3W/1', 'CL-I/1', 'CL-I/2', 'CL-I/3', 'CL-I/4', 'CL-I/5', 'CL-I/6', 'CL-I/7', 'CL-F/1']
CLS_GAME = {'main': 'main', 'arterial': 'arterial', 'collector': 'avenue', 'local': 'local', 'local45': 'local', 'oneway5': 'oneway5',
            'art21': 'art21', 'lane2': 'lane2', 'temp': 'local', 'oneway': 'oneway', 'track': None}
KHE = {'signal': 'רמזור', 'roundabout': 'כיכר', 'stop': 'עצור', 'riro': 'ימינה בלבד', 'gate': 'שער', 'corner': 'פינה', 'end': 'קצה', 'plaza': 'רחבה',
       'bridgehead': 'ראש גשר', 'none': 'בלי רמזור', 'cul': 'מעגל סיבוב'}
CHE = {'main': 'עורק ראשי', 'arterial': 'עורק', 'collector': 'מאסף', 'local': 'מקומי', 'avenue': 'שדרה', 'lane2': 'דרך גישה', 'oneway5': 'חד-סטרי למשאיות',
       'art21': 'עורק 2+1', 'local45': 'רחוב למשאיות', 'oneway': 'חד-סטרי', 'service': 'דרך שירות', 'track': 'דרך עפר', 'temp': 'זמני'}
LHE = {'golf': 'המיני גולף', 'play': 'מגרש המשחקים', 'picnic': 'פינת הפיקניק', 'boatPier': 'מזח הסירה', 'booth': 'הקופה של המיני גולף', 'box': 'האגם והפארק',
       'b1p': 'החניון של B1', 'b201': 'החניון של B2-01', 'hosp': 'בית החולים', 'clinic': 'המרפאה', 'lot': 'החניון', 'garden': 'הגינה', 'avenue': 'השדרה',
       'drive': 'הכניסה', 'court': 'החצר', 'yard': 'החצר', 'pol': 'תחנת המשטרה', 'hotel': 'המלון', 'office': 'מגדל המשרדים', 'sq': 'הכיכר', 'gate': 'השער'}
FIX_MAP, FIX_GAME, FIX_ASK, FIX_S9, FIX_NONE = 'המפה כבר תוקנה', 'המשחק — לסוף S9a', 'לאישורך', 'ייצא / ייבנה עם S9', '—'


def zone_of(x, y):
    i = max(0, min(7, next((k for k in range(8) if COLS[k] <= x < COLS[k + 1]), 7 if x >= 9600 else 0)))
    j = max(0, min(9, next((k for k in range(10) if ROWS[k] <= y < ROWS[k + 1]), 9 if y >= 7750 else 0)))
    return 'ABCDEFGH'[i] + str(j)


def dseg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def dpoly(px, py, pts):
    return min(dseg(px, py, *pts[i], *pts[i + 1]) for i in range(len(pts) - 1)) if len(pts) > 1 else math.hypot(px - pts[0][0], py - pts[0][1])


def samples(pts, step=20, skip=30):
    """points along a polyline, every `step` px, without the first and last `skip` px (the junction itself)"""
    out = []; L = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)); s = 0
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]; l = math.hypot(bx - ax, by - ay)
        if l == 0: continue
        t = 0
        while t <= l:
            if skip <= s + t <= L - skip: out.append((ax + (bx - ax) * t / l, ay + (by - ay) * t / l))
            t += step
        s += l
    if not out:   # a short piece: its middle
        k = len(pts) // 2; out = [((pts[k - 1][0] + pts[k][0]) / 2, (pts[k - 1][1] + pts[k][1]) / 2)] if len(pts) > 1 else [tuple(pts[0])]
    return out, L


def rgap(a, b):
    return math.hypot(max(0, max(a[0], b[0]) - min(a[2], b[2])), max(0, max(a[1], b[1]) - min(a[3], b[3])))


def rov(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


def m1(v): return round(v / 10, 1)


def rect_of(v):
    if isinstance(v, list) and len(v) == 4 and all(isinstance(t, (int, float)) for t in v): return v if (v[2] > v[0] and v[3] > v[1]) else None
    if isinstance(v, dict) and all(isinstance(v.get(k), (int, float)) for k in 'xywh'): return [v['x'], v['y'], v['x'] + v['w'], v['y'] + v['h']]
    return None


def asphalt(G):
    """the paved rectangles of the zone drawings of the game (car parks, yards, lanes, curb cuts) — where a road inside a lot can lie"""
    out = []
    def add(v):
        r = rect_of(v)
        if r: out.append(r)
    A2 = G.get('A2G') or {}
    for k in ('lot', 'drive', 'court', 'yard'): add(A2.get(k))
    for k in ('lane', 'inLeg', 'outLeg'): add((A2.get('er') or {}).get(k))
    for v in A2.get('svc') or []: add(v)
    add((A2.get('svcDrive') or {}).get('lane'))
    A5 = G.get('A5G') or {}
    for k in ('yard', 'lot', 'sq'): add(A5.get(k))
    for c in (A5.get('cuts') or []) + (A2.get('cuts') or []):
        if isinstance(c, list) and len(c) >= 5: add([c[1], c[2], c[1] + c[3], c[2] + c[4]])
    for k in ('A4_LOTS', 'D2_PARKING', 'E3_LOTS', 'C2_LOTS', 'D2_ACCESS', 'A6_LOTS'):
        for v in G.get(k) or []: add(v)
    for k in ('B4_LOTS', 'B3N_LOTS'):
        for v in G.get(k) or []:
            if isinstance(v, dict):
                add(v.get('yard'))
                for a in v.get('acc') or []: add(a)
    PAVED = re.compile(r'(pave|apron|cut|svc|park|aisle|stall|lane|asph|exit|bay|turn|drive|yard|lot|garage|court)', re.I)
    for k in ('D3ND', 'C4ND', 'D4ND', 'C5ND', 'D5ND', 'B5ND', 'A5ND', 'A2ND', 'B4G', 'A34D', 'C3D', 'B3LOOKD', 'B3NG'):
        D = G.get(k) or {}
        for q, vv in D.items():
            if not PAVED.search(q) or not isinstance(vv, list): continue
            for v in vv:
                if isinstance(v, list) and len(v) >= 4 and all(isinstance(t, (int, float)) for t in v[:4]):
                    r = v[:4]
                    if r[2] > r[0] and r[3] > r[1]: out.append(r)
                    elif r[2] > 0 and r[3] > 0 and r[2] < 2000: out.append([r[0], r[1], r[0] + r[2], r[1] + r[3]])   # x, y, w, h
                else: add(v)
    B = G.get('B12') or {}
    for q in ('b1p', 'b201', 'b202'):
        v = B.get(q) or {}
        for k in ('rect', 'aisle', 'cut', 'lane', 'bay', 'front'): add(v.get(k))
    return out


def mn(it):
    return min(it, key=lambda t: t[0])


def match(P, G, extra_notes=None, zones_extra=(), segs_extra=()):
    """9ע: zones_extra — אזורים שנבנו אחרי S8 (S9); segs_extra — קטעים שנבנו מחוץ לאזורים האלה"""
    X = extra_notes or {}
    stage_zones = {t['stage']: t['zones'] for t in P['transition']['stages']}
    BZ = [z for s in BUILT_STAGES for z in stage_zones.get(s, [])] + ['E3'] + [z for z in zones_extra if z != 'E3']
    NB = {n['id']: n for n in G['nodes']}; MN = {n['id']: n for n in P['nodes']}
    GE = [e for e in G['edges'] if not e['future']]
    gline = {e['id']: [[NB[e['a']]['x'], NB[e['a']]['y']], [NB[e['b']]['x'], NB[e['b']]['y']]] for e in GE}
    rows = []
    def row(kind, dirn, mid, gid, zone, dist, ok, note, fix, **kw):
        rows.append(dict(kind=kind, dir=dirn, map=mid, game=gid, zone=zone, dist_m=(None if dist is None else m1(dist)), ok=bool(ok), note=note,
                         fix=(FIX_NONE if ok and fix is None else fix), **kw))
    # ------------------------------------------------------------------ 1 · road segments (the network and the roads inside the lots)
    GA = asphalt(G)
    built_seg = [s for s in P['segments'] if s.get('stage') in BUILT_STAGES or s['id'] in S9A_SEGS or s['id'] in segs_extra]
    built_seg_ids = {s['id'] for s in built_seg}
    map_lines = [(s['id'], s['pts'], s['cls'], 'net') for s in built_seg]
    map_lines += [(r['id'], r['pts'], r.get('cls'), 'site') for r in P['site_roads'] if r.get('zone') in BZ and not r.get('replaced')]
    for sid, pts, cls, src in map_lines:
        sm, L = samples(pts)
        best = []
        for (x, y) in sm:
            d, e = mn((dpoly(x, y, gline[q]), q) for q in gline)
            best.append((d, e))
        dmax = max(d for d, _ in best); used = sorted({e for d, e in best if d <= TOL})
        z = zone_of(*pts[len(pts) // 2]) if len(pts) > 2 else zone_of((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
        if src == 'site' and cls == 'driveway':
            # a driveway: its mouth on the road (the curb cut); the rest is inside the lot
            mx, my = pts[0]; d0, e0 = mn((dpoly(mx, my, gline[q]) - next(e['half'] for e in GE if e['id'] == q), q) for q in gline)
            okd = d0 <= TOL
            row('driveway', 'map→game', sid, e0 if okd else None, z, max(0, d0), okd,
                X.get(('driveway', sid)) or (f'הפתח על {e0} (כניסה למגרש, לא קטע ברשת)' if okd else f'אין כביש במשחק מול הפתח ({m1(d0)} מ׳)'),
                None if okd else X.get(('driveway-fix', sid), FIX_ASK), len_m=m1(L))
            continue
        if src == 'site':
            dmax = max(min(min((dpoly(x, y, gline[q]) for q in gline)), min((rgap((x, y, x, y), r) for r in GA), default=1e9)) for x, y in sm)
            used = sorted({e for d, e in best if d <= TOL})
        ok = dmax <= TOL
        g_cls = sorted({next(e['cls'] for e in GE if e['id'] == q) for q in used})
        want = CLS_GAME.get(cls)
        cls_ok = (not used) or want is None or want in g_cls or src == 'site'
        note = X.get(('segment', sid))
        if not note:
            if ok and cls_ok: note = 'תואם: ' + ', '.join(used)
            elif ok: note = f'תואם במקום; הסוג במפה {CHE.get(cls, cls)}, במשחק {"/".join(CHE.get(q, q) for q in g_cls)}'
            else: note = f'הרחק המרבי מהמשחק {m1(dmax)} מ׳' + (f' (הקרוב: {best[0][1]})' if best else '')
        fix = None if (ok and cls_ok) else X.get(('segment-fix', sid), FIX_ASK)
        row('segment', 'map→game', sid, ', '.join(used) or None, z, dmax, ok and cls_ok, note, fix, len_m=m1(L), cls_map=cls, cls_game='/'.join(g_cls), src=src)
    TEMPS = [[t['x'], t['y']] for st in P['transition']['stages'] for t in st.get('temp_added', []) if isinstance(t.get('x'), list) and isinstance(t.get('y'), list)]
    all_map_lines = TEMPS + [pts for _, pts, _, _ in map_lines] + [s['pts'] for s in P['segments']] + [r['pts'] for r in P['site_roads']]
    for e in GE:
        a, b = gline[e['id']]; mz = zone_of((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        inb = mz in BZ or e.get('plan') in built_seg_ids
        sm, L = samples([a, b])
        dmax = max(min(dpoly(x, y, p) for p in all_map_lines) for x, y in sm)
        ok = dmax <= TOL
        key = ('game-segment', e['id'])
        if not inb:
            note = X.get(key) or ('אזור שעוד לא נבנה מחדש — ' + ('קיים גם במפה' if ok else 'לא במפה; ייצא כשהאזור נבנה'))
            row('segment', 'game→map', None, e['id'], mz, dmax, True, note, FIX_NONE if ok else X.get(('game-segment-fix', e['id']), FIX_S9), built=False, len_m=m1(L), name=e['name'])
            continue
        note = X.get(key) or ('תואם' if ok else f'במשחק ולא במפה — {m1(dmax)} מ׳ מהדרך הקרובה במפה')
        row('segment', 'game→map', None, e['id'], mz, dmax, ok, note, None if ok else X.get(('game-segment-fix', e['id']), FIX_ASK), built=True, len_m=m1(L), name=e['name'])
    # ------------------------------------------------------------------ 2 · junctions, with the kind of control
    gsig = set(G['signals']); grb = set((G.get('RB2') or {}).keys()); ginter = set(G['inter'])
    def gctl(gid):
        if gid in grb: return 'roundabout'
        if gid in gsig: return 'signal'
        n = NB[gid]
        if n.get('cul'): return 'cul'
        return 'none'
    mnodes = set()
    for s in built_seg: mnodes.update([s['a'], s['b']])
    KIND_OK = {'signal': {'signal'}, 'roundabout': {'roundabout'}, 'stop': {'none'}, 'riro': {'none'}, 'gate': {'none', 'cul'}, 'corner': {'none', 'cul'},
               'end': {'none', 'cul'}, 'plaza': {'none', 'cul'}, 'bridgehead': {'none', 'cul'}}
    for nid in sorted(mnodes):
        n = MN[nid]
        d, gid = mn((math.hypot(g['x'] - n['x'], g['y'] - n['y']), g['id']) for g in G['nodes'])
        k = n['kind']; z = n.get('zone') or zone_of(n['x'], n['y'])
        note = X.get(('junction', nid))
        if d > 60:
            row('junction', 'map→game', nid, None, z, d, False, note or f'אין צומת במשחק ב-6 מ׳ (הקרוב {gid}, ‏{m1(d)} מ׳)', X.get(('junction-fix', nid), FIX_ASK), kind_map=k); continue
        c = gctl(gid); cok = c in KIND_OK.get(k, {c})
        ok = d <= TOL and cok
        if not note:
            note = f'במפה {KHE.get(k, k)}, במשחק {KHE.get(c, c)}' + ('' if cok else ' — סוג השליטה שונה')
        row('junction', 'map→game', nid, gid, z, d, ok, note, None if ok else X.get(('junction-fix', nid), FIX_ASK), kind_map=k, kind_game=c)
    deg = {}
    for e in GE: deg[e['a']] = deg.get(e['a'], 0) + 1; deg[e['b']] = deg.get(e['b'], 0) + 1
    for gid in sorted(ginter):
        if deg.get(gid, 0) < 3 and gid not in gsig and gid not in grb: continue   # a bend or a joint of two pieces of one street — not a junction
        g = NB[gid]; z = zone_of(g['x'], g['y'])
        if z not in BZ and not any(e.get('plan') in built_seg_ids for e in GE if gid in (e['a'], e['b'])): continue
        d, nid = mn((math.hypot(m['x'] - g['x'], m['y'] - g['y']), m['id']) for m in P['nodes'])
        note = X.get(('game-junction', gid))
        if d <= TOL:
            k = MN[nid]['kind']; c = gctl(gid); cok = c in KIND_OK.get(k, {c})
            row('junction', 'game→map', nid, gid, z, d, cok, note or f'במשחק {KHE.get(c, c)}, במפה {KHE.get(k, k)}', None if cok else X.get(('junction-fix', nid), FIX_ASK), kind_map=k, kind_game=gctl(gid))
        else:
            # a junction of the game that is a mouth of a lot road in the map (a driveway, the road of a lot)
            dd = min(dpoly(g['x'], g['y'], r.get('draw') or r['pts']) for r in P['site_roads'] if not r.get('replaced'))
            dt = min((dpoly(g['x'], g['y'], t) for t in TEMPS), default=1e9)
            if dt <= 60:
                row('junction', 'game→map', None, gid, z, dt, True, note or 'חיבור זמני של המפה (עד שהאזור השכן נבנה)', None, kind_game=gctl(gid))
            elif dd <= 70:
                row('junction', 'game→map', None, gid, z, dd, True, note or 'במפה — פתח של דרך פנימית (כניסה למגרש), לא צומת ברשת', None, kind_game=gctl(gid))
            else:
                row('junction', 'game→map', None, gid, z, d, False, note or f'במשחק ולא במפה (הקרוב במפה {nid}, ‏{m1(d)} מ׳)', X.get(('game-junction-fix', gid), FIX_ASK), kind_game=gctl(gid))
    # ------------------------------------------------------------------ 3 · crosswalks
    def arm_dir(gid, eid):
        e = next(q for q in G['edges'] if q['id'] == eid); o = NB[e['b'] if e['a'] == gid else e['a']]; n = NB[gid]
        L = math.hypot(o['x'] - n['x'], o['y'] - n['y']) or 1; return (o['x'] - n['x']) / L, (o['y'] - n['y']) / L
    GX = [dict(id=c['id'], x=c['x'], y=c['y'], road=c['road'], node=c.get('node'), src='xw') for c in G['xw']]
    GX += [dict(id=c['id'], x=c['x'], y=c['y'], road=c['road'], node=c.get('node'), src='zebra') for c in G.get('zebra', [])]
    GX += [dict(id=c['id'], x=c['x'], y=c['y'], road=c['road'], node=None, src='drawn') for c in G.get('drawn', [])]
    for rid, rb in (G.get('RB2') or {}).items():
        for eid, dist in (rb.get('xw') or {}).items():
            ux, uy = arm_dir(rid, eid); GX.append(dict(id=f'RB-{rid}-{eid}', x=rb['x'] + ux * dist, y=rb['y'] + uy * dist, road=eid, node=rid, src='roundabout'))
    for i_, r_ in enumerate(((G.get('TERM') or {}).get('xw') or [])[:4]):
        if isinstance(r_, list) and len(r_) == 4: GX.append(dict(id=('X-AE', 'X-BE', 'X-AN', 'X-BS')[i_], x=(r_[0] + r_[2]) / 2, y=(r_[1] + r_[3]) / 2, road='המסוף', node='E3-BUS', src='terminal'))
    MX = []
    for c in P['bus']['crosswalks']:
        if c['node'] not in mnodes and c.get('seg') not in built_seg_ids and not c.get('r9s'): continue
        m = (c['d0'] + c['d1']) / 2; x, y = c['at'][0] + c['u'][0] * m, c['at'][1] + c['u'][1] * m
        MX.append(dict(id=f"{c['node']}·{c['seg']}", x=x, y=y, node=c['node'], seg=c['seg'], d=m))
    for c in ((P['bus'].get('terminal') or {}).get('r9') or {}).get('crossings', []):
        r = c['r']; MX.append(dict(id=c['id'], x=(r[0] + r[2]) / 2, y=(r[1] + r[3]) / 2, node='E3-BUS', seg='המסוף', d=0))
    for c in MX:
        d, g = mn((math.hypot(q['x'] - c['x'], q['y'] - c['y']), q) for q in GX) if GX else (1e9, None)
        z = zone_of(c['x'], c['y']); note = X.get(('crosswalk', c['id']))
        ok = d <= TOL
        if not note:
            note = f"{g['id']}" if ok else (f"במשחק — {g['id']} ב-{m1(d)} מ׳" if d <= 250 else 'אין מעבר במשחק בזרוע הזו')
        row('crosswalk', 'map→game', c['id'], g['id'] if g and d <= 250 else None, z, d, ok, note, None if ok else X.get(('crosswalk-fix', c['id']), FIX_ASK),
            from_junction_m=m1(c['d']))
    for g in GX:
        z = zone_of(g['x'], g['y'])
        if z not in BZ and not (g.get('node') in ('J54_26', 'J61_26')): continue
        d, c = mn((math.hypot(q['x'] - g['x'], q['y'] - g['y']), q) for q in MX) if MX else (1e9, None)
        ok = d <= TOL; note = X.get(('game-crosswalk', g['id']))
        if not note: note = c['id'] if ok else (f"במפה — {c['id']} ב-{m1(d)} מ׳" if d <= 250 else 'במשחק ולא במפה')
        row('crosswalk', 'game→map', c['id'] if c and d <= 250 else None, g['id'], z, d, ok, note, None if ok else X.get(('game-crosswalk-fix', g['id']), FIX_ASK), src=g['src'])
    # ------------------------------------------------------------------ 4 · bus bays
    GS = [dict(id=s['id'], x=s.get('x', s.get('roadX')), y=s.get('y', s.get('roadY')), chunk=s.get('chunk'), line=s.get('line')) for s in G['stops']]
    for b_ in ((G.get('TERM') or {}).get('bays') or []):
        r_ = b_.get('rect') if isinstance(b_, dict) else None
        if isinstance(r_, list) and len(r_) == 4: GS.append(dict(id=b_.get('id'), x=(r_[0] + r_[2]) / 2, y=(r_[1] + r_[3]) / 2, chunk='E3', line=b_.get('line')))
    for s_ in G.get('S6_MAP_STOPS') or []:
        if isinstance(s_, dict) and isinstance(s_.get('x'), (int, float)): GS.append(dict(id=s_['id'], x=s_['x'], y=s_['y'], chunk=s_.get('chunk'), line=None))
    MB = []
    for st in P['bus']['stops']:
        for k, b in enumerate(st.get('bay_list') or []):
            x, y = b['pole']; MB.append(dict(id=f"{st['id']}/{b['side']:+d}", stop=st['id'], x=x, y=y, seg=st.get('seg'), name=st.get('name')))
    T = P['bus'].get('terminal') or {}
    for b in T.get('bays', []):
        r = b['rect']; MB.append(dict(id=f"E3-BUS/{b['no']}", stop='E3-BUS', x=(r[0] + r[2]) / 2, y=(r[1] + r[3]) / 2, seg=None, name='מסוף האוטובוסים — מפרץ ' + str(b['no'])))
    for b in T.get('hold', []):
        r = b['rect']; MB.append(dict(id=f"E3-HOLD/{b['no']}", stop='E3-BUS', x=(r[0] + r[2]) / 2, y=(r[1] + r[3]) / 2, seg=None, name='מסוף האוטובוסים — מקום המתנה ' + str(b['no'])))
    for b in MB:
        z = zone_of(b['x'], b['y'])
        if z not in BZ and b['seg'] not in built_seg_ids: continue
        d, g = mn((math.hypot(q['x'] - b['x'], q['y'] - b['y']), q) for q in GS)
        ok = d <= TOL; note = X.get(('bay', b['id']))
        if not note: note = (g['id'] if ok else (f"במשחק — {g['id']} ב-{m1(d)} מ׳" if d <= 300 else 'המפרץ של המפה עוד לא במשחק'))
        row('bay', 'map→game', b['id'], g['id'] if d <= 300 else None, z, d, ok, note, None if ok else X.get(('bay-fix', b['id']), FIX_GAME), name=b['name'])
    for g in GS:
        z = zone_of(g['x'], g['y'])
        if z not in BZ: continue
        d, b = mn((math.hypot(q['x'] - g['x'], q['y'] - g['y']), q) for q in MB)
        ok = d <= TOL; note = X.get(('game-bay', g['id']))
        chunk_ok = (g.get('chunk') in (None, z))
        if not note:
            note = (b['id'] if ok else (f"במפה — {b['id']} ב-{m1(d)} מ׳" if d <= 300 else 'במשחק ולא במפה'))
            if not chunk_ok: note += f" · האזור הרשום בתחנה {g['chunk']}, והיא עומדת ב-{z}"
        row('bay', 'game→map', b['id'] if d <= 300 else None, g['id'], z, d, ok and chunk_ok, note,
            None if (ok and chunk_ok) else X.get(('game-bay-fix', g['id']), FIX_GAME), chunk_game=g.get('chunk'), chunk_real=z)
    # ------------------------------------------------------------------ 5 · lots (the lots, the sites and the items of round 7 that have a rectangle)
    GF = []
    def addf(i, r, lab, src):
        if r and len(r) == 4 and r[2] > r[0] and r[3] > r[1]: GF.append(dict(id=i, r=r, label=lab or '', src=src))
    for b in G.get('C4_BUILDINGS', []):
        if isinstance(b, dict):
            r = b.get('r') if isinstance(b.get('r'), list) else ([b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h']] if all(isinstance(b.get(k), (int, float)) for k in 'xywh') else None)
            addf(b.get('id'), r, b.get('label'), 'מבנה')
    for k in ('D2_PARKING', 'E3_LOTS', 'A4_LOTS', 'C2_LOTS', 'C3_LOTS', 'A6_LOTS'):   # 9ע: the platforms of E3 are a station, not a lot
        for b in G.get(k, []) or []:
            if isinstance(b, dict) and all(isinstance(b.get(q), (int, float)) for q in 'xywh'): addf(b['id'], [b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h']], b.get('label'), k)
    for b in G.get('C2_BUILDINGS', []) or []:
        if isinstance(b, dict) and isinstance(b.get('r'), list): addf(b['id'], b['r'], b.get('label'), 'C2_BUILDINGS')
    if isinstance(G.get('D2_POOL'), dict): addf('D2_POOL', rect_of(G['D2_POOL']), 'הבריכה של המלון', 'D2_POOL')
    for b in (G.get('D2_ISLANDS') or []): addf(b['id'], rect_of(b), 'האי של ההורדה', 'D2_ISLANDS')
    for b in (G.get('D2_BUILDINGS') or []):
        if isinstance(b, dict): addf(b['id'], [b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h']], b.get('label'), 'D2_BUILDINGS')
    for k in ('B4_LOTS', 'B3N_LOTS'):
        for b in G.get(k, []) or []:
            y = b.get('yard') if isinstance(b, dict) else None
            if isinstance(y, dict): addf(b['id'], [y['x'], y['y'], y['x'] + y['w'], y['y'] + y['h']], b.get('label'), k)
    for k, src in (('A2G', 'A2G'), ('A5G', 'A5G')):
        for q, v in (G.get(k) or {}).items():
            if isinstance(v, list) and len(v) == 4 and all(isinstance(t, (int, float)) for t in v): addf(f'{k}.{q}', v, LHE.get(q, q), src)
    B = G.get('B12') or {}
    for q in ('golf', 'play', 'picnic', 'boatPier', 'booth', 'box'):
        if isinstance(B.get(q), list): addf(f'B12.{q}', B[q], LHE.get(q, q), 'B12')
    for q in ('b1p', 'b201'):
        v = B.get(q) or {}
        if isinstance(v.get('rect'), list): addf(f'B12.{q}', v['rect'], LHE.get(q, q), 'B12')
        elif isinstance(v.get('aisle'), list): addf(f'B12.{q}', [v['aisle'][0], (v.get('sy') or [v['aisle'][1]])[0], v['aisle'][2], v['aisle'][3]], LHE.get(q, q), 'B12')
    for p in (B.get('piers') or []):
        for q in ('stem', 'head'):
            if isinstance(p.get(q), list): addf(p['id'] + '.' + q, p[q], p.get('label'), 'B12')
    for b in (G.get('B2_PIER') and [G['B2_PIER']] or []):
        inf = G.get('B2_PIER_INFO') or {}
        if 'w' in inf: addf(b['id'], [b['x'], b['y'] - inf['h'] / 2, b['x'] + inf['w'], b['y'] + inf['h'] / 2], b.get('label'), 'B2_PIER')
    for k in ('E4_BUILDINGS', 'E5_BUILDINGS', 'F34_BUILDINGS'):
        for b in G.get(k) or []:
            q = (b.get('s9') or {}) if isinstance(b, dict) else {}
            if isinstance(q.get('rect'), list): addf(b['id'], q['rect'], b.get('label'), k + ':' + str(q.get('lot')))
    lotb = {}
    for k in ('E4_STALLS', 'F34_STALLS', 'E4_TRUCK_STALLS'):
        for b in G.get(k) or []:
            r = rect_of(b)
            if r and isinstance(b, dict) and b.get('lot'):
                o = lotb.setdefault(b['lot'], list(r)); o[0] = min(o[0], r[0]); o[1] = min(o[1], r[1]); o[2] = max(o[2], r[2]); o[3] = max(o[3], r[3])
    for i, r in lotb.items(): addf(i, r, 'חניון ' + i, 'stalls')
    for k in ('E4_ACCESS', 'F34_ACCESS'):
        for b in G.get(k) or []: addf(b.get('id'), rect_of(b), b.get('label'), k)
    for k in ('F34_DECKS', 'F56_DECKS'):
        for i, r in enumerate(G.get(k) or []): addf(f'{k}.{i}', rect_of(r), 'דק — טיילת, מזח או מרפסת', k)
    sol = (G.get('E4_SOLAR') or {}).get('panels'); addf('E4-SOLAR-PANELS', rect_of(sol), 'השדה הסולרי', 'E4_SOLAR')
    for b in G.get('F56_BUOYS') or []:
        if isinstance(b, dict) and isinstance(b.get('x'), (int, float)): addf(b['id'], [b['x'] - 12, b['y'] - 12, b['x'] + 12, b['y'] + 12], 'מצוף', 'F56_BUOYS')
    addf('E5-DEPOT-TRACKS', rect_of(G.get('E5_DEPOT_TRACKS')), 'פסי מוסך הרכבות', 'E5'); addf('F6-BOOTH', rect_of(G.get('F56_BOOTH')), 'ביתן השומר', 'F56')
    for k in ('C4ND', 'D4ND', 'D5ND'):
        for b in (G.get(k) or {}).get('buildings', []) or []:
            if isinstance(b.get('lot'), list) and len(b['lot']) == 4 and all(isinstance(t, (int, float)) for t in b['lot']): addf(b['id'] + '.lot', b['lot'], b.get('label'), k)
    ML = []
    def addm(i, z, r, lab, kind, src, st=None):
        if r and len(r) == 4 and all(isinstance(t, (int, float)) for t in r) and z in BZ: ML.append(dict(id=i, zone=z, r=r, label=lab or '', kind=kind, src=src, status=st))
    for l in P['lots']: addm(l['id'], l['zone'], l.get('rect'), l.get('label'), l.get('use'), 'lot', l.get('status'))
    for l in P['sites']: addm(l['id'], l['zone'], l.get('rect'), l.get('label'), l.get('kind'), 'site', l.get('status'))
    for l in P['r7']['items']:
        if l.get('rect'): addm(l['id'], l['zone'], l['rect'], l.get('label'), l.get('kind'), 'r7', l.get('status'))
    for k in ((P.get('terrain') or {}).get('lake') or {}).get('keep', []):
        addm(k['id'], zone_of(k['x'], k['y']), [k['x'] - 30, k['y'] - 30, k['x'] + 30, k['y'] + 30], k.get('label'), 'keep', 'lake', None)
    for l in P.get('r9ayin_lots', []): addm(l['id'], l['zone'], l['rect'], l.get('label'), l.get('kind'), 'r9ayin', l.get('status'))
    for l in P.get('r9s_lots', []): addm(l['id'], l['zone'], l['rect'], l.get('label'), l.get('kind'), 'r9s', l.get('status'))
    # the ground of the zone drawings of the game (lawns, beds, yards, courts, plazas, paths) — for the lots that are not a building
    GZ = list(GA)
    for k in ('D3ND', 'C4ND', 'D4ND', 'C5ND', 'D5ND', 'B5ND', 'A5ND', 'A2ND', 'B4G', 'A34D', 'C3D', 'B3LOOKD', 'B3NG', 'A2G', 'A5G'):
        for q, vv in (G.get(k) or {}).items():
            for v in (vv if isinstance(vv, list) else [vv]):
                if isinstance(v, list) and len(v) >= 4 and all(isinstance(t, (int, float)) for t in v[:4]) and v[2] > v[0] and v[3] > v[1]: GZ.append(v[:4])
    BLD = re.compile(r'(building|home|shop|work|hotel|station|office|depot|refinery|plant|hall|school|clinic|store|kiosk|cafe|wc|gate|substation)', re.I)
    def cover(r, feats):
        nx = max(2, min(20, int((r[2] - r[0]) / 10))); ny = max(2, min(20, int((r[3] - r[1]) / 10))); n = k = 0
        cand = [f for f in feats if rov(r, f) > 0]
        for i in range(nx):
            for j in range(ny):
                x = r[0] + (i + .5) * (r[2] - r[0]) / nx; y = r[1] + (j + .5) * (r[3] - r[1]) / ny; n += 1
                if any(f[0] <= x <= f[2] and f[1] <= y <= f[3] for f in cand): k += 1
        return k / max(1, n)
    for m in ML:
        if (m.get('status') or {}).get('state') in ('הוחלף', 'בוטל'):
            row('lot', 'map→game', m['id'], None, m['zone'], None, True, 'הוחלף — ' + (m['status'].get('by') or ''), FIX_MAP, label=m['label'][:80], src=m['src']); continue
        r = m['r']; area = max(1, (r[2] - r[0]) * (r[3] - r[1]))
        hits = sorted(((rov(r, g['r']) / max(1, min(area, (g['r'][2] - g['r'][0]) * (g['r'][3] - g['r'][1]))), g) for g in GF if rov(r, g['r']) > 0), key=lambda t: -t[0])
        isb = bool(BLD.search(str(m['kind']) + ' ' + m['id'])) and m['src'] != 'lot'
        cv = cover(r, [g['r'] for g in GF] + ([] if isb else GZ))
        note = X.get(('lot', m['id']))
        good = (hits and hits[0][0] >= 0.2) or (not isb and cv >= 0.2)
        if good:
            what = ', '.join((g['label'] or g['id'])[:30] for s_, g in hits[:2] if s_ >= 0.2) or f'קרקע מעוצבת באזור ({round(cv * 100)}% מהמגרש)'
            row('lot', 'map→game', m['id'], ', '.join(g['id'] for s_, g in hits[:3] if s_ >= 0.2) or None, m['zone'], 0, True, note or 'במשחק: ' + what,
                None, label=m['label'][:80], src=m['src'], cover=round(cv, 2))
        else:
            d, g = mn((rgap(r, q['r']), q) for q in GF) if GF else (1e9, None)
            row('lot', 'map→game', m['id'], g['id'] if g and d <= 300 else None, m['zone'], d, False,
                note or ('אין במשחק ' + ('מבנה' if isb else 'מבנה, מגרש או קרקע מעוצבת') + ' על המגרש של המפה' + (f" (הקרוב: {g['id']}, ‏{m1(d)} מ׳)" if g and d <= 300 else '')),
                X.get(('lot-fix', m['id']), FIX_ASK), label=m['label'][:80], src=m['src'], cover=round(cv, 2))
    for g in GF:
        z = zone_of((g['r'][0] + g['r'][2]) / 2, (g['r'][1] + g['r'][3]) / 2)
        if z not in BZ: continue
        r = g['r']; garea = max(1, (r[2] - r[0]) * (r[3] - r[1]))
        live = [m for m in ML if (m.get('status') or {}).get('state') not in ('הוחלף', 'בוטל')]
        hits = sorted(((rov(r, m['r']) / garea, m) for m in live if rov(r, m['r']) > 0), key=lambda t: -t[0])
        note = X.get(('game-lot', g['id']))
        if hits and hits[0][0] >= 0.2:
            row('lot', 'game→map', hits[0][1]['id'], g['id'], z, 0, True, note or f"בתוך {hits[0][1]['id']}", None, label=g['label'][:60], src=g['src'])
        else:
            d, m = mn((rgap(r, q['r']), q) for q in live) if live else (1e9, None)
            ok = d <= TOL
            row('lot', 'game→map', m['id'] if m and d <= 300 else None, g['id'], z, d, ok, note or ('במשחק ולא במפה' + (f" (הקרוב: {m['id']}, ‏{m1(d)} מ׳)" if m and d <= 300 else '')),
                None if ok else X.get(('game-lot-fix', g['id']), FIX_ASK), label=g['label'][:60], src=g['src'])
    return rows, BZ
