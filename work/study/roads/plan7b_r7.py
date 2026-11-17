# -*- coding: utf-8 -*-
# 2.11 · round 7 of the map (the review 05:30 — R-64, R-61, R-65): every item of the master plan that the map lacked or drew only in part,
# at real size (10 px = 1 m), each with its way in (a road, a path or a pier), clear of the roads, the rails and the lots of the map.
# Nothing here touches the network (nodes, roads, segments) or the zones C4, D4, C5 and D5.
#   pre(S, DW)  — the sites of the zones already detailed (A2, A4, A5, C3 pads by the table of R-61; the car park of E3), before the lots
#   post(ctx)   — after the lots and the fill of R-43: the lots that change (B2, C2, C6, D2, F3), the airport and the island items, the sea,
#                 the terrain of A0 — returns the new items (out['r7']) and the checks of every new kind
import math

# ---------------------------------------------------------------- R-61: one table for the helipads (default, for the owner's approval)
# the pad drawn = the rotor diameter of the helicopter that lands on it, rounded up; a thin dashed ring = 1.5 × its length
HELI = {
    'light': dict(he='מסוק קל (R44)', rotor=10.06, length=11.66, pad=10, ring=17.5),
    'h130': dict(he='H130', rotor=10.69, length=12.64, pad=11, ring=19),
    'aw139': dict(he='AW139', rotor=13.8, length=16.66, pad=14, ring=25),
}
def pad_px(t): h = HELI[t]; return h['pad'] * 5, h['ring'] * 5          # radii in px (10 px = 1 m)
def pad_txt(t): h = HELI[t]; return f"{h['he']}: מנחת Ø {h['pad']} מ׳, טבעת Ø {h['ring']:g} מ׳"
DEFAULT = 'ברירת מחדל — לאישורך'
DECISIONS = []   # (code, the subject, the default, the alternative) — every one marked לאישורך
def dec(code, what, default, alt=''): DECISIONS.append(dict(code=code, what=what, default=default, alt=alt))

# ---------------------------------------------------------------- pre: the detailed zones (before the lots are made)
def pre(S, DW, it, dw):
    byid = {i['id']: i for i in S}
    def drop(ids):
        for k in [k for k, i in enumerate(S) if i['id'] in ids][::-1]: S.pop(k)
        for k in [k for k, d in enumerate(DW) if d['id'] in ids][::-1]: DW.pop(k)
    # A2 — the hospital pad: AW139 (the medical helicopter)
    p = byid['A2-HELI']; r, ring = pad_px('aw139')
    p.update(r=r, safety=ring, heli='aw139', label='המנחת של בית החולים — ' + pad_txt('aw139'), why=p['why'] + ' סבב 7 (R-61): לפי טבלת המנחתים.')
    q = byid['PATH-A2-HELI-P']; q['rect'] = [(380, 1000), (600, 1000)]
    # A4 — R-61: roof pads on the fire station and the ambulance base (AW139), instead of the ground pad of D-149; R-62: 5 bays
    drop({'A4-HELI', 'A4-SVC-HELI', 'DW-A4-HELI'})
    f = byid['A4-FIRE']
    f.update(label='תחנת הכיבוי — 5 תאים: 3 כבאיות, מכלית קצף ותא פנוי (20 × 30 מ׳), מנחת AW139 על הגג',
             why='התאים פונים מזרחה; רחבה של 13.6 מ׳ עד שדרת המערב — יציאה ישירה בלי עמוד בפתח. R-62: 5 תאים, כמו בתנאי הקבלה של A4 (A4‑01) ובפער הקנוני (S124.2).')
    m = byid['A4-EMS']; m.update(label='בסיס האמבולנסים — 5 עמדות (20 × 23 מ׳), מנחת AW139 על הגג')
    for bid, c in (('A4-FIRE', (906, 2800)), ('A4-EMS', (906, 3215))):
        S.append(dict(zone='A4', id=bid + '-HELI', kind='pad', rect=None, c=c, r=r, safety=ring, heli='aw139', parent=bid, roof=True,
                      label=('מנחת הגג של תחנת הכיבוי — ' if bid == 'A4-FIRE' else 'מנחת הגג של בסיס האמבולנסים — ') + pad_txt('aw139'),
                      why='R-61: מנחת גג בגודל AW139 — מחליף את מנחת הקרקע של D‑149. ' + DEFAULT + '. הטבעת (25 מ׳) רחבה מהגג (20 מ׳) ויוצאת 2.5 מ׳ מעל הרחבה והמדשאה, בלי מכשול גבוה.'))
    pa = byid['PATH-A4-1']; pa['why'] = 'מהמדרכה של שדרת הקריה, בין האולם לדרך השירות, אל המועדון, מסלול הריצה, הכדורסל והטניס.'
    # A4 — the running track (master plan A4: "מבני ספורט, מגרשים, מסלול") on the land the ground pad leaves
    S.append(dict(zone='A4', id='A4-TRACK', kind='path', rect=[(510, 2910), (765, 2910), (765, 3280), (510, 3280), (510, 2910)], hw=15, r7=True,
                  label='מסלול הריצה — לולאה של 125 מ׳, ברוחב 3 מ׳', why='תוכנית האב (A4): "מבני ספורט, מגרשים, מסלול". על השטח שמנחת הקרקע מפנה; מתחבר לשביל המגרשים.'))
    # A5 — the roof pad of the police station (its label always said so): H130
    r2, ring2 = pad_px('h130')
    S.append(dict(zone='A5', id='A5-POLICE-HELI', kind='pad', rect=None, c=(850, 3660), r=r2, safety=ring2, heli='h130', parent='A5-POLICE', roof=True,
                  label='מנחת הגג של תחנת המשטרה — ' + pad_txt('h130'), why='תוכנית האב (A5): תחנת המשטרה עם מנחת על הגג. R-61: מסוק המשטרה H130; הטבעת בתוך הגג (30 × 20 מ׳).'))
    # C3 — the pad of the player's home: AW139 (R-61: "מסוק של 16.66 מ׳"); 0.5 m east, so the hangar of level 8 stays outside the ring
    h = byid.get('C3-PH-HELI')
    if h:
        h.update(c=(h['c'][0] + 5, h['c'][1] + 5), r=r, safety=ring, heli='aw139', label='המנחת של בית השחקן — ' + pad_txt('aw139'),
                 why=h['why'] + ' סבב 7 (R-61): לפי טבלת המנחתים; זז 0.5 מ׳ מזרחה ו-0.5 מ׳ דרומה — המבנה למסוק (רמה 8) מחוץ לטבעת, ושום דבר לא זז ב-D4.')
    # E3 — the car park of the station, with the north row E3-N1 (master plan E3; D-241)
    it('E3', 'E3-P', 'parking', (4800, 2172, 5340, 2310), 'חניון התחנה E3 — 28 מקומות; השורה הצפונית E3‑N1: 16 חניות (4 נגישות, 2 טעינה)',
       'תוכנית האב (E3): התחנה המרכזית, המסוף וחניון. השורה הצפונית E3‑N1 לפי D‑241 (חלק א): 16 חניות, מהן 4 נגישות ו-2 עמדות טעינה; '
       'בין המסוף לבין מחסן החבילות, נכנסים מרחוב המסוף.', stalls=28, r5=True)
    dw('E3', 'DW-E3-P', 'LC-E3', (5346, 2262), 'הכניסה לחניון התחנה', 'מרחוב המסוף, 36 מ׳ מהצומת עם דרך האי — לא צומת.', to=(5300, 2262))
    dec('R-61', 'טבלת המנחתים: מנחת בקוטר הרוטור (קל 10 מ׳, ‏H130 ‏11 מ׳, ‏AW139 ‏14 מ׳) וטבעת מקווקוות פי 1.5 מאורך המסוק (17.5, ‏19, ‏25 מ׳) — לכל המנחתים במפה',
        'כל 12 המנחתים במפה לפי הטבלה, ומסוק בגודל אמיתי על כל אחד', 'המנחתים בגודל הקודם (18–20 מ׳)')
    dec('R-61 / D‑149', 'מנחתי גג על תחנת הכיבוי ועל בסיס האמבולנסים ב-A4, בגודל AW139 — במקום מנחת הקרקע של D‑149', 'שני מנחתי גג; מנחת הקרקע ודרך השירות שלו יוצאים, ובמקומם מסלול הריצה',
        'מנחת הקרקע של D‑149 נשאר (Ø 14 מ׳, טבעת 25 מ׳)')
    dec('R-61', 'המנחת בווילה 4 (C3): בין הבית לבריכה יש 12.2 מ׳, וטבעת של מסוק קל היא 17.5 מ׳', 'המנחת יוצא מהווילה (לא במפה)', 'להזיז את הבריכה ולשים מנחת Ø 10 מ׳ עם טבעת 17.5 מ׳')
    dec('R-61', 'המבנה למסוק בבית השחקן (9.6 × 13 מ׳) קטן מ-AW139 (אורך 16.66 מ׳, רוטור 13.8 מ׳)', 'בגיליון של C3: מבנה של 18 × 15 מ׳ לפחות; במפה — רק המנחת, מחוץ לטבעת', 'מסוק קל בבית השחקן ומבנה של 13 × 11 מ׳')
    dec('R-62', 'תחנת הכיבוי ב-A4: 5 תאים (תנאי הקבלה A4‑01 ו-S124.2) מול 3 תאים בטבלת השימושים (D‑260)', '5 תאים: 3 כבאיות, מכלית קצף ותא פנוי — גם בשורה של טבלת השימושים', '3 תאים')

