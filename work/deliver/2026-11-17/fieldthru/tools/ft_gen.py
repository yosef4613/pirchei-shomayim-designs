# -*- coding: utf-8 -*-
# ft_gen.py <dump.json> <base019l.json> <out.json> <סדר העמדות> — fieldthru: מוסיף טיסות ללוח של S15SIM (ft_sim.py), עם גרר לכל טיסה, וכותב את התוספת לחלק של המשחק
import sys, os, json, time, math, ft_sim as F
dump = json.load(open(sys.argv[1])); base = json.load(open(sys.argv[2])); outp = sys.argv[3]; order = sys.argv[4].split(',')
DROP = [x for x, s_ in ((('BT-P1', 'P1'),) if not os.environ.get('FT_KEEP_BTP1') else ()) + (('CT-P1', 'P1'), ('CT-P6', 'P6'), ('BL-P6', 'P6')) + ((('TG-C', 'C1'),) if os.environ.get('FT_DROP_TGC') else ()) if s_ in order]   # TG-C נשאר (משרת גם את C2; הביקור ב-C1 בתוך העמידה של הטיסה)
t0 = time.time(); Wd = F.World(dump, DROP); print('world', round(time.time() - t0, 1), 's · busy', len(Wd.busy), '· flights', len(Wd.FL), '· veh', len(Wd.VH), flush=True)
PLAN = {'P2': ('AC-NB-01', 'Sunbeak', 'PT-P2'), 'P3': ('AC-NB-01', 'Tidewind Air', 'PT-P3'), 'P4': ('AC-RJ-01', 'Skyline Regional', 'PT-P4'), 'R2': ('AC-NB-01', 'Coral Coast', 'PT-R'), 'GA6': ('AC-LT-01', 'GA', 'PT-GA'),
        'P5': (os.environ.get('FT_P5', 'AC-RJ-01'), 'Zebrano', 'PT-P5'), 'P1': ('AC-LG-01', 'Aurelia Air', 'PT-P1'), 'P6': ('AC-LG-01', 'Mirage Jet', 'PT-P6'), 'C1': ('AC-CG-01', 'Crateway Cargo', 'PT-C'), 'R1': ('AC-RJ-01', 'Confetti Air', 'PT-R'),
        'GA7b': ('AC-LT-01', 'GA', 'PT-HGR'),
        'GA2': ('AC-LT-01', 'GA', 'PT-GA'), 'GA3': ('AC-PR-01', 'GA', 'PT-GA'), 'GA4': ('AC-LT-01', 'GA', 'PT-GA'), 'GA5': ('AC-PR-01', 'GA', 'PT-GA'), 'GA7': ('AC-LT-01', 'GA', 'PT-GA'), 'R3': ('AC-CN-01', 'GA', 'PT-R')}   # R1 / R3 — לפי FT_TYPES (מנהלים: AC-CN-01 / AC-BJ-01)
# הבעלים 17.11 ~10:05: "כל העמדות פעילות … גם בעמדות הגדולות — לא רק לענקים, גם לגדולים ובינוניים" — FT_TYPES=P6=AC-NB-01,C1=AC-TB-01 (הסוג בעמדה)
for _kv in [x for x in os.environ.get('FT_TUGS', '').split(',') if '=' in x]:   # הגרר של העמדה (AF: רכב אחר של הצי)
    _k, _v = _kv.split('='); PLAN[_k] = PLAN[_k][:2] + (_v,)
for _kv in [x for x in os.environ.get('FT_TYPES', '').split(',') if '=' in x]:
    _k, _v = _kv.split('='); PLAN[_k] = (_v, 'GA' if _v in ('AC-CN-01', 'AC-BJ-01', 'AC-LT-01', 'AC-PR-01') else PLAN[_k][1]) + PLAN[_k][2:]
BV = {v['id']: v for v in base['veh']}
for v in dump['veh']:
    if v['id'] in ('PT-C', 'BL-C') and v['id'] not in BV: BV[v['id']] = v
Wd.tug = {}
def tug_reg(vid):
    if vid in Wd.tug: return Wd.tug[vid]
    sp = dump['spots'][vid]; r = sp['rect']; home = [(r[0] + r[2]) / 2, (r[1] + r[3]) / 2]; hh = F.HH[sp.get('h', 'S')]
    trs = TUG_OVR[vid] if vid in TUG_OVR else (F.base_trips(BV[vid]) if (vid in BV and vid not in set(os.environ.get('FT_FRESH', '').split(','))) else [])
    if vid in BV: home = BV[vid]['legs'][-1]['p'][0]; hh = BV[vid]['legs'][-1]['h']
    Wd.tug[vid] = dict(home=home, hh=hh, trips=trs, homeid=sp.get('home', ''), L=(BV[vid]['L'] if vid in BV else (44 if vid in ('PT-GA', 'PT-R', 'PT-HGR') else 60)), W=(BV[vid]['W'] if vid in BV else 22), new=list(TUG_NEW.get(vid, [])))
    return Wd.tug[vid]
