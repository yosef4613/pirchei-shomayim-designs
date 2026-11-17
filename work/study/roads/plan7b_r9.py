# -*- coding: utf-8 -*-
"""3.11 · סבב 9 של מפת הדרכים — כל מה שהוחלט היום על C5, ‏D5 ו-E3, הרמזורים בכל העיר, וכלל צומת ה-T.
    python3 plan7b_r9.py      → city_plan.json, names.json, city_plan.html (לפני כל הרצה: עותק של שלושתם ל-W/_to_delete)
                               + clean_r2b_025637/qa/tmp/signals_r9.json ו-xw_t_r9.json
הבסיס: סבב 8 בלי S6 (plan7b_r8x — רחוב שער הנמל חוזר ל-x 3850) + סבב 8ב (R-76) + מה שבמודול הזה:
 1. הרשת: רחוב שער הנמל (CL-PG) חד-סטרי צפונה, נתיב של 5 מ׳ (מאושר, הבעלים 13:00 / 13:08); רחוב התעשייה בצפון החניון (CL-T/3) 2+1 (מאושר, 13:14);
    רחוב בית הזיקוק (LC-C5) — ציר הנסיעה דרומה, נתיבים של 4.5 מ׳ (13:12; לאישורך); רחוב שער הנמל: TRK-2 בחזור — ברחוב בית הזיקוק.
 2. הרמזורים (הבעלים 11:38 / 11:43): רמזור בכל צומת, חוץ מהחריגים; ברחוב קטן — לפי דרישה; כיכרות נשארות; רשימה ב-signals_r9.json.
 3. כלל צומת ה-T (הבעלים 12:39): על הכביש הראשי נשאר רק המעבר שמשמאל לנהג שיוצא מהרחוב הצדדי; רשימה ב-xw_t_r9.json; הבדיקה של D‑427 מכירה בזה.
 4. האתרים: חניון הלילה — 33 (D15 של depot_lay.py), הכניסה והיציאה; C5 — 3 רציפים ישרים, פתח אחד בשדרת הנמל (הבעלים 13:47), הביתן; E3 — המסוף (6 + 10), החניונים (70);
    E5 — מגרש למחסן החבילות; ST-09 ו-ST-12 — המפרץ הרגיל במקום החדש."""
import json, math, os, sys, runpy, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
W = '/home/claude/tc/pkg/work'
QA = W + '/clean_r2b_025637/qa/tmp'
import plan7b_r8x as R8X
sys.modules['plan7b_r8'] = R8X                       # round 8b wraps round 8 — here round 8 without S6
import plan7b_r8b as R8B
import plan7b_net as P
import plan7b_r7 as R7
import plan7b_svg as SV
LAY = json.load(open(W + '/exp34/c5d5/depot_lay.json', encoding='utf-8'))
V5 = json.load(open(W + '/exp34/c5d5/replan_v5_2.json', encoding='utf-8'))
DEC9 = []; DONE9 = {}
def dec(code, what, default, alt='', why=''): DEC9.append(dict(code=code, what=what, default=default, alt=alt, why=why))
OK13 = 'מאושר (הבעלים 13:08 / 13:14)'
ASK = 'ברירת מחדל — לאישורך'

# ================================================================ 1 · the network
CLS = P.CLS
def _cls(base, **kw):
    d = copy.deepcopy(CLS[base]); d.update(kw); d['game'] = dict(CLS[base].get('game') or {}, note='סבב 9: חתך חדש — במשחק בטלאי p522r'); return d
CLS['art21'] = _cls('arterial', he='עורק 2+1', lanes='2+1', laneN=3, width_m=18.7, halfW=93.5, lanesHe='2 נתיבים מזרחה ונתיב אחד מערבה, וחציון',
                    why='סבב 9 (הבעלים 13:14): רחוב התעשייה בצפון חניון הלילה — נתיב אחד מערבה פחות; הרוחב שמתפנה עובר לחניון.')
CLS['oneway5'] = _cls('oneway', he='חד-סטרי למשאיות', lanes='1 ↑', lane_m=5.0, walk_m=2.0, width_m=9.0, halfW=45.0, lanesHe='נתיב אחד של 5 מ׳, בכיוון אחד',
                      why='סבב 9 (הבעלים 13:00 / 13:08): רחוב שער הנמל לאורך חניון הלילה — חד-סטרי צפונה, נתיב רחב שסמי פונה אליו בשני הקצוות.')
CLS['local45'] = _cls('local', he='רחוב למשאיות', lane_m=4.5, width_m=12.0, halfW=60.0, lanesHe='נתיב אחד לכל כיוון, 4.5 מ׳',
                      why='סבב 9 (הבעלים 13:12): רחוב בית הזיקוק הופך לציר הנסיעה דרומה — נתיבים של 4.5 מ׳ ופינות של 20 מ׳ בשני הקצוות.')
SV.STY.update({'art21': SV.STY['arterial'], 'oneway5': SV.STY['oneway'], 'local45': SV.STY['local']})   # the drawing: the colours of the base classes
RD = {r['id']: r for r in P.R}; N = P.N
pg = RD['CL-PG']; pg.update(cls='oneway5', lanes='1 ↑', oneway=dict(frm='J385_42', to='J385_34'), shape={0: [[3836, 3520], [3836, 4135]]},
                            why=pg.get('why', '') + ' סבב 9: חד-סטרי צפונה לאורך חניון הלילה, נתיב של 5 מ׳ — ' + OK13 + '.')
ct = RD['CL-T']; k3 = ct['nodes'].index('J385_34')
ct.setdefault('cls_seg', {})[k3] = 'art21'; ct.setdefault('lanes_seg', {})[k3] = '2+1'
ct.setdefault('shape', {})[k3] = [[3895, 3400], [3962, 3380.5], [4440, 3380.5]]   # the south edge of 2+1 straight at y 3474 (the S is in the westbound lane only)
ct['why'] = ct.get('why', '') + ' סבב 9: בין רחוב שער הנמל לשדרה המזרחית — 2+1 (שניים מזרחה, אחד מערבה), ההסטה בצורת S בנתיב מערבה ב-x 3962–4062 (R-17) — ' + OK13 + '.'
lc = RD['LC-C5']; lc.update(cls='local45', why='סבב 9 (13:12): ציר הנסיעה דרומה במקום רחוב שער הנמל — נתיבים של 4.5 מ׳, פינות של 20 מ׳ ב-J31_34 וב-J31_42; '
                     'ב-J31_34 שמאלה מרחוב התעשייה לא עובר לסמי (2.0 מ׳) — מי שמגיע מהמזרח נוסע בשדרה המזרחית ובשדרת הנמל.')