# ---------------------------------------------------------------- geometry
def ell(cx, cy, rx, ry, n=64): return [[round(cx + rx * math.cos(2 * math.pi * k / n), 1), round(cy + ry * math.sin(2 * math.pi * k / n), 1)] for k in range(n + 1)]
def ov(a, b, pad=0): return min(a[2], b[2]) - max(a[0], b[0]) > pad and min(a[3], b[3]) - max(a[1], b[1]) > pad
def gap(a, b): return math.hypot(max(0, max(a[0], b[0]) - min(a[2], b[2])), max(0, max(a[1], b[1]) - min(a[3], b[3])))
def band(p, q, hw):
    (ax, ay), (bx, by) = p, q
    return (min(ax, bx) - hw, min(ay, by) - hw, max(ax, bx) + hw, max(ay, by) + hw, 'diag') if (abs(ax - bx) > 1 and abs(ay - by) > 1) else \
           ((min(ax, bx), ay - hw, max(ax, bx), ay + hw) if abs(ay - by) <= 1 else (ax - hw, min(ay, by), ax + hw, max(ay, by)))
def bands(pts, hw): return [band(pts[k], pts[k + 1], hw) for k in range(len(pts) - 1)]
def dseg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy; t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)
def dpoly(x, y, p): return min(dseg(x, y, *p[k], *p[k + 1]) for k in range(len(p) - 1))
def plen(p): return sum(math.hypot(p[k + 1][0] - p[k][0], p[k + 1][1] - p[k][1]) for k in range(len(p) - 1))
def box_of(i):
    if i.get('c'): rr = i.get('ring', i.get('r', 0)); return (i['c'][0] - rr, i['c'][1] - rr, i['c'][0] + rr, i['c'][1] + rr)
    if i.get('pts'): xs = [q[0] for q in i['pts']]; ys = [q[1] for q in i['pts']]; h = i.get('hw', 0); return (min(xs) - h, min(ys) - h, max(xs) + h, max(ys) + h)
    return tuple(i['rect'])
def foot(i):   # the rectangles an item covers
    if i.get('pts') and i['kind'] not in ('contour', 'lane'): return bands(i['pts'], i.get('hw', 10))
    if i.get('c'): return [box_of(i)]
    return [tuple(i['rect'])] if i.get('rect') else []

