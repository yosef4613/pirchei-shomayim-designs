# -*- coding: utf-8 -*-
# ft_sim.py — fieldthru 17.11: המחולל של לוח הטיסות של S15SIM — עוד טיסות מעל הלוח הקיים (כלל 19א: אותו מחולל s15_sim.py — departure / takeoff /
# arrival / tug / boxes — ואותו כלל מסלול של fieldcalc, שגובר). מה חדש כאן — רק החיפוש:
#   (1) המכשולים — כל מה שרץ במשחק (dump_sim.js: הטיסות, כל הרכבים אחרי כל העטיפות, החונים, המסוק, הגרירות של R3) — כרסטר של תאים בזמן (מרחב־זמן,
#       כמו טבלת השמירה של המתכנן הישן AO), כדי לבדוק את כל הזמנים האפשריים של טיסה בבת אחת;
#   (2) הטיסה מחולקת לתבניות (דחיפה + הסעה עד קו ההמתנה · המתנה בקו ההמתנה · כניסה והמראה · נחיתה + הסעה לעמדה · עמידה) — כל תבנית נבדקת בכל
#       ההזזות בזמן, וההרכבה בוחרת זמן דחיפה, המתנה בקו ההמתנה (התור למסלול), זמן נחיתה ועמידה ≥ המינימום של הסוג (מטריצת השירות של fieldcalc);
#   (3) הגרר של הטיסה (s15_sim.tug) — נבדק באותו רסטר; אם נוגע — זמן אחר.
# בסוף — בדיקה מדויקת (OBB של s15_sim / s15SimAudit, כל 0.5 ש׳) של הכול מול הכול, והמרווחים במסלול (fieldcalc). קוד יציאה 1 בכישלון.
# שימוש: python3 ft_sim.py <dump.json> <out.json> [סדר העמדות, בפסיקים]
import sys, os, json, math, io, contextlib, types
import numpy as np
S15T = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-10/s15/tools'
sys.path.insert(0, S15T)
src = open(os.path.join(S15T, 's15_sim.py'), encoding='utf-8').read()
src = src[:src.index('ST = static_actors()\nschedule()')]
src = src.replace("via_c=sid in ('R2', 'GA6')", "via_c=sid.startswith(('R', 'GA'))").replace("remote=True if sid in ('R2', 'GA6') else None", "remote=True if sid.startswith(('R', 'GA')) else None")
M = types.ModuleType('ft_s15'); M.__file__ = os.path.join(S15T, 's15_sim.py')
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, M.__file__, 'exec'), M.__dict__)
D = M.D; T = M.T
for _m, _v in (('AC-MW-01', .1), ('AC-QJ-01', .12), ('AC-AM-01', .2), ('AC-HC-01', .1)): M.NGF.setdefault(_m, _v)   # סוגים שלא היו ב-s15_sim (המגוון — הבעלים 12:40)
HEAVY = {'AC-LG-01', 'AC-MW-01', 'AC-CG-01', 'AC-HC-01'}
RWY = [5000, -810, 9300, -570]
# זמן העמידה המינימלי (מטריצת השירות של fieldcalc — fc_calc.py: צר 400, ‏LG 470, ‏CG 440, אזורי 340, מנהלים 240–260, קלים 170–180)
# fieldthru (לאישורך): בהסעה של היום הדחיפה מ-P1 / P6 לבדה ~70 ש׳, ולכן 470 של LG לא נכנס במחזור של 720 — 400 (הטיסות של היום עומדות 311–420)
MINPARK = {'AC-NB-01': 330, 'AC-LG-01': 360, 'AC-CG-01': 340, 'AC-RJ-01': 300, 'AC-BJ-01': 240, 'AC-CN-01': 240, 'AC-LT-01': 150, 'AC-PR-01': 150, 'AC-TB-01': 340, 'AC-TP-01': 300}
DT = 1.0; N = int(T / DT)
# ---------------------------------------------------------------- הרסטר: תאים של 16 פיקס׳ בכל השדה
CS = 16.0; X0, Y0, X1, Y1 = 4600.0, -950.0, 9800.0, 2700.0
NX = int((X1 - X0) / CS); NY = int((Y1 - Y0) / CS); NC = NX * NY
CX = X0 + (np.arange(NX) + .5) * CS; CY = Y0 + (np.arange(NY) + .5) * CS
MARGIN_AC = 4.0     # מרווח בין מטוס למכשול (פיקס׳; 10 פיקס׳ = מטר) — מעבר לחצי התא של הרסטר
VK = 1.06           # הרכב המצויר קצת גדול מהקופסה של הסימולציה; הבדיקה המדויקת בסוף — בקופסה של s15SimAudit
def obb_cells(b, m):
    cx, cy, h, hl, hw = b; hl += m + CS * .5; hw += m + CS * .5
    c, s = math.cos(h), math.sin(h); ex = abs(hl * c) + abs(hw * s); ey = abs(hl * s) + abs(hw * c)
    i0 = max(0, int((cx - ex - X0) / CS)); i1 = min(NX - 1, int((cx + ex - X0) / CS)); j0 = max(0, int((cy - ey - Y0) / CS)); j1 = min(NY - 1, int((cy + ey - Y0) / CS))
    if i1 < i0 or j1 < j0: return np.zeros(0, dtype=np.int64)
    gx, gy = np.meshgrid(CX[i0:i1 + 1] - cx, CY[j0:j1 + 1] - cy, indexing='ij')
    u = gx * c + gy * s; v = -gx * s + gy * c
    k = (np.abs(u) <= hl) & (np.abs(v) <= hw)
    ii, jj = np.nonzero(k)
    return ((ii + i0) * NY + (jj + j0)).astype(np.int64)
def actor(o):
    a = M.Actor(o['id'], o['kind'], o['model'], o['home'], o['L'], o['W']); a.legs = o['legs']
    if o.get('airline'): a.airline = o['airline']
    return a
def ser(a):
    d = dict(id=a.id, kind=a.kind, model=a.model, home=a.home, L=a.L, W=a.W, legs=a.legs)
    if getattr(a, 'airline', None): d['airline'] = a.airline
    if a.kind == 'ac':
        W_ = [g for g in a.legs if g.get('h') is not None and g.get('f', 1) == 0]
        if W_: g = max(W_, key=lambda g: g['t1'] - g['t0']); d['park'] = [round(g['t0'], 3), round(g['t1'], 3)]
    return d
def boxes_of(a, P, vk=1.0):
    if a.kind == 'veh':
        x, y, h, z, f = P; return [(x, y, h, a.L / 2 * vk, a.W / 2 * vk)]
    return M.boxes(a, P)
# ---------------------------------------------------------------- המכשולים
class Occ:
    def __init__(s): s.o = np.zeros((N, NC), dtype=np.uint8)
    def add_actor(s, a, skip=lambda P: False, vk=1.0, m=0.0):
        # כל משבצת זמן מכסה את כל מה שהשחקן עובר בה (4 דגימות בשנייה) — גם מטוס בריצה על המסלול (300 פיקס׳ בשנייה) לא "קופץ" מעל מכשול
        for i in range(N):
            for sub in (0.0, .25, .5, .75):
                P = M.evalp(a, i * DT + sub * DT)
                if not P or skip(P): continue
                if sub and a.kind == 'veh': break
                for b in boxes_of(a, P, vk):
                    c = obb_cells(b, m); s.o[i, c] = 1
    def add_static(s, b, m=0.0, t0=0, t1=T):
        c = obb_cells(b, m)
        for i in range(int(t0 / DT), int(t1 / DT)): s.o[i % N, c] = 1
def template(a, t0, t1, vk=1.0):
    # התבנית: לכל דגימה (יחסית ל-t0) — התאים שהשחקן מכסה
    I = []; C = []
    n = int(round((t1 - t0) / DT))
    for k in range(n + 1):
        for sub in (0.0, .25, .5, .75):
            P = M.pose(a, t0 + (k + sub) * DT)
            if not P: continue
            for b in boxes_of(a, P, vk):
                c = obb_cells(b, MARGIN_AC); I.append(np.full(len(c), k, dtype=np.int64)); C.append(c)
    if not I: return (np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.int64), n)
    return (np.concatenate(I), np.concatenate(C), n)
def shifts_conflict(occ, tpl, base_t):
    # לכל הזזה s (0..N-1, בשניות): כמה תאים חופפים כשהתבנית מתחילה ב-(base_t + s)
    I, C, n = tpl
    if not len(I): return np.zeros(N, dtype=np.int64)
    out = np.zeros(N, dtype=np.int64); i0 = int(round(base_t / DT))
    for s in range(N):
        out[s] = occ.o[(i0 + s + I) % N, C].sum()
    return out
def rwy_wins_rel(a, t0, t1):
    # הכלל של fieldcalc: "תפוס" רק על המסלול (x בתוך הקצוות ± 50, צפונית לקו ההמתנה) ונמוך מ-40 — דגימה כל 0.25 ש׳
    W = []; cur = None; t = t0
    while t <= t1 + 1e-6:
        P = M.pose(a, t); on = bool(P) and P[3] < 40 and RWY[0] - 50 <= P[0] <= RWY[2] + 50 and P[1] < M.HOLD - 10
        if on and cur is None: cur = [t, t]
        elif on: cur[1] = t
        elif cur is not None: W.append(cur); cur = None
        t += .25
    if cur: W.append(cur)
    return W
# AIR-09 (התוכנית ששמרנו): המסלול 09/27 משני הכיוונים בתיאום המגדל — המסלול נשאר משאב אחד; כיוון הפוך מקבל את כל הבלוק (הגישה מקצה העולם / הטיפוס
# עד קצה העולם) ועוד 10 ש׳ — "החלפת כיוון מבוקרת"; באותו כיוון — הכלל של fieldcalc (3 ש׳ + 8 אחרי כבד)
DIR_PRE = {'a9': 8.0, 'a27': 1.5, 'd9': 0.0, 'd27': 0.0}; DIR_POST = {'a9': 0.0, 'a27': 0.0, 'd9': 4.0, 'd27': 10.0}; DIR_GAP = 10.0
def rwy_ok(w, model, busy, gap=3, kd=None):
    for e in busy:
        x0, x1, m1 = e[0], e[1], e[2]; k1 = e[3] if len(e) > 3 else None
        for k in (-T, 0, T):
            if kd and k1 and kd[1:] != k1[1:]:
                a0 = w[0] - DIR_PRE[kd]; a1 = w[1] + DIR_POST[kd]; b0 = x0 + k - DIR_PRE[k1]; b1 = x1 + k + DIR_POST[k1]
                if not (a0 >= b1 + DIR_GAP or b0 >= a1 + DIR_GAP): return False
            elif not (w[0] >= x1 + k + gap + (8 if m1 in HEAVY else 0) or x0 + k >= w[1] + gap + (8 if model in HEAVY else 0)): return False
    return True
def win_kind(a, w):
    P0 = M.evalp(a, w[0] % T); P1 = M.evalp(a, (w[1] + .5) % T)
    if not P0 or not P1: return 'a9'
    east = P1[0] >= P0[0]; dep = P1[3] > 0.5
    return ('d' if dep else 'a') + ('9' if east else '27')
def flight_rwy_wins(a):
    W = []; cur = None; t = -T
    for g in a.legs:
        pass
    t = 0.0
    while t < T:
        P = M.evalp(a, t); on = bool(P) and P[3] < 40 and RWY[0] - 50 <= P[0] <= RWY[2] + 50 and P[1] < M.HOLD - 10
        if on and cur is None: cur = [t, t]
        elif on: cur[1] = t
        elif cur is not None: W.append(cur); cur = None
        t += .25
    if cur: W.append(cur)
    # חלון שחוצה את סוף המחזור — מתחבר
    if len(W) > 1 and W[0][0] < .3 and W[-1][1] > T - .3: W[0] = [W[-1][0] - T, W[0][1]]; W.pop()
    return [[w[0], w[1], a.model] for w in W]
