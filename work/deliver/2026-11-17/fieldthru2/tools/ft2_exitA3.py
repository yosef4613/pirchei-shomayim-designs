# -*- coding: utf-8 -*-
# ft2_exitA3.py <world.json> <out_world.json> — fieldthru2 (D‑701): כל הנוחתים (09) שיוצאים היום ב-A4 (x 9190) — יוצאים ב-A3 החדש (x 8345) אם זה נכנס:
# אותה גישה ואותה נגיעה, גלגול קצר יותר (2,945 פיקס׳ במקום 3,790 — המסלול פנוי ~2 ש׳ מוקדם יותר), ההסעה מ-A3 החדש לעמדה; נבדק במדויק מול כל מה שרץ
# (בלי הטיסה עצמה והגרר שלה), והעמידה ≥ המינימום. אחר כך — כמה המסלול תפוס, והעולם החדש למחולל (ft2_gen.py)
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
os.environ['FT2_D701'] = '1'
import ft_sim as F
import ft2_sim
M = F.M; T = F.T
W = json.load(open(sys.argv[1])); outp = sys.argv[2]
TUG = {}
for v in W['veh']:
    for g in v['legs']:
        if g.get('att'): TUG.setdefault(g['att'], []).append(v['id'])
def busy(FL):
    s = 0.0
    for a in FL:
        for w in F.flight_rwy_wins(a): s += w[1] - w[0]
    return s / T * 100
FL0 = [F.actor(o) for o in W['flights']]; print('המסלול תפוס לפני: %.1f%%' % busy(FL0), flush=True)
Wd = F.World(W); changed = []
for i, o in enumerate(W['flights']):
    f = F.actor(o); L = f.legs; air = [g for g in L if g.get('f') == 4]
    if len(air) < 2: continue
    sa = air[1]['t0']; arr_i = L.index(air[1]); park = L[-1]
    # היציאה של היום: x של הרגל שאחרי הגלגול
    xs = [g['p'][-1][0] for g in L[arr_i + 1:arr_i + 3]]
    if not xs or min(abs(x - F.A3) for x in xs) > 150: continue
    C3, _ = F.arr1(f.home, f.model, 'A3N')
    if C3 is None: print(f.id, 'אין הסעה מ-A3'); continue
    ob = sa + C3.t; s0 = L[0]['t0']
    if s0 + T - ob < F.MINPARK.get(f.model, 300): print(f.id, 'העמידה קצרה'); continue
    a = M.Actor(f.id, 'ac', f.model, f.home, f.L, f.W); a.airline = getattr(f, 'airline', None)
    a.legs = [dict(g) for g in L[:arr_i]] + [dict(g, t0=round(g['t0'] + sa, 2), t1=round(g['t1'] + sa, 2)) for g in C3.legs] + [dict(p=[list(C3.legs[-1]['p'][-1])], t0=round(ob, 2), t1=round(s0 + T, 2), h=round(F.S_, 4), f=0)]
    # הגישה של הלוח (הרגל שנגמרת בנגיעה) — C3 מתחיל באותה גישה; הרגליים שלפני sa נשארות
    h = F.exact_flight(Wd, a, m=.5, skip_ids={f.id} | set(TUG.get(f.id, [])), vkv=1.0)
    if h: print(f.id, 'נוגע ב-', h[1], h[0]); continue
    if F.static_hit(Wd, a, s0, s0 + T, f.home): print(f.id, 'חונה'); continue
    W['flights'][i] = F.ser(a); W['flights'][i]['airline'] = o.get('airline'); W['flights'][i].update({k: v for k, v in o.items() if k in ('ft', 'kind', 'ftu')})
    Wd.FL = [x for x in Wd.FL if x.id != f.id] + [a]; Wd.PC = None; F.world_cache(Wd)
    changed.append(f.id); print(f.id, 'יוצא ב-A3 החדש · העמידה %+.0f ש׳' % (L[-1]['t0'] - ob), flush=True)
FL1 = [F.actor(o) for o in W['flights']]; print('המסלול תפוס אחרי: %.1f%% · שונו %d: %s' % (busy(FL1), len(changed), changed))
json.dump(W, open(outp, 'w'))