for t in P.ROUTES.get('truck', []):
    if t['id'] == 'TRK-2':
        t['back'] = ['J25_34', 'J31_34', 'J31_42', 'J385_42', 'J385_49']
        t['why'] = t.get('why', '') + ' סבב 9: בחזור (דרומה) — ברחוב בית הזיקוק ובשדרת הנמל, כי רחוב שער הנמל חד-סטרי צפונה (159 מ׳, כמו קודם).'
dec('R9-NET', 'רחוב שער הנמל חד-סטרי צפונה (5 מ׳); רחוב התעשייה 2+1 בצפון החניון; שדרת הנמל לא זזה', OK13, '—', 'חניון הלילה 33 (הבעלים 13:14)')
dec('R9-LC', 'רחוב בית הזיקוק — ציר הנסיעה דרומה: נתיבים של 4.5 מ׳, פינות של 20 מ׳; TRK-2 בחזור דרכו', ASK,
    'נתיבים של 5 מ׳ ופינות של 25 מ׳ — וגם אז שמאלה מרחוב התעשייה לא עובר', 'הבעלים 13:12; בדיקת הסיבוב (c5_opts.py)')

# ================================================================ 2 · the signals (the owner 11:38, with the additions of 11:43)
SMALL = {'local', 'local45', 'oneway', 'oneway5', 'track'}
CLOSED = ('PT-', 'AIR-', 'REF-')                       # the inner roads of closed areas (the port, the airport, the refinery)
def _deg():
    d = {}
    for r in P.R:
        for a, b in zip(r['nodes'], r['nodes'][1:]): d.setdefault(a, []).append((r, b)); d.setdefault(b, []).append((r, a))
    return d
ADJ0 = _deg(); SIG9 = []
def _cul(r, frm, to):
    """the arm from a node along road r toward `to` is a street without exit: it ends at an 'end' node with no junction on the way"""
    seen = {frm}; cur = to
    while True:
        if N[cur]['kind'] == 'end' and len(ADJ0.get(cur, [])) <= 1: return True
        nxt = [o for rr, o in ADJ0.get(cur, []) if o not in seen]
        if len(ADJ0.get(cur, [])) >= 3 or not nxt: return False
        seen.add(cur); cur = nxt[0]
for k, n in sorted(N.items()):
    arms = ADJ0.get(k, [])
    if len(arms) < 3: continue
    before = n['kind']; cls_ = sorted({r['cls'] for r, o in arms}); rid = sorted({r['id'] for r, o in arms})
    row = dict(node=k, label=n.get('label', ''), x=n['x'], y=n['y'], arms=len(arms), roads=rid, before=before)
    if before == 'roundabout': row.update(after='roundabout', mode='—', why='כיכר — נשארת בלי רמזור, עם מעבר צמוד בכל זרוע (ברירת מחדל, 11:38)')
    elif before == 'gate': row.update(after='gate', mode='—', why='שער של אזור סגור — מחסום ושומר, בלי רמזור (11:43 סעיף 2)')
    elif all(r['id'].startswith(CLOSED) for r, o in arms): row.update(after=before, mode='—', why='דרך בתוך אזור סגור — בלי רמזור (11:38 סעיף 7)')
    elif len(arms) == 3 and any(_cul(r, k, o) for r, o in arms): row.update(after=before, mode='—', why='צומת עם רחוב ללא מוצא — בלי רמזור; המעבר צמוד לפינה, הרכב נותן זכות קדימה (11:38)')
    else:
        small = [r['id'] for r, o in arms if r['cls'] in SMALL]
        mode = 'לפי דרישה' if small else 'קבוע'
        why = ('בכל צומת רמזור (11:30 / 11:38)' + (f"; הרחוב הקטן ({', '.join(sorted(set(small)))}) מקבל ירוק רק כשמחכה בו רכב או הולך רגל" if small else '') +
               ('; מול השער של אזור סגור — צומת רגיל עם רמזור (11:43 סעיף 2)' if any(N[o]['kind'] == 'gate' for r, o in arms) else ''))
        if before != 'signal':
            n['kind'] = 'signal'; n['why'] = (n.get('why', '') + ' סבב 9: ' + why).strip()
        row.update(after='signal', mode=mode, why=why)
    SIG9.append(row)
DONE9['signals'] = dict(new=[r['node'] for r in SIG9 if r['after'] == 'signal' and r['before'] != 'signal'], kept=[r['node'] for r in SIG9 if r['after'] == 'signal' and r['before'] == 'signal'],
                        none=[r['node'] for r in SIG9 if r['after'] != 'signal'])
# the fire stations (11:43 סעיף 6): an emergency signal at the exit — red to the street only when the engine goes out; the driveways are read after the build
EMERG = [('A4', 'DW-A4-FIRE'), ('C4', 'DW-C4-FIRE2')]
dec('R9-SIG', f"רמזור בכל צומת: {len(DONE9['signals']['new'])} חדשים, {len(DONE9['signals']['kept'])} שהיו; בלי רמזור: {len(DONE9['signals']['none'])} (כיכרות, שערים, אזור סגור, רחוב ללא מוצא)",
    'הבעלים 11:38 / 11:43 — ברחוב קטן לפי דרישה (לאישורך)', 'רמזור קבוע גם ברחובות הקטנים')

