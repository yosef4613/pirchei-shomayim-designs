# -*- coding: utf-8 -*-
# ft2_sim.py — fieldthru2: ההרחבה של המחולל של fieldthru (ft_sim.py — כלל 19א) לגאומטריה שהבעלים אישר (15:05, D‑701):
#   (1) מחבר חדש בין A למסלול, בין A2 ל-A3 של היום (מעל P5) — "A3" החדש (x ‏A3N); ה-A3 של היום נקרא A4 (x 9190).
#       עוד קו המתנה / כניסה למסלול, ויציאה מהמסלול לנוחתים (09);
#   (2) המראה בכיוון ההפוך (27, מערבה) — מ-A4 או מ-A3 החדש — רק כשהמסלול והאוויר פנויים לגמרי: הכלל של AIR-09 (ft_sim.rwy_ok עם הכיוון —
#       כיוון הפוך מקבל את כל הבלוק: הגישה מקצה העולם / הטיפוס עד קצה העולם, ועוד 10 ש׳).
# הקישורים: 'A1' / 'A2' — המראה 09 (כמו היום); 'A3N' / 'A4' — המראה 27. היציאות לנוחתים (09): 'A3' (= A4 של היום), 'A2', 'A3N'.
import sys, os, math
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
import numpy as np
import ft_sim as F
M = F.M; T = F.T
A3N = float(os.environ.get('FT2_A3N', 8345))
_dep1, _dep2, _arr1_09, _plan0 = F.dep1, F.dep2, F.arr1_09, F.plan_flight
def _with_a2(x, fn, *a):
    keep = F.A2; F.A2 = x
    try: return fn(*a)
    finally: F.A2 = keep
def dep1(sid, ac, link='A1'):
    if link == 'A3N': return _with_a2(A3N, _dep1, sid, ac, 'A2')
    if link == 'A4': return _dep1(sid, ac, 'A3')
    return _dep1(sid, ac, link)
def dep2_27x(ac, x):
    L = M.D.ACT[ac][0]; a = M.Actor('x', 'ac', ac, '', L, M.D.ACT[ac][1]); q = [x, M.HOLD + 40]; a.t = 0.0
    R = 90; P = M.Path(q, F.N_).go(y=F.RCY + R).tr(F.W_, R); a.move(P.P, 18, F.V_ARC, flags=1)
    q = a.legs[-1]['p'][-1]; xl = q[0] - 2260; a.move([q, [xl, F.RCY]], F.V_ARC, 640, flags=1)
    a.move([[xl, F.RCY], [0, F.RCY], [-2400, F.RCY]], 640, 760, z0=0, z1=520, flags=4)
    return a
def dep2(ac, link='A1'):
    if link == 'A3N': return dep2_27x(ac, A3N)
    if link == 'A4': return dep2_27x(ac, F.A3)
    return _dep2(ac, link)
def arr1_09(sid, ac, exit='A3'):
    if exit == 'A3N': return _with_a2(A3N, _arr1_09, sid, ac, 'A2')
    return _arr1_09(sid, ac, exit)
F.dep1 = dep1; F.dep2 = dep2; F.arr1_09 = arr1_09
KD = {'A1': 'd9', 'A2': 'd9', 'A3N': 'd27', 'A4': 'd27'}
def links_for(sid):
    # P1–P5: הגרר של היום מניח שהאף פונה מערבה אחרי הדחיפה (ft_sim.tug_trip) — הם נשארים ב-A1 / A2; ‏P6 והדרום — גם 27 מ-A3 החדש / A4
    base = tuple(x for x in os.environ.get('FT_LINKS', 'A1,A2').split(','))
    extra = tuple(x for x in os.environ.get('FT2_LINKS27', 'A3N,A4').split(',') if x)
    if sid.startswith('P') and sid != 'P6': return base
    return base + extra
