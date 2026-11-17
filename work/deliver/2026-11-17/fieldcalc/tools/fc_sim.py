#!/usr/bin/env python3
# fc_sim.py — fieldcalc 17.11: אימות החישוב במחולל של S15 עצמו (deliver/2026-11-10/s15/tools/s15_sim.py — לא משנים אותו; עותק בזיכרון עם 3 שינויים):
#   (1) rwy_wins: המסלול "תפוס" רק כשהמטוס באמת עליו — על הקרקע או נמוך מ-40 (במקום כל רגל הגישה מקצה העולם, ‏10.8 ש׳);
#   (2) clear: מרווח 3 ש׳ (במקום 8), ועוד 8 אחרי מטוס כבד (LG / MW / CG / HC) — כללי fc_calc.py;
#   (3) העמדות הדרומיות (R1–R3, ‏GA1–GA7) — דרך C ו-B (ב-s15_sim רק R2 / GA6).
# והלוח: PLAN של fc_calc.py. הבדיקות של המחולל נשארות כמו שהן: ac_conflict (מעטפות OBB של כל מטוס מול כל מטוס וכל חונה, כל 2 ש׳).
import sys, os, json, math, types
HERE = os.path.dirname(os.path.abspath(__file__))
S15T = os.path.join(HERE, '..', '..', '..', '2026-11-10', 's15', 'tools')
sys.path.insert(0, S15T)
src = open(os.path.join(S15T, 's15_sim.py'), encoding='utf-8').read()
cut = src.index('ST = static_actors()\nschedule()')
src = src[:cut]                                        # בלי הריצה של המודול (הלוח הישן והרכבים)
src = src.replace("via_c=sid in ('R2', 'GA6')", "via_c=sid.startswith(('R', 'GA'))").replace("remote=True if sid in ('R2', 'GA6') else None", "remote=True if sid.startswith(('R', 'GA')) else None")
# FC_WAIT: המתנות בדרך — אחרי הדחיפה (לפני ההסעה) WX[0] ש׳, ואחרי היציאה מהמסלול (בחיבור, מעבר לקו ההמתנה) WA[0] ש׳ — כמו התורים של המתכנן הישן
src = src.replace("WX = None", "")
src = src.replace("a.wait(a.legs[-1]['p'][-1], W_, a.t + 14, flags=1)  # הגרר מתנתק ומתרחק, המנועים מותנעים", "a.wait(a.legs[-1]['p'][-1], W_, a.t + 14 + WX[0], flags=1)  # הגרר מתנתק ומתרחק, המנועים מותנעים (+ המתנה בתור — fieldcalc)")
src = src.replace("a.move(P.P, PUSH, PUSH * .6, rev=True, flags=2); a.wait(a.legs[-1]['p'][-1], E_, a.t + 14, flags=1)", "a.move(P.P, PUSH, PUSH * .6, rev=True, flags=2); a.wait(a.legs[-1]['p'][-1], E_, a.t + 14 + WX[0], flags=1)")
src = src.replace("    a.move(P.P, 60, 70, flags=1)\n    q = a.legs[-1]['p'][-1]; s = D.STANDS[sid]; stop = ng_stop(sid, ac)", "    a.move(P.P, 60, 70, flags=1)\n    if WA[0] > 0: a.wait(a.legs[-1]['p'][-1], S_, a.t + WA[0], flags=1)   # fieldcalc: המתנה בחיבור, מעבר לקו ההמתנה\n    q = a.legs[-1]['p'][-1]; s = D.STANDS[sid]; stop = ng_stop(sid, ac)")
src = "WX = [0]; WA = [0]\n" + src
M = types.ModuleType('fc_s15'); M.__file__ = os.path.join(S15T, 's15_sim.py'); exec(compile(src, M.__file__, 'exec'), M.__dict__)
HEAVY = {'AC-LG-01', 'AC-MW-01', 'AC-CG-01', 'AC-HC-01'}
R = M.D.LOTS['AIR-RWY']['rect'] if hasattr(M.D, 'LOTS') and 'AIR-RWY' in getattr(M.D, 'LOTS', {}) else [5000, -810, 9300, -570]
def rwy_wins(a, after=None):
    # רק הרגליים שנוגעות במסלול (כמו המקור), ובתוכן — דגימה כל 0.25 ש׳: על המסלול ונמוך מ-40
    W = []; cur = None
    for g in a.legs:
        if after is not None and g['t1'] < after - 1e-6: continue
        if not any(p[1] < M.HOLD - 10 and R[0] - 50 <= p[0] <= R[2] + 50 for p in g['p']) and not (len(g['p']) >= 2 and g['p'][0][0] < R[0] and g['p'][-1][0] >= R[0] and g['p'][-1][1] < M.HOLD):
            if cur is not None: W.append(cur); cur = None
            continue
        t = g['t0'] if after is None else max(g['t0'], after)
        while t <= g['t1'] + 1e-6:
            P = M.evalp(a, t)
            on = bool(P) and P[3] < 40 and R[0] - 50 <= P[0] <= R[2] + 50 and P[1] < M.HOLD - 10
            if on and cur is None: cur = [t, t]
            elif on: cur[1] = t
            elif cur is not None: W.append(cur); cur = None
            t += .25
    if cur: W.append(cur)
    return W
