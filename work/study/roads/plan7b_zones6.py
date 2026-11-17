# -*- coding: utf-8 -*-
"""1.11 · round 6 of the road map (R-42: the map is the one source, and after every zone it takes what was built): B4 and B3 read from the
zone files themselves — the same files the sheets and the game patches are built from — so the map cannot drift from them:
  B4 ← exp34/b4v5/b4v5.json (B4 v5: the market 30 × 17 north, its car park south, 43 stalls of 2.8 × 5.6 m and two underground car parks, the park in the north-west corner);
  B3 ← exp34/b3v5/b3v5.json (B3 v5: 15 small houses, 2 small buildings, 4 private lanes, the strip facing the park, the shared garden;
       no school — D‑325; no car service — D‑326).
The lot rectangles here are at the game's road widths (the column 'game' of road_sections.json), as in the game."""
import json, os
W = '/home/claude/work'
B4 = json.load(open(W + '/exp34/b4v5/b4v5.json', encoding='utf-8'))
B3 = json.load(open(W + '/exp34/b3v5/b3v5.json', encoding='utf-8'))
C3 = json.load(open(W + '/exp34/c3/c3v3.json', encoding='utf-8'))   # 1.11 round 6ו: C3 v3 (S7F187)
BANDS3 = json.load(open(W + '/exp34/bld42/bands_bld42.json', encoding='utf-8'))
BANDS = json.load(open(W + '/exp34/b3v5/bands_bld41d.json', encoding='utf-8'))
USE = {'residential': 'home', 'shop': 'shop', 'clinic': 'public', 'school': 'public', 'service': 'service'}

def road_of(a):
    """the map road a curb cut (acc) of the game opens to — by the sidewalk it sits on"""
    x, y, w, h = a['x'], a['y'], a['w'], a['h']
    # 1.11 13:30: the point is the curb cut itself (on its own curb) — the build snaps it to the road's edge on THAT side (it was the centre line, and the snap took the far curb)
    if y >= 2482 and y + h <= 2502 and x < 1868: return 'LC-SCH', (x + w / 2, y + h / 2), (x + w / 2, y - 6)
    if 1252 <= x <= 1282: return 'CL-W', (x + w / 2, y + h / 2), (1320, y + h / 2)
    if 1728 <= x <= 1756: return 'LC-B', (x + w / 2, y + h / 2), (x - 60, y + h / 2)
    if 1844 <= x <= 1872: return 'LC-B', (x + w / 2, y + h / 2), (x + 80, y + h / 2)
    raise ValueError(('curb cut on no known road', a))

