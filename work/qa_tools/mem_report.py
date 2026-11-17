# 8.11 · mem_report.py — הדף של הזיכרון (R-89, ‏K‑239): בלי צילומים, עברית, טבלאות בלבד.
# python3 qa_tools/mem_report.py <final.json> <out.html> --before S7F271 --after try99N [--drop-before f.json] [--drop-after f.json]
#        [--vis vis_cmp.json] [--qa qa_dir/summary.txt] [--budget qa_tools/mem_budget.json] [--commit <sha>]
import json, sys, html, os, datetime
a = sys.argv[1:]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
FIN, OUT = a[0], a[1]
BEF, AFT = opt('--before', 'S7F271'), opt('--after')
D = json.load(open(FIN)); R = {r['tag']: r for r in D['runs']}
E = html.escape
def f1(x): return '' if x is None else ('%.1f' % x)
def sg(x): return '' if x is None else ('%+.1f' % x)
B = json.load(open(opt('--budget'))) if opt('--budget') else {'totalMB': 140, 'newZoneMB': 3, 'noiseMB': 2, 'zones': {}}
css = """
:root{--bg:#f7f6f2;--fg:#1d2329;--mut:#5d6873;--line:#d9d6cc;--card:#ffffff;--ok:#1d7a46;--bad:#b3261e;--acc:#2b5d8a;--hl:#eef3f8}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15191d;--fg:#e6e8ea;--mut:#9aa6b1;--line:#2c343b;--card:#1c2228;--ok:#5cc28a;--bad:#ff8a80;--acc:#8cb8e0;--hl:#1f2a34}}
:root[data-theme=dark]{--bg:#15191d;--fg:#e6e8ea;--mut:#9aa6b1;--line:#2c343b;--card:#1c2228;--ok:#5cc28a;--bad:#ff8a80;--acc:#8cb8e0;--hl:#1f2a34}
body{background:var(--bg);color:var(--fg);font:15px/1.55 "Segoe UI","Noto Sans Hebrew",Arial,sans-serif;margin:0;padding:0 16px 40px}
main{max-width:1100px;margin:0 auto}h1{font-size:24px;margin:22px 0 4px}h2{font-size:19px;margin:28px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
.sub{color:var(--mut);margin:0 0 14px}.cards{display:flex;flex-wrap:wrap;gap:10px}.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:150px;flex:1}
.card b{display:block;font-size:22px}.card span{color:var(--mut);font-size:13px}.ok{color:var(--ok);font-weight:600}.bad{color:var(--bad);font-weight:600}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--card)}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
th,td{padding:5px 9px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}th{background:var(--hl);font-weight:600}tr:last-child td{border-bottom:0}
td.n{text-align:left;direction:ltr}.mut{color:var(--mut)}ul{padding-inline-start:20px}li{margin:3px 0}code{direction:ltr;unicode-bidi:embed;font-size:13px}
"""
H = []
w = H.append
r0, r1 = R.get(BEF), R.get(AFT)
now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
w('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>דוח הזיכרון</title><style>%s</style></head><body><main>' % css)
w('<h1>הזיכרון לפי אזור — R-89 / K‑239</h1><p class="sub">בונה הזיכרון · ענף mem%s · %s · המדידה: %s</p>' % ((' · ' + E(opt('--commit'))) if opt('--commit') else '', now, E(B.get('metric', ''))))
# summary cards
w('<div class="cards">')
for t in R:
    r = R[t]; ok = r['final']['js'] <= B['totalMB']
    w('<div class="card"><span>%s · אחרי סיבוב</span><b class="%s">%s מ״ב</b><span>בפתיחה %s · קנבסים %s מ״ב</span></div>' % (E(t), 'ok' if ok else 'bad', f1(r['final']['js']), f1(r['open']['js']), f1(r['final']['cv']['mb'])))
