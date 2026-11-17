# rails 17.11 — מדידת כל הפיצולים, ההשתלבויות, הצמתים בלי מסוט והחפיפות ברשת המסילות (מתוך net_*.json של rail_extract.js)
# שימוש: python3 rail_measure.py <net.json> <out.json>
import json, math, sys
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]
S = {g['id']: g for g in R['segs']}; N = {n['id']: n for n in R['nodes']}
GAUGE, BED, TIE, SEP = 26.0, 44.0, 38.0, 38.0
def L(a, b): return math.hypot(b[0]-a[0], b[1]-a[1])
def resample(P, step=2.0):
    out = [tuple(P[0])]
    for i in range(1, len(P)):
        a, b = P[i-1], P[i]; d = L(a, b); k = max(1, int(d // step))
        for j in range(1, k+1): t = j/k; out.append((a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t))
    return out
def heading(P, i):
    a = P[max(0, i-1)]; b = P[min(len(P)-1, i+1)]; return math.atan2(b[1]-a[1], b[0]-a[0])
def dang(a, b):
    d = abs(a-b) % (2*math.pi); return min(d, 2*math.pi-d)
def dist_poly(p, P):
    best = (1e9, 0, 0)
    for i in range(len(P)-1):
        ax, ay = P[i]; bx, by = P[i+1]; dx, dy = bx-ax, by-ay; l2 = dx*dx+dy*dy or 1
        t = max(0, min(1, ((p[0]-ax)*dx+(p[1]-ay)*dy)/l2)); d = math.hypot(p[0]-ax-t*dx, p[1]-ay-t*dy)
        if d < best[0]: best = (d, i, t)
    return best
def radius3(a, b, c):
    ab, bc, ca = L(a, b), L(b, c), L(c, a); ar = abs((b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]))/2
    return 1e9 if ar < 1e-6 else ab*bc*ca/(4*ar)
def min_radius(P, upto=None):
    # רדיוס מינימלי לאורך הקו (על דגימה כל 6 פיקס׳, משולש של 3 נקודות במרווח 12) — עד upto פיקס׳ מההתחלה
    Q = resample(P, 2.0); acc = [0]
    for i in range(1, len(Q)): acc.append(acc[-1]+L(Q[i-1], Q[i]))
    m = 1e9
    for i in range(6, len(Q)-6, 3):
        if upto and acc[i] > upto: break
        m = min(m, radius3(Q[i-6], Q[i], Q[i+6]))
    return m
# ---- ends at each node (direction pointing away from the node)
ends = {}
def add_end(node, seg, pts):
    ends.setdefault(node, []).append({'seg': seg, 'pts': pts, 'h': math.atan2(pts[1][1]-pts[0][1], pts[1][0]-pts[0][0])})
for g in R['segs']:
    P = [tuple(p) for p in g['pts']]
    add_end(g['from'], g['id'], resample(P))
    add_end(g['to'], g['id'], resample(P[::-1]))
# mid-segment joins: a node of degree 1 lying on the interior of another segment
for nid, E in list(ends.items()):
    n = N.get(nid); 
    if not n or len(E) != 1: continue
    for g in R['segs']:
        if g['id'] == E[0]['seg'] or g['from'] == nid or g['to'] == nid: continue
        d, i, t = dist_poly((n['x'], n['y']), g['pts'])
        if d < 0.6:
            P = [tuple(p) for p in g['pts']]; cut = (n['x'], n['y'])
            add_end(nid, g['id']+'(→)', resample([cut]+P[i+1:]))
            add_end(nid, g['id']+'(←)', resample([cut]+P[:i+1][::-1]))
            n['mid'] = g['id']
def follow(seg_pts, max_len=900):
    return seg_pts  # (המשך לקטעים הבאים — מספיק לרוב; הקטעים קצרים מסומנים)
def chain(nid, end, max_len=900):
    # ממשיכים את הקו מעבר לצומת הבא בכיוון הישר ביותר, עד max_len
    pts = list(end['pts']); total = sum(L(pts[i-1], pts[i]) for i in range(1, len(pts)))
    seen = {end['seg']}; cur = end
    while total < max_len:
        last = pts[-1]; h = math.atan2(pts[-1][1]-pts[-2][1], pts[-1][0]-pts[-2][0])
        nxt = None
        for k, E in ends.items():
            n = N.get(k)
            if not n or L((n['x'], n['y']), last) > 0.8: continue
            cand = [e for e in E if e['seg'].split('(')[0] not in seen]
            if not cand: break
            nxt = min(cand, key=lambda e: dang(e['h'], h))
            if dang(nxt['h'], h) > 0.35: nxt = None
            break
        if not nxt: break
        seen.add(nxt['seg'].split('(')[0]); pts += nxt['pts'][1:]; total += sum(L(nxt['pts'][i-1], nxt['pts'][i]) for i in range(1, len(nxt['pts'])))
    return pts
J = []
for nid, E in ends.items():
    if len(E) < 3: continue
    n = N[nid]
    # the through pair: the two ends most opposite
    best = None
    for i in range(len(E)):
        for j in range(i+1, len(E)):
            d = dang(E[i]['h'], E[j]['h']+math.pi)
            if best is None or d < best[0]: best = (d, i, j)
    _, i, j = best; thr = [E[i], E[j]]
    for k, e in enumerate(E):
        if k in (i, j): continue
        par = min(thr, key=lambda t: dang(t['h'], e['h']))
        D = chain(nid, e, 900); Pm = chain(nid, par, 1200)
        acc = 0; s26 = s38 = s44 = None; f_ang = None; prev = D[0]
        for q in range(1, len(D)):
            acc += L(D[q-1], D[q]); d, ii, t = dist_poly(D[q], Pm)
            if s26 is None and d >= GAUGE:
                s26 = acc; hd = math.atan2(D[q][1]-D[q-1][1], D[q][0]-D[q-1][0]); a, b = Pm[ii], Pm[ii+1]; f_ang = math.degrees(dang(hd, math.atan2(b[1]-a[1], b[0]-a[0])))
            if s38 is None and d >= SEP: s38 = acc
            if s44 is None and d >= BED: s44 = acc; break
        toe = math.degrees(dang(e['h'], par['h']))
        rmin = min_radius(D, (s44 or 300)+60)
        J.append({'node': nid, 'x': round(n['x'], 1), 'y': round(n['y'], 1), 'type': n.get('type'), 'mid': n.get('mid'), 'main': [thr[0]['seg'], thr[1]['seg']], 'parent': par['seg'], 'div': e['seg'],
                  'toe_deg': round(toe, 1), 'frog_deg': round(f_ang, 1) if f_ang is not None else None, 'frog_at': round(s26, 1) if s26 else None, 'sep38_at': round(s38, 1) if s38 else None, 'sep44_at': round(s44, 1) if s44 else None,
                  'rmin_px': round(rmin, 1)})
# ---- crossings without a node (diamonds) and overlaps
def seg_inter(a, b, c, d):
    r = (b[0]-a[0], b[1]-a[1]); s = (d[0]-c[0], d[1]-c[1]); den = r[0]*s[1]-r[1]*s[0]
    if abs(den) < 1e-9: return None
    t = ((c[0]-a[0])*s[1]-(c[1]-a[1])*s[0])/den; u = ((c[0]-a[0])*r[1]-(c[1]-a[1])*r[0])/den
    if 0 <= t <= 1 and 0 <= u <= 1: return (a[0]+t*r[0], a[1]+t*r[1], math.atan2(r[1], r[0]), math.atan2(s[1], s[0]))
    return None
X = []; segs = R['segs']
nodexy = [(n['x'], n['y']) for n in R['nodes']]
for ia in range(len(segs)):
    for ib in range(ia+1, len(segs)):
        A, B = segs[ia]['pts'], segs[ib]['pts']
        for i in range(len(A)-1):
            for j in range(len(B)-1):
                r = seg_inter(A[i], A[i+1], B[j], B[j+1])
                if not r: continue
                if min(L((r[0], r[1]), q) for q in nodexy) < 3: continue
                ang = math.degrees(dang(r[2], r[3])); ang = min(ang, 180-ang)
                X.append({'a': segs[ia]['id'], 'b': segs[ib]['id'], 'x': round(r[0], 1), 'y': round(r[1], 1), 'angle_deg': round(ang, 1)})
# proximity (beds overlapping) between segments that do not share a node, sampled every 8 px
PX = []
for ia in range(len(segs)):
    A = resample(segs[ia]['pts'], 8)
    for ib in range(ia+1, len(segs)):
        ga, gb = segs[ia], segs[ib]
        if {ga['from'], ga['to']} & {gb['from'], gb['to']}: continue
        B = gb['pts']; bx0 = min(p[0] for p in B)-50; bx1 = max(p[0] for p in B)+50; by0 = min(p[1] for p in B)-50; by1 = max(p[1] for p in B)+50
        run = None
        for p in A:
            if not (bx0 < p[0] < bx1 and by0 < p[1] < by1): d = 1e9
            else: d = dist_poly(p, B)[0]
            if d < BED and d > 0.5:
                if run is None: run = [p, p, d, d]
                else: run[1] = p; run[2] = min(run[2], d); run[3] = max(run[3], d)
            elif run is not None:
                PX.append({'a': ga['id'], 'b': gb['id'], 'from': [round(run[0][0]), round(run[0][1])], 'to': [round(run[1][0]), round(run[1][1])], 'len': round(L(run[0], run[1])), 'dmin': round(run[2], 1), 'dmax': round(run[3], 1)}); run = None
        if run is not None: PX.append({'a': ga['id'], 'b': gb['id'], 'from': [round(run[0][0]), round(run[0][1])], 'to': [round(run[1][0]), round(run[1][1])], 'len': round(L(run[0], run[1])), 'dmin': round(run[2], 1), 'dmax': round(run[3], 1)})
segR = {g['id']: round(min_radius(g['pts']), 1) for g in segs if len(g['pts']) > 2}
json.dump({'junctions': J, 'crossings': X, 'proximity': PX, 'seg_rmin': segR}, open(OUT, 'w'), ensure_ascii=False, indent=0)
print('junctions', len(J), 'crossings', len(X), 'proximity', len(PX))
for j in sorted(J, key=lambda j: j['rmin_px']): print(j['node'], j['x'], j['y'], 'div', j['div'], 'par', j['parent'], 'toe', j['toe_deg'], 'frog', j['frog_deg'], '@', j['frog_at'], 'sep44@', j['sep44_at'], 'Rmin', j['rmin_px'])
print('--- crossings'); [print(x) for x in X]
print('--- proximity'); [print(p) for p in PX if p['len'] > 0]
print('--- seg rmin'); print(segR)
