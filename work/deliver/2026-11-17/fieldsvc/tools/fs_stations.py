#!/usr/bin/env python3
# fs_stations.py — fieldsvc: סעיף "התחנות והמחזור" בציור — מפה (SVG מהנתונים של S15D) של התחנות: חוות הדלק ופריקת המכלית מבית הזיקוק, נקודת המים והניקוז,
# מטבח הקייטרינג, והדרכים אליהן; והטבלה: קיבולת, צריכה לביקור, איפה מתמלאים, מתי. הפלט: stations.html (נכנס לדף).
import json, os, subprocess, html
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = '/home/user/tc_root/tc/pkg/work/src_game_t17_fieldsvc/parts/019l_S15_data.js'
D = json.loads(subprocess.check_output(['node', '-e', f"const fs=require('fs');const s=fs.readFileSync('{SRC}','utf8');const {{S15D}}=new Function(s+';return {{S15D,S15SIM}}')();console.log(JSON.stringify({{service:S15D.service,pockets:S15D.pockets,base:S15D.base,stands:S15D.stands,fence:S15D.fence,spots:S15D.spots}}))"]))
E = html.escape
bx = [5900, 600, 9620, 2600]; S = .22; W = (bx[2] - bx[0]) * S; H = (bx[3] - bx[1]) * S
X = lambda x: (x - bx[0]) * S; Y = lambda y: (y - bx[1]) * S
def R(r, cls, extra=''): return f'<rect x="{X(r[0]):.1f}" y="{Y(r[1]):.1f}" width="{(r[2]-r[0])*S:.1f}" height="{(r[3]-r[1])*S:.1f}" class="{cls}" {extra}/>'
g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" class="map" role="img" aria-label="התחנות של רכבי השירות בשדה">', f'<rect width="{W:.0f}" height="{H:.0f}" class="apron"/>']
g.append('<polyline points="' + ' '.join(f'{X(p[0]):.1f},{Y(p[1]):.1f}' for p in D['fence']) + '" class="fence"/>')
for r in D['service']: g.append(R(r['rect'], 'road' + (' ow' if r.get('oneway') else '')))
for k, q in D['pockets'].items(): g.append(R(q, 'pocket'))
for b in D['base']: g.append(R(b['rect'], 'base')); g.append(f'<text x="{X((b["rect"][0]+b["rect"][2])/2):.1f}" y="{Y(b["rect"][3])-3:.1f}" class="lab">{E(b["id"].replace("AIR-",""))}</text>')
for k, s in D['stands'].items(): g.append(f'<circle cx="{X(s["cx"]):.1f}" cy="{Y(s["nose"]):.1f}" r="3" class="stand"/><text x="{X(s["cx"]):.1f}" y="{Y(s["nose"])+12:.1f}" class="lab">{k}</text>')
ST = [('fuel', 'חוות הדלק (קיימת — 074n: המשאבה, המד, המילוי)', [7958, 1308, 8138, 1503], '#d6403a'),
      ('tank', 'פריקת המכלית מבית הזיקוק (חדש) — מעבר לגדר, בצד היבשה', [7790, 1360, 7855, 1450], '#a8322c'),
      ('ws', 'נקודת המים והניקוז (קיימת — 074n, בכיס P4|P5)', [8030, 700, 8128, 732], '#2d8fd8'),
      ('ws2', 'נקודת מים וניקוז שנייה בדרום (חדש — ל-R / GA)', [8470, 2216, 8600, 2244], '#2d8fd8'),
      ('kit', 'מטבח הקייטרינג — רציף הטעינה (חדש, ברחוב הבסיס)', [8160, 1310, 8330, 1360], '#2f6fd0')]
for k, he, r, c in ST:
    g.append(R(r, 'st', f'style="fill:{c}"')); g.append(f'<text x="{X(r[2])+4:.1f}" y="{Y((r[1]+r[3])/2)+4:.1f}" class="stl">{E(he.split(" (")[0])}</text>')
