# -*- coding: utf-8 -*-
# fx_page.py <fx_ret.json> <out.html> — fieldexit: הציור של היציאה המהירה (SVG בקוד, בלי תמונות) מהמספרים של fx_ret.py
import sys, json, math, io, contextlib
sys.path.insert(0, '.')
with contextlib.redirect_stdout(io.StringIO()):
    import fx_ret as X
R = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]
X0, X1, Y0, Y1 = 4900, 9600, -880, 120; S = 0.2
def px(x): return round((x - X0) * S, 1)
def py(y): return round((y - Y0) * S, 1)
svg = ['<svg viewBox="0 0 %d %d" role="img" aria-label="המסלול, A והיציאות המהירות">' % (px(X1), py(Y1))]
svg.append('<rect x="0" y="0" width="%s" height="%s" fill="var(--grass)"/>' % (px(X1), py(Y1)))
svg.append('<rect x="%s" y="%s" width="%s" height="%s" fill="var(--asph)"/>' % (px(5000), py(-810), px(9300) - px(5000), py(-570) - py(-810)))
svg.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="var(--paint)" stroke-dasharray="6 5" stroke-width="1.2"/>' % (px(5220), py(-690), px(9080), py(-690)))
svg.append('<rect x="%s" y="%s" width="%s" height="%s" fill="var(--asph)"/>' % (px(4900), py(-285), px(9450) - px(4900), py(-55) - py(-285)))
svg.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="var(--yel)" stroke-width="1"/>' % (px(4900), py(-170), px(9450), py(-170)))
for nm, x in (('A1', 5250), ('A2', 7150), ('A3', 8345), ('A4', 9190)):
    svg.append('<rect x="%s" y="%s" width="%s" height="%s" fill="var(--asph)"/>' % (px(x - 100), py(-570), 200 * S, py(-285) - py(-570)))
    svg.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="var(--red)" stroke-width="1.6"/>' % (px(x - 100), py(-470), px(x + 100), py(-470)))
    svg.append('<text x="%s" y="%s" class="lb">%s</text>' % (px(x), py(-25), nm))
svg.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="var(--red)" stroke-dasharray="3 3" stroke-width=".8"/>' % (px(5000), py(-480), px(9300), py(-480)))
svg.append('<text x="%s" y="%s" class="sm">y −480 — כאן נגמרת התפוסה</text>' % (px(5600), py(-500)))
COL = {'RET-A3N': 'var(--c1)', 'RET-A4': 'var(--c2)'}
for nm, xj in (('RET-A3N', 8345.0), ('RET-A4', 9190.0)):
    x0, P, ls = X.ret_pts(xj); d = ' '.join('%s,%s' % (px(p[0]), py(p[1])) for p in [[x0 - 300, X.RCY]] + P)
    svg.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round" opacity=".9"/>' % (d, COL[nm]))
    svg.append('<text x="%s" y="%s" class="lb" fill="%s">%s</text>' % (px(x0), py(-740), COL[nm], nm.replace('RET-A3N', 'יציאה מהירה A3').replace('RET-A4', 'יציאה מהירה A4')))
svg.append('<circle cx="%s" cy="%s" r="4" fill="var(--ink)"/><text x="%s" y="%s" class="sm">נגיעה 5300</text>' % (px(5300), py(-690), px(5300), py(-830)))
svg.append('<text x="%s" y="%s" class="sm">09 ← נחיתה מזרחה</text>' % (px(6200), py(-830)))
svg.append('</svg>')
TY = R['types']; NAMES = {'AC-PR-01': 'PR פרטי', 'AC-LT-01': 'LT פרטי', 'AC-BJ-01': 'BJ מנהלים', 'AC-CN-01': 'CN מנהלים', 'AC-TB-01': 'TB משא קל', 'AC-RJ-01': 'RJ אזורי', 'AC-QJ-01': 'QJ אזורי', 'AC-NB-01': 'NB צר', 'AC-MW-01': 'MW גדול', 'AC-LG-01': 'LG ענק', 'AC-CG-01': 'CG משא גדול'}
def c(v): return '—' if v is None else ('%.2f' % v).rstrip('0').rstrip('.')
rows = []
for ac, r in TY.items():
    best90 = r.get('90-A4'); ret = r.get('RET-A3N') if r.get('RET-A3N') is not None else r.get('RET-A4')
    which = 'A3' if r.get('RET-A3N') is not None else ('A4' if r.get('RET-A4') is not None else 'אין — נשאר 90°')
    sav = '−%s' % c(best90 - ret) if ret is not None else '0'
    rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><b>%s</b></td><td>%s</td></tr>' % (NAMES.get(ac, ac), c(r.get('90-A2')), c(r.get('90-A3N')), c(best90), which, c(ret), sav))