# ---------------------------------------------------------------- פרופיל מהירות להסעה (במקום האטה אחת לאורך כל הדרך — "קפוא"; הבעלים, הביקורת סעיף 14):
# האצה עד vmax בקטעים הישרים, vturn בקשתות, האטה לפני העצירה / הפנייה — רגליים בתאוצה קבועה (אותה צורה של רגל כמו s15_sim: v0 → v1 לינארי בזמן)
# מהישן (042_core.js: APTT_CLS.vTaxi, ‏apttTaxi — acc 20 / dec 22, הקשתות 34; בפיקסלים של הישן, 7.47 למטר) → פיקסלים של S15 (10 למטר): × 10 / 7.47
OLDK = 10 / 7.47
TAXI_BY = {k: round(v * OLDK, 1) for k, v in {'AC-NB-01': 60, 'AC-RJ-01': 58, 'AC-TP-01': 52, 'AC-CG-01': 52, 'AC-PR-01': 46, 'AC-BJ-01': 52, 'AC-LG-01': 46, 'AC-QJ-01': 56, 'AC-MW-01': 50, 'AC-LT-01': 46, 'AC-CN-01': 50, 'AC-TB-01': 48}.items()}
TAXI_V = 80.0; TURN_V = round(34 * OLDK, 1); ACC = round(20 * OLDK, 1); DEC = round(22 * OLDK, 1)
def prof_legs(P, vmax, vs, ve, vturn=TURN_V, acc=ACC, dec=DEC):
    n = len(P); S = [0.0]
    for i in range(1, n): S.append(S[-1] + math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]))
    cap = [vmax] * n; arc = [False] * n
    for i in range(1, n - 1):
        a = math.atan2(P[i][1] - P[i - 1][1], P[i][0] - P[i - 1][0]); b = math.atan2(P[i + 1][1] - P[i][1], P[i + 1][0] - P[i][0])
        d = abs(math.atan2(math.sin(b - a), math.cos(b - a)))
        if d > .02: cap[i] = min(cap[i], vturn); arc[i] = True
    # הקשת: גם הנקודה שלפני הראשונה ושאחרי האחרונה (הכניסה והיציאה מהקשת) — באותה מהירות
    for i in range(1, n - 1):
        if arc[i]:
            if not arc[i - 1]: cap[i - 1] = min(cap[i - 1], vturn)
            if i + 1 < n and not arc[i + 1]: cap[i + 1] = min(cap[i + 1], vturn)
    seg_arc = [arc[i] and arc[i + 1] for i in range(n - 1)]
    cap[0] = min(cap[0], vs); cap[-1] = min(cap[-1], ve)
    v = cap[:]
    for i in range(1, n): v[i] = min(v[i], math.sqrt(v[i - 1] ** 2 + 2 * acc * (S[i] - S[i - 1])))
    for i in range(n - 2, -1, -1): v[i] = min(v[i], math.sqrt(v[i + 1] ** 2 + 2 * dec * (S[i + 1] - S[i])))
    pcs = []
    def at(i, x):
        l = S[i + 1] - S[i]; f = x / l if l > 0 else 0
        return [P[i][0] + (P[i + 1][0] - P[i][0]) * f, P[i][1] + (P[i + 1][1] - P[i][1]) * f]
    for i in range(n - 1):
        l = S[i + 1] - S[i]
        if l < 1e-6: continue
        a0, b0 = v[i], v[i + 1]; m = max(a0, b0, vturn if seg_arc[i] else vmax)
        x1 = max(0.0, (m * m - a0 * a0) / (2 * acc)); x2 = l - max(0.0, (m * m - b0 * b0) / (2 * dec)); br = []
        if x1 < x2:
            if x1 > .5: br.append((x1, m))
            if x2 < l - .5: br.append((x2, m))
        else:
            x = max(0.0, min(l, (b0 * b0 - a0 * a0 + 2 * dec * l) / (2 * (acc + dec)))); vp = math.sqrt(max(0.0, a0 * a0 + 2 * acc * x))
            if .5 < x < l - .5: br.append((x, max(a0, b0, vp)))
        px, pv, pp = 0.0, a0, P[i]
        for x, vv in br + [(l, b0)]:
            q = P[i + 1] if x >= l else at(i, x); pcs.append(dict(a=pp, b=q, v0=pv, v1=vv, l=x - px)); px, pv, pp = x, vv, q
    out = []
    for q in pcs:
        if q['l'] < 1e-6: continue
        ac = (q['v1'] ** 2 - q['v0'] ** 2) / (2 * q['l']); o = out[-1] if out else None
        if o and abs(o['acc'] - ac) < max(.4, abs(ac) * .04) and abs(o['v1'] - q['v0']) < .05: o['p'].append(q['b']); o['v1'] = q['v1']; o['l'] += q['l']
        else: out.append(dict(p=[q['a'], q['b']], v0=q['v0'], v1=q['v1'], l=q['l'], acc=ac))
    for o in out: o['v0'] = max(.5, o['v0']); o['v1'] = max(.5, o['v1'])
    return out
def pmove(a, P, vmax, vs, ve, flags=1, vturn=TURN_V, rev=False, acc=ACC, dec=DEC):
    for o in prof_legs(P, vmax, vs, ve, vturn, acc, dec): a.move(o['p'], round(o['v0'], 2), round(o['v1'], 2), rev=rev, flags=flags)
# הדחיפה של הישן (042: apttPush — vPush של הסוג, האצה / האטה 6, מהירות התחלה וסוף 3; בפיקסלים של הישן) — במקום 16 → 9.6 לאורך 900 פיקס׳ (75 ש׳ שבהן A חסום)
PUSH_BY = {k: round(v * OLDK, 1) for k, v in {'AC-NB-01': 17, 'AC-RJ-01': 17, 'AC-TP-01': 17, 'AC-CG-01': 15, 'AC-PR-01': 14, 'AC-BJ-01': 15, 'AC-LG-01': 13, 'AC-QJ-01': 16, 'AC-MW-01': 14, 'AC-LT-01': 14, 'AC-CN-01': 15, 'AC-TB-01': 16}.items()}
def push_move(a, P, ac):
    v = PUSH_BY.get(ac, 20.0); pmove(a, P, v, 4.0, 4.0, flags=2, vturn=v, rev=True, acc=6 * OLDK, dec=6 * OLDK)
E_, S_, W_, N_ = M.E_, M.S_, M.W_, M.N_
TACY, TCCY, TBCX, RCY, A1, A3 = M.TACY, M.TCCY, M.TBCX, M.RCY, M.A1, M.A3
def south(sid): return sid.startswith(('R', 'GA'))
A2 = 7150
# הישן (044: AO_ROLL — "line-up at a mid-field link: roll needed (px)", בפיקסלים של הישן): מי שיכול להמריא מ-A2 (נשארים 2150 פיקס׳ עד הקצה)
OLD_ROLL = {k: v * OLDK for k, v in {'AC-PR-01': 500, 'AC-BJ-01': 700, 'AC-TP-01': 700, 'AC-RJ-01': 1000, 'AC-NB-01': 1500, 'AC-CG-01': 1500, 'AC-LG-01': 1900, 'AC-QJ-01': 1100, 'AC-MW-01': 1600, 'AC-LT-01': 550, 'AC-CN-01': 650, 'AC-AM-01': 600, 'AC-TB-01': 650}.items()}
def can_a2(ac): return OLD_ROLL.get(ac, 9e9) <= RWY[2] - (A2 + 90) - 40
def two_arc(q, LX, R1=400.0, th1=math.radians(40), R2=80.0):
    # הגדול אל קו ההמתנה של A1: שתי קשתות (400 פיקס׳ ל-40°, ואז 80) — הזנב לא עובר מעל הכיס של PT-C / ‏C1 (נמצא בחיפוש במדויק, lg_turn.py: מרווח ≥ 1.2 מ׳)
    def arcpts(c, r, a0, a1):
        n = max(6, int(abs(a1 - a0) * r / 10)); return [[c[0] + r * math.cos(a0 + (a1 - a0) * i / n), c[1] + r * math.sin(a0 + (a1 - a0) * i / n)] for i in range(n + 1)]
    pts = [[0.0, 0.0]]; h = math.pi
    for R, dth in ((R1, th1), (R2, math.pi / 2 - th1)):
        p = pts[-1]; c = [p[0] + R * math.cos(h + math.pi / 2), p[1] + R * math.sin(h + math.pi / 2)]; a0 = h - math.pi / 2
        pts += arcpts(c, R, a0, a0 + dth)[1:]; h += dth
    dx = LX - pts[-1][0]; dy = q[1] - pts[0][1]; P = [[x + dx, y + dy] for x, y in pts]
    return [list(q)] + P + [[LX, M.HOLD + 40]] if q[0] > P[0][0] + 20 else None
def dep1(sid, ac, link='A1'):
    # הדחיפה + 14 ש׳ (הגרר מתנתק, המנועים) + ההסעה עד קו ההמתנה של A1 (או A2 — כמו AO_ROLL של הישן) — כמו s15_sim.departure, בפרופיל המהירות
    L = D.ACT[ac][0]; a = M.Actor('FL-' + sid, 'ac', ac, sid, L, D.ACT[ac][1]); p0 = M.ng_stop(sid, ac); a.t = 0.0
    LX = A1 if link == 'A1' else (A3 if link == 'A3' else A2)
    if not south(sid):
        R = 120 if L < 600 else 300      # הגדול (668 פיקס׳): הפנייה בדחיפה מתחילה ב-y 130 — הזנב לא עולה על המסלול (ב-110 הזנב הגיע ל-y ‏−661, על קו האמצע)
        P = M.Path(p0, N_).go(y=TACY + R).tr(E_, R); push_move(a, P.P, ac)
        a.wait(a.legs[-1]['p'][-1], W_, a.t + 14, flags=1); q = a.legs[-1]['p'][-1]
        RH = 250 if L > 600 else 90      # הגדול: פנייה רחבה אל קו ההמתנה — הכנף לא עוברת מעל הזנב של המטוס ב-C1 / הכיס של PT-C (נבדק במדויק)
        if q[0] < LX + RH + 20:
            # העמדה ממערב לחיבור (C1): הדחיפה עם הזנב מערבה (האף מזרחה), הסעה מזרחה ופנייה שמאלה אל קו ההמתנה
            a.legs = []; a.t = 0.0; P = M.Path(p0, N_).go(y=TACY + R).tr(W_, R); push_move(a, P.P, ac)
            a.wait(a.legs[-1]['p'][-1], E_, a.t + 14, flags=1); q = a.legs[-1]['p'][-1]
            if q[0] > LX - RH - 20: return None
            P = M.Path(q, E_).go(x=LX - RH).tr(N_, RH).go(y=M.HOLD + 40)
        elif L > 600 and link == 'A1':
            P2 = two_arc(q, LX)
            if P2 is None: return None
            a.taxiP = P2; a.t_taxi0 = a.t; pmove(a, P2, TAXI_BY.get(ac, TAXI_V), 8, 18); return a
        else:
            P = M.Path(q, W_).go(x=LX + RH).tr(N_, RH).go(y=M.HOLD + 40)
    else:
        R = 90; P = M.Path(p0, N_).go(y=TCCY + R).tr(W_, R); push_move(a, P.P, ac)
        a.wait(a.legs[-1]['p'][-1], E_, a.t + 14, flags=1); q = a.legs[-1]['p'][-1]
        P = M.Path(q, E_).go(x=TBCX - 110).tr(N_, 110).go(y=TACY + 110).tr(W_, 110).go(x=LX + 90).tr(N_, 90).go(y=M.HOLD + 40)
    a.taxiP = P.P; a.t_taxi0 = a.t; pmove(a, P.P, TAXI_BY.get(ac, TAXI_V), 8, 18)
    return a
def dep1q(sid, ac, link='A1'):
    # כמו dep1, ועם נקודת תור על A לפני הפנייה אל קו ההמתנה (aoHold של הישן — ההמתנה בדרך): A_a — עד נקודת התור (עוצר), A_b — ממנה אל קו ההמתנה
    a = dep1(sid, ac, link)
    if a is None or not hasattr(a, 'taxiP'): return None
    P = a.taxiP; k = None
    for i in range(1, len(P) - 1):
        h0 = math.atan2(P[i][1] - P[i - 1][1], P[i][0] - P[i - 1][0]); h1 = math.atan2(P[i + 1][1] - P[i][1], P[i + 1][0] - P[i][0])
        if abs(math.atan2(math.sin(h1 - h0), math.cos(h1 - h0))) > .02 and abs(P[i][1] - TACY) < 1 and math.cos(h0) < -.999: k = i
    if k is None: return None
    tsx = P[k][0]; qx = tsx + 40
    if not any(abs(p[1] - TACY) < 1 and p[0] > qx + 60 for p in P[:k]): return None
    j = max(i for i in range(k) if P[i][0] >= qx)
    Pa = P[:j + 1] + [[qx, TACY]]; Pb = [[qx, TACY]] + P[k:]
    A = M.Actor(a.id, 'ac', ac, sid, a.L, a.W); A.legs = [dict(g) for g in a.legs if g['t1'] <= a.t_taxi0 + 1e-6]; A.t = a.t_taxi0
    pmove(A, Pa, TAXI_BY.get(ac, TAXI_V), 8, .5)
    B = M.Actor(a.id, 'ac', ac, sid, a.L, a.W); B.t = 0.0; pmove(B, Pb, TAXI_BY.get(ac, TAXI_V), .5, 18)
    return A, B, [qx, TACY]
