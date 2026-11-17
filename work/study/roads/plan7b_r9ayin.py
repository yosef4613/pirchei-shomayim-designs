# -*- coding: utf-8 -*-
"""8.11 · סבב 9ע של מפת הדרכים — S9 כולו כמו שנבנה: S7F267 (סוף S9a — המפרצים והמעברים במסוף), S7F268 (E4, ‏E5), ‏S7F269 (F3, ‏F4), ‏S7F270 (F5, ‏F6).
הבסיס: הפלט של סבב 9ס כמו שהוא (על S7F266) — עותק שלו ב-W/_to_delete/roads_before_r9ayin, וכל הרצה מתחילה ממנו מחדש.
  1. שליפה חוזרת מהמשחק S7F270 (probe_s7f270.js → game_s7f270.json): הרשת, התחנות של הקווים ושל המפה, מעברי המסוף, רשת המסילות, המבנים של S9.
  2. סטטוס "קיים — S9, ‏S7F26N" לכל מגרש, מבנה, דרך, מסילה, תחנה ומפרץ שנבנו; מה שהבונים שינו מהמפה — המפה כמו המשחק, עם "לאישורך".
  3. ציור לכל אזור של S9 כמו שנבנה, שורת "מעודכן עד: S7F270 · סבב 9ע" בכל ציור, וטבלת ההתאמה מחדש (map_vs_game_9ayin.json).
  4. ההצעה למעבר פסים מ-B ל-A בין E3 לתחנת החוף, לרכבת הנוסעים של 4 קרונות (ברירת מחדל, לאישורך).
    python3 plan7b_r9ayin.py → city_plan.json, city_plan.html, deliver/2026-11-08/map/Turbo_City_Roads_9ayin.html, map_vs_game_9ayin.json"""
import json, os, sys, shutil, math, re, html, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
W = os.path.dirname(os.path.dirname(HERE))
E = html.escape
import r9s_match as MT
import plan7b_r9s as R9S
import r9s_page as PG

VERSION = '9ע'; DATE = '8.11.2026'; BUILD = 'S7F270'; BUILD_SHA = 'adea776b78dc'
GAME = 'clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F270.html'
BACK = os.path.join(W, '_to_delete', 'roads_before_r9ayin')
OUT = os.path.join(W, 'deliver', '2026-11-08', 'map')
ZB = {'E4': 'S7F268', 'E5': 'S7F268', 'F3': 'S7F269', 'F4': 'S7F269', 'F5': 'S7F270', 'F6': 'S7F270'}
S9Z = ['E3', 'E4', 'E5', 'F3', 'F4', 'F5', 'F6']
ASK = 'לאישורך'
LOG = []
def log(sec, item, what): LOG.append(dict(sec=sec, item=item, what=what))
st = R9S.status


def start():
    os.makedirs(BACK, exist_ok=True)
    for f in R9S.FILES:
        b = os.path.join(BACK, f)
        if not os.path.exists(b): shutil.copyfile(os.path.join(HERE, f), b)
    P = json.load(open(os.path.join(BACK, 'city_plan.json'), encoding='utf-8')); H = open(os.path.join(BACK, 'city_plan.html'), encoding='utf-8').read()
    assert P['version'] == '9ס' and "<a id='r9s'></a>" in H, 'the copy is not the output of 9ס'
    return P, H


def d_version(P):
    P['version_was'] = P['version']; P['version'] = VERSION; P['batch'] = VERSION; P['at'] = DATE
    P['title'] = f'תוכנית הדרכים של כל העיר — סבב {VERSION}'
    P['synced_with'] = dict(build=BUILD, sha1=BUILD_SHA, file=GAME, probe='study/roads/probe_s7f270.js', date=DATE)
    P['updated_until'] = f'{BUILD} · סבב {VERSION} · {DATE}'
    log('הגרסה', 'שדה הגרסה', f'"{VERSION}" — מזין את כותרת הדף, את הכותרת הראשית, את שורת הסבב ואת טבלת הסבבים; מסונכרן עם {BUILD} ‏({BUILD_SHA}).')