# C14.07: שדרוג הטיסות של היום (019l) לפרופיל של הישן — FT_UPG=FL-P3,FL-R2,... (אחת אחרי השנייה, כל אחת מול כל השאר אחרי השדרוג של הקודמות), עם הגרר שלהן מחדש
TUG_OVR = {}; TUG_NEW = {}; UPG = []
TUGOF = {'FL-P3': 'PT-P3', 'FL-P2': 'PT-P2', 'FL-P4': 'PT-P4', 'FL-R2': 'PT-R', 'FL-GA6': 'PT-GA'}
if os.environ.get('FT_UPG'):
    for fid in os.environ['FT_UPG'].split(','):
        f = next((x for x in Wd.FL if x.id == fid), None); vid = TUGOF.get(fid)
        if not f or not vid: continue
        a, why = F.upgrade_base(Wd, f, skip_tug={fid: [vid]})
        if not a: print('שדרוג', fid, '—', why[:200], flush=True); Wd.log.append('%s: לא שודרג (%s)' % (fid, why[:160])); continue
        T0 = tug_reg(vid); keep = [tr for tr in T0['trips'] if not any(g.get('att') == fid for g in tr)]; T0['trips'] = keep
        tr, w = F.plan_trip(Wd, vid, a)
        if not tr: T0['trips'] = keep + [x for x in F.base_trips(BV[vid]) if any(g.get('att') == fid for g in x)]; print('שדרוג', fid, '— אין גרר', flush=True); Wd.log.append('%s: לא שודרג (הגרר)' % fid); continue
        T0['trips'].append(tr); T0['new'].append(tr); TUG_OVR[vid] = T0['trips']; TUG_NEW[vid] = T0['new']
        i = Wd.FL.index(f); Wd.FL[i] = a; Wd.PC = [(o, Y) for o, Y in F.world_cache(Wd) if o.id != fid]; F.cache_add(Wd, a)
        x = F.M.Actor(vid + '#' + fid, 'veh', 'LV-PT-01', '', T0['L'], T0['W']); x.legs = tr; F.cache_add(Wd, x)
        ow = F.flight_rwy_wins(f); Wd.busy = [b for b in Wd.busy if not any(abs(b[0] - q[0]) < .01 and abs(b[1] - q[1]) < .01 for q in ow)] + [list(q) + [F.win_kind(a, q)] for q in F.flight_rwy_wins(a)]
        UPG.append(a); print('שדרוג', fid, '—', why[:220], 'גרר', vid, w, flush=True); Wd.log.append(fid + ': ' + why[:200])
    if UPG:
        ser_up = {a.id: F.ser(a) for a in UPG}
        for k, o in enumerate(dump['flights']):
            if o['id'] in ser_up: q = ser_up[o['id']]; q['airline'] = o.get('airline'); q['kind'] = o.get('kind', 'ac'); dump['flights'][k] = q
        for q in dump['sched']:
            for a in UPG:
                if q[0] == a.home: q[4] = round(a.legs[0]['t0'] % F.T, 2)
        lg = Wd.log; tug_keep = Wd.tug; Wd = F.World(dump, DROP); Wd.log = lg; Wd.tug = tug_keep; print('world (אחרי השדרוג)', len(Wd.FL), flush=True)
import os, random
SEED = int(os.environ.get('FT_SEED', 0)); RNG = random.Random(SEED); PH = [RNG.randrange(F.N) for _ in order] if SEED else [(k * 97) % F.N for k in range(len(order))]
if SEED and os.environ.get('FT_SHUF'): order = order[:int(os.environ.get('FT_KEEP', 0))] + RNG.sample(order[int(os.environ.get('FT_KEEP', 0)):], len(order) - int(os.environ.get('FT_KEEP', 0)))
# הרכבים של העולם (אחרי כל העטיפות) — טבלת שמירה לרכבים (כמו AO.B של הישן גם לרכבים), בלי אלה שמתוכננים כאן מחדש; הגררים ורכבי הצד בודקים גם מולה
MANAGED = {'PT-GA', 'PT-HGR', 'PT-R', 'PT-C', 'PT-P1', 'PT-P5', 'PT-P6', 'BT-P5', 'CT-P1', 'CT-P6', 'BL-P6'} | ({'TG-C'} if 'TG-C' in DROP else set()) | ({'BT-P1'} if 'BT-P1' in DROP else set())
if os.environ.get('FT_OCCV', '1') != '0':
    t1 = time.time(); Wd.occV = F.Occ()
    for v in Wd.VH:
        if v.id not in MANAGED: Wd.occV.add_actor(v, vk=float(os.environ.get('FT_VKV', 1.3)))   # הגודל המצויר (s15k_fleet בודק במידות הציור + העגלות) — לא הקופסה של הסימולציה
    print('occV', round(time.time() - t1, 1), 's', flush=True)
