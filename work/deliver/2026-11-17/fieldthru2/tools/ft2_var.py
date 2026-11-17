# -*- coding: utf-8 -*-
# ft2_var.py <world.json> <out.json> [עמדות] [סוגים] — fieldthru2: מגוון סוגים בכל עמדה (הבעלים 17.11). שדרוג של ft_sim.py:variant_of (fieldthru, כלל 19א):
# לכל טיסה בלוח — גרסה לכל סוג שנכנס בעמדה (stands_matrix של fieldcalc — FITS / קו העצירה SHIFT), "תואמת זמן":
#   · אותם חלונות מסלול (אותה המראה ואותה נגיעה — המסלול והספירה לא משתנים);
#   · אותו רגע דחיפה (s0 של הטיסה בלוח) — הגרסה מגיעה לקו ההמתנה לפני השחרור (ממתינה בו יותר);
#   · נעצרת בעמדה לא אחרי הטיסה שבלוח (ob ≤ ob של הלוח) — חלון העמידה מכיל את זה של הלוח, ולכן כל מה שמתוזמן בעמידה (השירות, הנוסעים, s15k) נשאר בתוכו;
#   · נבדקת במדויק (OBB כל 0.25 ש׳) מול כל מה שרץ במשחק (העולם כפי שהוא רץ — dump של הבנייה), חוץ מהטיסה עצמה והגרר שלה;
#   · והגרר שלה (אותו רכב של הצי, AF) — נסיעה חדשה לגרסה (ft_sim.tug_trip), מול המטוסים בלי הטיסה עצמה, מול הרכבים בלי הגרר, ומול הנסיעות האחרות שלו.
import sys, os, json, time, math
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
import numpy as np
import ft_sim as F
if os.environ.get('FT2_D701'):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import ft2_sim   # D‑701: ‏A3 החדש + המראה הפוכה (27) מ-A3 / A4
M = F.M
# בעמדות הגדולות (P1 / P6) קו העצירה של כל סוג ב-y ‏855–915 — הגרר נוסע בשורה y 989 (מדרום לאף) לכל סוג, לא רק לענק (ב-864 הוא עובר מתחת לאף של סוג קטן יותר)
import inspect as _ins
_src = _ins.getsource(F.tug_trip).replace("big = a.L > 600", "big = a.L > 600 or sid in ('P1', 'P6')"); exec(compile(_src, F.__file__, 'exec'), F.__dict__)
if os.environ.get('FT2_HEAVY_A2'):
    for _fn in ('plan_flight', 'plan_flight2'):
        _s = _ins.getsource(getattr(F, _fn)).replace("ac != 'AC-LG-01'", "ac not in ('AC-LG-01', 'AC-MW-01', 'AC-CG-01')")
        exec(compile(_s, F.__file__, 'exec'), F.__dict__)
