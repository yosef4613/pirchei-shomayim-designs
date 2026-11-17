# -*- coding: utf-8 -*-
"""3.11 · סבב 8 של מפת הדרכים — מודול pre/post כמו plan7b_r7, והרצה של אותה הרכבה (plan7b_build.py ואז plan7b_page.py):
    python3 plan7b_r8.py      → city_plan.json, names.json, city_plan.html  (לפני כל הרצה: עותק של שלושתם ל-W/_to_delete)
המודול לא משנה אף קובץ אחר: הוא נטען לפני ההרכבה, משנה את הנתונים של המודולים (plan7b_net, plan7b_city, plan7b_svg) ועוטף את
ה-pre / post / checks של plan7b_r7, ואת label_layout ו-lots_layer של plan7b_svg (שני האחרונים — רק כדי להוסיף לפלט).
 1. S6 כמו שנבנה (הבעלים 20:29, ‏p511 · exp34/c5d5/map_r8_s6.json): רחוב שער הנמל (CL-PG) ב-x 3710, הצומת J371_34 ברחוב התעשייה,
    J385_42 → J371_42 (ו-J385_49 → J371_49 בדרך הרציף), PT-M מול הרחוב, המגרשים D5-01 ו-D5-DEPOT, הכניסות, התחנה ST-13;
    ועוד חניון המשאיות של C5 כמו שנבנה ב-p515 (הביתן מחוץ לרחבה, הכניסה 12.6 מ׳, היציאה לרחוב שער הנמל, בית הקפה והשירותים).
    ההתנגשויות — "לאישורך" עם הסיבה.
 2. R-69: שדרת השדה 3+3 אחרי השער עד סוף הנתיב השלישי (x 5600–5750, מעבר הדרגתי מסומן), 2+2 מתחת לגשר הרכבת ועד הטרמינל;
    התיאור של J46_16 מתוקן.
 3. R-73 / D‑398: מגרש לשדה הסולרי ב-E4 (המקום והגודל של E4_SOLAR במשחק) עם דרך שירות; "נשאר" (LIKE-01).
 4. D‑394 / D‑395: קו 4 — שלושה אוטובוסים, אחד כל 60 שנ׳; חניון הלילה ב-D5 — 48 מקומות (44 + 4), לפי הקווים והצבעים.
 5. F9 ו-G9 — "האי"."""
import json, math, os, sys, runpy
W = '/home/claude/work'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
S6 = json.load(open(W + '/exp34/c5d5/map_r8_s6.json', encoding='utf-8'))
DEPOT = json.load(open(W + '/clean_r2b_025637/tools/patches/c5d5v7d.json', encoding='utf-8'))['depot']   # the game's depot (p511): the 48 places by line and colour
DEFAULT = 'ברירת מחדל — לאישורך'
DEC = []   # the decisions of round 8, every one לאישורך
def dec(code, what, default, alt='', why=''): DEC.append(dict(code=code, what=what, default=default, alt=alt, why=why))
DONE = {}   # what was applied (the check of round 8 reads it)

import plan7b_net as P
import plan7b_city as CITY
import plan7b_svg as SV
import plan7b_r7 as R7

# ================================================================ 1 · the network (S6 as built + R-69 texts)
REN = {'J385_42': 'J371_42', 'J385_49': 'J371_49'}
def ren(o):
    if isinstance(o, str): return REN.get(o, o)
    if isinstance(o, list): return [ren(x) for x in o]
    if isinstance(o, tuple): return tuple(ren(x) for x in o)
    if isinstance(o, dict): return {k: ren(v) for k, v in o.items()}
    return o
N = P.N
mv = S6['nodes']['move'][0]
N['J371_42'] = dict(N.pop('J385_42'), id='J371_42', x=mv['x'], y=mv['y'], label=mv['label'],
                    why='S6 כמו שנבנה (p511, הבעלים 20:29): רחוב שער הנמל זז 14 מ׳ מערבה, והצומת איתו; השער הראשי של הנמל (PT-M) מולו. רמזור עם חץ.')
N['J371_49'] = dict(N.pop('J385_49'), id='J371_49', x=3710, label='דרך הרציף × דרך השער הראשי (מול רחוב שער הנמל)')
ad = S6['nodes']['add'][0]
N['J371_34'] = dict(id=ad['id'], x=ad['x'], y=ad['y'], kind=ad['kind'], label=ad['label'],
                    why='S6 כמו שנבנה (p511): הצומת החדש של רחוב שער הנמל ברחוב התעשייה, 60 מ׳ מ-J31_34; 14 מ׳ מ-J385_34 (רחוב המחסנים) — לאישורך (R-15).')
N['J31_42']['why'] = N['J31_42']['why'].replace('3850', '3710')
P.R[:] = ren(P.R)
for k in list(P.ROUTES): P.ROUTES[k] = ren(P.ROUTES[k])
RD = {r['id']: r for r in P.R}
cl = RD['CL-T']['nodes']; cl.insert(cl.index('J31_34') + 1, 'J371_34')
RD['CL-PG']['nodes'] = ['J371_34', 'J371_42']
RD['CL-PG']['why'] = RD['CL-PG'].get('why', '') + ' סבב 8 (S6 כמו שנבנה, p511): ב-x 3710, על השטח של D5-01 הישן — מטען הרכבת, הרווח והסדנה (הבעלים 20:29).'
RD['PT-M']['why'] = S6['segments']['replace']['PT-M/1']['note']
for line in P.ROUTES['bus']:
    p = line['path']; q = [p[0]]
    for a, b in zip(p, p[1:]):
        if {a, b} == {'J385_34', 'J31_34'}: q.append('J371_34')
        q.append(b)
    line['path'] = q
    line['stops'] = [tuple(['J31_34', 'J371_34'] + list(s[2:])) if set(s[:2]) == {'J31_34', 'J385_34'} else s for s in line['stops']]
