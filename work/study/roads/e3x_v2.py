# -*- coding: utf-8 -*-
"""3.11 17:20 · E3 — the crossings, version 2 (the owner 17:16: no longer islands or bays — only crossings; the buses need the room to turn and leave).
    A copy of qa/tmp/r9g_e3x.py (the first builder) with the proposal changed. python3 -I e3x_v2.py → deliver/2026-11-03/Turbo_City_E3_Crossings_v2.html (a new file)"""
import json, os, html, hashlib, math
W = '/home/claude/tc/pkg/work'; OUT = W + '/deliver/2026-11-03/Turbo_City_E3_Crossings_v2.html'
assert not os.path.exists(OUT)
M = json.load(open(W + '/study/roads/city_plan.json', encoding='utf-8')); T = M['bus']['terminal']; R9 = T['r9']
SHA = hashlib.sha1(open(W + '/study/roads/city_plan.json', 'rb').read()).hexdigest()[:12]
LC = {'1': '#1f5fd1', '2': '#a0521b', '3': '#2b2b2b', '4': '#0f8f8a', '5': '#6b3fd1', '6': '#2e9e3e'}
BOARD = {v: k for k, v in R9['board'].items()}; PARK = {v: k for k, v in R9['park'].items()}
e = lambda s: html.escape(str(s))
def rect(r, fill, extra=''): return f"<rect x='{r[0]}' y='{r[1]}' width='{r[2]-r[0]}' height='{r[3]-r[1]}' fill='{fill}' {extra}/>"
def text(t, x, y, cls='t', rot=0): return f"<text x='{x}' y='{y}' class='{cls}'" + (f" transform='rotate({rot} {x} {y})'" if rot else '') + f">{e(t)}</text>"
def zebra(r, vertical):
    o = rect(r, '#c9c4b5', "rx='2'"); x0, y0, x1, y1 = r
    if vertical:   # walkers go north–south: the stripes run east–west
        y = y0 + 3
        while y < y1 - 3: o += rect([x0 + 3, y, x1 - 3, y + 4], '#ffffff'); y += 9
    else:
        x = x0 + 3
        while x < x1 - 3: o += rect([x, y0 + 3, x + 4, y1 - 3], '#ffffff'); x += 9
    return o
