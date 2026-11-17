#!/usr/bin/env python3
# fc_calc2.py — fieldcalc 17.11 (אחרי הבקר, planrev/fieldcalc.txt; החלטת המתאם 07:46): תוספות לחישוב, על אותו לוח (fc_result.json) ואותן פונקציות (fc_calc.py):
#  (א) עמדות הכבודה לפי השיוך בפועל — תור לכל עמדה, וחיפוש של שיוך שבו אף עמדה לא מעל 60% (במקום "5 שרתים משותפים")
#  (ב) דרכי השירות: מי חוצה את B / את C, איפה, כמה פעמים במחזור, והתפוסה של המטוסים בנקודות החצייה (הכלל "מטוס קודם")
#  (ג) מי חונה בדרום (בסיס הצי הדרומי) ומי בצפון — לפי העבודות של כל עמדה
#  (ד) מחזור התחזוקה — מטוס מהלוח נכנס להאנגר, המתוקן חוזר ללוח: מי מחליף את מי, באיזו עמדה, באיזה חלון של B / C
#  (ה) העתודה מעבר ל-90: מפרץ המתנה באמצע B (ותרחיש B2) — במתזמן של fc_calc
#  (ו) אזור ההדף של R3 בלילה מול בסיס הצי הדרומי; כיוון המסלול (09 / 27) מול B; P6 בדחיפה מול היציאה של BH-5
#  (ז) המהירות של רכבי השירות מול הישן (מהמדידה במשחק — s15k_fleet) ומשכי הפעולות
# קוד יציאה 1 אם אחד התנאים לא מתקיים (עמדה מעל 60%, חנייה באזור ההדף, נתיב שירות שחוצה את B).
import os, sys, json, math, itertools, importlib.util, collections as C
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('fc', os.path.join(HERE, 'fc_calc.py')); FC = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']; spec.loader.exec_module(FC); sys.argv = _a
R = json.load(open(os.path.join(HERE, 'fc_result.json'), encoding='utf-8'))
T = FC.T; FL = R['schedule']; D = FC.D; ST = FC.ST; MATRIX = FC.MATRIX; AC = FC.AC
OUT = {}; FAILS = []
def cyc(t): return t % T

# ---------------------------------------------------------------- (א) עמדות הכבודה — לפי השיוך
HX = {h['id']: (h['r'][0] + h['r'][2]) / 2 for h in FC.HALLS}
PASS_X = 7909                      # AIR-PASS — המעבר מתחת לטרמינל (x 7865–7953): הדרך של רכבות הכבודה מהדרום אל הצד הצפוני של אגף השערים
def visits():
    V = []
    for f in FL:
        a = AC[f['model']]
        if not a['bag'] or a['cls'] in ('GA', 'EXEC', 'AMPH'): continue
        ob = f['onblock']; half = MATRIX[f['model']]['bags']['d'] / 2; n = MATRIX[f['model']]['bags']['n']
        for j in range(n):
            dA = FC.HALL['prep'] + FC.HALL['entry'] + a['bag'] / n * FC.HALL['cad'] + FC.HALL['exit']
            V.append(dict(stand=f['stand'], train=j, kind='dep', t=ob + 25 - 35 - dA + j * 6, dur=dA))
            V.append(dict(stand=f['stand'], train=j, kind='arr', t=ob + 25 + 2 * half + 35 + j * 6, dur=dA))
    return V
def q1(Vs):
    ev = sorted([dict(v, t=v['t'] + c * T) for v in Vs for c in range(3)], key=lambda v: v['t']); free = 0.0; W = []; busy = 0
    for v in ev:
        st = max(v['t'], free); free = st + v['dur']
        if T <= v['t'] < 2 * T: W.append(st - v['t']); busy += v['dur']
    return dict(visits=len(Vs), util=round(busy / T * 100, 1), wait_mean=round(sum(W) / len(W), 1) if W else 0, wait_max=round(max(W), 1) if W else 0)
def dist(stand, hid):
    sx = ST[stand]['cx']
    return abs(HX[hid] - PASS_X) + 1500 if stand.startswith('R') else abs(HX[hid] - sx)
V = visits()
_p6 = next(f for f in FL if f['stand'] == 'P6')
P6BLK = [(cyc(_p6['push'] - 10), cyc(_p6['push'] - 10) + 10 + 40 + 20, 'דחיפה'), (cyc(_p6['onblock'] - 45), cyc(_p6['onblock'] - 45) + 45 + 10, 'כניסה')]
def p6_wait(v):
    ex = cyc(v['t'] + v['dur']); w = 0
    for a, b, _ in P6BLK:
        for k in (-T, 0, T):
            if a + k <= ex <= b + k: w = max(w, b + k - ex)
    return w