def plan_flight(Wd, sid, ac, al, phase=0, prefer=None, accept=None, links=('A1', 'A2'), exits=('A3', 'A2')):
    # = ft_sim.plan_flight, עם: קישורים לכל עמדה (links_for), יציאה A3N, והכיוון בכלל המסלול (kd — d9 / d27 / a9)
    if sid.startswith('P') and sid != 'P6' and not os.environ.get('FT2_EXITS'): return _plan0(Wd, sid, ac, al, phase, prefer, accept, links, exits)   # P1–P5 — כמו היום (עם התור על A)
    links = links_for(sid); exits = tuple(exits) + tuple(x for x in os.environ.get('FT2_EXITS', 'A3N').split(',') if x and x not in exits)
    smask = np.zeros(F.NC, dtype=np.uint8); mp = F.MINPARK.get(ac, 300)
    DEP = []; ARR = []; why0 = []
    for ln in links:
        if ln == 'A2' and not F.can_a2(ac): continue
        A1_ = F.dep1(sid, ac, ln)
        if A1_ is None: continue
        B2 = F.dep2(ac, ln); tp1 = F.template(A1_, 0, A1_.t); tp2 = F.template(B2, 0, B2.t)
        h_ = F.static_hit(Wd, A1_, 0, A1_.t, sid) or F.static_hit(Wd, B2, 0, B2.t, sid)
        if h_: why0.append('dep ' + ln + ' ' + h_[0]); continue
        qh = A1_.legs[-1]['p'][-1]; hcs = F.free_prefix(Wd.occ, F.hold_cells([qh[0], qh[1], F.N_, 0, 1], ac), smask)
        if F.static_hit(Wd, F.still(ac, qh, F.N_), 0, 0, sid): hcs = None
        if hcs is None: why0.append('hold ' + ln + ' static'); continue
        DEP.append(dict(ln=ln, kd=KD.get(ln, 'd9'), A=A1_, B=B2, d1=A1_.t, d2=B2.t, c1=F.shifts_conflict(Wd.occ, tp1, 0), c2=F.shifts_conflict(Wd.occ, tp2, 0), hcs=hcs, w2=F.rwy_wins_rel(B2, 0, B2.t), qh=qh, q=None))
    for ex in exits:
        if ex in ('A2', 'A3N') and ac in F.HEAVY and ac != 'AC-LG-01' and ex == 'A2': continue
        C3, ttd_rel = F.arr1(sid, ac, ex)
        if C3 is None: continue
        tp3 = F.template(C3, 0, C3.t)
        h_ = F.static_hit(Wd, C3, 0, C3.t, sid)
        if h_: why0.append('arr ' + ex + ' ' + h_[0]); continue
        stop = C3.legs[-1]['p'][-1]; pcs = F.free_prefix(Wd.occ, F.hold_cells([stop[0], stop[1], F.S_, 0, 0], ac), smask)
        if F.static_hit(Wd, F.still(ac, stop, F.S_), 0, 0, sid): pcs = None
        if pcs is None: why0.append('park static'); continue
        ARR.append(dict(ex=ex, C=C3, d3=C3.t, c3=F.shifts_conflict(Wd.occ, tp3, 0), w3=F.rwy_wins_rel(C3, 0, C3.t), stop=stop, pcs=pcs))
    if not DEP or not ARR: return None, 'נוגע במטוס / ברכב שחונה קבוע (' + ', '.join(why0) + ')'
    opts = []
    order = [(phase + k) % F.N for k in range(F.N)] if prefer is None else prefer
    for rank, s0 in enumerate(order):
        for dp in DEP:
            if dp['c1'][s0]: continue
            th = s0 + dp['d1']; wq = 0
            tg0 = int(math.ceil(th + 4 - 1e-6))
            for tg in range(tg0, tg0 + F.WMAX):
                if not F.seg_free(dp['hcs'], th, tg): break
                if dp['c2'][tg % F.N]: continue
                ww = [tg + dp['w2'][0][0], tg + dp['w2'][0][1]]
                if not F.rwy_ok(ww, ac, Wd.busy, kd=dp['kd']): continue
                opts.append((tg - th + wq, rank, s0, dp, tg, ww, wq)); break
    opts.sort(key=lambda o: (round(o[0] / 6), o[1]))
    tries = 0; DG = dict(c3=0, rwy=0, park=0)
    for w, rank, s0, dp, tg, ww, wq in opts:
        tair = tg + dp['d2']; got = None
        for ar in ARR:
            for sa in range(int(math.ceil(tair)), int(s0 + T - mp - ar['d3']) + 1):
                if ar['c3'][sa % F.N]: DG['c3'] += 1; continue
                wa = [sa + ar['w3'][0][0], sa + ar['w3'][0][1]]
                if not F.rwy_ok(wa, ac, Wd.busy + [[ww[0], ww[1], ac, dp['kd']]], kd='a9'): DG['rwy'] += 1; continue
                ob = sa + ar['d3']
                if not F.seg_free(ar['pcs'], ob, s0 + T) or not F.seg_free(ar['pcs'], s0, s0 + .01): DG['park'] += 1; continue
                got = (sa, ar, ob, wa); break
            if got: break
        if not got: continue
        sa, ar, ob, wa = got
        cand = dict(s0=s0, w=w, tg=tg, sa=sa, ob=ob, park=s0 + T - ob, rw=[ww, wa], kd=[dp['kd'], 'a9'], ln=dp['ln'], ex=ar['ex'], wq=wq)
        a = F.build_flight(sid, ac, al, cand, dp['A'], dp['B'], ar['C'], dp['qh'], ar['stop'], dp['d1'], dp)
        tries += 1
        if accept is None or accept(a): return dict(a=a, best=cand, d=(dp['d1'], dp['d2'], ar['d3'])), 'נכנס'
        if tries > 60: break
    return None, 'אין זמן פנוי (%d אפשרויות דחיפה, %d נבדקו עם הגרר; נחיתה: %s)' % (len(opts), tries, DG)
