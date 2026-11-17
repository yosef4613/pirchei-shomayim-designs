#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-15 (the owner 29.10 12:00): one list for the whole city — redundant roads, junctions too close or at a sharp angle, flow that is not right.
Reads game_roads.json (probe_roads.js — byNode / byEdge of the game, 146 nodes, 183 edges, 10 px = 1 m) and writes roads_audit.json.
The airport (F–G, the field roads) is frozen until stage 8 (R-32) — listed apart, not proposed now.
Method (all from the numbers, no hand picks):
 * the network is first joined into streets: a node of degree 2 that is not a junction (a chunk boundary) is folded into its street;
 * a short street (< 70 m) whose two ends are also joined by another way at most 1.6 × its length + 60 m → "doubles a nearby road";
 * two junctions closer than 45 m along one street → "too close" (two signal heads in one queue);
 * an angle under 60° between two streets at a junction → "sharp angle";
 * a dead end inside the city (degree 1, not on the world's edge and not a future link) → "dead end";
 * a junction of four streets or more on a local street with an arterial → "a busy crossing on a local street" (flow);
 * the owner's two examples are checked by name."""
import json, math, os, collections, heapq
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(H, 'game_roads.json'), encoding='utf-8'))
N = {n['id']: n for n in D['nodes']}
EDGES = [e for e in D['edges']]
W, HH = D['world']['w'], D['world']['h']
adj = collections.defaultdict(list)
for e in EDGES: adj[e['a']].append(e); adj[e['b']].append(e)
dist = lambda a, b: math.hypot(N[a]['x'] - N[b]['x'], N[a]['y'] - N[b]['y']) / 10.0
chunk = lambda x, y: 'ABCDEFGH'[min(7, int(x // 1200))] + str(1 + min(9, int(y // 850)))
AIR = lambda x, y: chunk(x, y)[0] in 'FG' and int(chunk(x, y)[1:]) <= 3 or chunk(x, y) in ('E2',)   # the field — frozen (R-32)
JUNC = lambda nid: N[nid]['type'] in ('intersection', 'major') and len(adj[nid]) != 2 or len(adj[nid]) >= 3
# ---- streets: chains between junctions / ends ----
streets, seen = [], set()
for s in N:
    if not JUNC(s) and len(adj[s]) == 2: continue
    for e0 in adj[s]:
        if e0['id'] in seen: continue
        chain, cur, e = [s], s, e0
        while True:
            seen.add(e['id']); nxt = e['b'] if e['a'] == cur else e['a']; chain.append(nxt)
            if JUNC(nxt) or len(adj[nxt]) != 2: break
            e = [q for q in adj[nxt] if q['id'] != e['id']][0]; cur = nxt
        ids = []; L = 0
        for i in range(len(chain) - 1):
            q = [x for x in adj[chain[i]] if (x['a'], x['b']) in ((chain[i], chain[i + 1]), (chain[i + 1], chain[i]))][0]; ids.append(q); L += dist(chain[i], chain[i + 1])
        streets.append({'a': chain[0], 'b': chain[-1], 'nodes': chain, 'edges': [q['id'] for q in ids], 'len': round(L, 1), 'cls': max((q['cls'] for q in ids), key=['local', 'avenue', 'arterial'].index),
                        'name': ids[0]['name'], 'future': any(q['future'] for q in ids)})
G = collections.defaultdict(list)
for i, s in enumerate(streets):
    G[s['a']].append((s['b'], s['len'], i)); G[s['b']].append((s['a'], s['len'], i))
def alt(i):
    s = streets[i]; best = {s['a']: 0}; pq = [(0, s['a'])]
    while pq:
        d, u = heapq.heappop(pq)
        if u == s['b']: return d
        if d > best.get(u, 1e9): continue
        for v, l, j in G[u]:
            if j == i or streets[j]['future']: continue
            if d + l < best.get(v, 1e9): best[v] = d + l; heapq.heappush(pq, (d + l, v))
    return None
mid = lambda s: ((N[s['a']]['x'] + N[s['b']]['x']) / 2, (N[s['a']]['y'] + N[s['b']]['y']) / 2)
F = []
def add(kind, where, what, why, prop, hours, step, ids, xy):
    air = AIR(*xy)
    F.append({'kind': kind, 'where': where, 'what': what, 'why': why, 'prop': prop if not air else 'השדה — ישן, ייבנה מחדש ב-S15 / S16 (D‑462) — נכנס לגיליון הדרישות שלו', 'hours': hours if not air else '—',
              'step': step if not air else 'שלב 8', 'ids': ids, 'x': round(xy[0]), 'y': round(xy[1]), 'air': air})
# 1) short streets doubling a nearby road
for i, s in enumerate(streets):
    if s['future'] or s['len'] >= 70 or s['cls'] != 'local': continue
    a = alt(i)
    if a is not None and a <= 1.6 * s['len'] + 60:
        x, y = mid(s); add('מיותר', chunk(x, y), '%s (%s, %.0f מ׳)' % (s['name'], ' + '.join(s['edges']), s['len']),
                           'קטע קצר: בין %s ל-%s יש דרך אחרת של %.0f מ׳ (פי %.1f)' % (N[s['a']]['label'] or s['a'], N[s['b']]['label'] or s['b'], a, a / max(1, s['len'])),
                           'לסגור את הקטע; התנועה עוברת בדרך הקרובה', '0.5', 'עם האזור שלו (שלב 11)', s['edges'], (x, y))
# 2) junctions too close along one street
for s in streets:
    if s['future']: continue
    if s['len'] < 45 and JUNC(s['a']) and JUNC(s['b']) and len(adj[s['a']]) >= 3 and len(adj[s['b']]) >= 3:
        x, y = mid(s); add('צמתים קרובים', chunk(x, y), '%s — %s ו-%s, %.0f מ׳ זה מזה' % (s['name'], N[s['a']]['label'] or s['a'], N[s['b']]['label'] or s['b'], s['len']),
                           'שני צמתים במרחק של פחות מ-45 מ׳: התור של אחד חוסם את השני, ושני רמזורים ברצף', 'לאחד לצומת אחד או להרחיק לפחות 60 מ׳', '1', 'עם האזור שלו (שלב 11)', s['edges'], (x, y))
# 3) sharp angles
for nid, es in adj.items():
    if len(es) < 3: continue
    vec = []
    for e in es:
        o = e['b'] if e['a'] == nid else e['a']; vec.append((math.atan2(N[o]['y'] - N[nid]['y'], N[o]['x'] - N[nid]['x']), e))
    vec.sort(key=lambda t: t[0])
    for k in range(len(vec)):
        a1, e1 = vec[k]; a2, e2 = vec[(k + 1) % len(vec)]
        d = (a2 - a1) % (2 * math.pi)
        if math.degrees(d) < 60:
            n = N[nid]; add('זווית חדה', chunk(n['x'], n['y']), '%s — %s / %s, %.0f°' % (n['label'] or nid, e1['name'], e2['name'], math.degrees(d)),
                             'פנייה בזווית של פחות מ-60°: רכב ארוך לא מסתובב, והראות בצומת חלקית', 'ליישר את אחד הרחובות לזווית של 75°–90° לפני הצומת', '1', 'עם האזור שלו (שלב 11)', [e1['id'], e2['id']], (n['x'], n['y']))
# 4) dead ends inside the city
for nid, es in adj.items():
    n = N[nid]
    if len(es) != 1 or es[0]['future']: continue
    edge = n['x'] <= 5 or n['y'] <= 5 or n['x'] >= W - 5 or n['y'] >= HH - 5
    if edge: continue
    if n['type'] == 'boundary' and '/' in (n['label'] or ''):   # the road runs on into an area that is not built yet — a continuation, not a dead end
        add('ממשיך לאזור שלא נבנה', chunk(n['x'], n['y']), '%s — %s' % (n['label'] or nid, es[0]['name']), 'הכביש נגמר בגבול של אזור שעוד לא נבנה', 'ממשיכים אותו כשהאזור נבנה; עד אז — סיום מסודר (כיכר קטנה או מחסום)', '0', 'עם האזור הסמוך', [es[0]['id']], (n['x'], n['y'])); continue
    add('מבוי סתום', chunk(n['x'], n['y']), '%s — סוף %s' % (n['label'] or nid, es[0]['name']), 'הרחוב נגמר באמצע העיר בלי מעגל תנועה או חניה בסופו', 'לחבר לרחוב סמוך או לסיים בכיכר / בחניון', '0.5', 'עם האזור שלו (שלב 11)', [es[0]['id']], (n['x'], n['y']))
# 5) flow: a local street crossing an arterial at a 4-way junction
for nid, es in adj.items():
    if len(es) < 4: continue
    cl = collections.Counter(e['cls'] for e in es)
    if cl['arterial'] >= 2 and cl['local'] >= 1:
        n = N[nid]; add('זרימה', chunk(n['x'], n['y']), '%s — רחוב מקומי חוצה עורק (%s)' % (n['label'] or nid, ', '.join(e['name'] for e in es if e['cls'] == 'local')),
                         'רחוב מקומי שחוצה עורק בצומת של ארבע זרועות מוסיף שלב רמזור לעורק ומכניס תנועה עוברת לשכונה', 'ימינה-ימינה בלבד מהרחוב המקומי, או חיבור דרך רחוב מאסף', '1', 'עם R-16 (שלב 13)', [e['id'] for e in es], (n['x'], n['y']))
# the owner's two examples (29.10 12:00)
ex = [s for s in streets if 'B3-RES-E' in s['edges']]
if ex:
    s = ex[0]; x, y = mid(s)
    F.insert(0, {'kind': 'מיותר — הדוגמה שלך', 'where': 'B3 / C3', 'what': 'רחוב הדיירים — B3 מזרח (B3-RES-E, %.0f מ׳ צפון–דרום, x 2250)' % s['len'],
                 'why': 'הרחוב הקצר שבין רחוב המגורים לעורק האמצעי, ממערב לשדרת המרכז — מכפיל את שדרת המרכז (260 מ׳ מזרחה)',
                 'prop': 'לסגור אותו; רחוב המגורים ממשיך ישר מזרחה עד שדרת המרכז, אל הצומת N1 (‏y 1800, ממשיך שם לרחוב הגנים) — צומת אחד של ארבע זרועות, ולא צומת חדש 5 מ׳ ממנו', 'hours': '1.5',
                 'step': 'עם C3 / B3 (שלב 11, צעד 14)', 'ids': ['B3-RES-E', 'B3-RES-NE'], 'x': round(x), 'y': round(y), 'air': False})
F.insert(1, {'kind': 'מיותר — הדוגמה שלך', 'where': 'B4', 'what': 'רחוב הגנים מזרח — הקטע שבין המרפאה לבית הספר (בשרטוט של B4)', 'why': 'בשרטוט החדש של B4 — לא במשחק של היום',
             'prop': 'נסגר בשרטוט של B4 (התשובה לשאלה הפתוחה); בית הספר והמרפאה ניגשים מרחוב הדירות', 'hours': '0 (בתוך B4)', 'step': 'B4 (צעד 6)', 'ids': [], 'x': 1900, 'y': 3100, 'air': False})
for i, f in enumerate(F, 1): f['n'] = i
out = {'streets': len(streets), 'findings': F, 'counts': dict(collections.Counter(f['kind'] for f in F)), 'air': sum(1 for f in F if f['air'])}
json.dump(out, open(os.path.join(H, 'roads_audit.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('streets', len(streets), 'findings', len(F), out['counts'], 'airport', out['air'])
for f in F: print(f['n'], f['kind'], f['where'], f['what'][:90], '|', f['why'][:60])
