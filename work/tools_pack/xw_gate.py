#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3.11 23:35 · xw_gate — שתי בדיקות של מעברי החצייה, שתיהן עוצרות מסירה (הביקורת 23:16, אחרי מה שהבעלים מצא ב-AIR-W0 / J46_16):
  1. בכל צומת עם רמזור — מעבר בכל זרוע. החריגים היחידים: צומת T לפי D‑439 (על הכביש הראשי נשאר רק המעבר שמשמאל לנהג
     שיוצא מהרחוב הצדדי, והמעבר על הרחוב הצדדי קיים), וחריג רשום לפי D‑427 או D‑430 (tools_pack/xw_exceptions.json, עם סיבה).
  2. מפת הדרכים מול המשחק — כל מעבר שיש במפה (city_plan.json, ‏bus.crosswalks) בצומת שבנוי במשחק, קיים גם במשחק.
usage: python3 xw_gate.py <xw_dump.json> <out.json> [--prev <prev_xw_dump.json>] [--md <out.md>]
  xw_dump.json — מ-clean_r2b_025637/tools/dev/xw_dump.js. ‏--prev — הרשימה של המעברים שנוספו ושיצאו, לפי צומת וזרוע.
היציאה: 0 — שתי הבדיקות עברו; 1 — אחת מהן נכשלה."""
import sys, os, json, math, argparse
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('dump'); ap.add_argument('out'); ap.add_argument('--prev'); ap.add_argument('--md')
ap.add_argument('--plan', default=os.path.join(W, 'study', 'roads', 'city_plan.json')); ap.add_argument('--exc', default=os.path.join(W, 'tools_pack', 'xw_exceptions.json'))
A = ap.parse_args()
G = json.load(open(A.dump, encoding='utf-8')); P = json.load(open(A.plan, encoding='utf-8'))
EXC = json.load(open(A.exc, encoding='utf-8')).get('rows', []) if os.path.exists(A.exc) else []
NB = {n['id']: n for n in G['nodes']}; EB = {e['id']: e for e in G['edges']}
SIG = set(G['signals']) & set(G['inter']); INTER = set(G['inter'])
DIRS = {(1, 0): 'מזרחית', (-1, 0): 'מערבית', (0, 1): 'דרומית', (0, -1): 'צפונית'}
def side(u):
    k = max(DIRS, key=lambda d: d[0] * u[0] + d[1] * u[1]); return DIRS[k]
def arms(nid):
    out = []
    for e in G['edges']:
        if e['future'] or nid not in (e['a'], e['b']): continue
        n = NB[nid]; q = (e['p1'] if e['a'] == nid else e['pn']) or None
        if not q: o = NB.get(e['b'] if e['a'] == nid else e['a']); q = [o['x'], o['y']] if o else None
        if not q: continue
        dx, dy = q[0] - n['x'], q[1] - n['y']; L = math.hypot(dx, dy) or 1
        o = NB.get(e['b'] if e['a'] == nid else e['a']); Lf = math.hypot(o['x'] - n['x'], o['y'] - n['y']) if o else None
        out.append(dict(road=e['id'], name=e['name'], cls=e['cls'], u=(dx / L, dy / L), len=Lf, other=(e['b'] if e['a'] == nid else e['a'])))
    return out
def xws_on(nid, road):
    n = NB[nid]; r = []
    e0 = EB.get(road); o0 = NB.get(e0['b'] if e0 and e0['a'] == nid else e0['a']) if e0 else None
    Lr = math.hypot(o0['x'] - n['x'], o0['y'] - n['y']) if o0 else 0
    for c in G['xw']:   # a crossing of this junction on the arm — or any crossing on the arm within 25 m of the junction (a short arm between two junctions has one crossing for both)
        if c['road'] != road: continue
        if c['node'] == nid or math.hypot(c['x'] - n['x'], c['y'] - n['y']) <= min(Lr, 250): r.append(c['id'])
    for z in G['zebra'] + G.get('drawn', []):
        if z['road'] != road: continue
        e = EB.get(road)
        if not e: continue
        o = NB.get(e['b'] if e['a'] == nid else e['a'])
        d0 = math.hypot(z['x'] - n['x'], z['y'] - n['y']); d1 = math.hypot(z['x'] - o['x'], z['y'] - o['y']) if o else 1e9
        if (d0 <= d1 and d0 < 420) or d0 <= min(Lr, 250) or z.get('node') == nid: r.append(z['id'])   # 4.11 (the builder, try380): a zebra of this junction counts like a crossing of its signal (J31_16 south — the zebra past the pass point)
    return r
def exc(nid, road, mapnode=None, seg=None):
    for x in EXC:
        if (x.get('node') == nid and x.get('road') == road) or (mapnode and x.get('mapnode') == mapnode and x.get('seg') == seg): return x
    return None
TR = {(a, b) for a, b in G.get('tRule', [])}
# ---------------------------------------------------------------- check 1: a crossing on every arm of every junction with a signal
J1 = []; F1 = []
for nid in sorted(SIG):
    A_ = arms(nid); rows = []; n = NB[nid]
    for a in A_: a['xw'] = xws_on(nid, a['road'])
    missing = [a for a in A_ if not a['xw']]
    for a in missing:
        why = None; ok = False; x = exc(nid, a['road'])
        if x and x.get('rule') in ('D‑427', 'D‑430'): ok = True; why = x['rule'] + ' (רשום): ' + x.get('why', '')
        elif len(A_) == 3:
            # D‑439: the side street is the arm with no opposite arm; the main road = the two opposite arms
            opp = lambda p, q: p['u'][0] * q['u'][0] + p['u'][1] * q['u'][1] < -0.7
            sides = [s for s in A_ if not any(opp(s, t) for t in A_ if t is not s)]
            if len(sides) == 1 and a is not sides[0]:
                s = sides[0]; left = (-s['u'][1], s['u'][0])           # the left of a driver who leaves the side street (y down)
                main = [t for t in A_ if t is not s]; kept = [t for t in main if t is not a][0]
                lk = kept['u'][0] * left[0] + kept['u'][1] * left[1]
                if not s['xw']: why = 'D‑439 — אבל אין מעבר על הרחוב הצדדי (' + s['road'] + ')'
                elif lk <= 0: why = 'D‑439 — אבל יצא המעבר הלא נכון: נשאר ' + kept['road'] + ' (מימין לנהג שיוצא מ-' + s['road'] + '), והיה צריך להישאר ' + a['road']
                else: ok = True; why = 'D‑439: צומת T — נשאר רק המעבר שמשמאל לנהג שיוצא מ-' + s['road'] + ' (' + kept['road'] + ')'
            else: why = 'הזרוע של הרחוב הצדדי בצומת T — חייב מעבר'
        else: why = 'צומת של ' + str(len(A_)) + ' זרועות — מעבר בכל זרוע (D‑426)'
        a['why'] = why; a['ok'] = ok
        if not ok: F1.append(dict(node=nid, zone=G.get('zones', {}).get(nid, ''), road=a['road'], name=a['name'], arm=side(a['u']), why=why, len_m=round((a['len'] or 0) / 10, 1)))
    J1.append(dict(node=nid, zone=G.get('zones', {}).get(nid, ''), arms=len(A_), xw=sum(1 for a in A_ if a['xw']),
                   rows=[dict(road=a['road'], name=a['name'], arm=side(a['u']), xw=a['xw'], ok=bool(a['xw']) or a.get('ok', False), why=a.get('why', '')) for a in A_]))
# ---------------------------------------------------------------- check 2: every crossing of the road map at a junction built in the game is in the game
MN = {n['id']: n for n in P['nodes']} if isinstance(P['nodes'], list) else P['nodes']
F2 = []; M2 = []; PEND = []; notbuilt = 0
for c in P['bus']['crosswalks']:
    mx, my = c['at']; best = None
    for nid in INTER:
        n = NB[nid]; d = math.hypot(n['x'] - mx, n['y'] - my)
        if d <= 45 and (best is None or d < best[1]): best = (nid, d)
    if not best: notbuilt += 1; continue
    nid = best[0]; A_ = arms(nid); u = c['u']
    a = max(A_, key=lambda t: t['u'][0] * u[0] + t['u'][1] * u[1]) if A_ else None
    row = dict(mapnode=c['node'], seg=c['seg'], node=nid, zone=G.get('zones', {}).get(nid, ''), arm=side(u))
    if not a or a['u'][0] * u[0] + a['u'][1] * u[1] < 0.8:   # the arm of the map is not built yet (a road into a zone of a later stage) — listed, not a failure; the roads against the map — rules_gate / sync
        row['why'] = 'הזרוע של המפה (' + c['seg'] + ') עוד לא בנויה בצומת ' + nid + ' — המעבר נכנס עם הזרוע'; PEND.append(row); continue
    row['road'] = a['road']; row['name'] = a['name']; got = xws_on(nid, a['road']); row['xw'] = got
    if got: M2.append(row); continue
    x = exc(nid, a['road'], c['node'], c['seg'])
    if x: row['why'] = x.get('rule', '') + ' (רשום): ' + x.get('why', ''); M2.append(row); continue
    row['why'] = 'במפה יש מעבר בזרוע ה' + side(u) + ' (' + c['seg'] + '), ובמשחק אין (' + a['road'] + ')'; F2.append(row)
# the T junctions of the map (D‑439, P['r9']['xw_t']): the crossing that the map took out (to the right of the driver who leaves the side street) is not in the game either
SEGB = {s_['id']: s_ for s_ in P['segments']}; MNB = {n['id']: n for n in P['nodes']}
for r in (P.get('r9') or {}).get('xw_t', []):
    mn = MNB.get(r['node']); gone = r['removed'].split('(')[-1].rstrip(')'); sg = SEGB.get(gone)
    if not mn or not sg: continue
    best = min(((nid, math.hypot(NB[nid]['x'] - mn['x'], NB[nid]['y'] - mn['y'])) for nid in INTER), key=lambda t: t[1])
    if best[1] > 45: continue
    nid = best[0]; pts = sg['pts']; q = pts[1] if sg['a'] == r['node'] else pts[-2]; L = math.hypot(q[0] - mn['x'], q[1] - mn['y']) or 1; u = ((q[0] - mn['x']) / L, (q[1] - mn['y']) / L)
    A_ = arms(nid); a = max(A_, key=lambda t: t['u'][0] * u[0] + t['u'][1] * u[1]) if A_ else None
    if not a or a['u'][0] * u[0] + a['u'][1] * u[1] < 0.8 or len(A_) != 3: continue   # a junction of 4 arms in the game — D‑439 does not apply ("צמתים של 4 זרועות — בלי שינוי")
    got = xws_on(nid, a['road'])
    if got: F2.append(dict(mapnode=r['node'], seg=gone, node=nid, zone=G.get('zones', {}).get(nid, ''), arm=side(u), road=a['road'], xw=got,
                           why='D‑439: במפה המעבר הזה יצא (מימין לנהג שיוצא מ' + r['side'] + '), ובמשחק הוא קיים (' + a['road'] + ')'))
# ---------------------------------------------------------------- the crossings that were added / went out against the previous build
ADD = []; OUT = []
if A.prev:
    Q = json.load(open(A.prev, encoding='utf-8'))
    key = lambda c: c['id']
    old = {key(c): c for c in Q['xw'] + Q['zebra'] + Q.get('drawn', [])}; new = {key(c): c for c in G['xw'] + G['zebra'] + G.get('drawn', [])}
    def where(c, D):
        nb = {n['id']: n for n in D['nodes']}; nid = c.get('node')
        if not nid:   # a zebra: the nearest end of its road
            e = next((e for e in D['edges'] if e['id'] == c['road']), None)
            if e: nid = min((e['a'], e['b']), key=lambda k: math.hypot(nb[k]['x'] - c['x'], nb[k]['y'] - c['y']) if k in nb else 1e9)
        n = nb.get(nid); arm = side(((c['x'] - n['x']), (c['y'] - n['y']))) if n else ''
        return dict(id=c['id'], node=nid, zone=D.get('zones', {}).get(nid, ''), road=c['road'], arm=arm, x=c['x'], y=c['y'])
    ADD = [where(new[k], G) for k in sorted(set(new) - set(old))]; OUT = [where(old[k], Q) for k in sorted(set(old) - set(new))]
res = dict(build=G.get('build', ''), ok=not F1 and not F2,
           check1=dict(name='מעבר בכל זרוע של צומת עם רמזור', junctions=len(J1), arms=sum(j['arms'] for j in J1), xw=sum(j['xw'] for j in J1), fails=F1, table=J1),
           check2=dict(name='מעברי המפה בצמתים שבנויים במשחק', map_total=len(P['bus']['crosswalks']), not_built=notbuilt, matched=len(M2), pending_arm=PEND, fails=F2, ok_rows=M2),
           added=ADD, removed=OUT, exceptions=EXC)
json.dump(res, open(A.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# מעברי החצייה — ' + res['build'], '',
     '**בדיקה 1 — מעבר בכל זרוע של צומת עם רמזור:** ' + ('עברה' if not F1 else 'נכשלה') + f" · {len(J1)} צמתים, {res['check1']['arms']} זרועות, {res['check1']['xw']} זרועות עם מעבר · חסרים בלי חריג: {len(F1)}"]
for f in F1: L.append(f"- {f['zone']} · {f['node']} · הזרוע ה{f['arm']} ({f['road']}, {f['name']}, {f['len_m']} מ׳): {f['why']}")
L += ['', '**בדיקה 2 — מעברי המפה בצמתים שבנויים במשחק:** ' + ('עברה' if not F2 else 'נכשלה') + f" · במפה {len(P['bus']['crosswalks'])}, בצמתים שלא בנויים {notbuilt}, בזרועות שעוד לא בנויות {len(PEND)}, קיימים {len(M2)}, חסרים {len(F2)}"]
for f in F2: L.append(f"- {f['zone']} · {f['mapnode']} (במשחק {f['node']}) · הזרוע ה{f['arm']}: {f['why']}")
if PEND: L += ['', f'זרועות של המפה שעוד לא בנויות במשחק ({len(PEND)}; לא כישלון — המעבר נכנס עם הזרוע):'] + [f"- {f['zone']} · {f['mapnode']} (במשחק {f['node']}) · הזרוע ה{f['arm']} ({f['seg']})" for f in PEND]
if A.prev: L += ['', f'**נוספו {len(ADD)} מעברים, יצאו {len(OUT)}** (מול הבנייה הקודמת):'] + [f"- נוסף: {a['zone']} · {a['node']} · הזרוע ה{a['arm']} ({a['road']}) — {a['id']}" for a in ADD] + [f"- יצא: {a['zone']} · {a['node']} · הזרוע ה{a['arm']} ({a['road']}) — {a['id']}" for a in OUT]
if A.md: open(A.md, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L[:3] + [L[i] for i in range(len(L)) if L[i].startswith('**בדיקה 2') or L[i].startswith('**נוספו')]))
sys.exit(0 if res['ok'] else 1)