W = json.load(open(sys.argv[1])); outp = sys.argv[2]
ONLY = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
TYPES = sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] else ['AC-PR-01', 'AC-LT-01', 'AC-BJ-01', 'AC-CN-01', 'AC-TB-01', 'AC-TP-01', 'AC-RJ-01', 'AC-QJ-01', 'AC-NB-01', 'AC-MW-01', 'AC-CG-01', 'AC-LG-01']
CLS = {'AC-PR-01': 'GA', 'AC-LT-01': 'GA', 'AC-BJ-01': 'EXEC', 'AC-CN-01': 'EXEC', 'AC-AM-01': 'AMPH', 'AC-TB-01': 'CARGO', 'AC-TP-01': 'REG', 'AC-RJ-01': 'REG', 'AC-QJ-01': 'REG', 'AC-NB-01': 'NB', 'AC-MW-01': 'WIDE', 'AC-CG-01': 'CARGO', 'AC-LG-01': 'XL', 'AC-HC-01': 'CARGO'}
GROUP_OK = {'P': {'REG', 'NB', 'WIDE', 'XL'}, 'C': {'CARGO'}, 'R': {'REG', 'NB', 'EXEC'}, 'G': {'GA', 'EXEC'}}   # הבעלים 14:35: פרטי / מנהלים לא ב-P1–P6; עמדה גדולה — גם לבינוני / קטן מאותה משפחה
def allowed(sid, ac): return CLS.get(ac) in GROUP_OK.get(sid[0], set())
FIXED = set(os.environ.get('FT2_FIXED', 'P4,GA1,GA6,C2').split(','))   # P4 / GA1 / GA6 — מחזור התחזוקה של fieldfix (074zp2: אותו דגם כמו מטוס ההאנגר); C2 — הטיסה של 074p (TG-C, שני ביקורים)
MARG = float(os.environ.get('FT2_M', .5))
t0 = time.time()
FL = [F.actor(o) for o in W['flights']]; VH = [F.actor(o) for o in W['veh']]; HE = [F.actor(o) for o in W.get('heli', [])]; TW = F.ffr3_actors(W.get('ffr3'))
class Wd: pass
Wd.SIM = W; Wd.FL = FL; Wd.VH = VH; Wd.HE = HE; Wd.TW = TW; Wd.act = {q[0] for q in W['sched']}
mov = {v['id'] for v in W['veh']}; Wd.SP = []
for vid, sp in W['spots'].items():
    if vid in mov: continue
    r = sp['rect']; w, h = r[2] - r[0], r[3] - r[1]; x = M.Actor('SP-' + vid, 'veh', 'X', sp.get('home', ''), max(w, h), min(w, h))
    x.legs = [dict(p=[[(r[0] + r[2]) / 2, (r[1] + r[3]) / 2]], t0=-F.T, t1=3 * F.T, h=(math.pi / 2 if h >= w else 0), f=0)]; Wd.SP.append(x)
Wd.PK = {sid: F.pk_actor(sid, ac) for sid, ac in W['parked'].items() if ac and sid not in Wd.act}
Wd.pkc = {sid: np.unique(np.concatenate([F.obb_cells(b, 0) for b in M.boxes(a, M.evalp(a, 0))])) for sid, a in Wd.PK.items()}
Wd.busy = []
for a in FL: Wd.busy += [list(w[:3]) + [F.win_kind(a, w)] for w in F.flight_rwy_wins(a)]
Wd.PC = None; F.world_cache(Wd)
# טבלאות שמירה (מרחב־זמן) לפי שחקן — כדי להוריד את הטיסה עצמה / את הגרר עצמו
def occ_idx(a, vk=1.0):
    # כמו Occ.add_actor של ft_sim — אבל כרשימת אינדקסים (זמן × תא), כדי להוריד שחקן אחד מהספירה בלי טבלה מלאה לכל שחקן
    out = []
    for i in range(F.N):
        for sub in (0.0, .25, .5, .75):
            P = M.evalp(a, i * F.DT + sub * F.DT)
            if not P: continue
            if sub and a.kind == 'veh': break
            for b in F.boxes_of(a, P, vk):
                c = F.obb_cells(b, 0.0); out.append(i * F.NC + c)
    return np.unique(np.concatenate(out)) if out else np.zeros(0, dtype=np.int64)
def cnt_of(D):
    c = np.zeros(F.N * F.NC, dtype=np.uint8)
    for k, ix in D.items(): c[ix] += 1
    return c
def minus(cnt, ix):
    c = cnt.copy(); c[ix] -= 1; return (c > 0).reshape(F.N, F.NC)
OA = {a.id: occ_idx(a) for a in FL + HE + TW}; cntA = cnt_of(OA)
VKV = float(os.environ.get('FT_VKV', 1.3)); OV = {v.id: occ_idx(v, VKV) for v in VH}; cntV = cnt_of(OV)
print('world %.1f ש׳ · טיסות %d · רכבים %d' % (time.time() - t0, len(FL), len(VH)), flush=True)
TUG = {}
for v in W['veh']:
    for g in v['legs']:
        if g.get('att'): TUG.setdefault(g['att'], []).append(v['id'])