for t in P.ROUTES.get('truck', []):
    if t['id'] == 'TRK-2': t['path'] = ['J371_49', 'J371_42', 'J371_34', 'J31_34', 'J25_34']
# the bays as built (S6, rule 10 — לאישורך): with J371_34 and J371_42, CL-T between J31_34 and J371_34 and AR-S between J31_42 and J371_42 are 60 m
# (49 m between the curbs) — no room for a bay by any rule. ST-13 was built there (p511): the bay 15 m from the edge of the junction behind and
# 10.6 m from the one ahead (map_r8_s6.json: the pole of the westbound bay at x 3430). ST-07 (lines 1 and 3 of the map, not built yet) takes
# the same place on AR-S. The build has no way to place a bay by its built position, so the second pass over the bus lines (the end stops,
# right before the check of every bay) sets these bays: t0 from the first node of the stop, both sides, marked relaxed + as_built.
AS_BUILT = {frozenset(('J31_34', 'J371_34')): 205, frozenset(('J31_42', 'J371_42')): 185}   # ST-07: between the crosswalks of AR-S (4 m from each, 13.1 / 12.6 m from the edges)
AS_BUILT_WHY = {'התעשייה הקלה · בית הזיקוק': 'S6 כמו שנבנה (p511, כלל 10 — לאישורך): עם J371_34 נשארו 60 מ׳ בין J31_34 ל-J371_34 (49 מ׳ בין השפות); '
                                               'ST-13 נבנתה 15 מ׳ מקצה הצומת שמאחור ו-10.6 מ׳ מקצה הצומת שלפנים (במקום 20)',
                'בית הזיקוק · מסוף המכולות': 'סבב 8 (לאישורך): עם J371_42 נשארו 60 מ׳ בין J31_42 ל-J371_42 (49 מ׳ בין השפות); המפרץ באמצע, בין שני מעברי החצייה '
                                              '(13.1 / 12.6 מ׳ מקצות הצמתים) — נבנה עם הקווים 1 ו-3 של המפה'}
def _as_built_bays(g):
    for st in g['STOPS']:
        t0 = AS_BUILT.get(st['key'])
        if t0 is None or st.get('bay_list') is not None: continue
        a, b = st['a'], st['b']; s_, pa, L_, u, r = g['seg_frame'](a, b); e_ = g['CW'](s_['cls']) / 2; BAY, BAYL, JUNC, N_ = g['BAY'], g['BAYL'], g['JUNC'], g['N']
        if a not in AS_BUILT_NODES.get(st['key'], (a,)): t0 = L_ - t0 - BAYL
        st['bay_list'] = []
        for (da, db) in st['bays']:
            sd = 1 if (da, db) == (a, b) else -1; sv = (r[0] * sd, r[1] * sd)
            def P_(t, off): return [round(pa['x'] + u[0] * t + sv[0] * off, 1), round(pa['y'] + u[1] * t + sv[1] * off, 1)]
            poly = [P_(t0, e_ - 2), P_(t0 + BAY['entry'], e_ + BAY['depth']), P_(t0 + BAY['entry'] + BAY['stop'], e_ + BAY['depth']), P_(t0 + BAYL, e_ - 2)]
            ja = (t0 - g['cross_hw'](a, s_['road'])) if a in JUNC else None; jb = (L_ - t0 - BAYL - g['cross_hw'](b, s_['road'])) if b in JUNC else None
            near_ = (jb if sd == 1 else ja); far_ = (ja if sd == 1 else jb)
            g['BL'].setdefault(st['key'], []).append((t0 - 30, t0 + BAYL + 30, sd))
            st['bay_list'].append(dict(side=sd, dir=f"{da}→{db}", t0=round(t0), poly=poly, pole=P_(t0 + BAYL / 2, e_ + BAY['depth'] + 18),
                                       to_junction_m=round(min(x for x in (ja, jb) if x is not None) / 10, 1) if (ja is not None or jb is not None) else None,
                                       toward=N_[db]['label'], near_m=round(near_ / 10, 1) if near_ is not None else None, far_m=round(far_ / 10, 1) if far_ is not None else None,
                                       relaxed=True, as_built=True, why=AS_BUILT_WHY.get(st['name'], '')))
        st['seg'] = s_['id']; st['road'] = s_['road']
        g['stop_bad'][:] = [x for x in g['stop_bad'] if x != f"{st['name']}: אין מקום למפרץ"]
        g['STOP_EXC'].append(st['name'])
        DONE.setdefault('as_built_bays', []).append(dict(name=st['name'], seg=s_['id'], bays=[(bb['dir'], bb['near_m'], bb['far_m'], bb['pole']) for bb in st['bay_list']]))
AS_BUILT_NODES = {frozenset(('J31_34', 'J371_34')): ('J31_34',), frozenset(('J31_42', 'J371_42')): ('J31_42',)}   # t0 is measured from this node
class _Lines(list):
    """the bus lines: the second pass of the build over them (the end stops, ENDS = [] right before it) sets the bays as built"""
    def __iter__(self):
        g = sys._getframe(1).f_globals
        if g.get('ENDS') == [] and 'STOPS' in g and 'seg_frame' in g and not g.get('_R8_BAYS'):
            g['_R8_BAYS'] = True; _as_built_bays(g)
        return super().__iter__()