V_ARC = round(30 * OLDK, 1)   # הישן (042: apttTakeoff — vArc 30): הפנייה אל המסלול
def dep2_27(ac):
    # AIR-09: ‏27 — מקו ההמתנה של A3 פונים מערבה אל המסלול, הריצה מערבה (אותו אורך ריצה כמו 09 מ-A1 — עד 2260 פיקס׳), הטיפוס ויציאה מהעולם במערב
    L = D.ACT[ac][0]; a = M.Actor('x', 'ac', ac, '', L, D.ACT[ac][1]); q = [A3, M.HOLD + 40]; a.t = 0.0
    R = 90; P = M.Path(q, N_).go(y=RCY + R).tr(W_, R); a.move(P.P, 18, V_ARC, flags=1)
    q = a.legs[-1]['p'][-1]; xl = q[0] - 2260; a.move([q, [xl, RCY]], V_ARC, 640, flags=1)
    a.move([[xl, RCY], [0, RCY], [-2400, RCY]], 640, 760, z0=0, z1=520, flags=4)
    return a
def dep2(ac, link='A1'):
    if link == 'A3': return dep2_27(ac)
    # מקו ההמתנה: הכניסה למסלול (בקשת — במהירות של הישן), הריצה, הטיפוס ויציאה מהעולם (s15_sim.takeoff, בלי ההמתנה)
    L = D.ACT[ac][0]; a = M.Actor('x', 'ac', ac, '', L, D.ACT[ac][1]); LX = A1 if link == 'A1' else A2; q = [LX, M.HOLD + 40]; a.t = 0.0
    R = 90; P = M.Path(q, N_).go(y=RCY + R).tr(E_, R); a.move(P.P, 18, V_ARC, flags=1)
    q = a.legs[-1]['p'][-1]; a.move([q, [7600 if link == 'A1' else 8600, RCY]], V_ARC, 640, flags=1)
    a.move([[7600 if link == 'A1' else 8600, RCY], [9600, RCY], [11600, RCY]], 640, 760, z0=0, z1=520, flags=4)
    return a
def arr1(sid, ac, exit='A3'):
    if exit.endswith('r'): return arr1_27(sid, ac, exit[:-1])
    return arr1_09(sid, ac, exit)
def arr1_27(sid, ac, exit='A2'):
    # AIR-09: ‏27 — הגישה מהמזרח (מקצה העולם), הנגיעה ב-9000, הגלגול מערבה עד A2 / A1, פנייה שמאלה (דרומה) אל A, וההסעה לעמדה — כמו arr1 של 09
    L = D.ACT[ac][0]; a = M.Actor('x', 'ac', ac, sid, L, D.ACT[ac][1]); td = 9000; a.t = 0.0
    a.move([[11600, RCY], [td, RCY]], 720, 700, z0=620 * 2600 / 7700, z1=0, flags=4); t_td = a.t
    exit_x = A1 if exit == 'A1' else A2
    a.move([[td, RCY], [exit_x + 100, RCY]], 700, 60, flags=1)
    P = M.Path([exit_x + 100, RCY], W_).tr(S_, 100).go(y=TACY - 110); a.move(P.P, 60, 70, flags=1)
    return arr1_taxi(a, sid, ac, t_td)
def arr1_09(sid, ac, exit='A3'):
    # הגישה (מקצה העולם), הנגיעה ב-5300, הגלגול עד A3 (או A2 — היציאה המהירה באמצע, תוכנית האב F0), היציאה, וההסעה לעמדה — כמו s15_sim.arrival; t=0 = תחילת הגישה
    L = D.ACT[ac][0]; a = M.Actor('x', 'ac', ac, sid, L, D.ACT[ac][1]); td = 5300; a.t = 0.0
    a.move([[-2400, RCY], [td, RCY]], 720, 700, z0=620, z1=0, flags=4); t_td = a.t
    exit_x = A3 if exit == 'A3' else A2
    a.move([[td, RCY], [exit_x - 100, RCY]], 700, 60, flags=1)
    P = M.Path([exit_x - 100, RCY], E_).tr(S_, 100).go(y=TACY - 110); a.move(P.P, 60, 70, flags=1)
    return arr1_taxi(a, sid, ac, t_td)
def arr1_taxi(a, sid, ac, t_td):
    L = D.ACT[ac][0]; q = a.legs[-1]['p'][-1]; s = D.STANDS[sid]; stop = M.ng_stop(sid, ac)
    if not south(sid):
        dx = q[0] - s['cx']; r = min(110.0, abs(dx) / 2)
        if L > 600:   # הגדול נכנס לעמדה בפנייה רחבה (300) — הזנב לא עובר מעל המסלול
            P = M.Path(q, S_).tr(W_ if dx > 0 else E_, 110)   # 110 — בדיוק על הקו של A (TACY − 110 + 110); ב-100 הגדול נסע 10 פיקס׳ מהקו (s15_ac_centerline_d650 ב-try7406)
            q2 = P.P[-1]; dx2 = q2[0] - s['cx']
            if abs(dx2) < 300 + 20: return None, None
            P = P.go(x=s['cx'] + (300 if dx2 > 0 else -300)).tr(S_, 300).go(y=stop[1])
            a.taxiP = P.P; a.t_taxi0 = a.t; a.nlegs0 = len(a.legs); pmove(a, P.P, TAXI_BY.get(ac, TAXI_V), 70, 0.5); return a, t_td
        if r < 70: return None, None
        if dx > 0: P = M.Path(q, S_).tr(W_, r).go(x=s['cx'] + r).tr(S_, r).go(y=stop[1])
        else: P = M.Path(q, S_).tr(E_, r).go(x=s['cx'] - r).tr(S_, r).go(y=stop[1])
    else:
        # הדרום: מ-A3 מזרחה אל B (כמו היום); מ-A2 — מזרחה לאורך A עד B (נגד הזרם של ההמראות — הבדיקה מכריעה)
        P = M.Path(q, S_).tr(E_, 110); x1 = P.P[-1][0]
        P = (P.go(x=TBCX - 110).tr(S_, 110) if x1 < TBCX - 110 else P.tr(S_, TBCX - x1)).go(y=TCCY - 110).tr(W_, 110).go(x=s['cx'] + 90).tr(S_, 90).go(y=stop[1])
    a.taxiP = P.P; a.t_taxi0 = a.t; a.nlegs0 = len(a.legs); pmove(a, P.P, TAXI_BY.get(ac, TAXI_V), 70, 0.5)
    return a, t_td
# ---------------------------------------------------------------- המכשולים מה-dump (או מהנתונים של 019l)
PK_L = {'AC-LG-01': 668, 'AC-NB-01': 376, 'AC-RJ-01': 317, 'AC-CG-01': 549, 'AC-TB-01': 120, 'AC-LT-01': 91, 'AC-PR-01': 83, 'AC-BJ-01': 144, 'AC-CN-01': 144}
PK_W = {'AC-LG-01': 648, 'AC-NB-01': 358, 'AC-RJ-01': 260, 'AC-CG-01': 476, 'AC-TB-01': 200, 'AC-LT-01': 112, 'AC-PR-01': 110, 'AC-BJ-01': 158, 'AC-CN-01': 140}
def pk_actor(sid, ac):
    s = D.STANDS[sid]; L = PK_L.get(ac, 300); Wd = PK_W.get(ac, 300); a = M.Actor('PK-' + sid, 'ac', ac, sid, L, Wd)
    a.legs = [dict(p=[[s['cx'], s['nose'] - M.NGF.get(ac, .12) * L]], t0=-T, t1=3 * T, h=S_, f=0)]; return a
def ffr3_actors(M3):
    # הגרירות של R3 בלילה (fieldfix, ‏074zo: FFR3.build) — היציאה ב-18:00 / 18:10 (שלב 0 / 20 במחזור), החזרה ב-04:45 (שלב 570), וביניהן המטוס ב-R3
    out = []
    if not isinstance(M3, list): return out
    for m in M3:
        ac = m.get('ac') or 'AC-RJ-01'; L = m.get('Lpx') or D.ACT.get(ac, (300, 300))[0]; Wd_ = D.ACT.get(ac, (300, 300))[1]
        t_out = 0.0 if (m.get('tOut') is not None and m['tOut'] < 18 * 60 + 5) else 20.0
        for nm, part, t0 in (('out', m['out'], t_out), ('back', m['back'], 570.0)):
            a = M.Actor('R3-' + nm + '-' + str(m.get('id')), 'ac', ac, 'R3', L, Wd_)
            a.legs = [dict(g, t0=g['t0'] + t0, t1=g['t1'] + t0) for g in part['legs']]
            out.append(a)
    return [a for a in out if TOWS] + r3_night(M3)
TOWS = os.environ.get('FT_TOWS', '0') != '0'   # 0 (ברירת המחדל): הגרירות של R3 לא מכשול — הזמנים שלהן נבחרים אחרי הלוח (tow_search, השריון של AO לגרירות של G77_MLV בישן)
R3P = [9369.0, 2180.0, -math.pi / 2]           # 019m:S15_HGR.r3
FF_W = {'AC-RJ-01': 260, 'AC-BJ-01': 158, 'AC-LT-01': 112, 'AC-PR-01': 110, 'AC-NB-01': 358, 'AC-LG-01': 648, 'AC-CG-01': 476, 'AC-TB-01': 200, 'AC-TP-01': 270, 'AC-CN-01': 140}
def r3_night(M3):
    # המטוס של הלילה ב-R3 — הבדיקה fieldfix_r3 (074zo:ffR3Audit) בודקת אותו מול כל מי שנע לאורך כל המחזור (הלילה ארוך ממחזור) — מכשול קבוע
    out = []
    for m in (M3 if isinstance(M3, list) else []):
        a = M.Actor('R3-night-' + str(m.get('id')), 'ac', m.get('ac') or 'AC-RJ-01', 'R3', m.get('Lpx') or 300, FF_W.get(m.get('ac'), 150))
        a.legs = [dict(p=[R3P[:2]], t0=-T, t1=3 * T, h=R3P[2], f=0)]; out.append(a)
    return out
def tow_search(movers, M3, margin=6.0, dt=.5):
    # הזמנים של הגרירות אל R3 ובחזרה (fieldfix: ‏18:00 / 18:10, ‏04:45) — לכל אחד מהשלושה: הדקה הקרובה לזמן של fieldfix שבה כל הדרך פנויה מול כל מה שנע
    # (כמו ffR3Audit: הקופסאות של S15, כל 0.5 ש׳, ועוד margin ש׳ לפני ואחרי); ‏1 דקת משחק = 2 ש׳ במחזור
    if not isinstance(M3, list): return {}
    PA = [(o, pose_arr(o)) for o in movers]; res = {}
    def path_poses(L):
        a = M.Actor('tw', 'ac', 'AC-RJ-01', '', 300, 300); a.legs = L['legs']; n = int(L['dur'] / dt) + 1
        P0 = M.evalp(a, 0); P1 = M.evalp(a, L['dur'])
        ts = [-margin + k * dt for k in range(int((L['dur'] + 2 * margin) / dt) + 1)]
        return [(t, M.evalp(a, min(max(t, 0), L['dur'])) or (P0 if t < 0 else P1)) for t in ts]
    def free(m, PP, ph):
        me = M.Actor('m', 'ac', m.get('ac') or 'AC-RJ-01', '', m.get('Lpx') or 300, FF_W.get(m.get('ac'), 150))
        for t, P in PP:
            A = M.boxes(me, tuple(P[:3]) + (0, 0))
            if not A: continue
            i = int(round(((ph + t) % T) / EDT)) % EN
            for o, Y in PA:
                r = Y[i]
                if np.isnan(r[0]) or abs(r[0] - P[0]) > 800 or abs(r[1] - P[1]) > 800: continue
                if o.kind == 'veh' and r[4] == 16: continue
                B = boxes_of(o, tuple(r))
                if any(M.obb_hit(x, y) for x in A for y in B): return (o.id, round((ph + t) % T, 1))
        return None
    for m in M3:
        d_out = (m.get('tOut') if m.get('tOut') is not None else 18 * 60 + 10); d_back = 4 * 60 + 45
        po = path_poses(m['out']); pb = path_poses(m['back']); got = {}
        for nm, PP, m0, lo, hi in (('out', po, d_out, 17 * 60, 19 * 60 + 40), ('back', pb, d_back, 4 * 60 + 30, 6 * 60 + 30)):
            cands = sorted(range(lo, hi + 1), key=lambda x: (abs(x - m0), x)); first = None
            for mm in cands:
                h = free(m, PP, (2 * mm) % T)
                if h is None: got[nm] = mm; break
                if first is None: first = (mm, h)
            if nm not in got: got[nm + '_why'] = first
        res[m['id']] = got
    return res
