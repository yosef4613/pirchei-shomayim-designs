# ft_variety.py <world.json> <result.json> <out.json> — fieldthru: לכל עמדה בלוח — אילו סוגים נוספים (לפי stands_matrix של fieldcalc) נכנסים באותו חלון
# (אותה המראה ואותה נגיעה, הדחיפה וההסעה לפי הסוג), בלי חפיפה מול כל השאר — הבסיס לסבב של הסוגים בעמדה (הבעלים 12:40)
import sys, json, time, ft_sim as F
Wj = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); outp = sys.argv[3]
rep = {v['id']: v for v in R['veh']}
Wj['flights'] = [o for o in Wj['flights'] if o['id'] not in {f['id'] for f in R['flights']}] + R['flights']
Wj['veh'] = [rep.get(o['id'], o) for o in Wj['veh']] + [v for v in R['veh'] if v['id'] not in {o['id'] for o in Wj['veh']}]
Wj['sched'] = [q for q in Wj['sched'] if q[0] not in {x[0] for x in R['sched']}] + R['sched']
t0 = time.time(); Wd = F.World(Wj); print('world', round(time.time() - t0, 1), flush=True)
TUG = {}
for v in Wj['veh']:
    for g in v['legs']:
        if g.get('att'): TUG.setdefault(g['att'], set()).add(v['id'])
MODELS = ['AC-PR-01', 'AC-LT-01', 'AC-BJ-01', 'AC-CN-01', 'AC-TB-01', 'AC-TP-01', 'AC-RJ-01', 'AC-NB-01', 'AC-MW-01', 'AC-CG-01', 'AC-LG-01']
out = {}
ONLY = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else None
for f in list(Wd.FL):
    if ONLY and f.home not in ONLY: continue
    sid = f.home; cur = f.model; row = {'now': cur, 'ok': [], 'no': {}}
    for m in MODELS:
        if m == cur or (F.FITS is not None and (sid, m) not in F.FITS) or m not in F.D.ACT: continue
        a, why = F.variant_of(Wd, f, m, skip=TUG.get(f.id, ()))
        if a: row['ok'].append(m)
        else: row['no'][m] = why[:120]
    out[f.id] = row; print(f.id, sid, cur, '→ נכנסים:', [m[3:5] for m in row['ok']], '· לא:', {k[3:5]: v[:50] for k, v in row['no'].items()}, flush=True)
json.dump(out, open(outp, 'w'), ensure_ascii=False, indent=1)