w('</div>')
w('<p>היעד: %s מ״ב אחרי סיבוב, אחרי ניקוי זיכרון (K‑239). כל הבניות נמדדו באותה ריצה, אחת אחרי השנייה, כל אחת בדפדפן חדש, ורק כשאין דפדפן אחר במכונה (בדיקה כל 5 שניות; מדידה מחכה עד שהוא נגמר).</p>' % B['totalMB'])
# table per build
w('<h2>לפי בנייה</h2><div class="tw"><table><tr><th>בנייה</th><th>sha1</th><th>JS בפתיחה</th><th>JS אחרי סיבוב</th><th>העלייה בסיבוב</th><th>הגבוה בסיבוב</th><th>קנבסים בפתיחה (מ״ב / מספר)</th><th>קנבסים אחרי סיבוב</th><th>זיכרון התהליכים (PSS)</th><th>חיכה לבד (ש׳)</th></tr>')
for t, r in R.items():
    pk = max([z['js'] for z in r['zones']] + [r['open']['js']])
    w('<tr><td>%s</td><td class="n">%s</td><td>%s</td><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s / %d</td><td>%s / %d</td><td>%d</td><td>%s</td></tr>' % (E(t), r['sha1'], f1(r['open']['js']), f1(r['final']['js']), sg(r['final']['js'] - r['open']['js']), f1(pk), f1(r['open']['cv']['mb']), r['open']['cv']['n'], f1(r['final']['cv']['mb']), r['final']['cv']['n'], r['final']['pss']['total'], r.get('pausedS', '')))
w('</table></div><p class="mut">JS = ה-heap של הדף אחרי ניקוי (הקטנה מבין 3 דגימות, 0.7 שנייה זו מזו). קנבסים = כל הקנבסים החיים, רוחב × גובה × 4 — מחוץ ל-heap, מדווח ליד. PSS = כל תהליכי הדפדפן.</p>')
# per zone
if r0 and r1:
    Z0 = {z['z']: z for z in r0['zones']}; Z1 = {z['z']: z for z in r1['zones']}
    w('<h2>לפי אזור — לפני (%s) ואחרי (%s)</h2><p class="sub">התוספת של כל אזור = ה-JS אחרי הביקור בו פחות ה-JS אחרי האזור הקודם בסיבוב (A0 → H0, ‏A1 → H1 …). שלילי = מטמון של אזור קודם שהשתחרר.</p>' % (E(BEF), E(AFT)))
    w('<div class="tw"><table><tr><th>אזור</th><th>בנוי</th><th>JS לפני</th><th>תוספת לפני</th><th>JS אחרי</th><th>תוספת אחרי</th><th>התקציב</th><th>בתקציב</th><th>קנבסים: תוספת לפני / אחרי</th></tr>')
    for k in sorted(Z1, key=lambda k: (int(k[1:]), k[0])):
        z0, z1 = Z0.get(k, {}), Z1[k]; cap = B['zones'].get(k, B['newZoneMB']); ok = z1['dJs'] <= cap + B.get('noiseMB', 0)
        w('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class="%s">%s</td><td>%s / %s</td></tr>' % (k, 'כן' if z1.get('built') else '', f1(z0.get('js')), sg(z0.get('dJs')), f1(z1['js']), sg(z1['dJs']), f1(cap), 'ok' if ok else 'bad', 'כן' if ok else 'לא', sg(z0.get('dCv')), sg(z1.get('dCv'))))
    w('</table></div>')
# causes
C = json.load(open(opt('--causes'))) if opt('--causes') else []
if C:
    w('<h2>הגורמים — עשרת הגדולים</h2><p class="sub">%s</p><div class="tw"><table><tr><th>#</th><th>מה</th><th>סוג</th><th>לפני (מ״ב)</th><th>אחרי (מ״ב)</th><th>מה נעשה</th></tr>' % E('איך נמדד: אחרי סיבוב מהיר בכל האזורים, לולאת הפריימים נעצרת, ומרוקנים מטמון אחד בכל פעם — ההפרש אחרי ניקוי הוא מה שהוא החזיק (qa_tools/mem_drop.js; אבחון בלבד). JS — ב-heap; קנבס — בזיכרון הציור, מחוץ ל-heap.'))
    for i, c in enumerate(C, 1):
        w('<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="white-space:normal">%s</td></tr>' % (i, E(c['what']), E(c['kind']), E(str(c['before'])), E(str(c['after'])), E(c['done'])))
    w('</table></div>')
