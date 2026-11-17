#!/usr/bin/env python3
# gen_page.py — brandin 17.11: הדף "מה שסומן 'לשמור' — מה נכנס למשחק" (טבלה לפי אזור; מה נשאר ולמה). בלי תמונות; HTML בלבד.
#  usage: python3 gen_page.py <keep_inventory.json> <probe.json|-> <out.html> <try> <commit>
import sys, json, html, collections
INV, PR, OUT, TRY, COMMIT = sys.argv[1:6]
inv = json.load(open(INV, encoding='utf-8'))
pr = json.load(open(PR, encoding='utf-8')) if PR != '-' else None
noscr = set((pr or {}).get('place', {}).get('noScreen', []))
cmiss = set((pr or {}).get('cityMissing', []))
omiss = set((pr or {}).get('opsMissing', []))
cnopos = set((pr or {}).get('cityNoPos', []))
BIG = {'ops:S15J-FIDS-01', 'ops:S15J-FIDS-09', 'ops:S15J-FIDS-10', 'ops:S15J-FIDS-11'}
FAM = {'terminal_hanging': 'השלטים התלויים בטרמינל', 'interior_fids': 'לוחות הטיסות בפנים', 'bridge_gate_screen': 'מסכי השערים על השרוולים', 'runway_taxiway': 'שלטי המסלול והמסלולונים',
       'building_plate': 'לוחות הזהות של המבנים', 'landside_building_sign': 'שלטי הצד היבשתי', 'operational_e4_plate': 'הלוחות התפעוליים (שערים, חניונים, הסעה)', 'parking_p_marker': 'סימני P',
       'counter_label': 'תוויות הדלפקים', 'crew_briefing_board': 'לוח התדריך של הצוות'}
def status(x):
    s, p, lv = x['sec'], x['part'], x['level']
    if s in ('library', 'poster'): return 'had', 'כבר במשחק (נבדק: מצויר בלי שגיאה)'
    if s == 'airport': return 'had', 'הלוגו המאושר המקורי — כבר במשחק (TC_BRANDS.rental)'
    if s == 'ops':
        if x['key'] in BIG: return 'left', 'לוח טיסות גדול: של המעצב — 2 טיסות לכל רשימה, של היום (074x3) — עד 8. לא הוחלף כדי לא לאבד טיסות — לאישורך (מוכן בדגל TCBI.bigFids)'
        if x['key'][4:] in omiss: return 'left', 'לא נמצא בעולם בבדיקה'
        return 'now', 'נכנס: ' + x['where'].split(' (')[0]
    if p == 'logo' or p == 'proposal':
        if (x.get('place') or '').replace('KISS', 'DROP') in noscr: return 'left', 'למקום אין מסך F במשחק — אין איפה להציג (הזהות / ההצעה מוכנות בקוד)'
        return 'now', 'נכנס: מסך המקום (F)' + (' — הלוגו בכותרת' if p == 'logo' else ' — שלט מתחת לכותרת (D‑631: לא מוסיפים שלט על מבנה בלי משטח)')
    if x['where'].startswith('BLD40') and lv != 'ok' and any(k.startswith('k') for k in ()): pass
    pf = (x.get('place') or '').replace('KISS', 'DROP') + ':' + p
    if pf in cmiss or pf in cnopos: return 'left', 'נבנה, אבל בבדיקה לא נמצא מצויר בעולם — לבירור'
    if lv == 'ok': return 'had', 'כבר במשחק — הפס של המשחק עם הלוגו המאושר (אפשר להחליף בעיצוב של המעצב: __TC_BRANDIN.TCBI.okToo)'
    return 'now', 'נכנס: ' + x['where']
rows = [x for x in inv if x['mark'] == 'keep']
redo = [x for x in inv if x['mark'] == 'redo']
for x in rows: x['st'], x['why'] = status(x)
REG = ['השדה', 'העיר', 'האי', 'הנמל', '62 הזהויות', 'פוסטרים']
S = collections.OrderedDict((r, collections.Counter()) for r in REG)
for x in rows: S[x['region']][x['st']] += 1; S[x['region']]['n'] += 1
def kindof(x):
    if x['sec'] == 'ops': return 'שילוט תפעולי — ' + FAM.get(x['where'].split('(')[-1].rstrip(')'), x['where'])
    if x['sec'] == 'library': return 'לוגו מקורי (62 הזהויות)'
    if x['sec'] == 'poster': return 'פוסטר אירוע — ' + ('לחזית 600×900' if x['part'] == 'facade' else 'למסך 960×600')
    if x['sec'] == 'airport': return 'לוגו ההשכרה בשדה (900×600)'
    if x['part'] == 'logo': return 'זהות מקומית (900×600)'
    if x['part'] == 'proposal': return 'הצעת שלט (120×24)'
    return 'שלט על משטח קיים — ' + x['where'].split(' (')[0]