def add(S, DW):
    """appends B4 and B3 to the map's sites (S) and driveways (DW)"""
    # ---------------- B4 (v4) ----------------
    W4 = 'B4 v5 — מהקובץ של האזור (b4v5.json), אותו מקור כמו הגיליון והמשחק'
    for b in B4['buildings']:
        t = BANDS[b['type']]
        S.append(dict(zone='B4', id=b['id'], kind='building', rect=tuple(b['foot']), label='%s — %d × %d מ׳, %d קומות' % (b['label'], t['W'], t['D'], t['floors']),
                      why=W4 + '; הכניסה ' + ('מרחוב בית הספר' if b['id'] == 'B4-N1' else 'מהרחוב שלה') + '.', use=USE.get(b['kind'], 'home'), floors=t['floors'], band_px=max(0, b['band'][3] - b['band'][1]), r6=True))
    for l in B4['lots']:
        y = l['yard']; n = sum(len(r['xs']) for r in l['rows']) + len(l['ew'])
        r = [y['x'], y['y'], y['x'] + y['w'], y['y'] + y['h']]
        for rw in l['rows']: r = [min(r[0], min(rw['xs'])), min(r[1], rw['y']), max(r[2], max(rw['xs']) + 38), max(r[3], rw['y'] + 76)]
        for e in l['ew']: r = [min(r[0], e['x']), min(r[1], e['y']), max(r[2], e['x'] + 76), max(r[3], e['y'] + 38)]
        S.append(dict(zone='B4', id=l['id'], kind='parking', rect=tuple(r), label='%s — %d מקומות' % (l['label'], n), why=W4 + '.', stalls=n, r6=True))
        for i, a in enumerate(l['acc']):
            rd, at, to = road_of(a); DW.append(dict(zone='B4', id='DW-%s%s' % (l['id'], '-%d' % (i + 1) if len(l['acc']) > 1 else ''), road=rd, at=at, label='הכניסה ל' + l['label'], why=W4 + '.', to=to, lanes='1+1'))
    pkr = [s_['rect'] for s_ in S if s_['zone'] == 'B4' and s_['kind'] == 'parking']
    for q in B4.get('lanes') or []:
        y1 = min([q['y'] + q['h']] + [r[1] for r in pkr if r[0] < q['x'] + q['w'] and r[2] > q['x'] and r[1] > q['y']])   # the lane ends where its car park begins
        S.append(dict(zone='B4', id=q['id'], kind='yard', rect=(q['x'], q['y'], q['x'] + q['w'], y1), label=q['label'], why=W4 + '.', r6=True))
    n1 = next(b for b in B4['buildings'] if b['id'] == 'B4-N1')
    S.append(dict(zone='B4', id='B4-N1-FRONT', kind='yard', rect=(n1['foot'][0], 2618, n1['foot'][2], n1['foot'][1]), label='החצר הקדמית של N1 והשביל לרחוב בית הספר', why=W4 + '; הכניסה הראשית צפונה.', r6=True))
    for g in B4.get('garages') or []:
        if any(min(g['ramp'][2], r[2]) > max(g['ramp'][0], r[0]) and min(g['ramp'][3], r[3]) > max(g['ramp'][1], r[1]) for r in pkr): continue   # a ramp inside a car park is part of it
        S.append(dict(zone='B4', id=g['id'] + '-RAMP', kind='yard', rect=tuple(g['ramp']), label='הרמפה של ' + g['label'] + ' — %d מקומות' % g['stalls'], why=W4 + '; ברירת מחדל לאישורך (R-48 (א)).', r6=True))
    d = B4['drop']; S.append(dict(zone='B4', id='B4-S3-DROP', kind='yard', rect=tuple(d), label='מפרץ ההורדה של בית הספר', why=W4 + '.', r6=True))
    S.append(dict(zone='B4', id='B4-PARK', kind='park', rect=(1282, 2618, 1395, 2820), label='הפארק השכונתי — מגרש משחקים, ספסלים ועצים', why=W4 + '; בפינה הצפונית-מערבית, כמו בתוכנית.', use='park', r6=True))
    S.append(dict(zone='B4', id='B4-COURT', kind='court', rect=tuple(B4['court']), label='מגרש הכדורסל של בית הספר — 28 × 15 מ׳', why=W4 + '; R-48 (ד).', r6=True))
    # ---------------- B3 (v5) ----------------
    W3 = 'B3 v5 — מהקובץ של האזור (b3v5.json), אותו מקור כמו הגיליון והמשחק (D‑324)'
    lots = {h['id']: h['lot'] for h in B3['houselots']}
    for b in B3['buildings']:
        t = BANDS[b['type']]
        if b['id'] in lots:
            S.append(dict(zone='B3', id=b['id'] + '-LOT', kind='lot', rect=tuple(lots[b['id']]), label='בית פרטי · ' + b['addr'], why=W3 + '; חניה בשביל הרכב, גינה וגדר חיה.', use='home', r6=True))
            S.append(dict(zone='B3', id=b['id'], kind='house', rect=tuple(b['foot']), label='הבית — %d × %d מ׳, 2 קומות' % (t['W'], t['D']), why='הטביעה של הבית', parent=b['id'] + '-LOT', r6=True))
        else:
            S.append(dict(zone='B3', id=b['id'], kind='building', rect=tuple(b['foot']), label='%s — %d × %d מ׳, %d קומות' % (b['label'], t['W'], t['D'], t['floors']), why=W3 + '; החניה מאחור.', use='home', floors=t['floors'], band_px=max(0, b['band'][3] - b['band'][1]), r6=True))
    for l in B3['lots']:
        y = l['yard']; r = (y['x'], y['y'], y['x'] + y['w'], y['y'] + y['h'])
        if l['id'].startswith('B3-LN-'):
            S.append(dict(zone='B3', id=l['id'], kind='yard', rect=r, label=l['label'] + ' — סמטה משותפת ללא מוצא, אבנים משתלבות', why=W3 + '; לא רחוב ברשת — חצר משותפת של הבתים (D‑328, ברירת מחדל).', r6=True))
            ct = [s_ for s_ in B3['stalls'] if s_['lot'] == l['id'] and s_.get('rot') == 'S']
            if ct:
                cr = (min(s_['x'] for s_ in ct), min(s_['y'] for s_ in ct), max(s_['x'] + s_['w'] for s_ in ct), max(s_['y'] + s_['h'] for s_ in ct))
                S.append(dict(zone='B3', id=l['id'] + '-PK', kind='parking', rect=cr, label='החניה שמאחורי הבניינים, מ' + l['label'] + ' — %d מקומות' % len(ct), why=W3 + '; מעבר לרצועה שהגג מכסה (R-09).', stalls=len(ct),
                              aisle_m2=(cr[2] - cr[0]) * 56 / 100, r6=True))                    # its aisle is the lane in front of it
        elif l['id'].endswith('-PK'):
            n = len(l['ew']); S.append(dict(zone='B3', id=l['id'], kind='parking', rect=(r[0], r[1], r[2], r[3]), label='%s — %d מקומות' % (l['label'], n), why=W3 + '.', stalls=n, r6=True))
        for i, a in enumerate(l['acc']):
            rd, at, to = road_of(a); DW.append(dict(zone='B3', id='DW-' + l['id'], road=rd, at=at, label='הכניסה ל' + l['label'], why=W3 + '.', to=to, lanes='1'))
    S.append(dict(zone='B3', id='B3-STRIP-W', kind='park', rect=(1282, 1718, 1732, 1798), label='הרצועה מול הפארק — טיילת, עצים וספסלים', why='D‑260; טבלת השימושים.', use='park', r6=True))
    S.append(dict(zone='B3', id='B3-STRIP-E', kind='park', rect=(1868, 1718, 2350, 1798), label='הרצועה מול הפארק — טיילת, עצים וספסלים', why='D‑260; טבלת השימושים.', use='park', r6=True))
    S.append(dict(zone='B3', id='B3-GARDEN', kind='park', rect=(2064, 2370, 2262, 2546), label='הגינה המשותפת — מגרש משחקים', why=W3 + '.', use='park', r6=True))
    return S, DW

