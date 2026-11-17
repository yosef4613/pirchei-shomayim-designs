# -*- coding: utf-8 -*-
# fx_ret.py <world.json> <out.json> — fieldexit (D‑704 סעיף 1): היציאה המהירה בזווית (~30°) במחולל של fieldthru (ft_sim.py — כלל 19א, אותן רגליים).
# לכל סוג: זמן התפוסה של הנחיתה על המסלול (הכלל של המשחק — 074zv:ftOps: גובה < 40, ‏x בתוך המסלול ± 50, ‏y < ‏−480) ביציאות של היום (90°: A2 / A3 החדש / A4)
# מול יציאה מהירה (RET): מהקו האמצעי בקשת אל 30°, ישר ב-30°, וקשת אל 90° (דרומה) — נגמרת באותה נקודת מסירה כמו החיבור (x של החיבור, y ‏−280),
# וממנה ההסעה לעמדה של היום (arr1_taxi). מהירות היציאה מהמסלול 250 פיקס׳/ש׳ (25 מ׳/ש׳); ההאטה לפי הסוג (מרחק העצירה).
# אחר כך — הערכה על הלוח של היום (העולם): כל נחיתה באותו רגע נגיעה, ביציאה המהירה המתאימה; כמה המסלול תפוס, הפער הגדול. בלי בדיקת התנגשויות (השלב הבא).
import sys, os, json, math, io, contextlib
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
with contextlib.redirect_stdout(io.StringIO()):
    import ft_sim as F
M = F.M; T = F.T; RCY = F.RCY; TD = 5300.0; VTD = 700.0; VEX = 250.0
# ההאטה לפי הסוג (פיקס׳/ש׳²): קלים 110, בינוניים 82 (= הנחיתה של היום שיוצאת ב-A3 החדש), כבדים 64 (= היציאה של היום ב-A4)
LIGHT = {'AC-PR-01', 'AC-LT-01', 'AC-BJ-01', 'AC-CN-01', 'AC-TB-01', 'AC-AM-01', 'AC-TP-01'}
def dec_of(ac): return 64.0 if ac in F.HEAVY else (110.0 if ac in LIGHT else 82.0)
def ret_pts(xj, R1=600.0, R2=150.0, th=math.radians(30), yj=-280.0):
    # הצורה, מסוף ההסעה אחורה: (xj, yj) כיוון דרום; קשת R2 מ-90° אל 30°; ישר ב-30°; קשת R1 אל 0° על הקו האמצעי
    # קדימה: נקודת ההתחלה (x0, RCY); קשת R1 → 30°: dx1 = R1 sin30, dy1 = R1(1−cos30); קשת R2 30°→90°: dx2 = R2(1−sin30)... (מרכז הקשת מימין)
    dx1 = R1 * math.sin(th); dy1 = R1 * (1 - math.cos(th))
    dx2 = R2 * math.cos(th); dy2 = R2 * (1 - math.sin(th))      # מ-30° אל 90°: המרכז במרחק R2 בניצב
    ly = (yj - RCY) - dy1 - dy2; ls = ly / math.sin(th); dxs = ls * math.cos(th)
    x0 = xj - dx1 - dxs - dx2
    P = []
    for i in range(13):   # קשת 1
        a = th * i / 12; P.append([x0 + R1 * math.sin(a), RCY + R1 * (1 - math.cos(a))])
    xs, ys = P[-1]; xe, ye = xs + dxs, ys + ly; P.append([xe, ye])
    cx, cy = xe - R2 * math.sin(th), ye + R2 * math.cos(th)
    for i in range(1, 13):
        a = th + (math.pi / 2 - th) * i / 12; P.append([cx + R2 * math.sin(a), cy - R2 * math.cos(a)])
    return x0, P, ls
def arr_ret(sid, ac, xj):
    x0, P, ls = ret_pts(xj); d = dec_of(ac)
    need = (VTD ** 2 - VEX ** 2) / (2 * d)
    if x0 - TD < need: return None, None, x0, need
    L = M.D.ACT[ac][0]; a = M.Actor('x', 'ac', ac, sid, L, M.D.ACT[ac][1]); a.t = 0.0
    a.move([[-2400, RCY], [TD, RCY]], 720, VTD, z0=620, z1=0, flags=4); t_td = a.t
    vroll = math.sqrt(max(VEX ** 2, VTD ** 2 - 2 * d * (x0 - TD)))   # אם המקום רחוק מהמינימום — עוד גלגול מהיר עד הפתח (ההאטה של הסוג, לא יותר)
    xb = TD + (VTD ** 2 - VEX ** 2) / (2 * d)
    a.move([[TD, RCY], [xb, RCY]], VTD, VEX, flags=1)
    if x0 > xb + 1: a.move([[xb, RCY], [x0, RCY]], VEX, VEX, flags=1)
    n1 = 13; a.move(P[:n1], VEX, VEX, flags=1)          # הקשת אל 30° במהירות היציאה
    a.move(P[n1 - 1:n1 + 1], VEX, 60, flags=1)           # הישר — האטה אל מהירות הקשת
    a.move(P[n1:], 60, 70, flags=1)
    if sid is None: return a, t_td, x0, need
    a.legs[-1]['p'][-1] = [xj, -280.0]
    return F.arr1_taxi(a, sid, ac, t_td) + (x0, need)