# ---------------------------------------------------------------- post: everything else
WATER = {'pier', 'boat', 'berths', 'buoy', 'lane', 'rig', 'dock', 'fishstand', 'tugpier'}
MARK = {'xmark', 'corner', 'stopline', 'signal', 'gate', 'tower', 'bay', 'lights', 'contour', 'lane', 'buoy', 'runup', 'footbridge', 'unit', 'blast'}
def post(ctx):
    I = []
    def add(zone, id, kind, label, why, **kw): d = dict(zone=zone, id=id, kind=kind, label=label, why=why, stage=kw.pop('stage', None), **kw); I.append(d); return d
    LOTS, AIRF, ISLF = ctx['LOTS'], ctx['AIRF'], ctx['ISLF']; LB = {l['id']: l for l in LOTS}
    AL = {l['id']: l for l in AIRF['lots']}; IL = {l['id']: l for l in ISLF['lots']}
    def relot(lid, rect=None, label=None, why=None):
        l = LB[lid]
        if rect: l['rect'] = [float(v) for v in rect]
        if label: l['label'] = label
        if why: l['why'] = why
        l['r7'] = True; return l
    # ============================================================ A0 — the ridge: contour lines and hillshade (D-188)
    for k in range(6):
        add('A0', f'A0-CT{k + 1}', 'contour', f'קו גובה {k + 1}', 'D‑188: רכס הררי עם קווי גובה והצללה; הרכס לאורך דרך הרכס (x 600), הפסגה ב-(600, ‎−560).',
            pts=ell(600, -560, 110 + 85 * k, 170 + 55 * k), level=6 - k, clip=[0, -850, 1200, 0])
    add('A0', 'A0-SUMMIT', 'tower', 'פסגת הרכס', 'הנקודה הגבוהה של A0 — קצה דרך הרכס.', c=[600, -560], r=30, lbl=True)
    # ============================================================ A1 — the walking trail in the forest
    add('A1', 'A1-TRAIL', 'path', 'שביל ההליכה ביער — לולאה של 170 מ׳', 'תוכנית האב (A1): שביל הליכה. יוצא מהמדרכה של דרך הרכס ומקיף את היער המערבי; בלי רכב.',
        pts=[[546, 380], [420, 380], [420, 120], [140, 120], [140, 640], [420, 640], [420, 380]], hw=12, access=('road', 'LC-A0'), lbl=True)
    # ============================================================ C0, D0, E0 — the approach lights of runway 09; the track to them
    xs = [4950, 4850] + list(range(4750, 3200, -150))
    add('D0', 'AL-09', 'lights', 'אורות הגישה למסלול 09 — מ-x 3250 עד הסף (x 5000), כל 15 מ׳, ופס רוחב ב-x 4450', 'תוכנית האב (C0, ‏D0): אורות הגישה משתלבים בשדה, על עמודים שבירים; בלי מבנים ועצים גבוהים מתחת לנתיב הגישה (D‑164).',
        pts=[[x, -690] for x in xs], bars=[[4450, -780, 4450, -600], [3850, -760, 3850, -620]], access=('svc', 'AL-09-SVC'), zones=['C0', 'D0', 'E0'])
    add('D0', 'AL-09-SVC', 'svc', 'דרך התחזוקה של אורות הגישה — דרך עפר, נתיב אחד', 'מקצה דרך העפר של C0 לאורך קו האורות, ומשם גם אל דרך העפר של D0; לרכב התחזוקה בלבד.',
        pts=[[3110, -600], [3110, -660], [4780, -660]], hw=19.5, cls='track', access=('road', 'TR-C0'))
    # ============================================================ E0, F0, G0 — the perimeter road along the north fence (D-244)
    add('F0', 'AIR-PERIM-N', 'svc', 'דרך ההיקף — לאורך הגדר הצפונית והמערבית, נתיב אחד (3.9 מ׳)', 'תוכנית האב (E0, ‏F0): גדר ודרך היקפית (D‑244); מתחברת לכביש ההיקף של H0 ולרחבה המערבית — צד אווירי.',
        pts=[[4820, -60], [4820, -830], [9472, -830]], hw=19.5, cls='service', access=('air', 'AIR-PERIM'), zones=['E0', 'F0', 'G0', 'H0'])
    # ============================================================ H0 — the end of the runway: RESA, the localizer, the approach lights of 27
    add('H0', 'AIR-RESA', 'resa', 'שטח הבטיחות בקצה המסלול — 12 × 20 מ׳', 'תוכנית האב (H0): x 9300–9420 (חלק ו); משטח מהודק, בלי מכשול.', rect=[9300, -810, 9420, -570], access=('air', 'AIR-PERIM-N'), lbl=True)
    add('H0', 'AIR-LOC', 'loc', 'המשדר הכיווני — מערך האנטנות על הציר', 'תוכנית האב (H0): x 9430–9460 (חלק ו).', rect=[9430, -810, 9460, -570], access=('air', 'AIR-PERIM'))
    add('H0', 'AL-27', 'lights', 'אורות הגישה למסלול 27 — על הציר עד הגדר', 'תוכנית האב (H0): על הציר עד הגדר (x 9600); בכביש ההיקף — אורות שקועים.',
        pts=[[x, -690] for x in (9330, 9390, 9500, 9545, 9590)], access=('air', 'AIR-PERIM'))
    # ============================================================ F1, G1, H1 — the equipment pockets between the noses (D-213 (5)); H3 — of R1–R3
    PL = ctx['F_places']
    for nm, r in ctx['F_pockets']:
        z = ctx['zone_of']((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        add(z, 'AIR-' + nm, 'pocket', f"כיס ציוד {nm.replace('GSE-', '')} — {len(PL.get(nm, []))} רכבי שירות", 'תוכנית האב (F1): כיס ציוד בין החרטומים, מחוץ לדרך של המטוס (D‑213 (5)); לכל סוג שירות של העמדות שלו.',
            rect=r, access=('air', 'AIRSIDE'), air=True)
    for nm, r in (('GSE-R1|R2', [8711, 2426, 8965, 2545]), ('GSE-R2|R3', [9065, 2426, 9206, 2545])):
        add('H3', 'AIR-' + nm, 'pocket', f"כיס ציוד {nm.replace('GSE-', '')}", 'תוכנית האב (H3): בין החרטומים של R1–R3, לפני הכנפיים — מחוץ לדרך של המטוס (חלק ו2).', rect=r, access=('air', 'AIRSIDE'), air=True)
    # G3 — the pockets of GA, before the 5 m in front of the noses
    for nm, r in (('GA1|GA2', [7395, 2130, 7462, 2202]), ('GA2|GA3', [7552, 2130, 7619, 2202]), ('GA3|GA4', [7709, 2130, 7776, 2202]),
                  ('GA4|GA5', [7866, 2142, 7956, 2202]), ('GA5|GA6', [8046, 2142, 8159, 2202]), ('GA6|GA7', [8249, 2142, 8362, 2202])):
        add('G3', 'AIR-GSE-' + nm, 'pocket', f'כיס ציוד {nm}', 'תוכנית האב (G3): כיסי הציוד של התעופה הכללית — בין החרטומים, מחוץ לדרך של המטוס (חלק ו2).', rect=r, access=('air', 'AIRSIDE'), air=True)
    # G3 / H3 / the airside — a marked crossing wherever a service road crosses a taxiway or a stand: the aircraft first
    for sv in AIRF['service']:
        for l in AIRF['lots']:
            if l['kind'] not in ('taxi', 'stand'): continue
            a, b = sv['rect'], l['rect']
            if ov(a, b, 1):
                x = [max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])]
                if (x[2] - x[0]) * (x[3] - x[1]) < 400: continue
                z = ctx['zone_of']((x[0] + x[2]) / 2, (x[1] + x[3]) / 2)
                add(z, f"XM-{sv['id'][4:]}-{l['id'][4:]}", 'xmark', f"מעבר מסומן — {sv['label'].split(' — ')[0]} × {l['label']} — המטוס קודם", 'תוכנית האב (G3): מעבר מסומן במקום שבו מטוס חוצה דרך שירות; המטוס קודם (ביקורת 6).', rect=x, air=True)
    # H3 — the engine run-up: on R3 at night, with the blast fence (part ו2) — default for the owner
    add('H3', 'AIR-RUNUP', 'runup', 'הרצת המנועים — בעמדה R3, בלילה', 'תוכנית האב (H3): מקום חדש בשלב 8 (R4 יצאה ב-D‑252). ברירת מחדל: R3 בלילה, כשהעמדה פנויה, עם מחסום הדף לכיוון הים (חלק ו2). ' + DEFAULT + '.',
        rect=[9236, 2140, 9524, 2480], parent='AIR-R3', access=('air', 'AIRSIDE'), air=True, lbl=True)
    add('H3', 'AIR-BLAST', 'blast', 'מחסום ההדף מאחורי R3', 'קיר הדף בגובה 4 מ׳ לאורך הקצה הדרומי של העמדה.', rect=[9216, 2508, 9544, 2540], access=('air', 'AIRSIDE'), air=True)
    dec('H3-1', 'הרצת המנועים בשלב 8 (R4 יצאה ב-D‑252)', 'בעמדה R3 בלילה, עם מחסום הדף לכיוון הים', 'משטח הרצה נפרד — רק אם עמדה מרוחקת יוצאת (5 + 3)')
    # ============================================================ E2 — P-WEST, P-RENT and the hotel of the airfield with the crew hotel (D-241, R-65)
    le = AL['AIR-LAND-E2']; le['rect'] = [5430, 1005, 5720, 1475]; le['label'] = 'צד היבשה של המטען — חצר המשאיות, נתיב ההמתנה והביתן'; le['r7'] = True; le['road_ok'] = ['AIR-CARGO-RD']
    def alot(id, he, kind, r, **kw):
        l = dict(id=id, label=he, kind=kind, rect=[float(v) for v in r], airside=False, zone=ctx['zone_of']((r[0] + r[2]) / 2, (r[1] + r[3]) / 2), future=True, stage='8', r7=True, **kw)
        AIRF['lots'].append(l); return l
    alot('AIR-HOTEL', 'מלון השדה ומלון הצוותים — 57 × 18 מ׳, 6 קומות, כ-150 חדרים', 'building', [4850, 1005, 5420, 1185], floors=6,
         why='R-65 (ברירת מחדל לאישורך): מלון אחד לשדה ולצוותים, לפני השער (D‑241); מול דרך המטען, והולכי הרגל בגשר AIR‑1.')
    alot('AIR-PWEST', 'P‑WEST — 22 חניות (2 נגישות, 3 טעינה)', 'parking', [4850, 1312, 5190, 1482], stalls=22,
         why='D‑241 (חלק א): החניון של שירותי הקרקע לפני השער; נכנסים מדרך המטען, ויוצאים ימינה בלבד אל דרך הנוסעים.')
    alot('AIR-PRENT', 'P‑RENT — השכרת רכב, 14 מקומות', 'parking', [5200, 1312, 5420, 1482], stalls=14,
         why='D‑241 (חלק א): השכרת הרכב P‑WEST‑N, לצד P‑WEST; אותן כניסה ויציאה.')
    for k, (x, pk) in enumerate(((4890, 'AIR-PWEST'), (5300, 'AIR-PRENT'))):
        add('E2', f'DW-{pk[4:]}-OUT', 'svc', 'יציאה ימינה בלבד אל דרך הנוסעים', 'D‑241: הדרכים של P‑WEST ושל השכרת הרכב לכביש השדה — יציאה ימינה בלבד, לנתיב היוצא.',
            pts=[[x, 1482], [x, 1500]], hw=19.5, cls='driveway', access=('air', 'AIR-PAX'), air=True)
    add('E2', 'AIR-1', 'footbridge', 'גשר הולכי הרגל AIR‑1 — מעל דרך הנוסעים, 3 × 28 מ׳', 'D‑241 (חלק א): במקום מעבר החצייה AIR‑1 (x 5090–5120); הנחיתה הצפונית בשביל של P‑WEST, הדרומית ב-E3.',
        rect=[5090, 1440, 5120, 1766], access=('lot', 'AIR-PWEST'), air=True, lbl=True)
    add('E2', 'AIR-1-N', 'stair', 'הנחיתה הצפונית של AIR‑1 — מדרגות ומעלית', 'בתוך P‑WEST, על השביל שלו.', rect=[5080, 1436, 5130, 1482], parent='AIR-PWEST', access=('lot', 'AIR-PWEST'), air=True)
    add('E3', 'AIR-1-S', 'stair', 'הנחיתה הדרומית של AIR‑1 — מדרגות ומעלית', 'D‑241: הנחיתה הדרומית ב-E3, על המדרכה של דרך הנוסעים, מול המסוף.', rect=[5080, 1716, 5150, 1766], access=('road', 'AIR-PAX'))
    dec('R-65', 'המלונות', 'D2 על מגרש גדול יותר (24 × 44 מ׳); ‏A5 כמו שהוא; מלון השדה יחד עם מלון הצוותים (E2); מלון הים (F3); האי — אכסניית ההר כמלון', 'מלון הים ב-F4 ולא ב-F3')
    # ============================================================ F2 — the tower on the terminal, the fill bay, the corners for the semis, AIR-K, the car park's ground floor
    add('F2', 'AIR-TWR-ROOF', 'tower', 'מגדל הפיקוח — על גג הטרמינל', 'תוכנית האב (F2): המגדל על גגו (D‑244 (2)); תא של 10 מ׳ מעל אגף השערים.', c=[6900, 960], r=50, parent='AIR-CORE', air=True, lbl=True)
    fl = ctx['F_land']['FILL']
    add('F2', 'AIR-FILL', 'bay', 'מפרץ המילוי של מכליות הדלק — הנתיב המערבי של המחבר', 'תוכנית האב (F2) וחלק א: המכליות ממלאות מצד היבשה, בידי השומרים של שער הצד האווירי.',
        rect=[fl['x0'], fl['y0'], fl['x1'], fl['y1']], air=True, access=('air', 'AIR-CONN'), lbl=True)
    for k, (x, y, sx, sy) in enumerate(((6179, 1313, 1, 1), (7086, 1313, -1, 1), (7086, 1701, -1, -1), (6179, 1701, 1, -1))):
        add('F2', f'AIR-K{k + 1}', 'corner', f'פינה לסמי K{k + 1} — רדיוס 12 מ׳', 'תוכנית האב (F2): הפינות של הלולאה לסמי — השפה הפנימית קטומה ברדיוס 12 מ׳ (חלק ו).',
            c=[x + sx * 120, y + sy * 120], r=120, corner=[x, y], sgn=[sx, sy], air=True)
    add('F2', 'AIR-K', 'signal', 'הצומת AIR‑K — רמזור; קו עצירה לנתיב הנכנס ב-x 5810', 'תוכנית האב (F2): הצומת AIR‑K עם רמזור וקו עצירה לנתיב הנכנס (חלקים א, ו).', c=[6120, 1600], r=60, air=True)
    add('E2', 'AIR-K-STOP', 'stopline', 'קו העצירה של AIR‑K', 'ב-x 5810, בנתיבים הנכנסים.', rect=[5805, 1606, 5815, 1690], air=True)
    for id_, he, r_, why in (('AIR-MSCP-SHORT', 'קומת הקרקע — חניה קצרה, 31 מקומות', [6190, 1330, 6650, 1500], 'החניה הקצרה ליד החזית.'),
                             ('AIR-MSCP-TAXI', 'קומת הקרקע — תור המוניות, 12 מקומות', [6670, 1330, 7050, 1420], 'המוניות מחכות בתור לאורך הצד הצפוני, יוצאות לחזית.'),
                             ('AIR-MSCP-CHECK', 'קומת הקרקע — 4 מקומות לבדיקה הנוספת של שער הנוסעים', [6190, 1520, 6390, 1600], 'D‑241: מכונית שנבחרה לבדיקה נוספת ממשיכה לכאן, ליד הכניסה מהגישה.')):
        add('F2', id_, 'unit', he, 'תוכנית האב (F2): בקומת הקרקע של החניון הרב-קומתי — ' + why, rect=r_, parent='AIR-MSCP', air=True, access=('lot', 'AIR-MSCP'), lbl=True)
    # G2 — the airside gate of the staff and the service at x 7860, the queue inside the crew car park
    sg = ctx['F_staffGate']
    add('G2', 'AIR-STAFF-GATE', 'gate', 'שער הצד האווירי — עובדים ושירות (x 7860)', 'תוכנית האב (G2), חלק א: השער בגדר, ההמתנה בתוך חניון הצוות; מעבר לשער — דרך השירות לאורך הגדר.',
        rect=[sg['x'] - 8, sg['y0'], sg['x'] + 8, sg['y1']], air=True, access=('air', 'AIR-AIRROAD_W'))
    add('G2', 'AIR-STAFF-Q', 'unit', 'נתיב ההמתנה לשער — בתוך חניון הצוות', 'חלק א: התור לשער לא יוצא לכביש.', rect=[7600, 1470, 7855, 1520], parent='AIR-CREW', air=True, access=('lot', 'AIR-CREW'))
    # ============================================================ the pads of the airport and of the island — by the table (R-61); D-267
    for pid, t, why in (('AIR-H2', 'light', 'קל ותיירות'), ('AIR-H3', 'h130', 'תיירות ושכר'), ('AIR-H4', 'aw139', 'מסוק המנהלים (D‑267), שכר, אמבולנס'),
                        ('AIR-O2', 'h130', 'משטרה וחילוץ'), ('AIR-O1', 'aw139', 'משטרה, חילוץ ואמבולנס')):
        l = AL[pid]; r_, ring_ = pad_px(t); x0, y0, x1, y1 = l['rect']
        l.update(c=[(x0 + x1) / 2, (y0 + y1) / 2], r=r_, ring=ring_, heli=t, label=f"מנחת {pid[4:]} — {why} — {pad_txt(t)}")
    dec('D‑267', 'מנחת של 15 מ׳ למסוק המנהלים', 'H4 הוא מנחת המנהלים, לפי הטבלה של R-61 ל-AW139: מנחת מצויר 14 מ׳ וטבעת 25 מ׳ (הרוטור 13.8 מ׳)', 'מנחת מצויר 15 מ׳, כמו בנוסח של D‑267')
    hl = IL['IS-HELI']; r_, ring_ = pad_px('h130'); x0, y0, x1, y1 = hl['rect']
    hl.update(c=[(x0 + x1) / 2, (y0 + y1) / 2], r=r_, ring=ring_, heli='h130', label='מנחת האי — מסוק תיירות ופינוי — ' + pad_txt('h130'))
    # ============================================================ E3 — (the car park in pre); the sidewalk under the rail bridge is the avenue's own (arterial, 2.5 m)
    # ============================================================ F3 — the marina basin: 4 piers, 60 berths; the club, the rental, the fuel; the sea hotel (R-65)
    relot('F3-F1', [6240, 1880, 6520, 2030], 'חניון המרינה — 16 מקומות')
    relot('F3-01', [6245, 2200, 6520, 2470], 'מלון הים — 27.5 × 27 מ׳, 8 קומות, כ-120 חדרים', 'R-65 (ברירת מחדל לאישורך): המלון על הים — במרינה (F3), מול האגן והחוף; החניה בחניון המרינה.')
    add('F3', 'F3-CLUB', 'building', 'מועדון השייט ובית הקפה — 15 × 14 מ׳', 'תוכנית האב (F3): חוף המרינה — מועדון שייט; בית הקפה בקומת הקרקע.', rect=[6250, 2045, 6400, 2185], floors=2, access=('road', 'CL-F'), lbl=True)
    add('F3', 'F3-RENT', 'building', 'השכרת הסירות — 11 × 14 מ׳', 'תוכנית האב (F3): השכרת סירות, על הטיילת ומול המזח הראשון.', rect=[6410, 2045, 6520, 2185], floors=1, access=('path', 'F3-PROM'), lbl=True)
    add('F3', 'F3-FUELK', 'building', 'הדלק לסירות — הקיוסק', 'תוכנית האב (F3): דלק לסירות; המשאבה ברציף הדלק שליד הפתח.', rect=[6410, 2480, 6520, 2540], floors=1, access=('path', 'F3-PROM'), lbl=True)
    add('F3', 'F3-PROM', 'path', 'הטיילת של המרינה — 3 מ׳', 'תוכנית האב (F3): טיילת לאורך הרציף המערבי של האגן; מהמדרכה של דרך המרינה.', pts=[[6540, 1880], [6540, 2540]], hw=15, access=('road', 'CL-F'), lbl=True)
    piers = []
    # rows from the north quay: boats 5.5 m · pier 2 m · boats 5.5 m · fairway 6 m … the fourth pier with boats on its north side only; the mouth in the south-east
    for k, (y, two) in enumerate(((1945, True), (2135, True), (2325, True), (2515, False))):
        p = add('F3', f'F3-PIER{k + 1}', 'pier', f'מזח {k + 1} של המרינה — 2 × 42 מ׳, {18 if two else 6} מקומות', 'תוכנית האב (F3): אגן המרינה, 4 מזחים וכ-60 מקומות (BOAT‑05); סירות של עד 6 מ׳, מעבר של 6 מ׳ בין השורות.',
                rect=[6560, y - 10, 6980, y + 10], access=('path', 'F3-PROM'), berths=dict(sides=[-1, 1] if two else [-1], n=9 if two else 6, depth=55, slot=45), lbl=True)
        piers.append(p)
    add('F3', 'F3-FUELD', 'dock', 'רציף הדלק לסירות — בראש מזח 4', 'ליד פתח האגן (בדרום-מזרח) — הסירה מתדלקת בדרך החוצה; הקיוסק בשורש המזח.', rect=[6980, 2500, 7060, 2540], access=('pier', 'F3-PIER4'))
    # ============================================================ B2 — the 4 fishing stands, the mini golf, the playground; one café (the other lot was a double)
    relot('B2-01', [1271, 1135, 1871, 1457], 'מיני גולף ומגרש המשחקים', 'תוכנית האב (B2): מיני גולף ומגרש משחקים (קיים). היה מגרש שני של "בית קפה" — כפילות.')
    relot('B2-02', None, 'בית קפה האגם והקיוסק (קיימים)', 'תוכנית האב (B2): בית הקפה — הבית והקיוסק של היום על החוף.')
    add('B2', 'B2-GOLF', 'court', 'מיני גולף — 18 גומות, 26 × 29 מ׳', 'תוכנית האב (B2).', rect=[1340, 1150, 1600, 1440], parent='B2-01', access=('lot', 'B2-01'), lbl=True)
    add('B2', 'B2-PLAY', 'court', 'מגרש המשחקים — 24 × 20 מ׳ (קיים)', 'תוכנית האב (B2): מגרש המשחקים של היום.', rect=[1620, 1150, 1860, 1350], parent='B2-01', access=('lot', 'B2-01'), lbl=True)
    add('B2', 'B2-LAKEPATH', 'path', 'שביל החוף של האגם — 2 מ׳', 'מהמדרכה של שדרת המערב לאורך החוף הדרומי, אל עמדות הדיג ובית הקפה.', pts=[[1259, 1122], [2100, 1122]], hw=10, access=('road', 'CL-W'))
    LK = ctx['LAKE_TODAY']
    for k, x in enumerate((1600, 1760, 1920, 2080)):
        sy = LK['cy'] + LK['ry'] * math.sqrt(max(0, 1 - ((x - LK['cx']) / LK['rx']) ** 2))
        add('B2', f'B2-FS{k + 1}', 'fishstand', f'עמדת דיג {k + 1}', 'תוכנית האב (B2): 4 עמדות דיג על החוף הדרומי של האגם; דק של 3 מ׳ מעל המים.', rect=[x - 15, round(sy - 14), x + 15, 1114], access=('path', 'B2-LAKEPATH'))
    # ============================================================ C2 — the mall's car park and the row of shops
    relot('C2-01', None, 'הקניון, החניון שלו ושורת החנויות', 'תוכנית האב (C2): קניון, סופר, חנות דיג; חניון.')
    add('C2', 'C2-MALL-P', 'parking', 'חניון הקניון — 27 מקומות', 'תוכנית האב (C2): חניון. נכנסים מדרך השדות, בכניסה של הקניון.', rect=[2660, 860, 3020, 1050], stalls=27, parent='C2-01', access=('lot', 'C2-01'), lbl=True)
    add('C2', 'C2-MALL', 'building', 'הקניון — 36 × 13 מ׳, 2 קומות', 'תוכנית האב (C2).', rect=[2660, 1060, 3020, 1190], floors=2, parent='C2-01', access=('lot', 'C2-MALL-P'), lbl=True)
    add('C2', 'C2-SHOPS', 'building', 'שורת החנויות — חנות הדיג, בית הקפה והמסעדה', 'תוכנית האב (C2): חנות דיג (קיים); בית הקפה והמסעדה בשורה של הקניון (D‑309).', rect=[2660, 1196, 3020, 1260], floors=1, parent='C2-01',
        units=['חנות הדיג', 'בית הקפה', 'המסעדה'], access=('lot', 'C2-MALL'), lbl=True)
    # ============================================================ C6 — the four container blocks; the oil terminal (a reserved lot, the roads untouched)
    relot('C6-01', [3176, 4450, 3330, 4700], 'משרד שילוח')
    for d in ctx['LOT_DW'] + ctx['SITE_ROADS']:   # the driveway of D6-02 stood west of its lot (on the old C6-01) — back to its own frontage, 21 m from J385_49
        if d['id'] == 'DW-D6-02':
            if d.get('at'): d['at'] = [3650.0, d['at'][1]]; d['to_junction_m'] = round(math.hypot(3850 - 3650, 4900 - d['at'][1]) / 10, 1)
            for key in ('pts', 'draw'):
                if d.get(key): d[key] = [[3650.0, q[1]] for q in d[key]]
    relot('C6-02', None, 'מסוף הנפט — מגרש שמור (שלב הלוגיסטיקה, 14)', 'תוכנית האב (C6): מסוף הנפט — מגרש שמור. בקצה רחוב החצר, ליד מסילת בית הזיקוק (D‑177); הסדנה של הנמל — ב-D6 וב-E6.')
    add('C6', 'C6-CY', 'yard', 'חצר המכולות — 4 בלוקים', 'תוכנית האב (C6): מסוף המכולות, 4 בלוקים, מסילות; מול דרך הרציף.', rect=[3345, 4450, 3600, 4830], access=('road', 'PT-Q'), lbl=True)
    for k, r_ in enumerate(([3355, 4465, 3465, 4630], [3480, 4465, 3590, 4630], [3355, 4650, 3465, 4815], [3480, 4650, 3590, 4815])):
        add('C6', f'C6-CB{k + 1}', 'cblock', f'בלוק מכולות {k + 1} — 11 × 16.5 מ׳', 'ערמות של עד 3 מכולות, מעבר של 2 מ׳ בין הבלוקים.', rect=r_, parent='C6-CY', access=('lot', 'C6-CY'))
    # ============================================================ D2 — the hotel on a larger lot (R-65); the hi-tech campus in three buildings (D-141)
    relot('D2-02', [4300, 1000, 4540, 1440], 'המלון העסקי — מגרש 24 × 44 מ׳: 120 חדרים, גן בריכה וחניון אורחים', 'R-65 (ברירת מחדל לאישורך): המגרש גדל מ-22 × 17 מ׳; כיכר המטה קטנה צפונה.')
    relot('D2-F2', [4300, 850, 4600, 990])
    add('D2', 'D2-HOTEL', 'building', 'המלון — 22 × 18 מ׳, 8 קומות', 'R-65.', rect=[4310, 1010, 4530, 1190], floors=8, parent='D2-02', access=('lot', 'D2-HOTEL-POOL'), lbl=True)
    add('D2', 'D2-HOTEL-POOL', 'park', 'גן הבריכה של המלון', 'R-65.', rect=[4310, 1200, 4530, 1300], parent='D2-02', access=('lot', 'D2-HOTEL'))
    add('D2', 'D2-HOTEL-P', 'parking', 'חניון האורחים — 10 מקומות', 'R-65; מהכניסה של המלון בדרך המטען.', rect=[4310, 1310, 4530, 1430], stalls=10, parent='D2-02', access=('road', 'CL-AC'), lbl=True)
    for k, (r_, fl_) in enumerate((([3790, 1000, 3990, 1150], 6), ([4080, 1000, 4280, 1130], 4), ([3790, 1280, 4060, 1420], 3))):
        add('D2', f'D2-HT{k + 1}', 'building', f'מבנה {k + 1} של קמפוס ההייטק — {fl_} קומות', 'D‑141: 2–3 מבנים בגבהים שונים וחצר פנימית.', rect=r_, floors=fl_, parent='D2-F1', access=('lot', 'D2-F1'))
    add('D2', 'D2-HT-YARD', 'park', 'החצר הפנימית של הקמפוס', 'D‑141.', rect=[3790, 1160, 4280, 1270], parent='D2-F1', access=('lot', 'D2-F1'))
    if 'IS-HOSTEL' in IL: IL['IS-HOSTEL']['label'] = 'מלון האי — אכסניית ההר'
    # ============================================================ B6 — the second pier and the fishing stands; B7 — the fishing bay (D-158)
    add('B6', 'B6-PIER2', 'pier', 'המזח השני — מזח הדיג המערבי, 6 × 15 מ׳', 'תוכנית האב (B6): 2 מזחים ועמדות דיג; ליד קפה החוף.', rect=[1330, 5000, 1390, 5150], access=('lot', 'B6-BEACH'), lbl=True)
    for pid, (x0, x1) in (('B6-PIER', (1610, 1670)), ('B6-PIER2', (1330, 1390))):
        for k, (sd, y) in enumerate(((-1, 5060), (-1, 5110), (1, 5060), (1, 5110))):
            add('B6', f'{pid}-FS{k + 1}', 'fishstand', 'עמדת דיג', 'תוכנית האב (B6): עמדות דיג בצדי המזחים.', rect=[x0 - 25, y, x0, y + 25] if sd < 0 else [x1, y, x1 + 25, y + 25], parent=pid, access=('pier', pid))
    for k, (x0, y0) in enumerate(((1880, 5000), (2100, 5000))):
        add('B7', f'B7-PIER{k + 1}', 'pier', f'מזח {k + 1} של מפרץ הדיג — 3 × 42 מ׳', 'D‑158: מפרץ הדיג עם החוף הדרומי — מזחים וסירות דייג; 9 מ׳ ויותר ממסלול המעבורת.', rect=[x0, y0, x0 + 30, 5420], access=('lot', 'B6-BEACH'), lbl=True)
    for k, r_ in enumerate(([1915, 5100, 1950, 5210], [1915, 5240, 1950, 5350], [1840, 5150, 1875, 5260], [2060, 5120, 2095, 5230], [2060, 5260, 2095, 5370], [2135, 5160, 2170, 5270])):
        add('B7', f'B7-BOAT{k + 1}', 'boat', f'סירת דייג {k + 1} — 11 × 3.5 מ׳', 'D‑158: סירות הדייג קשורות למזחים.', rect=r_, access=('pier', 'B7-PIER1' if r_[0] < 2000 else 'B7-PIER2'))
    # ============================================================ E7 — the tugs, in the gap of C6 / D6
    add('D7', 'TUG-PIER', 'tugpier', 'מזח הגוררות — בפער C6 / D6, ‏4 × 30 מ׳', 'תוכנית האב (E7): הגוררות עוברות לפער C6 / D6; המזח יוצא מהרציף, בין מקומות העגינה של C ושל D.', rect=[3580, 5200, 3620, 5500], access=('quay', 'PT-Q'), lbl=True)
    for k, r_ in enumerate(([3485, 5215, 3570, 5465], [3630, 5215, 3715, 5465], [3725, 5215, 3810, 5465])):
        add('D7', f'TUG-{k + 1}', 'boat', f'גוררת {k + 1} — 25 × 8.5 מ׳', 'הגוררות של הנמל.' + (' רתומה לגוררת 2.' if k == 2 else ''), rect=r_, access=('pier', 'TUG-PIER' if k < 2 else 'TUG-2'), tug=True)
    add('C6', 'C6-LIGHT', 'tower', 'מגדלור החוף — בפינה המערבית של הרציף', 'D‑156: מגדלור החוף; מסמן את הכניסה לנמל מהמערב, ליד מפרץ הדיג.', c=[2470, 5160], r=35, access=('quay', 'PT-Q'), lbl=True)
    # ============================================================ G7 — the gas rig with its helideck (D-156) and the supply boat's landing
    r_, ring_ = pad_px('aw139')
    add('G7', 'G7-RIG', 'rig', 'אסדת הגז — 23 × 18 מ׳ (D‑156)', 'תוכנית האב (G7): אסדת גז בים העמוק עם מנחת ומסוקי עובדים; המיקום הסופי בחלק ד — הרחק מהגשר ומהמסילה המזרחית.', rect=[7950, 5420, 8180, 5600], access=('pier', 'G7-RIG-DOCK'), lbl=True)
    add('G7', 'G7-RIG-HELI', 'pad', 'מנחת האסדה — מסוקי העובדים, ' + pad_txt('aw139'), 'D‑156: מסוקי העובדים (AW139).', c=[8110, 5490], r=r_, ring=ring_, heli='aw139', parent='G7-RIG', water_ok=True, access=('lot', 'G7-RIG'))
    add('G7', 'G7-RIG-DOCK', 'dock', 'רציף סירת האספקה של האסדה', 'הסירה מגיעה מנמל E6.', rect=[7915, 5480, 7950, 5560], access=('lot', 'G7-RIG'))
    # ============================================================ the sea: the lanes and the buoys (F5, G5, F7, C8, D8, E8, C9, D9)
    LANES = [('L1', 'נתיב האוניות במזרח (F5, ‏G5)', [[8380, 3820], [6900, 3820], [6900, 4950]], 200, 'ship', 'F5'),
             ('L2', 'נתיב האוניות מדרום אל הנמל (C9, ‏D9 → C8 / D8 → C7 / D7)', [[3600, 7740], [3600, 5720]], 250, 'ship', 'D8'),
             ('L3', 'נתיב ספינות המטען — מזרח-מערב (C8, ‏D8, ‏E8)', [[2450, 6450], [5700, 6450], [5700, 5800]], 200, 'ship', 'D8'),
             ('L4', 'נתיב השיט אל האי ואל המרינה (F7)', [[6880, 2620], [6880, 4950], [6550, 5420], [6650, 5640], [6400, 6150], [6060, 6950], [6060, 7400]], 70, 'small', 'F7')]
    for lid, he, pts, hw, kind, z in LANES:
        add(z, 'LANE-' + lid, 'lane', he, 'תוכנית האב: ' + he + '; מצופים אדומים משמאל ירוקים מימין בכניסה (בשיט קטן — צהובים).', pts=pts, hw=hw, lane=kind, lbl=True)
    for lid, he, pts, hw, kind, z in LANES:
        step = {'L2': 400}.get(lid, 600 if kind == 'ship' else 450); L = plen(pts); d = step / 2
        while d < L:
            acc = 0
            for k in range(len(pts) - 1):
                (ax, ay), (bx, by) = pts[k], pts[k + 1]; l = math.hypot(bx - ax, by - ay)
                if acc + l >= d:
                    t = (d - acc) / l; x, y = ax + (bx - ax) * t, ay + (by - ay) * t; ux, uy = (bx - ax) / l, (by - ay) / l; break
                acc += l
            for sd, col in ((-1, 'red'), (1, 'green')):
                bx_, by_ = x - uy * hw * sd, y + ux * hw * sd
                if not ctx['is_sea'](bx_, by_) or any(dpoly(bx_, by_, rp) < 140 for rp in ctx['RAILP']) or dpoly(bx_, by_, ctx['FERRY']) < 120 or dpoly(bx_, by_, ctx['BRIDGE']) < 160: continue
                if any(gap((bx_ - 1, by_ - 1, bx_ + 1, by_ + 1), box_of(o)) < 60 for o in I if o['kind'] in ('pier', 'boat', 'rig', 'tugpier', 'dock')): continue
                z_ = ctx['zone_of'](bx_, by_)
                add(z_, f'BUOY-{lid}-{int(d)}-{"L" if sd < 0 else "R"}', 'buoy', ('מצוף ' + ('אדום' if col == 'red' else 'ירוק')) if kind == 'ship' else 'מצוף צהוב', he, c=[round(bx_), round(by_)], r=14 if kind == 'ship' else 10,
                    col=(col if kind == 'ship' else 'yellow'), lane=lid)
            d += step
    for k, (x, y) in enumerate(((6495, 5440), (6610, 5420), (6585, 5610), (6700, 5600))):
        if any(o['kind'] == 'buoy' and math.hypot(o['c'][0] - x, o['c'][1] - y) < 80 for o in I): continue
        add('F7', f'BUOY-L4-F7-{k + 1}', 'buoy', 'מצוף צהוב', 'נתיב השיט אל האי ואל המרינה (F7) — בין גשר הכביש לגשר המסילה', c=[x, y], r=10, col='yellow', lane='L4')
    dec('F5 / G5', 'נתיב האוניות במזרח: תוכנית האב — "אל הנמל"; חלק ד — הנתיבים לנמל מדרום, ממערב לגשר', 'הנתיב מסומן ב-F5 ו-G5 עד המסילה המזרחית; האוניות לנמל באות מדרום (C9 / D9)', 'הנתיב ממשיך מתחת לגשרי המסילה ולגשר האי אל E7')
    # ============================================================ F9 — the paths on the west slope; H9 — the service road to the lighthouse and the pad
    for id_, pts, he, to in (('IS-TRAIL-1', [[6962, 7298], [7134, 7298]], 'שביל המדרון המערבי — מהנמל אל הכפר', 'IS-VILLAGE'),
                             ('IS-TRAIL-2', [[6955, 7560], [7160, 7560], [7160, 7480], [7200, 7480]], 'שביל המדרון המערבי — מהנמל אל יער הפסגה', 'IS-SUMMIT')):
        add('F9', id_, 'path', he, 'תוכנית האב (F9): המדרון המערבי של ההר — שבילים; מהמדרכה של דרך הנמל, 2 מ׳.', pts=pts, hw=10, access=('island', 'IS-HARBOR'), to=to, lbl=True)
    for r in ISLF['roads']:
        if r['id'] == 'IS-SVC': r['label'] = 'דרך השירות למגדלור ולמנחת — מסביב לסוף המסילה (נבדקה)'; r['pts'] = [[8890, 7690], [9340, 7690], [9340, 7050]]
    ISLF['roads'].append(dict(id='IS-SVC-HELI', label='השלוחה אל מנחת האי', cls='service', pts=[[9340, 7100], [9215, 7100]]))
    dec('שאלה 1 במפה', 'הגישה למגדלור ולמנחת באי', 'דרך השירות סביב סוף המסילה, עם שלוחה למנחת — נבדקה: לא חוצה מסילה ולא נכנסת לים', 'שביל וגשר הולכי רגל מרחבת התחנה, בלי כביש')
    return I