units = sorted({(v['stand'], v['train']) for v in V})
cand = {u: sorted(HX, key=lambda h: dist(u[0], h))[:3] for u in units}
best = None
for combo in itertools.product(*[cand[u] for u in units]):
    A = dict(zip(units, combo)); per = C.defaultdict(list)
    for v in V: per[A[(v['stand'], v['train'])]].append(v)
    Q = {h: q1(per.get(h, [])) for h in HX}
    mx = max(q['util'] for q in Q.values()); wm = max(q['wait_max'] for q in Q.values()); dsum = sum(dist(u[0], A[u]) for u in units)
    pw = sum(p6_wait(v) for v in per.get('BH-5', []))
    key = (round(mx / 5), wm > 30, pw > 0, sum(q['wait_mean'] * q['visits'] for q in Q.values()) + pw, dsum)
    if best is None or key < best[0]: best = (key, A, Q)
_, A, Q = best
def assign_of(A0):
    per = C.defaultdict(list)
    for v in V: per[A0[(v['stand'], v['train'])]].append(v)
    return {h: q1(per.get(h, [])) for h in HX}
old = {}
for u in units:
    s = u[0]; old[u] = 'BH-1' if s in ('P1', 'P2') else 'BH-2' if s == 'P3' else 'BH-3' if s == 'P4' else 'BH-4' if s == 'P5' else 'BH-5'
Qold = assign_of(old)
OUT['halls_assign'] = dict(
    before=dict(assign={'%s/%d' % u: old[u] for u in units}, per=Qold, max=max(q['util'] for q in Qold.values())),
    after=dict(assign={'%s/%d' % u: A[u] for u in units}, per=Q, max=max(q['util'] for q in Q.values()), wait_max=max(q['wait_max'] for q in Q.values())),
    rule='כל רכבת לעמדה שלה (לפי השיוך), תור של רכבת אחת בכל עמדה; R — דרך המעבר מתחת לטרמינל (AIR-PASS, ‏x 7909), לכן העמדות הקרובות למעבר')
if OUT['halls_assign']['after']['max'] > 60 or OUT['halls_assign']['after']['wait_max'] > 30: FAILS.append('עמדת כבודה מעל 60% או המתנה מעל 30 ש׳')

# ---------------------------------------------------------------- (ב) דרכי השירות והחצייה של B / C
SV = {s['id']: s['rect'] for s in D['service']}
TWB, TWC = D['twb'], D['twc']
def rint(a, b): return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
crossB = [k for k, r in SV.items() if rint(r, TWB)]
crossC = [k for k, r in SV.items() if rint(r, TWC)]
if crossB: FAILS.append('דרך שירות חוצה את B: ' + ', '.join(crossB))
XC = {'XC_E': (SV['AIR-XC_E'][0] + SV['AIR-XC_E'][2]) / 2, 'XC_W': (SV['AIR-XC_W'][0] + SV['AIR-XC_W'][2]) / 2}
HALFW = {'XC_E': (SV['AIR-XC_E'][2] - SV['AIR-XC_E'][0]) / 2, 'XC_W': (SV['AIR-XC_W'][2] - SV['AIR-XC_W'][0]) / 2}
TBX = 9400
def c_windows(xc, hw):
    """החלונות שבהם מטוס על C בנקודת החצייה (גוף + חצי מוטה + 3 מ׳), מהלוח: לדרום — מ-9400 מערבה עד העמדה; לצפון — הפוך."""
    W = []
    for f in FL:
        for key, d in (('link_in', 'S'), ('link_out', 'N')):
            li = f.get(key)
            if not li: continue
            t0, t1 = li['C']; t1 = t1 if t1 >= t0 else t1 + T; cx = ST[f['stand']]['cx']
            lo, hi = min(cx, TBX), max(cx, TBX); span = FC.DIM[f['model']][1] / 2 + 30 + hw
            if xc + span < lo or xc - span > hi: continue
            def x_at(t): u = (t - t0) / max(1e-6, t1 - t0); return TBX + (cx - TBX) * u if d == 'S' else cx + (TBX - cx) * u
            occ = [t for t in [t0 + i * .5 for i in range(int((t1 - t0) / .5) + 1)] if abs(x_at(t) - xc) < span]
            # גם בכניסה לעמדה / ביציאה ממנה — המטוס בקצה C (cx) עוד כמה שניות: כלול ב-t0 / t1
            if occ: W.append((cyc(occ[0]), cyc(occ[0]) + (occ[-1] - occ[0]) + .5, f['stand'], d))
    return W