log = []
for k, sid in enumerate(order):
    ac, al, tug = PLAN[sid]; t1 = time.time(); got = {}
    if F.FITS is not None and (sid, ac) not in F.FITS: log.append('%s %s: לא נכנס בעמדה (stands_matrix של fieldcalc)' % (sid, ac)); print(log[-1], flush=True); continue
    tug_reg(tug)
    TUGS = [tug] + (['PT-HGR'] if sid.startswith('GA') else []) + ([x for x in os.environ.get('FT_TUG2_' + sid, '').split(',') if x])   # AF של הישן: גרר נוסף מהצי כשהראשון עסוק
    for x in TUGS: tug_reg(x)
    def acc(a):
        h = F.exact_flight(Wd, a)
        if h: got.setdefault('rej', []).append(h); return False
        for x in TUGS:
            tr, why = F.plan_trip(Wd, x, a)
            if tr: got['tr'] = tr; got['w'] = why; got['tug'] = x; return True
        return False
    R, why = (F.plan_flight2 if os.environ.get('FT_SEG') else F.plan_flight)(Wd, sid, ac, al, phase=PH[k], accept=acc, exits=tuple(os.environ.get('FT_EXITS', 'A3,A2').split(',')), links=tuple(os.environ.get('FT_LINKS', 'A1,A2').split(',')))
    line = '%s %s %s %s גרר %s %s %.1f ש׳' % (sid, ac, al, why, tug, got.get('w'), time.time() - t1) + (' · נדחו במדויק %d (%s)' % (len(got['rej']), got['rej'][:2]) if got.get('rej') else '')
    if R:
        b = R['best']; line += ' · דחיפה %.0f · %s · המתנה בקו %.0f · בדרך %.0f / %.0f · נגיעה %.0f · %s · עמידה %.0f' % (b['s0'] % F.T, b['ln'], b['w'], b.get('wq', 0), b.get('wa', 0), (b['sa'] + 10.8) % F.T, b['ex'], b['park'])
        tug = got['tug']; T0 = Wd.tug[tug]; T0['trips'].append(got['tr']); T0['new'].append(got['tr'])
        x = F.M.Actor(tug + '#' + sid, 'veh', 'LV-PT-01', '', T0['L'], T0['W']); x.legs = got['tr']
        F.commit(Wd, sid, ac, al, R, []); Wd.occ.add_actor(x, vk=F.VK); F.cache_add(Wd, R['a']); F.cache_add(Wd, x)
        if getattr(Wd, 'occV', None) is not None: Wd.occV.add_actor(x, vk=F.VK)
    print(line, flush=True); log.append(line)
# רכבי הצד של העמדות הגדולות (BT-P1 — הכבודה של P1, ‏BL-P6 — המסוע של P6; ‏CT-P1 / CT-P6 — 074o מתכנן מחדש לטיסה) ושל P5 (BT-P5)
SIDE = {'P1': [('BT-P1', 'LV-BT-01', 110, 40, 30, 140, 989)], 'P6': [('BL-P6', 'G7-BL', 62, 40, 20, 130, 989)], 'P5': [('BT-P5', 'LV-BT-01', 90, 52, 30, 150, 864)]}
for _k in os.environ.get('FT_NOSIDE', '').split(','):
    SIDE.pop(_k, None)
sidev = []
for a in Wd.new:
    for vid, model, dx, dy, after, stay, ry in SIDE.get(a.home, []):
        sp = dump['spots'][vid]; r = sp['rect']; home = [(r[0] + r[2]) / 2, (r[1] + r[3]) / 2]; hh = F.HH[sp.get('h', 'S')]
        bv = BV.get(vid); L = bv['L'] if bv else (40 if model == 'LV-BT-01' else 75); Wv = bv['W'] if bv else 22
        tr = F.plan_side(Wd, vid, model, a, home, dx, dy, after, stay, ry, L, Wv)
        if not tr: log.append('%s: אין זמן לרכב %s' % (a.home, vid)); print(log[-1]); continue
        v = F.veh_from_trips(vid, model, sp.get('home', ''), L, Wv, home, hh, [tr]); sidev.append(F.ser(v)); log.append('%s: %s ‏%.0f–%.0f' % (a.home, vid, tr[0]['t0'], tr[-1]['t1']))
        x = F.M.Actor(vid, 'veh', model, '', L, Wv); x.legs = tr; Wd.occ.add_actor(x, vk=F.VK); F.cache_add(Wd, x)
        if getattr(Wd, 'occV', None) is not None: Wd.occV.add_actor(x, vk=F.VK)
