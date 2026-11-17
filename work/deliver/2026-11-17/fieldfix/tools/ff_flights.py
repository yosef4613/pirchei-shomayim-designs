# -*- coding: utf-8 -*-
# ff_flights.py <sim_dump.json> <out.json> [מועמדים] — fieldfix: תמהיל הטיסות (מנהלים GA1 / הענקים P1, P6 / משא C1) בכלי של S15 (s15_sim.py:
# make_flight / departure / arrival / takeoff / tug / side / ac_conflict) — מול כל מה שרץ במשחק (הסימולציה אחרי כל העטיפות, מ-dump_sim.js), בלי לערוך את 019l.
import sys, json, math, io, contextlib
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-10/s15/tools')
with contextlib.redirect_stdout(io.StringIO()):
    import s15_design as D, s15_sim as S
src, out = sys.argv[1], sys.argv[2]
WANT = (sys.argv[3] if len(sys.argv) > 3 else 'GA1,P6,P1,C1').split(',')
SIM = json.load(open(src, encoding='utf-8')); T = S.T
# ---- הכלל של המסלול — של fieldcalc (deliver/2026-11-17/fieldcalc/for_fieldfix_rwy_rule.txt, ‏fc_sim.py; המתאם 17.11: הכלל שלו גובר):
#   rwy_wins: "תפוס" רק כשהמטוס באמת על המסלול (x 4950–9350, צפונית לקו ההמתנה, נמוך מ-40) — דגימה כל 0.25 ש׳ (במקום כל רגל הגישה);
#   clear: מרווח 3 ש׳, ועוד 8 אחרי מטוס כבד (LG / MW / CG / HC) — לפי מי שלפני ומי שאחרי. FF_RULE=s15 — הכלל הישן (להשוואה).
import os
HEAVY = {'AC-LG-01', 'AC-MW-01', 'AC-CG-01', 'AC-HC-01'}; CUR = [None]
if os.environ.get('FF_RULE', 'fc') == 'fc':
    def _rwy_wins(a, after=None):
        W = []; cur = None
        for g in a.legs:
            if after is not None and g['t1'] < after - 1e-6: continue
            if not any(p[1] < S.HOLD - 10 and 4900 <= p[0] <= 9400 for p in g['p']) and not (len(g['p']) >= 2 and g['p'][0][0] < 4950 and g['p'][-1][0] >= 4950 and g['p'][-1][1] < S.HOLD):
                if cur is not None: W.append(cur); cur = None
                continue
            t = g['t0'] if after is None else max(g['t0'], after)
            while t <= g['t1'] + 1e-6:
                P = S.evalp(a, t); on = bool(P) and P[3] < 40 and 4900 <= P[0] <= 9400 and P[1] < S.HOLD - 10
                if on and cur is None: cur = [t, t]
                elif on: cur[1] = t
                elif cur is not None: W.append(cur); cur = None
                t += .25
        if cur: W.append(cur)
        return [w + [a.model] for w in W]
    def _rwy_busy(a, after=None):
        W = _rwy_wins(a, after); return W[0] if W else None
    def _clear(b, busy, gap=3):
        m2 = b[2] if len(b) > 2 else CUR[0]
        for q in busy:
            x0, x1 = q[0], q[1]; m1 = q[2] if len(q) > 2 else None
            for k in (-T, 0, T):
                if not (b[0] >= x1 + k + gap + (8 if m1 in HEAVY else 0) or x0 + k >= b[1] + gap + (8 if m2 in HEAVY else 0)): return False
        return True
    S.rwy_wins = _rwy_wins; S.rwy_busy = _rwy_busy; S.clear = _clear
NEED = {'GA1': 250, 'P1': 470, 'P6': 470, 'C1': 440}   # זמן העמידה המינימלי — מטריצת השירות של fieldcalc (מנהלים 240–260, ‏LG ‏470, ‏CG ‏440)
def actor(o):
    a = S.Actor(o['id'], o['kind'], o['model'], o['home'], o['L'], o['W']); a.legs = o['legs']
    if o.get('airline'): a.airline = o['airline']
    return a
