# -*- coding: utf-8 -*-
# ft2_p6big.py <world.json> <out.json> — fieldthru2 (הבעלים 17:35: "למה לא מנצלים לגדולים גם את P6"): הגדולים (LG / MW) ב-P6 ממריאים ב-27 מ-A4 (D‑701) —
# וזה דורש "פנוי לגמרי" (כל הבלוק בכיוון ההפוך + 10 ש׳ — ft2_sim / ft_sim.rwy_ok). בלוח של היום הפער הגדול ביותר במסלול — 34.5 ש׳, וזה לא מספיק.
# כאן — "חלון 27" בלו״ז, בלי שינוי גאומטריה: מזיזים טיסה אחת של הלוח (כולה — כל הרגליים והגרר שלה) בכמה שניות, כך שנפתח פער של ≥ 55 ש׳ במסלול,
# נבדק במדויק מול כל מה שרץ; ואז הגרסה הגדולה של P6 בחלון הזה — יוצאת מ-P6 אל A4 ומחכה בקו ההמתנה (aoHold) עד החלון.
import sys, os, json, math, time
os.environ.setdefault('FT_WMAX', '160'); os.environ['FT2_D701'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
import numpy as np
import ft_sim as F
import ft2_sim
import inspect as _ins
_src = _ins.getsource(F.tug_trip).replace("big = a.L > 600", "big = a.L > 600 or sid in ('P1', 'P6')"); exec(compile(_src, F.__file__, 'exec'), F.__dict__)
M = F.M; T = F.T
W = json.load(open(sys.argv[1])); outp = sys.argv[2]
FIX = set(os.environ.get('FT2_NOSHIFT', 'FL-P6,FL-GA1,FL-C2').split(','))
def wins(FL):
    w = []
    for a in FL:
        for x in F.flight_rwy_wins(a): w.append((x[0] % T, x[0] % T + (x[1] - x[0]), a.id, F.win_kind(a, x), a.model))
    return sorted(w)
def max_gap(w):
    best = (0, None)
    for i, x in enumerate(w):
        nx = w[(i + 1) % len(w)]; g = (nx[0] + (T if i + 1 == len(w) else 0)) - x[1]
        if g > best[0]: best = (g, x[1])
    return best
TUG = {}
for v in W['veh']:
    for g in v['legs']:
        if g.get('att'): TUG.setdefault(g['att'], []).append(v['id'])
def shift_legs(L, d): return [dict(g, t0=round(g['t0'] + d, 2), t1=round(g['t1'] + d, 2)) for g in L]
FL0 = [F.actor(o) for o in W['flights']]; print('הפער הגדול היום: %.1f ש׳ (אחרי %.1f)' % max_gap(wins(FL0)), flush=True)
Wd = F.World(W); F.world_cache(Wd)
cands = []
# שתי טיסות (FT2_PAIR=1): לכל זוג — הזזות בכמה שניות, כך שנפתח פער של ≥ FT2_GAP; קודם רק המסלול (מהיר), אחר כך במדויק
IDS = [o['id'] for o in W['flights'] if o['id'] not in FIX]; base_w = {a.id: [(x[0] % T, x[0] % T + (x[1] - x[0]), a.id, F.win_kind(a, x), a.model) for x in F.flight_rwy_wins(a)] for a in FL0}
def gap_with(sh):
    w = []
    for fid, L in base_w.items():
        d = sh.get(fid, 0); w += [((x0 + d) % T, (x0 + d) % T + (x1 - x0), i, k, m) for x0, x1, i, k, m in L]
    return max_gap(sorted(w)), sorted(w)
def rwy_clean(w):
    for i in range(len(w)):
        for j in range(len(w)):
            if i == j: continue
            a, b = w[i], w[j]
            for k in (-T, 0, T):
                b0 = b[0] + k
                if a[0] <= b0 < a[1] + 3 + (8 if a[4] in F.HEAVY else 0): return False
    return True
D = [x for k in range(1, 21) for x in (2 * k, -2 * k)]
GAP = float(os.environ.get('FT2_GAP', 58))
if os.environ.get('FT2_PAIR'):
    for i, f1 in enumerate(IDS):
        for f2 in IDS[i + 1:]:
            for d1 in D:
                for d2 in D:
                    (g, at), w = gap_with({f1: d1, f2: d2})
                    if g >= GAP and rwy_clean(w): cands.append((abs(d1) + abs(d2), (f1, d1), (f2, d2), g, at))
    cands.sort(); print('זוגות מועמדים:', [(c[1], c[2], round(c[3], 1)) for c in cands[:10]], len(cands), flush=True)
res = dict(shift=None, pairs=[(c[1], c[2], round(c[3], 1)) for c in cands[:20]])
for _, fid, d, g, at in ([] if os.environ.get('FT2_PAIR') else cands[:8]):
    o = next(x for x in W['flights'] if x['id'] == fid); a = F.actor(dict(o, legs=shift_legs(o['legs'], d)))
    h = F.exact_flight(Wd, a, m=.5, skip_ids={fid} | set(TUG.get(fid, [])), vkv=1.0)
    if h: print(fid, d, '— נוגע ב-', h[1], h[0]); continue
    # הגררים של הטיסה — אותה הזזה; מול הרכבים (exact, 0.5 ש׳)
    okv = True
    for vid in TUG.get(fid, []):
        v = next(x for x in W['veh'] if x['id'] == vid); trs = F.base_trips(v)
        trs2 = [shift_legs(tr, d) if any(gg.get('att') == fid for gg in tr) else tr for tr in trs]
        z = F.veh_from_trips(vid, v['model'], v['home'], v['L'], v['W'], v['legs'][-1]['p'][0], v['legs'][-1].get('h', F.S_), trs2)
        VH = [F.actor(x) for x in W['veh'] if x['id'] != vid]
        hit = None
        for k in range(int(T / .5)):
            t = k * .5; q = M.evalp(z, t)
            if not q or q[4] in (0, 16): continue
            for y in VH:
                r = M.evalp(y, t)
                if r and r[4] != 16 and abs(r[0] - q[0]) < 200 and abs(r[1] - q[1]) < 200 and M.obb_hit(F.boxes_of(z, q)[0], F.boxes_of(y, r)[0]): hit = (y.id, t); break
            if hit: break
        if hit: print(fid, d, '— הגרר', vid, 'נוגע ב-', hit); okv = False; break
    if not okv: continue
    res['shift'] = dict(fid=fid, d=d, gap=round(g, 1), at=round(at, 1)); print('הזזה:', res['shift'], flush=True); break
json.dump(res, open(outp, 'w'), ensure_ascii=False)