P.ROUTES['bus'] = _Lines(P.ROUTES['bus'])
DONE['net'] = dict(nodes=['J371_34 (חדש)', 'J385_42 → J371_42', 'J385_49 → J371_49'], cl_t=list(cl), cl_pg=RD['CL-PG']['nodes'], pt_m=RD['PT-M']['nodes'])
# R-69: the texts of the avenue and of J46_16
RD['AR-N']['why'] = ('הזרימה הגדולה בעיר היא נוסעי השדה אל המרכז והתחנה — הציר הראשי, 3 נתיבים לכל כיוון, משדרת המרכז מזרחה עד השער הקבוע (4800, 1600) '
                     'וממנו (דרך הנוסעים, R-69) 3+3 עד אחרי המחסום; מעבר הדרגתי מסומן ל-2+2 ב-x 5600–5750, ו-2+2 מתחת לגשר הרכבת ועד הטרמינל.')
N['J46_16'].update(label='שדרת השדה × שדרת המזרח × דרך המטען — שדרת השדה ממשיכה מזרחה אל השדה, 3+3',
                   why='הצומת מערבית ל-x 4719, שם מתחיל מקום ההמתנה לשער הנוסעים (2 נתיבי בדיקה ל-19 מכוניות עד המחסום ב-x 5600, D‑160); לכן שדרת המזרח על x 4600. '
                       'מזרחה ממנו שדרת השדה נשארת 3+3 (R-69) עד אחרי המחסום, עם מעבר הדרגתי ל-2+2 לפני גשר הרכבת.')
dec('R-69', 'הדרך לשדה במפה: 3+3 עד x 5600, מעבר הדרגתי של 15 מ׳ (x 5600–5750), 2+2 מתחת לגשר הרכבת ועד הטרמינל',
    DEFAULT + ' — המעבר אחרי המחסום של שער הנוסעים ולפני הגשר; במשחק (p512) אותו מקום', 'מעבר הדרגתי מיד אחרי השער (x 4800), אם המחסום יוצא')

# ================================================================ 2 · the airport road (R-69): AIR-PAX3 (3+3) to x 5600, the taper, AIR-PAX (2+2)
_air0 = CITY.airport
def airport():
    A = _air0(); rs = A['roads']
    k = next(i for i, r in enumerate(rs) if r['id'] == 'AIR-PAX'); r = rs[k]
    r.update(pts=[[5600, 1600], [6120, 1600]], label='דרך הנוסעים — 2 נתיבים לכל כיוון, מסוף הנתיב השלישי מתחת לגשר הרכבת ועד הטרמינל')
    r['taper'] = dict(x0=5600, x1=5750, side=1, label='מעבר הדרגתי מסומן אחרי המחסום: 3 → 2 נתיבים, לפני גשר הרכבת (R-69)')
    rs.insert(k, dict(id='AIR-PAX3', label='שדרת השדה אחרי השער — 3 נתיבים לכל כיוון עד המחסום והמעבר ההדרגתי (R-69)', pts=[[4800, 1600], [5600, 1600]],
                      lanes=6, oneway=False, cls='main'))
    DONE['air'] = dict(pax3=[[4800, 1600], [5600, 1600]], taper=[5600, 5750], pax=r['pts'])
    return A
CITY.airport = airport

# ================================================================ 3 · the names: F9 and G9 are "האי" (names.json — the build writes it from SV.ZN)
SV.ZN['F9'] = ('האי', 'island'); SV.ZN['G9'] = ('האי', 'island')
DONE['names'] = {z: SV.ZN[z][0] for z in ('F9', 'G9', 'H9')}