class World:
    def __init__(s, dump, drop=()):
        s.SIM = dump; s.FL = [actor(o) for o in dump['flights']]; s.VH = [actor(o) for o in dump['veh'] if o['id'] not in drop]; s.drop = set(drop)
        s.HE = [actor(o) for o in dump.get('heli', [])]; s.TW = ffr3_actors(dump.get('ffr3'))
        s.sched = [list(q) for q in dump['sched']]; s.act = {q[0] for q in s.sched}
        mov = {v['id'] for v in dump['veh']}; s.SP = []
        for vid, sp in dump['spots'].items():
            if vid in mov: continue
            r = sp['rect']; w, h = r[2] - r[0], r[3] - r[1]; x = M.Actor('SP-' + vid, 'veh', 'X', sp.get('home', ''), max(w, h), min(w, h))
            x.legs = [dict(p=[[(r[0] + r[2]) / 2, (r[1] + r[3]) / 2]], t0=-T, t1=3 * T, h=(math.pi / 2 if h >= w else 0), f=0)]; s.SP.append(x)
        s.PK = {sid: pk_actor(sid, ac) for sid, ac in dump['parked'].items() if ac and sid not in s.act}
        s.occ = Occ(); s.occA = Occ(); s.static = np.zeros(NC, dtype=np.uint8)
        for a in s.FL + s.HE + s.TW: s.occ.add_actor(a); s.occA.add_actor(a)
        for v in s.VH: s.occ.add_actor(v, vk=VK)
        s.rebuild_static()
        s.pkc = {sid: np.unique(np.concatenate([obb_cells(b, 0) for b in M.boxes(a, M.evalp(a, 0))])) for sid, a in s.PK.items()}
        s.busy = []
        for a in s.FL: s.busy += [list(w[:3]) + [win_kind(a, w)] for w in flight_rwy_wins(a)]
        s.new = []; s.newveh = []; s.log = []
    def rebuild_static(s, skip=()):
        s.static = np.zeros(NC, dtype=np.uint8)
        for x in s.SP:
            if x.id in skip: continue
            P = M.evalp(x, 0); s.static[obb_cells(boxes_of(x, P, VK)[0], 0)] = 1
    def static_mask(s, skip):
        m = s.static.copy()
        for sid, c in s.pkc.items():
            if sid != skip and sid not in s.act: m[c] = 1
        return m
# ---------------------------------------------------------------- החיפוש של טיסה אחת (aoSearch של הישן, על כל ההזזות בבת אחת)
WMAX = int(os.environ.get('FT_WMAX', 45)); WQ = int(os.environ.get('FT_WQ', 60))   # WQ — ההמתנה בתור על A (לפני הפנייה אל קו ההמתנה)      # ההמתנה הארוכה בקו ההמתנה (התור למסלול; בישן AO.cfg.maxHold 15, ‏MAXW 360)
def hold_cells(pose, ac):
    a = M.Actor('h', 'ac', ac, '', *D.ACT[ac]); return np.unique(np.concatenate([obb_cells(b, MARGIN_AC) for b in M.boxes(a, pose)]))
def free_prefix(occ, cells, smask):
    # לכל שנייה: האם הצורה הקבועה (המתנה / עמידה) פנויה; ומערך מצטבר לבדיקת קטע
    if smask[cells].any(): return None
    bad = occ.o[:, cells].any(axis=1).astype(np.int64); cs = np.concatenate([[0], np.cumsum(np.concatenate([bad, bad, bad]))])
    return cs
def seg_free(cs, t0, t1):
    # [t0, t1) בשניות (אפשר מעבר למחזור)
    a = int(math.floor(t0 / DT)) % N; b = a + max(0, int(math.ceil((t1 - t0) / DT)))
    if b - a >= N: return cs[a + N] - cs[a] == 0 and cs[a + 2 * N] - cs[a + N] == 0
    return cs[b] - cs[a] == 0
def still(ac, p, h):
    a = M.Actor('s', 'ac', ac, '', *D.ACT[ac]); a.legs = [dict(p=[list(p)], t0=-1, t1=1, h=h, f=0)]; return a
def static_hit(Wd, a, t0, t1, skip_pk, m=4.0):
    # מול מה שחונה קבוע (הרכבים בכיסים, המטוסים החונים) — בדיקה מדויקת (OBB) במקום הרסטר (שהוא שמרני ב-חצי תא)
    S = [x for x in Wd.SP] + [p for sid, p in Wd.PK.items() if sid != skip_pk and sid not in Wd.act]
    SB = [(x, boxes_of(x, M.evalp(x, 0), VK if x.kind == 'veh' else 1.0)) for x in S]
    t = t0
    while t <= t1 + 1e-6:
        P = M.pose(a, t)
        if P:
            for b in M.boxes(a, P):
                bb = (b[0], b[1], b[2], b[3] + m, b[4] + m)
                for x, B in SB:
                    if abs(B[0][0] - b[0]) > 900 or abs(B[0][1] - b[1]) > 900: continue
                    if any(M.obb_hit(bb, q) for q in B): return x.id, t
        t += .2
    return None
def plan_flight(Wd, sid, ac, al, phase=0, prefer=None, accept=None, links=('A1', 'A2'), exits=('A3', 'A2')):
    smask = np.zeros(NC, dtype=np.uint8); mp = MINPARK.get(ac, 300)
    DEP = []; ARR = []; why0 = []
    for ln in links:
        if ln == 'A2' and not can_a2(ac): continue
        A1_ = dep1(sid, ac, ln)
        if A1_ is None: continue
        B2 = dep2(ac, ln); tp1 = template(A1_, 0, A1_.t); tp2 = template(B2, 0, B2.t)
        h_ = static_hit(Wd, A1_, 0, A1_.t, sid) or static_hit(Wd, B2, 0, B2.t, sid)
        if h_: why0.append('dep ' + ln + ' ' + h_[0]); continue
        qh = A1_.legs[-1]['p'][-1]; hcs = free_prefix(Wd.occ, hold_cells([qh[0], qh[1], N_, 0, 1], ac), smask)
        if static_hit(Wd, still(ac, qh, N_), 0, 0, sid): hcs = None
        if hcs is None: why0.append('hold ' + ln + ' static'); continue
        DEP.append(dict(ln=ln, A=A1_, B=B2, d1=A1_.t, d2=B2.t, c1=shifts_conflict(Wd.occ, tp1, 0), c2=shifts_conflict(Wd.occ, tp2, 0), hcs=hcs, w2=rwy_wins_rel(B2, 0, B2.t), qh=qh, q=None))
        QQ = dep1q(sid, ac, ln) if WQ > 0 else None
        if QQ:
            Aa, Ab, Qp = QQ; tpa = template(Aa, 0, Aa.t); tpb = template(Ab, 0, Ab.t); qcs = free_prefix(Wd.occ, hold_cells([Qp[0], Qp[1], W_, 0, 1], ac), smask)
            if qcs is not None and not static_hit(Wd, Ab, 0, Ab.t, sid):
                DEP.append(dict(ln=ln, A=Aa, Ab=Ab, B=B2, d1=Aa.t, d1b=Ab.t, d2=B2.t, c1=shifts_conflict(Wd.occ, tpa, 0), c1b=shifts_conflict(Wd.occ, tpb, 0), c2=DEP[-1]['c2'], qcs=qcs, hcs=hcs, w2=rwy_wins_rel(B2, 0, B2.t), qh=qh, q=Qp))
    for ex in exits:
        if ex == 'A2' and ac in HEAVY and ac != 'AC-LG-01': continue
        C3, ttd_rel = arr1(sid, ac, ex)
        if C3 is None: continue
        tp3 = template(C3, 0, C3.t)
        h_ = static_hit(Wd, C3, 0, C3.t, sid)
        if h_: why0.append('arr ' + ex + ' ' + h_[0]); continue
        stop = C3.legs[-1]['p'][-1]; pcs = free_prefix(Wd.occ, hold_cells([stop[0], stop[1], S_, 0, 0], ac), smask)
        if static_hit(Wd, still(ac, stop, S_), 0, 0, sid): pcs = None
        if pcs is None: why0.append('park static'); continue
        ARR.append(dict(ex=ex, C=C3, d3=C3.t, c3=shifts_conflict(Wd.occ, tp3, 0), w3=rwy_wins_rel(C3, 0, C3.t), stop=stop, pcs=pcs))
    if not DEP or not ARR: return None, 'נוגע במטוס / ברכב שחונה קבוע (' + ', '.join(why0) + ')'
    opts = []
    order = [(phase + k) % N for k in range(N)] if prefer is None else prefer
    for rank, s0 in enumerate(order):
        for dp in DEP:
            if dp['c1'][s0]: continue
            th = s0 + dp['d1']; wq = 0
            if dp['q'] is not None:
                # התור על A: ההמתנה הקצרה ביותר בנקודת התור שאחריה ההמשך עד קו ההמתנה פנוי (בלי — הגרסה בלי התור)
                t1 = None
                for tq in range(int(math.ceil(th + 1)), int(math.ceil(th + 1)) + WQ):
                    if not seg_free(dp['qcs'], th, tq): break
                    if not dp['c1b'][tq % N]: t1 = tq; break
                if t1 is None: continue
                wq = t1 - th; th = t1 + dp['d1b']
            tg0 = int(math.ceil(th + 4 - 1e-6))
            for tg in range(tg0, tg0 + WMAX):
                if not seg_free(dp['hcs'], th, tg): break
                if dp['c2'][tg % N]: continue
                ww = [tg + dp['w2'][0][0], tg + dp['w2'][0][1]]
                if not rwy_ok(ww, ac, Wd.busy): continue
                opts.append((tg - th + wq, rank, s0, dp, tg, ww, wq)); break
    opts.sort(key=lambda o: (round(o[0] / 6), o[1]))
    tries = 0; DG = dict(c3=0, rwy=0, park=0)
    for w, rank, s0, dp, tg, ww, wq in opts:
        tair = tg + dp['d2']; got = None
        for ar in ARR:
            for sa in range(int(math.ceil(tair)), int(s0 + T - mp - ar['d3']) + 1):
                if ar['c3'][sa % N]: DG['c3'] += 1; continue
                wa = [sa + ar['w3'][0][0], sa + ar['w3'][0][1]]
                if not rwy_ok(wa, ac, Wd.busy + [[ww[0], ww[1], ac]]): DG['rwy'] += 1; continue
                ob = sa + ar['d3']
                if not seg_free(ar['pcs'], ob, s0 + T) or not seg_free(ar['pcs'], s0, s0 + .01): DG['park'] += 1; continue
                got = (sa, ar, ob, wa); break
            if got: break
        if not got: continue
        sa, ar, ob, wa = got
        cand = dict(s0=s0, w=w, tg=tg, sa=sa, ob=ob, park=s0 + T - ob, rw=[ww, wa], ln=dp['ln'], ex=ar['ex'], wq=wq)
        a = build_flight(sid, ac, al, cand, dp['A'], dp['B'], ar['C'], dp['qh'], ar['stop'], dp['d1'], dp)
        tries += 1
        if accept is None or accept(a): return dict(a=a, best=cand, d=(dp['d1'], dp['d2'], ar['d3'])), 'נכנס'
        if tries > 60: break
    return None, 'אין זמן פנוי (%d אפשרויות דחיפה, %d נבדקו עם הגרר; נחיתה: %s)' % (len(opts), tries, DG)
def build_flight(sid, ac, al, best, A1_, B2, C3, qh, stop, d1, dp=None):
    # ההרכבה: הרגליים של s15_sim (דחיפה, המתנה, הסעה, המתנה בקו, כניסה, ריצה, טיפוס, גישה, נגיעה, יציאה, הסעה, עמידה)
    a = M.Actor('FL-' + sid, 'ac', ac, sid, D.ACT[ac][0], D.ACT[ac][1]); a.airline = al
    def put(src, t0):
        for g in src.legs:
            h = dict(g); h['t0'] = round(g['t0'] + t0, 2); h['t1'] = round(g['t1'] + t0, 2); a.legs.append(h)
    put(A1_, best['s0'])
    if dp is not None and dp.get('q') is not None:
        # ההמתנה בתור על A — רגל איטית מאוד (חצי פיקסל) ולא המתנה, כדי שהמבנה של הרגליים (g77TvLegIx: דחיפה, המתנה, הסעה, המתנה בקו, כניסה, ריצה) לא ישתנה
        Q = dp['q']; t1 = best['s0'] + d1 + best['wq']
        if best['wq'] > 0: a.legs.append(dict(p=[list(Q), [Q[0] - .5, Q[1]]], t0=round(best['s0'] + d1, 2), t1=round(t1, 2), v0=round(.5 / max(1e-6, best['wq']), 4), v1=round(.5 / max(1e-6, best['wq']), 4), r=0, z0=0, z1=0, f=1))
        put(dp['Ab'], t1); d1 = t1 - best['s0'] + dp['d1b']
    a.legs.append(dict(p=[list(qh)], t0=round(best['s0'] + d1, 2), t1=round(best['tg'], 2), h=round(N_, 4), f=1))
    put(B2, best['tg']); put(C3, best['sa'])
    a.legs.append(dict(p=[list(stop)], t0=round(best['ob'], 2), t1=round(best['s0'] + T, 2), h=round(S_, 4), f=0))
    return a
