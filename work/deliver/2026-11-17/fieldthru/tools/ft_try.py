import sys, json, time, ft_sim as F
dump = json.load(open(sys.argv[1])); order = sys.argv[2].split(',')
t0 = time.time(); Wd = F.World(dump); print('world', round(time.time() - t0, 1), 's · busy', len(Wd.busy), flush=True)
PLAN = {'P5': ('AC-NB-01', 'Zebrano', 'PT-P5'), 'P1': ('AC-LG-01', 'Aurelia Air', 'PT-P1'), 'P6': ('AC-LG-01', 'Mirage Jet', 'PT-P6'), 'C1': ('AC-CG-01', 'Crateway Cargo', 'PT-C'), 'R1': ('AC-RJ-01', 'Confetti Air', 'PT-R'),
        'GA2': ('AC-LT-01', 'GA', 'PT-GA'), 'GA3': ('AC-PR-01', 'GA', 'PT-GA'), 'GA4': ('AC-LT-01', 'GA', 'PT-GA'), 'GA5': ('AC-PR-01', 'GA', 'PT-GA'), 'GA7': ('AC-LT-01', 'GA', 'PT-GA')}
for k, sid in enumerate(order):
    ac, al, tug = PLAN[sid]; t1 = time.time(); got = {}
    def acc(a):
        v, why = F.plan_tug(Wd, tug, a)
        if v: got['v'] = v; got['w'] = why
        return v is not None
    R, why = F.plan_flight(Wd, sid, ac, al, phase=(k * 97) % F.N, accept=acc)
    print(sid, ac, why, R and {k2: (round(v, 1) if isinstance(v, float) else v) for k2, v in R['best'].items() if k2 != 'rw'}, 'גרר', got.get('w'), round(time.time() - t1, 1), 's', flush=True)
    if R: F.commit(Wd, sid, ac, al, R, [got['v']])
print('טיסות', len(Wd.FL), 'תנועות ב-1800', round(2 * len(Wd.FL) * 1800 / F.T, 1))