F.plan_flight = plan_flight
# (3) D‑701 תוספת (הבעלים 15:10): "במעבר B עוד נתיב … נתיב יוצא ונתיב נכנס" — B ברוחב 23 מ׳ (x 9285–9515); היוצאים מהדרום (צפונה) בנתיב המערבי,
# הנכנסים (דרומה) בנתיב המזרחי — לקטנים (מוטה עד LANE_W). שניים עוברים יחד רק אם יש מקום בין הכנפיים — הבדיקה במרחב־זמן / OBB מכריעה בכל קטע;
# מטוס גדול נוסע בקו האמצעי — ואז אחד-אחד, כמו היום.
LANE = float(os.environ.get('FT2_LANE', 55)); LANE_W = float(os.environ.get('FT2_LANE_W', 200))
if os.environ.get('FT2_LANES', '1') != '0':
    _d1b, _atx = F.dep1, F.arr1_taxi
    def _lane(fn, dx, sid, ac, *a):
        if not str(sid).startswith(('GA', 'R')) or M.D.ACT[ac][1] > LANE_W: return fn(sid, ac, *a)
        keep = F.TBCX; F.TBCX = keep + dx
        try: return fn(sid, ac, *a)
        finally: F.TBCX = keep
    def dep1_l(sid, ac, link='A1'): return _lane(_d1b, -LANE, sid, ac, link)
    def arr1_taxi_l(a, sid, ac, t_td):
        if not str(sid).startswith(('GA', 'R')) or M.D.ACT[ac][1] > LANE_W: return _atx(a, sid, ac, t_td)
        keep = F.TBCX; F.TBCX = keep + LANE
        try: return _atx(a, sid, ac, t_td)
        finally: F.TBCX = keep
    F.dep1 = dep1_l; F.arr1_taxi = arr1_taxi_l
# (4) המתנה בדרך (aoHold של הישן) גם בהסעה אחרי הנחיתה — ft_sim.plan_flight2 (seg_walk, נקודות תור על A / B / C) — עם הכיוונים של D‑701 (A3N / A4 → 27)
import inspect as _ins
F.KD2 = KD
_s2 = _ins.getsource(F.plan_flight2).replace("kd='d27' if ln == 'A3' else 'd9'", "kd=KD2.get(ln, 'd27' if ln == 'A3' else 'd9')")
exec(compile(_s2, F.__file__, 'exec'), F.__dict__)
# (5) נתיב שני ב-C (המתאם 15:30, אותו כלל של B): הנכנסים (מערבה, אל העמדות) בנתיב הצפוני — לקטנים; היוצאים בקו האמצעי
LANE_C = float(os.environ.get('FT2_CLANE', 55))
if os.environ.get('FT2_LANES', '1') != '0' and LANE_C:
    _atx2 = F.arr1_taxi
    def arr1_taxi_c(a, sid, ac, t_td):
        if not str(sid).startswith(('GA', 'R')) or M.D.ACT[ac][1] > LANE_W: return _atx2(a, sid, ac, t_td)
        keep = F.TCCY; F.TCCY = keep - LANE_C
        try: return _atx2(a, sid, ac, t_td)
        finally: F.TCCY = keep
    F.arr1_taxi = arr1_taxi_c