FL0 = [actor(o) for o in SIM['flights']]
V0 = [actor(o) for o in SIM['veh'] if not any(g.get('att') for g in o['legs'])] + [actor(o) for o in SIM.get('tows', [])]
ATT = [actor(o) for o in SIM['veh'] if any(g.get('att') for g in o['legs'])]   # הגררים (צמודים לאף בדחיפה) — נבדקים, אבל בלי הרגל הצמודה
V0 += ATT
for o in SIM.get('ffr3', []): V0.append(actor(o))   # הגרירות של R3 (fieldfix) — אם נמסרו
def spot_statics():   # הרכבים שחונים קבוע (S15D.spots שלא בסימולציה) — כמו s15StaticFleet; גם הם בבדיקה (s15k_fleet ראה אותם, הכלי הקודם לא)
    mov = {v['id'] for v in SIM['veh']}; L = []
    for vid, sp in SIM['spots'].items():
        if vid in mov: continue
        r = sp['rect']; w, h = r[2] - r[0], r[3] - r[1]; x = S.Actor('SP-' + vid, 'veh', 'X', sp.get('home', ''), max(w, h), min(w, h))
        x.legs = [dict(p=[[(r[0] + r[2]) / 2, (r[1] + r[3]) / 2]], t0=-T, t1=3 * T, h=(math.pi / 2 if h >= w else 0), f=0)]; L.append(x)
    return L
SPV = spot_statics()
def statics(skip):
    L = []
    for q in SIM['stat']:
        if q['heli'] or q['key'] == 'PK-' + skip: continue
        if q['id'] not in D.ACT: continue
        x = S.Actor(q['key'], 'ac', q['id'], q['key'][3:], *D.ACT[q['id']]); x.legs = [dict(p=[[q['x'], q['y']]], t0=-T, t1=3 * T, h=q['th'], f=0)]; L.append(x)
    return L
AL = {'P1': 'Confetti Air', 'P6': 'Aurelia Air', 'GA1': 'GA', 'C1': 'Crateway Cargo'}
AC = {'P1': 'AC-LG-01', 'P6': 'AC-LG-01', 'GA1': 'AC-BJ-01', 'C1': 'AC-CG-01'}
SOUTH = {'R2', 'GA6', 'GA1'}
def dep_west(a, sid, ac, t0):   # C1 — ממערב ל-A1: הזנב מערבה, האף מזרחה, ואז מזרחה עד A1 וצפונה (כמו dep_c1 של s15i)
    p0 = S.ng_stop(sid, ac); a.t = t0; R = 120
    P = S.Path(p0, S.N_).go(y=S.TACY + R).tr(S.W_, R)
    a.move(P.P, S.PUSH, S.PUSH * .6, rev=True, flags=2); a.wait(a.legs[-1]['p'][-1], S.E_, a.t + 14, flags=1)
    q = a.legs[-1]['p'][-1]; P = S.Path(q, S.E_).go(x=S.A1 - 90).tr(S.N_, 90).go(y=S.HOLD + 40)
    a.move(P.P, S.TAXI, 18, flags=1); return a
def make(sid, ttd, tdep, busy):
    ac, al = AC[sid], AL[sid]; L, W = D.ACT[ac]; a = S.Actor('FL-' + sid, 'ac', ac, sid, L, W); a.airline = al
    if sid == 'C1': dep_west(a, sid, ac, tdep)
    else: S.departure(a, sid, ac, tdep, via_c=sid in SOUTH)
    base = [dict(g) for g in a.legs]; t_hold = a.t; t_go = t_hold + 4
    while True:
        a.legs = [dict(g) for g in base]; a.t = t_hold; S.takeoff(a, ac, t_go); b = S.rwy_busy(a, after=t_hold)
        if S.clear(b, busy): break
        t_go += 2
        if t_go > t_hold + 200: return None
    tw = S.rwy_busy(a, after=t_hold); t_air = a.t; ttd2 = ttd
    while ttd2 - 12 < t_air: ttd2 += T
    n0 = len(a.legs); S.arrival(a, sid, ac, ttd2, remote=True if sid in SOUTH else None)
    if a.legs[n0]['t0'] < t_air: return None
    ba = S.rwy_busy(a, after=a.legs[n0]['t0'])
    if not S.clear(ba, busy + [tw]): return None
    if a.t > tdep + T - 30: return None
    a.wait(a.legs[-1]['p'][-1], S.S_, tdep + T, flags=0); return a
