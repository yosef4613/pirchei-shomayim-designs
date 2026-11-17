# -*- coding: utf-8 -*-
# ft2_seq.py <world.json> <var.json> <out.json> — fieldthru2: הסבב של הסוגים בכל עמדה (5 סבבים = שעה) — נבדק סבב-סבב: בכל סבב כל הטיסות שלו יחד
# (הגרסאות של כל העמדות באותו סבב + הנסיעות של הגררים שלהן), במדויק (OBB כל 0.5 ש׳ — כמו s15SimAudit / ft_verify.py): מטוס × מטוס / רכב / חונה,
# הגררים שהשתנו × כל הרכבים (רק זוגות חדשים — לא מה שכבר היה בלוח), והמרווחים במסלול. סבב שנכשל — העמדה שנגעה חוזרת לסוג של הלוח בסבב הזה.
import sys, os, json, math, time, itertools
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
import ft_sim as F
M = F.M; T = F.T
W = json.load(open(sys.argv[1])); VAR = json.load(open(sys.argv[2])); outp = sys.argv[3]; K = int(os.environ.get('FT2_K', 5))
PREF = {'P1': ['AC-LG-01', 'AC-NB-01', 'AC-LG-01', 'AC-QJ-01', 'AC-RJ-01'], 'P2': ['AC-NB-01', 'AC-RJ-01', 'AC-NB-01', 'AC-QJ-01', 'AC-NB-01'], 'P3': ['AC-NB-01', 'AC-QJ-01', 'AC-NB-01', 'AC-RJ-01', 'AC-NB-01'],
        'P5': ['AC-RJ-01', 'AC-NB-01', 'AC-QJ-01', 'AC-RJ-01', 'AC-TP-01'], 'R2': ['AC-NB-01', 'AC-BJ-01', 'AC-NB-01', 'AC-CN-01', 'AC-NB-01'], 'GA2': ['AC-LT-01', 'AC-PR-01', 'AC-LT-01', 'AC-PR-01', 'AC-LT-01'],
        'P6': ['AC-RJ-01', 'AC-NB-01', 'AC-RJ-01', 'AC-QJ-01', 'AC-RJ-01']}
if os.environ.get('FT2_PREF'): PREF.update(json.load(open(os.environ['FT2_PREF'])))
BAN = set(x for x in os.environ.get('FT2_BAN', '').split(',') if x)   # "P5:AC-TP-01" — סוג שהשרוול לא מקבל בקו העצירה שלו (ft2_probe.js)
FLB = {o['id']: o for o in W['flights']}; VB = {v['id']: v for v in W['veh']}
# הגרסאות: 0 = הלוח
seqs = {}
for fid, r in VAR.items():
    sid = r['stand']; vars_ = [None] + [v for v in r['ok'] if (sid + ':' + v['ac']) not in BAN]
    pref = PREF.get(sid)
    if not pref or len(vars_) == 1: continue
    sq = []
    for m in pref[:K]:
        if m == r['base']: sq.append(0); continue
        j = next((i for i, v in enumerate(vars_) if v and v['ac'] == m), None); sq.append(j if j is not None else 0)
    seqs[fid] = dict(stand=sid, base=r['base'], vars=vars_, seq=sq)
def world_k(k):
    FL = []; trips = {}
    for o in W['flights']:
        S = seqs.get(o['id']); v = S['vars'][S['seq'][k]] if S else None
        if v is None: FL.append(F.actor(o)); continue
        a = M.Actor(o['id'], 'ac', v['ac'], o['home'], v['L'], v['W']); a.legs = v['legs']; a.airline = o.get('airline'); FL.append(a)
        for vid, t in v['tugs'].items(): trips.setdefault(vid, {})[o['id']] = t['trip']
    VH = []
    for o in W['veh']:
        if o['id'] not in trips: VH.append(F.actor(o)); continue
        base = F.base_trips(o); new = []; seen = set()
        for tr in base:
            att = next((g['att'] for g in tr if g.get('att')), None)
            if att and att in trips[o['id']]:
                seen.add(att); t2 = trips[o['id']][att]
                if t2: new.append(t2)          # None — הגרר של הלוח לא יוצא בסבב הזה (גרר אחר מהצי)
            else: new.append(tr)
        for att, t2 in trips[o['id']].items():
            if att not in seen and t2: new.append(t2)   # גרר חלופי — נסיעה נוספת
        if not new: VH.append(F.actor(dict(o, legs=[dict(p=[o['legs'][-1]['p'][0]], t0=0, t1=T, h=o['legs'][-1].get('h', F.S_), f=0)]))); continue
        home = o['legs'][-1]['p'][0]; hh = o['legs'][-1].get('h', F.S_)
        v = F.veh_from_trips(o['id'], o['model'], o['home'], o['L'], o['W'], home, hh, new); VH.append(v)
    return FL, VH, set(trips)