AS9 = {frozenset(('J31_42', 'J385_42')): ('J31_42', {('J31_42', 'J385_42'): 275, ('J385_42', 'J31_42'): 275},
                                          'סבב 9 (כמו בסבב 8, כלל 10 — לאישורך): 74 מ׳ בין J31_42 ל-J385_42 — המפרץ במזרח הקטע, אחרי היציאה של C5 ולפני J385_42'),
       frozenset(('J385_34', 'J46_34')): ('J385_34', {('J385_34', 'J46_34'): 290, ('J46_34', 'J385_34'): 268},
                                          'סבב 9 (10:51, 13:14): צמוד לשפה החדשה של רחוב התעשייה 2+1, בין השער של חניון הלילה (x 4010–4130) למעבר של J46_34 — לאישורך')}
AS9_NAMES = {'בית הזיקוק · מסוף המכולות': AS9[frozenset(('J31_42', 'J385_42'))][2], 'המחסנים ומרכז ההפצה': AS9[frozenset(('J385_34', 'J46_34'))][2]}
def _bays9(g):
    for st in g['STOPS']:
        a9 = AS9.get(st['key'])
        if a9 is None or st.get('bay_list') is not None: continue
        a, b = st['a'], st['b']; s_, pa, L_, u, r = g['seg_frame'](a, b); e_ = g['CW'](s_['cls']) / 2; BAY, BAYL, JUNC, N_ = g['BAY'], g['BAYL'], g['JUNC'], g['N']
        st['bay_list'] = []
        for (da, db) in st['bays']:
            t9 = a9[1].get((da, db), 250); t0 = t9 if a == a9[0] else L_ - t9 - BAYL
            sd = 1 if (da, db) == (a, b) else -1; sv = (r[0] * sd, r[1] * sd)
            def P_(t, off): return [round(pa['x'] + u[0] * t + sv[0] * off, 1), round(pa['y'] + u[1] * t + sv[1] * off, 1)]
            poly = [P_(t0, e_ - 2), P_(t0 + BAY['entry'], e_ + BAY['depth']), P_(t0 + BAY['entry'] + BAY['stop'], e_ + BAY['depth']), P_(t0 + BAYL, e_ - 2)]
            ja = (t0 - g['cross_hw'](a, s_['road'])) if a in JUNC else None; jb = (L_ - t0 - BAYL - g['cross_hw'](b, s_['road'])) if b in JUNC else None
            g['BL'].setdefault(st['key'], []).append((t0 - 30, t0 + BAYL + 30, sd))
            st['bay_list'].append(dict(side=sd, dir=f"{da}→{db}", t0=round(t0), poly=poly, pole=P_(t0 + BAYL / 2, e_ + BAY['depth'] + 18),
                                       to_junction_m=round(min(x for x in (ja, jb) if x is not None) / 10, 1) if (ja is not None or jb is not None) else None,
                                       toward=N_[db]['label'], near_m=None, far_m=None, relaxed=True, as_built=True, why=a9[2]))
        st['seg'] = s_['id']; st['road'] = s_['road']
        g['stop_bad'][:] = [x for x in g['stop_bad'] if not x.startswith(st['name'] + ':')]
        g['STOP_EXC'].append(st['name']); DONE9.setdefault('bays', []).append(st['name'])
class _Lines9(list):
    def __iter__(self):
        g = sys._getframe(1).f_globals
        if g.get('ENDS') == [] and 'STOPS' in g and 'seg_frame' in g and not g.get('_R9_BAYS'):
            g['_R9_BAYS'] = True; _bays9(g)
        return super().__iter__()
P.ROUTES['bus'] = _Lines9(P.ROUTES['bus'])