# budget
w('<h2>התקציב</h2><ul><li>היעד הכולל: <b>%s מ״ב</b> אחרי סיבוב, אחרי ניקוי (K‑239).</li><li>אזור חדש: <b>%s מ״ב</b> לכל היותר (ברירת מחדל, לאישורך), ועוד %s מ״ב לרעש של המדידה.</li><li>%s</li><li>הבדיקה: <code>BUDGET=qa_tools/mem_budget.json node qa_tools/mem_zones.js out.json build.html</code> — יציאה 1 כשאזור עובר את התקציב או כשהסך מעל היעד.</li></ul>' % (B['totalMB'], B['newZoneMB'], B.get('noiseMB', 0), E(B.get('rule', ''))))
if B.get('zones'):
    w('<p>אזורים עם תקציב משלהם (נמדדו מעל 3 מ״ב — עם סיבה):</p><ul>')
    for k, v in B['zones'].items(): w('<li>%s: %s מ״ב — %s</li>' % (E(k), v, E((B.get('why') or {}).get(k, ''))))
    w('</ul>')
if r1 and r1.get('budget'):
    bb = r1['budget']; w('<p>הבדיקה על %s: <span class="%s">%s</span> %s</p>' % (E(AFT), 'ok' if bb['ok'] else 'bad', 'עוברת' if bb['ok'] else 'נכשלת', E(' · '.join(bb['fails'][:12]))))
# perf
if r0 and r1 and r0.get('perf') and r1.get('perf'):
    w('<h2>הזמן לפריים</h2><p class="sub">זמן ה-JS של כל פריים (requestAnimationFrame), אותו זום (%s) ואותם מקומות, אחרי הסיבוב; "נסיעה" — המצלמה זזה ברצף מ-E3 ל-F5 ובחזרה. אלפיות שנייה.</p>' % f1(r1['zoom']))
    w('<div class="tw"><table><tr><th>מקום</th><th>חציון לפני</th><th>חציון אחרי</th><th>אחוזון 90 לפני</th><th>אחוזון 90 אחרי</th><th>פריימים לפני / אחרי</th></tr>')
    for k in r1['perf']['places']:
        p0, p1 = r0['perf']['places'].get(k, {}), r1['perf']['places'][k]
        w('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s / %s</td></tr>' % (E(k), p0.get('med', ''), p1['med'], p0.get('p90', ''), p1['p90'], p0.get('n', ''), p1['n']))
    w('</table></div>')
# visual
if opt('--vis') and os.path.exists(opt('--vis')):
    V = json.load(open(opt('--vis')))
    w('<h2>הבדיקה בעין</h2><p>%d צילומים של הקנבס של המשחק (14 מקומות, ביום ובלילה, פעמיים — לפני ואחרי סיבוב ברחבי העיר), במצב הדטרמיניסטי של המשחק (שעון קבוע, זרע קבוע): <b>%d זהים לגמרי</b>, %d בתוך הרעש של הכלי (ההבדל בין שתי ריצות של אותה בנייה), <span class="%s">%d מעבר לרעש</span>.</p>' % (len(V['rows']), V['same'], V['withinNoise'], 'ok' if not V['differ'] else 'bad', V['differ']))
    if V.get('note'): w('<p class="mut">%s</p>' % E(V['note']))
# qa
if opt('--qa') and os.path.exists(opt('--qa')):
    w('<h2>הבדיקות החוסמות</h2><div class="tw"><table>')
    for line in open(opt('--qa'), encoding='utf-8').read().splitlines():
        if line.startswith(('✓', '✗', 'אין החמרה', 'החמרה', 'סך הכול', 'נכשלו')): w('<tr><td style="white-space:normal">%s</td></tr>' % E(line))
    w('</table></div>')
w('</main></body></html>')
open(OUT, 'w', encoding='utf-8').write('\n'.join(H))
print(OUT, os.path.getsize(OUT))