for a in Wd.new:
    if a.home != 'C1' or 'TG-C' not in DROP: continue
    bv = BV['TG-C']; home = bv['legs'][-1]['p'][0]; hh = bv['legs'][-1].get('h', F.S_)
    fc2 = next((f for f in Wd.FL if f.home == 'C2'), None); c2w = F.park_window(fc2) if fc2 else None
    trs = F.plan_tgc2(Wd, a, home, c2w) if c2w else F.plan_tgc(Wd, a, home)
    if not trs: log.append('C1: אין זמן ל-TG-C'); print(log[-1]); continue
    v = F.veh_from_trips('TG-C', bv['model'], bv['home'], bv['L'], bv['W'], home, hh, trs); sidev.append(F.ser(v)); log.append('C1: TG-C — %d נסיעות (%s)' % (len(trs), ', '.join('C1' if any(abs(g['p'][0][0] - 5200) < 1 and g.get('f') == 8 for g in tr) else 'C2' for tr in trs)))
    for tr in trs:
        x = F.M.Actor('TG-C', 'veh', 'LV-BT-01', '', bv['L'], bv['W']); x.legs = tr; Wd.occ.add_actor(x, vk=F.VK); F.cache_add(Wd, x)
veh = []
for vid, T0 in Wd.tug.items():
    if not T0['new']: continue
    v = F.veh_from_trips(vid, 'LV-PT-01', T0['homeid'], T0['L'], T0['W'], T0['home'], T0['hh'], T0['trips']); veh.append(F.ser(v))
veh += sidev
# הרכבים שתוזמנו למטוס החונה של עמדה שקיבלה טיסה, ולא תוזמנו כאן מחדש — נשארים בבית (074o מתכנן את CT-P1 / CT-P6 מחדש לטיסה)
newst = {a.home for a in Wd.new}; have = {v['id'] for v in veh}
SERV = {'BT-P1': 'P1', 'CT-P1': 'P1', 'CT-P6': 'P6', 'BL-P6': 'P6', 'TG-C': 'C1'}
for vid in DROP:
    if vid in have or SERV.get(vid) not in newst: continue
    bv = BV.get(vid) or next((v for v in dump['veh'] if v['id'] == vid), None)
    if not bv: continue
    hp = bv['legs'][-1]['p'][0]; hh = bv['legs'][-1].get('h', F.S_)
    veh.append(dict(id=vid, kind='veh', model=bv['model'], home=bv['home'], L=bv['L'], W=bv['W'], legs=[dict(p=[hp], t0=0, t1=F.T, h=hh, f=0)])); log.append('%s: %s נשאר בבית' % (SERV[vid], vid) + (' (מתוכנן מחדש לטיסה ב-074o)' if vid.startswith('CT-') else ' (אין חלון בעמידה — השלב הבא)'))
# ורכב שתוזמן למטוס חונה של עמדה שלא קיבלה טיסה — חוזר למכשולים (לא היה צריך להוריד אותו)
new = [F.ser(a) for a in Wd.new]
for f in new: f['ft'] = 1
for a in UPG:
    q = F.ser(a); q['airline'] = next((o.get('airline') for o in dump['flights'] if o['id'] == a.id), None); q['kind'] = 'ac'; q['ftu'] = 1; new.append(q)
sched = [q for q in Wd.sched if q[0] in {a.home for a in Wd.new} | {a.home for a in UPG}]
# השריון של הגרירות של R3 (fieldfix 074zo — FFR3; הישן: G77_MLV / aoCommit) — הזמנים נבחרים אחרי הלוח, מול כל מה שנע
fin = {v['id']: v for v in veh}; MOV = list(Wd.FL) + [F.actor(fin.get(o['id'], o)) for o in dump['veh']] + [F.actor(v) for v in veh if v['id'] not in {o['id'] for o in dump['veh']}] + list(Wd.HE)
t1 = time.time(); R3T = F.tow_search(MOV, dump.get('ffr3')); log.append('R3: ' + ' · '.join('%s החוצה %s חזרה %s' % (k, v.get('out', v.get('out_why')), v.get('back', v.get('back_why'))) for k, v in R3T.items())); print(log[-1], '%.1f ש׳' % (time.time() - t1), flush=True)
res = dict(seed=SEED, order=order, flights=new, sched=sched, veh=veh, log=log, r3=R3T, n_flights=len(Wd.FL), moves1800=round(2 * len(Wd.FL) * 1800 / F.T, 1), busy=sorted([[round(w[0], 2), round(w[1], 2), w[2]] for w in Wd.busy]))
json.dump(res, open(outp, 'w'), ensure_ascii=False)
print('טיסות', len(Wd.FL), '· תנועות מסלול ב-1800 ש׳', res['moves1800'], '· חדשות', len(new), '· רכבים', [v['id'] for v in veh])