VB = {v['id']: v for v in W['veh']}
def trips_of(vid): return F.base_trips(VB[vid])
def tug_variant(vid, f, a):
    # הנסיעה של הגרר לגרסה: אותה צורה (ft_sim.tug_trip), מול המטוסים בלי f, מול הרכבים בלי הגרר, מול הנסיעות האחרות שלו (AF_GAP), ומול הכיסים
    v = VB[vid]; home = v['legs'][-1]['p'][0]; hh = v['legs'][-1].get('h', F.S_)
    others = [tr for tr in trips_of(vid) if not any(g.get('att') == f.id for g in tr)]
    oA = minus(cntA, OA[f.id]); oV = minus(cntV, OV[vid])
    pkm = np.zeros(F.NC, dtype=np.uint8)
    for sid, c in Wd.pkc.items():
        if sid != f.home: pkm[c] = 1
    class T0: pass
    Wt = type('Wt', (), {})(); Wt.SP = Wd.SP
    for useV in ((True,) if os.environ.get('FT2_REQV') else (True, False)):
        for early in (0, 6, 14, 24, 40, 60, 80):
            for late in (1, 5, 9):
                tr = F.tug_trip(vid, a, home, hh, early, late)
                if not F.trips_ok(others, tr): continue
                I, C = F.trip_template(tr, v['L'], v['W'])
                if len(I):
                    ix = (int(round(tr[0]['t0'] / F.DT)) + I) % F.N
                    if oA[ix, C].any() or pkm[C].any() or (useV and oV[ix, C].any()): continue
                if F.veh_static_hit(Wt, tr, home, v['L'], v['W']): continue
                return tr, (early, late, 'V' if useV else '-')
    return None, None
EXACT = bool(os.environ.get('FT2_EXACT')); OBX = float(os.environ.get('FT2_OBX', 60)); S0X = float(os.environ.get('FT2_S0X', 60))
def build_var(f, ac, s0, tg, sa, ln, ex, prof):
    # prof: 'own' — ההסעה והדחיפה של הסוג (ft_sim: TAXI_BY / PUSH_BY של הישן); 'base' — באותה מהירות של הטיסה שבלוח (אותו קצב בדרך — אותם מפגשים)
    sid = f.home; keep = (dict(F.TAXI_BY), dict(F.PUSH_BY))
    try:
        if prof == 'base':
            F.TAXI_BY[ac] = F.TAXI_BY.get(f.model, F.TAXI_V); F.PUSH_BY[ac] = F.PUSH_BY.get(f.model, 20.0)
        A = F.dep1(sid, ac, ln)
        if A is None: return None, 'אין דחיפה'
        C3, _ = F.arr1(sid, ac, ex)
        if C3 is None: return None, 'אין הסעה'
    finally:
        F.TAXI_BY.clear(); F.TAXI_BY.update(keep[0]); F.PUSH_BY.clear(); F.PUSH_BY.update(keep[1])
    if s0 + A.t > tg - 2: return None, 'late'
    B2 = F.dep2(ac, ln); qh = A.legs[-1]['p'][-1]; ob = sa + C3.t
    a = M.Actor(f.id, 'ac', ac, sid, M.D.ACT[ac][0], M.D.ACT[ac][1]); a.airline = getattr(f, 'airline', None)
    for g in A.legs: h = dict(g); h['t0'] = round(g['t0'] + s0, 2); h['t1'] = round(g['t1'] + s0, 2); a.legs.append(h)
    a.legs.append(dict(p=[list(qh)], t0=round(s0 + A.t, 2), t1=round(tg, 2), h=round(F.N_, 4), f=1))
    for g in B2.legs: h = dict(g); h['t0'] = round(g['t0'] + tg, 2); h['t1'] = round(g['t1'] + tg, 2); a.legs.append(h)
    for g in C3.legs: h = dict(g); h['t0'] = round(g['t0'] + sa, 2); h['t1'] = round(g['t1'] + sa, 2); a.legs.append(h)
    a.legs.append(dict(p=[list(C3.legs[-1]['p'][-1])], t0=round(ob, 2), t1=round(s0 + F.T, 2), h=round(F.S_, 4), f=0))
    return a, ob
