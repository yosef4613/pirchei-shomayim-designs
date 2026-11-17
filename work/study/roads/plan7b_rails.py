# -*- coding: utf-8 -*-
"""1.11 (R-47, the review 11:50 / 12:55): the fixed check of the rail routes — for every working flow a continuous path on which every
switch is taken in the direction of travel, without a reversal.
A train runs along a track; where another track's end lies on it there is a switch — the train may take it only if the branch leaves in
its direction of travel (the angle between them under 35°). At the end of a track that joins another, it goes on along the other one in the
direction that continues its own (again under 35°); a buffer, a depot door or the edge of the world end the run. A flow may also forbid a
stretch (the freight to the airport does not pass the platforms of the central station — that is what the bypass is for)."""
import math
COS = math.cos(math.radians(35))

def _prep(rails):
    L = {}
    for r in rails:
        p = r['pts']; c = [0.0]
        for a, b in zip(p, p[1:]): c.append(c[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        L[r['id']] = dict(r=r, p=p, c=c, n=c[-1])
    return L

def _tan(T, s):
    p, c = T['p'], T['c']
    for k in range(len(p) - 1):
        if c[k] <= s <= c[k + 1] or k == len(p) - 2:
            dx, dy = p[k + 1][0] - p[k][0], p[k + 1][1] - p[k][1]; l = math.hypot(dx, dy) or 1
            return dx / l, dy / l

def _at(T, s):
    p, c = T['p'], T['c']
    for k in range(len(p) - 1):
        if c[k] <= s <= c[k + 1] or k == len(p) - 2:
            t = (s - c[k]) / ((c[k + 1] - c[k]) or 1); return p[k][0] + (p[k + 1][0] - p[k][0]) * t, p[k][1] + (p[k + 1][1] - p[k][1]) * t

def _locate(T, x, y, tol=3.0):
    best = None; p, c = T['p'], T['c']
    for k in range(len(p) - 1):
        ax, ay = p[k]; bx, by = p[k + 1]; dx, dy = bx - ax, by - ay; ll = dx * dx + dy * dy or 1
        t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / ll)); d = math.hypot(x - ax - t * dx, y - ay - t * dy)
        if d <= tol and (best is None or d < best[0]): best = (d, c[k] + t * math.sqrt(ll))
    return None if best is None else best[1]

def graph(rails):
    L = _prep(rails); att = {k: [] for k in L}
    for k, T in L.items():
        for e, (kind, *rest) in enumerate(T['r']['ends']):
            if kind != 'join': continue
            o = rest[0]
            if o not in L: continue
            x, y = T['p'][0] if e == 0 else T['p'][-1]
            s = _locate(L[o], x, y)
            if s is not None: att[o].append((s, k, e))
    return L, att

def run(L, att, start, goal, forbid=lambda line, x, y: False, limit=400):
    """BFS over (line, s, dir); start = (line, s, dir); goal(line, s, dir) → True. Returns the path (the lines in order) or None."""
    seen = set(); q = [(start, [start[0]])]
    while q and limit:
        limit -= 1; (ln, s, d), path = q.pop(0)
        if (ln, round(s), d) in seen: continue
        seen.add((ln, round(s), d)); T = L[ln]
        end = T['n'] if d > 0 else 0.0
        # the stretch from s towards the end in direction d — as far as it is allowed: the goal on it, the switches before the stop
        reach = abs(end - s); blocked = False
        for k in range(0, int(abs(end - s)) + 1, 10):
            ss = s + d * k; x, y = _at(T, ss)
            if forbid(ln, x, y): reach = max(0, k - 10); blocked = True; break
            if goal(ln, ss, d): return path
        nxt = []
        for (sa, o, e) in att[ln]:
            if (sa - s) * d <= 0.5 or abs(sa - s) > reach: continue
            tx, ty = _tan(T, sa); tx, ty = tx * d, ty * d
            O = L[o]; od = 1 if e == 0 else -1; ox, oy = _tan(O, 0.0 if e == 0 else O['n']); ox, oy = ox * od, oy * od
            if tx * ox + ty * oy >= COS: nxt.append(((o, 0.0 if e == 0 else O['n'], od), path + [o]))
        kind, *rest = T['r']['ends'][1 if d > 0 else 0]
        if not blocked and kind == 'join' and rest[0] in L:
            O = L[rest[0]]; x, y = T['p'][-1] if d > 0 else T['p'][0]; so = _locate(O, x, y)
            if so is not None:
                tx, ty = _tan(T, end); tx, ty = tx * d, ty * d; ox, oy = _tan(O, so)
                for od in (1, -1):
                    if tx * ox * od + ty * oy * od >= COS: nxt.append(((rest[0], so, od), path + [rest[0]]))
        q += nxt
    return None