# ================================================================ 4 · the sites (pre): D5 (S6 as built), C5 (p515 as built), E4 (the solar field)
_pre0 = R7.pre
def pre(S, DW, it, dw):
    _pre0(S, DW, it, dw)
    by = {i['id']: i for i in S}; bd = {d['id']: d for d in DW}
    # D5 — the night depot as built (p511): 16 lanes of 3.5 m, 3 buses each; 44 of the lines + 4 spare, by line and colour (D‑394 / D‑395)
    d5 = by['D5-DEPOT']; L = list(S6['lots']['D5-DEPOT']['rect']); L[2] = min(L[2], 4448)   # the band of AR-E (x 4600, 3+3 with its sidewalk) begins at x 4448; in the game AR-E is at x 4611
    lines = {}
    for b in DEPOT['lanes']: lines.setdefault(b['line'], []).append(b)
    alloc = [dict(lane=b['lane'], pos=b['pos'], line=b['line'], color=b.get('mapColor'), x=b['x'], y=b['y'], w=b['w'], h=b['h']) for b in DEPOT['lanes']]
    d5.update(rect=L, label='חניון הלילה של האוטובוסים — 48 מקומות: 44 של הקווים ו-4 רזרבה, לפי הקווים והצבעים',
              why='S6 כמו שנבנה (p511): 16 נתיבים של 3.5 מ׳, 3 אוטובוסים של 13.5 מ׳ בכל נתיב; נכנסים מצפון (רחוב התעשייה) ויוצאים במערב (רחוב שער הנמל). '
                  'כל נתיב — קו אחד בצבע שלו, חוץ מנתיב אחד (קו 2 וקו 5): עם 14 / 4 / 8 / 3 / 7 / 8 ועוד 4 רזרבה צריך 17 נתיבים — לאישורך. '
                  'בבוקר האוטובוסים יוצאים למסוף בהדרגה ובלילה חוזרים (D‑395, כשהקווים חוזרים).',
              stalls=48, depot=dict(lanes=16, per=3, aisle=110, alloc=alloc, counts={k: len(v) for k, v in lines.items()}))
    for k in ('DW-D5-IN', 'DW-D5-OUT'):
        if k in bd and k in S6['driveways']:
            q = S6['driveways'][k]; bd[k]['at'] = tuple(q['at'])
            if q.get('to'): bd[k]['to'] = tuple(q['to'])
    bd['DW-D5-OUT']['why'] = 'אל רחוב שער הנמל (ב-x 3710), 20 מ׳ משדרת הנמל — כמו שנבנה (p511).'
    # D5-01 as built (p511): the strip between CL-PG and the depot — the shipping office, the rail freight and the workshop, with its dock
    q = S6['lots']['D5-01']
    it('D5', 'D5-01', 'yard', tuple(q['rect']), q['label'] + ' — המשרד, הרציף והחצר',
       'S6 כמו שנבנה (p511, הבעלים 20:29): רחוב שער הנמל זז ל-x 3710, על השטח של D5-01 הישן; בין הרחוב לחניון הלילה — משרד השילוח ומטען הרכבת '
       '(מטבלת השימושים של D5: "משרד שילוח"), עם רציף לסמי ולמשאית ויציאה לרחוב שער הנמל.', use=q['use'], r5=True, r8=True)
    dq = S6['driveways']['DW-D5-01']
    dw('D5', 'DW-D5-01', 'CL-PG', tuple(dq['at']), dq['label'], 'מרחוב שער הנמל, 47 מ׳ מרחוב התעשייה — כמו שנבנה (p511).', to=(dq['at'][0] + 58, dq['at'][1]))
    dec('S6-D5', 'חניון הלילה: 48 מקומות ב-16 נתיבים של 3 — נתיב אחד מעורב (קו 2 וקו 5)', DEFAULT,
        '17 נתיבים (חניון רחב ב-3.5 מ׳), או שינוי בכמויות של הקווים', 'הכמויות 14/4/8/3/7/8 + 4 לא מתחלקות ל-16 × 3 בלי ערבוב')
    # C5 — the truck park as built (p515): 4 angled docks, the booth north of the entry, the entry of 12.6 m, the exit to CL-PG
    t = by['C5-TRUCKS']; t.update(rect=[3178, 3870, 3545, 4124], stalls=4, label='חניון המשאיות — 4 רציפים באלכסון ו-8 חניות עובדים',
                                  why='p515 (הביקורת על S7F210): 4 רציפים של 45° על החזית של מסוף הרציפים ורחבת תמרון של 8 מ׳ ומעלה; סמי של 16.5 מ׳ נכנס מרחוב בית הזיקוק, '
                                      'נוסע ברוורס לכל רציף כשבשאר עומד סמי, ויוצא קדימה לרחוב שער הנמל (בדיקה קבועה במשחק). החניות הארוכות לא נכנסות עם כניסה שעובדת — לאישורך.')
    for k, r in (('C5-GATE', [3186, 3962, 3226, 4002]), ('C5-CAFE', [3548, 3888, 3598, 3948]), ('C5-WC', [3552, 3990, 3598, 4040])):
        if k in by: by[k]['rect'] = r; by[k]['why'] = by[k].get('why', '') + ' סבב 8: כמו שנבנה (p511 / p515).'
    if 'DW-C5-TRUCKS' in bd: bd['DW-C5-TRUCKS'].update(at=(3164, 4053), to=(3240, 4053), why='12.6 מ׳ — הכניסה של הסמי (p515), 20 מ׳ משדרת הנמל.')
    dw('C5', 'DW-C5-TRUCKS-OUT', 'CL-PG', (3651, 4070), 'היציאה של חניון המשאיות — אל רחוב שער הנמל',
       'p515: הסמי יוצא קדימה מהרציף, לאורך הרחבה, ופונה צפונה ברחוב שער הנמל — 18.9 מ׳ ממרכז הצומת עם שדרת הנמל, נתיב אחד ליציאה בלבד; '
       'לאישורך (בסבב 7 הייתה רק הכניסה).', to=(3560, 4070), lanes='1')
    if 'DW-D6-FUEL' in bd: bd['DW-D6-FUEL'].update(at=(3769, 4440), why='מדרך השער הראשי (PT-M, שזזה עם רחוב שער הנמל ל-x 3710), 19 מ׳ משדרת הנמל.')
    dec('C5-TRUCKS', 'חניון המשאיות של C5: 4 רציפים באלכסון, 0 חניות ארוכות, יציאה לרחוב שער הנמל', DEFAULT,
        'החניה הארוכה של הסמיים (10) במגרש אחר — למשל בחצר של D4 או ב-E5', 'ב-36 × 24 מ׳ סמי של 16.5 מ׳ נכנס ויוצא רק מ-4 רציפים באלכסון')
    # E4 — the solar field (R-73 / D‑398, LIKE-01): the panels and the inverter hut of the game (E4_SOLAR), with a service road from LC-E3
    it('E4', 'E4-SOLAR', 'field', (5580, 2860, 5770, 2985), 'השדה הסולרי — שורות פאנלים וביתן ממיר · נשאר',
       'R-73 / D‑398: "מה שהבעלים אהב" (LIKE-01, הבעלים 2.11 19:19) — המקום והגודל של היום במשחק (E4_SOLAR: הפאנלים 16.6 × 6.6 מ׳ בארבע שורות והביתן), '
       'עם שוליים; דרך שירות מרחוב התחנה (LC-E3). נשאר בכל בנייה מחדש של E4.', keep=True, like='LIKE-01', r5=True)
    dw('E4', 'DW-E4-SOLAR', 'LC-E3', (5412, 2925), 'דרך השירות של השדה הסולרי', 'מקצה רחוב התחנה מזרחה אל השדה הסולרי — נתיב אחד לטנדר התחזוקה.', to=(5580, 2925), lanes='1')
    DONE['sites'] = dict(depot=L, c5=t['rect'], solar=[5580, 2860, 5770, 2985])
R7.pre = pre