def game_items(G):
    """the built things of S9 in the game: the buildings (with the lot of the map they stand on), the car parks, the entries, the decks, the solar field, the buoys"""
    out = []
    for k in ('E4_BUILDINGS', 'E5_BUILDINGS', 'F34_BUILDINGS'):
        for b in G.get(k) or []:
            q = b.get('s9') or {}
            if isinstance(q.get('rect'), list):
                out.append(dict(id=b['id'], zone=q.get('zone') or MT.zone_of(*q['rect'][:2]), kind='building', label=b['label'].split(' — ')[0], rect=q['rect'], lot=q.get('lot')))
    lots = {}
    for k in ('E4_STALLS', 'F34_STALLS', 'E4_TRUCK_STALLS'):
        for b in G.get(k) or []:
            r = MT.rect_of(b)
            if r and b.get('lot'):
                o = lots.setdefault(b['lot'], dict(r=list(r), n=0)); o['n'] += 1; o['r'] = [min(o['r'][0], r[0]), min(o['r'][1], r[1]), max(o['r'][2], r[2]), max(o['r'][3], r[3])]
    for i, o in lots.items():
        out.append(dict(id=i, zone=MT.zone_of((o['r'][0] + o['r'][2]) / 2, (o['r'][1] + o['r'][3]) / 2), kind='parking', label=f'חניון {i} — {o["n"]} מקומות', rect=o['r']))
    for k in ('E4_ACCESS', 'F34_ACCESS'):
        for b in G.get(k) or []:
            r = MT.rect_of(b)
            if r: out.append(dict(id=b['id'], zone=MT.zone_of(*r[:2]), kind='entry', label=b.get('label', ''), rect=r))
    sol = MT.rect_of((G.get('E4_SOLAR') or {}).get('panels'))
    if sol: out.append(dict(id='E4-SOLAR-PANELS', zone='E4', kind='solar', label='השדה הסולרי (LIKE-01) — 3.6 מ׳ מערבה מהמפרט', rect=sol))
    dt = MT.rect_of(G.get('E5_DEPOT_TRACKS'))
    if dt: out.append(dict(id='E5-DEPOT-TRACKS', zone='E5', kind='rail', label='פסי מוסך הרכבות', rect=dt))
    for i, r in enumerate((G.get('F34_DECKS') or []) + (G.get('F56_DECKS') or [])):
        r = MT.rect_of(r)
        if r: out.append(dict(id=f'DECK-{i + 1}', zone=MT.zone_of((r[0] + r[2]) / 2, (r[1] + r[3]) / 2), kind='deck', label='דק — טיילת, מזח או מרפסת', rect=r))
    bo = MT.rect_of(G.get('F56_BOOTH'))
    if bo: out.append(dict(id='F6-BOOTH', zone='F6', kind='building', label='ביתן השומר ברחבת ראש הגשר', rect=bo))
    for b in G.get('F56_BUOYS') or []:
        out.append(dict(id=b['id'], zone=b.get('zone') or MT.zone_of(b['x'], b['y']), kind='buoy', label=('מצוף אדום' if b.get('color') == 'red' else 'מצוף ירוק') + f" {b['id']}",
                        rect=[b['x'] - 12, b['y'] - 12, b['x'] + 12, b['y'] + 12], moved=(b.get('spec') and list(b['spec']) != [b['x'], b['y']])))
    for x in out: x['status'] = st('קיים', 'S9', ZB.get(x['zone'], BUILD), src='המשחק')
    return out


def d_s9(P, G):
    GI = game_items(G); P['r9ayin_lots'] = GI
    by_lot = Counter(x['lot'] for x in GI if x.get('lot'))
    n = Counter()
    for coll in (P['lots'], P['sites'], P['r7']['items']):
        for l in coll:
            z = l.get('zone')
            if z not in ZB: continue
            if l['id'].startswith('BUOY-'):
                l['status'] = st('הוחלף', 'S9', by=f'18 המצופים של נתיב השיט כמו שנבנו ({ZB[z]}) — אדום ב-x ‏6600, ירוק ב-x ‏6950; ' + ASK, src='המשחק'); n['buoy'] += 1; continue
            if l['id'] in ('F3-PIER1', 'F3-PIER2', 'F3-PIER3', 'F3-PIER4', 'F3-FUELD', 'F3-FUELK'):
                l['status'] = st('הוחלף', 'S9', by='המזחים, מזח הדלק והביתן שלו כמו שנבנו ב-S7F269 (ארבעה מזחים, 31 מעגנים) — ' + ASK, src='המשחק'); n['f3'] += 1; continue
            if by_lot.get(l['id']):
                l['status'] = st('קיים', 'S9', ZB[z], src='המשחק'); l['future'] = False; n['lot'] += 1
    for s in P['sites']:
        if s['id'] == 'E4-SOLAR' and not s.get('rect_was'):
            s['rect_was'] = list(s['rect']); s['rect'] = [s['rect'][0] - 36, s['rect'][1], s['rect'][2] - 36, s['rect'][3]]
            s['why'] = (s.get('why') or '') + ' · סבב 9ע: 3.6 מ׳ מערבה, כמו במשחק (S7F268) — כדי לא לגעת ברציף של תחנת החוף; ' + ASK + '.'
    log('S9', 'המגרשים והמבנים', f"{len([x for x in GI if x['kind'] == 'building'])} מבנים, {len([x for x in GI if x['kind'] == 'parking'])} חניונים, "
        f"{len([x for x in GI if x['kind'] == 'entry'])} כניסות, {len([x for x in GI if x['kind'] == 'deck'])} דקים ו-{len([x for x in GI if x['kind'] == 'buoy'])} מצופים — מהמשחק, "
        f"בסטטוס \"קיים — S9\" עם הבנייה (E4, ‏E5 — S7F268; F3, ‏F4 — S7F269; F5, ‏F6 — S7F270). {n['lot']} מגרשים של המפה שהמבנים עומדים עליהם — \"קיים\".")
    T = P['bus']['terminal']['r9']['crossings']; TG = ((G.get('TERM') or {}).get('xw') or [])
    for c, r in zip([c for c in T if c['id'] in ('TX-A-E', 'TX-B-E')], [TG[0], TG[1]] if len(TG) >= 2 else []):
        if c['r'] != r: c['r_was'] = c['r']; c['r'] = list(r)
    log('S9a', 'המעברים במסוף', 'TX-A-E ו-TX-B-E — באורך של המשחק (x ‏5540–5700, ‏X-AE ו-X-BE); ‏TX-A-N ו-TX-B-S — כמו במשחק (X-AN, ‏X-BS, ‏S7F267).')
    log('S9', 'המזחים של המרינה (F3)', f"{n['f3']} הפריטים של המפה (ארבעת המזחים, מזח הדלק והביתן) — \"הוחלף\" בדקים ובמזחים של המשחק: ארבעה מזחים, 31 מעגנים עם מזחי אצבע, מזח הדלק וביתן המשאבה. " + ASK + '.')
    log('S9', 'השדה הסולרי (E4)', '3.6 מ׳ מערבה, כמו במשחק — כדי לא לגעת ברציף של תחנת החוף. ' + ASK + '.')
    log('S9', 'המצופים של נתיב השיט (F4–F6)', f'{n["buoy"]} המצופים של המפה (שני נתיבים, L1 ו-L4) מסומנים "הוחלף": במשחק 18 מצופים — אדום ב-x ‏6600 וירוק ב-x ‏6950, '
        'לפי המפרט של S9; ‏BY-R9 ו-BY-G9 זזו 6 מ׳ צפונה, מעל הגשר של מסילת ההיפוך. ' + ASK + '.')
    log('S9', 'חניון המרינה (F3)', 'P-F3-M — ‏16 מקומות בשתי שורות, והכניסה DW-F3-P מדרך המרינה (CL-F/1), כמו במשחק; לולאת ההורדה של מלון הים והכניסה DW-F3-01.')
    log('S9', 'החניונים של E4', 'P-E4-ST זז 1 מ׳ מזרחה; בחצר המסילה (P-E4-RY) שתי חניות בציור עמדו על נתיב השער — אותן 6, שלוש מכל צד. כמו במשחק; ' + ASK + '.')
    return GI


