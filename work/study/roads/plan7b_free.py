# -*- coding: utf-8 -*-
"""1.11 round 6 (R-43): the fixed check of the map — in an urban zone no free parcel of 15 × 15 m or more is left without a use.
On a 1 m grid every cell of a zone is marked: a road (its band at the plan's section, the site roads and the driveways), a rail (a band
of 6 m per track), a lot or a site of any kind, the sea, the lake, the island's water. What is left is free; the free parcels of 15 × 15 m
and more are found one by one (the largest square first, then marked and searched again).
The zones checked: every land zone of the city except the forest, the park, the island, the airport and the row 0 strip at the edge of
the world (the review 11:50: there the free land is nature). Fields zones (C1, D1) are checked too — their free land must be a field."""
import math
import numpy as np
SKIP_TYPES = ('forest', 'park', 'island', 'air', 'sea')
def scan(out, zn, zrect, is_sea, in_lake, CLS, cell=10, minm=15):
    occ_rects, polys = [], []
    hw_of = lambda s: CLS[s['cls']]['halfW'] if s.get('cls') in CLS else 40
    for s in out['segments']:
        if s.get('kind') == 'bridge': continue
        p = s['pts']
        for a, b in zip(p, p[1:]): occ_rects.append((min(a[0], b[0]) - hw_of(s), min(a[1], b[1]) - hw_of(s), max(a[0], b[0]) + hw_of(s), max(a[1], b[1]) + hw_of(s)))
    for r in out.get('site_roads', []):
        p = r.get('pts') or []; hw = r.get('hw', 25)
        for a, b in zip(p, p[1:]): occ_rects.append((min(a[0], b[0]) - hw, min(a[1], b[1]) - hw, max(a[0], b[0]) + hw, max(a[1], b[1]) + hw))
    for r in out.get('rails', []):
        p = r.get('pts') or []; hw = 60 if r.get('kind') in ('main', 'east') else 35
        for a, b in zip(p, p[1:]): occ_rects.append((min(a[0], b[0]) - hw, min(a[1], b[1]) - hw, max(a[0], b[0]) + hw, max(a[1], b[1]) + hw))
    items = list(out.get('sites', [])) + list(out.get('lots', [])) + list(out['air'].get('lots', [])) + list(out['island'].get('lots', []))
    occ_rects += [tuple(r) for r in out.get('extra', [])]   # the bus terminal of E3 and the platforms of the stations (not lots, but taken)
    for i in items:
        r = i.get('rect')
        if i.get('kind') == 'pad' and i.get('c'): c, rr = i['c'], i.get('r', 100) + i.get('safety', 0); occ_rects.append((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr)); continue
        if i.get('kind') in ('path', 'site'):
            p = r or []; hw = i.get('hw', 15)
            if p and isinstance(p[0], (list, tuple)):
                for a, b in zip(p, p[1:]): occ_rects.append((min(a[0], b[0]) - hw, min(a[1], b[1]) - hw, max(a[0], b[0]) + hw, max(a[1], b[1]) + hw))
            continue
        if r and not isinstance(r[0], (list, tuple)): occ_rects.append(tuple(r))
        elif i.get('poly'): xs = [q[0] for q in i['poly']]; ys = [q[1] for q in i['poly']]; occ_rects.append((min(xs), min(ys), max(xs), max(ys)))
    res = {}
    for z, (nm, typ) in zn.items():
        if typ in SKIP_TYPES or z.endswith('0') and len(z) == 2: continue
        x0, y0, x1, y1 = zrect(z); W, H = int((x1 - x0) // cell), int((y1 - y0) // cell)
        free = np.ones((H, W), bool)
        for r in occ_rects:
            if r[2] <= x0 or r[0] >= x1 or r[3] <= y0 or r[1] >= y1: continue
            a0, b0 = max(0, int((r[0] - x0) // cell)), max(0, int((r[1] - y0) // cell)); a1, b1 = min(W, int(math.ceil((r[2] - x0) / cell))), min(H, int(math.ceil((r[3] - y0) / cell)))
            free[b0:b1, a0:a1] = False
        for j in range(H):
            for i_ in range(0, W, 3):
                x, y = x0 + (i_ + .5) * cell, y0 + (j + .5) * cell
                if free[j, i_] and (is_sea(x, y) or in_lake(x, y)): free[j, max(0, i_ - 1):i_ + 3] = False
        found = []
        while True:
            dp = np.zeros((H + 1, W + 1), int)
            for j in range(H):
                row = free[j]
                for i_ in range(W):
                    if row[i_]: dp[j + 1, i_ + 1] = 1 + min(dp[j, i_ + 1], dp[j + 1, i_], dp[j, i_])
            k = int(dp.max())
            if k * cell < minm * 10: break
            jj, ii = np.unravel_index(int(dp.argmax()), dp.shape)
            sq = (x0 + (ii - k) * cell, y0 + (jj - k) * cell, x0 + ii * cell, y0 + jj * cell)
            # grow it into the free rectangle it sits in (to report the real parcel)
            a0, b0, a1, b1 = ii - k, jj - k, ii, jj
            while a0 > 0 and free[b0:b1, a0 - 1].all(): a0 -= 1
            while a1 < W and free[b0:b1, a1].all(): a1 += 1
            while b0 > 0 and free[b0 - 1, a0:a1].all(): b0 -= 1
            while b1 < H and free[b1, a0:a1].all(): b1 += 1
            found.append(dict(rect=[x0 + a0 * cell, y0 + b0 * cell, x0 + a1 * cell, y0 + b1 * cell], m=[(a1 - a0), (b1 - b0)]))
            free[b0:b1, a0:a1] = False
            if len(found) > 12: break
        if found: res[z] = found
    return res
