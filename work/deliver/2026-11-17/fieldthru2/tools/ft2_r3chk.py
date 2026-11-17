# -*- coding: utf-8 -*-
# ft2_r3chk.py <world.json> <seq.json> — fieldthru2: כל גרסה בסבב (והנסיעות של הגררים שלה) מול הגרירות של R3 בלילה (fieldfix, ‏FFR3 — בזמנים שנבחרו ב-019l2:FTS.add.r3),
# כמו הבדיקה fieldfix_r3: הקופסאות של S15, כל 0.5 ש׳, ועוד 6 ש׳ לפני ואחרי
import sys, os, json
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools')
import ft_sim as F
M = F.M; T = F.T
W = json.load(open(sys.argv[1])); S = json.load(open(sys.argv[2]))
R3 = json.loads(open('/home/user/tc_root/tc/pkg/work/src_game_t17_fieldthru2/parts/019l2_ft_sched.js', encoding='utf-8').read().split(',add:', 1)[1].split('};\n(function', 1)[0])['r3']
bad = 0; n = 0
for m in W.get('ffr3') or []:
    q = R3.get(m['id'])
    if not q: continue
    for nm, mm in (('out', q[0]), ('back', q[1])):
        L = m[nm]; ph = (2 * mm) % T
        tw = M.Actor('TW', 'ac', m.get('ac') or 'AC-RJ-01', 'R3', m.get('Lpx') or 300, F.FF_W.get(m.get('ac'), 150)); tw.legs = [dict(g, t0=g['t0'] + ph, t1=g['t1'] + ph) for g in L['legs']]
        for fid, x in S['seqs'].items():
            for j in set(x['seq']):
                if not j: continue
                v = x['vars'][j]; a = M.Actor(fid, 'ac', v['ac'], x['stand'], v['L'], v['W']); a.legs = v['legs']
                acts = [a] + [F.actor(dict(id=k, kind='veh', model='X', home='', L=44, W=22, legs=t)) for k, t in v['tugs'].items() if t.get('trip')] if False else [a]
                for vid, t in v['tugs'].items():
                    if t.get('trip'): z = M.Actor(vid, 'veh', 'X', '', 60, 22); z.legs = t['trip']; acts.append(z)
                for o in acts:
                    t = tw.legs[0]['t0'] - 6
                    while t <= tw.legs[-1]['t1'] + 6:
                        P = M.evalp(tw, min(max(t, tw.legs[0]['t0']), tw.legs[-1]['t1'])); Q = M.evalp(o, t % T) or M.evalp(o, t)
                        n += 1
                        if P and Q and (o.kind != 'veh' or Q[4] != 16) and any(M.obb_hit(p, qq) for p in M.boxes(tw, tuple(P[:3]) + (0, 0)) for qq in F.boxes_of(o, Q)):
                            print('נגיעה:', m['id'], nm, 'דקה', mm, '×', o.id, v['ac'][3:5], 'ב-%.1f' % (t % T)); bad += 1; break
                        t += .5
print('בדיקות', n, '· נגיעות', bad)
