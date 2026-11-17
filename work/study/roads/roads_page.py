#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-15: the page "רשת הכבישים — רשימה לכל העיר" — the map of the whole network with every finding of roads_audit.py, a short table by area
(what was found, the proposal, when), and the full list. Writes roads_r15.html."""
import json, os, html, collections
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(H, 'game_roads.json'), encoding='utf-8')); A = json.load(open(os.path.join(H, 'roads_audit.json'), encoding='utf-8'))
E = lambda s: html.escape(str(s), quote=False)
N = {n['id']: n for n in D['nodes']}; F = A['findings']
W, HH = D['world']['w'], D['world']['h']
WID = {'arterial': 60, 'avenue': 44, 'local': 30}
COL = {'מיותר — הדוגמה שלך': 'ex', 'מיותר': 'red', 'צמתים קרובים': 'close', 'מבוי סתום': 'dead', 'ממשיך לאזור שלא נבנה': 'cont', 'זרימה': 'flow'}
svg = ['<svg viewBox="-40 -40 %d %d" role="img" aria-label="רשת הכבישים של העיר עם הממצאים">' % (W + 80, HH + 80)]
for c in D['chunks']:
    svg.append('<rect x="%d" y="%d" width="%d" height="%d" class="ch"/><text x="%d" y="%d" class="chl">%s</text>' % (c['x'], c['y'], c['w'], c['h'], c['x'] + 30, c['y'] + 70, c['id']))
svg.append('<rect x="6000" y="0" width="3600" height="2550" class="air"/><text x="7800" y="1300" class="airl" text-anchor="middle">השדה — ישן, ייבנה מחדש ב-S15 / S16</text>')
for e in D['edges']:
    a, b = N[e['a']], N[e['b']]
    svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="rd %s%s" stroke-width="%d"/>' % (a['x'], a['y'], b['x'], b['y'], e['cls'], ' fut' if e['future'] else '', WID[e['cls']]))
for f in F:
    if not f.get('x') and not f.get('y'): continue
    k = COL.get(f['kind'], 'red'); r = 70 if k == 'ex' else 52
    svg.append('<g class="mk %s"><circle cx="%d" cy="%d" r="%d"/><text x="%d" y="%d" text-anchor="middle">%d</text></g>' % (k, f['x'], f['y'], r, f['x'], f['y'] + 22, f['n']))
svg.append('</svg>')
# ---- by area: the proposal for each group (the numbers come from the audit; the proposal is the coordinator's) ----
AREA = [
 ('B3 / C3', 'הדוגמה שלך: רחוב הדיירים (B3-RES-E) מיותר; וגם שני צמתים 26 מ׳ זה מזה על העורק האמצעי (N3 ו-B3R3)', 'לסגור את B3-RES-E; רחוב המגורים ממשיך מזרחה אל N1 (צומת אחד של ארבע זרועות עם רחוב הגנים). אז B3R3 כבר לא צומת — והבעיה של 26 מ׳ נעלמת איתו', 'צעד 14 (B3 / C3)'),
 ('B4', '8 קטעים קצרים (30–41 מ׳) ו-9 זוגות צמתים קרובים — הרשת של היום', 'B4 נבנה מאפס לפי השרטוט (צעד 6): רחוב הגנים מזרח נסגר (הדוגמה שלך), ובשרטוט — לפחות 60 מ׳ בין צמתים; הבדיקה הזו רצה על השרטוט לפני הבנייה', 'צעד 6'),
 ('A4', 'שני קטעי החיבור ל-B4 (68 מ׳) ושני צמתים 34 מ׳ זה מזה על השדרה', 'כמו באפשרות ב׳ של דף המגרשים: הלולאה המקומית יוצאת, והחיבורים ל-B4 נשארים רק מהשדרה', 'צעד 14 (A4)'),
 ('E4 / E5', 'בחצר הרכבת ובתחנת הכוח: 8 קטעים קצרים (29–59 מ׳) ו-5 זוגות צמתים קרובים — ציר שירות שמתפצל כל 30 מ׳', 'ציר אחד לאורך החצר עם כניסות לכל מתקן מהציר, בלי צמתים; תחנת הכוח ותחנת המשנה — כניסה אחת משותפת', 'צעד 15 (E4–E6 מאפס)'),
 ('D4 / D5 / D6 / E6', 'שערי הנמל: שלושה צמתים במרחק 29–31 מ׳ על R-EAST ועל דרך הנמל; שני רחובות מקומיים שחוצים את R-EAST בצומת של ארבע זרועות', 'לאחד את השערים לצומת אחד עם רמזור; הרחובות המקומיים — ימינה-ימינה בלבד (R-16)', 'צעד 15 · R-16 בצעד 8'),
 ('B5 / B6', 'הקמפוס והחוף: 7 זוגות צמתים קרובים (25–38 מ׳) וקטע מיותר אחד', 'כיכר אחת בכניסה לחוף במקום שלושה צמתים; רחוב העירייה מערב — נסגר', 'צעד 14 (B5) · שלב 12 (B6)'),
 ('C4 / C5 / C6', 'שדרת המרכז ב-C5: צמתים 16 ו-34 מ׳ זה מזה; החיבור ל-C6', 'הכניסה לשדרת התרבות — מהצומת הקיים של שדרת התעשייה, לא צומת נוסף', 'צעד 15 (C5 / C6)'),
 ('D2 / D3', 'R-EAST ליד כביש השדה החדש (AIR-W0): שני צמתים קרובים; רחוב מקומי חוצה עורק בשדרת העסקים', 'הצומת של AIR-W0 — חלק מהשדה, ייבנה מחדש ב-S16; שדרת העסקים — ימינה-ימינה (R-16)', 'S16 · צעד 13 (D2)'),
 ('גבולות', '6 כבישים נגמרים בגבול של אזור שעוד לא נבנה (A2, ‏A3, ‏C1, ‏D1, ‏E2, ‏F3)', 'ממשיכים אותם כשהאזור נבנה; עד אז — סיום מסודר', 'עם האזור הסמוך'),
]
rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (E(a), E(b), E(c), E(d)) for a, b, c, d in AREA)
full = ''.join('<tr class="%s"><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (COL.get(f['kind'], ''), f['n'], E(f['kind']), E(f['where']), E(f['what']), E(f['why']), E(f['prop']), E(f['step'])) for f in F)
cnt = collections.Counter(f['kind'] for f in F)
page = '''<title>רשת הכבישים · R-15</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root{--bg:#f3f2ed;--fg:#1d2124;--mut:#5d656b;--line:#d6d4cc;--card:#fbfaf6;--road:#7d838a;--fut:#c2c6ca;--ch:#e7e5dc;--air:#e3ddd0;--red:#b8321f;--ex:#7b2fbf;--close:#c47b14;--dead:#2b6cb0;--cont:#6b7a88;--flow:#1f8a5b}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#15181b;--fg:#e7e9ea;--mut:#a3abb1;--line:#30363b;--card:#1c2024;--road:#9aa1a8;--fut:#4a5056;--ch:#20252a;--air:#2c2a24;--red:#f07a66;--ex:#c18cf0;--close:#f0b257;--dead:#7fb0e8;--cont:#9aa8b5;--flow:#5fd19c;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#15181b;--fg:#e7e9ea;--mut:#a3abb1;--line:#30363b;--card:#1c2024;--road:#9aa1a8;--fut:#4a5056;--ch:#20252a;--air:#2c2a24;--red:#f07a66;--ex:#c18cf0;--close:#f0b257;--dead:#7fb0e8;--cont:#9aa8b5;--flow:#5fd19c;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:16px/1.55 'Assistant','Segoe UI',Arial,sans-serif;direction:rtl}
.w{max-width:1100px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 48px;display:grid;gap:14px}
h1{font-size:clamp(24px,4vw,30px);margin:0;text-wrap:balance} h2{font-size:20px;margin:6px 0 0} p{margin:0;max-width:78ch} .mut{color:var(--mut)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;min-width:0}
.sv{overflow-x:auto} svg{width:100%;min-width:620px;height:auto;display:block}
.ch{fill:var(--ch);stroke:var(--line);stroke-width:4} .chl{font:700 60px sans-serif;fill:var(--mut)} .air{fill:var(--air);opacity:.8} .airl{font:700 120px sans-serif;fill:var(--mut)}
.rd{stroke:var(--road);stroke-linecap:round} .rd.fut{stroke:var(--fut);stroke-dasharray:40 30}
.mk circle{stroke:var(--card);stroke-width:8} .mk text{font:700 56px sans-serif;fill:#fff}
.mk.red circle{fill:var(--red)} .mk.ex circle{fill:var(--ex)} .mk.close circle{fill:var(--close)} .mk.dead circle{fill:var(--dead)} .mk.cont circle{fill:var(--cont)} .mk.flow circle{fill:var(--flow)}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:14px} .legend span::before{content:"";display:inline-block;width:12px;height:12px;border-radius:50%;margin-inline-end:6px;vertical-align:-1px;background:var(--c)}
.tw{overflow-x:auto} table{border-collapse:collapse;width:100%;min-width:760px;font-size:14px} th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:right;vertical-align:top} th{color:var(--mut);font-weight:600}
details summary{cursor:pointer;font-weight:700}
</style>
<div class="w">
<h1>רשת הכבישים — רשימה לכל העיר · R-15</h1>
<p class="mut">לעינך לפני שבונים (הבעלים 29.10 12:00): כל הכבישים והצמתים של המשחק — %STREETS% רחובות, אחרי שחיברתי את הקטעים שנחתכים בגבולות האזורים — נבדקו לפי מספרים ולא בעין: קטע קצר שמכפיל דרך קרובה, צמתים במרחק של פחות מ-45 מ׳, זווית של פחות מ-60° (לא נמצאה אף אחת), מבוי סתום, ורחוב מקומי שחוצה עורק. השדה ישן וייבנה מחדש ב-S15 / S16 (D‑462); עד אז אין בו תיקונים קטנים, ומה שנמצא בו מסומן ועובר לשם. הנתונים — מהמשחק עצמו (probe_roads.js).</p>
<div class="legend"><span style="--c:var(--ex)">הדוגמאות שלך (%EX%)</span><span style="--c:var(--red)">קטע מיותר (%RED%)</span><span style="--c:var(--close)">צמתים קרובים (%CLOSE%)</span><span style="--c:var(--flow)">זרימה (%FLOW%)</span><span style="--c:var(--dead)">מבוי סתום (%DEAD%)</span><span style="--c:var(--cont)">ממשיך לאזור שלא נבנה (%CONT%)</span></div>
<div class="card sv">%SVG%</div>
<h2>לפי אזור — מה נמצא ומה מוצע</h2>
<div class="tw card"><table><thead><tr><th>אזור</th><th>מה נמצא</th><th>ההצעה</th><th>מתי</th></tr></thead><tbody>%ROWS%</tbody></table></div>
<p class="mut">השעות: בתוך השעות של הכבישים בכל אזור בתוכנית (צעד 6 — B4; צעדים 13–15 — ‏2 + 3 + 3; רשת הכבישים ו-R-16 / R-17 בצעד 8 — 4 + 3 + 2). כל אזור מקבל שרטוט של הכבישים לפני ואחרי לעינך לפני שבונים, והבדיקה הזו רצה על כל שרטוט. עד שתחליט — ההצעות האלה הן ברירת המחדל, ולא עוצרות עבודה אחרת.</p>
%LANES%
<details class="card"><summary>הרשימה המלאה — %N% ממצאים</summary><div class="tw"><table><thead><tr><th>#</th><th>סוג</th><th>אזור</th><th>מה</th><th>למה</th><th>הצעה</th><th>מתי</th></tr></thead><tbody>%FULL%</tbody></table></div></details>
</div>'''
for k, v in [('%STREETS%', str(A['streets'])), ('%EX%', str(cnt['מיותר — הדוגמה שלך'])), ('%RED%', str(cnt['מיותר'])), ('%CLOSE%', str(cnt['צמתים קרובים'])), ('%FLOW%', str(cnt['זרימה'])), ('%DEAD%', str(cnt['מבוי סתום'])),
             ('%CONT%', str(cnt['ממשיך לאזור שלא נבנה'])), ('%SVG%', ''.join(svg)), ('%ROWS%', rows), ('%N%', str(len(F))), ('%FULL%', full)]:
    page = page.replace(k, v)
page = page.replace('%LANES%', open(os.path.join(H, 'lanes_section.html'), encoding='utf-8').read() if os.path.exists(os.path.join(H, 'lanes_section.html')) else '')
open(os.path.join(H, 'roads_r15.html'), 'w', encoding='utf-8').write(page); print('roads_r15.html', len(page))