def commit(Wd, sid, ac, al, R, veh=()):
    for v in veh:
        Wd.VH = [x for x in Wd.VH if x.id != v.id] + [v]; Wd.newveh = [x for x in Wd.newveh if x.id != v.id] + [v]; Wd.occ.add_actor(v, vk=VK)
        Wd.SP = [x for x in Wd.SP if x.id != 'SP-' + v.id]
    Wd.rebuild_static()
    a = R['a']; Wd.FL.append(a); Wd.occ.add_actor(a); Wd.occA.add_actor(a); Wd.busy += [[w[0] % T, w[0] % T + (w[1] - w[0]), ac] + ([R['best']['kd'][i]] if R['best'].get('kd') else []) for i, w in enumerate(R['best']['rw'])]
    Wd.act.add(sid); Wd.sched.append([sid, ac, al, round(R['best']['sa'] % T, 2), round(R['best']['s0'] % T, 2)]); Wd.new.append(a)
# ---------------------------------------------------------------- הגרר של הטיסה (s15_sim.tug — אותה צורה: מהבית אל האף, צמוד בדחיפה, מתנתק, מתרחק וחוזר)
def spot_c(sp): r = sp['rect']; return [(r[0] + r[2]) / 2, (r[1] + r[3]) / 2]
HH = {'S': S_, 'N': N_, 'E': E_, 'W': W_}
def tug_build(Wd, vid, a, early=0.0, late=1.0, home=None, hh=None):
    sp = Wd.SIM['spots'].get(vid); home = home or spot_c(sp); hh = hh if hh is not None else HH[(sp or {}).get('h', 'S')]
    g = a.legs[0]; t_push = g['t0']; p0 = g['p'][0]; sid = a.home
    v = M.Actor(vid, 'veh', 'LV-PT-01', (sp or {}).get('home', 'AIR'), 60, 22)
    if sid[0] in 'RG': v.L = 44
    off = M.NGF[a.model] * a.L + v.L / 2 + 4; front = [p0[0], p0[1] + off]
    big = a.L > 600
    if sid[0] == 'P':
        ln = 989 if big else (864 if p0[0] > home[0] else 820)
        out = [home, [home[0], ln], [p0[0], ln], front]
    else:
        out = [home, [home[0], front[1] + 12], [front[0], front[1] + 12], front]
    dur = 2 * M.plen(M.fillet(out)) / (40 + 8)
    v.t = t_push - dur - 6 - early; v.move(out, 40, 8); v.wait(front, N_, t_push, flags=8)
    v.legs.append(dict(p=[g['p'][0], g['p'][-1]], t0=g['t0'], t1=g['t1'], att=a.id, f=16)); v.t = g['t1']
    q = g['p'][-1]; h = W_ if sid[0] == 'P' else E_
    nose = [q[0] + off * math.cos(h), q[1] + off * math.sin(h)]
    v.wait(nose, h + math.pi, v.t + late, flags=8)
    clear_y = q[1] + a.W / 2 + v.L / 2 + 14
    if sid[0] == 'P':
        ln = 989 if big else (820 if home[0] < nose[0] else 864)
        back = [nose, [nose[0], clear_y], [nose[0], ln], [home[0], ln], home]
        v.move(back[:2], 45, 20); v.move(back[1:], 20, 8)
    else:
        back = [nose, [nose[0], q[1] - 0], [home[0], q[1] - 0], home] if False else list(reversed(out))
        back = [nose, [nose[0], front[1] + 12], [home[0], front[1] + 12], home]
        v.move(back, 30, 8)
    v.wait(home, hh, t_push + T - dur - 6 - early)
    return v
def veh_template(v):
    # התבנית של רכב — בלי הזמן שבבית (חונה) ובלי הזמן הצמוד לאף
    I = []; C = []
    t0 = v.legs[0]['t0']
    for k in range(int(T / DT)):
        t = t0 + k * DT; P = M.pose(v, t)
        if not P or P[4] == 16: continue
        if P[4] == 0 and abs(P[0] - v.legs[-1]['p'][0][0]) < 1 and abs(P[1] - v.legs[-1]['p'][0][1]) < 1: continue
        for b in boxes_of(v, P, VK):
            c = obb_cells(b, 2.0); I.append(np.full(len(c), k, dtype=np.int64)); C.append(c)
    return (np.concatenate(I), np.concatenate(C), int(T / DT)) if I else (np.zeros(0, dtype=np.int64),) * 2 + (0,)
def plan_tug(Wd, vid, a, own_cells=None):
    # הגרר מול המטוסים בלבד (הטיסות, החונים, המסוק) — מול הרכבים הסדר נעשה במשחק ב-s15k (074r: s15kRun — "aoSearchG של הישן": זמן יציאה אחר בתוך המרווח)
    pkm = np.zeros(NC, dtype=np.uint8)
    for sid, c in Wd.pkc.items():
        if sid not in Wd.act and sid != a.home: pkm[c] = 1
    for early in (0, 4, 8, 14, 20, 30, 45, 60):
        for late in (1, 4, 8, 14, 20, 30):
            v = tug_build(Wd, vid, a, early, late)
            I, C, n = veh_template(v)
            if not len(I): return v, (early, late)
            hits = Wd.occA.o[(int(round(v.legs[0]['t0'] / DT)) + I) % N, C]
            if not hits.any() and not pkm[C].any(): return v, (early, late)
    return None, None
# ---------------------------------------------------------------- גרר עם כמה נסיעות במחזור (כמו AF של הישן: רכב אחד של הצי משרת עמדות שונות, נסיעה אחרי נסיעה, AF.GAP בין משימות)
AF_GAP = 2.5
def base_trips(v):
    # הנסיעות של רכב מתוך הרגליים שלו: כל מה שבין עמידות בבית (f 0)
    L = v['legs'] if isinstance(v, dict) else v.legs; out = []; cur = []
    for g in L:
        if g.get('h') is not None and g.get('f') == 0:
            if cur: out.append(cur); cur = []
            continue
        cur.append(g)
    if cur: out.append(cur)
    return out
def trip_span(tr): return tr[0]['t0'], tr[-1]['t1']
def tug_trip(vid, a, home, hh, early=0.0, late=1.0):
    g = dict(a.legs[0]); pl = [x for x in a.legs if x.get('r') and x.get('f') == 2]
    if pl: g['t1'] = pl[-1]['t1']; g['p'] = [a.legs[0]['p'][0], pl[-1]['p'][-1]]
    t_push = g['t0']; p0 = g['p'][0]; sid = a.home
    v = M.Actor(vid, 'veh', 'LV-PT-01', '', 44 if sid[0] in 'RG' else 60, 22)
    off = M.NGF[a.model] * a.L + v.L / 2 + 4; front = [p0[0], p0[1] + off]; big = a.L > 600
    HG = vid == 'PT-HGR'   # הגרר של האנגר א׳ — גרר שני ל-GA: בדרכי השירות החד-סטריות (דרך הבסיס מזרחה, מעבר C מזרח דרומה, דרך המרוחקות מערבה, מעבר C מערב צפונה)
    if HG:
        out = [home, [home[0], 1648], [9192, 1648], [9192, front[1] + 12], [front[0], front[1] + 12], front]
    elif sid[0] == 'P':
        ln = 989 if big else (864 if p0[0] > home[0] else 820); out = [home, [home[0], ln], [p0[0], ln], front]
    elif sid[0] == 'C' and sid != 'C2':
        # עמדת המשא המערבית (C1): מהבית מדרום לאף של C2 (y 760 — לא דרך המטוס שחונה ב-C2), מערבה, וצפונה אל האף
        yl = C_LANE if abs(home[1] - C_LANE) > 30 else home[1] + 45   # מכיס שבגובה השורה (PT-P1) — קודם דרומה, לא פנייה בתוך הכיס (BT-P1 צמוד — try7407)
        out = [home, [home[0], yl], [front[0], yl], front]
    elif sid[0] == 'R' and abs(home[0] - front[0]) > 60:
        # העמדות המרוחקות: מהכיס דרומה אל השורה y 2540 (מדרום לאפים של R — לא מתחת לאף של השכנה), לאורכה, וצפונה אל האף
        out = [home, [home[0], R_LANE], [front[0], R_LANE], front]
    else:
        out = [home, [home[0], front[1] + 12], [front[0], front[1] + 12], front]
    dur = 2 * M.plen(M.fillet(out)) / (40 + 8)
    v.t = t_push - dur - 6 - early; v.move(out, 40, 8); v.wait(front, N_, t_push, flags=8)
    v.legs.append(dict(p=[g['p'][0], g['p'][-1]], t0=g['t0'], t1=g['t1'], att=a.id, f=16)); v.t = g['t1']
    q = g['p'][-1]; h = W_ if sid[0] == 'P' else E_
    nose = [q[0] + off * math.cos(h), q[1] + off * math.sin(h)]
    v.wait(nose, h + math.pi, v.t + late, flags=8)
    if sid[0] == 'P':
        clear_y = q[1] + a.W / 2 + v.L / 2 + 14; ln = 989 if big else (820 if home[0] < nose[0] else 864)
        back = [nose, [nose[0], clear_y], [nose[0], ln], [home[0], ln], home]; v.move(back[:2], 45, 20); v.move(back[1:], 20, 8)
    elif HG:
        back = [nose, [nose[0], 2056], [7887, 2056], [7887, 1648], [home[0], 1648], home]; v.move(back[:2], 45, 20); v.move(back[1:], 20, 8)
    elif sid.startswith('GA'):
        yb = 2092 if nose[0] < home[0] else (D.SVC['AIR-TAIL_ROAD']['rect'][1] + D.SVC['AIR-TAIL_ROAD']['rect'][3]) / 2   # 2092 — מעל הכיס של PT-GA1 (GA1|GA2 מ-2130; ב-2100 — נגיעה ב-try7409)
        back = [nose, [nose[0], yb], [home[0], yb], home]; v.move(back[:2], 45, 20); v.move(back[1:], 20, 8)
    elif sid[0] == 'C' and sid != 'C2':
        yl = C_LANE if abs(home[1] - C_LANE) > 30 else home[1] + 45
        back = [nose, [nose[0], yl], [home[0], yl], home]; v.move(back[:2], 45, 20); v.move(back[1:], 20, 8)
    elif sid[0] == 'R' and abs(home[0] - front[0]) > 60:
        xr = nose[0] + 75   # חזרה דרומה ממזרח לקו של האף (המדרגות MS-R1 בכיס שממערב)
        back = [nose, [nose[0], nose[1] + 75], [xr, nose[1] + 75], [xr, R_LANE], [home[0], R_LANE], home]; v.move(back[:2], 45, 20); v.move(back[1:], 20, 8)
    else:
        back = [nose, [nose[0], front[1] - 60], [home[0], front[1] - 60], home]; v.move(back[:2], 45, 20); v.move(back[1:], 20, 8)
    return v.legs
C_LANE = float(os.environ.get('FT_CLANE', 760)); R_LANE = float(os.environ.get('FT_RLANE', 2540))
def trips_ok(trs, new):
    a0, a1 = trip_span(new)
    for tr in trs:
        b0, b1 = trip_span(tr)
        for k in (-T, 0, T):
            if not (a1 + AF_GAP <= b0 + k or b1 + k + AF_GAP <= a0): return False
    return True
def _shift_trip(tr, dt): return [dict(g, t0=round(g['t0'] + dt, 2), t1=round(g['t1'] + dt, 2)) for g in tr]
def veh_from_trips(vid, model, homeid, L, Wd_, home, hh, trs):
    # כל הנסיעות בתוך מחזור אחד שמתחיל בנסיעה המוקדמת (נסיעה שתוכננה ב-+720 — מוזזת אחורה)
    trs = sorted(trs, key=lambda tr: tr[0]['t0']); b0 = trs[0][0]['t0']
    trs = sorted([_shift_trip(tr, -T * math.floor((tr[0]['t0'] - b0) / T)) if tr[0]['t0'] - b0 >= T - 1e-6 else tr for tr in trs], key=lambda tr: tr[0]['t0'])
    v = M.Actor(vid, 'veh', model, homeid, L, Wd_); t_first = trs[0][0]['t0']
    for i, tr in enumerate(trs):
        if i: v.legs.append(dict(p=[list(home)], t0=round(trs[i - 1][-1]['t1'], 2), t1=round(tr[0]['t0'], 2), h=round(hh, 4), f=0))
        v.legs += [dict(g) for g in tr]
    v.legs.append(dict(p=[list(home)], t0=round(trs[-1][-1]['t1'], 2), t1=round(t_first + T, 2), h=round(hh, 4), f=0))
    return v
def trip_template(tr, L=44, W_=22):
    v = M.Actor('x', 'veh', 'X', '', L, W_); v.legs = tr; I = []; C = []; t0 = tr[0]['t0']; n = int((tr[-1]['t1'] - t0) / DT)
    for k in range(n + 1):
        P = M.pose(v, t0 + k * DT)
        if not P or P[4] == 16: continue
        for b in boxes_of(v, P, VK):
            c = obb_cells(b, 2.0); I.append(np.full(len(c), k, dtype=np.int64)); C.append(c)
    return (np.concatenate(I), np.concatenate(C)) if I else (np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.int64))