# ================================================================ 5 · the lots (post): D5-01 as built; the substation of E4 off the solar field
_post0 = R7.post
import plan7b_fill as FILL
def _lot(g, z, lid, label, use, rect, road, at, depth_dir, why):
    """a lot of the build's own kind (as its generator makes them): the lot, its driveway (a lowered curb, not a junction) and the stub drawn as a road"""
    x, y = at; inn = [x + depth_dir[0] * 60, y + depth_dir[1] * 60]
    s_ = next(s for s in g['SEG'] if s['road'] == road); cw = g['CW'](s_['cls']) / 2 - 3; hw = g['CLS'][s_['cls']]['halfW']
    st_in = [x - depth_dir[0] * (hw - cw), y - depth_dir[1] * (hw - cw)]
    tj = round(min(math.hypot(x - a, y - b) for a, b in g['JUNC_PTS']) / 10, 1)
    l = dict(id=lid, zone=z, kind='lot', use=use, label=label, rect=[float(v) for v in rect], future=True, front=road, dw=f"DW-{lid}", r8=True, why=why)
    g['LOTS'].append(l)
    g['LOT_DW'].append(dict(zone=z, id=f"DW-{lid}", road=road, at=[float(x), float(y)], label=f"הכניסה ל{label}", why='הנמכת שפה מהדרך שמול המגרש — לא צומת.',
                            to=None, lanes='1+1', to_junction_m=tj))
    g['SITE_ROADS'].append(dict(id=f"DW-{lid}", zone=z, kind='driveway', cls='driveway', lanes='1+1', hw=30, pts=[[float(x), float(y)], inn],
                                draw=[st_in, inn], label=f"הכניסה ל{label}", road=road, oneway=False))
    return l
def _drop_lot(g, lid):
    for key in ('LOTS', 'LOT_DW', 'SITE_ROADS'):
        g[key][:] = [o for o in g[key] if o['id'] not in (lid, f"DW-{lid}")]
def _refill(g, zones):
    """the free parcels of these zones again (plan7b_fill — the same rule as the build), after the lots moved"""
    for l in [l for l in g['LOTS'] if l.get('fill') and l['zone'] in zones]: g['LOTS'].remove(l); g['FILL_LOTS'].remove(l)
    g['FILL_UNPLANNED'][:] = [u for u in g['FILL_UNPLANNED'] if u.split(' ')[0] not in zones]
    F0 = g['free_scan']()
    for z in sorted(zones):
        if F0.get(z): g['FREE0'][z] = F0[z]
        else: g['FREE0'].pop(z, None)
        for k_, f_ in enumerate(F0.get(z, [])):
            nm, use, why, planned = FILL.name_for(z, SV.ZN[z][1], f_['rect'])
            if not planned: g['FILL_UNPLANNED'].append(f"{z} {int(f_['m'][0])}×{int(f_['m'][1])} מ׳")
            l_ = dict(id=f"{z}-F{k_ + 1}", zone=z, kind='lot', use=use, label=nm, rect=[float(v) for v in f_['rect']], future=True, front=None, fill=True, why=why,
                      size_m=[int(f_['m'][0]), int(f_['m'][1])])
            g['LOTS'].append(l_); g['FILL_LOTS'].append(l_)