def arr_90(sid, ac, ex):
    if ex == 'A4': return F.arr1_09(sid, ac, 'A3')   # A4 של D‑701 = ה-A3 של היום ב-ft_sim (x 9190)
    if ex == 'A3N':
        keep = F.A2; F.A2 = 8345
        try: return F.arr1_09(sid, ac, 'A2')
        finally: F.A2 = keep
    return F.arr1_09(sid, ac, ex)
def occ(a):
    W = F.rwy_wins_rel(a, 0, a.t); return round(sum(w[1] - w[0] for w in W), 2) if W else None
EXITS = {'A2': 7150.0, 'A3N': 8345.0, 'A4': 9190.0}
if __name__ == '__main__':
    W = json.load(open(sys.argv[1])); outp = sys.argv[2]
    res = dict(types={}, rets={}, world={})
    for nm, xj in EXITS.items():
        x0, P, ls = ret_pts(xj); res['rets']['RET-' + nm] = dict(x_start=round(x0), x_join=xj, straight=round(ls), cross480=round(next(p[0] for p in P if p[1] >= -480)))
    print('היציאות המהירות:', res['rets'], flush=True)
    TYPES = ['AC-PR-01', 'AC-LT-01', 'AC-BJ-01', 'AC-CN-01', 'AC-TB-01', 'AC-RJ-01', 'AC-QJ-01', 'AC-NB-01', 'AC-MW-01', 'AC-LG-01', 'AC-CG-01']
    for ac in TYPES:
        row = {}
        for ex in EXITS:
            a, _ = arr_90('P5' if ex != 'A3N' else 'P4', ac, ex)
            if a is not None: row['90-' + ex] = occ(a)
            r = arr_ret(None, ac, EXITS[ex])
            if r[0] is not None: row['RET-' + ex] = occ(r[0])
            else: row['RET-' + ex + '_why'] = 'צריך %d פיקס׳ עד 250 — יש %d' % (r[3], r[2] - TD)
        res['types'][ac] = row; print(ac, row, flush=True)
    # הלוח של היום: כל טיסה — חלונות המסלול; הנחיתה מוחלפת ביציאה המהירה המוקדמת ביותר שהסוג יכול (באותו רגע נגיעה)
    def wins_all(FL, repl):
        w = []
        for a in FL:
            for x in F.flight_rwy_wins(a):
                k = F.win_kind(a, x); d = x[1] - x[0]
                if k == 'a9' and a.id in repl: d = repl[a.id]
                w.append([x[0] % T, x[0] % T + d, a.id, k, a.model])
        return sorted(w)
    def stats(w):
        busy = sum(x[1] - x[0] for x in w); gaps = []
        for i, x in enumerate(w):
            nx = w[(i + 1) % len(w)]; gaps.append(round((nx[0] + (T if i + 1 == len(w) else 0)) - x[1], 1))
        return dict(n=len(w), busy_pct=round(busy / T * 100, 1), busy_s=round(busy, 1), max_gap=max(gaps), gaps_ge20=sum(1 for g in gaps if g >= 20), mean_gap=round(sum(gaps) / len(gaps), 1))
    FL = [F.actor(o) for o in W['flights']]; repl = {}; per = {}
    for a in FL:
        arrw = [x for x in F.flight_rwy_wins(a) if F.win_kind(a, x) == 'a9']
        if not arrw: continue
        cur = round(arrw[0][1] - arrw[0][0], 2); best = None
        for ex in ('A2', 'A3N', 'A4'):
            r = arr_ret(a.home, a.model, EXITS[ex])
            if r[0] is None: continue
            o = occ(r[0])
            if o is not None and (best is None or o < best[1]): best = (ex, o)
        per[a.id] = dict(model=a.model, today=cur, ret=best)
        if best and best[1] < cur: repl[a.id] = best[1]
    res['world']['per'] = per; res['world']['today'] = stats(wins_all(FL, {})); res['world']['ret'] = stats(wins_all(FL, repl))
    print(json.dumps(res['world'], ensure_ascii=False), flush=True)
    json.dump(res, open(outp, 'w'), ensure_ascii=False, indent=1)
