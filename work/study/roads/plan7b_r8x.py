# -*- coding: utf-8 -*-
"""3.11 · סבב 8 בלי S6 (לסבב 9: רחוב שער הנמל חוזר ל-x 3850 — הבעלים 09:59 / 11:26) — העתק של plan7b_r8.py בלי חלק 1 של S6, בלי D5/C5 כמו שנבנו (סבב 9 נותן את שלו), בלי בדיקת S6.
המקור: סבב 8 של מפת הדרכים — מודול pre/post כמו plan7b_r7, והרצה של אותה הרכבה (plan7b_build.py ואז plan7b_page.py):
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
DEFAULT = 'ברירת מחדל — לאישורך'
DEC = []   # the decisions of round 8, every one לאישורך
def dec(code, what, default, alt='', why=''): DEC.append(dict(code=code, what=what, default=default, alt=alt, why=why))
DONE = {}   # what was applied (the check of round 8 reads it)

import plan7b_net as P
import plan7b_city as CITY
import plan7b_svg as SV
import plan7b_r7 as R7

# ================================================================ 1 · the network (S6 as built + R-69 texts)
N = P.N; RD = {r['id']: r for r in P.R}
DONE['net'] = dict(nodes=[], note='S6 לא נכנס — רחוב שער הנמל ב-x 3850 כמו בסבב 7')
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
    # E4 — the solar field (R-73 / D‑398, LIKE-01): the panels and the inverter hut of the game (E4_SOLAR), with a service road from LC-E3
    it('E4', 'E4-SOLAR', 'field', (5580, 2860, 5770, 2985), 'השדה הסולרי — שורות פאנלים וביתן ממיר · נשאר',
       'R-73 / D‑398: "מה שהבעלים אהב" (LIKE-01, הבעלים 2.11 19:19) — המקום והגודל של היום במשחק (E4_SOLAR: הפאנלים 16.6 × 6.6 מ׳ בארבע שורות והביתן), '
       'עם שוליים; דרך שירות מרחוב התחנה (LC-E3). נשאר בכל בנייה מחדש של E4.', keep=True, like='LIKE-01', r5=True)
    dw('E4', 'DW-E4-SOLAR', 'LC-E3', (5412, 2925), 'דרך השירות של השדה הסולרי', 'מקצה רחוב התחנה מזרחה אל השדה הסולרי — נתיב אחד לטנדר התחזוקה.', to=(5580, 2925), lanes='1')
    DONE['sites'] = dict(solar=[5580, 2860, 5770, 2985])
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
    DONE['lots'] = dict(moved=moved, moved_d6=moved_d6)
    return items
R7.post = post

# ================================================================ 6 · the checks of round 8 (+ the reasons of the conflicts in the checks of the build)
_chk0 = R7.checks
R15_OK_S6 = {'CL-T: J371_34–J385_34': 'לאישורך (S6 כמו שנבנה): רחוב שער הנמל זז לשטח של D5-01; ברירת המחדל — רחוב המחסנים נגמר בכניסה בלבד (ימינה פנימה וימינה החוצה); החלופה — רחוב המחסנים זז מערבה ל-x 3710 (המגרש D4-03 עובר לצד המזרחי)',
          'J31_42–J371_42': 'לאישורך: 60 מ׳ בין שני הצמתים של שדרת הנמל — J31_42 ימינה בלבד (לא רמזור)'}
def checks(ctx, I):
    out = list(_chk0(ctx, I))
    g = sys._getframe(1).f_globals   # the build's own globals: the checks list, the stops, the segments
    seg = g.get('SEG', []); segby = {s['id']: s for s in seg}
    a = DONE.get('air', {}); s = DONE.get('sites', {}); n = DONE.get('names', {})
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
SEG_REN = {}   # S6 (map_r8_s6.json): CL-T/2 split into 2a and 2b; the game's CL-T/3 stays
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
        P_['title'] = 'תוכנית הדרכים של כל העיר — סבב 8'; P_['batch'] = '8'; P_['at'] = '3.11.2026'
        for line in P_['routes']['bus']:
            if line['id'] in FLEET:
                line['buses_calc'] = line.get('buses'); line['buses'] = FLEET[line['id']]
                if line['id'] == '4': line.update(headway_s=60, note='D‑394: שלושה אוטובוסים, אחד כל 60 שנ׳')
        P_['bus']['fleet'] = dict(lines=FLEET, spare=4, total=48, depot='D5-DEPOT', why='D‑394 / D‑395: 44 אוטובוסים של הקווים ו-4 רזרבה — 48 מקומות בחניון הלילה ב-D5')
        P_['r8'] = dict(at='3.11.2026', decisions=DEC, done={k: v for k, v in DONE.items()}, s6=None,
                        why='סבב 8 בלי S6: R-69, השדה הסולרי, האוטובוסים והשמות')
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


if __name__ == '__main__':
    os.chdir(HERE)
    runpy.run_path(os.path.join(HERE, 'plan7b_build.py'), run_name='__main__')
    runpy.run_path(os.path.join(HERE, 'plan7b_page.py'), run_name='__main__')