def veh_static_hit(Wd, tr, home, L=44, W_=22, dt=.5):
    # הנסיעה מול הכיסים של הרכבים שחונים קבוע (S15D.spots) — OBB מדויק, בלי הכיסים שליד הבית של הרכב עצמו
    v = M.Actor('x', 'veh', 'X', '', L, W_); v.legs = tr; t = tr[0]['t0']; t1 = tr[-1]['t1']
    SB = [(x, boxes_of(x, M.evalp(x, 0), VK)) for x in Wd.SP if math.hypot(x.legs[0]['p'][0][0] - home[0], x.legs[0]['p'][0][1] - home[1]) > 70]
    while t <= t1:
        P = M.evalp(v, t)
        if P and P[4] != 16:
            b = boxes_of(v, P, VK)[0]
            for x, B in SB:
                if abs(B[0][0] - b[0]) > 400 or abs(B[0][1] - b[1]) > 400: continue
                if M.obb_hit(b, B[0]): return x.id, round(t, 1)
        t += dt
    return None
def plan_trip(Wd, vid, a):
    T0 = Wd.tug[vid]; home, hh = T0['home'], T0['hh']
    pkm = np.zeros(NC, dtype=np.uint8)
    for sid, c in Wd.pkc.items():
        if sid not in Wd.act and sid != a.home: pkm[c] = 1
    OV = getattr(Wd, 'occV', None)
    for useV in ((True, False) if OV is not None else (False,)):
        for early in (0, 6, 14, 24, 40, 60):
            for late in (1, 5, 9):   # המטוס יוצא לדרך 14 ש׳ אחרי סוף הדחיפה — הגרר לא נשאר מול האף (FL-P5 × PT-P5 ב-try7406 עם 16)
                tr = tug_trip(vid, a, home, hh, early, late)
                if not trips_ok(T0['trips'], tr): continue
                I, C = trip_template(tr)
                if len(I):
                    ix = (int(round(tr[0]['t0'] / DT)) + I) % N
                    if Wd.occA.o[ix, C].any() or pkm[C].any() or (useV and OV.o[ix, C].any()): continue
                if veh_static_hit(Wd, tr, home, T0['L'], T0['W']): continue
                return tr, (early, late) + (('V',) if useV else ())
    return None, None
# ---------------------------------------------------------------- הבדיקה המדויקת בסוף (כמו s15SimAudit — 074j:108, ‏s15_sim.check): כל מטוס מול כל מטוס, רכב וחונה, כל 0.5 ש׳
def exact_check(FL, VH, PK, dt=.5, veh_pairs=False):
    issues = []; n = int(T / dt)
    for i in range(n):
        t = i * dt; P = []
        for a in FL + VH + PK:
            q = M.evalp(a, t)
            if not q: continue
            if a.kind == 'veh' and q[4] == 16: continue
            B = boxes_of(a, q)
            if not B: continue
            P.append((a, B, q))
        for x in range(len(P)):
            for y in range(x + 1, len(P)):
                a, A, qa = P[x]; b, Bb, qb = P[y]
                if a.kind == 'veh' and b.kind == 'veh' and not veh_pairs: continue
                if a.kind == 'veh' and b.kind == 'veh' and a.home == b.home and qa[4] == 0 and qb[4] == 0: continue
                if abs(qa[0] - qb[0]) > 900 or abs(qa[1] - qb[1]) > 900: continue
                if any(M.obb_hit(p, q) for p in A for q in Bb): issues.append((t, a.id, b.id))
    return issues
def rwy_check(FL):
    W = []
    for a in FL:
        for w in flight_rwy_wins(a): W.append((w[0], w[1], w[2], a.id))
    W.sort(); bad = []
    for i in range(len(W)):
        for j in range(len(W)):
            if i == j: continue
            a, b = W[i], W[j]
            for k in (-T, 0, T):
                b0, b1 = b[0] + k, b[1] + k
                if a[0] <= b0 and not (b0 >= a[1] + 3 + (8 if a[2] in HEAVY else 0)) and b0 < a[1] + 20: bad.append((round(a[0], 1), a[3], round(b0, 1), b[3]))
    occ = sum(w[1] - w[0] for w in W)
    return bad, round(occ / T * 100, 1), len(W)
# ---------------------------------------------------------------- בדיקה מדויקת של טיסה מועמדת מול הכול (OBB, כל 0.25 ש׳) — הרסטר הוא סינון; זו ההכרעה
EDT = .25; EN = int(T / EDT)
def pose_arr(a):
    X = np.full((EN, 5), np.nan)
    for i in range(EN):
        P = M.evalp(a, i * EDT)
        if P: X[i] = P[:5]
    return X
def world_cache(Wd):
    if getattr(Wd, 'PC', None) is not None: return Wd.PC
    Wd.PC = []
    for a in Wd.FL + Wd.VH + Wd.HE + Wd.TW: Wd.PC.append((a, pose_arr(a)))
    return Wd.PC
def cache_add(Wd, a):
    world_cache(Wd); Wd.PC.append((a, pose_arr(a)))
def exact_flight(Wd, a, m=1.0, skip_ids=(), vkv=None):
    vkv = VK if vkv is None else vkv
    PC = world_cache(Wd); X = pose_arr(a)
    S = [p for sid, p in Wd.PK.items() if sid != a.home and sid not in Wd.act] + Wd.SP
    for i in range(EN):
        q = X[i]
        if np.isnan(q[0]) or q[3] > 30: continue
        if q[4] == 0 and i > 0 and not np.isnan(X[i - 1][0]) and abs(X[i - 1][0] - q[0]) < .01 and abs(X[i - 1][1] - q[1]) < .01 and i % 8: continue   # עומד — כל 2 ש׳ מספיק
        A = [(b[0], b[1], b[2], b[3] + m, b[4] + m) for b in M.boxes(a, tuple(q))]
        for o, Y in PC:
            if o.id in skip_ids: continue
            r = Y[i]
            if np.isnan(r[0]) or abs(r[0] - q[0]) > 900 or abs(r[1] - q[1]) > 900: continue
            if o.kind == 'veh' and r[4] == 16: continue
            B = boxes_of(o, tuple(r), vkv if o.kind == 'veh' else 1.0)
            if any(M.obb_hit(x, y) for x in A for y in B): return (round(i * EDT, 2), o.id)
        for o in S:
            r = M.evalp(o, 0)
            if abs(r[0] - q[0]) > 900 or abs(r[1] - q[1]) > 900: continue
            B = boxes_of(o, r, VK if o.kind == 'veh' else 1.0)
            if any(M.obb_hit(x, y) for x in A for y in B): return (round(i * EDT, 2), o.id)
    return None

# ---------------------------------------------------------------- רכב שירות לצד המטוס בעמדה (s15_sim.side — אותה צורה), לפי חלון העמידה של הטיסה החדשה
def side_trip(vid, model, a, home, dx, dy, t_in, stay, ry, L=None, W=None, speed=40):
    s = D.STANDS[a.home]; st = M.ng_stop(a.home, a.model); tgt = [s['cx'] + dx, st[1] + dy]
    v = M.Actor(vid, 'veh', model, '', L or 40, W or 22)
    out = [home, [home[0], ry], [tgt[0], ry], tgt]; back = list(reversed(out))
    v.t = t_in; v.move(out, speed, 8); v.wait(tgt, N_, v.t + stay, flags=8); v.move(back, speed, 8)
    return v.legs
def park_window(a):
    g = a.legs[-1]; return g['t0'], g['t1']
def plan_side(Wd, vid, model, a, home, dx, dy, after, stay, ry, L, W_, before=60):
    p0, p1 = park_window(a); pkm = np.zeros(NC, dtype=np.uint8)
    for sid, c in Wd.pkc.items():
        if sid not in Wd.act: pkm[c] = 1
    OV = getattr(Wd, 'occV', None)
    for useV in ((True, False) if OV is not None else (False,)):
        for k in range(0, 160, 4):
            tr = side_trip(vid, model, a, home, dx, dy, p0 + after + k, stay, ry, L, W_)
            if tr[-1]['t1'] > p1 - before: break
            I, C = trip_template(tr)
            if len(I):
                ix = (int(round(tr[0]['t0'] / DT)) + I) % N
                if Wd.occA.o[ix, C].any() or pkm[C].any() or (useV and OV.o[ix, C].any()): continue
            return tr
    return None
# ---------------------------------------------------------------- ההסעה עם המתנות בדרך (aoHold של הישן, בכל נקודת תור לאורך A / B / C — "SIPP" על הקו):
# הדרך מחולקת לקטעים בנקודות תור (כל ~500 פיקס׳ על הישרים); לכל קטע 4 גרסאות (נכנס בתנועה / מעצירה × יוצא בתנועה / לעצירה);
# קדימה בחמדנות: עוברים בתנועה אם אפשר, ואם לא — הקטע הקודם מסתיים בעצירה, וממתינים בנקודה עד שהקטע הבא פנוי.
SEG_L = float(os.environ.get('FT_SEGL', 520)); WSEG = int(os.environ.get('FT_WSEG', 40))
def split_nodes(P):
    S = [0.0]
    for i in range(1, len(P)): S.append(S[-1] + math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]))
    L = S[-1]; cuts = []
    def straight_at(s):
        for i in range(1, len(P)):
            if S[i] >= s:
                h = math.atan2(P[i][1] - P[i - 1][1], P[i][0] - P[i - 1][0]); seglen = S[i] - S[i - 1]
                return seglen > 200 and (s - S[i - 1]) > 80 and (S[i] - s) > 80, i
        return False, len(P) - 1
    s = SEG_L
    while s < L - 250:
        ok, i = straight_at(s)
        if ok: cuts.append((s, i))
        s += SEG_L if ok else 40
    segs = []; prev = 0.0; pts = [list(P[0])]; k = 1; out = []
    # בונים את הקטעים: כל קטע — רשימת נקודות
    cut_s = [c[0] for c in cuts]; ci = 0; cur = [list(P[0])]
    for i in range(1, len(P)):
        while ci < len(cut_s) and cut_s[ci] <= S[i] + 1e-6 and cut_s[ci] > S[i - 1]:
            f = (cut_s[ci] - S[i - 1]) / max(1e-6, S[i] - S[i - 1]); q = [P[i - 1][0] + (P[i][0] - P[i - 1][0]) * f, P[i - 1][1] + (P[i][1] - P[i - 1][1]) * f]
            cur.append(q); out.append(cur); cur = [q]; ci += 1
        cur.append(list(P[i]))
    out.append(cur)
    return out
def seg_variants(seg, ac, vin_flow, vout_flow, v0=8, vend=18):
    V = TAXI_BY.get(ac, TAXI_V); res = {}
    for mi in ('f', 's'):
        for mo in ('f', 's'):
            if mi == 'f' and vin_flow is None: continue
            if mo == 'f' and vout_flow is None: continue
            vs = (vin_flow if mi == 'f' else .5) if vin_flow is not None or mi == 's' else v0
            ve = (vout_flow if mo == 'f' else .5)
            a = M.Actor('x', 'ac', ac, '', *D.ACT[ac]); a.t = 0.0; pmove(a, seg, V, vs, ve); res[(mi, mo)] = a
    return res
def seg_plan(sid, ac, P, first_vs, last_ve):
    # הקטעים והגרסאות: הקטע הראשון נכנס ב-first_vs (מעצירה / בתנועה), האחרון יוצא ב-last_ve
    SG = split_nodes(P); V = TAXI_BY.get(ac, TAXI_V); out = []
    for j, seg in enumerate(SG):
        first = j == 0; last = j == len(SG) - 1; var = {}
        for mi in (('x',) if first else ('f', 's')):
            for mo in (('x',) if last else ('f', 's')):
                vs = first_vs if first else (V if mi == 'f' else .5); ve = last_ve if last else (V if mo == 'f' else .5)
                a = M.Actor('x', 'ac', ac, '', *D.ACT[ac]); a.t = 0.0; pmove(a, seg, V, vs, ve); var[(mi, mo)] = a
        out.append(dict(seg=seg, var=var, node=seg[-1], h=math.atan2(seg[-1][1] - seg[-2][1], seg[-1][0] - seg[-2][0])))
    return out
def seg_prepare(Wd, SP_, ac, smask):
    for sg in SP_:
        sg['c'] = {k: shifts_conflict(Wd.occ, template(a, 0, a.t), 0) for k, a in sg['var'].items()}
        sg['d'] = {k: a.t for k, a in sg['var'].items()}
        q = sg['node']; sg['ncs'] = free_prefix(Wd.occ, hold_cells([q[0], q[1], sg['h'], 0, 1], ac), smask)
    return SP_
def _free(sg, k, t):
    ti = int(round(t)); return k in sg['c'] and not sg['c'][k][ti % N]
