# -*- coding: utf-8 -*-
"""8.11 · סבב 9ס של מפת הדרכים — המפה מעודכנת למה שנבנה (S7F265), מסונכרנת עם המשחק ועם ההחלטות של הבעלים מ-8.11 (D‑502 עד D‑505).
הבסיס: הפלט של סבב 9נ2 כמו שהוא (city_plan.json, ‏city_plan.html) — עותק שלו ב-W/_to_delete/roads_before_r9s, וכל הרצה מתחילה ממנו מחדש.
השרשרת של הסבבים הקודמים לא רצה שוב: היא קוראת קבצים מנתיב שכבר לא קיים (/home/claude/…), והתוצאה שלה כבר בקבצים.
מה הסבב עושה — לפי הביקורת של 7.11 20:30 (R-84, ‏R-85, ‏R-86; סבב הסדר: 16:40 סעיף ז, 17:45 סעיפים א, ב.5, ג 1–8):
  1. שדה גרסה אחד (version = "9ס") — הכותרת, הכותרת הראשית, שורת הסבב וטבלת הסבבים נגזרים ממנו.
  2. D2 החדש (D‑496, ‏S7F264) מהמשחק, הדרך מהמעגל לחניון החנויות (הבעלים 09:07) וההורדה של המלון (09:09); C2, ‏B2 ו-B1 (האגם, המזחים, הסירה) מהמשחק.
  3. S9a כמו שנבנה ב-S7F265; ‏BYPASS, ‏ST-COAST, ‏REF-SPUR (בוטלה — D‑504), הצינור PIPE-REF, ורציפי E3 (D‑505).
  4. הסטטוס של כל מגרש, הצמתים, המעברים, הדרכים, התחנות ועמודת "היום" של הקווים — נגזרים מהמשחק (probe_s7f265.js → game_s7f265.json).
  5. השלבים S13–S16 לכל האזורים, וציורי השלבים S14–S16; שורת "מעודכן עד" בכל ציור.
  6. טבלת ההתאמה מפה↔משחק בשני הכיוונים (r9s_match.py) → deliver/2026-11-08/map/map_vs_game_9s.json.
    python3 plan7b_r9s.py → city_plan.json, city_plan.html, deliver/2026-11-08/map/Turbo_City_Roads_9s.html, map_vs_game_9s.json"""
import json, os, sys, shutil, math, re, html, copy, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
W = os.path.dirname(os.path.dirname(HERE))
E = html.escape
import r9s_match as MT

VERSION = '9ס'; DATE = '8.11.2026'; BUILD = 'S7F266'; BUILD_SHA = '2c56ba6266fb'   # 8.11 02:40: S7F266 (הרציפים, העקיפה, הצינור)
GAME_FILE = os.path.join(W, 'clean_r2b_025637', 'out', '_rebuild_S7F265.html')
BACK = os.path.join(W, '_to_delete', 'roads_before_r9s')
OUT = os.path.join(W, 'deliver', '2026-11-08', 'map')
PIPE_SHARED = os.path.join(W, 'shared', 'pipe_ref.json')
PLAN_NEW = os.path.join(W, 'plan600', 'data', 'new.json')
FILES = ('city_plan.json', 'city_plan.html', 'names.json')
ASK = 'לאישורך'
LOG = []          # (the section of the page, the item, what was done) — the section of 9ס and the handback are made from it
def log(sec, item, what): LOG.append(dict(sec=sec, item=item, what=what))


def start():
    """the 9נ2 output, as it is: a copy once (before the first run), and every run starts from the copy"""
    os.makedirs(BACK, exist_ok=True)
    for f in FILES:
        b = os.path.join(BACK, f)
        if not os.path.exists(b): shutil.copyfile(os.path.join(HERE, f), b)
    P = json.load(open(os.path.join(BACK, 'city_plan.json'), encoding='utf-8'))
    H = open(os.path.join(BACK, 'city_plan.html'), encoding='utf-8').read()
    assert P['batch'] == '9נ' and '<h2>סבב 9נ2' in H, 'the copy is not the output of 9נ2'
    return P, H


# ====================================================================== 1 · the version — one field
def d_version(P):
    P['version'] = VERSION; P['batch'] = VERSION; P['at'] = DATE; P['by'] = 'סוכן המפה'
    P['title'] = f'תוכנית הדרכים של כל העיר — סבב {VERSION}'
    P['synced_with'] = dict(build=BUILD, sha1=BUILD_SHA, file='clean_r2b_025637/out/_rebuild_S7F265.html', probe='study/roads/probe_s7f265.js', date=DATE)
    P['updated_until'] = f'{BUILD} · סבב {VERSION} · {DATE}'
    log('ז.1', 'שדה הגרסה', f'שדה גרסה אחד ("{VERSION}") מזין את כותרת הדף, את הכותרת הראשית, את שורת הסבב ואת טבלת הסבבים.')


# ====================================================================== 2 · D2 — as built (D‑496, S7F264), the road of 09:07, the hotel of 09:09
REPL_D2 = 'D2 גרסה 3 (D‑496, ‏S7F264)'
def status(state, stage=None, build=None, by=None, src=None):
    return {k: v for k, v in dict(state=state, stage=stage, build=build, by=by, src=src).items() if v}