def d_s9_net(P, G):
    built = 0
    for s in P['segments']:
        z = set(s.get('zones') or [s.get('home')])
        if s.get('stage') == 'S9' and s['id'] not in ('CL-F/2', 'CL-F/3') and (z & set(ZB)) and not s.get('built'):
            s['built'] = ZB.get(s.get('home'), BUILD); s['state'] = 'קיים'; built += 1
        if s['id'] in ('CL-F/2', 'CL-F/3'):
            s['today'] = ('לא נבנה ב-S7F269: הצד הצפוני של העורק (y ‏1760) נכנס 3.8 מ׳ לחניון של השדה ב-F2, והחיבור ל-AIR-S מחבר את העיר לרשת השדה, שסגורה עד S16. '
                          'דרך המרינה נשארת עם המחסום ב-K61_176 — ' + ASK + ' (ברירת המחדל: עם S16)')
    for r in P['air']['roads']:
        if r['id'] in ('AIR-ACCESS', 'AIR-CONN', 'AIR-SOUTH'): r['today'] = 'לא נבנה ב-S9 — עם S16 (' + ASK + ')'
    for t in P['transition']['stages']:
        for x in t.get('temp_added', []):
            if x['id'] == 'TMP-S6-4': x['removed_in'] = 'S7F268'; x['today'] = 'יצא ב-S7F268, עם הדרכים הישנות של E5; D5-C2 היא נקודה על שדרת המזרח'
    log('S9', 'הדרכים', f'{built} קטעים של S9 — "קיים", עם הבנייה. הדרכים הישנות של E4 ו-E5 (13 צמתים ו-17 קטעים) והחיבור הזמני TMP-S6-4 יצאו מהמשחק (S7F268) — '
        'כמו במפה. ‏CL-F/2, ‏CL-F/3 והדרכים של השדה (AIR-ACCESS, ‏AIR-CONN, ‏AIR-SOUTH) לא נבנו — עם S16 (' + ASK + '); עד אז המחסום ב-K61_176.')