def merged(W):
    segs = sorted((a, b) for a, b, *_ in W); M = []
    for a, b in segs:
        if M and a <= M[-1][1]: M[-1][1] = max(M[-1][1], b)
        else: M.append([a, b])
    return M
cross = {}
for k in XC:
    W = c_windows(XC[k], HALFW[k]); M = merged(W); busy = sum(b - a for a, b in M)
    cross[k] = dict(x=XC[k], windows=[[round(a, 1), round(b, 1), s, d] for a, b, s, d in W], busy=round(busy, 1), util=round(busy / T * 100, 1),
                    wait_mean=round(sum((b - a) ** 2 for a, b in M) / (2 * T), 2), wait_max=round(max((b - a for a, b in M), default=0), 1))
# כמה חציות של C במחזור — שתי אפשרויות: (1) כל הצי בבסיס של היום (צפון / אמצע), (2) עם בסיס הצי הדרומי (H4)
SOUTH = FC.SOUTH
jobs = [j for f in FL for j in FC.svc_jobs(f)]
south_jobs = [j for j in jobs if j[5] in SOUTH]
def crossings(south_base):
    n = C.Counter()
    for vt, r, d, p, key, s in south_jobs:
        if south_base and vt not in ('BT', 'FT'):   # מהבסיס הדרומי — בלי חצייה; רכבות הכבודה (לאולמות בצפון) ומכליות (חוות הדלק) — כן
            continue
        n[vt] += 2                                   # הלוך דרך XC_E (דרומה), חזור דרך XC_W (צפונה)
    if south_base: n['FTs'] += 2                     # המתדלק הקטן של הדרום — מילוי בחוות הדלק פעם במחזור
    n['LIMO'] += 2 * sum(1 for f in FL if AC[f['model']]['cls'] == 'EXEC')   # הלימוזינה של המנהלים: G-STAFF → XC_E → GA1 / R3 → XC_W
    return n
c_today, c_south = crossings(False), crossings(True)
XT = (TWC[3] - TWC[1] + 44) / FC.VEH_V + 2             # זמן החצייה של רכב (150 פיקס׳ + 2 × 22 — רוחב הדרך — ב-40 פיקס׳/ש׳ + 2 ש׳ האצה)
OUT['service_roads'] = dict(
    crossB=crossB, crossC=crossC, rule='מטוס קודם: הרכב עוצר בקו העצירה של הדרך (2 מ׳ מהשוליים של C) כשמטוס בחלון של נקודת החצייה, וממשיך כשהחלון נגמר',
    route_south='הבסיס (AIR-BASE-8 / הכיסים) → AIRROAD_W → BASE_ROAD (מזרחה) → XC_E — חוצה את C ב-x %d → TAIL_ROAD (מערבה) → העמדה; חזרה: TAIL_ROAD → XC_W — חוצה את C ב-x %d → AIRROAD_W' % (XC['XC_E'], XC['XC_W']),
    route_bags_R='R1 / R2 → TAIL_ROAD → XC_W (חוצה את C) → AIRROAD_W → AIR-PASS (מתחת לטרמינל) → הדרך הצפונית של אגף השערים (y 820–864) → העמדה → AIR-PASS → BASE_ST → BASE_E → BASE_ROAD → XC_E (חוצה את C) → TAIL_ROAD → R',
    cross=cross, per_cycle_today=dict(c_today), per_cycle_south=dict(c_south), n_today=sum(c_today.values()), n_south=sum(c_south.values()), veh_cross_s=round(XT, 1),
    veh_occ_today=round(sum(c_today.values()) * XT / 2 / T * 100, 1), veh_occ_south=round(sum(c_south.values()) * XT / 2 / T * 100, 1))

