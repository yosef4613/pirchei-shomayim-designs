# -*- coding: utf-8 -*-
# ft2_diag.py <world.json> <עמדה> <סוג> [יציאה] — fieldthru2: למה אין חלון לנחיתה לעמדה בדרום — לכל שחקן בשדה: בכמה מתוך 720 הזמנים האפשריים
# הנחיתה + ההסעה (התבנית של ft_sim.arr1) נוגעת בו; והזמנים עם הכי מעט נוגעים — מי הם, ואיפה (x, y)
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
if os.environ.get('FT2_D701'): import ft2_sim
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
import ft_sim as F
M = F.M
W = json.load(open(sys.argv[1])); sid = sys.argv[2]; ac = sys.argv[3]; ex = sys.argv[4] if len(sys.argv) > 4 else 'A3'
C3, _ = F.arr1(sid, ac, ex); I, C, n = F.template(C3, 0, C3.t)
actors = [F.actor(o) for o in W['flights']] + [F.actor(o) for o in W['veh']] + [F.actor(o) for o in W.get('heli', [])] + F.ffr3_actors(W.get('ffr3'))
hit = collections.Counter(); per = np.zeros(F.N, dtype=np.int64); who = collections.defaultdict(set)
for a in actors:
    o = F.Occ(); o.add_actor(a, vk=(F.VK if a.kind == 'veh' else 1.0))
    for s in range(F.N):
        h = o.o[(s + I) % F.N, C]
        if h.any():
            hit[a.id] += 1; per[s] += 1; who[s].add(a.id)
    del o
print('הנחיתה ל-%s (%s, יציאה %s): %.0f ש׳ מתחילת הגישה עד העצירה' % (sid, ac, ex, C3.t))
print('נוגעים (בכמה זמנים מתוך 720):', hit.most_common(14))
best = np.argsort(per)[:6]
for s in best: print('זמן', s, '· נוגעים', per[s], sorted(who[s]))
print('זמנים פנויים לגמרי:', int((per == 0).sum()))
