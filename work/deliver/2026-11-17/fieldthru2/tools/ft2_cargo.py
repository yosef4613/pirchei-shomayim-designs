# -*- coding: utf-8 -*-
# ft2_cargo.py <world.json> <out.json> — fieldthru2: סבב המשא (המתאם 15:30: "CG ו-HC חייבים להיכנס בסבב הזה"): בסבב הזה הטיסות של C1 ושל C2 לא מגיעות
# (המטוסים "בדרך"), ורכבי המשא שלהן נשארים בבית — ובמקומן:
#   HC — המשא הענק על שתי העמדות יחד (CH; האף ב-y ‏710 — בתוך הגדר של המשחק, ft2_ch.py), או CG — מטען סילון ב-C1 (בלי C2 לידו).
# אותו מחולל (ft_sim.plan_flight / ft2_sim), מול כל מה שרץ במשחק בלי C1 / C2, והגרר מהצי (PT-C / PT-P1) — נבדק מול המטוסים והרכבים.
import sys, os, json, math, time
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ft_sim as F
import inspect as _ins
if os.environ.get('FT2_D701'): import ft2_sim
M = F.M; T = F.T
_src = _ins.getsource(F.tug_trip).replace("big = a.L > 600", "big = a.L > 600 or sid in ('P1', 'P6')"); exec(compile(_src, F.__file__, 'exec'), F.__dict__)
for _fn in ('plan_flight', 'plan_flight2'):
    _s = _ins.getsource(getattr(F, _fn)).replace("ac != 'AC-LG-01'", "ac not in ('AC-LG-01', 'AC-MW-01', 'AC-CG-01')"); exec(compile(_s, F.__file__, 'exec'), F.__dict__)
W = json.load(open(sys.argv[1])); outp = sys.argv[2]
CA = [4790, -60, 5760, 800]   # רחבת המשא המערבית (C1 / C2 / CH)
def touches(tr): return any(CA[0] <= p[0] <= CA[2] and CA[1] <= p[1] <= CA[3] for g in tr for p in g['p'])
RMF = {'FL-C1', 'FL-C2'}
W0 = dict(W); W0['flights'] = [f for f in W['flights'] if f['id'] not in RMF]; W0['sched'] = [q for q in W['sched'] if q[0] not in ('C1', 'C2')]; W0['parked'] = dict(W['parked'], C1=None, C2=None, CH=None)   # במשחק הטיסות קיימות (בגרסה) — אין מטוס חונה קבוע ב-C1 / C2
neutral = {}; vv = []
for v in W['veh']:
    trs = F.base_trips(v); keep = [tr for tr in trs if not touches(tr) and not any(g.get('att') in RMF for g in tr)]
    if len(keep) == len(trs): vv.append(v); continue
    home = v['legs'][-1]['p'][0]; hh = v['legs'][-1].get('h', F.S_)
    if keep: nv = F.ser(F.veh_from_trips(v['id'], v['model'], v['home'], v['L'], v['W'], home, hh, keep)); nv['legs'] = nv['legs']
    else: nv = dict(v, legs=[dict(p=[home], t0=0, t1=T, h=hh, f=0)])
    neutral[v['id']] = [len(trs), len(keep)]; vv.append(dict(v, legs=nv['legs']))
W0['veh'] = vv
print('בסבב המשא — רכבים שנשארים בבית (נסיעות לפני / אחרי):', neutral, flush=True)
Wd = F.World(W0); print('world', len(Wd.FL), 'טיסות', flush=True)
# CH למשא הענק: האף ב-y 710 (בתוך הגדר — 019m:S15_POLY, ‏y 725); MINPARK — כמו מטען
F.SHIFT[('CH', 'AC-HC-01')] = F.D.STANDS['CH']['nose'] - 710.0
if F.FITS is not None: F.FITS.add(('CH', 'AC-HC-01'))
F.MINPARK.setdefault('AC-HC-01', 380); F.MINPARK['AC-CG-01'] = max(F.MINPARK.get('AC-CG-01', 340), 340)
VB = {v['id']: v for v in W0['veh']}
Wd.tug = {}
def tug_reg(vid):
    v = VB[vid]; home = v['legs'][-1]['p'][0]; hh = v['legs'][-1].get('h', F.S_)
    Wd.tug[vid] = dict(home=home, hh=hh, trips=F.base_trips(v), homeid=v['home'], L=v['L'], W=v['W'], new=[])
OV = F.Occ()
for v in Wd.VH: OV.add_actor(v, vk=1.3)
Wd.occV = OV
res = dict(neutral=neutral, flights={})
for key, sid, ac, al, tugs in (('HC', 'CH', 'AC-HC-01', 'Crateway Cargo', ('PT-C', 'PT-P1')), ('CG', 'C1', 'AC-CG-01', 'Boxline Cargo', ('PT-C', 'PT-P1'))):
    t0 = time.time(); got = {}
    for x in tugs: tug_reg(x)
    def acc(a):
        h = F.exact_flight(Wd, a)
        if h: got.setdefault('rej', []).append(h); return False
        for x in tugs:
            tr, why = F.plan_trip(Wd, x, a)
            if tr and 'V' in why: got['tr'] = tr; got['tug'] = x; got['w'] = why; return True
        got.setdefault('rej', []).append('גרר'); return False
    best = None
    for pf in ((F.plan_flight, F.plan_flight2) if os.environ.get('FT2_SEG2') else (F.plan_flight,)):
        R, why = pf(Wd, sid, ac, al, phase=0, accept=acc)
        if R: best = R; break
    if not best: print(key, sid, ac, 'לא:', why, got.get('rej', [])[:4], '%.0f ש׳' % (time.time() - t0), flush=True); res['flights'][key] = dict(ok=False, why=why); continue
    a = best['a']; a.id = 'FL-C1'; a.home = 'C1'; s = F.ser(a); s['airline'] = al
    print(key, sid, ac, 'נכנס · דחיפה %.0f · עמידה %.0f · יציאה %s · גרר %s %s' % (best['best']['s0'] % T, best['best']['park'], best['best']['ex'], got['tug'], got['w']), '%.0f ש׳' % (time.time() - t0), flush=True)
    res['flights'][key] = dict(ok=True, flight=s, tug=got['tug'], trip=got['tr'], stand=sid)
json.dump(res, open(outp, 'w'), ensure_ascii=False)