def d_d2(P, G):
    NB = {n['id']: n for n in G['nodes']}
    # the road from the circle to the shops' car park — the owner 09:07 (p688): a new class, an access road 1+1 of 7 m (the builder's default — to approve)
    P['classes']['lane2'] = dict(he='דרך גישה 1+1', lanes='1+1', laneN=2, lane_m=3.5, walk_m=1.0, width_m=9.0, halfW=45.0, twoway=True, dirN=1, median_m=0,
                                 lanesHe='נתיב אחד לכל כיוון, 7 מ׳ בסך הכול, ומדרכה של מטר מכל צד',
                                 game=dict(type='lane2', halfW_px=35, note='p688 — מחלקה חדשה במשחק'),
                                 why='הבעלים 8.11 09:07 (לאישורך — ברירת המחדל של הבונה): רחוב מקומי (9.6 מ׳ ושתי מדרכות של 2 מ׳) לא נכנס ברצועה של 9.1 מ׳ בין שורת החנויות למלון בלי להזיז מבנה.')
    for nid, kind, label in (('K43_10', 'corner', 'הדרך לחניון החנויות יוצאת מהמעגל של דרך השדות'), ('K43_11', 'end', 'הדרך מהמעגל נכנסת למעבר של חניון החנויות (D2-LOT-01)')):
        g = NB[nid]
        if not any(n['id'] == nid for n in P['nodes']):
            P['nodes'].append(dict(id=nid, x=g['x'], y=g['y'], kind=kind, label=label, why='הבעלים 8.11 09:07 · במשחק p688 (S7F265)', deg=2 if kind == 'corner' else 1, zone='D2'))
    k08 = next(n for n in P['nodes'] if n['id'] == 'K43_08')
    k08['today'] = 'היום (עד S12): סוף זמני של דרך השדות — מעגל סיבוב, וממנו יוצאת הדרך לחניון החנויות (p659, ‏p688); דרך החממות (LC-D1) צפונה — עם S12'
    k08['deg'] = 3
    rd = dict(id='D2-LCH', name='הדרך לחניון החנויות', cls='lane2', nodes=['K43_08', 'K43_10', 'K43_11'], lanes='1+1', truck=False, kind='road',
              why='הבעלים 8.11 09:07: "כביש שיורד בצמוד למלון משמאל, מהכיכר לחניות של החנויות" — מהמעגל K43_08 דרומה, ברצועה שבין שורת החנויות למלון, '
                  'אל המעבר של חניון החנויות. במשחק: D2-LCH1 ו-D2-LCH2 (p688, ‏S7F265) — פתח במעגל, הנמכה אל המעבר, שני פנסים בצד המלון.')
    if not any(r['id'] == 'D2-LCH' for r in P['roads']): P['roads'].append(rd)
    for k, (a, b) in enumerate((('K43_08', 'K43_10'), ('K43_10', 'K43_11')), 1):
        A, B = NB[a], NB[b]; sid = f'D2-LCH/{k}'
        if any(s['id'] == sid for s in P['segments']): continue
        P['segments'].append(dict(id=sid, road='D2-LCH', a=a, b=b, cls='lane2', lanes='1+1', kind='road', len_m=round(math.hypot(B['x'] - A['x'], B['y'] - A['y']) / 10, 1),
                                  pts=[[A['x'], A['y']], [B['x'], B['y']]], truck=False, zones=['D2'], home='D2', stage='S8', built='S7F265',
                                  game=f'D2-LCH{k}', owner='הבעלים 8.11 09:07'))
    P['zones']['D2']['purpose_was'] = P['zones']['D2'].get('purpose'); P['zones']['D2']['purpose'] = 'עסקים, מלונות, קולנוע ושורת חנויות (D‑496)'
    P['zones']['D2']['roads'] = sorted(set(P['zones']['D2']['roads']) | {'D2-LCH'}); P['zones']['D2']['segments'] += ['D2-LCH/1', 'D2-LCH/2']
    log('ב.5', 'D2 — הדרך מהמעגל לחניון החנויות (09:07)', 'K43_08 → K43_10 ‏(4265, 862) → K43_11 ‏(4265, 1070): דרך גישה 1+1 ברוחב 7 מ׳ ומדרכה של מטר מכל צד — '
        'מחלקה חדשה במפה (lane2), כמו במשחק (D2-LCH1 / D2-LCH2, ‏p688). ' + ASK + ': רחוב מקומי לא נכנס ברצועה של 9.1 מ׳.')
    # the old D2 — replaced, not deleted
    old_lots = [l for l in P['lots'] if l['zone'] == 'D2']; old_r7 = [i for i in P['r7']['items'] if i.get('zone') == 'D2']
    old_dw = [d for d in P['driveways'] if d['zone'] == 'D2']; old_sr = [r for r in P['site_roads'] if r.get('zone') == 'D2']
    for x in old_lots + old_r7:
        x['status'] = status('הוחלף', 'S8', by=REPL_D2, src='המשחק')
        x['future'] = False
    for x in old_dw + old_sr: x['replaced'] = REPL_D2
    # the new D2, from the game
    new = []
    for b in G['D2_BUILDINGS']:
        new.append(dict(id=b['id'], zone='D2', kind='building', label=b['label'] + (f" — {b['kind']}" if b.get('kind') and b['kind'] not in b['label'] else ''),
                        rect=[b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h']], entrance=[b['entrance']['x'], b['entrance']['y']] if b.get('entrance') else None))
    for b in G['D2_PARKING']:
        new.append(dict(id=b['id'], zone='D2', kind='parking' if 'LOT' in b['id'] else ('drop' if 'DROP' in b['id'] else 'svc'), label=b['label'],
                        rect=[b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h']]))
    pl = G['D2_POOL']; new.append(dict(id='D2-POOL', zone='D2', kind='water', label='הבריכה של המלון', rect=[pl['x'], pl['y'], pl['x'] + pl['w'], pl['y'] + pl['h']]))
    for b in G['D2_ISLANDS']:
        new.append(dict(id=b['id'], zone='D2', kind='island', label='האי של ההורדה — נכנסים מערבה בחצי הצפוני ויוצאים מזרחה בחצי הדרומי (09:09)', rect=[b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h']]))
    for x in new: x['status'] = status('קיים', 'S8', 'S7F264', src='המשחק')
    for x in new:
        if x['id'] in ('D2-DROP', 'D2-ISL-DROP'): x['status'] = status('קיים', 'S8', 'S7F265', by='הבעלים 8.11 09:09', src='המשחק')
    P['r9s_lots'] = [l for l in P.get('r9s_lots', []) if l['zone'] != 'D2'] + new
    dws = []
    for a in G['D2_ACCESS']:
        r = [a['x'], a['y'], a['x'] + a['w'], a['y'] + a['h']]
        road = {'DW-D2-04': 'CL-MALL', 'DW-D2-02': 'CL-AC', 'DW-D2-03': 'CL-AC', 'DW-D2-01': 'LC-N'}.get(a['id'])
        dws.append(dict(id=a['id'] + '·9ס', game=a['id'], zone='D2', road=road, rect=r, label=a['label'], status=status('קיים', 'S8', 'S7F264', src='המשחק')))
    dws.append(dict(id='DW-D2-DROP·9ס', game='D2-DROP', zone='D2', road='CL-AC', rect=[4526, 1222, 4600, 1306], label='ההורדה של המלון — חיבור ישר מדרך המטען: נכנסים מערבה בחצי הצפוני, יוצאים מזרחה בחצי הדרומי, סביב האי, בלי רוורס',
                    status=status('קיים', 'S8', 'S7F265', by='הבעלים 8.11 09:09', src='המשחק')))
    P['r9s_driveways'] = dws
    P.setdefault('replaced', [])
    P['replaced'] = [r for r in P['replaced'] if r.get('by') != REPL_D2] + [dict(id=x['id'], kind=k, label=x.get('label', ''), by=REPL_D2) for k, xs in
                                                                          (('מגרש', old_lots), ('פריט', old_r7), ('פתח', old_dw)) for x in xs]
    log('ב.5', 'D2 — הציור של האזור', f'ה-D2 הישן (המלון העסקי, קמפוס ההייטק, כיכר המטה, המשרדים והמגדלים) — {len(old_lots)} מגרשים, {len(old_r7)} פריטים ו-{len(old_dw)} פתחים — '
        f'מסומן "הוחלף ב-{REPL_D2}" ולא נמחק. במקומו מהמשחק: {len(G["D2_BUILDINGS"])} מבנים (שורת החנויות, הקולנוע, המלון הגדול, מגדל המטה ו"אופק טכנולוגיות"), '
        f'{len(G["D2_PARKING"])} חניונים ומפרצים, הבריכה, האי של ההורדה ו-{len(dws)} פתחים.')
    log('ב.5', 'D2 — ההורדה של המלון (09:09)', 'חיבור ישר מדרך המטען (x 4600): נכנסים מערבה בחצי הצפוני ויוצאים מזרחה בחצי הדרומי, סביב האי D2-ISL-DROP, בלי רוורס; '
        'הפינה של דרך המטען ישרה, עם אבן שפה (p687).')


# ====================================================================== 3 · B2 and B1 — the lake, the piers, the boat, the mini golf of 9 holes (S7F252)
def d_lake(P, G):
    B = G['B12']; REPL = 'B2 / B1 כמו שנבנו (D‑485, ‏D‑488, ‏S7F252)'
    olds = [i for i in P['r7']['items'] if i.get('zone') == 'B2' and i['id'] in ('B2-GOLF', 'B2-PLAY', 'B2-LAKEPATH', 'B2-FS1', 'B2-FS2', 'B2-FS3', 'B2-FS4')]
    for x in olds: x['status'] = status('הוחלף', 'S8', by=REPL, src='המשחק')
    new = [dict(id='B2-GOLF9', zone='B2', kind='court', label='מיני גולף — 9 גומות (36 × 30 מ׳)', rect=B['golf']),
           dict(id='B2-PLAY9', zone='B2', kind='court', label='מגרש המשחקים', rect=B['play']),
           dict(id='B2-GOLF-BOOTH', zone='B2', kind='building', label='הקופה של המיני גולף', rect=B['booth'])]
    for p in B['piers']:
        z = MT.zone_of((p['stem'][0] + p['stem'][2]) / 2, (p['stem'][1] + p['stem'][3]) / 2)
        new.append(dict(id=p['id'], zone=z, kind='pier', label=p['label'], rect=[min(p['stem'][0], p['head'][0]), min(p['stem'][1], p['head'][1]), max(p['stem'][2], p['head'][2]), max(p['stem'][3], p['head'][3])],
                        parts=[p['stem'], p['head']]))
    new += [dict(id='B1-BOAT-PIER', zone='B1', kind='pier', label='מזח הסירה — סירת המשוטים של האגם (B1-BOAT)', rect=B['boatPier']),
            dict(id='B1-PICNIC', zone='B1', kind='park', label='פינת הפיקניק — ארבעה שולחנות ומנגל', rect=B['picnic']),
            dict(id='B1-P', zone='B1', kind='parking', label='החניון של B1 — 10 חניות', rect=B['b1p']['rect'])]
    for x in new: x['status'] = status('קיים', 'S8', 'S7F252', src='המשחק')
    P['r9s_lots'] = [l for l in P.get('r9s_lots', []) if l['id'] not in {x['id'] for x in new}] + new
    P['terrain']['lake_game'] = dict(id='B2-LAKE', label=G['B2_LAKE']['label'], pts=G['B2_LAKE']['pts'], build='S7F252', why='האגם כמו שנבנה ב-S8 (D‑485): B2 ו-B1, רציף אחד')
    P['zones'].setdefault('B1', {})['stage'] = 'S12'
    P['zones']['B1']['parts'] = [dict(stage='S8', build='S7F252', what='האגם בתוך B1, המזח הצפוני, המזח המערבי, מזח הסירה וסירת המשוטים, פינת הפיקניק והחניון של B1'),
                                 dict(stage='S12', what='שאר B1 — הפארק הצפוני')]
    P['replaced'] = [r for r in P.get('replaced', []) if r.get('by') != REPL] + [dict(id=x['id'], kind='פריט', label=x['label'], by=REPL) for x in olds]
    log('ב.5', 'B2 — המיני גולף והדיג', 'במקום "מיני גולף — 18 גומות", "שביל החוף" ו-4 עמדות הדיג (B2-FS1–4) — כמו במשחק: מיני גולף של 9 גומות, מגרש המשחקים, '
        'ושלושה מזחי דיג (הצפוני, המערבי והדרומי). הישנים מסומנים "הוחלף".')
    log('ב.5', 'B1 — מה שכבר נבנה', 'B1 כבר לא כולו "עתידי — S12": האגם בתוך B1, המזח הצפוני, המזח המערבי, מזח הסירה, סירת המשוטים, פינת הפיקניק והחניון — '
        '"נבנה ב-S8 (S7F252)"; שאר הפארק — S12.')


# ====================================================================== 4 · S9a as built in S7F265
S9A_BUILT = ['LC-E3/1', 'LC-E3/2', 'LC-E3W/1', 'CL-I/1', 'CL-I/2', 'CL-I/3', 'CL-I/4', 'CL-I/5', 'CL-I/6', 'CL-I/7', 'CL-F/1']
def d_s9a(P, G):
    for s in P['segments']:
        if s['id'] in S9A_BUILT: s['built'] = BUILD; s['state'] = 'קיים'
    for s in P['segments']:
        if s['id'] == 'CL-F/2': s['today'] = 'לא נבנה — בין חניון השדה (מוקפא, עד y ‏1692) לאגן המרינה (y ‏1830) יש 13.8 מ׳, ועורק 2+2 צריך 23.6 מ׳; עם CL-F/3 ושער הדרום (S13) — ' + ASK
    k = next(n for n in P['nodes'] if n['id'] == 'K61_176')
    k['today'] = 'היום: סוף זמני של דרך המרינה (CL-F/1), עם מחסום — עד CL-F/2 ו-CL-F/3 (S13)'
    for c in P['crossings']:
        if c['id'] in ('UX-1', 'LX-1', 'LX-2'): c['built'] = BUILD
        if c['id'] in ('LX-1', 'LX-2'): c['today'] = 'נבנה ב-S7F265: משטח, מסילות שקועות, מחסומים ואורות שיורדים כשרכבת מתקרבת; ראש הגשר סגור במחסום'
        if c['id'] in ('LX-3', 'LX-4'): c['state'] = 'בוטל (D‑504)'; c['why'] = 'בוטל (D‑504): מסילת בית הזיקוק יצאה מהתוכנית; במקומה הצינור PIPE-REF על עמודים גבוהים, מעל שדרת הנמל.'
    lots = [l for l in P['sites'] + P['r7']['items'] + P['lots'] if l.get('zone') == 'E3']
    for l in lots:
        if l['id'] in ('E3-PB',) or 'E3-PB' in l['id']:
            l['stalls_was'] = l.get('stalls'); l['stalls'] = 15
            l['label_was'] = l.get('label'); l['label'] = 'חניון E3-PB — 15 חניות (במקום 20; חצר מסוף החבילות נשארת עד שמחסן החבילות עובר ל-E5-04 ב-S9b — ' + ASK + ')'
    # the buildings of E3 that have no lot of their own in the map (the station, the kiosk, the toilets, the dispatchers' building, the parcels' terminal)
    have = [l.get('rect') for l in P['sites'] + P['r7']['items'] + P['lots'] if l.get('zone') == 'E3' and isinstance(l.get('rect'), list)]
    add = []
    for b in G['C4_BUILDINGS']:
        if not isinstance(b, dict) or b.get('id') not in ('E3-STATION', 'E3-KIOSK', 'E3-WC', 'E3-BUS-TERMINAL', 'E3-PARCELS'): continue
        r = [b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h']] if 'w' in b else b.get('r')
        if r and not any(q and len(q) == 4 and all(isinstance(t, (int, float)) for t in q) and MT.rov(r, q) > 0.5 * (r[2] - r[0]) * (r[3] - r[1]) for q in have):
            add.append(dict(id=b['id'], zone='E3', kind='building', label=b['label'], rect=[round(v, 1) for v in r], status=status('קיים', 'S9', BUILD, src='המשחק')))
    P['r9s_lots'] = [l for l in P.get('r9s_lots', []) if l['id'] not in {a['id'] for a in add}] + add
    log('ג.1', 'E3 — המבנים בלי מגרש', 'נוספו למפה מהמשחק: ' + ', '.join(a['id'] for a in add) + ' — כל מבנה במגרש משלו.')
    log('ג.4', 'S9a כמו שנבנה', 'UX-1 בשלוש מסילות; J61_26 ברמזור; CL-F/1 עד K61_176 עם מחסום (CL-F/2 — עם S13, ' + ASK + '); CL-I/6–7, ‏LX-1 ו-LX-2; '
        'LC-E3/1 קטע אחד מהשער עד J54_26; ‏LC-E3/2; ‏J54_26 בארבע זרועות; E3-PA — ‏50 חניות, ‏E3-PB — ‏15 (' + ASK + ').')


# ====================================================================== 5 · the owner's decisions of 8.11 (D‑502 … D‑505)
def d_owner(P):
    R = {r['id']: r for r in P['rails']}
    by = R['BYPASS']; by['state'] = 'נבנה בחלקים'; by['stage'] = 'S9'
    by['parts'] = [dict(zone='E3', state='נבנה ב-S7F266 (D‑503)', what='לכל האורך ב-E3 — תיקון של S9a, שהניחה אותה רק על הגשר'),
                   dict(zone='E4', state='עם S9', what='החלק ב-E4')]
    _bj = os.path.join(W, 'shared', 'bypass_e3.json')
    if os.path.exists(_bj):
        _B = json.load(open(_bj, encoding='utf-8')); by['parts'][0]['pts'] = _B['pts']; by['parts'][0]['what'] += ' · כמו שנבנתה: ' + _B['note']
    by['note'] = (by.get('note') or '') + ' · סבב 9ס (D‑503): לא "עתידי, שלב 14" — החלק ב-E3 נבנה ב-S7F266, החלק ב-E4 עם S9.'
    rs = R['REF-SPUR']; rs['state'] = 'בוטלה (D‑504)'; rs['stage'] = None; rs['cancelled'] = True
    rs['note'] = 'בוטלה (D‑504, הבעלים 8.11): המסילות לבית הזיקוק יוצאות מהמפה ומהתוכנית; במקומן הצינור PIPE-REF על עמודים גבוהים, באותו מסדרון.'
    S = {s['id']: s for s in P['stations']}
    S['ST-COAST']['stage'] = 'S9'; S['ST-COAST']['why'] = 'D‑503: תחנת החוף (E4–E5) — עם S9, לא שלב 17'
    e3 = S['ST-E3']; e3['rects_was'] = e3['rects']
    e3['rects'] = [[5736, 1760, 5774, 2530], [5826, 1760, 5874, 2530]]
    e3['label'] = 'התחנה המרכזית (E3) — 2 רציפים, y ‏1760–2530 (D‑505)'
    e3['why'] = ('D‑505 (הבעלים 8.11): שני הרציפים מתארכים משני הקצוות — מ-y ‏1850–2290 (440 פיקסלים, שני קרונות) ל-y ‏1760–2530 (770 פיקסלים: ארבעה קרונות של RL-PS-01, כ-183 פיקסלים כל אחד, ומרווח), '
                 'באותו רוחב. הגג השקוף (LIKE-02) נשאר כמו שהוא; בהארכות — סוככי רציף באותו סגנון, ספסלים, תאורה, שילוט, פס מישושי וגדר. נבנה ב-S7F266.')
    e3['state'] = 'נבנה ב-S7F266 (D‑505)'
    # the pipe: the shared file of the game agent, or the corridor of the old spur
    src = 'המסדרון של REF-SPUR (הקובץ המשותף pipe_ref.json של סוכן המשחק עוד לא קיים — לסנכרן)'
    pts = [[2930, 5200], [2930, 5080]] + [p[:2] for p in rs['pts']]
    if os.path.exists(PIPE_SHARED):
        try:
            J = json.load(open(PIPE_SHARED, encoding='utf-8')); q = J.get('pts') or J.get('path') or J.get('route') or (J.get('axis') or {}).get('pts')
            if q and J.get('stage_rest'):   # 8.11: the game's axis is the C5 part; the rest (S10) follows the corridor of the old spur south of it
                q = [[2728, 5200], [2728, 4250]] + [t for t in q if t[1] < 4250][::-1] if q[0][1] < q[-1][1] else q
            if q and all(isinstance(t, (list, tuple)) and len(t) >= 2 for t in q): pts = [[t[0], t[1]] for t in q]; src = 'הקובץ המשותף pipe_ref.json (סוכן המשחק)'
        except Exception as e: src += f' — הקובץ לא נקרא: {e}'
    P['pipes'] = [dict(id='PIPE-REF', label='הצינור לבית הזיקוק — על עמודים גבוהים (D‑504)', pts=pts, src=src, clear_m=7,
                       why='D‑504 (מחזק את D‑475 ו-D‑480): ממזח הנפט (ממערב ל-C6) צפונה, מעל שדרת הנמל, אל חוות המכלים ב-C5; גובה חופשי של 7 מ׳ לפחות מעל כביש ומסילה.',
                       parts=[dict(zone='C5', state='נבנה ב-S7F266', what='החלק שבתוך C5 — עד גבול האזור (y ‏4250), עם תחנת מגופים', pts=[p for p in pts if p[1] <= 4250] or None),
                              dict(zone='C6', state='עם S10', what='השאר — ממזח הנפט עד גבול C5', pts=[p for p in pts if p[1] >= 4250] or None)],
                       valve=[2723, 4052])]
    log('D‑503', 'מסילת העקיפה', 'לא "עתידי, שלב 14": החלק ב-E3 — "נבנה ב-S7F266 (D‑503)", החלק ב-E4 — "עם S9".')
    log('D‑503', 'ST-COAST — תחנת החוף', 'שלב S9 (לא 17).')
    log('D‑504', 'REF-SPUR', '"בוטלה (D‑504)" — מצוירת אפורה ומקווקוות עם התווית, לא נמחקת; מעברי המפלס LX-3 ו-LX-4 שלה — "בוטל".')
    log('D‑504', 'PIPE-REF — שכבה חדשה', 'צינור על עמודים גבוהים (7 מ׳ חופשי לפחות) במסדרון של השלוחה הישנה: ממזח הנפט (ממערב ל-C6) ועד חוות המכלים ב-C5. '
        'החלק ב-C5 — S7F266, עם תחנת מגופים; השאר — S10. המסלול: ' + src + '.')
    log('D‑505', 'ST-E3 — הרציפים', 'שני הרציפים y ‏1760–2530 (במקום 1850–2290), באותו רוחב — "נבנה ב-S7F266".')


# ====================================================================== 6 · junctions, crosswalks and roads — as in the game (R-86 ג.2–4)
def d_net(P, G):
    NB = {n['id']: n for n in G['nodes']}; MN = {n['id']: n for n in P['nodes']}
    # J18_25: a signal (the owner 3.11 11:30 — every junction with a signal), as in the game
    j = MN['J18_25']; j['kind_was'] = j['kind']; j['kind'] = 'signal'
    j['why'] = 'סבב 9ס (R-86): רמזור, כמו במשחק — הבעלים 3.11 11:30: "כל הצמתים עם רמזור"; רחוב בית הספר מקבל ירוק רק כשמחכה בו רכב או הולך רגל.'
    if not any(s['node'] == 'J18_25' for s in P['signals']):
        P['signals'].append(dict(node='J18_25', label=j['label'], approaches=[dict(**{'from': 'J18_16', 'road': 'LC-B', 'cls': 'local', 'through': 1, 'left': 1, 'arrow': True}),
                                                                              dict(**{'from': 'J12_25', 'road': 'LC-SCH', 'cls': 'local', 'through': 0, 'left': 1, 'arrow': True}),
                                                                              dict(**{'from': 'B4S', 'road': 'LC-B', 'cls': 'local', 'through': 1, 'left': 0, 'arrow': False})],
                                 phases=['רחוב השכונה — ישר', 'רחוב בית הספר — לפי דרישה'], preempt=True, why=j['why'], r9s=True))
    # J18_16 and J31_42: the name said "right only", the detail a left lane — in the game both are signals with a left turn
    for nid in ('J18_16', 'J31_42'):
        n = MN[nid]; n['label_was'] = n['label']; n['label'] = re.sub(r'\s*\(ימינה בלבד\)', '', n['label']).strip() + ' (רמזור; נתיב שמאלה עם חץ)'
        for s in P['signals']:
            if s['node'] == nid: s['label_was'] = s.get('label'); s['label'] = n['label']
    def deep(o, old, new):
        if isinstance(o, dict): return {k: (v if k.endswith('_was') else deep(v, old, new)) for k, v in o.items()}
        if isinstance(o, list): return [deep(v, old, new) for v in o]
        return o.replace(old, new) if isinstance(o, str) else o
    for nid in ('J18_16', 'J31_42'):
        n = MN[nid]; P['bus'] = deep(P['bus'], n['label_was'], n['label']); P['signals'] = deep(P['signals'], n['label_was'], n['label'])
    for st in P['bus']['stops']:
        if 'ימינה בלבד' in (st.get('name') or '') and 'J18_16' in json.dumps(st): st['name_was'] = st['name']; st['name'] = st['name'].replace(' (ימינה בלבד)', '').replace('ימינה בלבד', 'רמזור')
    # the dead ends of the villas' streets — where the game has them
    for nid in ('E31_23', 'E39_19'):
        n = MN[nid]; g = NB[nid]
        if (n['x'], n['y']) != (g['x'], g['y']):
            n['at_was'] = [n['x'], n['y']]; n['x'], n['y'] = g['x'], g['y']
            for s in P['segments']:
                for k in (0, -1):
                    if s['pts'][k] == n['at_was']: s['pts'][k] = [g['x'], g['y']]; s['len_m'] = round(sum(math.hypot(s['pts'][i + 1][0] - s['pts'][i][0], s['pts'][i + 1][1] - s['pts'][i][1]) for i in range(len(s['pts']) - 1)) / 10, 1)
    # שדרת הקריה (A3): the network road ends at A3W (60, 2550), as in the game; the leg north at x 115 is the aisle of the car park A3-P
    for r in P['site_roads']:
        if r['id'] == 'A3-SPORTS-RD' and r['pts'][-1] != [60, 2550]:
            r['pts_was'] = r['pts']; r['pts'] = [r['pts'][0], [60, 2550]]; r['draw_was'] = r.get('draw'); r['draw'] = [r['draw'][0], [60, 2550]]
            r['label'] = 'שדרת הקריה — מהכיכר מערבה עד הכניסה לחניון של קריית הספורט (A3W)'
            P['site_roads'].append(dict(id='A3-P-AISLE', zone='A3', kind='site', cls='service', lanes='1+1', hw=30, pts=[[115, 2482], [115, 1760]], draw=[[115, 2482], [115, 1760]],
                                        label='המעבר של החניון של קריית הספורט (A3-P) — בתוך החניון, לא דרך', road=None, via='A3-SPORTS-RD', oneway=False, r9s=True))
    # the crosswalks: the west arm of the sports roundabout; the arm of רחוב השכונה at J18_16, and at J385_42, where the game has them
    XW = P['bus']['crosswalks']
    if not any(c['node'] == 'J12_25' and c['seg'] == 'A3-SPORTS-RD' for c in XW):
        XW.append(dict(node='J12_25', seg='A3-SPORTS-RD', d0=180, d1=220, at=[1200, 2550], u=[-1.0, 0.0], cw=78.0, r9s=True,
                       why='סבב 9ס (R-86): מעבר בכל ארבע הזרועות של כיכר הספורט — הזרוע המערבית (שדרת הקריה), כמו במשחק (200 פיקסלים ממרכז הכיכר)'))
    for c in XW:
        if c['node'] == 'J12_25' and c['seg'] == 'CL-W/3':
            c['game'] = 'אין — רחבת היציאה של הכבאיות של A4 מתחילה 12 מ׳ ממרכז הכיכר (RB2.noXw)'; c['fix'] = 'המשחק — לסוף S9a (' + ASK + ')'
        if c['node'] == 'J18_16' and c['seg'] == 'LC-B/1' and c['d0'] != 65:
            c['d_was'] = [c['d0'], c['d1']]; c['d0'], c['d1'] = 65, 105; c['r9s'] = True
            c['why'] = 'סבב 9ס (R-86): צמוד לקו העצירה — 8.5 מ׳ מהצומת, כמו במשחק (היה 14 מ׳)'
        if c['node'] == 'J385_42' and c['seg'] == 'AR-S/3':
            g = next(q for q in G['xw'] if q['id'] == 'XW-J385_42-AR-S3'); m = abs(g['x'] - c['at'][0])
            c['d_was'] = [c['d0'], c['d1']]; c['d0'], c['d1'] = round(m - 20), round(m + 20); c['r9s'] = True
    log('ג.2', 'J18_25', 'במפה היה "עצור / זכות קדימה" — עכשיו רמזור, כמו במשחק (הבעלים 3.11 11:30: "כל הצמתים עם רמזור"); רחוב בית הספר — לפי דרישה.')
    log('ג.2', 'J18_16 ו-J31_42', 'השם אמר "(ימינה בלבד)" והפירוט — נתיב שמאלה עם חץ. במשחק שניהם ברמזור עם פנייה שמאלה, ולכן הפירוט נכון והשם תוקן; גם ST-03. ' + ASK + '.')
    log('ג.2', 'D4B ו-D5-C2', 'החיבורים הזמניים של המפה (TMP-S5-3, ‏TMP-S6-4) — בטבלת ההתאמה כחריג זמני, עד S9b; ב-D4B מעבר אחד מתוך שלושה (R-81).')
    log('ג.3', 'כיכר הספורט (J12_25)', 'נוסף במפה המעבר בזרוע המערבית (שדרת הקריה), כמו במשחק. בזרוע הדרומית יש במפה מעבר ובמשחק אין — רחבת היציאה של הכבאיות; '
        'מי מתקן: המשחק — לסוף S9a (' + ASK + ': או חריג רשום לפי D‑427).')
    log('ג.3', 'J18_16 — זרוע רחוב השכונה', 'המעבר במפה זז ל-8.5 מ׳ מהצומת, צמוד לקו העצירה, כמו במשחק (היה 14 מ׳).')
    log('ג.3', 'המסוף E3', '4 המעברים לנוסעים בין האיים (D‑423, ‏TX-A-N, ‏TX-A-E, ‏TX-B-S, ‏TX-B-E) — במפה, ובמשחק אין אף אחד; מי מתקן: המשחק — לסוף S9a (להוסיף לשורה 89).')
    log('ג.5', 'התחנות — האזור שרשום בתחנה', 'בשש תחנות במשחק (BUS1-A3, ‏BUS1-B3, ‏BUS1-D2S, ‏BUS2-C3R, ‏BUS2-C5, ‏BUS2-D5) האזור הרשום אינו האזור שבו התחנה עומדת. '
        'ברירת המחדל (' + ASK + '): השדה של האזור — האזור שבו התחנה עומדת; האזור שהיא משרתת — בשדה נפרד, כדי שהבדיקות והפרטים החיים לא יספרו אותה באזור הלא נכון. '
        'מי מתקן: המשחק — לסוף S9a, עם התחנות של המפה. 14 מפרצים של המפה באזורים בנויים עוד לא במשחק — בטבלת ההתאמה; ‏ST-11 נבדק מול D2 החדש: המפרצים על שדרת השדה, מחוץ למגרשים ולפתחים.')
    log('ג.4', 'לולאת האמבולנסים (A2)', 'נמדד מול המשחק: הנתיב של המפה (x ‏1085, ‏y ‏1240–1400) בתוך הנתיב של המשחק (x ‏1066–1110) — 0.3 מ׳; ההפרש של כ-10 מ׳ שבביקורת לא נמצא. בלי שינוי.')
    log('ג.4', 'E4 ו-E5 — הדרכים הישנות', 'הדרכים הפנימיות הישנות שבמשחק ואינן במפה — בטבלת ההתאמה, בכיוון משחק ← מפה, עם "ייצא / ייבנה עם S9".')
    log('ג.4', 'שדרת הקריה (A3)', 'במפה הדרך המשיכה צפונה ב-x ‏115 אל החניון (79 מ׳). במשחק היא נגמרת ב-A3W (60, 2550), והקטע הצפוני הוא המעבר של החניון A3-P. המפה תוקנה כמו המשחק.')
    log('ג.4', 'קצות רחוב הווילות וסמטת הווילות', 'E31_23 ו-E39_19 זזו 10.9 ו-9 מ׳ — למקום של מעגלי הסיבוב במשחק.')


# ====================================================================== 7 · the stages of every zone (16:40 ב.4, ג; 17:45 ג.7–8)
S14_SEA = ['G4', 'H4', 'G5', 'H5']; S13_SEA = ['G6', 'H6', 'H7', 'E8']; S15_16 = ['G2', 'G3', 'H3']
def d_stages(P):
    Z = json.load(open(PLAN_NEW, encoding='utf-8'))['zoneSync']['zones']
    PS = {z: v['stage'] for z, v in Z.items()}
    for z in S14_SEA: PS[z] = 'S14'
    for z in S13_SEA: PS[z] = 'S13'
    for z in S15_16: PS[z] = 'S15–S16'
    P['zone_stage'] = PS
    P['zone_stage_why'] = {**{z: 'ים פתוח — גלים, נתיב האוניות והמצופים (R-83; ' + ASK + ')' for z in S14_SEA},
                           **{z: 'S13, כמו בתוכנית (R-86 ג.7)' for z in S13_SEA},
                           'G2': 'S15 — הצד האווירי; S16 — חניון הצוות (D‑464, לפי התוכן; ' + ASK + ')',
                           'G3': 'S15 — המנחתים, העמדות המרוחקות והרצת המנועים; S16 — החניון הארוך וההשכרה (D‑160, ‏D‑464; ' + ASK + ')',
                           'H3': 'S15 — הצד האווירי; S16 — צד היבשה: החניון הארוך וההשכרה עם G3 (D‑160, ‏D‑464; ' + ASK + ')'}
    have = {t['stage'] for t in P['transition']['stages']}
    WHAT = {'S14': 'הים — האוניות, הסירות והדיג (D‑463), והים הפתוח במזרח: G4, ‏H4, ‏G5 (המשך נתיב האוניות) ו-H5 — גלים, נתיב האוניות והמצופים (' + ASK + ')',
            'S15': 'השדה, הצד האווירי (D‑464): המסלולים, המנחתים, העמדות המרוחקות והרצת המנועים; הטרמינל ב-F2',
            'S16': 'השדה, צד היבשה (D‑464): החזית של F2, החניון הארוך, ההשכרה וחניון הצוות; קו 4 עד חזית הטרמינל (R-84); בסוף — השחקן בשדה'}
    for s in ('S14', 'S15', 'S16'):
        zs = sorted(z for z, v in PS.items() if v == s or (v == 'S15–S16' and s in ('S15', 'S16')))
        if s not in have:
            P['transition']['stages'].append(dict(stage=s, zones=zs, why=WHAT[s], new_segments=[], removed=[], temp_added=[], temp_removed=[], dead_ends=[], joins=[], pieces=1, r9s=True))
    for t in P['transition']['stages']:
        if t['stage'] == 'S13':
            for z in S13_SEA:
                if z not in t['zones']: t['zones'].append(z)
    for z in S14_SEA + S13_SEA + S15_16:
        P['zones'].setdefault(z, {})['stage'] = PS[z]
    log('ג.7', 'אזורים בלי שלב', 'G4, ‏H4, ‏G5 ו-H5 → S14 (ים פתוח; ' + ASK + '); ‏G6, ‏H6, ‏H7 ו-E8 → S13, כמו בתוכנית. כל 80 האזורים עם שלב בריחוף, בשכבת השלבים ובטבלה.')
    log('ז.4', 'S14–S16 מול התוכנית', 'השלבים מטבלת האזורים של התוכנית, ו-G2, ‏G3 ו-H3 בשני השלבים — S15 לצד האווירי ו-S16 לצד היבשה, לפי התוכן (D‑464; ' + ASK + '; לסנכרן עם סוכן התוכנית).')
    log('ג.8', 'ציורי השלבים', 'נוספו הציורים של S14, ‏S15 ו-S16 בפרק "המעבר — אזור אחרי אזור".')
    return PS


# ====================================================================== 8 · the status of every lot — from the game and the stages (R-86 ג.1)
def lot_status(P, rows, PS, BZ):
    ZB = {'B4': 'S7F182', 'B3': 'S7F186', 'A3': 'S7F190', 'A4': 'S7F190', 'C3': 'S7F187', 'D3': 'S7F190', 'C4': 'S7F194', 'D4': 'S7F194', 'C5': 'S7F220', 'D5': 'S7F220',
          'A5': 'S7F232', 'B5': 'S7F242', 'A2': 'S7F248', 'B2': 'S7F252', 'C2': 'S7F256', 'D2': 'S7F264', 'E3': 'S7F265'}
    seen = {r['map']: r for r in rows if r['kind'] == 'lot' and r['dir'] == 'map→game'}
    n = dict(built=0, missing=0, future=0, isl=0, r7=0)
    def stage_of(l):
        s = PS.get(l.get('zone'), '—')
        return s
    for coll, items in (('lots', P['lots']), ('sites', P['sites']), ('r7', P['r7']['items']), ('island', P['island']['lots']), ('r9s', P.get('r9s_lots', []))):
        for l in items:
            if (l.get('status') or {}).get('state') in ('הוחלף', 'בוטל', 'קיים'):
                if l['status']['state'] == 'קיים': n['built'] += 1
                continue
            z = l.get('zone'); s = stage_of(l)
            was = 'שלב 12' if coll == 'island' else ('סבב 7' if coll == 'r7' else ('עתידי' if l.get('future') else None))
            if z in BZ:
                r = seen.get(l['id'])
                if r and r['ok']:
                    l['status'] = status('קיים', s, ZB.get(z), src='המשחק'); l['future'] = False; n['built'] += 1
                elif r:
                    l['status'] = status('קיים באזור — לא כמו במפה', s, ZB.get(z), by=r['note'][:160], src='טבלת ההתאמה'); l['future'] = False; n['missing'] += 1
                else:
                    l['status'] = status('קיים', s, ZB.get(z), src='האזור נבנה'); l['future'] = False; n['built'] += 1
            else:
                l['status'] = status('עתידי', s, src='טבלת השלבים'); n['future'] += 1
            if was: l['status']['was'] = was
            if coll == 'island': n['isl'] += 1
            if coll == 'r7': n['r7'] += 1
    log('ג.1', 'הסטטוס של המגרשים', f"נגזר מהמשחק ומטבלת השלבים, לא ביד: {n['built']} קיימים (נבנו), {n['missing']} באזור שנבנה אבל לא כמו במפה (בטבלת ההתאמה, עם הסבר), "
        f"{n['future']} עתידיים עם השלב שלהם. {n['isl']} המגרשים באי — S13 (היה \"שלב 12\"); {n['r7']} הפריטים של סבב 7 — עם הסטטוס והשלב שלהם (היה \"סבב 7\").")
    return n


# ====================================================================== 9 · the lines — "today" from the game, "planned" by D‑460 (16:40 ז.3; 17:45 א, ג.6)
D460 = {'1': (6.3, 1, 14), '2': (5.2, 1.5, 4), '3': (4.5, 1.25, 8), '4': (2.9, 1, 3), '5': (8.6, 1.25, 7), '6': (8, 1, 8)}
def game_lines(G):
    NB = {n['id']: n for n in G['nodes']}; EB = {e['id']: e for e in G['edges']}
    out = {}
    for l in map(str, G['BUS_LINES']):
        rt = G['routes'].get(l) or G['routes'].get(int(l)) or []
        zs = []; L = 0
        for st in rt:
            e = EB.get(st.get('edgeId'))
            if not e: continue
            a, b = NB[e['a']], NB[e['b']]
            if st.get('dirSign', 1) < 0: a, b = b, a
            L += math.hypot(b['x'] - a['x'], b['y'] - a['y'])
            for t in (0.25, 0.75):
                z = MT.zone_of(a['x'] + (b['x'] - a['x']) * t, a['y'] + (b['y'] - a['y']) * t)
                if not zs or zs[-1] != z: zs.append(z)
        ustops = [s for s in G['stops'] if str(s.get('line')) == l]
        uturn = any(rt[i].get('edgeId') == rt[i + 1].get('edgeId') for i in range(len(rt) - 1))
        out[l] = dict(zones=zs, len_km=round(L / 10000, 2), stops=[s['id'] for s in ustops], buses=sum(1 for _ in []), uturn=uturn, edges=[s.get('edgeId') for s in rt])
    return out

def d_lines(P, G):
    GL = game_lines(G); P['lines_today'] = dict(build=BUILD, buses_in_service=G.get('busVehicles', 0), lines=GL,
                                                src='המסלולים שבקוד המשחק — נגזר בסקריפט, לא ביד', text_game=read_line_info())
    for l in P['routes']['bus']:
        r, h, b = D460[l['id']]; l['d460'] = dict(round_min=r, every_min=h, buses=b)
    l4 = next(l for l in P['routes']['bus'] if l['id'] == '4')
    l4['ends_was'] = l4.get('ends'); l4['why_was'] = l4['why']
    l4['ends'] = [['AP1', 'שער הנוסעים — ב-S16 הקו ממשיך עד חזית הטרמינל']]
    l4['why'] = ('קו השדה (R-84): לא מופעל עד S16, כי הכבישים שלו בשדה עוד לא מוכנים (הכלל של הבעלים 5.11 08:36: "קו שיש לו את כל הכבישים שלו מוכנים — אפשר להפעיל"). '
                 'ב-S16 הוא נבנה עד חזית הטרמינל, עם מפרצים לאוטובוס של 13.5 מ׳ ובלי פרסה. עד אז שלושת האוטובוסים שלו (D‑460) ברזרבה. '
                 'היום במשחק: מהמסוף צפונה עד AIR-W0 ופרסה חזרה — אין לו יעד שקווים 1 ו-2 לא מגיעים אליו.')
    l4['len_note'] = f"{l4['len_km']} ק״מ — רק החלק שבעיר, מהמסוף עד שער השדה (AP1); ההמשך בשדה — ב-S16"
    for st in P['bus']['stops']:
        if st['id'] == 'ST-20': st['name_was'] = st.get('name'); st['name'] = 'שער הנוסעים — ב-S16: מפרצי החזית של הטרמינל, לאוטובוס של 13.5 מ׳'
    log('א', 'קו 4 — מה כתוב במפה', 'במקום "כמו היום" ו"חבילה 7ח": קו השדה לא מופעל עד S16; ב-S16 — עד חזית הטרמינל, מפרצים ל-13.5 מ׳, בלי פרסה; 3 אוטובוסים ברזרבה (D‑460). '
        f"האורך במפה — {l4['len_km']} ק״מ בעיר בלבד (עד AP1), ובמשחק היום {GL.get('4', {}).get('len_km', '—')} ק״מ (פרסה ב-AIR-W0). גם ST-20 תוקן.")
    log('ז.3', 'טבלת הקווים — "היום"', 'נגזרת בסקריפט מהמסלולים שבקוד המשחק, לא ביד: לכל קו — האזורים, האורך והתחנות; 0 אוטובוסים בשירות (הקווים מושהים). "המתוכנן" — לפי D‑460.')
    return GL

def read_line_info():
    try:
        s = open(os.path.join(W, 'src_game', 'parts', '056_E3_D3_F2.js'), encoding='utf-8').read()
        m = re.search(r"const BUS_LINE_INFO=\{(.*?)\};", s, re.S)
        return {k: v for k, v in re.findall(r"(\d):\['[^']*','([^']*)'", m.group(1))} if m else {}
    except Exception: return {}


# ====================================================================== 10 · the notes of the matching table (explanations, and who fixes)
def notes(P):
    X = {}
    F_MAP, F_GAME, F_ASK = MT.FIX_MAP, MT.FIX_GAME, MT.FIX_ASK
    X[('segment', 'CL-AC/2')] = 'במשחק D2-COM-E הוא רחוב מקומי (9.6 מ׳); במפה מאסף 1+1 — קטע של 20 מ׳ אל שער המטען של השדה (AP2)'
    X[('segment-fix', 'CL-AC/2')] = F_ASK + ' — ברירת המחדל: המשחק בסוג של המפה, עם השער ב-S16'
    X[('segment', 'DW-B5-SVC')] = 'במשחק — שביל מרוצף צר לאורך הקמפוס; במפה — שביל השירות והכיבוי (נתיב אחד)'
    X[('segment-fix', 'DW-B5-SVC')] = F_ASK + ' — ברירת המחדל: המשחק מרחיב לשביל שירות וכיבוי, כמו במפה (כלל 31)'
    for k in ('D3-V1-IN', 'D3-V4-IN', 'C3-PH-GATE'):
        X[('driveway', k)] = 'הכניסה של הווילה מסמטה פנימית (לא מהרשת) — במשחק הסמטה היא חלק מהגינון של האזור'; X[('driveway-fix', k)] = F_ASK
    X[('junction', 'J06_42')] = 'במפה רמזור (הכלל "רמזור בכל צומת"), במשחק בלי רמזור ועם מעברי זברה — הצומת על הגבול של A6, שנבנה ב-S11'
    X[('junction-fix', 'J06_42')] = F_ASK + ' — ברירת המחדל: הרמזור של המפה, במשחק עם A6 (S11)'
    X[('game-junction', 'A6-NF')] = 'שער החווה — A6 נבנה ב-S11; במפה הצומת הזה עוד לא קיים'
    X[('game-junction-fix', 'A6-NF')] = 'עם S11'
    for k in ('J12_25·CL-W/3',):
        X[('crosswalk', k)] = 'במשחק אין — רחבת היציאה של הכבאיות של A4 מתחילה 12 מ׳ ממרכז הכיכר'; X[('crosswalk-fix', k)] = F_GAME + ' (' + F_ASK + ': או חריג רשום לפי D‑427)'
    for k, s in (('J12_42·CL-W/5', 'S11 (B6)'), ('J25_42·PT-W/1', 'S10 (C6)'), ('J31_08·LC-N/2', 'S12 (C1)'), ('J31_08·LC-C1/1', 'S12 (C1)'), ('J385_42·PT-M/1', 'S10 (D6)'), ('J06_42·LC-A6/1', 'S11 (A6)')):
        X[('crosswalk', k)] = f'הזרוע באזור שעוד לא נבנה מחדש — {s}'; X[('crosswalk-fix', k)] = 'עם ' + s
    for t in ('TX-A-N', 'TX-A-E', 'TX-B-S', 'TX-B-E'):
        X[('crosswalk', t)] = 'מעבר לנוסעים בתוך המסוף (D‑423) — במשחק אין אף אחד'; X[('crosswalk-fix', t)] = F_GAME + ' (להוסיף לשורה 89)'
    X[('game-crosswalk', 'XW-D4B-E4-IN-S')] = 'D4B — החיבור הזמני TMP-S5-3 (עד S9b); מעבר אחד מתוך שלושה (R-81) — חריג זמני'
    X[('game-crosswalk-fix', 'XW-D4B-E4-IN-S')] = 'חריג זמני — עד S9b'
    X[('game-crosswalk', 'A34D.zebra@516,2550')] = 'מעבר על שדרת הקריה מול האולם (x ‏516) — במפה אין שם צומת; כלל 21: מעבר רק בצומת'
    X[('game-crosswalk-fix', 'A34D.zebra@516,2550')] = F_ASK + ' — ברירת המחדל: המשחק מוציא אותו, או שהמפה מסמנת שם צומת עם השביל של האולם'
    X[('game-crosswalk', 'D3ND.zebra@3899,2450')] = 'המעבר על סמטת הווילות, 10 מ׳ מהצומת עם רחוב המוסכים — המעבר של הרחוב הצדדי בצומת T (D‑439)'
    X[('game-crosswalk-fix', 'D3ND.zebra@3899,2450')] = F_MAP.replace('כבר תוקנה', 'מוסיפה') + ' (' + F_ASK + ')'
    for b, what in (('ST-05/+1', 'ST-05'), ('ST-05/-1', 'ST-05'), ('ST-06/+1', 'ST-06'), ('ST-06/-1', 'ST-06'), ('ST-07/+1', 'ST-07'), ('ST-07/-1', 'ST-07'), ('ST-08/+1', 'ST-08'),
                    ('ST-08/-1', 'ST-08'), ('ST-10/+1', 'ST-10'), ('ST-10/-1', 'ST-10'), ('ST-11/+1', 'ST-11'), ('ST-11/-1', 'ST-11'), ('ST-18/+1', 'ST-18')):
        X[('bay', b)] = 'המפרץ של המפה עוד לא במשחק — "התחנות של המפה" בשורה 89 (A10)' + (' · ST-11 ב-D2: נבדק מול D2 החדש — המפרצים על שדרת השדה מחוץ למגרשים, לא נוגעים בפתחים' if what == 'ST-11' else '')
    for b in ('ST-14/+1', 'ST-14/-1', 'ST-15/+1', 'ST-15/-1'):
        X[('bay', b)] = 'תחנה של קו 5 (המרינה והחוף) — הקו מחכה ל-S13'; X[('bay-fix', b)] = 'עם קו 5 (S13)'
    X[('bay', 'ST-01/-1')] = 'המפרץ צפונה של ST-01: במפה y ‏2114–2344; במשחק התחנה (BUS2-D3C / BUS4-GATE) ב-y ‏2113 — בתחילת המפרץ, 11.6 מ׳ מהאמצע'
    X[('bay-fix', 'ST-01/-1')] = F_GAME + ' — התחנה זזה לאמצע המפרץ עם טלאי הקווים'
    X[('game-bay', 'BUS1-B4')] = 'תחנה של קו 1 ברחוב בית הספר — במפה התחנה של B4 היא ST-18, על שדרת המערב'
    X[('game-bay-fix', 'BUS1-B4')] = F_GAME + ' — יוצאת בטלאי הקווים, כשהקו עובר ל-ST-18'
    for g in ('BUS1-E3', 'BUS2-E3', 'BUS3-E3', 'BUS4-E3'):
        X[('game-bay', g)] = 'מפרץ העלייה של הקו במסוף — במפה 12 המפרצים של המסוף (E3-BUS/1–12); המיקום לפי D‑469'
    X[('lot', 'C5-REFINERY')] = 'חוות המכלים של בית הזיקוק — במשחק המתקן של C5 (S7F220) לא באותו מלבן; הצינור PIPE-REF נכנס אליה (D‑504)'
    X[('lot-fix', 'C5-REFINERY')] = F_ASK + ' — לבדוק עם S7F266 (הצינור)'
    for k in ('C5-WC', 'C5-GATE', 'C5-CAFE', 'C5-SUBSTATION', 'C5-WORKSHOP-YARD', 'C5-TRUCKS', 'C4-DEPOT-YARD', 'D5-DEPOT'):
        X[('lot-fix', k)] = F_ASK + ' — ברירת המחדל: המפה כמו המשחק בסבב הבא, אחרי בדיקה של הגיליון של האזור'
    for k in ('A3-PITCH', 'A3-STAND-N', 'A3-STAND-S', 'A4-FOOT5', 'A4-BASKET', 'A4-TENNIS'):
        X[('lot', k)] = 'במשחק המגרש מצויר בשכבה של קריית הספורט (A34D) — לא כמלבן של מגרש; בדיקה בעין בדף החי'
        X[('lot-fix', k)] = F_ASK
    for g in ('E3-STATION', 'E3-KIOSK', 'E3-WC', 'E3-BUS-TERMINAL'):
        X[('game-lot', g)] = 'מבנה של E3 שבמפה הוא חלק מהתחנה או מהמסוף, בלי מגרש משלו'; X[('game-lot-fix', g)] = F_MAP.replace('כבר תוקנה', '— בסבב הבא (מגרש לכל מבנה)')
    for k in range(1, 13):
        X[('bay', f'E3-BUS/{k}')] = 'המסוף: 12 מפרצים במפה (6 לעלייה, 6 לחניה גב אל גב — D‑469); במשחק מפרץ עלייה אחד לכל קו (BUS1–4-E3)'
        X[('bay-fix', f'E3-BUS/{k}')] = F_GAME + ' — מנוע המסוף ו-15 האוטובוסים בלילה (שורה 89)'
    X[('game-lot', 'B2-PIER')] = 'מזח הדיג הישן (WF-07) — במפה ברשימה של מה שנשאר על חוף האגם (בנתוני האגם של המפה); לפי הביקורת במשחק שלושה מזחים — לבדוק אם הוא עוד מצויר'
    X[('game-lot-fix', 'B2-PIER')] = F_ASK
    X[('game-lot', 'E3-PB')] = 'E3-PB — ‏15 חניות (לאישורך); במפה המגרש של 20 — הגבול זז עם מחסן החבילות (S9b)'; X[('game-lot-fix', 'E3-PB')] = F_ASK
    X[('game-lot', 'A4-FIRE')] = 'תחנת הכיבוי — במפה המגרש A4-FIRE ודרך הצוות A4-CREW-WAY; 5.4 מ׳ בין הקווים'; X[('game-lot-fix', 'A4-FIRE')] = F_ASK
    X[('game-segment', 'TMP-S6-4')] = 'החיבור הזמני TMP-S6-4 של המפה (שער הנמל העתידי ב-E5) — יוצא ב-S9b'
    return X


def main():
    os.chdir(HERE)
    P, H = start()
    G = json.load(open(os.path.join(HERE, 'game_s7f265.json'), encoding='utf-8'))
    assert G['BUILD'].endswith(('s7f265', 's7f266')), G['BUILD']   # 8.11: S7F266 (הרציפים, העקיפה והצינור) — אותה רשת
    d_version(P); d_d2(P, G); d_lake(P, G); d_s9a(P, G); d_owner(P); d_net(P, G)
    PS = d_stages(P); GL = d_lines(P, G)
    rows, BZ = MT.match(P, G, notes(P))
    n = lot_status(P, rows, PS, BZ)
    rows, BZ = MT.match(P, G, notes(P))          # again, with the statuses (a replaced lot is a row of its own)
    import r9s_page as PG
    H2, info = PG.page(H, P, G, rows, BZ, PS, GL, LOG)
    T = table_json(P, G, rows, BZ)
    P['r9s'] = dict(at=DATE, by='סוכן המפה', build=BUILD, log=LOG, counts=T['counts'])
    json.dump(P, open(os.path.join(HERE, 'city_plan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(HERE, 'city_plan.html'), 'w', encoding='utf-8').write(H2)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'Turbo_City_Roads_9s.html'), 'w', encoding='utf-8').write(H2)
    json.dump(T, open(os.path.join(OUT, 'map_vs_game_9s.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('r9s', T['counts']['total'], 'rows ·', T['counts']['bad'], 'not matching ·', info)


def table_json(P, G, rows, BZ):
    from collections import Counter
    c = Counter((r['kind'], r['dir'], r['ok']) for r in rows)
    cnt = dict(total=len(rows), bad=sum(1 for r in rows if not r['ok']),
               by_kind={f'{k}·{d}': dict(ok=c[(k, d, True)], bad=c[(k, d, False)]) for k, d in sorted({(k, d) for k, d, _ in c})},
               by_fix=dict(Counter(r['fix'] for r in rows if not r['ok'])))
    return dict(id='map_vs_game_9s', title=f'טבלת ההתאמה — מפת הדרכים סבב {VERSION} מול המשחק {BUILD}', at=DATE,
                map=dict(file='study/roads/city_plan.json', version=VERSION), game=dict(build=BUILD, sha1=BUILD_SHA, file='clean_r2b_025637/out/_rebuild_S7F265.html', title=G.get('title')),
                rule='מרחק של יותר מ-4.5 מ׳ — לא תואם, עם הסבר ועם "מי מתקן" (המפה כבר תוקנה / המשחק — לסוף S9a / לאישורך)',
                built_zones=BZ + ['וגם הקטעים של S9a מחוץ ל-E3: ' + ', '.join(S9A_BUILT)],
                fields=dict(kind=dict(lot='מגרש', segment='קטע דרך', driveway='פתח — כניסה למגרש', junction='צומת, עם סוג השליטה', crosswalk='מעבר חצייה', bay='מפרץ תחנה'),
                            dir={'map→game': 'מה שבמפה, ומה מולו במשחק', 'game→map': 'מה שבמשחק, ומה מולו במפה'}, dist_m='המרחק במטרים', ok='תואם', fix='מי מתקן', note='הסבר'),
                counts=cnt, rows=rows)


if __name__ == '__main__':
    main()