# ---------------------------------------------------------------- the checks of round 7 (one for every new kind)
def checks(ctx, I):
    out = []
    def C(name, bad, ok_txt): out.append((name, not bad, ok_txt if not bad else ok_txt + ' בעיות: ' + '; '.join(bad[:12])))
    is_sea, in_lake = ctx['is_sea'], ctx['in_lake']
    IB = {i['id']: i for i in I}
    LOTR = [(l['id'], tuple(l['rect']), l.get('use')) for l in ctx['LOTS']]
    SITR = [(s['id'], box_of(s) if s['kind'] in ('pad',) else tuple(s['rect']), s['kind']) for s in ctx['SITES'] if s['kind'] not in ('site', 'path', 'house') and s.get('rect') or s['kind'] == 'pad']
    AIRR = [(l['id'], tuple(l['rect']), l['kind']) for l in ctx['AIRF']['lots']]
    ISLR = [(l['id'], tuple(l['rect']), l['kind']) for l in ctx['ISLF']['lots']]
    ROADB = [(s['road'], b) for s in ctx['SEG'] if s['kind'] != 'bridge' for b in bands(s['pts'], ctx['hw'](s)) if not b[4:]]
    DIAG = [(s['road'], s['pts'][k], s['pts'][k + 1], ctx['hw'](s)) for s in ctx['SEG'] if s['kind'] != 'bridge' for k in range(len(s['pts']) - 1)
            if abs(s['pts'][k][0] - s['pts'][k + 1][0]) > 1 and abs(s['pts'][k][1] - s['pts'][k + 1][1]) > 1]
    def rect_seg(b, p, q):   # the distance from a rectangle to a segment
        best = 1e9
        for t in range(41):
            x, y = p[0] + (q[0] - p[0]) * t / 40, p[1] + (q[1] - p[1]) * t / 40
            best = min(best, math.hypot(max(b[0] - x, 0, x - b[2]), max(b[1] - y, 0, y - b[3])))
        return best
    SRB = [(r['id'], b) for r in ctx['SITE_ROADS'] for b in bands(r['pts'], r['hw'])]
    AIRDB = [(r['id'], b) for r in ctx['AIRF']['roads'] for b in bands(r['pts'], ctx['airhw'](r))]
    SVCB = [(s['id'], tuple(s['rect'])) for s in ctx['AIRF']['service']]
    RAILB = [(r['id'], b) for r in ctx['RAILS'] for b in bands(r['pts'], 25)]
    GREEN = ('forest', 'fields', 'park', 'coast')
    DWAY = {r['id'] for r in ctx['SITE_ROADS'] if r['kind'] == 'driveway'}
    # 1. the land items of the city (lots, buildings, yards, car parks, paths, tracks): on land, clear of roads, rails and lots
    bad = []; n = 0
    for i in I:
        if i['kind'] in WATER or i['kind'] in MARK or i.get('air') or i['kind'] in ('pad', 'resa', 'loc', 'pocket', 'stair'): continue
        n += 1; F = foot(i)
        for b in F:
            for x, y in ((b[0] + 3, b[1] + 3), (b[2] - 3, b[3] - 3), ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)):
                if is_sea(x, y) or in_lake(x, y): bad.append(f"{i['id']} במים"); break
            for rid, rb in ROADB + SRB:
                if rid in DWAY and (i['kind'] in ('svc', 'path') or rid == 'DW-' + str(i.get('parent'))): continue
                if ov(b, rb, 1) and not (i['kind'] in ('svc', 'path') and rid in (i.get('access') or ('', ''))[1:]): bad.append(f"{i['id']}×{rid}")
            for rid, rb in RAILB:
                if ov(b, rb, 1): bad.append(f"{i['id']}×מסילה {rid}")
            for rid, p_, q_, h_ in DIAG:
                if rect_seg(b, p_, q_) < h_ - 1: bad.append(f"{i['id']}×{rid}")
            for lid, lb, use in LOTR:
                if lid == i.get('parent') or (i['kind'] in ('path', 'svc') and use in GREEN): continue
                if ov(b, lb, 1): bad.append(f"{i['id']}×{lid}")
            for sid, sb, sk in SITR:
                if sid == i.get('parent') or sid == i['id']: continue
                if ov(b, sb, 1): bad.append(f"{i['id']}×{sid}")
            for lid, lb, lk in ISLR:
                if lk not in ('park',) and ov(b, lb, 1): bad.append(f"{i['id']}×{lid}")
        for j in I:
            if j is i or j['kind'] in WATER or j['kind'] in MARK or j.get('air') or j.get('parent') == i['id'] or i.get('parent') == j['id'] or j['kind'] in ('pad', 'stair'): continue
            if any(ov(b, c, 1) for b in F for c in foot(j)) and not (i['kind'] in ('path', 'svc') and j['kind'] in ('path', 'svc')): bad.append(f"{i['id']}×{j['id']}")
    C('סבב 7 — הפריטים החדשים ביבשה (מגרשים, מבנים, חניונים, שבילים ודרכי שירות): על היבשה, בלי חפיפה לכביש, לדרך פנימית, למסילה, למגרש או לפריט אחר', sorted(set(bad)),
      f"{n} פריטים; שביל ודרך עפר יכולים לעבור בתוך יער, שדה, פארק או חוף (כמו בתוכנית האב: \"אורות הגישה משתלבים בשדה\", \"שביל הליכה ביער\").")
    # 2. the water: piers, docks, stands, boats and the rig — in the sea or the lake, a pier touches the land
    bad = []; nw = 0
    for i in I:
        if i['kind'] not in ('pier', 'boat', 'dock', 'fishstand', 'tugpier', 'rig'): continue
        nw += 1; x0, y0, x1, y1 = i['rect']
        if i['kind'] in ('boat', 'rig'):
            if not all(is_sea(x, y) for x, y in ((x0 + 2, y0 + 2), (x1 - 2, y1 - 2), (x0 + 2, y1 - 2), (x1 - 2, y0 + 2))): bad.append(f"{i['id']} לא במים")
        else:
            wet = [is_sea(x, y) or in_lake(x, y) for x, y in ((x0 + 3, y0 + 3), (x1 - 3, y1 - 3), (x0 + 3, y1 - 3), (x1 - 3, y0 + 3), ((x0 + x1) / 2, (y0 + y1) / 2))]
            if not any(wet): bad.append(f"{i['id']} לא במים")
        for j in I:
            if j is i or j['kind'] not in ('pier', 'boat', 'dock', 'tugpier', 'rig') or j.get('parent') == i['id'] or i.get('parent') == j['id']: continue
            if ov(tuple(i['rect']), tuple(j['rect']), 1): bad.append(f"{i['id']}×{j['id']}")
        if i['kind'] != 'boat':
            for rid, rb in RAILB:
                if ov(tuple(i['rect']), rb, 1): bad.append(f"{i['id']}×מסילה {rid}")
        if i['kind'] in ('pier', 'tugpier', 'dock') and i.get('berths') is None and i['kind'] != 'dock':
            pass
    ferry = [b for b in bands(ctx['FERRY'], 65)]
    for i in I:
        if i['kind'] in ('pier', 'boat', 'tugpier', 'rig') and any(dseg((i['rect'][0] + i['rect'][2]) / 2, y, *ctx['FERRY'][k], *ctx['FERRY'][k + 1]) < 65 + 20 for y in (i['rect'][1], i['rect'][3]) for k in range(len(ctx['FERRY']) - 1)):
            bad.append(f"{i['id']} על מסלול המעבורת")
    nb = sum(sum(len(p['berths']['sides']) * p['berths']['n'] for _ in [0]) for p in I if p.get('berths'))
    C('סבב 7 — המזחים, הסירות והאסדה: במים, מזח נוגע ביבשה, בלי חפיפה ביניהם, למסילה או למסלול המעבורת (חצי גוף של 6.5 מ׳ ועוד 2 מ׳)', sorted(set(bad)),
      f"{nw} פריטים במים; אגן המרינה — 4 מזחים ו-{nb} מקומות; מפרץ הדיג — 2 מזחים ו-6 סירות; מזח הגוררות — 3 גוררות; המזח השני של B6 ו-8 עמדות דיג; 4 עמדות דיג באגם.")
    # 3. the access of every new item: its road, path, pier or lot really touches it
    def anchors(a):
        kind, ref = a
        if kind == 'road': return [b for rid, b in ROADB + SRB + AIRDB if rid == ref]
        if kind == 'svc': return [b for j in I if j['id'] == ref for b in foot(j)]
        if kind in ('path', 'pier'): return [b for j in I + ctx['SITES'] if j['id'] == ref for b in (foot(j) if j.get('pts') or j.get('kind') == 'path' and isinstance(j['rect'][0], (list, tuple)) else [tuple(j['rect'])])]
        if kind == 'lot': return [b for lid, b, _ in LOTR + AIRR + ISLR if lid == ref] + [b for sid, b, _ in SITR if sid == ref] + [b for j in I if j['id'] == ref for b in foot(j)]
        if kind == 'air':
            if ref == 'AIRSIDE': return [b for _, b in SVCB] + [b for lid, b, k in AIRR if k == 'apron']
            return [b for sid, b in SVCB if sid == ref] + [b for rid, b in AIRDB if rid == ref] + [b for j in I if j['id'] == ref for b in foot(j)]
        if kind == 'island': return [b for r in ctx['ISLF']['roads'] if r['id'] == ref for b in bands(r['pts'], 54 if r['cls'] == 'local' else 19.5)]
        if kind == 'quay': return [(2510, 4960, 6000, 5200)]
        return []
    bad = []; na = 0; via = {}
    for i in I:
        if not i.get('access'): continue
        na += 1; A = anchors(i['access'])
        if not A: bad.append(f"{i['id']}: אין {i['access'][1]}"); continue
        g = min(gap(b, a) for b in foot(i) for a in A)
        if g > 20: bad.append(f"{i['id']} — {g / 10:.1f} מ׳ מ-{i['access'][1]}")
        i['access_txt'] = {'AIRSIDE': 'שבילי השירות והרחבות של הצד האווירי'}.get(i['access'][1], i['access'][1]); via[i['access'][0]] = via.get(i['access'][0], 0) + 1
    C('סבב 7 — הגישה: לכל פריט חדש דרך, שביל, מזח או מגרש שנוגע בו באמת (עד 2 מ׳)', bad,
      f"{na} פריטים: " + ', '.join(f"{ {'road': 'מכביש', 'svc': 'מדרך שירות חדשה', 'path': 'משביל', 'pier': 'ממזח', 'lot': 'דרך המגרש שלידו', 'air': 'מהשבילים והרחבות של הצד האווירי', 'island': 'מכביש האי', 'quay': 'מהרציף'}.get(k, k)} {v}" for k, v in sorted(via.items(), key=lambda kv: -kv[1])) + '.')
    # 4. the airport (stage 8): the new lots of E2 and the items of the airside — clear of each other, of the paved areas they must not cover, inside / outside the fence
    bad = []; nair = 0
    from_fence = ctx['pip']
    for l in ctx['AIRF']['lots']:
        if not l.get('r7'): continue
        nair += 1
        if from_fence(*((l['rect'][0] + l['rect'][2]) / 2, (l['rect'][1] + l['rect'][3]) / 2), ctx['AIRF']['fence']): bad.append(f"{l['id']} בתוך הגדר")
        for m in ctx['AIRF']['lots']:
            if m is l or m['kind'] in ('apron',): continue
            if ov(tuple(l['rect']), tuple(m['rect']), 1): bad.append(f"{l['id']}×{m['id']}")
        for rid, b in AIRDB:
            if ov(tuple(l['rect']), b, 1) and rid not in l.get('road_ok', []): bad.append(f"{l['id']}×{rid}")
        if l.get('stalls') and l['stalls'] * 25 > (l['rect'][2] - l['rect'][0]) * (l['rect'][3] - l['rect'][1]) / 100 - sum((j['rect'][2] - j['rect'][0]) * (j['rect'][3] - j['rect'][1]) / 100 for j in I if j.get('parent') == l['id']):
            bad.append(f"{l['id']}: {l['stalls']} מקומות לא נכנסים")
    for i in I:
        if not i.get('air') or i['kind'] in ('xmark', 'corner', 'signal', 'stopline', 'tower', 'svc', 'footbridge', 'unit', 'runup'): continue
        nair += 1; b = box_of(i)
        inside = from_fence((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, ctx['AIRF']['fence'])
        if i['kind'] in ('pocket', 'blast', 'gate') and not inside and i['kind'] != 'gate': bad.append(f"{i['id']} מחוץ לגדר")
        if i['kind'] in ('stair',) and inside: bad.append(f"{i['id']} בתוך הגדר")
        for sid, sb in SVCB:
            if i['kind'] == 'pocket' and ov(b, sb, 1): bad.append(f"{i['id']}×{sid}")
        for m in ctx['AIRF']['lots']:
            if i['kind'] == 'pocket' and m['kind'] in ('building', 'pad', 'taxi', 'runway', 'parking') and ov(b, tuple(m['rect']), 1): bad.append(f"{i['id']}×{m['id']}")
            if i['kind'] == 'pocket' and m['kind'] == 'pad' and m.get('c') and gap(b, (m['c'][0], m['c'][1], m['c'][0], m['c'][1])) < m['ring']: bad.append(f"{i['id']} בטבעת של {m['id']}")
    for i in I:
        if i['kind'] in ('resa', 'loc'):
            nair += 1
            for m in ctx['AIRF']['lots']:
                if m['kind'] in ('taxi', 'building', 'stand') and ov(tuple(i['rect']), tuple(m['rect']), 1): bad.append(f"{i['id']}×{m['id']}")
            for sid, sb in SVCB:
                if ov(tuple(i['rect']), sb, 1): bad.append(f"{i['id']}×{sid}")
    nx = sum(1 for i in I if i['kind'] == 'xmark')
    C('סבב 7 — השדה (שלב 8): המגרשים החדשים של צד היבשה מחוץ לגדר ובלי חפיפה; כיסי הציוד, מחסום ההדף, שטח הבטיחות והמשדר — בתוך הגדר, לא על דרך שירות, מסלול, מבנה או טבעת של מנחת', sorted(set(bad)),
      f"{nair} פריטים. בצד היבשה (E2): P‑WEST ‏(22), ‏P‑RENT ‏(14) ומלון השדה והצוותים; גשר AIR‑1 עם שתי נחיתות. בצד האווירי: {sum(1 for i in I if i['kind'] == 'pocket')} כיסי ציוד, {nx} מעברים מסומנים (המטוס קודם), "
      "הרצת המנועים ב-R3 עם מחסום הדף, שטח הבטיחות והמשדר ב-H0, דרך ההיקף לאורך הגדר הצפונית, השער של העובדים ב-x 7860, המגדל על הגג, מפרץ המילוי, 4 הפינות לסמי והצומת AIR‑K.")
    # 5. the approach lights and the perimeter road: on the runway's axis, outside the paved areas, the track clear of the lots
    bad = []
    for i in I:
        if i['kind'] != 'lights': continue
        if any(abs(y + 690) > 1 for x, y in i['pts']): bad.append(f"{i['id']} לא על הציר")
        for x, y in i['pts']:
            for m in ctx['AIRF']['lots']:
                if m['kind'] in ('runway', 'taxi', 'building', 'stand') and m['rect'][0] < x < m['rect'][2] and m['rect'][1] < y < m['rect'][3]: bad.append(f"{i['id']} ({x}) על {m['id']}")
            for lid, lb, use in LOTR:
                if lb[0] < x < lb[2] and lb[1] < y < lb[3] and use not in GREEN: bad.append(f"{i['id']} ({x}) על {lid}")
    C('סבב 7 — אורות הגישה (09 ו-27): על ציר המסלול (y ‎−690), לא על משטח, מבנה או מגרש שאינו שדה', bad,
      f"מסלול 09: {len(IB['AL-09']['pts'])} נקודות מ-x 3250 עד x 4950 ושני פסי רוחב, עם דרך תחזוקה; מסלול 27: {len(IB['AL-27']['pts'])} נקודות עד הגדר.")
    # 6. the pads — one table (R-61): every pad in the map has a helicopter; the pad drawn = its rotor; the ring = 1.5 × its length; nothing built in the ring
    bad = []; rows = []
    PADS = [(s['id'], s['zone'], s.get('heli'), s['c'], s['r'], s['safety'], s.get('parent'), s.get('label')) for s in ctx['SITES'] if s['kind'] == 'pad'] + \
           [(l['id'], l['zone'], l.get('heli'), l.get('c'), l.get('r'), l.get('ring'), None, l['label']) for l in ctx['AIRF']['lots'] + ctx['ISLF']['lots'] if l['kind'] == 'pad'] + \
           [(i['id'], i['zone'], i.get('heli'), i['c'], i['r'], i['ring'], i.get('parent'), i['label']) for i in I if i['kind'] == 'pad']
    BLD = [(s['id'], tuple(s['rect'])) for s in ctx['SITES'] if s['kind'] in ('building', 'house')] + [(l['id'], tuple(l['rect'])) for l in ctx['AIRF']['lots'] + ctx['ISLF']['lots'] if l['kind'] == 'building'] + \
          [(i['id'], tuple(i['rect'])) for i in I if i['kind'] == 'building']
    def dc(c, r): return math.hypot(max(r[0] - c[0], 0, c[0] - r[2]), max(r[1] - c[1], 0, c[1] - r[3]))
    for pid, z, t, c, r, ring, par, lab in PADS:
        if t not in HELI: bad.append(f"{pid}: אין מסוק"); continue
        pr, rr = pad_px(t)
        if abs(r - pr) > .5 or abs(ring - rr) > .5: bad.append(f"{pid}: {r / 5:g} / {ring / 5:g} מ׳ במקום {HELI[t]['pad']} / {HELI[t]['ring']}")
        for bid, b in BLD:
            if bid == par: continue
            if dc(c, b) < ring - .5: bad.append(f"{pid}: הטבעת על {bid}")
        for rid, b in ROADB:
            if dc(c, b) < ring - .5: bad.append(f"{pid}: הטבעת על {rid}")
        rows.append(dict(id=pid, zone=z, heli=t, he=HELI[t]['he'], pad=HELI[t]['pad'], ring=HELI[t]['ring'], roof=bool(par), label=lab))
    ctx['PAD_ROWS'] = rows
    cnt = {}
    for r in rows: cnt[r['he']] = cnt.get(r['he'], 0) + 1
    C('R-61 — טבלת המנחתים: לכל מנחת במפה מסוק; המנחת המצויר בקוטר הרוטור (קל 10 מ׳, ‏H130 ‏11 מ׳, ‏AW139 ‏14 מ׳), הטבעת פי 1.5 מאורך המסוק (17.5, ‏19, ‏25 מ׳), ובטבעת אין מבנה או כביש', bad,
      f"{len(rows)} מנחתים: " + ', '.join(f"{k} — {v}" for k, v in cnt.items()) + f"; {sum(1 for r in rows if r['roof'])} מהם על גג (A4 ‏×2, ‏A5) או על האסדה. על כל מנחת מסוק בגודל אמיתי. " + DEFAULT + '.')
    # 7. the sea: the buoys in the water, clear of the ferry, the bridges and the rails; every zone of the lanes has its buoys
    bad = []; per = {}
    for i in I:
        if i['kind'] != 'buoy': continue
        if not is_sea(*i['c']): bad.append(f"{i['id']} לא במים")
        per[i['zone']] = per.get(i['zone'], 0) + 1
    need = ['F5', 'G5', 'F7', 'C8', 'D8', 'E8', 'C9', 'D9']
    for z in need:
        if per.get(z, 0) < 2: bad.append(f"ב-{z} רק {per.get(z, 0)} מצופים")
    for i in I:
        if i['kind'] != 'lane': continue
        for k in range(len(i['pts']) - 1):
            (ax, ay), (bx, by) = i['pts'][k], i['pts'][k + 1]; m = max(1, int(math.hypot(bx - ax, by - ay) // 50))
            if any(not is_sea(ax + (bx - ax) * t / m, ay + (by - ay) * t / m) for t in range(m + 1)): bad.append(f"{i['id']} עובר ביבשה"); break
    C('סבב 7 — הים: נתיבי האוניות והשיט במים בלבד, המצופים במים, לא על מסלול המעבורת, הגשרים או המסילות; בכל אזור של נתיב לפחות 2 מצופים', bad,
      f"{sum(1 for i in I if i['kind'] == 'lane')} נתיבים, {sum(per.values())} מצופים: " + ', '.join(f"{z} — {per.get(z, 0)}" for z in need) + '.')
    # 8. A0 — the contour lines: closed, nested, inside the zone after the clip; the hillshade
    cts = sorted([i for i in I if i['kind'] == 'contour'], key=lambda i: i['level'])
    bad = []
    for a, b in zip(cts[::-1], cts[::-1][1:]):   # a — the inner line, b — the next one out: every point of a inside b
        if not all(((x - 600) / (110 + 85 * (6 - b['level']))) ** 2 + ((y + 560) / (170 + 55 * (6 - b['level']))) ** 2 < 1 for x, y in a['pts']): bad.append(f"{a['id']} חוצה את {b['id']}")
    C('D‑188 — קווי הגובה וההצללה ב-A0: קווים סגורים זה בתוך זה, בלי חיתוך, בתוך האזור (נחתכים בקצה העולם)', bad,
      f"{len(cts)} קווי גובה סביב הפסגה (600, ‎−560), לאורך דרך הרכס; הצללה בצד הדרום-מזרחי של כל קו.")
    # 9. the island: the service road to the lighthouse and the pad — on land, not over a track, it reaches both
    bad = []
    sv = next(r for r in ctx['ISLF']['roads'] if r['id'] == 'IS-SVC'); sp = next(r for r in ctx['ISLF']['roads'] if r['id'] == 'IS-SVC-HELI')
    dmin = min(dpoly(x, y, rp) for r in (sv, sp) for k in range(len(r['pts']) - 1) for t in range(11) for x, y in [(r['pts'][k][0] + (r['pts'][k + 1][0] - r['pts'][k][0]) * t / 10, r['pts'][k][1] + (r['pts'][k + 1][1] - r['pts'][k][1]) * t / 10)] for rp in ctx['ISLRAIL'])
    if dmin < 19.5 + 30: bad.append(f"קרוב למסילה: {dmin / 10:.1f} מ׳")
    for r in (sv, sp):
        for k in range(len(r['pts']) - 1):
            for t in range(11):
                x, y = r['pts'][k][0] + (r['pts'][k + 1][0] - r['pts'][k][0]) * t / 10, r['pts'][k][1] + (r['pts'][k + 1][1] - r['pts'][k][1]) * t / 10
                if is_sea(x, y): bad.append(f"{r['id']} בים ב-({x:.0f}, {y:.0f})"); break
    IL = {l['id']: l for l in ctx['ISLF']['lots']}
    if gap(tuple(IL['IS-LIGHT']['rect']), band(sv['pts'][-2], sv['pts'][-1], 19.5)) > 20: bad.append('לא מגיעה למגדלור')
    hl = IL['IS-HELI']; hb = (hl['c'][0] - hl['ring'], hl['c'][1] - hl['ring'], hl['c'][0] + hl['ring'], hl['c'][1] + hl['ring'])
    if gap(hb, band(sp['pts'][0], sp['pts'][1], 19.5)) > 20: bad.append('לא מגיעה למנחת')
    if gap(tuple(IL['IS-TURN']['rect']), band(sv['pts'][0], sv['pts'][1], 19.5)) > 20: bad.append('לא מתחברת לרחבת הסיבוב')
    C('האי (H9) — דרך השירות למגדלור ולמנחת: על היבשה, רחוקה מהמסילה, יוצאת מרחבת הסיבוב ומגיעה לשניהם (שאלה 1 במפה)', bad,
      f"המרחק הקטן ביותר מציר המסילה: {dmin / 10:.1f} מ׳; מגיעה למגדלור ובשלוחה של 7.5 מ׳ למנחת. השבילים במדרון המערבי (F9) — מדרך הנמל אל הכפר ואל יער הפסגה.")
    # 10. R-65 — the hotels of the city, each on its lot
    H = [('D2-02', 'D2'), ('A5-HOTEL', 'A5'), ('AIR-HOTEL', 'E2'), ('F3-01', 'F3'), ('IS-HOSTEL', 'G9')]
    allr = {l['id']: l for l in ctx['LOTS'] + ctx['AIRF']['lots'] + ctx['ISLF']['lots'] + ctx['SITES'] if l.get('rect') and not isinstance(l['rect'][0], (list, tuple))}
    bad = [h for h, z in H if h not in allr]
    ctx['HOTELS'] = [dict(id=h, zone=z, label=allr[h]['label'], m=[round((allr[h]['rect'][2] - allr[h]['rect'][0]) / 10, 1), round((allr[h]['rect'][3] - allr[h]['rect'][1]) / 10, 1)]) for h, z in H if h in allr]
    C('R-65 — המלונות: D2 על מגרש גדול יותר, ‏A5, מלון השדה עם מלון הצוותים, מלון הים והאי — כל אחד מגרש במפה', bad,
      '; '.join(f"{h['zone']} — {h['label'].split(' — ')[0]} ({h['m'][0]} × {h['m'][1]} מ׳)" for h in ctx['HOTELS']) + '. ' + DEFAULT + '.')
    return out