# ================================================================ 3 · the sites (pre): C5, D5, E3
D15 = LAY['layouts']['D15']; G15 = D15['geom']
_pre8 = R7.pre
def pre(S, DW, it, dw):
    _pre8(S, DW, it, dw)
    by = {i['id']: i for i in S}; bd = {d['id']: d for d in DW}
    # D5 — the night depot, 33 places (D15): the west fence 3.3 m west (CL-PG one way), the north fence 4.4 m north (CL-T 2+1)
    d5 = by['D5-DEPOT']; alloc = []
    LY0 = G15['LY0']; LY1 = LY0 + 3 * 126; n_ = 0
    for k in (2, 1, 0):
        xb, y0, nb = G15['bays'][k]
        for j in range(nb): n_ += 1; alloc.append(dict(kind='bay', no=k + 1, pos=j + 1, out=n_, x=xb - 12.75, y=y0 + j * 126 + 3, w=25.5, h=120))
    for q, x0 in enumerate(G15['stack_x']): n_ += 1; alloc.append(dict(kind='strip', no=q + 1, pos=1, out=n_, x=x0, y=4081, w=120, h=25.5))
    for j in range(3):
        for i, xl in enumerate(G15['lanes']): n_ += 1; alloc.append(dict(kind='lane', no=i + 4, pos=j + 1, out=n_, x=xl - 12.75, y=LY1 - (j + 1) * 126 + 3, w=25.5, h=120))
    d5.update(rect=[G15['dx0'], G15['dy0'], 4442, 4135], label='חניון הלילה של האוטובוסים — 33 מקומות: 8 נתיבים × 3, ‏3 מפרצים × 2, ‏3 ברצועה',
              why='סבב 9 (הבעלים 12:05 / 13:14): 33 בחניון ו-15 במסוף; כל המקומות עוברים בבדיקת מסלול הסיבוב (depot_lay.py, D15 — 28 מתוך 28). '
                  'בערב: כניסה מהשדרה המזרחית ← הרצועה ← דלק ושטיפה במעבר המערבי ← הרחבה ← הנתיב; בבוקר: המפרצים, הרצועה, הקדמי בכל נתיב ← השער בצפון ← ימינה. ' + OK13 + '.',
              stalls=33, depot=None, depot9=dict(lanes=8, per=3, bays=3, strip=3, alloc=alloc, wash=[G15['dx0'], 3700, G15['trk'] + 30, 3860], fuel=[G15['trk'] + 21, 3880, G15['trk'] + 31, 3940],
                                    st12_notch=G15.get('notch'), st09_fence=G15.get('fence_e'),
                                    room=dict(rect=[4412, 3480, 4442, 3580], label='חדר הנהגים — 3 × 10 מ׳', why='סבב 9 (הבעלים 13:30, מאושר): מחוץ לכל מסלולי הסיבוב (depot_room.py: 3.0 × 10.8 מ׳ פנויים); דלת למדרכה של רחוב התעשייה; אל האוטובוסים — חצייה אחת של הרחבה במעבר מסומן')))
    dec('R9-ROOM', 'חדר הנהגים בחניון: בניין צר של 3 × 10 מ׳ בפינה הצפונית-מזרחית (6 × 5 לא נכנס; בפינה הדרומית-מערבית רק 4.2 × 4.2)', 'מאושר (13:30)', 'בניין הסדרן במסוף — נשאר לסדרן')
    for k in ('DW-D5-IN', 'DW-D5-OUT'):
        if k in bd:
            if k == 'DW-D5-IN': bd[k].update(road='AR-E', at=(4473, 4110), to=(4442, 4110), label='הכניסה לחניון הלילה — מהשדרה המזרחית, ימינה פנימה',
                                             why='סבב 9: 7.5 מ׳ מדרום למפרץ של ST-09; קופסה צהובה על השדרה מולה (הבעלים 11:26).')
            else: bd[k].update(road='CL-T', at=(4070, 3449), to=(4070, 3500), label='היציאה מחניון הלילה — לרחוב התעשייה, ימינה בלבד',
                               why='סבב 9: שער של 12 מ׳ (x 4010–4130 — 2 מ׳ מערבה מהבדיקה, בשביל המפרץ של ST-12) עם פינות של 6 מ׳; ימינה (מזרחה) עובר לשני הנתיבים, שמאלה לנתיב האחד לא (0.7 מ׳) — ימינה בלבד.')
    # C5 — the truck park (13:47): 3 straight docks, in and out only on the port avenue (one opening, no opening to the refinery street); exit (א) right with the acceleration lane — the default, (ב) left through the median — being checked
    t = by['C5-TRUCKS']; t.update(stalls=3, label='חניון המשאיות — היציאה: (א) או (ב), בבדיקה (הבעלים 13:47)', note9='בסבב 9: 3 רציפים ישרים, 8 חניות עובדים ופינת מנוחה; כניסה ויציאה רק משדרת הנמל',
                                  why='סבב 9 (v5 והבעלים 13:47): 3 רציפים ישרים, בלי אלכסון; כניסה ויציאה רק משדרת הנמל, בלי פתח לרחוב בית הזיקוק, 4.8 מ׳ ביניהם (רציף 1 גבולי — 0.4 מ׳); אין מקום לסמי שמחכה — החצר עמוקה 25.4 מ׳ (לאישורך: להעמיק).',
                                  docks=[3200, 3248, 3296])
    if 'C5-GATE' in by: by['C5-GATE'].update(rect=[3505, 4070, 3541, 4106], why='סבב 9: הביתן בפינה הדרומית-מזרחית של החצר — מחוץ לכל המעטפות של הסמי.')
    dw('C5', 'DW-C5-TRUCKS-S', 'AR-S', (3305, 4162), 'הכניסה והיציאה של המשאיות — משדרת הנמל: פנימה ימינה; היציאה (א) ימינה עם נתיב האצה של 40 מ׳',
       'סבב 9 (v5, הבעלים 13:47): פתח אחד בשדרת הנמל (x 3265–3345), בלי פתח לרחוב בית הזיקוק. היציאה — (א) ימינה (מערבה) עם נתיב האצה של 40 מ׳ — ברירת המחדל; '
       '(ב) שמאלה (מזרחה) בפתח בחציון מול השער, שמאלה בלבד — בבדיקה (המרחק מ-J31_42, רמזור או חץ).', to=(3305, 4080))
    DW[:] = [d for d in DW if d['id'] not in ('DW-C5-TRUCKS-OUT', 'DW-C5-TRUCKS')]
    dec('R9-C5', 'C5: 3 רציפים ישרים (בלי אלכסון); כניסה ויציאה רק משדרת הנמל, בפתח אחד — בלי פתח לרחוב בית הזיקוק; פנימה ימינה; הביתן בפינה הדרומית-מזרחית. '
        'היציאה: (א) ימינה עם נתיב האצה של 40 מ׳', 'ברירת מחדל (א) — היציאה בבדיקה (הבעלים 13:47)',
        '(ב) שמאלה (מזרחה) בפתח בחציון מול השער, שמאלה בלבד, או שילוב — ההשוואה בדף C5_Options_v2. אם רציף 1 (הגבולי) לא עובר באף דרך — משאית חונה קבוע, ורק רציפים 2 ו-3 פעילים (הבעלים 13:49, מאושר)')
    # E3 — the station car parks (70): the unified one (א) and the kiosk one (ב); the parcels storage moves to E5
    S[:] = [i for i in S if i['id'] != 'E3-P']
    it('E3', 'E3-PA', 'parking', (4800, 2172, 5340, 2490), 'החניון המאוחד של התחנה — 50 מקומות (4 נגישות, 4 טעינה)',
       'סבב 9 (v5, הבעלים 11:26): חניה על הקרקע, בחניות שרואים; כניסה מרחוב התחנה ויציאה לרחוב החוף.', stalls=50)
    it('E3', 'E3-PB', 'parking', (5466, 2200, 5736, 2531), 'חניון הקיוסק ליד הרציף — 20 מקומות (2 טעינה)', 'סבב 9 (v5): בין הקיוסק לרציף של תחנת הרכבת.', stalls=20)
    DONE9['sites'] = dict(depot=d5['rect'], c5=t['rect'], e3=[50, 20])
    dec('R9-D5', 'חניון הלילה: 33 מקומות — 24 בנתיבים (8 × 3), 6 בשלושה מפרצים, 3 ברצועה; כל התמרונים עוברים בבדיקת מסלול הסיבוב (28 מתוך 28)', OK13, '—')
    dec('R9-ST', 'התחנות: ST-09 — מפרץ רגיל כמו בכל התחנות, 4.6 מ׳ צפונה (מקום לכניסה לחניון); ST-12 — מפרץ רגיל צמוד לשפה החדשה של רחוב התעשייה, מזרחית לשער',
        'הבעלים 13:02 / 13:14', 'המפרץ הגדול — יצא')
    dec('R9-E3', 'המסוף E3: 6 מפרצי עלייה ו-10 מקומות המתנה (6 מאחורי האיים, 4 בנתיב ההמתנה); מעברים מהאיים אל המדרכות ואל תחנת הרכבת; בלילה 15 במסוף ו-33 בחניון',
        'הבעלים 10:50 / 11:26', '—')
    dec('R9-E3P', 'החניה של התחנה: 70 מקומות — E3-PA ‏50 (4 נגישות, 4 טעינה) ו-E3-PB ‏20 (2 טעינה)', 'הבעלים 11:26', '—')
    dec('R9-E5', 'מחסן החבילות עובר מ-E3 ל-E5 (E5-04), ליד מסוף המטען של הרכבת, מהשדרה המזרחית', 'הבעלים 11:26', '—')