Wt, Wr = R['world']['today'], R['world']['ret']
html = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>יציאה מהירה מהמסלול</title>
<style>:root{--bg:#f6f4ee;--ink:#1d2328;--mut:#5d6670;--grass:#9cb98a;--asph:#4a4f55;--paint:#f2f2ee;--yel:#e0b93a;--red:#c8402e;--c1:#1f8fd6;--c2:#e07a1f;--line:#d8d3c6}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15191d;--ink:#e8e6e0;--mut:#a3abb3;--grass:#3e5a36;--asph:#2a2e33;--paint:#d8d8d2;--line:#333a41}}
:root[data-theme=dark]{--bg:#15191d;--ink:#e8e6e0;--mut:#a3abb3;--grass:#3e5a36;--asph:#2a2e33;--paint:#d8d8d2;--line:#333a41}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,"Segoe UI",Arial,sans-serif}main{max-width:1000px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:4px 0 2px}h2{font-size:17px;margin:22px 0 6px}p,li{color:var(--ink)}.mut{color:var(--mut);font-size:13px}
svg{width:100%%;height:auto;display:block;border:1px solid var(--line);border-radius:6px}.lb{font-size:13px;fill:var(--ink);text-anchor:middle;font-weight:600}.sm{font-size:10px;fill:var(--ink)}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%%;font-size:14px}td,th{border-bottom:1px solid var(--line);padding:5px 7px;text-align:right}th{font-weight:600;color:var(--mut)}
.kpi{display:flex;flex-wrap:wrap;gap:10px}.kpi div{border:1px solid var(--line);border-radius:6px;padding:8px 12px;min-width:150px}.kpi b{font-size:20px;display:block}</style></head><body><main>
<h1>יציאה מהירה מהמסלול (D‑704 סעיף 1) — המספרים במחולל</h1>
<p class="mut">fieldexit · 17.11 · מהמחולל של fieldthru (ft_sim.py — אותן רגליים, אותו כלל מסלול של המשחק: נמוך מ-40, ‏y &lt; ‏−480). הלוח: 14 טיסות עם P6 (העולם של try8092). שלב 1 — מדידה, בלי בנייה.</p>
%s
<p class="mut">הצורה: מהקו האמצעי בקשת של 60 מ׳ אל 30°, ישר 51 מ׳ ב-30°, וקשת של 15 מ׳ אל דרום — נגמרת בנקודה של החיבור (A3 החדש x 8345 / A4 x 9190, ‏y ‏−280), ומשם ההסעה לעמדה כמו היום. יוצאים ב-25 מ׳/ש׳ (250 פיקס׳/ש׳) בלי לעצור. הקו האדום המקווקו — y ‏−480: מכאן המסלול פנוי.</p>
<h2>זמן התפוסה של נחיתה, לפי סוג (שניות)</h2>
<div class="tw"><table><tr><th>סוג</th><th>היום 90° ב-A2</th><th>90° ב-A3 החדש</th><th>היום 90° ב-A4</th><th>יציאה מהירה</th><th>התפוסה</th><th>חיסכון מול A4</th></tr>%s</table></div>
<p class="mut">ההאטה לפי הסוג (מרחק העצירה): קלים 11 מ׳/ש׳², בינוניים 8.2 (= הנחיתה של היום שיוצאת ב-A3 החדש), כבדים 6.4 (= היציאה של היום ב-A4). קלים צריכים 194 מ׳ עד 25 מ׳/ש׳ — היציאה המהירה של A3 מתחילה 217 מ׳ אחרי הנגיעה; בינוניים צריכים 261 מ׳ — רק של A4 (302 מ׳); הכבדים צריכים 334 מ׳ — אין מקום, נשארים ביציאה של היום (LG יוצא היום ב-A2 — 9 ש׳).</p>
<h2>הלוח של היום, כל נחיתה ביציאה המהירה שלה (באותו רגע נגיעה)</h2>
<div class="kpi"><div>המסלול תפוס<b>%s%% ← %s%%</b></div><div>שניות תפוסות במחזור<b>%s ← %s</b></div><div>הפער הממוצע<b>%s ← %s ש׳</b></div><div>פערים של 20 ש׳ ומעלה<b>%d ← %d</b></div><div>הפער הגדול<b>%s ← %s ש׳</b></div></div>
<ul><li>משתחררות %d שניות מסלול בכל מחזור של 720 ש׳ (13 נחיתות מתוך 14; LG נשאר).</li>
<li>הערכה (המסלול בלבד): טיסה נוספת צריכה ~34 ש׳ מסלול (נחיתה ~9, המראה ~17 בממוצע היום, ועוד המרווחים) — כלומר עד 2 טיסות נוספות, ‎+10 תנועות (70 → ~80 בחצי שעה). 88–92 צריך גם המראה קצרה יותר (ההמראות הן היום ~53%% מהתפוסה) ואת העמדות בדרום (GA4 / GA5 / GA7 / R3 — הקישור B).</li>
<li>הגדולים ב-P6: הפער הגדול לא משתנה (34.5 ש׳) — חלון של 55–60 ש׳ ייפתח רק בתכנון מחדש של הזמנים; יש יותר פערים של 20+ ש׳ לחבר. לא נמדד עדיין.</li>
<li>עוד לא נבדק: התנגשויות (OBB מול כל מה שרץ), הסעה ארוכה יותר לעמדות ממערב ל-A4 (P2–P5 יוצאים היום ב-A4 בכל מקרה), הגרר, והעמידה המינימלית.</li></ul>
<h2>מה הלאה (אחרי חידוש המכסה)</h2>
<ol><li>המחולל המלא: כל נחיתה ביציאה המהירה, בבדיקה המדויקת (כמו ft2_exitA3.py), ואחר כך הוספת טיסות (P6 / GA4 / GA5 / GA7 / R3) וספירת התנועות.</li>
<li>הבנייה: האספלט, הקו האמצעי הצהוב בקשת, השלטים (19l3 — חלק חדש משלי), והלו״ז (019l2).</li><li>הגדולים ב-P6 — מדידה; הגדר של רחבת המשא (HC / CG); P6 עצמה.</li></ol>
</main></body></html>''' % ('\n'.join(svg), '\n'.join(rows), Wt['busy_pct'], Wr['busy_pct'], Wt['busy_s'], Wr['busy_s'], Wt['mean_gap'], Wr['mean_gap'], Wt['gaps_ge20'], Wr['gaps_ge20'], Wt['max_gap'], Wr['max_gap'], round(Wt['busy_s'] - Wr['busy_s']))
open(out, 'w', encoding='utf-8').write(html); print('ok', len(html))