def variant_tc(f, ac, exits=('A3', 'A2')):
    sid = f.home; L = f.legs
    if F.FITS is not None and (sid, ac) not in F.FITS: return None, 'לא נכנס בעמדה (stands_matrix)'
    hold = [g for g in L if g.get('h') is not None and g.get('f') == 1 and abs(g['p'][0][1] - (M.HOLD + 40)) < 1.5]
    air = [g for g in L if g.get('f') == 4]
    if not hold or len(air) < 2: return None, 'אין מבנה מוכר'
    tg = hold[-1]['t1']; sa = air[1]['t0']; s00 = L[0]['t0']; ob0 = L[-1]['t0']
    ln = 'A1' if abs(hold[-1]['p'][0][0] - F.A1) < 2 else ('A2' if abs(hold[-1]['p'][0][0] - F.A2) < 2 else None)
    if ln is None or (ln == 'A2' and not F.can_a2(ac)): return None, 'קו ההמתנה (%s) לא מתאים לסוג' % ln
    why = []; ow = F.flight_rwy_wins(f); others = [b for b in Wd.busy if not any(abs(b[0] - w[0]) < .01 and abs(b[1] - w[1]) < .01 for w in ow)]
    fallback = None
    hb = hold[-1]['t0']   # הרגע שבו הטיסה שבלוח מגיעה לקו ההמתנה — הגרסה מגיעה אליו באותו רגע (לא יושבת בקו כשאחרים עוברים מאחוריה)
    for prof in ('own', 'base'):
        keep = (dict(F.TAXI_BY), dict(F.PUSH_BY))
        try:
            if prof == 'base': F.TAXI_BY[ac] = F.TAXI_BY.get(f.model, F.TAXI_V); F.PUSH_BY[ac] = F.PUSH_BY.get(f.model, 20.0)
            A0 = F.dep1(sid, ac, ln)
        finally:
            F.TAXI_BY.clear(); F.TAXI_BY.update(keep[0]); F.PUSH_BY.clear(); F.PUSH_BY.update(keep[1])
        if A0 is None: why.append('אין דחיפה'); continue
        dm = round(hb - s00 - A0.t, 1); cands = []
        for d in ([0] if EXACT else [dm, 0] + [dm + k for k in (3, -3, 6, -6, 9, -9)] + [-k for k in range(3, int(S0X) + 1, 3)]):
            if d not in cands and s00 + d + A0.t <= tg - 2 and d >= -S0X: cands.append(d)
        for ds in cands:
            s0 = s00 + ds
            for ex in exits:
                if ex == 'A2' and ac in F.HEAVY and ac != 'AC-LG-01' and not os.environ.get('FT2_HEAVY_A2'): continue   # FT2_HEAVY_A2: גם MW / CG יוצאים ב-A2 (גלגול 175 מ׳ — כמו LG)
                a, ob = build_var(f, ac, s0, tg, sa, ln, ex, prof)
                if a is None:
                    if ob != 'late': why.append(ex + ' ' + ob)
                    continue
                if ob > ob0 + (float(os.environ.get('FT2_EXACT_TOL', 3)) if EXACT else OBX): why.append('%s נעצר %.0f ש׳ אחרי הלוח' % (ex, ob - ob0)); continue
                if EXACT and ob < ob0 - .05:
                    # אותו רגע עצירה כמו בלוח: המטוס עוצר בקו של הסוג ומחכה שם (הרגל של העמידה מתחילה ב-ob של הלוח — השרוול, הנוסעים, הכבודה והשירות באותם זמנים)
                    pk = a.legs.pop(); a.legs.append(dict(p=pk['p'], t0=pk['t0'], t1=round(ob0, 2), h=pk['h'], f=1)); a.legs.append(dict(pk, t0=round(ob0, 2))); ob = ob0
                if s0 + F.T - ob < F.MINPARK.get(ac, 300): why.append('%s עמידה קצרה' % ex); continue
                hs = F.static_hit(Wd, a, s0, s0 + F.T, sid)
                if hs: why.append('%s חונה %s' % (ex, hs[0])); continue
                h = F.exact_flight(Wd, a, m=MARG, skip_ids={f.id} | set(TUG.get(f.id, [])), vkv=1.0)
                if h: why.append('%s נוגע ב-%s (%.0f)' % (ex, h[1], h[0] % F.T)); continue
                nw = F.flight_rwy_wins(a)
                if not all(F.rwy_ok(w, ac, others, kd=F.win_kind(a, w)) for w in nw): why.append(ex + ' המסלול (כבד)'); continue
                tugs = {}; bad = None
                for vid in TUG.get(f.id, []):
                    tr, w = tug_variant(vid, f, a)
                    if not tr: bad = vid; break
                    tugs[vid] = dict(trip=tr, w=w)
                    if w[2] != 'V':
                        # AF של הישן: גרר אחר מהצי (נבדק גם מול הרכבים) — והגרר של הלוח לא יוצא בסבב הזה
                        for alt in [x for x in os.environ.get('FT2_ALT', 'PT-C,PT-P2,PT-P3').split(',') if x and x in VB and x != vid]:
                            tr2, w2 = tug_variant(alt, f, a)
                            if tr2 and w2[2] == 'V': tugs.pop(vid); tugs[alt] = dict(trip=tr2, w=w2); tugs[vid] = dict(trip=None, w=('-', '-', 'off')); break
                if bad: why.append('%s אין זמן לגרר %s' % (ex, bad)); continue
                sol = dict(ac=ac, L=a.L, W=a.W, legs=a.legs, park=[round(ob, 2), round(s0 + F.T, 2)], ex=ex, prof=prof, ds=ds, ob0=ob0, dob=round(ob - ob0, 1), tugs=tugs)
                if all(x['w'][2] in ('V', 'off') for x in tugs.values()): return sol, 'נכנס'
                if fallback is None: fallback = sol   # הגרר נבדק רק מול המטוסים — עדיף פתרון שבו הוא נבדק גם מול הרכבים
    if fallback is not None: return fallback, 'נכנס (הגרר — רק מול המטוסים)'
    if not why: why = ['מגיע לקו ההמתנה אחרי השחרור גם בדחיפה מוקדמת ב-%d ש׳' % S0X]
    from collections import Counter
    c = Counter(why); return None, ' · '.join('%s ×%d' % (k, n) if n > 1 else k for k, n in c.most_common(4))