# ---------------------------------------------------------------- (ג) מי חונה בדרום ומי בצפון
def kmin_of(J): return FC.kmin(J) if J else 0
byv = C.defaultdict(list)
for j in jobs: byv[j[0]].append(j)
split = {}
for vt, J in sorted(byv.items()):
    Js = [j for j in J if j[5] in SOUTH]; Jn = [j for j in J if j[5] not in SOUTH]
    ks, kn = kmin_of(Js), kmin_of(Jn)
    if vt in ('BT', 'FT'): ks_base = 0      # רכבות הכבודה של R — מהאולמות בצפון; המכליות — מחוות הדלק (באמצע)
    else: ks_base = ks
    split[vt] = dict(he=FC.VEH_HE.get(vt, vt), south=ks_base, north=kn + (ks if vt in ('BT', 'FT') else 0), total_need=R['fleet'][vt]['need'],
                     south_stands=sorted({j[5] for j in Js}), north_stands=sorted({j[5] for j in Jn}))
OUT['fleet_split'] = dict(rows=split, south_total=sum(v['south'] for v in split.values()), south_spots=28,
                          note='בבסיס הדרומי — רק מי שמשרת את R / GA (גררים, GPU, מדרגות, אוטובוסים, מסוע ל-R2, מתדלק קטן, קייטרינג / מים / שירותים / ניקיון ל-R); השאר — בכיסים של הצפון ובחניון הצי של היום (AIR-BASE-8)')
SOUTH_SPOTS = 28

# ---------------------------------------------------------------- (ד) מחזור התחזוקה
def free_windows(intervals, lo=0):
    M = merged([(a, b) for a, b in intervals]); F = []
    if not M: return [[0, T]]
    for i in range(len(M)):
        a = M[i][1]; b = M[(i + 1) % len(M)][0] + (T if i == len(M) - 1 else 0)
        if b - a > 0: F.append([round(cyc(a), 1), round(cyc(a) + (b - a), 1)])
    return sorted(F, key=lambda w: -(w[1] - w[0]))
Bw = [(cyc(f[k]['B'][0]), cyc(f[k]['B'][0]) + (f[k]['B'][1] - f[k]['B'][0]) % T) for f in FL for k in ('link_in', 'link_out') if f.get(k)]
def Cw_x(x0, x1):    # מטוסים על C בקטע [x0, x1]
    W = []
    for f in FL:
        for key, d in (('link_in', 'S'), ('link_out', 'N')):
            li = f.get(key)
            if not li: continue
            cx = ST[f['stand']]['cx']
            if max(cx, TBX) < x0 or min(cx, TBX) > x1: continue
            t0 = li['C'][0]; t1 = li['C'][1] if li['C'][1] >= t0 else li['C'][1] + T
            W.append((cyc(t0), cyc(t0) + (t1 - t0)))
    return W
TOWV = 30.0      # גרירה קדימה (פיקס׳/ש׳ ≈ 11 קמ״ש), כמו הגרר של R3 אצל fieldfix
HG = {h['id']: h for h in D['base']}
MAINT = []
pool = C.Counter(f['model'] for f in FL)
def tow(name, hangar, models, donor, path, use_B, cx0, cx1):
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:])); dur = L / TOWV + 40     # 20 ש׳ חיבור + 20 ש׳ ניתוק
    occ = Cw_x(cx0, cx1) + (Bw if use_B else []); fw = free_windows(occ)
    fit = next((w for w in fw if w[1] - w[0] >= dur + 10), None)
    f = next(q for q in FL if q['stand'] == donor)
    MAINT.append(dict(hangar=name, hid=hangar, label=HG[hangar]['label'], models=models, in_service=sum(pool[m] for m in models), airframes=sum(pool[m] for m in models) + 1,
                      donor=donor, donor_push=f['push'], donor_onblock=f['onblock'], path_len=round(L), tow_s=round(dur), uses_B=use_B,
                      window=fit, free_longest=fw[0] if fw else None, ok=bool(fit)))
    if not fit: FAILS.append('אין חלון לגרירה של התחזוקה: ' + name)