def veh_conflict(v, others, dt=1.0):   # כמו ac_conflict, בלי הרגעים שבהם הגרר צמוד לאף (f 16 — חלק מהמטוס, כמו ב-S15 check)
    for i in range(int(T / dt)):
        t = i * dt; P = S.evalp(v, t)
        if not P or P[4] == 16: continue
        A = S.boxes(v, P)
        for b in others:
            Q = S.evalp(b, t)
            if not Q or (b.kind == 'veh' and Q[4] == 16): continue
            if any(S.obb_hit(p, q) for p in A for q in S.boxes(b, Q)): return (t, b.id)
    return None
def ser(a):
    d = dict(id=a.id, kind=a.kind, model=a.model, home=a.home, L=a.L, W=a.W, legs=a.legs, **({'airline': a.airline} if hasattr(a, 'airline') else {}))
    if a.kind == 'ac':   # כמו s15_sim.export: park — הזמן בעמדה (השרוולים, הלוחות, הצוות)
        W_ = [g for g in a.legs if g.get('h') is not None and g.get('f', 1) == 0]
        if W_: g = max(W_, key=lambda g: g['t1'] - g['t0']); d['park'] = [round(g['t0'], 3), round(g['t1'], 3)]
    return d
FL = list(FL0); VV = list(V0); res = []; log = []
for sid in WANT:
    busy = [w for a in FL for w in S.rwy_wins(a)]
    ST = statics(sid) + SPV; others = FL + VV + ST
    best = None; tried = 0
    for tdep in range(0, T, 6):
        for dtd in (range(60, T - 60, 6) if os.environ.get('FF_SCAN', 'up') == 'up' else range(T - 60, 180, -6)):   # מהנחיתה המוקדמת — העמידה הארוכה ביותר לכל המראה (הסדר הישן — מהמאוחרת — מצא את הקצרה)
            tried += 1
            CUR[0] = AC[sid]; a = make(sid, (tdep + dtd) % T, tdep, busy)
            if not a: continue
            with contextlib.redirect_stdout(io.StringIO()):
                hit = S.ac_conflict(a, [o for o in others if o.id != 'FL-' + sid], dt=1.0)
            if hit: continue
            w = a.legs[-1]['t1'] - a.legs[-1]['t0']
            if not best or w > best[3]: best = (a, (tdep + dtd) % T, tdep, w)
            break
        if best and best[3] >= NEED.get(sid, 240): break
    if not best: log.append(sid + ': אין חלון במסלול / בהסעה בלי חפיפה (נוסו ' + str(tried) + ')'); continue
    if best[3] < NEED.get(sid, 0) and os.environ.get('FF_STRICT', '1') == '1': log.append(sid + ': החלון הארוך ביותר ' + str(round(best[3])) + ' ש׳ בעמדה — פחות מהשירות (' + str(NEED[sid]) + ') — לא נכנס'); continue
    a, ttd, tdep, w = best
    # הגרר (הדחיפה) — הכלי של S15 (tug); אם אין לו בית בעמדה — בלי
    S.FL = FL + [a]; VT = []
    vid = {'P1': 'PT-P1', 'P6': 'PT-P6', 'GA1': 'PT-GA1', 'C1': None}[sid]
    if sid == 'GA1':
        try:
            v = S.Actor('PT-GA1', 'veh', 'LV-PT-01', 'AIR-GSE-GA1|GA2', 44, 22); g = a.legs[0]; t_push = g['t0']; p0 = g['p'][0]
            P = D.POCKETS['AIR-GSE-GA1|GA2']['rect']; home = [(P[0] + P[2]) / 2, (P[1] + P[3]) / 2]
            off = S.NGF[a.model] * a.L + v.L / 2 + 4; front = [p0[0], p0[1] + off]
            out_ = [home, [home[0], front[1] + 12], [front[0], front[1] + 12], front]; dur = 2 * S.plen(out_) / (40 + 8)
            v.t = t_push - dur - 6; v.move(out_, 40, 8); v.wait(front, S.N_, t_push, flags=8)
            v.legs.append(dict(p=[g['p'][0], g['p'][-1]], t0=g['t0'], t1=g['t1'], att=a.id, f=16)); v.t = g['t1']
            q = g['p'][-1]; h = S.E_; nose = [q[0] + off * math.cos(h), q[1] + off * math.sin(h)]; v.wait(nose, h + math.pi, v.t + 1, flags=8)
            ty = (D.SVC['AIR-GA_SPUR']['rect'][1] + D.SVC['AIR-GA_SPUR']['rect'][3]) / 2
            back = [nose, [nose[0], ty], [home[0], ty], home]; v.move(back[:2], 45, 20); v.move(back[1:], 20, 8); v.wait(home, S.N_, t_push + T - dur - 6)
            hit = veh_conflict(v, FL + [a] + VV + ST)
            if hit: log.append(sid + ': הגרר PT-GA1 — חפיפה ' + str(hit)[:120] + ' (בלי)')
            else: VT.append(v)
        except Exception as e: log.append(sid + ': הגרר PT-GA1 — ' + str(e)[:160])
        vid = None
    if vid and vid in D.SPOTS and not any(v.id == vid for v in VV):
        try:
            v = S.tug(vid, sid)
            with contextlib.redirect_stdout(io.StringIO()):
                hit = veh_conflict(v, FL + [a] + VV + ST)
            if hit: log.append(sid + ': הגרר ' + vid + ' — חפיפה ' + str(hit)[:120] + ' (בלי גרר)')
            else: VT.append(v)
        except Exception as e: log.append(sid + ': הגרר — ' + str(e)[:100])
    elif vid:   # הגרר כבר משרת עמדה אחרת (PT-GA ל-GA6): נסיעה נוספת בתוך ההמתנה שלו בבית — הרגליים של tug() משולבות בלו״ז שלו
        try:
            old = [v for v in VV if v.id == vid][0]; v = S.tug(vid, sid); trip = [dict(g) for g in v.legs if not (g.get('h') is not None and g.get('f', 1) == 0 and len(g['p']) == 1 and g is v.legs[-1])]
            t_a, t_b = trip[0]['t0'], trip[-1]['t1']; W0 = None
            for k in (0, T, -T, 2 * T):
                for i, g in enumerate(old.legs):
                    if g.get('f', 1) == 0 and g.get('h') is not None and g['t0'] + 1 <= t_a + k and t_b + k <= g['t1'] - 1: W0 = (i, k); break
                if W0: break
            if not W0: raise Exception('אין חלון בבית')
            i, k = W0; g = old.legs[i]
            for q in trip: q['t0'] += k; q['t1'] += k
            new = S.Actor(old.id, old.kind, old.model, old.home, old.L, old.W)
            new.legs = old.legs[:i] + [dict(g, t1=t_a + k)] + trip + [dict(g, t0=t_b + k)] + old.legs[i + 1:]
            with contextlib.redirect_stdout(io.StringIO()):
                hit = veh_conflict(new, [o for o in FL + [a] + VV + ST if o.id != vid])   # בלי המטוס שלו (הדחיפה — הגרר צמוד לאף, כמו ב-S15)
            if hit: log.append(sid + ': הגרר ' + vid + ' (נסיעה נוספת) — חפיפה ' + str(hit)[:120])
            else: VV = [x for x in VV if x.id != vid]; VT.append(new); log.append(sid + ': ' + vid + ' — נסיעה נוספת ' + str(round(t_a + k, 1)) + '–' + str(round(t_b + k, 1)))
        except Exception as e: log.append(sid + ': הגרר המשותף — ' + str(e)[:120])
    FL.append(a); VV += VT
    res.append(dict(sid=sid, flight=ser(a), sched=[sid, a.model, a.airline, ttd, tdep], veh=[ser(v) for v in VT], window=[round(a.legs[-1]['t0'], 1), round(a.legs[-1]['t1'], 1)], rwy=S.rwy_wins(a)))
    log.append(sid + ': ' + a.model + ' ' + a.airline + ' · ממריא ' + str(tdep) + ' · נוחת ' + str(ttd) + ' · בעמדה ' + str(round(w)) + ' ש׳' + (' · גרר ' + VT[0].id if VT else ''))
json.dump(dict(add=res, log=log), open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('\n'.join(log))