def post(ctx):
    g = sys._getframe(1).f_globals   # the build's globals: its lots, their driveways, the fill and the free scan
    items = _post0(ctx)
    LOTS = ctx['LOTS']; moved = []; moved_d6 = []
    # E4 (R-73): the solar field stays (LIKE-01); the substation was on it — it moves to the strip north of the field, on LC-E3; the lot the
    # generator gave the substation (the place of the control centre in round 7) is the control centre again
    sub = next((l for l in LOTS if l['zone'] == 'E4' and l['label'] == 'תחנת משנה'), None)
    if sub and not any(l['zone'] == 'E4' and l['label'] == 'מרכז בקרה עירוני' for l in LOTS):
        old = sub['id']; nid = 'E4-03'
        for d in g['LOT_DW'] + g['SITE_ROADS']:
            if d['id'] == f"DW-{old}": d['id'] = f"DW-{nid}"; d['label'] = 'הכניסה למרכז בקרה עירוני'
        sub.update(id=nid, label='מרכז בקרה עירוני', dw=f"DW-{nid}", why='סבב 8: המקום שלו מסבב 7 (תחנת המשנה זזה מהשדה הסולרי).')
        _lot(g, 'E4', 'E4-02', 'תחנת משנה', 'rail', [5466, 2709, 5730, 2850], 'LC-E3', (5454, 2815), (1, 0),
             'סבב 8 (R-73 / D‑398): השדה הסולרי נשאר (LIKE-01), ותחנת המשנה זזה מעליו לרצועה שמצפון לו — 26 × 14 מ׳, מול רחוב התחנה.')
        moved.append(('E4-02 תחנת משנה', [5466, 2709, 5616, 2950], [5466, 2709, 5730, 2850])); moved.append(('E4-03 מרכז בקרה עירוני', list(sub['rect']), list(sub['rect'])))
    # D6: PT-M moved with CL-PG to x 3710 — the administration and customs lot is on its east side now (in round 7 on its west side, x 3600–3761);
    # the generator had put it on the place of the port warehouse 1 (D6-WH1, a row of the plan)
    adm = next((l for l in LOTS if l['zone'] == 'D6' and l['label'] == 'מנהלת נמל ומכס' and not l.get('fill')), None)
    if adm and adm['rect'][0] > 4000:
        lid = adm['id']; old = list(adm['rect']); _drop_lot(g, lid)
        _lot(g, 'D6', lid, 'מנהלת נמל ומכס', 'port', [3781, 4485, 3915, 4829], 'PT-M', (3769, 4660), (1, 0),
             'סבב 8: דרך השער הראשי (PT-M) זזה עם רחוב שער הנמל ל-x 3710 — המגרש עובר לצד המזרחי שלה, מול השער; המחסן D6-WH1 נשאר במקומו.')
        moved_d6.append((lid + ' מנהלת נמל ומכס', old, [3781, 4485, 3915, 4829]))
    _refill(g, {'D6', 'E4'})
    # E2 (R-69): the avenue is 3+3 (main) to x 5600 — its band 3.9 m wider on each side; the lots of the land side and the bridge AIR-1 follow it
    AL = {l['id']: l for l in ctx['AIRF']['lots']}; IB = {i['id']: i for i in items}
    AL['AIR-LAND-E2']['rect'] = [5430.0, 1005.0, 5720.0, 1446.0]
    AL['AIR-PWEST'].update(rect=[4850.0, 1312.0, 5190.0, 1446.0], stalls=16, label='P‑WEST — 16 חניות (2 נגישות, 2 טעינה)',
                           why=AL['AIR-PWEST']['why'] + ' סבב 8 (R-69): שדרת השדה 3+3 — המגרש 13.4 מ׳ במקום 17, ו-16 מקומות במקום 22 (לאישורך).')
    AL['AIR-PRENT'].update(rect=[5200.0, 1312.0, 5420.0, 1446.0], stalls=11, label='P‑RENT — השכרת רכב, 11 מקומות',
                           why=AL['AIR-PRENT']['why'] + ' סבב 8 (R-69): 11 מקומות במקום 14 (לאישורך).')
    for k in ('DW-PWEST-OUT', 'DW-PRENT-OUT'):
        x = IB[k]['pts'][0][0]; IB[k].update(pts=[[x, 1446], [x, 1470]], access=('air', 'AIR-PAX3'))
    IB['AIR-1'].update(rect=[5090, 1400, 5120, 1802], label='גשר הולכי הרגל AIR‑1 — מעל שדרת השדה (3+3), 3 × 36 מ׳')
    IB['AIR-1-N'].update(rect=[5080, 1400, 5130, 1446])
    IB['AIR-1-S'].update(rect=[5080, 1752, 5150, 1802], access=('road', 'AIR-PAX3'))
    dec('R-69-E2', 'צד היבשה של השדה (שלב 8): P‑WEST עם 16 מקומות (במקום 22) ו-P‑RENT עם 11 (במקום 14); הגשר AIR‑1 ארוך ב-7.8 מ׳',
        DEFAULT + ' — שדרת השדה 3+3 רחבה ב-3.9 מ׳ לכל צד, ומצפון למגרשים דרך המטען', 'חניון של שתי קומות ב-P‑WEST, או P‑RENT מצפון לדרך המטען')
    DONE['lots'] = dict(d501=S6['lots']['D5-01']['rect'], moved=moved, moved_d6=moved_d6)
    return items
R7.post = post

# ================================================================ 6 · the checks of round 8 (+ the reasons of the conflicts in the checks of the build)
_chk0 = R7.checks
R15_OK = {'CL-T: J371_34–J385_34': 'לאישורך (S6 כמו שנבנה): רחוב שער הנמל זז לשטח של D5-01; ברירת המחדל — רחוב המחסנים נגמר בכניסה בלבד (ימינה פנימה וימינה החוצה); החלופה — רחוב המחסנים זז מערבה ל-x 3710 (המגרש D4-03 עובר לצד המזרחי)',
          'J31_42–J371_42': 'לאישורך: 60 מ׳ בין שני הצמתים של שדרת הנמל — J31_42 ימינה בלבד (לא רמזור)'}