def d_s9_rails(P, G):
    R = {r['id']: r for r in P['rails']}
    by = R['BYPASS']
    for p in by.get('parts', []):
        if p['zone'] == 'E4': p['state'] = 'נבנה ב-S7F268 (D‑503)'; p['what'] = 'ממשיכה מהבולמים של S7F266 דרומה ב-x ‏5978, ומתחברת ל-MAIN-B ב-y ‏2900 בקשת; FRT-4 נוסעת עליה'
    by['state'] = 'קיים — E3: S7F266, ‏E4: S7F268'
    for y in ('Y1', 'Y2', 'Y3', 'Y-LEAD-N', 'Y-LEAD-S', 'Y-X12', 'Y-X23'):
        if y in R: R[y]['state'] = 'קיים'; R[y]['built'] = 'S7F268'
    sd = R['SIDING']; sg = G.get('F56_SIDING') or {}
    sd['state'] = 'נבנה עד גבול F6 (x ‏7200) — S7F270'; sd['stage'] = 'S9 / S13'
    sd['note'] = ('סבב 9ע: המסוט על המסילה המזרחית ב-(6460, 5120), גשר משלה מעל המים, צפון-מזרחה עד y ‏5050 ועד גבול האזור (x ‏7200); שם בולם זמני עם פנס אדום ושלט "ההמשך עם G6". '
                  'עוד לא ברשת המסילות של הסימולציה — אין רכבת שמשתמשת בה עד S16 (' + ASK + ').')
    if isinstance(sg.get('pts'), list): sd['pts_built'] = sg['pts']
    S = {s['id']: s for s in P['stations']}
    S['ST-COAST']['state'] = 'קיים — S9 (S7F268)'; S['ST-COAST']['why'] = 'D‑503 / D‑515: הרציף לכל האורך (y ‏2700–3560) עם גג שקוף לכל אורכו בסגנון LIKE-02, ספסלים, שלטים ותאורה; מעבר מקורה מהרחבה אל האולם ואל הרציף.'
    S['ST-E3']['state'] = 'קיים — הרציפים y ‏1760–2530 (S7F266), הגג השקוף לכל האורך (S7F267, ‏D‑515)'
    # the proposal: a crossover from B to A between E3 and the coast station, for the passenger train of 4 cars (D‑505)
    P['proposals'] = [dict(id='X-BA', kind='xover', state='הצעה — ' + ASK, a=[5900, 2702], b=[5800, 2822],
                           why='רכבת הנוסעים של 4 קרונות (732 פיקסלים) יוצאת מרציף 2 של E3 בפס B, ותחנת החוף נמצאת רק ממערב לפס A. בין סוף הרציפים (y ‏2530) לגשר UX-1 אין מקום, והגשר לא נושא מסוט; '
                               'לכן מעבר מ-B ל-A מיד דרומית לגשר: מסוט על B ב-y ‏2702 ומסוט על A ב-y ‏2822 (120 פיקסלים — כמו X-S, בשיפוע תלול יותר). '
                               'X-S זז 3 מ׳ דרומה (A ב-y ‏2852 → B ב-y ‏3024), כדי ששני המסוטים על A לא ייגעו זה בזה; ‏X-N והעקיפה (B ב-y ‏2900) — בלי שינוי. '
                               'הרכבת עוצרת ברציף של תחנת החוף בין y ‏2826 ל-3558 (נשארים 2 פיקסלים עד סוף הרציף ב-3560).',
                           alt='החלופה: פנים רציף שני לתחנת החוף בצד של B (בין הפסים, כמו רציף 2 של E3) — בלי מעבר, אבל אז X-S ו-X-N צריכים לצאת מתחום התחנה; '
                               'או ש-FRT-1 עוברת לפס B, והרכבת יוצאת מרציף 1 של E3 בפס A.',
                           xs_was=[R['X-S']['pts'][0], R['X-S']['pts'][-1]])]
    log('S9', 'המסילות', 'מסילת העקיפה — E3: ‏S7F266, ‏E4: ‏S7F268 (ל-MAIN-B ב-y ‏2900). תחנת החוף — "קיים" (S7F268), עם הגג השקוף. חצר הרכבות (Y1–Y3, הכניסות והמסוטים) — S7F268. '
        'מסילת ההיפוך (SIDING-F6) — עד x ‏7200 עם בולם זמני (S7F270); ההמשך עם G6 (S13); עוד לא ברשת של הסימולציה (' + ASK + ').')
    log('התלבטויות', 'מעבר פסים מ-B ל-A לרכבת של 4 קרונות', P['proposals'][0]['why'] + ' ' + P['proposals'][0]['alt'] + ' (' + ASK + '.)')


def d_bays(P, G):
    MS = {s['id']: s for s in G.get('S6_MAP_STOPS') or []}
    lines = [s for s in G['stops']]
    log('S9a', 'המפרצים ומעברי המסוף (S7F267)', f'{len(MS)} תחנות מפה במשחק (מפרצים שהקו יגיע אליהם כשיופעל), ובהן ST-09 צפון (S7F268), "המרינה" (S7F269) ו"החוף המזרחי" (S7F270) בשני הצדדים; '
        'ST10-E ו-ST11-W חדשים; ‏ST-01 מזרח, ‏ST-03, ‏ST05-N ו-ST-13 זזו לאמצע המפרץ של המפה. ארבעת המעברים במסוף (X-AE, ‏X-BE, ‏X-AN, ‏X-BS) — במשחק. '
        'הזרוע הדרומית של כיכר הספורט — חריג רשום (D‑427). ‏BUS1-B4 יצאה מקו 1.')
    log('S9a', 'מפרצים שלא נכנסים', 'ST-04 מזרח, ‏ST-11 מזרח, ‏ST-18, ‏ST-05 מערב ו-ST-09 מזרח — אין לאורך הקטע 23 מ׳ פנויים (כלל 24 — מזיזים את התחנה, לא את המפרץ). '
        'ברירת המחדל של הבונה: לשנות את הפריט באזור (שביל, כניסה, רמזור) עם הציור של האזור; עד אז בלי תחנה — ' + ASK + '.')


def d_lines(P, G):
    GL = R9S.game_lines(G); P['lines_today'] = dict(build=BUILD, buses_in_service=G.get('busVehicles', 0), lines=GL, src='המסלולים שבקוד המשחק — נגזר בסקריפט, לא ביד',
                                                    text_game=read_info(G))
    log('הקווים', 'עמודת "היום"', 'נגזרת מחדש מ-S7F270: ' + '; '.join(f"קו {l} — {' → '.join(g['zones'])}" for l, g in GL.items()) +
        '. קו 4 יצא מהקווים שפועלים (D‑520); 0 אוטובוסים בשירות — אף קו לא מוכן לפי R-88 (S7F267).')
    return GL


def read_info(G):
    return {}