K = collections.OrderedDict()
for x in rows: K.setdefault((x['region'], kindof(x)), collections.Counter())[x['st']] += 1
e = html.escape
H = ['''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>מה נכנס למשחק</title><style>
:root{--bg:#f4f1ea;--fg:#1c2628;--muted:#5b6869;--card:#fff;--line:#d9d4c8;--had:#1e7a46;--now:#2a6fc4;--left:#b0541a}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d;--had:#4cc483;--now:#6aa8f0;--left:#f0a06a}}
:root[data-theme="dark"]{--bg:#111a1c;--fg:#e8ede9;--muted:#9aa7a6;--card:#1a2427;--line:#2c3a3d;--had:#4cc483;--now:#6aa8f0;--left:#f0a06a}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Arial,"Noto Sans Hebrew",sans-serif}main{max-width:1100px;margin:auto;padding:16px}
h1{font-size:25px;margin:.3em 0}h2{font-size:19px;margin:1.4em 0 .4em}.muted{color:var(--muted)}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;font-size:14px}
td,th{border-bottom:1px solid var(--line);padding:7px 8px;text-align:right;vertical-align:top}th{font-weight:700;background:color-mix(in srgb,var(--line) 35%,transparent)}
td.n{font-variant-numeric:tabular-nums;white-space:nowrap}.had{color:var(--had);font-weight:700}.now{color:var(--now);font-weight:700}.left{color:var(--left);font-weight:700}
.sum{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}.sum div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px}.sum b{font-size:22px;display:block}
details{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:6px 10px}summary{cursor:pointer;font-weight:700}
ul{margin:.3em 0;padding-inline-start:1.2em}li{margin:.2em 0}
</style></head><body><main>''']
tot = collections.Counter()
for x in rows: tot[x['st']] += 1
H.append('<h1>מה שסימנת "טוב — לשמור" — מה נכנס למשחק</h1>')
H.append('<p class="muted">לפי הקובץ שסימנת (owner_marks_1117.json): %d חלקים מסומנים "לשמור" ו-%d "לעצב מחדש". מה שסומן "לעצב מחדש" — לא נגעתי בו; הוא נשאר כמו שהוא עד שתשלח עיצוב חדש. הניסיון: %s · הענף t17_brandin %s · 17.11.2026.</p>' % (len(rows), len(redo), e(TRY), e(COMMIT)))
H.append('<div class="sum"><div><b>%d</b>חלקים "לשמור"</div><div><b class="had">%d</b>כבר היו במשחק</div><div><b class="now">%d</b>נכנסו עכשיו</div><div><b class="left">%d</b>נשארו</div></div>' % (len(rows), tot['had'], tot['now'], tot['left']))
H.append('<h2>לפי אזור</h2><div class="tw"><table><thead><tr><th>אזור</th><th>"לשמור"</th><th>כבר במשחק</th><th>נכנס עכשיו</th><th>נשאר</th></tr></thead><tbody>')
for r, c in S.items():
    if c['n']: H.append('<tr><td>%s</td><td class="n">%d</td><td class="n had">%d</td><td class="n now">%d</td><td class="n left">%d</td></tr>' % (e(r), c['n'], c['had'], c['now'], c['left']))
H.append('</tbody></table></div>')
H.append('<h2>לפי סוג</h2><div class="tw"><table><thead><tr><th>אזור</th><th>סוג</th><th>"לשמור"</th><th>כבר במשחק</th><th>נכנס עכשיו</th><th>נשאר</th></tr></thead><tbody>')
for (r, k), c in sorted(K.items(), key=lambda a: (REG.index(a[0][0]), a[0][1])):
    H.append('<tr><td>%s</td><td>%s</td><td class="n">%d</td><td class="n had">%d</td><td class="n now">%d</td><td class="n left">%d</td></tr>' % (e(r), e(k), sum(c.values()), c['had'], c['now'], c['left']))