def checks(ctx, I):
    out = list(_chk0(ctx, I))
    g = sys._getframe(1).f_globals   # the build's own globals: the checks list, the stops, the segments
    seg = g.get('SEG', []); segby = {s['id']: s for s in seg}
    # the conflicts of map_r8_s6.json: R-15 and rule 10 — every one with its reason (לאישורך)
    for c in g.get('checks', []):
        if c['name'].startswith('R-15') and not c['ok']:
            parts = [x.strip() for x in c['det'].split('. ')[0].split(';')]
            left = [x for x in parts if not any(k in x for k in R15_OK)]
            reasons = [f"{k} — {v}" for k, v in R15_OK.items() if any(k in x for x in parts)]
            if not left:
                c['ok'] = True; c['det'] = 'החריגות — עם סיבה, לאישורך: ' + ' · '.join(reasons) + '. ' + c['det']
            for k, v in R15_OK.items():
                if any(k in x for x in parts): dec('R-15', k, v)
    # R-46 / R-63: the bays as built (ST-13, ST-07) — every one with its reason (לאישורך), like the other stops of the list
    import re
    for c in g.get('checks', []):
        if c['name'].startswith('R-46') and not c['ok']:
            left = [n for n in g.get('EXC_ND', []) if n not in AS_BUILT_WHY]
            for nm, why in AS_BUILT_WHY.items():
                c['det'] = re.sub(r'(\(' + re.escape(nm) + r'\): [^;]*?) — אין סיבה', lambda m: m.group(1) + ' — ' + why, c['det'])
            if not left: c['ok'] = True
    for row in g.get('STOP_EXC_ROWS', []):
        if row['name'] in AS_BUILT_WHY: row.update(why=AS_BUILT_WHY[row['name']], default='המפרץ כמו שנבנה ב-S6 (ST-13), ו-ST-07 באמצע הקטע — לאישורך')
    for cf in S6['conflicts']:
        if cf['rule'] == 'כלל 10': dec('כלל 10', cf['what'], DEFAULT + ' — המפרצים כמו שנבנו', 'תחנה בלי מפרץ, או בקטע הסמוך בקו')
    dec('כלל 10', 'ST-07 (בית הזיקוק · מסוף המכולות, שדרת הנמל): 60 מ׳ בין J31_42 ל-J371_42 — המפרץ באמצע, בין שני מעברי החצייה (13.1 / 12.6 מ׳ מקצות הצמתים)',
        DEFAULT + ' — נבנה עם הקווים 1 ו-3 של המפה', 'התחנה בלי מפרץ, או בקטע הסמוך (J371_42–J46_42) יחד עם "שער הנמל הראשי"')
    a = DONE.get('air', {}); s = DONE.get('sites', {}); n = DONE.get('names', {})
    st = [x for x in g.get('STOPS', []) if x.get('id') == 'ST-13']
    out.append(('סבב 8 — S6 כמו שנבנה (p511 · map_r8_s6.json): רחוב שער הנמל ב-x 3710, J371_34, ‏J371_42, ‏PT-M מולו, D5-01 ו-D5-DEPOT, הכניסות; ההתנגשויות לאישורך',
                bool(DONE.get('net') and s.get('depot') and DONE.get('lots')) and segby.get('CL-PG/1', {}).get('pts', [[0]])[0][0] == 3710,
                f"הצמתים: {', '.join(DONE['net']['nodes'])}; רחוב התעשייה: {' → '.join(DONE['net']['cl_t'])}; רחוב שער הנמל: {' → '.join(DONE['net']['cl_pg'])}; "
                f"PT-M: {' → '.join(DONE['net']['pt_m'])}; D5-DEPOT {s.get('depot')}; D5-01 {DONE['lots']['d501']}; ST-13: {len(st)} תחנה; "
                f"חניון המשאיות של C5 כמו ב-p515: {s.get('c5')}, הביתן מחוץ לרחבה, הכניסה 12.6 מ׳ והיציאה לרחוב שער הנמל; "
                f"PT-M זזה — המגרש של המנהלה והמכס עבר לצד המזרחי שלה: {DONE['lots'].get('moved_d6')}; "
                f"המפרצים כמו שנבנו (כלל 10, לאישורך): {[(b['name'], [(x[0], x[1], x[2]) for x in b['bays']]) for b in DONE.get('as_built_bays', [])]}."))
    out.append(('R-69 — שדרת השדה 3+3 עד אחרי המחסום, מעבר הדרגתי מסומן ל-2+2 לפני גשר הרכבת, 2+2 עד הטרמינל',
                bool(a) and a.get('taper') == [5600, 5750],
                f"דרך הנוסעים: 3+3 {a.get('pax3')}, מעבר הדרגתי x {a.get('taper')}, 2+2 {a.get('pax')}; התיאור של J46_16 תוקן."))
    sl = [x for x in ctx['SITES'] if x['id'] == 'E4-SOLAR']
    hit = [r['id'] for r in ctx['RAILS'] if sl and any(sl[0]['rect'][0] - 20 < p[0] < sl[0]['rect'][2] + 20 and sl[0]['rect'][1] - 20 < p[1] < sl[0]['rect'][3] + 20 for p in r['pts'])]
    out.append(('R-73 / D‑398 — השדה הסולרי ב-E4 נשאר (LIKE-01), עם דרך שירות; תחנת המשנה לא עליו',
                bool(sl) and not hit, f"E4-SOLAR {sl[0]['rect'] if sl else '—'} · דרך שירות DW-E4-SOLAR מרחוב התחנה · תחנת המשנה זזה מהשדה, ומרכז הבקרה חזר למקומו: {DONE.get('lots', {}).get('moved')}" + (f" · מסילה קרובה: {hit}" if hit else '')))
    out.append(('השמות — F9 ו-G9 "האי" (names.json והמפה)', all(v == 'האי' for v in n.values()), json.dumps(n, ensure_ascii=False)))
    return out
R7.checks = checks

# ================================================================ 7 · the output: the title, round 8, the buses (D‑394 / D‑395)
FLEET = {'1': 14, '2': 4, '3': 8, '4': 3, '5': 7, '6': 8}
_lay0 = SV.label_layout
SEG_REN = {'CL-T/2': 'CL-T/2a', 'CL-T/3': 'CL-T/2b', 'CL-T/4': 'CL-T/3'}   # S6 (map_r8_s6.json): CL-T/2 split into 2a and 2b; the game's CL-T/3 stays
def _seg_ren(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and v in SEG_REN and k in ('id', 'seg'): o[k] = SEG_REN[v]
            else: _seg_ren(v)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str) and v in SEG_REN: o[i] = SEG_REN[v]
            else: _seg_ren(v)
def label_layout(P_):
    if not P_.get('r8'):
        for k in ('segments', 'bus', 'zones', 'transition'): _seg_ren(P_[k])
        for b in DONE.get('as_built_bays', []): b['seg'] = SEG_REN.get(b['seg'], b['seg'])
        DONE['net']['segments'] = 'רחוב התעשייה: J31_34–J371_34 הוא CL-T/2a ו-J371_34–J385_34 הוא CL-T/2b (S6, כמו במשחק); CL-T/3 (J385_34–J46_34) בלי שינוי'
        P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 8'; P_['batch'] = '8'; P_['at'] = '3.11.2026'
        for line in P_['routes']['bus']:
            if line['id'] in FLEET:
                line['buses_calc'] = line.get('buses'); line['buses'] = FLEET[line['id']]
                if line['id'] == '4': line.update(headway_s=60, note='D‑394: שלושה אוטובוסים, אחד כל 60 שנ׳')
        P_['bus']['fleet'] = dict(lines=FLEET, spare=4, total=48, depot='D5-DEPOT', why='D‑394 / D‑395: 44 אוטובוסים של הקווים ו-4 רזרבה — 48 מקומות בחניון הלילה ב-D5')
        P_['r8'] = dict(at='3.11.2026', decisions=DEC, done={k: v for k, v in DONE.items()}, s6=S6['id'],
                        why='סבב 8: S6 כמו שנבנה, R-69, השדה הסולרי, האוטובוסים והשמות — ההתנגשויות לאישורך')
    return _lay0(P_)