FREE = set(x for x in os.environ.get('FT2_FREE', '').split(',') if x)   # "P1:AC-MW-01,..." — גרסה "חופשית": לו״ז חדש לעמדה בסבב הזה (חלונות מסלול אחרים), מול העולם בלי הטיסה של הלוח
_WF = {}
def world_without(f):
    if f.id in _WF: return _WF[f.id]
    d = dict(W); d['flights'] = [o for o in W['flights'] if o['id'] != f.id]; d['sched'] = [q for q in W['sched'] if q[0] != f.home]
    Wf = F.World(d); _WF.clear(); _WF[f.id] = Wf; return Wf
def variant_free(f, ac):
    if F.FITS is not None and (f.home, ac) not in F.FITS: return None, 'לא נכנס בעמדה'
    Wf = world_without(f); got = {}
    def acc(a):
        h = F.exact_flight(Wf, a, m=MARG, skip_ids=set(TUG.get(f.id, [])), vkv=1.0)
        if h: got.setdefault('rej', []).append(h); return False
        tg = {}
        for vid in TUG.get(f.id, []):
            tr, w = tug_variant(vid, f, a)
            if not tr: got.setdefault('rej', []).append(('גרר', vid)); return False
            tg[vid] = dict(trip=tr, w=w)
        got['tugs'] = tg; return True
    R, why = (F.plan_flight2 if os.environ.get('FT2_SEG') else F.plan_flight)(Wf, f.home, ac, getattr(f, 'airline', None), phase=int(f.legs[0]['t0']) % F.N, accept=acc)
    if not R: return None, why + (' · נדחו %s' % got['rej'][:3] if got.get('rej') else '')
    a = R['a']; a.id = f.id; L = a.legs[-1]
    return dict(ac=ac, L=a.L, W=a.W, legs=a.legs, park=[round(L['t0'], 2), round(L['t1'], 2)], ex=R['best']['ex'], prof='free', ds=round(a.legs[0]['t0'] - f.legs[0]['t0'], 1), ob0=f.legs[-1]['t0'], dob=round(L['t0'] - f.legs[-1]['t0'], 1), tugs=got['tugs']), 'נכנס (לו״ז חדש)'