def notes(P):
    X = R9S.notes(P)
    F_MAP, F_GAME, F_ASK = MT.FIX_MAP, MT.FIX_GAME, MT.FIX_ASK
    X[('crosswalk', 'J12_25·CL-W/3')] = 'חריג רשום (D‑427, ‏S7F267): רחבת היציאה של הכבאיות של A4 מתחילה 12 מ׳ ממרכז הכיכר'; X[('crosswalk-fix', 'J12_25·CL-W/3')] = 'חריג רשום — ' + F_ASK
    for b, why in (('ST-04/-1', 'ST-04 מזרח'), ('ST-11/+1', 'ST-11 מזרח'), ('ST-11/-1', 'ST-11'), ('ST-18/+1', 'ST-18'), ('ST-05/+1', 'ST-05 מערב'), ('ST-09/-1', 'ST-09 מזרח')):
        X[('bay', b)] = f'{why} — אין לאורך הקטע 23 מ׳ פנויים (S7F267, לאישורך 2): משנים את הפריט באזור עם הציור שלו; עד אז בלי תחנה'; X[('bay-fix', b)] = F_ASK
    for b in ('ST-07/+1', 'ST-07/-1', 'ST-08/+1', 'ST-08/-1'):
        X[('bay', b)] = 'המסילה ב-C6 ו-D6 — המפרץ עם S10 (S7F267)'; X[('bay-fix', b)] = 'עם S10'
    for k in ('E3-BUS/%d' % i for i in range(1, 13)):
        X.pop(('bay', k), None); X.pop(('bay-fix', k), None)
    for t in ('TX-A-N', 'TX-A-E', 'TX-B-S', 'TX-B-E'): X.pop(('crosswalk', t), None); X.pop(('crosswalk-fix', t), None)
    X[('game-lot', 'E3-PB')] = 'E3-PB — ‏15 חניות (לאישורך); במפה המגרש של 20 — הגבול זז עם מחסן החבילות (S9b)'; X[('game-lot-fix', 'E3-PB')] = F_ASK
    X[('segment', 'CL-F/2')] = 'לא נבנה — הצד הצפוני נכנס 3.8 מ׳ לחניון השדה ב-F2'; X[('segment-fix', 'CL-F/2')] = F_ASK + ' — עם S16'
    return X


def lot_status(P, rows):
    seen = {r['map']: r for r in rows if r['kind'] == 'lot' and r['dir'] == 'map→game'}; n = Counter()
    for coll in (P['lots'], P['sites'], P['r7']['items']):
        for l in coll:
            z = l.get('zone')
            if z not in ZB or (l.get('status') or {}).get('state') in ('הוחלף', 'בוטל', 'קיים'): continue
            r = seen.get(l['id'])
            if r and r['ok']: l['status'] = st('קיים', 'S9', ZB[z], src='המשחק'); n['ok'] += 1
            elif r: l['status'] = st('קיים באזור — לא כמו במפה', 'S9', ZB[z], by=r['note'][:160], src='טבלת ההתאמה'); n['bad'] += 1
            else: l['status'] = st('קיים', 'S9', ZB[z], src='האזור נבנה'); n['ok'] += 1
            l['future'] = False
    log('S9', 'הסטטוס של שאר המגרשים', f"{n['ok']} נוספים — \"קיים\"; {n['bad']} באזור שנבנה אבל לא כמו במפה (בטבלת ההתאמה, עם הסבר).")


# ---------------------------------------------------------------------- the page
SFILL = dict(PG.SFILL, entry='#ebebe7', solar='#2f4f7f', rail='#b9b2a3', deck='#c8a97e', buoy='#d0342c')