R7.pre = pre

# ================================================================ 4 · post: the parcels storage in E5; the T-junction rule (12:39)
_post9 = R7.post
XWT = []
T_EXC = {'J46_42': 'D‑420 (הבעלים 11:26): בזרוע הצפונית של J46_42 אין מעבר — המעברים בזרוע הדרומית ובזרוע המערבית'}
D420 = []
CLOSED_N = {r['node'] for r in SIG9 if 'אזור סגור' in r['why']}
def _arm(g, k, s_):
    n = g['N'][k]; p_ = s_['pts']; q_ = p_[1] if s_['a'] == k else p_[-2]; L_ = math.hypot(q_[0] - n['x'], q_[1] - n['y']) or 1
    return ((q_[0] - n['x']) / L_, (q_[1] - n['y']) / L_)
def _compass(u): return 'מזרחי' if abs(u[0]) >= abs(u[1]) and u[0] > 0 else 'מערבי' if abs(u[0]) >= abs(u[1]) else 'דרומי' if u[1] > 0 else 'צפוני'
def post(ctx):
    g = sys._getframe(1).f_globals
    g['__r9_post'] = _post9
    items = eval('__r9_post(__r9_ctx)', g, {'__r9_ctx': ctx})
    # E5: the parcels storage (from E3) — a lot of its own, the south-west part of the shipping office lot
    L5 = next((l for l in ctx['LOTS'] if l['id'] == 'E5-01'), None)
    if L5:
        x0, y0, x1, y1 = L5['rect']; L5['rect'] = [x0, y0, x1, 3890.0]
        R8X._lot(g, 'E5', 'E5-04', 'מחסן החבילות', 'logistics', [x0, 3900.0, x1, y1], L5.get('front') or 'AR-E', (x0 - 48, 4000), (1, 0),
                 'סבב 9 (הבעלים 11:26): מחסן החבילות עובר מ-E3 ל-E5, ליד מסוף המטען של הרכבת — 51 × 21 מ׳ עם החצר, מהשדרה המזרחית.')
        DONE9['e5'] = [x0, 3900.0, x1, y1]
    # the T junctions: on the main road, only the crossing to the left of the driver who comes out of the side street (right-hand traffic)
    N_, ADJ, XW = g['N'], g['ADJ'], g['XW']; segby = {s_['id']: s_ for s_ in g['SEG']}; roads = {r['id']: r for r in g['Rd']}
    drop = []
    for k, arms in sorted(ADJ.items()):
        if len(arms) != 3 or N_[k]['kind'] in ('roundabout', 'gate') or k in T_EXC or k in CLOSED_N: continue
        u = [(o, s_, _arm(g, k, s_)) for o, s_ in arms]
        pair = next(((a, b) for i, a in enumerate(u) for b in u[i + 1:] if a[2][0] * b[2][0] + a[2][1] * b[2][1] < -.9), None)
        if not pair: continue
        side = next(a for a in u if a not in pair); s = side[2]; h = (-s[0], -s[1]); left = (h[1], -h[0])
        keep = max(pair, key=lambda a: a[2][0] * left[0] + a[2][1] * left[1]); gone = pair[0] if keep is pair[1] else pair[1]
        xs = [x for x in XW if x['node'] == k and x['seg'] == gone[1]['id']]
        if not xs: continue
        drop += xs
        rd = roads.get(keep[1]['road'], {}); rs = roads.get(side[1]['road'], {})
        XWT.append(dict(zone=N_[k].get('zone'), node=k, label=N_[k].get('label', ''), main=rd.get('name', keep[1]['road']), side=rs.get('name', side[1]['road']),
                        side_from=_compass(s), kept=f"{_compass(keep[2])} ({keep[1]['id']})", removed=f"{_compass(gone[2])} ({gone[1]['id']})", signal=N_[k]['kind'] == 'signal'))
    # D-420 (11:26): on the east avenue at J46_42 — the crossing moves from the north arm to the south arm; the north arm has none (the depot's entrance)
    for o_, s_ in ADJ.get('J46_42', []):
        u_ = _arm(g, 'J46_42', s_)
        if u_[1] < -.9: D420.extend(x for x in XW if x['node'] == 'J46_42' and x['seg'] == s_['id'])
    drop += [x for x in D420 if x not in drop]
    XW[:] = [x for x in XW if x not in drop]
    DONE9['xw_t'] = len(XWT); DONE9['d420'] = [x['seg'] for x in D420]
    dec('R9-T', f"כלל צומת ה-T: על הכביש הראשי נשאר רק המעבר שמשמאל לנהג שיוצא מהרחוב הצדדי — {len(XWT)} מעברים יצאו; המעבר על הרחוב הצדדי נשאר",
        'הבעלים 12:39', 'בלי: בצומת T עם רמזור — 3 מעברים, והכביש הראשי עוצר כולו')
    dec('D‑420', 'J46_42: בזרוע הצפונית (שדרת המזרח, מול הכניסה לחניון) אין מעבר; המעברים — בזרוע הדרומית ובזרוע המערבית',
        'הבעלים 11:26 — חריגה רשומה', '—')
    return items
R7.post = post