SV.label_layout = label_layout

# the depot by line and colour, and the solar panels — over the lots layer of the drawing
_lots0 = SV.lots_layer
def lots_layer(P_):
    o = _lots0(P_); add = []
    for i in P_.get('sites', []):
        dp = i.get('depot') or {}
        for b in dp.get('alloc', []):
            add.append(f"<rect x='{SV.f1(b['x'] + 2)}' y='{SV.f1(b['y'] + 4)}' width='{SV.f1(b['w'] - 4)}' height='{SV.f1(b['h'] - 8)}' rx='6' fill='{b.get('color') or '#8a8f96'}' opacity='.95'/>")
        if i['id'] == 'E4-SOLAR':
            x0, y0, x1, y1 = i['rect']
            for k in range(4): add.append(f"<rect x='{x0 + 14}' y='{y0 + 18 + k * 18}' width='{x1 - x0 - 70}' height='12' fill='#2d4a7a' stroke='#9fb6d8' stroke-width='1.5'/>")
            add.append(f"<rect x='{x1 - 50}' y='{y1 - 40}' width='40' height='24' fill='#8e9aa8' stroke='#556' stroke-width='2'/>")
    k = o.rfind('</g>'); return o[:k] + ''.join(add) + o[k:]
SV.lots_layer = lots_layer


def page_r8():
    """the page (plan7b_page.py writes it): a section of round 8 — what changed and what is לאישורך — before the checks"""
    import html
    e = lambda x: html.escape(str(x)); D = json.load(open(os.path.join(HERE, 'city_plan.json'), encoding='utf-8')); R = D['r8']; dn = R['done']
    dp = next(i for i in D['sites'] if i['id'] == 'D5-DEPOT')['depot']
    rows = [('S6 כמו שנבנה', 'רחוב שער הנמל (CL-PG) ב-x 3710 מ-J371_34 (חדש, ברחוב התעשייה) עד J371_42 (היה J385_42); J385_49 → J371_49; דרך השער הראשי (PT-M) מולו. '
             + dn['net'].get('segments', '') + '. המגרשים D5-01 (שילוח ומטען רכבת) ו-D5-DEPOT, הכניסות DW-D5-01, ‏DW-D5-IN, ‏DW-D5-OUT כמו שנבנו; המנהלה והמכס של D6 עברו לצד המזרחי של PT-M.'),
            ('C5 — חניון המשאיות (p515)', '4 רציפים באלכסון, 8 חניות עובדים, הביתן מחוץ לרחבה, הכניסה מרחוב בית הזיקוק (DW-C5-TRUCKS) והיציאה החדשה לרחוב שער הנמל (DW-C5-TRUCKS-OUT); בית הקפה והשירותים כמו שנבנו.'),
            ('R-69', 'שדרת השדה 3+3 מהשער (x 4800) עד המחסום (x 5600), מעבר הדרגתי מסומן ל-2+2 ב-x 5600–5750, ו-2+2 מתחת לגשר הרכבת ועד הטרמינל; התיאור של J46_16 תוקן. '
             'בצד היבשה (שלב 8): P‑WEST ו-P‑RENT קטנים יותר, והגשר AIR‑1 ארוך יותר.'),
            ('R-73 / D‑398', 'השדה הסולרי של E4 (E4-SOLAR, ‏19 × 12.5 מ׳ — המקום והגודל של היום) נשאר (LIKE-01), עם דרך שירות מרחוב התחנה; תחנת המשנה זזה מעליו לרצועה שמצפון לו, ומרכז הבקרה במקומו מסבב 7.'),
            ('D‑394 / D‑395', 'קו 4 — שלושה אוטובוסים, אחד כל 60 שנ׳. חניון הלילה ב-D5: 48 מקומות — ' + ', '.join(f"קו {k}: {v}" for k, v in sorted(dp['counts'].items())) + ' (44 של הקווים ו-4 רזרבה), בצבעים של הקווים.'),
            ('השמות', 'F9 ו-G9 — "האי" (גם H9).')]
    H = ["<h2>סבב 8 — מה השתנה (3.11.2026)</h2><div class='wrap'><table><tr><th>נושא</th><th>מה במפה</th></tr>"]
    H += [f"<tr><td class='id'>{e(a_)}</td><td class='small'>{e(b_)}</td></tr>" for a_, b_ in rows]
    H.append("</table></div><h3>לאישורך — ברירות המחדל של סבב 8</h3><div class='wrap'><table><tr><th>מקור</th><th>הנושא</th><th>ברירת המחדל במפה</th><th>החלופה</th></tr>")
    H += [f"<tr><td class='id'>{e(d_['code'])}</td><td>{e(d_['what'])}</td><td><b>{e(d_['default'])}</b></td><td class='small'>{e(d_['alt'])}</td></tr>" for d_ in R['decisions']]
    H.append("</table></div>")
    p = os.path.join(HERE, 'city_plan.html'); T = open(p, encoding='utf-8').read(); k = T.index("<h2>הבדיקות</h2>")
    open(p, 'w', encoding='utf-8').write(T[:k] + ''.join(H) + T[k:])


if __name__ == '__main__':
    os.chdir(HERE)
    runpy.run_path(os.path.join(HERE, 'plan7b_build.py'), run_name='__main__')
    runpy.run_path(os.path.join(HERE, 'plan7b_page.py'), run_name='__main__')
    page_r8()
