# ft_verify.py <world.json> <result.json> — הבדיקה המדויקת של הכול אחרי התוספת (s15SimAudit: מטוס × מטוס / רכב / חונה, כל 0.5 ש׳) + המסלול (fieldcalc)
import sys, json, ft_sim as F
Wj = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2]))
rep = {v['id']: v for v in R['veh']}
FL = [F.actor(o) for o in Wj['flights']] + [F.actor(o) for o in R['flights']]
VH = [F.actor(rep.get(o['id'], o)) for o in Wj['veh']] + [F.actor(v) for v in R['veh'] if v['id'] not in {o['id'] for o in Wj['veh']}]
act = {q[0] for q in Wj['sched']} | {q[0] for q in R['sched']}
PK = [F.pk_actor(s, a) for s, a in Wj['parked'].items() if a and s not in act]
TW = F.ffr3_actors(Wj.get('ffr3'))
iss = F.exact_check(FL + TW, VH, PK, dt=.5)
bad, occ, nw = F.rwy_check(FL)
pairs = {}
for t, a, b in iss: pairs.setdefault(a + ' × ' + b, []).append(t)
print('טיסות', len(FL), '· תנועות ב-1800 ש׳', round(2 * len(FL) * 1800 / F.T, 1), '· חפיפות', len(iss), '· זוגות', {k: (len(v), v[0]) for k, v in list(pairs.items())[:12]}, '· המסלול: הפרות', len(bad), bad[:4], 'תפוס %', occ)
sys.exit(1 if iss or bad else 0)