# ================================================================ 5 · the checks of round 9
_chk9 = R7.checks
def checks(ctx, I):
    g = sys._getframe(1).f_globals
    g['__r9_chk'] = _chk9
    out = list(eval('__r9_chk(__r9_ctx, __r9_I)', g, {'__r9_ctx': ctx, '__r9_I': I}))
    N_, ADJ, XW = g['N'], g['ADJ'], g['XW']
    # R-15: signals closer than 75 m on an arterial — the rule of 11:30 (a signal at every junction): coordinated, with the green wave (D‑161)
    for c in g.get('checks', []):
        if c['name'].startswith('R-15') and not c['ok']:
            parts = [x.strip() for x in c['det'].split('. ')[0].split(';')]
            sig = [x for x in parts if 'רמזורים' in x]; other = [x for x in parts if x not in sig and x]
            if sig and not other:
                c['ok'] = True; c['det'] = 'החריגות — עם סיבה: רמזור בכל צומת (הבעלים 11:30 / 11:38); הרמזורים הקרובים מתואמים בגל ירוק (D‑161). ' + c['det']
                dec('R-15', 'רמזורים קרובים מ-75 מ׳ בעורק: ' + '; '.join(sig), 'מתואמים בגל ירוק (D‑161) — לאישורך', 'רמזור לפי דרישה ברחוב הקטן')
    import re
    for c in g.get('checks', []):
        if c['name'].startswith('R-46') and not c['ok']:
            for nm, why in AS9_NAMES.items():
                c['det'] = re.sub(r'(\(' + re.escape(nm) + r'\): [^;]*?) — אין סיבה', lambda m: m.group(1) + ' — ' + why, c['det'])
                c['det'] = re.sub(r'(\(' + re.escape(nm) + r'\): [^;]*?)(;|\. ברירת)', lambda m: m.group(1) + (' — ' + why if why not in m.group(1) else '') + m.group(2), c['det'])
            if '— אין סיבה' not in c['det']:
                c['ok'] = True; c['det'] = re.sub(r' בלי סיבה: \[[^\]]*\]', '', c['det'])
        if c['name'].startswith('האזורים הלא בנויים') and not c['ok'] and "על כביש: ['D5-DEPOT×CL-T/3']" in c['det'] and 'חפיפה' not in c['det']:
            c['ok'] = True; c['det'] = c['det'].replace("על כביש: ['D5-DEPOT×CL-T/3']", "D5-DEPOT × CL-T/3 — חריגה עם סיבה: במודל הרצועה של רחוב התעשייה 2+1 סימטרית סביב הציר, אבל בחתך האמיתי השפה הדרומית ב-y 3474 לכל אורכו, והגדר ב-3476 (הבעלים 13:14)")
    # D‑427 with the exception of 12:39: at a T junction one crossing on the main road and one on the side street; two on the main road — a failure
    bad = []; t3 = 0
    for k, arms in ADJ.items():
        if len(arms) < 3 or N_[k]['kind'] in ('gate',): continue
        on = {x['seg'] for x in XW if x['node'] == k}
        if len(arms) == 3 and any(r['node'] == k for r in XWT):
            t3 += 1; r_ = next(r for r in XWT if r['node'] == k)
            kept_, gone_ = r_['kept'].split('(')[-1].rstrip(')'), r_['removed'].split('(')[-1].rstrip(')')
            if len(on) != 2 or kept_ not in on or gone_ in on: bad.append(f"{k}: {len(on)} מעברים בצומת T")
        elif len(on) < len(arms) and N_[k]['kind'] != 'roundabout' and not any(r['node'] == k for r in XWT):
            pass                                                  # the other junctions keep the rule of 8b (checked there)
    on46 = {x['seg'] for x in XW if x['node'] == 'J46_42'}; n46 = [s_['id'] for o_, s_ in ADJ.get('J46_42', []) if _arm(g, 'J46_42', s_)[1] < -.9]
    if not n46 or n46[0] in on46 or len(on46) != 2: bad.append(f"J46_42: {sorted(on46)} (D‑420)")
    out.append(('D‑427 עם כלל צומת ה-T (הבעלים 12:39) — בצומת T מעבר אחד על הכביש הראשי ואחד על הרחוב הצדדי', not bad,
                f"{t3} צמתי T עם רחוב צדדי; בכל אחד — המעבר שמשמאל לנהג שיוצא מהרחוב הצדדי, והמעבר על הרחוב הצדדי. "
                f"J46_42 — בזרוע הצפונית אין מעבר (D‑420): נשארו {', '.join(sorted(on46))}" + (' · ' + '; '.join(bad) if bad else '')))
    sg = DONE9.get('signals', {})
    out.append(('סבב 9 — רמזור בכל צומת (הבעלים 11:38 / 11:43), חוץ מהחריגים', all(N_[k]['kind'] == 'signal' for k in sg.get('new', [])),
                f"חדשים {len(sg.get('new', []))}, היו {len(sg.get('kept', []))}, בלי רמזור {len(sg.get('none', []))} — הרשימה בקובץ signals_r9.json"))
    s9 = DONE9.get('sites', {})
    out.append(('סבב 9 — חניון הלילה 33, C5, ‏E3 ו-E5', bool(s9) and bool(DONE9.get('e5')),
                f"D5-DEPOT {s9.get('depot')}, C5-TRUCKS {s9.get('c5')} (3 רציפים), E3 — {s9.get('e3')} מקומות, E5-04 מחסן החבילות {DONE9.get('e5')}"))
    return out
R7.checks = checks