STATION = [5700, 1850, 5736, 2290]; ENTR = (5700, 1995)
def base(prop):
    o = [rect([4860, 1700, 5900, 1770], '#d9d4c7'), rect([4860, 2170, 5740, 2240], '#d9d4c7'), rect(T['rect'], '#5b6470')]
    o.append(text('המדרכה הצפונית', 5180, 1745, 'tw')); o.append(text('המדרכה הדרומית · החניונים', 5180, 2212, 'tw'))
    for p in M['stations'][0]['rects']: o.append(rect(p, '#b9c7d6', "stroke='#5a6f86' stroke-width='2'"))
    o.append(rect(STATION, '#e9e4d6', "stroke='#8a8070' stroke-width='2'")); o.append(text('תחנת הרכבת — הכניסה', 5718, 2040, 'ts', -90))
    for b in T['bays']:
        no = b['no']; ln = BOARD.get(no) or PARK.get(no); col = LC.get(ln, '#8a8f96'); r = b['rect']
        o.append(rect(r, col, "fill-opacity='.35' stroke='#ffffff' stroke-width='1.5' stroke-dasharray='6 4'"))
        o.append(text(f"{no}{' · קו ' + ln if ln else ''}{' · עלייה' if no in BOARD else (' · חניה' if no in PARK else '')}", (r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 5, 'tb'))
        nx = r[2]; o.append(f"<line x1='{nx}' y1='{r[1]}' x2='{nx}' y2='{r[3]}' stroke='#f2c200' stroke-width='3'/>")   # the nose (the buses drive east along the islands)
    for h in T['hold']:
        r = list(h['rect']); 
        if prop: r[0] -= 60; r[2] -= 60
        o.append(rect(r, '#8a8f96', "fill-opacity='.45' stroke='#ffffff' stroke-dasharray='5 4'")); o.append(text(f"המתנה {h['no']}", (r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 5, 'tb'))
    for p in T['platforms']:
        r = list(p['rect'])
        if prop: r[2] = 5660
        o.append(rect(r, '#e8e2d0', "stroke='#8a8070' stroke-width='2'")); o.append(text(f"אי {p['id']}׳", 5300, (r[1] + r[3]) / 2 + 5, 'tw'))
    wb = R9['west']['building']; o.append(rect(wb, '#d8cfb6', "stroke='#6b5a3a' stroke-width='2'")); o.append(text('הסדרן', (wb[0] + wb[2]) / 2, (wb[1] + wb[3]) / 2 + 5, 'ts'))
    o.append(f"<path d='M 5400 2240 L 5400 2172' stroke='#ffffff' stroke-width='6' marker-end='url(#ar)'/>"); o.append(text('השער', 5440, 2232, 'tw'))
    return o
def plan():
    o = base(False)
    em = R9['east']['mid']; o.append(rect(em, '#e8e2d0', "stroke='#8a8070' stroke-width='2'"))
    for c in R9['crossings']: o.append(zebra(c['r'], c['v'])); o.append(text(c['id'], (c['r'][0] + c['r'][2]) / 2, c['r'][1] - 6, 'tr'))
    return o
TURN = [5540, 1770, 5700, 2170]                      # the east end of the yard: the room to turn and leave — free (only paint)
WALK = [5700, 1770, 5736, 1850]                      # the station's pavement, from its front north to the north pavement (outside the yard)
XS = [('X-AE', [5540, 1895, 5700, 1925], False, 'מהקצה של אי א׳ מזרחה — אל המדרכה של התחנה'), ('X-BE', [5540, 2065, 5700, 2095], False, 'מהקצה של אי ב׳ מזרחה — אל המדרכה של התחנה'),
      ('X-M', [5548, 1925, 5588, 2065], True, 'בין הקצוות של שני האיים — אפשרות, לאישורך')]
def prop():
    o = base(False)
    o.append(rect(TURN, '#ffd24a', "fill-opacity='.13' stroke='#ffd24a' stroke-width='2' stroke-dasharray='8 6'")); o.append(text('שטח התמרון — פנוי', 5620, 2155, 'tr'))
    o.append(rect(WALK, '#d9d4c7')); o.append(text('המדרכה של התחנה', 5718, 1812, 'ts', -90))
    for cid, r, v, what in XS:
        o.append(zebra(r, v) if cid != 'X-M' else rect(r, 'none', "stroke='#ffffff' stroke-width='3' stroke-dasharray='7 5'"))
        o.append(text(cid, (r[0] + r[2]) / 2 + (30 if v else 0), (r[1] + r[3]) / 2 + (5 if v else -20), 'tr'))
    return o
def svg(parts, title):
    return (f"<figure><figcaption>{e(title)}</figcaption><svg viewBox='4860 1700 1040 545' role='img' aria-label='{e(title)}'>"
            "<defs><marker id='ar' viewBox='0 0 10 10' refX='5' refY='5' markerWidth='4' markerHeight='4' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='#ffffff'/></marker></defs>"
            + ''.join(parts) + "</svg></figure>")
def L(r, v): return round(((r[3] - r[1]) if v else (r[2] - r[0])) / 10, 1)
cp = [(c['id'], c['what'], L(c['r'], c['v'])) for c in R9['crossings']]
cx = [(c, w, L(r, v)) for c, r, v, w in XS]
rows_p = ''.join(f"<tr><td class='id'>{e(a)}</td><td>{e(b)}</td><td>{c}</td></tr>" for a, b, c in cp)
rows_x = ''.join(f"<tr><td class='id'>{e(a)}</td><td>{e(b)}</td><td>{c}</td></tr>" for a, b, c in cx)
# the trips, from the island's east tip (x 5540): metres and how many crossings — the routes as drawn
XL = (5700 - 5540) / 10; YA, YB = 1910, 2080   # the crossing to the station (16 m) and the middles of the islands
TRIPS = [('מאי א׳ לתחנה', (12 + 4 + 8.5, 1), (XL, 1)), ('מאי ב׳ לתחנה', (12 + 4 + 8.5, 1), (XL, 1)),
         ('מאי א׳ לאי ב׳ (מעבר בין קווים)', (12 + 4 + 17 + 4 + 12, 2), (XL + (YB - YA) / 10 + XL, 2)), ('מאי א׳ לאי ב׳ — ב-X-M (אפשרות)', (12 + 4 + 17 + 4 + 12, 2), ((2065 - 1925) / 10, 1)),
         ('מאי א׳ לחניון בדרום', (12 + 4 + 17 + 4 + 2.6 + 9, 3), (XL + (2170 - YA) / 10, 1)), ('מאי ב׳ לחניון בדרום', (9.4 + 9, 1), (XL + (2170 - YB) / 10, 1)),
         ('מאי א׳ למדרכה הצפונית', (9.4 + 14, 1), (XL + (YA - 1770) / 10, 1)), ('מאי ב׳ למדרכה הצפונית', (12 + 4 + 17 + 4 + 2.6 + 14, 3), (XL + (YB - 1770) / 10, 1))]
wrows = ''.join(f"<tr><td class='id'>{e(a)}</td><td>{round(p[0])} · {p[1]}</td><td>{round(q[0])} · {q[1]}</td></tr>" for a, p, q in TRIPS)
CSS = """:root{--bg:#f7f5f0;--fg:#1d2228;--mut:#5b6470;--card:#ffffff;--line:#d9d4c7}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15181c;--fg:#e8e6e1;--mut:#a8b0ba;--card:#1e2328;--line:#3a4048}}
:root[data-theme="dark"]{--bg:#15181c;--fg:#e8e6e1;--mut:#a8b0ba;--card:#1e2328;--line:#3a4048}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 "Segoe UI",Arial,sans-serif}main{max-width:1100px;margin:0 auto;padding:16px}
h1{font-size:1.5rem;margin:.4em 0}h2{font-size:1.15rem;margin:1.2em 0 .4em}p,li{max-width:70ch}.small{color:var(--mut);font-size:.9rem}
figure{margin:12px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px}figcaption{font-weight:600;margin-bottom:6px}
svg{width:100%;height:auto;display:block}.t,.tw,.tb,.ts,.tr,.tg{font:600 13px "Segoe UI",Arial;text-anchor:middle}.tw{fill:#fff}.tb{fill:#fff;font-size:11px}.ts{fill:#1d2228;font-size:12px}
.tr{fill:#ffd24a;font-size:12px}.tg{fill:#1d7a3a;font-size:14px}
.wrap{overflow-x:auto}table{border-collapse:collapse;margin:8px 0;min-width:420px}td,th{border:1px solid var(--line);padding:4px 10px;text-align:right}th{background:var(--card)}td.id{font-weight:600}"""
TXT = dict(
 intro='מסוף האוטובוסים של E3 לפי מפת הדרכים סבב 9, והמעברים בגרסה 2. הבעלים (17:16): "הארכת את המפרצים ב-E3 — רציתי רק מעבר חציה, כי צריך שיהיה לאוטובוסים איך לתמרן ולצאת נורמלי מהמסוף". הגרסה הראשונה האריכה את האיים עד x 5660 — היא בוטלה.',
 plan_h='המצב בתוכנית (סבב 9)', plan_p='4 מעברים: מאי א׳ צפונה (12.5 מ׳ — חוצה את נתיב ההמתנה ואת נתיב הנסיעה), מאי ב׳ דרומה, ומכל אי מזרחה אל התחנה, דרך ההמשך המקורה של האיים ובלוק באמצע — שניהם בתוך הקצה המזרחי של החצר, שבו האוטובוסים מסתובבים.',
 prop_h='גרסה 2: רק מעברים', prop_p='האיים והמפרצים נשארים בדיוק כמו בתוכנית (עד x 5540). הקצה המזרחי של החצר (x 5540–5700, ‏16 מ׳) פנוי כולו לתמרון וליציאה — בלי המשך מקורה ובלי בלוק באמצע; יש בו רק צבע על הכביש. מהקצה של כל אי — מעבר ישר אחד מזרחה, אל המדרכה של התחנה; משם הולכים על המדרכה, מחוץ לחצר, צפונה למדרכה הצפונית ודרומה לחניון. כך אף אחד לא חוצה את נתיב ההמתנה ואת נתיב הנסיעה בצפון ובדרום.',
 rules_h='איך עובר כל מעבר',
 rules=['שני מעברים קבועים (X-AE, ‏X-BE): פסי חצייה צבועים, בניצב לתנועה; האוטובוסים בתוך המסוף נותנים זכות קדימה (החריגה הרשומה של המסוף).', 'לא מאריכים אי, מפרץ או מדרכה לתוך החצר. מה שבתוך שטח התמרון — רק צבע.',
        'המדרכה של התחנה ממשיכה צפונה עד המדרכה הצפונית (x 5700–5736) — מחוץ לחצר, כך שההליכה לצפון ולדרום לא חוצה אף נתיב.', 'X-M — מעבר בין הקצוות של שני האיים, לנוסע שעובר מקו לקו: 14 מ׳ במקום 49; הוא עובר מול החרטום של מפרצים 6 ו-9, ולכן הוא אפשרות לאישורך, לא ברירת מחדל.',
        'אף אדם לא הולך בנתיב האוטובוסים מחוץ למעבר. בדיקת האנשים בכביש מכירה רק את המעברים האלה.',
        'מקום ההמתנה 4 נכנס 6 מ׳ לשטח התמרון, כמו בתוכנית. ברירת המחדל: הוא נשאר במקומו (לאישורך).'],
 table_h='המעברים', walk_h='ההליכה מאמצע האי (מ׳, בערך, ומספר המעברים)', ask_h='לאישורך',
 ask=['ברירת המחדל: שני מעברים (X-AE, ‏X-BE), והאיים והמפרצים כמו בתוכנית. הבונה יבנה כך, אלא אם תכתוב אחרת.', 'X-M בין האיים — כן או לא (ברירת המחדל: לא, כי הוא מול החרטום של שני מפרצים).', 'מה משתפר מול התוכנית: לתחנה — 16 מ׳ ישר; לחניון ולמדרכה הצפונית — מעבר אחד במקום שלושה; ושטח התמרון פנוי.'],
 src=f'המקור: מפת הדרכים (city_plan.json ‏{SHA}), המסוף וסבב 9. המספרים מחושבים מהנתונים, לא מוקלדים.')
page = ("<!doctype html><html lang='he' dir='rtl'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>E3 — המעברים במסוף · גרסה 2</title><style>" + CSS + "</style></head><body><main>"
        f"<h1>E3 — המעברים במסוף האוטובוסים</h1><p>{e(TXT['intro'])}</p>"
        f"<h2>{e(TXT['plan_h'])}</h2><p>{e(TXT['plan_p'])}</p>" + svg(plan(), 'התוכנית — סבב 9') +
        f"<div class='wrap'><table><tr><th>המעבר</th><th>מאיפה לאן</th><th>אורך (מ׳)</th></tr>{rows_p}</table></div>"
        f"<h2>{e(TXT['prop_h'])}</h2><p>{e(TXT['prop_p'])}</p>" + svg(prop(), 'גרסה 2 — רק מעברים, שטח התמרון פנוי') +
        f"<div class='wrap'><table><tr><th>המעבר</th><th>מאיפה לאן</th><th>אורך (מ׳)</th></tr>{rows_x}</table></div>"
        f"<h2>{e(TXT['rules_h'])}</h2><ul>" + ''.join(f"<li>{e(r)}</li>" for r in TXT['rules']) + "</ul>"
        f"<h2>{e(TXT['walk_h'])}</h2><div class='wrap'><table><tr><th>הדרך</th><th>בתוכנית: מ׳ · מעברים</th><th>בגרסה 2: מ׳ · מעברים</th></tr>{wrows}</table></div>"
        f"<h2>{e(TXT['ask_h'])}</h2><ul>" + ''.join(f"<li>{e(r)}</li>" for r in TXT['ask']) + f"</ul><p class='small'>{e(TXT['src'])}</p></main></body></html>")
open(OUT, 'w', encoding='utf-8').write(page)
vis = [TXT['intro'], TXT['plan_h'], TXT['plan_p'], TXT['prop_h'], TXT['prop_p'], TXT['rules_h'], *TXT['rules'], TXT['walk_h'], TXT['ask_h'], *TXT['ask'], TXT['src']]
open(OUT.replace('.html', '_text.txt'), 'w', encoding='utf-8').write('\n'.join(vis))
print('written', OUT, os.path.getsize(OUT), hashlib.sha1(open(OUT, 'rb').read()).hexdigest()[:12])