tow('א׳', 'AIR-BASE-1', ['AC-RJ-01'], 'R1', [(9369, 2300), (9369, 1850), (8661, 1850), (8661, 2300)], False, 8661, 9475)   # מ-R3 (אחרי ההרצה של הלילה) — רק C
tow('ב׳', 'AIR-BASE-2', ['AC-BJ-01', 'AC-CN-01'], 'GA1', [(8450, 1516), (8450, 1850), (7350, 1850), (7350, 2000)], False, 7350, 8552)
tow('ג׳', 'AIR-BASE-3', ['AC-LT-01', 'AC-PR-01'], 'GA2', [(8243, 1538), (8243, 1850), (7507, 1850), (7507, 1990)], False, 7507, 8338)
OUT['maint'] = dict(rows=MAINT, cycle='כל יום משחק — האנגר אחד, לפי הסדר של fieldfix (א׳ → ב׳ → ג׳): בלילה המטוס המתוקן מריץ מנועים ב-R3 (הבדיקה האחרונה אחרי התיקון), '
                    'ובבוקר (04:45) הוא לא חוזר להאנגר אלא נגרר לעמדה של הטיסה שהוא מחליף, בחלון שבו C (ו-B, להאנגר א׳) פנויים; '
                    'המטוס של אותה טיסה — אחרי הנחיתה הבאה — מסיע לרחבת ההאנגר (א׳: מ-A3 דרך B ישר לרחבה, בלי C) ונדחף פנימה. כך בכל רגע: '
                    'מטוס אחד בהאנגר מכל סוג, והלוח לא מאבד טיסה',
                    note='צר-גוף / ‏LG / מטען — לא בהאנגרים של השדה (הם בבסיס של החברה); ‏AC-TP-01 — לא בלוח (fieldfix הוציא אותו מ-R3)')

# ---------------------------------------------------------------- (ה) העתודה: מפרץ המתנה באמצע B
def link_ok_bay(w, L, b2=False):
    lt = ('AC-LT-01', 'AC-PR-01')
    for q in L:
        for seg in ('B', 'C'):
            a0, a1 = w[seg]; b0, b1 = q[seg]
            if seg == 'C' and w['dir'] != q['dir']:
                xs = max(w['x'], q['x']); sub = (FC.TBX - xs) / FC.TAXI_V + 4
                def part(z, t0, t1): return (t0, min(t1, t0 + sub)) if z['dir'] == 'S' else (max(t0, t1 - sub), t1)
                a0, a1 = part(w, a0, a1); b0, b1 = part(q, b0, b1)
            if w['dir'] != q['dir']:
                if seg == 'B':
                    # המפרץ באמצע B (y ~880, צד מזרח): המנוגדים נפגשים רק בחצי אחד — כל חצי נבדק לבד (+3), והמפרץ מחזיק מטוס אחד
                    am, bm = (a0 + a1) / 2, (b0 + b1) / 2
                    wa = [(a0, am), (am, a1)] if w['dir'] == 'S' else [(am, a1), (a0, am)]     # [צפון, דרום]
                    wb = [(b0, bm), (bm, b1)] if q['dir'] == 'S' else [(bm, b1), (b0, bm)]
                    if FC.overlap(wa[0][0], wa[0][1], wb[0][0], wb[0][1], 3) or FC.overlap(wa[1][0], wa[1][1], wb[1][0], wb[1][1], 3): return False
                    continue
                if FC.overlap(a0, a1, b0, b1, 3): return False
            else:
                for k in (-T, 0, T):
                    if abs(a0 - (b0 + k)) < 10 or abs(a1 - (b1 + k)) < 10: return False
                    if (a0 - (b0 + k)) * (a1 - (b1 + k)) < 0: return False
    return True
def grow(link):
    keep = FC.link_ok; FC.link_ok = link
    try:
        mx = list(FC.PLAN); added = []
        extra = FC.EXTRA + [('GA6', 'AC-LT-01', 'GA', 1), ('GA7', 'AC-PR-01', 'GA', 1), ('R3', 'AC-CN-01', 'Executive', 1), ('GA1', 'AC-BJ-01', 'Executive', 1)]
        for x in extra:
            trial = [(a, b, c, (n + 1 if (a, b) == (x[0], x[1]) else n)) for a, b, c, n in mx]
            fl2, miss2, E2, L2 = FC.schedule(trial)
            if not miss2: mx = trial; added.append(x[0])
        fl2, miss2, E2, L2 = FC.schedule(mx)
        return dict(added=added, flights=len(fl2), rwy=FC.rwy_stats(E2), link=FC.link_stats(L2))
    finally:
        FC.link_ok = keep
OUT['reserve'] = dict(base=dict(flights=len(FL), rwy=R['scen']['max']['rwy'], link=R['scen']['max']['link']), bay=grow(link_ok_bay),
                      b2=dict(rwy=R['scen']['b2']['rwy'], link=R['scen']['b2']['link'], note='B2 — מסלול הסעה מקביל לקלים לאורך הגדר המזרחית: נפסל ב-0.4 מ׳ מהגדר; הזזת הגדר ב-3 מ׳ מזרחה (גדר — לא מבנה ולא דרך) — לאישורך'),
                      bay_geom=dict(rect=[9475, 820, 9560, 1000], he='מפרץ המתנה באמצע B (צד מזרח, x 9475–9560, ‏y 820–1000) — מטוס אחד ממתין, המנוגד עובר'))