def page(H, P, G, rows, BZ, PS, GL):
    VER = P['version']; now = time.localtime(); info = {}
    H = re.sub(r"<title>[^<]*</title>", f"<title>מפת הדרכים · סבב {VER}</title>", H, count=1)
    H = re.sub(r"<h1>[^<]*</h1>", f"<h1>{E(P['title'])}</h1>", H, count=1)
    m = re.search(r"<div class='mut'>סבב 9ס · [^<]*?· <span class='small'>", H); assert m
    H = H[:m.start()] + f"<div class='mut'>סבב {E(VER)} · {DATE} · עודכן {now.tm_hour:02d}:{now.tm_min:02d} · מסונכרן עם המשחק {BUILD} · <span class='small'>" + H[m.end():]
    j = H.index("<tr><td><a href='#r9s'>")
    H = H[:j] + (f"<tr><td><a href='#r9ayin'>סבב {E(VER)}</a></td><td class='small'>{now.tm_mday}.{now.tm_mon} {now.tm_hour:02d}:{now.tm_min:02d}</td>"
                 f"<td class='small'>{E('S9 כולו כמו שנבנה (S7F267–S7F270): E4, ‏E5, ‏F3–F6, המסילות, תחנת החוף, המפרצים ומעברי המסוף; המפה כמו המשחק במה שהבונים שינו; ציור לכל אזור של S9; טבלת ההתאמה מחדש; הצעה למעבר פסים מ-B ל-A.')}</td></tr>") + H[j:]
    # the lots layer: the hatch of "future" off what is built in S9; the replaced buoys out; the things of S9 from the game
    a, b = PG.span(H, 'lots'); L = H[a:b]; a7, b7 = PG.span(H, 'r7'); R7 = H[a7:b7]; fut = gone = 0
    for l in P['lots'] + P['r7']['items'] + P['sites']:
        r = l.get('rect')
        if l.get('zone') not in ZB or not (isinstance(r, list) and len(r) == 4 and all(isinstance(t, (int, float)) for t in r)): continue
        s_ = (l.get('status') or {}).get('state', ''); rx = PG.rect_re(l.get('rect_was') or r)
        if s_ == 'הוחלף' or l.get('rect_was'):
            L, k1 = rx.subn('', L); R7, k2 = rx.subn('', R7); gone += k1 + k2
        elif s_.startswith('קיים'):
            fx = re.compile(rx.pattern.replace("[^>]*/>", r"[^>]*class='fut'[^>]*/>")); L, k1 = fx.subn('', L); R7, k2 = fx.subn('', R7); fut += k1 + k2
    for l in P['r7']['items']:
        if l.get('zone') in ZB and (l.get('status') or {}).get('state') == 'הוחלף' and isinstance(l.get('c'), list):
            cx = re.compile(r"<circle cx='%s' cy='%s' r='%s'[^>]*/>" % (re.escape(PG.f1(l['c'][0])), re.escape(PG.f1(l['c'][1])), re.escape(PG.f1(l.get('r', 14)))))
            L, k1 = cx.subn('', L); R7, k2 = cx.subn('', R7); gone += k1 + k2
    o = ["<g id='r9ayin-built'>"]
    for l in P['r9ayin_lots']:
        r = l['rect']; o.append(f"<rect x='{PG.f1(r[0])}' y='{PG.f1(r[1])}' width='{PG.f1(r[2] - r[0])}' height='{PG.f1(r[3] - r[1])}' fill='{SFILL.get(l['kind'], '#d6dade')}' stroke='#556' stroke-width='{4 if l['kind'] == 'building' else 2}'/>")
    for s in P['sites']:
        if s['id'] == 'E4-SOLAR': r = s['rect']; o.append(f"<rect x='{PG.f1(r[0])}' y='{PG.f1(r[1])}' width='{PG.f1(r[2] - r[0])}' height='{PG.f1(r[3] - r[1])}' fill='#c9d6e6' stroke='#2f4f7f' stroke-width='3'/>")
    o.append('</g>')
    L = L[:-4] + ''.join(o) + '</g>'
    H = H[:a7] + R7 + H[b7:]; a, b = PG.span(H, 'lots'); H = H[:a] + L + H[b:]
    info.update(fut_off=fut, out=gone)
    # the siding as built (to x 7200), and the proposal of the crossover — in the rails layer, the proposal dashed
    a, b = PG.span(H, 'rails'); sd = next(r for r in P['rails'] if r['id'] == 'SIDING')
    add = ''
    if sd.get('pts_built'):
        add += f"<polyline points='{' '.join(f'{PG.f1(x)},{PG.f1(y)}' for x, y in sd['pts_built'])}' fill='none' stroke='#3a3a3a' stroke-width='20'/>"
    pr = P['proposals'][0]
    add += (f"<g id='r9ayin-xba'><line x1='{pr['a'][0]}' y1='{pr['a'][1]}' x2='{pr['b'][0]}' y2='{pr['b'][1]}' stroke='#c8372d' stroke-width='16' stroke-dasharray='26 16'/>"
            f"<text x='5690' y='2770' class='r9s' style='text-anchor:end;fill:#c8372d'>X-BA — הצעה ({ASK})</text></g>")
    H = H[:b - 4] + add + H[b - 4:]
    # the hover data: the statuses, the new things, the rails and the stations
    pre = '<script>window.__MAP='; a = H.index(pre) + len(pre); b = H.index(';</script>', a)
    D = json.loads(H[a:b].replace('<\\/', '</')); I = D['info']
    byid = {}
    for coll in (P['lots'], P['sites'], P['r7']['items']):
        for l in coll: byid[l['id']] = l
    def stx(s):
        t = s.get('state', '') + (' — שלב ' + s['stage'] if s.get('stage') else '') + (' (' + s['build'] + ')' if s.get('build') else '')
        return t + (' · ' + s['by'] if s.get('by') and s.get('state') != 'קיים' else '')
    nh = 0
    for k, t in enumerate(I):
        m = re.search(r"<div class='tl'>([A-Z0-9][A-Za-z0-9-]*) · ([A-H][0-9]) · ([^<]*)</div>", t)
        if m and m.group(2) in ZB and byid.get(m.group(1), {}).get('status'):
            I[k] = t[:m.start(3)] + E(stx(byid[m.group(1)]['status'])) + t[m.end(3):]; nh += 1
    for l in P['r9ayin_lots']:
        r = l['rect']; I.append(f"<b>{E(l['label'])}</b><div class='tl'>{E(l['id'])} · {E(l['zone'])} · {E(stx(l['status']))}</div><div class='tl'>סבב 9ע — מהמשחק</div>"); D['lots'].append([r[0], r[1], r[2], r[3], len(I) - 1])
    REP = [("E3 — נבנה ב-S7F266 (D‑503); E4 — עם S9", "קיים — E3: S7F266, ‏E4: S7F268 (D‑503)"), ("עתידי — S9 (D‑503)", "קיים — S9 (S7F268)"),
           ("<b>מסילת ההיפוך של רכבת השדה (חלק ד)</b><div class='tl'>עתידית — S13", "<b>מסילת ההיפוך של רכבת השדה (חלק ד)</b><div class='tl'>נבנתה עד x ‏7200 (S7F270), בולם זמני; ההמשך עם G6 (S13)")]
    for k, t in enumerate(I):
        for x, y in REP: t = t.replace(x, y)
        I[k] = t
    info['hover'] = nh
    H = H[:a] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + H[b:]
    # the tables of the rails and the stations
    cut = H.index("<a id='r9s'></a>")
    A = H[:cut]
    for x, y in REP[:2]: A = A.replace(x, y)
    m = re.search(r"<tr><td class='id'>SIDING</td>.*?</tr>|<tr><td class='id'>[^<]*</td><td>מסילת ההיפוך של רכבת השדה.*?</tr>", A)
    if m: A = A[:m.start()] + m.group(0).replace('עתידית — S13', 'נבנתה עד x ‏7200 (S7F270); ההמשך עם G6 (S13)') + A[m.end():]
    H = A + H[cut:]
    # the lines
    H = PG.lines_tables(H, P, G, GL)
    # "updated until": the lines of 9ס become this round's; the drawings of the section of 9ס are history now
    s9s = H.index("<a id='r9s'></a>"); s9n2 = H.index("<a id='r9n2'></a>")
    old = f"מעודכן עד: S7F266 · סבב 9ס · {DATE}"; new = f"מעודכן עד: {BUILD} · סבב {VER} · {DATE}"
    H = H[:s9s].replace(old, new) + H[s9s:s9n2].replace(old, f"ציור של סבב 9ס — היסטוריה; המצב היום — במפות שלמעלה, מעודכן עד {BUILD} · סבב {VER} · {DATE}") + \
        H[s9n2:].replace("מעודכן עד S7F266 · סבב 9ס", f"מעודכן עד {BUILD} · סבב {VER}")
    # the section of 9ע, before the section of 9ס
    sec = section(P, G, rows, BZ, GL).replace("</svg><b>", f"</svg><div class='upd'>{E(new)}</div><b>")
    info['upd_new'] = sec.count("<div class='upd'>"); info['upd_all'] = H.count(new)
    H = PG.one(H, "<a id='r9s'></a>", sec + "<a id='r9s'></a>")
    return H, info