def seg_walk(SP_, t0, n0cs=None):
    # קדימה (בחמדנות, עם חזרה של צעד אחד): [(j, גרסה, התחלה)] + ההמתנות [(j, זמן, משך)] וזמן ההגעה לסוף; None — אין
    n = len(SP_); plan = []; waits = []; t = float(t0); mi = 'x'
    for j in range(n):
        sg = SP_[j]; last = j == n - 1; mo_list = ('x',) if last else ('f', 's')
        k = (mi, mo_list[0])
        if _free(sg, k, t): plan.append((j, k, t)); t += sg['d'][k]; mi = 'f' if not last else 'x'; continue
        # צריך לחכות לפני הקטע הזה: בנקודה שבתחילתו
        if mi == 'f':
            pj, pk, pt = plan.pop(); pk2 = (pk[0], 's')
            if not _free(SP_[pj], pk2, pt): return None
            ta = pt + SP_[pj]['d'][pk2]; cs = SP_[pj]['ncs']; mi = 's'; plan.append((pj, pk2, pt))
        else:
            ta = t; cs = n0cs if j == 0 else SP_[j - 1]['ncs']
        if cs is None: return None
        got = None
        for tw in range(int(math.ceil(ta)), int(math.ceil(ta)) + WSEG):
            if not seg_free(cs, ta, tw): break
            for mo in mo_list:
                k = (mi, mo)
                if _free(sg, k, tw): got = (k, tw); break
            if got: break
        if not got: return None
        k, tw = got; waits.append((j, ta, tw - ta)); plan.append((j, k, tw)); t = tw + sg['d'][k]; mi = 'x' if last else ('f' if k[1] == 'f' else 's')
        if not last and k[1] == 's':
            # הקטע הזה מסתיים בעצירה (נבחר כי בתנועה לא היה פנוי): ההמתנה הבאה תחושב בצעד הבא
            pass
    return plan, waits, t
def seg_legs(a, SP_, plan, waits):
    # מוסיף לשחקן את הרגליים: הקטעים בגרסה שנבחרה, וההמתנות — רגל איטית מאוד (חצי פיקסל), כדי שמבנה הרגליים לא ישתנה (g77TvLegIx)
    W = {j: (ta, d) for j, ta, d in waits}
    for j, k, t0 in plan:
        if j in W and W[j][1] > 1e-6:
            ta, d = W[j]; q = SP_[j]['seg'][0]; h = SP_[j - 1]['h'] if j > 0 else math.atan2(SP_[j]['seg'][1][1] - q[1], SP_[j]['seg'][1][0] - q[0])
            q2 = [q[0] + .5 * math.cos(h), q[1] + .5 * math.sin(h)]
            if j == 0 and a.legs and a.legs[-1].get('h') is not None:   # בתחילת ההסעה — המתנת המנועים מתארכת
                a.legs[-1]['t1'] = round(t0, 2)
            else:
                a.legs.append(dict(p=[list(q), q2], t0=round(ta, 2), t1=round(t0, 2), v0=round(.5 / d, 4), v1=round(.5 / d, 4), r=0, z0=0, z1=0, f=1))
        src = SP_[j]['var'][k]
        for g in src.legs:
            h = dict(g); h['t0'] = round(g['t0'] + t0, 2); h['t1'] = round(g['t1'] + t0, 2); a.legs.append(h)
    return a
# ---------------------------------------------------------------- החיפוש עם המתנות בדרך (aoPlanG של הישן: נחיתה ← עמידה ← יציאה, עם המתנות בתור)
def _pre(a, t1):
    x = M.Actor(a.id, 'ac', a.model, a.home, a.L, a.W); x.legs = [dict(g) for g in a.legs if g['t1'] <= t1 + 1e-6]; x.t = t1; return x
def plan_flight2(Wd, sid, ac, al, phase=0, accept=None, links=('A1', 'A2'), exits=('A3', 'A2')):
    smask = np.zeros(NC, dtype=np.uint8); mp = MINPARK.get(ac, 300); DEP = []; ARR = []; why0 = []
    for ln in links:
        if ln == 'A2' and not can_a2(ac): continue
        A = dep1(sid, ac, ln)
        if A is None or not hasattr(A, 'taxiP'): continue
        if static_hit(Wd, A, 0, A.t, sid): why0.append('dep ' + ln); continue
        B2 = dep2(ac, ln)
        if static_hit(Wd, B2, 0, B2.t, sid): continue
        pre = _pre(A, A.t_taxi0); q0 = pre.legs[-1]['p'][-1]; h0 = pre.legs[-1].get('h', W_)
        n0cs = free_prefix(Wd.occ, hold_cells([q0[0], q0[1], h0, 0, 1], ac), smask)
        SP_ = seg_prepare(Wd, seg_plan(sid, ac, A.taxiP, 8, 18), ac, smask)
        qh = A.taxiP[-1]; hcs = free_prefix(Wd.occ, hold_cells([qh[0], qh[1], N_, 0, 1], ac), smask)
        if hcs is None: continue
        DEP.append(dict(ln=ln, kd='d27' if ln == 'A3' else 'd9', pre=pre, dpre=pre.t, cpre=shifts_conflict(Wd.occ, template(pre, 0, pre.t), 0), n0cs=n0cs, SP=SP_, B=B2, d2=B2.t,
                        c2=shifts_conflict(Wd.occ, template(B2, 0, B2.t), 0), w2=rwy_wins_rel(B2, 0, B2.t), qh=qh, hcs=hcs))
    for ex in exits:
        if ex in ('A2', 'A2r') and ac in HEAVY and ac != 'AC-LG-01': continue
        C, _ = arr1(sid, ac, ex)
        if C is None or not hasattr(C, 'taxiP'): continue
        if static_hit(Wd, C, 0, C.t, sid): why0.append('arr ' + ex); continue
        pre = _pre(C, C.t_taxi0); stop = C.taxiP[-1]
        pcs = free_prefix(Wd.occ, hold_cells([stop[0], stop[1], S_, 0, 0], ac), smask)
        if pcs is None or static_hit(Wd, still(ac, stop, S_), 0, 0, sid): continue
        SPa = seg_prepare(Wd, seg_plan(sid, ac, C.taxiP, 70, .5), ac, smask)
        ARR.append(dict(ex=ex, kd='a27' if ex.endswith('r') else 'a9', pre=pre, dpre=pre.t, cpre=shifts_conflict(Wd.occ, template(pre, 0, pre.t), 0), SP=SPa, w3=rwy_wins_rel(pre, 0, pre.t), stop=stop, pcs=pcs))
    if not DEP or not ARR: return None, 'נוגע במה שחונה קבוע (' + ', '.join(why0) + ')'
    opts = []; order = [(phase + k) % N for k in range(N)]
    for rank, s0 in enumerate(order):
        for dp in DEP:
            if dp['cpre'][s0]: continue
            r = seg_walk(dp['SP'], s0 + dp['dpre'], dp['n0cs'])
            if not r: continue
            plan, waits, th = r; tg0 = int(math.ceil(th + 4 - 1e-6)); wsum = sum(w[2] for w in waits)
            for tg in range(tg0, tg0 + WMAX):
                if not seg_free(dp['hcs'], th, tg): break
                if dp['c2'][tg % N]: continue
                ww = [tg + dp['w2'][0][0], tg + dp['w2'][0][1]]
                if not rwy_ok(ww, ac, Wd.busy, kd=dp['kd']): continue
                opts.append((tg - th + wsum, rank, s0, dp, plan, waits, th, tg, ww)); break
    opts.sort(key=lambda o: (round(o[0] / 8), o[1])); tries = 0; DG = dict(pre=0, rwy=0, walk=0, park=0)
    for wtot, rank, s0, dp, plan, waits, th, tg, ww in opts:
        tair = tg + dp['d2']; got = None
        for ar in ARR:
            for sa in range(int(math.ceil(tair)), int(s0 + T - mp - ar['dpre'] - 30) + 1):
                if ar['cpre'][sa % N]: DG['pre'] += 1; continue
                wa = [sa + ar['w3'][0][0], sa + ar['w3'][0][1]]
                if not rwy_ok(wa, ac, Wd.busy + [[ww[0], ww[1], ac, dp['kd']]], kd=ar['kd']): DG['rwy'] += 1; continue
                r = seg_walk(ar['SP'], sa + ar['dpre'], None)
                if not r: DG['walk'] += 1; continue
                pla, wta, ob = r
                if s0 + T - ob < mp or not seg_free(ar['pcs'], ob, s0 + T) or not seg_free(ar['pcs'], s0, s0 + .01): DG['park'] += 1; continue
                got = (sa, ar, pla, wta, ob, wa); break
            if got: break
        if not got: continue
        sa, ar, pla, wta, ob, wa = got
        a = M.Actor('FL-' + sid, 'ac', ac, sid, D.ACT[ac][0], D.ACT[ac][1]); a.airline = al
        for g in dp['pre'].legs: h = dict(g); h['t0'] = round(g['t0'] + s0, 2); h['t1'] = round(g['t1'] + s0, 2); a.legs.append(h)
        seg_legs(a, dp['SP'], plan, waits)
        a.legs.append(dict(p=[list(dp['qh'])], t0=round(th, 2), t1=round(tg, 2), h=round(N_, 4), f=1))
        for g in dp['B'].legs: h = dict(g); h['t0'] = round(g['t0'] + tg, 2); h['t1'] = round(g['t1'] + tg, 2); a.legs.append(h)
        for g in ar['pre'].legs: h = dict(g); h['t0'] = round(g['t0'] + sa, 2); h['t1'] = round(g['t1'] + sa, 2); a.legs.append(h)
        seg_legs(a, ar['SP'], pla, wta)
        a.legs.append(dict(p=[list(ar['stop'])], t0=round(ob, 2), t1=round(s0 + T, 2), h=round(S_, 4), f=0))
        cand = dict(s0=s0, w=tg - th, wq=sum(w[2] for w in waits), wa=sum(w[2] for w in wta), tg=tg, sa=sa, ob=ob, park=s0 + T - ob, rw=[ww, wa], kd=[dp['kd'], ar['kd']], ln=dp['ln'], ex=ar['ex'])
        tries += 1
        if accept is None or accept(a): return dict(a=a, best=cand, d=(0, dp['d2'], 0)), 'נכנס'
        if tries > 40: break
    return None, 'אין זמן פנוי (%d אפשרויות יציאה, %d נבדקו; נחיתה: %s)' % (len(opts), tries, DG)
# ---------------------------------------------------------------- TG-C (גרר המשא עם העגלות — s15_sim.extra) — לפי חלון העמידה של טיסת C1, באותן דרכים
def tgc_trips(home, t1, t2):
    trs = []
    for t0 in (t1, t2):
        if t0 is None: continue
        v = M.Actor('TG-C', 'veh', 'LV-BT-01', '', 45, 22); v.t = t0
        P1 = [home, [home[0], 525], [5200, 525], [5200, 600]]; P2 = [[5200, 600], [5200, 710], [5470, 710], [5470, 772]]; P3 = [[5470, 772], [5470, 710], [5200, 710], [5200, 525], [home[0], 525], home]
        v.move(P1, 25, 5); v.wait([5200, 600], N_, v.t + 50, flags=8); v.move(P2, 25, 5); v.wait([5470, 778], S_, v.t + 40, flags=8); v.move(P3, 25, 5); trs.append(v.legs)
    return trs