# ---------------------------------------------------------------- (ו) ההדף של R3, כיוון המסלול, P6 מול BH-5
BL = D['blast']; HAZ = [BL[0] - 20, BL[1], BL[2] + 20, BL[3] + 200]      # מאחורי הקיר — 20 מ׳ דרומה (ההדף אחרי הקיר נחלש) ו-2 מ׳ לצדדים
gse_in = [g['id'] for g in FC.GSE_S if rint(g['r'], HAZ)]
road = FC.GSE_ROAD['r']; road_in = rint(road, HAZ)
OUT['blast'] = dict(wall=BL, hazard=HAZ, gse_in=gse_in, road_in=road_in, hours='20:30–04:25 (fieldfix: ההרצה ב-R3)',
                    fix='החניות של הבסיס הדרומי — עד x 9196 (כל 40 פיקס׳); דרך הבסיס — עד x 9190 (בלי הקטע שמאחורי הקיר)')
# הבסיס הדרומי — שתי שורות (14 + 14) לפי החלוקה (ג) + רזרבה: הגבוהים (אוטובוס, קייטרינג, מדרגות, מתדלק) מצפון לדרך, הנמוכים (גררים, GPU, מסוע) מדרום לה
ROW1 = ['AB', 'AB', 'AB', 'CT', 'CT', 'MS', 'MS', 'MS', 'FTs', 'FTs', 'FTs', 'SVC', 'WT', 'LV']
ROW2 = ['PT', 'PT', 'PT', 'PT', 'PT', 'PT', 'PT', 'GP', 'GP', 'GP', 'GP', 'GP', 'BL', 'BL']
HT = {'AB': 100, 'CT': 100, 'FTs': 75, 'MS': 75, 'SVC': 70, 'WT': 75, 'LV': 70, 'PT': 60, 'GP': 60, 'BL': 75}
WD = {'AB': 32, 'CT': 30, 'MS': 26, 'FTs': 26}
cnt = C.Counter(); GSE_FIX = []
for row, y0, up in ((ROW1, 2696, True), (ROW2, 2748, False)):
    for j, t in enumerate(row):
        cnt[t] += 1; w = WD.get(t, 24); x0 = 8492 + j * 48; h = HT[t]
        GSE_FIX.append(dict(id='S-%s%d' % (t, cnt[t]), t=t, r=[x0, y0 - h if up else y0, x0 + w, y0 if up else y0 + h]))
ROW_ROAD = [8480, 2700, 9190, 2744]
ROAD_FIX = ROW_ROAD
gse_fix_in = [g['id'] for g in GSE_FIX if rint(g['r'], HAZ)]
overl = [(a['id'], b['id']) for a, b in itertools.combinations(GSE_FIX, 2) if rint(a['r'], b['r'])]
inexp = [g['id'] for g in GSE_FIX if not (g['r'][0] >= FC.EXP['rect'][0] and g['r'][2] <= FC.EXP['rect'][2] and g['r'][1] >= FC.EXP['rect'][1] and g['r'][3] <= FC.EXP['rect'][3])]
if inexp: FAILS.append('חנייה מחוץ להרחבה: ' + ', '.join(inexp))
if OUT['fleet_split']['south_total'] > len(GSE_FIX): FAILS.append('הבסיס הדרומי קטן מדי')
spare = {t: sum(1 for g in GSE_FIX if g['t'] == t) - OUT['fleet_split']['rows'].get(t, {}).get('south', 0) for t in set(g['t'] for g in GSE_FIX)}
if any(v < 0 for v in spare.values()): FAILS.append('חסרות חניות בדרום: ' + str({k: v for k, v in spare.items() if v < 0}))
OUT['fleet_split']['spare'] = spare
OUT['blast'].update(gse_fix=GSE_FIX, road_fix=ROAD_FIX, gse_fix_in=gse_fix_in, gse_fix_overlap=overl, ok=not gse_fix_in and not rint(ROAD_FIX, HAZ) and not overl)
if not OUT['blast']['ok']: FAILS.append('חנייה / דרך באזור ההדף של R3')
# כיוון המסלול: כל תנועה לדרום עוברת את כל B (y −170 → 1925) בכל כיוון של המסלול — הזמן ב-B לא משתנה; ב-27 הנחיתות של הדרום יוצאות ב-A1 / A2 ומסיעות לאורך A עד B
lenB = FC.TCCY - FC.TACY; tB = lenB / FC.PLAN_TAXI_B
a_extra = (9190 - 7150) / FC.TAXI_V
OUT['rwy_dir'] = dict(B_len=lenB, B_s=round(tB, 1), per_south_move_B_09=round(tB, 1), per_south_move_B_27=round(tB, 1), A_extra_27=round(a_extra, 1),
                      text='09 או 27 — אותו זמן ב-B (%.0f ש׳ לכל תנועה לדרום: B הוא הקישור היחיד והאורך שלו קבוע); ב-27 הנחיתות של הדרום יוצאות ב-A2 (x 7150) ומסיעות עוד ~%.0f ש׳ על A עד B. הדו-כיווני לא מוריד את התפוסה של B.' % (tB, a_extra))