g.append('</svg>')
rows = [('מכלית דלק (FT)', '30,000 ל׳ (G77_FI)', 'לפי הסוג: קל 200–300, מנהלים 1,500, אזורי 3,000–4,500, צר 6,000–8,000, רחב 20,000+ (043:g77FiUp)', 'חוות הדלק — אחרי כל ביקור, כשנשאר פחות מהביקור הבא (D‑111: "מתמלאים לפני שחונים")', 'המשאבה, הצינור, המד של המכלית עולה והמד של החווה יורד (046:s6bFillAct)'),
        ('חוות הדלק', 'המכלים של AIR-BASE-4', 'כל מילוי של מכלית', 'מכלית הכביש FUEL-01 מבית הזיקוק T-103 (074w_logi: lgwFuelTick — סף ⇒ סבב) פורקת בתחנה שליד הגדר', 'המכלית מגיעה מהעיר, צינור דרך הגדר, המד של החווה עולה'),
        ('מכלית מים (WT)', '1,200 ל׳', '120–250 ל׳ לביקור', 'נקודת המים — הקרובה (צפון / דרום)', 'הארון, הצינור הכחול, המד'),
        ('רכב שירותים (LV)', '800 ל׳ פסולת', '80–200 ל׳ לביקור', 'נקודת הניקוז — הקרובה', 'הצינור החום אל הניקוז'),
        ('קייטרינג (CT)', 'עגלות: מלא 12 / קטן 4', 'לפי הנוסעים (6–12 עגלות)', 'מטבח הקייטרינג — אחרי כל ביקור (העגלות הריקות יוצאות, המלאות נכנסות)', 'התא עולה לגובה הרציף, עגלות עוברות'),
        ('חשמל קרקע (GP)', 'סולר', 'קטן', 'חוות הדלק — פעם במשמרת', 'כמו המכלית')]
tr = ''.join('<tr>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in rows)
out = f'''<h2>5. התחנות והמחזור — כל רכב מתרוקן בעבודה ומתמלא בתחנה שלו (הבעלים 15:35)</h2>
<p class="meta">קיים במשחק (074n, מהמנוע הישן): חוות הדלק עם המשאבה והמד (S6B_DEPOT → S15G_DEP), נקודת המים והניקוז (S6B_WS → S15G_WS), ספר המילוי (043:G77_FI — קיבולת לכל סוג, g77FiUp — כמה לכל מטוס), המד על כל מכלית. חדש: פריקת מכלית הכביש מבית הזיקוק (החיבור לשרשרת הקיימת 074w_logi — FUEL-01 / T-103; העטיפה של sealife על lgwFuelTick נשמרת), נקודת מים וניקוז שנייה בדרום, מטבח הקייטרינג. התחנות — מחוץ למסלולי ההסעה ולעמדות, ליד דרכי השירות (המפה).</p>
<div style="overflow-x:auto">{"".join(g)}</div>
<table class="t"><thead><tr><th>רכב / תחנה</th><th>קיבולת</th><th>לביקור</th><th>איפה ומתי מתמלא / מתרוקן</th><th>מה רואים</th></tr></thead><tbody>{tr}</tbody></table>
<div class="note">הבדיקה החוסמת (שלב 2): אף רכב לא יוצא לעבודה בלי מספיק (המלאי שלו ≥ מה שהביקור צריך); כל מילוי וריקון נרשם (ספר G77_FI לכל רכב); המלאי של חוות הדלק לא יורד לאפס לאורך יום משחק (4 מחזורים של 720 ש׳); כל רכב מגיע לתחנה שלו בדרכים (בלי חפיפה — אותה בדיקה של s15k / s15_sim_no_overlap).</div>'''
open(os.path.join(HERE, 'stations.html'), 'w', encoding='utf-8').write(out); print('ok', len(out))