act = {q[0] for q in W['sched']}; PK = [F.pk_actor(s, a) for s, a in W['parked'].items() if a and s not in act]; TW = F.ffr3_actors(W.get('ffr3'))
def vpairs(VH, ids, dt=.5):
    out = set()
    for i in range(int(T / dt)):
        t = i * dt; P = []
        for a in VH:
            q = M.evalp(a, t)
            if not q or q[4] == 16: continue
            P.append((a, q))
        for a, qa in P:
            if a.id not in ids: continue
            A = F.boxes_of(a, qa)
            for b, qb in P:
                if b.id == a.id or abs(qa[0] - qb[0]) > 300 or abs(qa[1] - qb[1]) > 300: continue
                if qa[4] == 0 and qb[4] == 0: continue
                if any(M.obb_hit(x, y) for x in A for y in F.boxes_of(b, qb)): out.add(tuple(sorted((a.id, b.id))))
    return out
B0 = [F.actor(o) for o in W['flights']]; BV0 = [F.actor(o) for o in W['veh']]
TUGS = set(itertools.chain.from_iterable(t for S in seqs.values() for v in S['vars'] if v for t in v['tugs']))
basep = vpairs(BV0, TUGS); print('זוגות רכבים בלוח (קיימים):', sorted(basep), flush=True)
TWID = {a.id for a in TW}
def pairs_of(iss): return {(a, b) for t, a, b in iss if not (a in TWID and b in TWID)}
base_iss = pairs_of(F.exact_check(B0 + TW, BV0, PK, dt=.5)); print('זוגות בלוח של היום (כבר במשחק, לא נספרים):', sorted(base_iss), flush=True)
rep = []
PRI = ['P1', 'P6', 'P5', 'P2', 'P3', 'R2', 'R1', 'GA2', 'GA3']
def check(k):
    FL, VH, ch = world_k(k)
    iss = [(t, a, b) for t, a, b in F.exact_check(FL + TW, VH, PK, dt=.5) if (a, b) not in base_iss and not (a in TWID and b in TWID)]
    bad, occ, nw = F.rwy_check(FL); vp = vpairs(VH, ch) - basep
    return iss, vp, bad
def involved(fid, k, iss, vp, bad):
    S = seqs[fid]; v = S['vars'][S['seq'][k]]; ids = {fid} | (set(v['tugs']) if v else set())
    return any(a in ids or b in ids for t, a, b in iss) or any(a in ids or b in ids for a, b in vp) or any(x[1] == fid or x[3] == fid for x in bad)
order = sorted(seqs, key=lambda f: PRI.index(seqs[f]['stand']) if seqs[f]['stand'] in PRI else 99)
for k in range(K):
    want = {f: seqs[f]['seq'][k] for f in order}
    for f in order: seqs[f]['seq'][k] = 0
    for f in order:
        S = seqs[f]; cands = [want[f]] + [j for j in range(1, len(S['vars'])) if j != want[f]] if want[f] else []
        for j in cands:
            S['seq'][k] = j; t0 = time.time(); iss, vp, bad = check(k)
            if not involved(f, k, iss, vp, bad) and not iss and not vp and not bad:
                print('סבב %d · %s: %s ✓ (%.0f ש׳)' % (k + 1, S['stand'], S['vars'][j]['ac'][3:5], time.time() - t0), flush=True); break
            print('סבב %d · %s: %s ✗ %s %s' % (k + 1, S['stand'], S['vars'][j]['ac'][3:5], sorted({(a, b) for t, a, b in iss})[:3], sorted(vp)[:2]), flush=True); S['seq'][k] = 0
    iss, vp, bad = check(k); rep.append(dict(k=k, ok=not iss and not vp and not bad, types={S['stand']: (S['vars'][S['seq'][k]] or {'ac': S['base']})['ac'] for S in seqs.values()}))
for fid, S in seqs.items(): print(S['stand'], [(S['vars'][j] or {'ac': S['base']})['ac'][3:5] for j in S['seq']])
json.dump(dict(K=K, seqs=seqs, rep=rep), open(outp, 'w'), ensure_ascii=False)
print('ok' if all(r['ok'] for r in rep) else 'יש סבב שנכשל')