# P6 בדחיפה / בכניסה מול היציאה של BH-5 (הנתיב של היציאה חוצה את המלבן של P6 ליד האף)
p6 = next(f for f in FL if f['stand'] == 'P6')
blk = P6BLK
hits = []
for v in V:
    if OUT['halls_assign']['after']['assign']['%s/%d' % (v['stand'], v['train'])] != 'BH-5': continue
    ex = cyc(v['t'] + v['dur'])
    for a, b, what in blk:
        for k in (-T, 0, T):
            if a + k <= ex <= b + k: hits.append(dict(stand=v['stand'], kind=v['kind'], exit=round(ex, 1), what=what, wait=round(b + k - ex, 1)))
OUT['p6_bh5'] = dict(blocks=[[round(a, 1), round(b, 1), w] for a, b, w in blk], hits=hits,
                     rule='הרכבת שמסיימת באולם בזמן ש-P6 בדחיפה או בכניסה — נשארת בנתיב של העמדה (בתוך האולם, מאחורי הדלת המזרחית) עד שהחלון נגמר; במשחק — s15k_fleet בודק את זה (כל 0.25 ש׳)')

# ---------------------------------------------------------------- (ז) המהירות של רכבי השירות מול הישן (מהמדידה במשחק, s15k_fleet — try6648)
sp = {}
try:
    fj = json.load(open(os.path.join(HERE, '..', 'qa', 'fch_try6648.json'), encoding='utf-8'))
    det = next(a['d'] for a in fj['audit'] if a['id'] == 's15k_fleet')
    import re
    for m in re.finditer(r'([A-Z]+) ([\d.]+)/([\d.]+) · ([\d.]+)', det): sp[m.group(1)] = dict(vmax=float(m.group(2)), vavg=float(m.group(3)), old=float(m.group(4)))
except Exception as e:
    sp = {'err': str(e)}
OUT['speeds'] = dict(src='s15k_fleet במשחק (try6648, כל 0.25 ש׳, קמ״ש)', rows=sp,
                     ops=dict(bags_per_unit=dict(new=2.2, old='2.2–3.5'), belt=dict(new='228–285 ש׳', old='—'), fuel=dict(new=MATRIX['AC-NB-01']['fuel']['d'], old=(MATRIX['AC-NB-01']['fuel'].get('note') or '')),
                              cater=dict(new=MATRIX['AC-NB-01']['cater']['d'], old=MATRIX['AC-NB-01']['cater'].get('note')), push=dict(new=MATRIX['AC-NB-01']['push']['d'], old=MATRIX['AC-NB-01']['push'].get('note'))))

# ---------------------------------------------------------------- (ח) המחולל של S15 עם המתנות (fc_sim.py, ‏FC_WAIT=1, ‏FC_TAXI=90)
gen = {}
for name in ('fc_sim_result.json', 'fc_sim_result_big.json', 'fc_sim_result_t90.json', 'fc_sim_result_t90_wait.json', 'fc_sim_result_t90_big_wait.json'):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        g = json.load(open(p, encoding='utf-8')); gen[name] = dict(flights=g['flights'], moves1800=g['moves1800'], rwy_util=g['rwy_util'], miss=g['miss'], taxi=g.get('taxi'), waits=g.get('waits'), order=g.get('order'))
OUT['generator'] = gen