def add_c3(S, DW, villa, it, dw):
    """1.11 round 6ו (R-42, the review 15:10 R-57): C3 from its zone file c3v3.json — the villas in their own sizes, the pads, the player's lot
    round the turning circle, the gate into the west wing, the pad 4 m east (the hangar of L8 clear of its safety circle)"""
    WC = 'C3 v3 — מהקובץ של האזור (c3v3.json), אותו מקור כמו הגיליון והמשחק (S7F187)'
    lots = {h['id']: h['lot'] for h in C3['houselots']}
    for b in C3['buildings']:
        t = BANDS3[b['type']]; x0, y0, x1, y1 = lots[b['id']]; n = sum(1 for q in C3['stalls'] if q['house'] == b['id'])
        S.append(dict(zone='C3', id=b['id'], kind='lot', rect=(x0, y0, x1, y1), label='%s — %d חניות' % (b['label'], n), why=WC + '; החזית אל רחוב הווילות, כניסה משלה.', use='home', r6=True))
        S.append(dict(zone='C3', id=b['id'] + '-H', kind='house', rect=tuple(b['foot']), label='הבית — %s × %s מ׳, %d קומות' % (t['W'], t['D'], t['floors']), why='הטביעה של הווילה', parent=b['id'], r6=True))
    S.append(dict(zone='C3', id='C3-GARDEN', kind='park', rect=(3178, 1760, 3590, 1850), label='המדשאה — גינה, ספסלים והגנן (EYE‑2)', why=WC + '; בין שדרת השדה לווילה 4, בלי מבנה.', use='park', r6=True))
    x0, y0, x1, y1 = C3['ph']['lot']
    villa('C3', 'C3-PH', (x0, y0, x1, y1), 'בית השחקן (LOT-PH) — המגרש לפי רמה 8', WC + '; סביב מעגל הסיבוב: הכנף המערבית לבית של כל רמה, המזרחית למנחת, לבריכה ולמבנה למסוק.', 'N', poly_c=tuple(C3['turn']['c']), use='home', house=False)
    lv8 = C3['levels'][7]; pd = lv8['pad']
    it('C3', 'C3-PH-HELI', 'pad', None, 'המנחת של בית השחקן — Ø %d מ׳, בטיחות Ø %d מ׳' % (pd['r'] / 5, pd['safety'] / 5), WC + '; 4 מ׳ מזרחה מסבב 6ה, כדי שהמבנה למסוק של רמה 8 יהיה מחוץ לשטח הבטיחות (R-57).', c=tuple(pd['c']), r=pd['r'], safety=pd['safety'])
    g = C3['gate']
    it('C3', 'C3-PH-GATE', 'site', [(g['x'] + g['w'], g['axis']), (g['x'] - 25, g['axis'])], 'שער בית השחקן', WC + '; מהצד המערבי של מעגל הסיבוב אל הכנף המערבית (R-57).', hw=28, lanes='1', via='E31_23', cls='driveway')
    for l in C3['lots']:
        a = l['acc'][0]; west = a['x'] < 3110; y_ = a['y'] + a['h'] / 2
        dw('C3', 'DW-' + l['id'][:5], 'LC-C3', (3056 if west else 3164, y_), 'הכניסה ל' + l['id'][3:5], WC + '; %d חניות על משטח מרוצף.' % (len(l.get('rows') or []) or round(l['yard']['h'] / 28)), to=(3006 if west else 3214, y_))