H.append('</tbody></table></div>')
H.append('''<h2>איך זה נכנס</h2><ul>
<li><b>השילוט התפעולי של השדה (89):</b> הציור של המעצב (airport-ops) על אותם משטחים, באותו מקום ובאותו גודל — השלטים התלויים, לוחות הטיסות ומסכי השערים (עם הטיסות החיות), שלטי המסלול, לוחות המבנים, הלוחות התפעוליים, סימני P, הדלפקים ולוח התדריך.</li>
<li><b>שלטי העיר על משטח קיים:</b> הלוח של המעצב במקום הלוח הישן — החזיתות של C2 ו-D2, השלטים על הפאה, לוחות המתקנים, והשלטים שבתוך ציור הבניין (השוק, בית החולים, המחסנים, המרקיזה של התיאטרון עם ההצגה של הערב).</li>
<li><b>הזהות המקומית (900×600):</b> הלוגו בכותרת של מסך המקום (F).</li>
<li><b>הצעת השלט (120×24):</b> למקום שאין בו היום משטח לשלט — לפי D‑631 לא מוסיפים שלט חדש על המבנה; ההצעה מוצגת במסך המקום (F), מתחת לכותרת. לאישורך: אם תרצה — משטח חדש בעולם, מקום אחר מקום.</li>
<li><b>62 הזהויות, הלוגו של ההשכרה והפוסטרים:</b> כבר היו במשחק (טבלת המותגים, ‏074n3s) — נבדק שכל אחד מצויר בלי שגיאה.</li>
<li><b>חידוש 01 · מזנוני השדה (אישרת ב-19:00):</b> ששת המזנונים — השלט והלוגו המאוירים החדשים במקום הזמניים של airlogos: השלט התלוי של המזנון, והלוגו במרכז לוח התפריט מעל הדלפק. הציור מוקטן לגודל של השלט במשחק (כ-60 ק״ב למזנון במקום 470–720). בדיקת לפני / אחרי: Refined_check.html.</li>
<li><b>מה שסומן "לעצב מחדש":</b> לא נגעתי. שלטי השדה של airlogos (החנויות, המזנונים, חברות התעופה, חזיתות הטרמינל) נשארים במשחק כזמניים — יוחלפו כשיגיע העיצוב החדש.</li></ul>''')
left = [x for x in rows if x['st'] == 'left']
H.append('<h2>מה נשאר ולמה (%d)</h2>' % len(left))
if left:
    H.append('<div class="tw"><table><thead><tr><th>אזור</th><th>מקום</th><th>חלק</th><th>למה</th></tr></thead><tbody>')
    for x in left: H.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(x['region']), e(x['name'] + (' · ' + x['place'] if x.get('place') else '')), e(x['part']), e(x['why'])))
    H.append('</tbody></table></div>')
else: H.append('<p>לא נשאר כלום.</p>')
H.append('<h2>כל הפריטים, לפי אזור</h2>')
for r in REG:
    L = [x for x in rows if x['region'] == r]
    if not L: continue
    H.append('<details><summary>%s — %d</summary><div class="tw"><table><thead><tr><th>פריט</th><th>חלק</th><th>גודל</th><th>מצב</th></tr></thead><tbody>' % (e(r), len(L)))
    for x in L:
        nm = x['name'] + (' · ' + x['place'] if x.get('place') else '') + (' · ' + x['text'] if x.get('text') and x['text'] != x['name'] else '')
        H.append('<tr><td>%s</td><td>%s</td><td class="n">%s</td><td class="%s">%s</td></tr>' % (e(nm), e(x['part']), e(x.get('size') or ''), x['st'], e(x['why'])))
    H.append('</tbody></table></div></details>')
H.append('<p class="muted">הציור של כל פריט — בדף הסקירה (Brand_signs_review.html). בדיקה במשחק: window.__TC_BRANDIN (audit, stats).</p></main></body></html>')
open(OUT, 'w', encoding='utf-8').write('\n'.join(H))
print(OUT, dict(tot), {r: dict(c) for r, c in S.items()})