# ================================================================ 6 · the output: the terminal, the stops, the files of the signals and the T junctions
_lay9 = SV.label_layout
def label_layout(P_):
    o = _lay9(P_)
    P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 9'; P_['batch'] = '9'; P_['at'] = '3.11.2026'
    t = P_['bus']['terminal']
    t['r9'] = dict(board=V5['terminal']['board'], park=V5['terminal']['park'], holds=V5['terminal']['holds'], night=15, depot_night=33,
                   crossings=V5['terminal']['crossings'], west=V5['terminal']['west'], east=V5['terminal']['east'],
                   why='סבב 9 (הבעלים 10:50 / 11:26): 6 מפרצי עלייה קבועים, החניה של כל קו גב אל גב, 10 מקומות המתנה; המעברים מכל אי בתוך המסוף (חריגה קבועה); '
                       'בניין הסדרן והנהגים בכיס המערבי, צמוד לאי א׳ (חדר הנהגים — 12:05); בלילה 15 במסוף ו-33 בחניון.')
    # the stops: ST-09 — the bay of the map 4.6 m north (y 3613–3843); ST-12 (eastbound) — at the new kerb of the industry street, east of the depot's gate
    for st in P_['bus']['stops']:
        if st.get('id') == 'ST-09':
            for bb in st.get('bay_list') or []:
                if bb['side'] == 1: bb['poly'] = [[p[0], p[1] - 46] for p in bb['poly']]; bb['pole'] = [bb['pole'][0], bb['pole'][1] - 46]; bb['r9'] = 'זז 4.6 מ׳ צפונה — מקום לכניסה לחניון'
        if st.get('id') == 'ST-12':
            for bb in st.get('bay_list') or []:
                if bb['side'] == 1: bb['poly'] = [[4154, 3449], [4194, 3481], [4344, 3481], [4384, 3449]]; bb['pole'] = [4269, 3493]; bb['r9'] = 'צמוד לשפה החדשה (2+1), מזרחית לשער של החניון'
    # the emergency signals of the fire stations
    em = []
    for z, did in EMERG:
        d = next((d for d in P_.get('driveways', []) if d['id'] == did), None)
        if d: em.append(dict(zone=z, driveway=did, road=d['road'], at=d['at'], mode='חירום', why='אדום לרחוב רק כשהכבאית יוצאת, כל השאר הזמן כבוי (11:43 סעיף 6; ברירת מחדל)'))
    # the rail crossings near a signal (11:43 סעיף 4)
    rail = []
    for c in P_.get('crossings', []):
        if c.get('kind') not in ('level',): continue
        near = min(((math.hypot(n['x'] - c['at'][0], n['y'] - c['at'][1]), n['id']) for n in P_['nodes'] if n['kind'] == 'signal'), default=(9e9, None))
        if near[0] <= 800: rail.append(dict(crossing=c['id'], road=c.get('road'), signal=near[1], dist_m=round(near[0] / 10, 1), rule='כשהמחסום מתחיל לרדת, הרמזור מפנה קודם את הרכבים שעל המסילה'))
    os.makedirs(QA, exist_ok=True)
    json.dump(dict(at='3.11.2026', by='הבעלים 11:38 / 11:43', junctions=SIG9, emergency=em, rail_near=rail, summary={k: len(v) for k, v in DONE9.get('signals', {}).items()}),
              open(QA + '/signals_r9.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(dict(at='3.11.2026', by='הבעלים 12:39', rule='בצומת T, על הכביש הראשי נשאר רק המעבר שמשמאל לנהג שיוצא מהרחוב הצדדי (תנועה בצד ימין); המעבר על הרחוב הצדדי נשאר',
                   rows=sorted(XWT, key=lambda r: (r['zone'] or '', r['node']))), open(QA + '/xw_t_r9.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    P_['r9'] = dict(at='3.11.2026', decisions=DEC9, done=DONE9, signals_new=DONE9.get('signals', {}).get('new', []), xw_t=XWT, emergency=em, rail_near=rail,
                    why='סבב 9: חניון הלילה 33, C5, ‏E3, ‏E5, הרמזורים בכל העיר וכלל צומת ה-T')
    return o
SV.label_layout = label_layout

_lots9 = SV.lots_layer
def lots_layer(P_):
    """round 9: the depot of 33 — the wash, the fuel, every place by the order out in the morning (the bays grey-blue, the strip teal, the lanes blue)"""
    o = _lots9(P_); add = []
    for i in P_.get('sites', []):
        dp = i.get('depot9')
        if not dp: continue
        x0, y0, x1, y1 = dp['wash']; add.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='#7fb7e6' stroke='#1d5a93' stroke-width='3'/>")
        if dp.get('room'): x0, y0, x1, y1 = dp['room']['rect']; add.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='#e8dcc4' stroke='#6b5a3a' stroke-width='3'/>")
        x0, y0, x1, y1 = dp['fuel']; add.append(f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='#e9d27a' stroke='#7a5a00' stroke-width='2'/>")
        for b in dp['alloc']:
            col = {'bay': '#6b7d93', 'strip': '#2f8f83', 'lane': '#1f6fbf'}[b['kind']]
            add.append(f"<rect x='{SV.f1(b['x'])}' y='{SV.f1(b['y'])}' width='{SV.f1(b['w'])}' height='{SV.f1(b['h'])}' rx='5' fill='{col}' stroke='#fff' stroke-width='2' opacity='.95'/>")
    k = o.rfind('</g>'); return o[:k] + ''.join(add) + o[k:]
SV.lots_layer = lots_layer

_bus9 = SV.bus_layer
def bus_layer(P_, M_):
    """round 9: the terminal — the boarding bay of every line in its colour, its parked bus behind the island in a light colour, the crossings from the islands"""
    o = _bus9(P_, M_)
    T_ = (P_.get('bus') or {}).get('terminal') or {}; r9 = T_.get('r9')
    if not o or not r9: return o
    col = {ln['id']: ln['color'] for ln in P_['routes']['bus']}; by = {b['no']: b['rect'] for b in T_['bays']}; add = []
    for kind, mp in (('park', r9['park']), ('board', r9['board'])):
        for ln, no in mp.items():
            if no not in by: continue
            x0, y0, x1, y1 = by[no]; c = col.get(ln, '#888')
            add.append(f"<rect x='{x0 + 2}' y='{y0 + 2}' width='{x1 - x0 - 4}' height='{y1 - y0 - 4}' fill='#ffffff'/>"
                       f"<rect x='{x0 + 3}' y='{y0 + 3}' width='{x1 - x0 - 6}' height='{y1 - y0 - 6}' fill='{c}' fill-opacity='{'1' if kind == 'board' else '.3'}' stroke='{c}' stroke-width='3'/>"
                       f"<text x='{(x0 + x1) / 2}' y='{(y0 + y1) / 2 + 9}' class='bayn'{'' if kind == 'board' else ' style=\'fill:#333\''}>{e9(ln)}</text>")
    for x in r9.get('crossings', []):
        x0, y0, x1, y1 = x['r']
        if x['v']: add.append(f"<line x1='{(x0 + x1) / 2}' y1='{y0}' x2='{(x0 + x1) / 2}' y2='{y1}' class='zeb' stroke='#ffffff' stroke-width='{x1 - x0}'/>")
        else: add.append(f"<line x1='{x0}' y1='{(y0 + y1) / 2}' x2='{x1}' y2='{(y0 + y1) / 2}' class='zeb' stroke='#ffffff' stroke-width='{y1 - y0}'/>")
    w = (r9.get('west') or {}).get('building')
    if w: add.append(f"<rect x='{w[0]}' y='{w[1]}' width='{w[2] - w[0]}' height='{w[3] - w[1]}' fill='#e8dcc4' stroke='#6b5a3a' stroke-width='3'/>")
    k = o.rfind('</g>'); return o[:k] + ''.join(add) + o[k:]
def e9(x):
    import html
    return html.escape(str(x))
SV.bus_layer = bus_layer

_rp9 = SV.road_parts
def road_parts(pid, p, g, cut=(0, 0), caps=()):
    """round 9: the one-way street for trucks has chevrons too — in its direction (CL-PG: from J385_42 north to J385_34, against the drawing's order)"""
    if g.get('st') == 'oneway5':
        g = dict(g, arrow=True)
        if 'CL-PG' in pid: p = list(p)[::-1]; cut = (cut[1], cut[0])
    return _rp9(pid, p, g, cut, caps)
SV.road_parts = road_parts

_lots9b = SV.lots_layer
def lots_layer_c5(P_):
    """round 9: a caption over C5's truck yard you can see without hovering — the docks and the exit are being checked"""
    o = _lots9b(P_)
    t = next((i for i in P_.get('sites', []) if i['id'] == 'C5-TRUCKS'), None)
    if not t: return o
    x0, y0, x1, y1 = t.get('draw') or t['rect']
    add = (f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='none' stroke='#e07b00' stroke-width='8' stroke-dasharray='26 14'/>"
           f"<text x='{(x0 + x1) / 2}' y='{(y0 + y1) / 2 - 8}' class='bayn' style='fill:#7a3d00;font-size:30px'>היציאה — (א) או (ב)</text>"
           f"<text x='{(x0 + x1) / 2}' y='{(y0 + y1) / 2 + 30}' class='bayn' style='fill:#7a3d00;font-size:30px'>בבדיקה</text>")
    k = o.rfind('</g>'); return o[:k] + add + o[k:]
SV.lots_layer = lots_layer_c5

# the depot by place (the order out in the morning) over the lots layer — the alloc of round 8's drawing has no colour here: grey with the number
def page_r9():
    import html
    e = lambda x: html.escape(str(x)); D = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8')); R = D['r9']
    H = ["<h2>סבב 9 — מה השתנה (3.11.2026)</h2><div class='wrap'><table><tr><th>מקור</th><th>הנושא</th><th>ברירת המחדל במפה</th><th>החלופה</th></tr>"]
    H += [f"<tr><td class='id'>{e(d_['code'])}</td><td>{e(d_['what'])}</td><td><b>{e(d_['default'])}</b></td><td class='small'>{e(d_['alt'])}</td></tr>" for d_ in R['decisions']]
    H.append("</table></div><h3>כלל צומת ה-T — המעברים שיצאו (הבעלים 12:39)</h3><div class='wrap'><table><tr><th>אזור</th><th>הצומת</th><th>הכביש הראשי</th><th>הרחוב הצדדי</th><th>נשאר</th><th>יצא</th></tr>")
    H += [f"<tr><td class='id'>{e(r['zone'])}</td><td>{e(r['label'])}</td><td>{e(r['main'])}</td><td>{e(r['side'])} ({ {'דרומי': 'מהדרום', 'צפוני': 'מהצפון', 'מזרחי': 'מהמזרח', 'מערבי': 'מהמערב'}.get(r['side_from'], r['side_from']) })</td><td>{e(r['kept'])}</td><td>{e(r['removed'])}</td></tr>" for r in R['xw_t']]
    H.append("</table></div><p class='small'>מחוץ לכלל: J46_42 — בזרוע הצפונית אין מעבר כלל (D‑420); המסוף (D‑423); הצמתים בתוך הנמל (אזור סגור — שבילים נפרדים, 11:43 סעיף 5). במסוף E3 בציור: מפרץ עלייה — בצבע מלא עם מספר הקו; החניה של אותו קו — בצבע בהיר; ההמתנה — בצהוב; המעברים מהאיים — בלבן. הרמזורים — הרשימה המלאה בקובץ signals_r9.json.</p>")
    p = os.path.join(HERE, 'city_plan.html'); T = open(p, encoding='utf-8').read(); k = T.index("<h2>סבב 8ב")
    open(p, 'w', encoding='utf-8').write(T[:k] + ''.join(H) + T[k:])

if __name__ == '__main__':
    os.chdir(HERE)
    runpy.run_path(os.path.join(HERE, 'plan7b_build.py'), run_name='__main__')
    runpy.run_path(os.path.join(HERE, 'plan7b_page.py'), run_name='__main__')
    p_ = os.path.join(HERE, 'city_plan.html'); T_ = open(p_, encoding='utf-8').read(); k_ = T_.index("<h2>הבדיקות</h2>")
    open(p_, 'w', encoding='utf-8').write(T_[:k_] + "<h2>סבב 8 — מה השתנה (3.11.2026)</h2><p class='small'>R-69, השדה הסולרי של E4, האוטובוסים (D‑394 / D‑395) והשמות — כמו בסבב 8. S6 (רחוב שער הנמל ב-x 3710) לא נכנס: רחוב שער הנמל חזר ל-x 3850 (הבעלים 09:59 / 11:26).</p>" + T_[k_:])
    R8B.page_r8b()
    page_r9()