# ---------------------------------------------------------------- (ט) פרופיל העמדות — כל עמדה × כל סוג (AIR‑35 / AIR‑36 של הישן: "stand profiles, the matrix") — למתכנן (fieldthru)
plan_st = {f['stand']: f['model'] for f in FL}
prof = {}
BRJ = None
try: BRJ = json.load(open(os.path.join(HERE, '..', 'qa', 'bridges_try6649.json'), encoding='utf-8'))
except Exception: pass
types = [m for m in FC.DIM if m in AC and AC[m]['cls'] not in ('HELI',)]
for sid in ST:
    if sid == 'CH': continue
    row = {}
    for m in types:
        f = FC.foot(sid, m); r = ST[sid]['rect']; why = []
        if not FC.inside(f, [r[0] - 1, r[1] - 1, r[2] + 1, r[3] + 1]): why.append('לא נכנס')
        for s2, m2 in plan_st.items():
            if s2 == sid: continue
            g = FC.rgap(f, FC.foot(s2, m2)); need = 30 if (AC[m]['cls'] not in ('GA', 'EXEC') or AC[m2]['cls'] not in ('GA', 'EXEC')) else 20
            if g < need: why.append('כנף מול %s' % s2)
        for pk, pr in D['pockets'].items():
            if any(FC.rint(pr, q) for q in FC.shape(sid, m)): why.append('כיס ' + pk.replace('AIR-GSE-', ''))
        if BRJ:
            b = next((q for q in BRJ['rows'] if q['stand'] == sid and q['ac'] == m), None)
            if b is not None and not b.get('ok'): why.append('שרוול')
        row[m] = why
    prof[sid] = row
OUT['stand_profile'] = dict(types=types, rows={s: {m: (not w) for m, w in r.items()} for s, r in prof.items()}, why={s: {m: w for m, w in r.items() if w} for s, r in prof.items()},
                            plan_ok=all(not prof[s][m] for s, m in plan_st.items()), note='עובר = המעטפת בתוך העמדה, 3 מ׳ (קלים — 2) מקצה הכנף של השכנים בלוח, בלי כיס ציוד מתחת לגוף / לכנף / לזנב, ובעמדות השרוול — השרוול עוגן (q_bridges במשחק)')
if not OUT['stand_profile']['plan_ok']: FAILS.append('סוג בלוח שלא מתאים לעמדה שלו')
OUT['fails'] = FAILS; OUT['ok'] = not FAILS
json.dump(OUT, open(os.path.join(HERE, 'fc_result2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
h = OUT['halls_assign']
print('עמדות הכבודה — לפני (השיוך של הציור):', {k: v['util'] for k, v in h['before']['per'].items()}, '· אחרי:', {k: v['util'] for k, v in h['after']['per'].items()}, '· המתנה מרבית', h['after']['wait_max'])
print('  השיוך:', h['after']['assign'])
s = OUT['service_roads']; print('דרכי שירות שחוצות את B:', s['crossB'], '· את C:', s['crossC'])
for k, v in s['cross'].items(): print('  ', k, 'x', v['x'], 'תפוסה של מטוסים', v['util'], '% · המתנה ממוצעת', v['wait_mean'], 'מרבית', v['wait_max'])
print('  חציות של C במחזור: היום', s['n_today'], dict(s['per_cycle_today']), '· עם הבסיס הדרומי', s['n_south'], dict(s['per_cycle_south']))
print('צי — דרום / צפון:', {k: (v['south'], v['north']) for k, v in OUT['fleet_split']['rows'].items()}, '· בדרום', OUT['fleet_split']['south_total'], 'מתוך', OUT['fleet_split']['south_spots'])
for m in OUT['maint']['rows']: print('תחזוקה', m['hangar'], m['models'], 'בשירות', m['in_service'], '· גרירה', m['tow_s'], 'ש׳ · חלון', m['window'], '· הארוך', m['free_longest'])
print('עתודה (מפרץ ב-B):', OUT['reserve']['bay'])
print('הדף של R3: בתוך האזור', OUT['blast']['gse_in'], OUT['blast']['road_in'], '· אחרי התיקון', OUT['blast']['gse_fix_in'], OUT['blast']['ok'])
print('P6 מול BH-5:', OUT['p6_bh5']['hits'])
print('המחולל:', gen)
print('פרופיל העמדות:', {s_: [m.replace('AC-', '').replace('-01', '') for m, ok in r.items() if ok] for s_, r in OUT['stand_profile']['rows'].items()}, '· הלוח מתאים:', OUT['stand_profile']['plan_ok'])
print('תוצאה:', 'עובר' if OUT['ok'] else 'נכשל — ' + ' · '.join(FAILS))
sys.exit(0 if OUT['ok'] else 1)