def plan_tgc2(Wd, a, home, c2win):
    # TG-C (גרר המשא עם העגלות): ביקור ב-C1 בתוך העמידה של הטיסה החדשה ב-C1, וביקור ב-C2 בתוך העמידה של FL-C2 — אותן דרכים של s15_sim.extra;
    # אם שני הביקורים נכנסים בנסיעה אחת (C1 ואז C2, כמו היום) — אחת; אחרת שתי נסיעות (AF של הישן: משימה אחרי משימה), כל אחת נבדקת מול המטוסים והרכבים
    p0, p1 = park_window(a); OV = getattr(Wd, 'occV', None); T0 = T
    def legs_c1(t0):
        v = M.Actor('TG-C', 'veh', 'LV-BT-01', '', 45, 22); v.t = t0
        v.move([home, [home[0], 525], [5200, 525], [5200, 600]], 25, 5); v.wait([5200, 600], N_, v.t + 50, flags=8); v.move([[5200, 600], [5200, 525], [home[0], 525], home], 25, 5); return v.legs
    def legs_c2(t0):
        v = M.Actor('TG-C', 'veh', 'LV-BT-01', '', 45, 22); v.t = t0
        v.move([home, [home[0], 525], [5350, 525], [5350, 710], [5470, 710], [5470, 772]], 25, 5); v.wait([5470, 778], S_, v.t + 40, flags=8)
        v.move([[5470, 772], [5470, 710], [5350, 710], [5350, 525], [home[0], 525], home], 25, 5); return v.legs
    def free(tr, useV=True):
        I, C = trip_template(tr, 90, 30)   # עם העגלות (גרר משא — הרכבת המצוירת ארוכה מהטרקטור; BL-C × TG-C ב-try7411)
        if not len(I): return True
        ix = (int(round(tr[0]['t0'] / DT)) + I) % N
        return not (Wd.occA.o[ix, C].any() or (useV and OV is not None and OV.o[ix, C].any()))
    def inwin(t, w):
        return any(w[0] <= t + k and t + k <= w[1] for k in (-T0, 0, T0))
    got1 = None
    for useV in (True, False):
        for k in range(0, 300, 5):
            t0 = p0 + 10 + k; tr = legs_c1(t0); w8 = [g for g in tr if g.get('f') == 8][0]
            if w8['t1'] > p1 - 20: break
            if free(tr, useV): got1 = tr; break
        if got1: break
    got2 = None
    for useV in (True, False):
        for k in range(0, 720, 5):
            t0 = c2win[0] + 10 + k; tr = legs_c2(t0); w8 = [g for g in tr if g.get('f') == 8][0]
            if not (inwin(w8['t0'], c2win) and inwin(w8['t1'], c2win)): continue
            if got1 and not trips_ok([got1], tr): continue
            if free(tr, useV): got2 = tr; break
        if got2: break
    # עוד נסיעה ל-C2 שמכסה את החזרה של PT-C הביתה (בבית — הכיס של TG-C על הדרך שלו; כמו בלוח של היום: שני ביקורים במחזור)
    got3 = None
    for (c0, c1) in COVER_TGC:
        for useV in (True, False):
            for k in range(0, 200, 5):
                t0 = c1 - k; tr = legs_c2(t0)
                if not (tr[0]['t0'] <= c0 - 3 and tr[-1]['t1'] >= c1 + 3): continue
                if not trips_ok([x for x in (got1, got2) if x], tr): continue
                if free(tr, useV): got3 = tr; break
            if got3: break
    out = [x for x in (got1, got2, got3) if x]
    return out or None
COVER_TGC = [(525.0, 556.0)]   # PT-C (074p — FL-C2) חוזר הביתה ליד הכיס של TG-C (נמדד ב-try7407: ‏540)
def plan_tgc(Wd, a, home):
    p0, p1 = park_window(a); pkm = np.zeros(NC, dtype=np.uint8)
    for k in range(0, 120, 6):
        t1 = p0 + 20 + k; tr1 = tgc_trips(home, t1, None)[0]; d = tr1[-1]['t1'] - tr1[0]['t0']
        t2 = tr1[-1]['t1'] + 10
        trs = tgc_trips(home, t1, t2 if t2 + d < p1 - 30 else None)
        if trs[-1][-1]['t1'] > p1 - 30: continue
        ok = True
        for tr in trs:
            I, C = trip_template(tr)
            if len(I) and Wd.occA.o[(int(round(tr[0]['t0'] / DT)) + I) % N, C].any(): ok = False; break
        if ok: return trs
    return None
# ---------------------------------------------------------------- C14.07 ("בחדש דברים קפואים / איטיים לעומת הישן"): שדרוג הטיסות של היום לפרופיל של הישן
# הדחיפה (apttPush), ההסעה (apttTaxi) והכניסה למסלול (apttTakeoff) — כמו הטיסות החדשות; הזמנים שהמערכות האחרות בנויות עליהם לא זזים:
# הדחיפה מתחילה באותה שנייה, ההמראה באותה שנייה (ההמתנה — בקו ההמתנה במקום הסעה איטית), הגישה והנגיעה באותה שנייה; ההסעה פנימה מהירה יותר — העצירה
# בעמדה מוקדמת (העמידה מתארכת, כל רכבי השירות שבתוכה נשארים בתוכה). נבדק במדויק מול כל השאר; אם נוגע — נשאר כמו שהוא
def upgrade_base(Wd, f, exits=('A3', 'A2'), skip_tug={}):
    ac = f.model; sid = f.home; L = f.legs; s0 = L[0]['t0']
    hold = [g for g in L if g.get('h') is not None and g.get('f') == 1 and abs(g['p'][0][1] - (M.HOLD + 40)) < 1.5]
    air = [g for g in L if g.get('f') == 4]
    if not hold or len(air) < 2: return None, 'אין מבנה מוכר'
    tg = hold[-1]['t1']; sa = air[1]['t0']; ln = 'A1' if abs(hold[-1]['p'][0][0] - A1) < 2 else ('A2' if abs(hold[-1]['p'][0][0] - A2) < 2 else None)
    if ln is None: return None, 'קו המתנה לא מוכר'
    A = dep1(sid, ac, ln)
    if A is None: return None, 'אין דחיפה'
    if s0 + A.t > tg - 2: return None, 'הדחיפה המהירה לא מקדימה'
    s0o = s0; s0late = round(tg - A.t - 2, 2)   # בין הדחיפה בזמן של היום (ממתין בקו ההמתנה) לדחיפה מאוחרת (מגיע לקו בזמן) — הראשון בלי חפיפה
    B2 = dep2(ac, ln); qh = A.legs[-1]['p'][-1]; tug = skip_tug.get(f.id, ())
    why = []
    for s0 in sorted(set([s0late] + [round(s0o + k * 3, 2) for k in range(int((s0late - s0o) / 3) + 1)]), key=lambda x: -x):
     for ex in exits:
         C3, _ = arr1(sid, ac, ex)
         if C3 is None: continue
         ob = sa + C3.t
         if ob > L[-1]['t0'] + .01:
                 if s0 == s0late: why.append(ex + ' מאוחר')
                 continue
         a = M.Actor(f.id, 'ac', ac, sid, f.L, f.W); a.airline = getattr(f, 'airline', None)
         for g in A.legs: h = dict(g); h['t0'] = round(g['t0'] + s0, 2); h['t1'] = round(g['t1'] + s0, 2); a.legs.append(h)
         a.legs.append(dict(p=[list(qh)], t0=round(s0 + A.t, 2), t1=round(tg, 2), h=round(N_, 4), f=1))
         for g in B2.legs: h = dict(g); h['t0'] = round(g['t0'] + tg, 2); h['t1'] = round(g['t1'] + tg, 2); a.legs.append(h)
         for g in C3.legs: h = dict(g); h['t0'] = round(g['t0'] + sa, 2); h['t1'] = round(g['t1'] + sa, 2); a.legs.append(h)
         a.legs.append(dict(p=[list(C3.legs[-1]['p'][-1])], t0=round(ob, 2), t1=round(s0 + T, 2), h=round(S_, 4), f=0))
         if static_hit(Wd, a, s0, s0 + T, sid): why.append(ex + ' חונה'); continue
         h = exact_flight(Wd, a, m=0.0, skip_ids={f.id} | set(tug), vkv=1.0)
         if h:
                 if s0 == s0late: why.append(ex + ' ' + str(h))
                 continue
         a.s0o = s0o
         old_w = flight_rwy_wins(f); new_w = flight_rwy_wins(a)
         others = [b for b in Wd.busy if not any(abs(b[0] - w[0]) < .01 and abs(b[1] - w[1]) < .01 for w in old_w)]
         if not all(rwy_ok(w, ac, others, kd=win_kind(a, w)) for w in new_w): why.append(ex + ' המסלול'); continue
         po = [g for g in L if g.get('r') and g.get('f') == 2]; pn = [g for g in A.legs if g.get('r') and g.get('f') == 2]
         return a, 'שודרג: הדחיפה %.0f→%.0f ש׳ (יוצא ב-%.0f במקום %.0f), מהעמדה עד הקו %.0f→%.0f ש׳, העצירה בעמדה %.0f→%.0f (%s) — העמידה %.0f→%.0f ש׳ · המסלול %s → %s' % (
             (po[-1]['t1'] - s0o) if po else 0, pn[-1]['t1'] if pn else 0, s0 % T, s0o % T, hold[-1]['t0'] - s0o, A.t, L[-1]['t0'], ob, ex,
             s0o + T - L[-1]['t0'], s0 + T - ob, [round(w[1] - w[0], 1) for w in old_w], [round(w[1] - w[0], 1) for w in new_w])
    return None, ' · '.join(why) or 'אין יציאה'
# ---------------------------------------------------------------- קווי העצירה לפי סוג (fieldcalc, ‏stands_matrix.json — 17.11 10:54): עמדה גדולה מקבלת סוג קטן יותר,
# והמטוס עוצר "אחורה" (shift פיקס׳ מקו האף של העמדה), כך שהכנף לא מעל כיס הציוד שליד האף. הבעלים 11:10: "העמדות הגדולות הם לא רק למטוסי ענק"
SHIFT = {}
try:
    _SM = json.load(open('/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldcalc/tools/stands_matrix.json', encoding='utf-8'))
    for _sid, _st in _SM['stands'].items():
        for _m, _r in _st.get('row', {}).items():
            if _r.get('ok') and _r.get('shift'): SHIFT[(_sid, _m)] = float(_r['shift'])
    FITS = {(_sid, _m) for _sid, _st in _SM['stands'].items() for _m, _r in _st.get('row', {}).items() if _r.get('ok')}
except Exception as _e:
    FITS = None
_ng0 = M.ng_stop
def _ng_shift(sid, ac):
    p = _ng0(sid, ac); sh = SHIFT.get((sid, ac), 0.0)
    return [p[0], p[1] - sh] if sh else p
M.ng_stop = _ng_shift
# ---------------------------------------------------------------- (הבעלים 12:40) מגוון סוגים בכל עמדה: גרסה של טיסה לסוג אחר — אותה המראה ואותה נגיעה (המסלול לא משתנה),
# הדחיפה וההסעה לפי הסוג (הסוג נכנס בעמדה לפי stands_matrix של fieldcalc — FITS / SHIFT), נבדקת במדויק מול כל השאר. לסבב של הסוגים בעמדה (מחזור אחרי מחזור)
def variant_of(Wd, f, ac, exits=('A3', 'A2'), skip=()):
    sid = f.home; L = f.legs
    if FITS is not None and (sid, ac) not in FITS: return None, 'לא נכנס בעמדה'
    hold = [g for g in L if g.get('h') is not None and g.get('f') == 1 and abs(g['p'][0][1] - (M.HOLD + 40)) < 1.5]
    air = [g for g in L if g.get('f') == 4]
    if not hold or len(air) < 2: return None, 'אין מבנה מוכר'
    tg = hold[-1]['t1']; sa = air[1]['t0']; ln = 'A1' if abs(hold[-1]['p'][0][0] - A1) < 2 else ('A2' if abs(hold[-1]['p'][0][0] - A2) < 2 else None)
    if ln is None or (ln == 'A2' and not can_a2(ac)): return None, 'קו ההמתנה לא מתאים לסוג'
    A = dep1(sid, ac, ln)
    if A is None: return None, 'אין דחיפה'
    B2 = dep2(ac, ln); qh = A.legs[-1]['p'][-1]; why = []
    for s0 in [round(tg - A.t - 2 - k * 3, 2) for k in range(0, 30)]:
        for ex in exits:
            if ex == 'A2' and ac in HEAVY and ac != 'AC-LG-01': continue
            C3, _ = arr1(sid, ac, ex)
            if C3 is None: continue
            ob = sa + C3.t
            if s0 + T - ob < MINPARK.get(ac, 300): continue
            a = M.Actor(f.id, 'ac', ac, sid, D.ACT[ac][0], D.ACT[ac][1])
            for g in A.legs: h = dict(g); h['t0'] = round(g['t0'] + s0, 2); h['t1'] = round(g['t1'] + s0, 2); a.legs.append(h)
            a.legs.append(dict(p=[list(qh)], t0=round(s0 + A.t, 2), t1=round(tg, 2), h=round(N_, 4), f=1))
            for g in B2.legs: h = dict(g); h['t0'] = round(g['t0'] + tg, 2); h['t1'] = round(g['t1'] + tg, 2); a.legs.append(h)
            for g in C3.legs: h = dict(g); h['t0'] = round(g['t0'] + sa, 2); h['t1'] = round(g['t1'] + sa, 2); a.legs.append(h)
            a.legs.append(dict(p=[list(C3.legs[-1]['p'][-1])], t0=round(ob, 2), t1=round(s0 + T, 2), h=round(S_, 4), f=0))
            if static_hit(Wd, a, s0, s0 + T, sid): why.append('חונה'); continue
            h = exact_flight(Wd, a, m=0.0, skip_ids={f.id} | set(skip), vkv=1.0)
            if h: why.append(str(h)); continue
            ow = flight_rwy_wins(f); nw = flight_rwy_wins(a)
            others = [b for b in Wd.busy if not any(abs(b[0] - w[0]) < .01 and abs(b[1] - w[1]) < .01 for w in ow)]
            if not all(rwy_ok(w, ac, others, kd=win_kind(a, w)) for w in nw): why.append('המסלול'); continue
            return a, 'גרסה %s: הדחיפה ב-%.0f, העמידה %.0f ש׳ (%s)' % (ac[3:5], s0 % T, s0 + T - ob, ex)
    return None, (' · '.join(sorted(set(why)))[:160] or 'אין')