def section(P, G, rows, BZ, GL):
    VER = P['version']; o = [f"<a id='r9ayin'></a><h2>סבב {VER} — S9 כולו כמו שנבנה (S7F267–S7F270), והמפה מסונכרנת עם המשחק</h2>"]
    o.append("<div class='box'><b>מה ביקשו:</b> המתאם, 8.11 — S9 נבנה כולו: S7F267 (סוף S9a — המפרצים והמעברים במסוף), S7F268 (E4, ‏E5), S7F269 (F3, ‏F4), S7F270 (F5, ‏F6). "
             f"<b>המקור:</b> המשחק {BUILD} ‏({BUILD_SHA}), מורץ בדפדפן (probe_s7f270.js), וההחזרות של הבונים. "
             "<b>הדרכים שהבעלים אישר לא שונו</b> — מה שבנוי מתואר כמו במשחק; מה שהבונים שינו מהמפה — כמו במשחק, עם \"לאישורך\".</div>")
    o.append("<h3>מה נעשה</h3><div class='wrap'><table><tr><th>הנושא</th><th>מה</th><th>מה נעשה</th></tr>" +
             ''.join(f"<tr><td>{E(x['sec'])}</td><td>{E(x['item'])}</td><td class='small'>{E(x['what'])}</td></tr>" for x in LOG) + "</table></div>")
    # a drawing for every zone of S9, as built
    lab = {}
    for l in P['r9ayin_lots']:
        if l['kind'] in ('building', 'parking'): lab.setdefault(l['zone'], []).append(l)
    o.append("<h3>הציורים — כל אזור של S9 כמו שנבנה</h3><div class='grid2'>")
    import plan7b_svg as SV
    for z in ('E4', 'E5', 'F3', 'F4', 'F5', 'F6'):
        x0, y0, x1, y1 = SV.zrect(z)
        t = ''.join(PG.t_((l['rect'][0] + l['rect'][2]) / 2, (l['rect'][1] + l['rect'][3]) / 2 + 8, l['label'][:22], 'r9s') for l in lab.get(z, []) if (l['rect'][2] - l['rect'][0]) > 50)
        if z in ('F5', 'F6'):
            t += ''.join(PG.t_(b['x'] + (30 if b.get('color') == 'green' else -30), b['y'] + 8, b['id'], 'r9s', 'start' if b.get('color') == 'green' else 'end') for b in G.get('F56_BUOYS') or [] if b.get('zone') == z)
        nm = P['zones'].get(z, {}).get('purpose', '')
        o.append(PG.sec_svg(f'{x0 - 60} {y0 - 60} {x1 - x0 + 120} {y1 - y0 + 120}', f'{z} — {nm} · נבנה ב-{ZB[z]}',
                            f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='none' stroke='#1f5fd1' stroke-width='10'/>" + t))
    pr = P['proposals'][0]
    o.append(PG.sec_svg('5450 2350 800 1350', 'ההצעה: מעבר פסים מ-B ל-A (X-BA) בין E3 לתחנת החוף — ' + ASK,
                        "<rect x='5736' y='2826' width='38' height='732' fill='none' stroke='#1f5fd1' stroke-width='8' stroke-dasharray='20 12'/>" +
                        PG.t_(5700, 3200, '4 קרונות — 2826–3558', 'r9s', 'end') + PG.t_(5940, 2610, 'UX-1 — הגשר', 'r9s', 'start') + PG.t_(5700, 2510, 'סוף הרציפים של E3', 'r9s', 'end') +
                        f"<line x1='{pr['xs_was'][0][0]}' y1='{pr['xs_was'][0][1]}' x2='{pr['xs_was'][1][0]}' y2='{pr['xs_was'][1][1]}' stroke='#7a7a7a' stroke-width='8' stroke-dasharray='10 10'/>" +
                        "<line x1='5800' y1='2852' x2='5900' y2='3024' stroke='#1f5fd1' stroke-width='10'/>" + PG.t_(5930, 2950, 'X-S — 3 מ׳ דרומה', 'r9s', 'start')))
    o.append("</div>")
    o.append(f"<h3>ההתלבטות — מעבר פסים מ-B ל-A לרכבת הנוסעים של 4 קרונות ({ASK})</h3><p>{E(pr['why'])}</p><p class='small'>{E(pr['alt'])}</p>")
    c = Counter((r['kind'], r['dir'], r['ok']) for r in rows)
    KH = {'lot': 'מגרשים', 'segment': 'קטעי דרך', 'driveway': 'פתחים', 'junction': 'צמתים', 'crosswalk': 'מעברי חצייה', 'bay': 'מפרצי תחנה'}
    o.append("<h3>המפה מול המשחק — טבלת ההתאמה (S7F270)</h3>"
             f"<p class='small'>הקובץ המלא: map_vs_game_9ayin.json ({len(rows)} שורות). האזורים שנבנו: {E(', '.join(BZ))}. יותר מ-4.5 מ׳ — לא תואם, עם הסבר ועם \"מי מתקן\".</p>"
             "<div class='wrap'><table><tr><th>מה</th><th>מהמפה למשחק — תואם / לא</th><th>מהמשחק למפה — תואם / לא</th></tr>" +
             ''.join(f"<tr><td>{KH[k]}</td><td>{c[(k, 'map→game', True)]} / <b>{c[(k, 'map→game', False)]}</b></td><td>{c[(k, 'game→map', True)]} / <b>{c[(k, 'game→map', False)]}</b></td></tr>"
                     for k in ('lot', 'segment', 'driveway', 'junction', 'crosswalk', 'bay')) + "</table></div>")
    bad = [r for r in rows if not r['ok']]; DIR = {'map→game': 'מפה ← משחק', 'game→map': 'משחק ← מפה'}
    o.append("<p class='small'>מי מתקן: " + ' · '.join(f"{E(k)} — {v}" for k, v in Counter(r['fix'] for r in bad).most_common()) + "</p>")
    o.append(f"<details><summary><b>כל מה שלא תואם</b> — {len(bad)} שורות</summary><div class='wrap'><table><tr><th>מה</th><th>כיוון</th><th>במפה</th><th>במשחק</th><th>אזור</th><th>מרחק (מ׳)</th><th>הסבר</th><th>מי מתקן</th></tr>" +
             ''.join(f"<tr><td>{KH[r['kind']]}</td><td class='small'>{DIR[r['dir']]}</td><td class='id'>{E(r['map'] or '—')}</td><td class='id'>{E(r['game'] or '—')}</td><td class='id'>{E(r['zone'] or '')}</td>"
                     f"<td>{'' if r['dist_m'] is None else r['dist_m']}</td><td class='small'>{E(r['note'])}</td><td class='small'>{E(r['fix'] or '')}</td></tr>"
                     for r in sorted(bad, key=lambda r: (r['kind'], r['zone'] or '', r['map'] or r['game'] or ''))) + "</table></div></details>")
    asks = [x for x in LOG if ASK in x['what']]
    o.append("<h3>לאישורך — ברירות המחדל של הסבב</h3><ul>" + ''.join(f"<li><b>{E(x['item'])}</b> — {E(x['what'])}</li>" for x in asks) + "</ul>")
    return ''.join(o)


def main():
    os.chdir(HERE)
    P, H = start()
    G = json.load(open(os.path.join(HERE, 'game_s7f270.json'), encoding='utf-8'))
    assert G['BUILD'].endswith('s7f270'), G['BUILD']
    d_version(P); d_s9(P, G); d_s9_net(P, G); d_s9_rails(P, G); d_bays(P, G); GL = d_lines(P, G)
    PS = P.get('zone_stage') or {}
    segs = [s['id'] for s in P['segments'] if s.get('built')]
    rows, BZ = MT.match(P, G, notes(P), zones_extra=S9Z, segs_extra=segs)
    lot_status(P, rows)
    rows, BZ = MT.match(P, G, notes(P), zones_extra=S9Z, segs_extra=segs)
    H2, info = page(H, P, G, rows, BZ, PS, GL)
    T = R9S.table_json(P, G, rows, BZ)
    T.update(id='map_vs_game_9ayin', title=f'טבלת ההתאמה — מפת הדרכים סבב {VERSION} מול המשחק {BUILD}', map=dict(file='study/roads/city_plan.json', version=VERSION),
             game=dict(build=BUILD, sha1=BUILD_SHA, file=GAME, title=G.get('title')), built_zones=BZ)
    P['r9ayin'] = dict(at=DATE, by='סוכן המפה', build=BUILD, log=LOG, counts=T['counts'])
    json.dump(P, open(os.path.join(HERE, 'city_plan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(HERE, 'city_plan.html'), 'w', encoding='utf-8').write(H2)
    open(os.path.join(OUT, 'Turbo_City_Roads_9ayin.html'), 'w', encoding='utf-8').write(H2)
    json.dump(T, open(os.path.join(OUT, 'map_vs_game_9ayin.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('r9ayin', T['counts']['total'], 'rows ·', T['counts']['bad'], 'not matching ·', info)


if __name__ == '__main__':
    main()