MODEL = {}
def clear(b, busy, gap=3):
    for q in busy:
        x0, x1 = q[0], q[1]; m = q[2] if len(q) > 2 else CUR[0]
        for k in (-M.T, 0, M.T):
            w1 = gap + (8 if m in HEAVY else 0); w2 = gap + (8 if CUR[0] in HEAVY else 0)
            if not (b[0] >= x1 + k + w1 or x0 + k >= b[1] + w2): return False
    return True
CUR = [None]
WAITS = [(0, 0), (8, 0), (0, 8), (16, 0), (0, 16), (24, 8), (8, 24), (32, 0), (0, 32)]
M.rwy_wins = rwy_wins; M.clear = clear
if os.environ.get('FC_TAXI'): M.TAXI = float(os.environ['FC_TAXI'])      # בתוכנית: 90 בקטעים הישרים (≈ 17 קשר); היום 60
def make_flight(sid, ac, al, ttd, tdep, busy):
    CUR[0] = ac
    return M_make(sid, ac, al, ttd, tdep, busy)
M_make = M.make_flight
def schedule(plan):
    FL = []; busy = []; sched = []; miss = []
    M.ACTIVE = [(s, m, al) for s, m, al, n in plan]
    ST = M.static_actors(); M.ST = ST
    for k, (sid, ac, al, n) in enumerate(plan):
        done = False; CUR[0] = ac
        for tdep in [((k * 41) + d) % M.T for d in range(0, M.T, 12)]:
            for dtd in range(120, M.T - 60, 8):
                ttd = (tdep + dtd) % M.T
                ok = None
                for wx, wa in (WAITS if os.environ.get('FC_WAIT') else [(0, 0)]):
                    M.WX[0] = wx; M.WA[0] = wa
                    a = M.make_flight(sid, ac, al, ttd, tdep, busy)
                    if not a: continue
                    if M.ac_conflict(a, FL + ST): continue
                    ok = a; break
                M.WX[0] = 0; M.WA[0] = 0
                a = ok
                if not a: continue
                FL.append(a); busy += [[w[0], w[1], ac] for w in M.rwy_wins(a)]; sched.append((sid, ac, al, ttd, tdep)); done = True; break
            if done: break
        if not done: miss.append(sid)
        print('  ', sid, ac, 'נכנס' if done else 'לא נכנס', flush=True)
    return FL, sched, miss, busy
if __name__ == '__main__':
    import importlib.util
    spec = importlib.util.spec_from_file_location('fc', os.path.join(HERE, 'fc_calc.py')); fc = importlib.util.module_from_spec(spec); sys.argv = ['x']; spec.loader.exec_module(fc)
    plan = [r for r in fc.PLAN]
    # הסדר: הדרום (B) קודם, אחר כך הגדולים
    if os.environ.get('FC_ORDER') == 'big':   # הגדולים קודם (P1 / P6 / C1), אחר כך הצפון, ואז הדרום
        plan.sort(key=lambda r: (0 if r[1] in HEAVY else (1 if not r[0].startswith(('R', 'GA')) else 2), -M.D.ACT[r[1]][0]))
    else:
        plan.sort(key=lambda r: (0 if r[0].startswith(('R', 'GA')) else 1, -M.D.ACT[r[1]][0]))
    FL, sched, miss, busy = schedule(plan)
    occ = sum(w[1] - w[0] for w in busy)
    out = dict(flights=len(FL), moves720=2 * len(FL), moves1800=round(2 * len(FL) * 1800 / M.T, 1), rwy_occ=round(occ), rwy_util=round(occ / M.T * 100, 1), miss=miss,
               sched=sched, rwy=[[round(w[0], 1), round(w[1], 1), w[2]] for w in sorted(busy)])
    out['taxi'] = M.TAXI
    out['order'] = os.environ.get('FC_ORDER') or 'south'; out['waits'] = bool(os.environ.get('FC_WAIT'))
    json.dump(out, open(os.path.join(HERE, 'fc_sim_result%s%s%s.json' % ('_t%d' % M.TAXI if os.environ.get('FC_TAXI') else '', '_big' if os.environ.get('FC_ORDER') == 'big' else '', '_wait' if os.environ.get('FC_WAIT') else '')), 'w'), ensure_ascii=False, indent=1)
    print('במחולל של S15 (עם כללי fieldcalc): טיסות', out['flights'], '· תנועות ב-1800 ש׳', out['moves1800'], '· המסלול תפוס', out['rwy_util'], '% · לא נכנסו', miss)