def variant_clone(f, ac):
    # "אותו מסלול": כשקו העצירה של הסוג = של הטיסה שבלוח — כל הרגליים של הלוח (אותם מקומות ואותם זמנים), רק הסוג משתנה; הגרר — אותה נסיעה.
    # כך כל מה שמתוזמן בטעינה (הכבודה, הנוסעים, השירות, s15k) נשאר בדיוק — נבדק במדויק מול כל מה שרץ (המטוס הגדול יותר — מול הרכבים במקומות של היום)
    if F.FITS is not None and (f.home, ac) not in F.FITS: return None, 'לא נכנס בעמדה'
    if abs(F.M.ng_stop(f.home, ac)[1] - F.M.ng_stop(f.home, f.model)[1]) > float(os.environ.get('FT2_CLONE_TOL', 25)): return None, 'קו עצירה אחר (%.0f פיקס׳)' % (F.M.ng_stop(f.home, ac)[1] - F.M.ng_stop(f.home, f.model)[1])
    a = M.Actor(f.id, 'ac', ac, f.home, M.D.ACT[ac][0], M.D.ACT[ac][1]); a.airline = getattr(f, 'airline', None); a.legs = [dict(g) for g in f.legs]
    s0 = f.legs[0]['t0']
    hs = F.static_hit(Wd, a, s0, s0 + F.T, f.home)
    if hs: return None, 'חונה ' + hs[0]
    h = F.exact_flight(Wd, a, m=MARG, skip_ids={f.id} | set(TUG.get(f.id, [])), vkv=1.0)
    if h: return None, 'נוגע ב-%s (%.0f)' % (h[1], h[0] % F.T)
    ow = F.flight_rwy_wins(f); others = [b for b in Wd.busy if not any(abs(b[0] - w[0]) < .01 and abs(b[1] - w[1]) < .01 for w in ow)]
    if not all(F.rwy_ok(w, ac, others, kd=F.win_kind(a, w)) for w in F.flight_rwy_wins(a)): return None, 'המסלול (כבד)'
    L = a.legs[-1]
    return dict(ac=ac, L=a.L, W=a.W, legs=a.legs, park=[L['t0'], L['t1']], ex='=', prof='clone', ds=0, ob0=L['t0'], dob=0, tugs={}), 'נכנס (אותו מסלול)'
res = {}
for f in FL:
    if ONLY and f.home not in ONLY: continue
    if f.home in FIXED: continue
    row = dict(stand=f.home, base=f.model, airline=getattr(f, 'airline', None), ok=[], no={}, tugs=TUG.get(f.id, []))
    for ac in TYPES:
        if ac == f.model or ac not in M.D.ACT or not allowed(f.home, ac): continue
        t1 = time.time()
        if FREE and (f.home + ':' + ac) not in FREE: continue
        V, why = variant_clone(f, ac) if os.environ.get('FT2_CLONE') else (None, '')
        if not V and os.environ.get('FT2_CLONE') != 'only': V, why = variant_tc(f, ac)
        if not V and (f.home + ':' + ac) in FREE: V, why = variant_free(f, ac)
        if V: row['ok'].append(V)
        else: row['no'][ac] = why
        print(f.id, f.home, f.model[3:5], '→', ac[3:5], 'כן (%s, %s, דחיפה %+.0f, עצירה %+.0f, גרר %s)' % (V['ex'], V['prof'], V['ds'], V['dob'], {k: x['w'] for k, x in V['tugs'].items()}) if V else 'לא: ' + why[:200], '%.1f ש׳' % (time.time() - t1), flush=True)
    res[f.id] = row
json.dump(res, open(outp, 'w'), ensure_ascii=False)
print('סה״כ', {k: [v['ac'][3:5] for v in r['ok']] for k, r in res.items()})
