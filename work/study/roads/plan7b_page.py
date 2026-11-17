# 30.10 · batch 7b: the page of the road plan (study/roads/city_plan.html) — every choice with one sentence why.
import json, math, html
import plan7b_svg as SV
W = '/home/claude/work/study/roads'
P = json.load(open(W + '/city_plan.json'))
GR = json.load(open(W + '/game_roads.json')); P['_old_ids'] = [x['id'] for x in GR['edges']]
CLS = P['classes']; N = {n['id']: n for n in P['nodes']}
USE_HE = {t['type']: t.get('he') or t['type'] for t in json.load(open('/home/claude/work/plan600/data/uses.json'))['types']}
M = SV.model(P, GR)
e = lambda s: html.escape(str(s))
def seglen(rid): return sum(s['len_m'] for s in P['segments'] if s['road'] == rid)
out = []
A = out.append
A('''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>תוכנית הדרכים</title><style>
:root{--bg:#fbfaf6;--fg:#1f2328;--mut:#626a73;--line:#dedbd2;--card:#fff;--art:#c9442c;--col:#e59a2f;--loc:#8a8f96;--ok:#1d7a3a;--bad:#b42318;--tmp:#a0137f}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16181b;--fg:#e8e6e1;--mut:#a3a9b1;--line:#33373d;--card:#1e2125}}
:root[data-theme="dark"]{--bg:#16181b;--fg:#e8e6e1;--mut:#a3a9b1;--line:#33373d;--card:#1e2125}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,"Segoe UI",Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:20px 16px 60px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:34px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}h3{font-size:16px;margin:18px 0 8px}
.mut{color:var(--mut)}.small{font-size:13px}
img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card)}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:right;vertical-align:top}
th{font-weight:600;color:var(--mut);font-size:13px}td.id{white-space:nowrap;font-family:ui-monospace,Menlo,monospace;font-size:13px;direction:ltr;text-align:right}
.wrap{overflow-x:auto}.tag{display:inline-block;padding:0 7px;border-radius:9px;font-size:12px;color:#fff}
.t-arterial{background:var(--art)}.t-collector{background:var(--col)}.t-local{background:var(--loc)}.t-track{background:#a27c52}
.ok{color:var(--ok);font-weight:600}.bad{color:var(--bad);font-weight:600}.tmp{color:var(--tmp)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}.grid.st{grid-template-columns:repeat(auto-fill,minmax(360px,1fr))}.zc{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}
.zc img{border:0}.zc b{font-size:15px}.pill{font-size:12px;color:var(--mut)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px;align-items:start}.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
ul{margin:6px 0;padding-inline-start:20px}
''' + SV.STYLE + '''</style></head><body>''' + SV.defs(P, GR, M) + '''<main>''')
tt = P['totals']
A(f"<h1>{e(P['title'])}</h1><div class='mut'>7ב · {e(P['at'])} · {e(P['by'])} · <span class='small'>הנתונים בקובץ התוכנית שליד הדף · המפות מצוירות בדף עצמו, בלי תמונות</span></div>")
A("<div class='box' style='margin-top:14px'><b>מה חדש בסבב 7 (2.11 — הביקורת של 05:30: R-64, ‏R-61, ‏R-65).</b> "
  "המפה הושלמה מול תוכנית האב: כל פריט שהיה חסר או חלקי בטבלת ההתאמה נוסף בגודל אמיתי, עם הגישה שלו, בלי חפיפה לכבישים, למסילות ולמגרשים. "
  "<b>בשדה (שלב 8):</b> אורות הגישה של 09 ו-27, שטח הבטיחות והמשדר בקצה המסלול, דרך ההיקף לאורך הגדר, ‏P‑WEST, ‏P‑RENT, מלון השדה והצוותים, גשר הולכי הרגל AIR‑1, "
  "המגדל על גג הטרמינל, מפרץ המילוי של המכליות, הפינות לסמי, הצומת AIR‑K, קומת הקרקע של החניון הרב-קומתי, שער העובדים ב-x 7860, כיסי הציוד, המעברים המסומנים והרצת המנועים. "
  "<b>בעיר:</b> חניון התחנה עם E3‑N1, הקניון עם החניון ושורת החנויות, עמדות הדיג, המיני גולף ומגרש המשחקים באגם, מסלול הריצה ב-A4, ארבעת בלוקי המכולות ומגרש שמור למסוף הנפט, "
  "המלון של D2 על מגרש גדול יותר, ומועדון השייט, השכרת הסירות והדלק במרינה. "
  "<b>בים:</b> אגן המרינה עם 4 מזחים ו-60 מקומות, מפרץ הדיג עם מזחים וסירות, המזח השני ועמדות הדיג בחוף, מזח הגוררות בפער C6 / D6, אסדת הגז עם המנחת, ונתיבי השיט עם המצופים. "
  "<b>ביבשה ובאי:</b> קווי הגובה וההצללה של A0, שביל ההליכה ב-A1, השבילים במדרון המערבי של האי, ודרך השירות למגדלור ולמנחת (נבדקה). "
  "<b>R-61:</b> כל המנחתים לפי טבלה אחת, עם מסוק בגודל אמיתי; מנחתי גג על תחנת הכיבוי ובסיס האמבולנסים ב-A4. <b>R-62:</b> תחנת הכיבוי — 5 תאים. "
  "<b>R-65:</b> חמישה מלונות, כל אחד על מגרש. "
  "<b>10 בדיקות קבועות חדשות</b>, אחת לכל סוג חדש — והטבלה שבסוף הדף. כל ברירת מחדל מסומנת לאישורך.</div>")
A("<div class='box' style='margin-top:14px'><b>מה חדש בסבב 6 (1.11).</b> "
  "<b>טבלת חתכים אחת</b> (road_sections.json, R-42): לכל סוג דרך החתך שבמשחק היום (נקרא מהבנייה: נתיב 4.4 מ׳, מדרכה 2 מ׳) והחתך של התוכנית (D‑305, נתיב 3.9 מ׳). המפה קוראת ממנה, והבנייה של המשחק תיבדק מולה. "
  "<b>האזורים שנבנו נקראים מהקבצים שלהם:</b> ‏B4 בגרסה 5 (הסופר בצפון, 41 חניות בגודל 2.8 × 5.6 מ׳ ושני חניונים תת-קרקעיים, מגרש כדורסל) ו-B3 בגרסה 5.2 (15 בתים פרטיים, בתים טוריים ובניין דירות קטן, 4 סמטאות ללא מוצא). "
  "בית ספר 2 יצא (D‑325), ועמדת השירות של B3 עוברת לתחנת הדלק של C4 (D‑326). התחנה של קו 6 ברחוב השכונה (ST-19) יצאה (D‑330). "
  "<b>תחנות מול צמתים</b> נמדדות מקצה הצומת: 20 מ׳ לפני הצומת שלפנים, ו-10 מ׳ אחרי הצומת שמאחור (D‑332). "
  "בדיקה קבועה חדשה: המגרשים של אזור שנבנה עומדים מול רוחב הכבישים במשחק. "
  "<br><b>סבב 6ב (1.11, 13:00):</b> ‏<b>C4 מפורט</b> לפי טבלת השימושים, כל מבנה בגודל האמיתי שלו במשחק: חנות כלי העבודה בפינה הצפונית-מערבית, תחנת דלק 2 על שדרת המרכז, תחנת כיבוי 2 בקצה הדרום-מערבי, המחסן, המפעל, מסוף הרציפים ומשרד השילוח, וחיץ עצים מול C3. "
  "תחנת הדלק שהייתה ב-C2 ותחנת הכיבוי שהייתה בצפון C5 יצאו מהמפה (R-44 (7), ‏D‑260). "
  "ב-C5, בבלוק שהתפנה: משרד השילוח, תחנת המשנה, מסוף הרציפים והמוסך. בית הקפה, השירותים וביתן השער נמצאים בחניון המשאיות. "
  "בבלוק החדש עובר רחוב חצר המפעלים, ולכן ארבעה מבנים זזים 14 עד 26 מ׳ מהמקום שלהם במשחק. ההזזה מחכה לאישורך (D‑334). "
  "<b>בדיקה קבועה חדשה (R-43):</b> אין שטח פנוי של 15 × 15 מ׳ ומעלה בלי שימוש. נמצאו 31 שטחים ב-17 אזורים, וכל אחד קיבל שימוש מתוכנית האב, מטבלת השימושים או מהקובץ של האזור. "
  "<br><b>סבב 6ג (1.11, 13:40):</b> הכניסות לחניונים ולסמטאות של B3 ו-B4 צוירו בצד הלא נכון של הכביש, ועכשיו הן בצד שלהן. בגלל זה המפרץ של ST-18, על שדרת המערב ליד B4, זז 4 מ׳ צפונה, אל מעבר לכניסה לנתיב של החניון. "
  "הקצה הישן של העורק האמצעי ב-B3 יצא גם מהמשחק, והגינה של B3 גדלה לפינה. נוספה רשימה אחת של שמות אזורים ורחובות (names.json), שהמשחק קורא ממנה (R-51). "
  "<br><b>סבב 6ד (1.11, 14:00) — מסילת העקיפה (R-47):</b> העקיפה יוצאת עכשיו מפס ב׳ ב-y 2900, מצפון לשלושת מעברי הפסים (X-P, ‏X-N ו-X-S), ולא ב-y 4660. "
  "כך רכבת משא מהנמל עוברת לפס ב׳ ב-X-P, ורכבת מהחצר עוברת לפס ב׳ ב-X-N, ושתיהן עולות על העקיפה לפני התחנה המרכזית, בלי להתהפך. מסילת בית הזיקוק יוצאת מ-P1 בקשת אמיתית ולא בזווית ישרה. "
  "<b>בדיקה קבועה חדשה:</b> מסלולי הרכבות — לכל זרימה (מהנמל ומהחצר אל מסוף רכבת–אוויר בעקיפה של התחנה, מהנמל אל בית הזיקוק, מהחצר אל הנמל, מהאי אל התחנה) מסלול רציף, וכל מסוט בכיוון הנסיעה. על המסילה הקודמת הבדיקה נכשלת. "
  "המחיר: רכבת משא עוברת ליד תחנת החוף העתידית בפס ב׳, בצד הרחוק מהרציף. ברירת מחדל לאישורך (D‑335). "
  "<br><b>סבב 6ה (1.11, 14:10) — ממצאי R-46 ו-R-45:</b> המפרצים במסוף E3 מצוירים עכשיו בגודל שבבדיקה — 16 × 3.5 מ׳ בין הקווים, ומקומות ההמתנה 15 מ׳; הטקסט של הבדיקה מחושב מהמידות. "
  "ליד הצומת J46_16: 20 המטרים שבביקורת הם עד הקו הקפוא של השדה (R-32), והמחסום עצמו נמצא 80 מ׳ מזרחה, ב-x 5600, כמו ב-D‑160. לפניו שני נתיבי בדיקה ל-19 מכוניות ונתיב עקיפה לקו 4 ולחירום. "
  "במפה נוספו המחסום, גלאי תור מיד אחרי מעבר החצייה, וקופסה צהובה על הצומת. ההצרה מ-3 ל-2 נתיבים עברה אל אחרי המחסום (x 5600–5749), לפני גשר הרכבת. "
  "<b>בדיקה קבועה חדשה:</b> התור לשער לא מגיע לצומת. לאישורך (D‑336). "
  "<b>מספרי הקווים (R-45):</b> המפה לוקחת את המספרים של היום (D‑243): קו 4 נשאר קו השדה, קו 2 — הקניון והכפר, קו 3 — התעשייה והנמל, קו 5 — המרינה, החוף והאי. "
  "טבלה אחת בסעיף הקווים: הקו היום, הקו במפה ומספר האוטובוסים בכל אחד (D‑337). "
  "<br><b>סבב 6ו (1.11, 16:30) — C3 כמו במשחק, ו-8 מ׳ בין מסוטים (R-57, ‏R-47):</b> C3 נקרא עכשיו מהקובץ של האזור (c3v3.json), כמו B3 ו-B4 — אותו מקור כמו הגיליון והמשחק (S7F187): "
  "חמש הווילות בגודל שלהן, כל אחת עם המשטח והחניות שלה; השער של בית השחקן יוצא מהצד המערבי של מעגל הסיבוב אל הכנף המערבית; המנחת זז 4 מ׳ מזרחה, כדי שהמבנה למסוק של רמה 8 יהיה מחוץ לשטח הבטיחות. "
  "החניון האחורי של C2 יצא מהמשחק בשביל שדרת השדה (D‑341). "
  "<b>בדיקה קבועה חדשה (R-47):</b> לפחות 8 מ׳ בין שני מסוטים על אותה מסילה. היא מצאה שלושה: מעבר הפסים W1–W2 יצא מאותה נקודה כמו המסוט של P1 — זז 8 מ׳ מזרחה; בחצר הרכבות שני המסוטים בין הפסים היו 1.6 מ׳ מהכניסות — עכשיו 8.4 מ׳ ו-20 מ׳.</div>")
A("<div class='box' style='margin-top:14px'><b>מה זה.</b> רשת דרכים חדשה לכל המפה, לא קשורה לכבישים של היום — מהיום נלקח רק השטח (הים, החוף, האגם, האי). "
  "שלושה דברים קבועים: השדה (R-32, רק שלושת השערים), קווי הרכבת וגשר האי. "
  f"<br><b>במספרים:</b> {tt['nodes']} צמתים, {tt['segments']} קטעים, " + ', '.join(f'{k} {v} ק"מ' for k, v in tt['km'].items()) +
  f"; {tt['signals']} רמזורים, {tt['roundabouts']} כיכרות, {tt['riro']} צמתי ימינה-בלבד; {tt['temp']} חיבורים זמניים במעבר."
  f"<br><b>האגם:</b> האגם של B2 מורחב אל B1 לפי תוכנית האב (D‑13, GATE‑100) — אגם אחד, {P['terrain']['lake']['area_m2']:,} מ״ר (היום {P['terrain']['lake']['today_m2']:,}); החצי הדרומי, עם הדיג, בית הקפה והקיוסק, נשאר כמו היום."
  f" <b>האוטובוסים:</b> {len(P['routes']['bus'])} קווים חדשים על הרשת החדשה, כולם מהמסוף ב-E3 ({len(P['bus']['terminal']['bays'])} מפרצים ו-{len(P['bus']['terminal']['hold'])} מקומות המתנה), {len(P['bus']['stops'])} תחנות, וחניון לילה ב-D5."
  f"<br><b>העורק הראשי 3+3:</b> שדרת השדה משער הנוסעים עד שדרת המרכז, ושדרת המזרח מהשדה עד הנמל. <b>אחרי שער הנוסעים — 2 נתיבים לכל כיוון עד הטרמינל</b> (הבעלים, 1.11): מתחת לגשר הרכבת, בלולאת הטרמינל ובדרך החזרה; הירידה מ-3 ל-2 בהצרה מסומנת אחת אחרי השער (x 4800–5400), לא בצומת."
  f" <b>העתיד:</b> השדה של שלב 8 (חלק ו, D‑262), האי של D‑259 עם הגשר והרכבת בשני פסים, מסילת ההיפוך ומסילת בית הזיקוק; {len(P['lots'])} מגרשים חדשים בכל האזורים, לכל אחד כניסה מדרך.</div>")
A("<h2>מפת העתיד</h2><p class='mut small'>זו המפה של העיר כשכל התוכנית בנויה — המקור לכל השרטוטים של האזורים. כל מה שעוד לא בנוי מסומן בפסים ובקו מקווקו. "
  "גלגלת, צביטה או הכפתורים להגדלה; גרירה להזזה. ריחוף (בטלפון — נגיעה) על דרך, צומת, מגרש או אזור מראה מה זה ומאיזו דרך מגיעים אליו. "
  "חמשת הכפתורים מציגים ומסתירים שכבה בכל המפות בדף. השמות נשארים באותו גודל על המסך ולא עולים זה על זה — שם שאין לו מקום מופיע כשמגדילים.</p>" + SV.city_svg(P, M))
A(SV.legend_html(P, M))
A("<h3>מבטים קרובים — מאותה מפה</h3><div class='grid2'>" + ''.join(f"<div class='zc vw'>{SV.view_svg(P, M, vb, t)}<b>{e(t)}</b></div>" for vb, t in (
    ((4700, -950, 9700, 2700), 'השדה העתידי — שלב 8 (חלק ו, D‑262)'), ((5700, 4900, 9700, 7800), 'האי (D‑259) והגשר האלכסוני — כביש ושני פסי רכבת'),
    ((2300, 3300, 6400, 5300), 'הנמל, מסילות הנמל, חניון הלילה של האוטובוסים ו-E3'), ((4750, 1650, 5800, 2350), 'מסוף האוטובוסים של E3 — 12 מפרצים ומקומות המתנה'),
    ((6150, 1780, 7250, 2620), 'סבב 7 — אגן המרינה: 4 מזחים, 60 מקומות, המועדון ומלון הים'), ((4780, 960, 5800, 1800), 'סבב 7 — P‑WEST, ‏P‑RENT, מלון השדה וגשר AIR‑1'),
    ((1200, 4550, 2450, 5500), 'סבב 7 — החוף, שני המזחים, עמדות הדיג ומפרץ הדיג'), ((-60, -880, 1260, 880), 'סבב 7 — קווי הגובה של A0 ושביל ההליכה ב-A1'),
    ((7150, 1880, 9600, 2560), 'סבב 7 — המנחתים לפי הטבלה, כיסי הציוד, המעברים והרצת המנועים'), ((2350, 4300, 3900, 5600), 'סבב 7 — בלוקי המכולות, מסוף הנפט ומזח הגוררות'))) + "</div>")
A("<h2>ההיררכיה — ולמה</h2><div class='box'><ul>")
for c in ('main', 'arterial', 'collector', 'local', 'oneway', 'track'):
    A(f"<li><span class='tag t-{c}'>{e(CLS[c]['he'])}</span> {e(CLS[c]['lanes'])} · רוחב {CLS[c]['width_m']} מ׳ · {CLS[c]['speed']} קמ\"ש · {e(CLS[c]['sigLeft'])} — {e(CLS[c]['why'])}</li>")
A("</ul><h3>כללים</h3><ul>")
RULE_HE = {'scale': 'קנה המידה', 'R15': 'R-15', 'R16': 'R-16', 'riro': 'ימינה בלבד', 'junctions': 'הצמתים', 'driveways': 'הכניסות', 'lane_width': 'רוחב הנתיב'}
for k, v in P['rules'].items(): A(f"<li><b>{e(RULE_HE.get(k, k))}</b>: {e(v)}</li>")
A("</ul></div>")
A("<h2>הדרכים</h2><div class='wrap'><table><tr><th>מזהה</th><th>שם</th><th>סוג</th><th>נתיבים</th><th>אורך</th><th>משאיות</th><th>למה</th></tr>")
for r in P['roads']:
    A(f"<tr><td class='id'>{e(r['id'])}</td><td>{e(r['name'])}</td><td><span class='tag t-{r['cls']}'>{e(CLS[r['cls']]['he'])}</span></td><td>{e(r['lanes'])}</td>"
      f"<td>{seglen(r['id']):.0f} מ׳</td><td>{'כן' if r['truck'] else 'רק חלוקה'}</td><td>{e(r['why'])}{(' <span class=mut>(' + e(r['note']) + ')</span>') if r.get('note') else ''}</td></tr>")
A("</table></div>")
A("<h2>הצמתים</h2><h3>רמזורים (R-16: נתיב שמאלה וחץ בכל גישה, עדיפות לחירום)</h3><div class='wrap'><table><tr><th>צומת</th><th>איפה</th><th>גישות</th><th>מופעים</th><th>למה</th></tr>")
for s in P['signals']:
    ap = '<br>'.join(f"{e(a['road'])} מ-{e(a['from'])}: {a['through']} ישר" + (' + שמאלה עם חץ' if a['left'] else ' (של השדה)') for a in s['approaches'])
    A(f"<tr><td class='id'>{e(s['node'])}</td><td>{e(s['label'])}</td><td class='small'>{ap}</td><td class='small'>{' → '.join(e(p) for p in s['phases'])}</td><td>{e(s['why'])}</td></tr>")
A("</table></div><h3>כיכרות</h3><div class='wrap'><table><tr><th>צומת</th><th>שם</th><th>זרועות</th><th>למה</th></tr>")
for s in P['roundabouts']: A(f"<tr><td class='id'>{e(s['node'])}</td><td>{e(s['label'])}</td><td>{s['arms']}</td><td>{e(s['why'])}</td></tr>")
A("</table></div><h3>ימינה בלבד (רחוב מקומי על עורק)</h3><div class='wrap'><table><tr><th>צומת</th><th>איפה</th><th>למה</th></tr>")
for s in P['riro']: A(f"<tr><td class='id'>{e(s['node'])}</td><td>{e(s['label'])}</td><td>{e(s['why'])}</td></tr>")
A("</table></div><p class='mut small'>כל שאר הצמתים — עצור או זכות קדימה לדרך הגבוהה בהיררכיה; כניסה למגרש אחד (חניון, חצר, שער) אינה צומת.</p>")
A("<h2>המסילות</h2><p class='mut small'>כל המסילות של העיר, קיימות ועתידיות, מקצה לקצה: כל מסילה נגמרת על מסילה אחרת (מסוט), בבולמים או בדלת המוסך, או ביציאה מהמפה. "
  "המקורות: הקוד של היום (הקו הראשי, החצר, מסילות הרציף, רכבת–אוויר), חלק ד (האי, מסילת ההיפוך, מסילת העקיפה D‑130), חלק ו (רכבת–אוויר) ו-D‑177 (בית הזיקוק).</p>")
A("<div class='wrap'><table><tr><th>מסילה</th><th>שם</th><th>מאיפה</th><th>לאן</th><th>אורך</th><th>מצב</th></tr>")
RLB = {r['id']: r for r in P['rails']}
def endtxt(k, w):
    return {'join': lambda: 'מסוט אל ' + (RLB[w]['label'].split(' — ')[0] if w in RLB else w), 'buffer': lambda: w, 'door': lambda: w, 'edge': lambda: w}[k]()
for r in P['rails']:
    ln_ = sum(math.hypot(r['pts'][m + 1][0] - r['pts'][m][0], r['pts'][m + 1][1] - r['pts'][m][1]) for m in range(len(r['pts']) - 1)) / 10
    A(f"<tr><td class='id'>{e(r['id'])}</td><td>{e(r['label'])}{('<div class=small>' + e(r['note']) + '</div>') if r.get('note') else ''}</td><td class='small'>{e(endtxt(*r['ends'][0]))}</td>"
      f"<td class='small'>{e(endtxt(*r['ends'][1]))}</td><td>{ln_:.0f} מ׳</td><td>{'קיימת' if r['state'] == 'today' else 'עתידית — שלב ' + e(r.get('stage') or '')}</td></tr>")
A("</table></div><h3>מספר הפסים בכל קטע</h3><div class='wrap'><table><tr><th>קטע</th><th>פסים לפי התוכנית</th><th>במפה</th><th>המסילות</th></tr>")
for x in P['rail_sections']:
    A(f"<tr><td>{e(x['name'])}</td><td>{x['want']}</td><td>{x['got']}{'' if x['got'] == x['want'] else ' ✗'}</td><td class='id small'>{e(', '.join(x['lines']))}</td></tr>")
A("</table></div><h3>תחנות ומסופים</h3><div class='wrap'><table><tr><th>מזהה</th><th>מה</th><th>מצב</th></tr>")
for st in P['stations']:
    A(f"<tr><td class='id'>{e(st['id'])}</td><td>{e(st['label'])}</td><td>{'קיים' if st['state'] == 'today' else 'עתידי — שלב ' + e(st.get('stage') or '')}</td></tr>")
px = P['pax']
A(f"</table></div><p><b>{e(px['label'])}</b> — דרומה בפס א׳, דרך הקשת אל הרציף ומסילת הנמל המזרחית אל המסוט של האי; חזרה בפס ב׳ של האי, ב-B-LINK ובפס ב׳ של הקו הראשי — בלי נסיעה לאחור על הקו (D‑242). "
  "רכבות המשא לשדה נוסעות במסילת העקיפה ולא עוברות ליד הרציפים.</p>")
A("<h3>החציות עם כבישים</h3><div class='wrap'><table><tr><th>מזהה</th><th>סוג</th><th>דרך</th><th>מסילות</th><th>איפה</th><th>למה</th></tr>")
RDN0 = {r['id']: r['name'] for r in P['roads']}
for c in P['crossings']:
    kind = 'מחסום' if c['kind'] == 'level' else 'גשר רכבת מעל הכביש'
    A(f"<tr><td class='id'>{e(c['id'])}</td><td>{kind}</td><td>{e(RDN0.get(c['road'], 'כביש השדה' if c['road'] == 'airport' else c['road']))}</td><td class='id'>{e(', '.join(c['rail']))}</td>"
      f"<td class='id small'>{e(' · '.join(f'({q[0]}, {q[1]})' for q in c.get('pts', [])))}</td><td>{e(c['why'])}</td></tr>")
A("</table></div><h3>גשרי כביש</h3><div class='wrap'><table><tr><th>מזהה</th><th>סוג</th><th>אורך</th><th>למה</th></tr>")
br = next(r for r in P['roads'] if r['id'] == 'BR-I')
A(f"<tr><td class='id'>BR-I</td><td>גשר הכביש לאי — על הסיפון המשותף עם 2 פסי הרכבת</td><td>{seglen('BR-I'):.0f} מ׳</td><td>{e(br['why'])}</td></tr></table></div>")
TODAY_FLEET = [('1', 'D3 · מרכז העיר C3 · הקניון C2 · האגם B2 · הפארק B3 · B4 · התעשייה C4', 'כמו היום — טבעת העיר. המסלול עובר לטבעת של המפה אזור אחרי אזור', 7),
               ('2', 'D3 · מגדלי העסקים והמלון D2 · הקניון C2 · הווילות B3', 'כמו היום — הקניון והכפר. הכפר נוסף כשייבנה', 6),
               ('3', 'D4 · שער הנמל D5 · E5', 'כמו היום — התעשייה והנמל', 5),
               ('4', 'שער שדה התעופה · D3', 'כמו היום — השדה. המפרץ בשדה מוארך לשני אוטובוסים בגודל של כולם, כך שהקו מגיע לטרמינל (חבילה 7ח)', 5)]
A("<h2>קווים</h2>")
RDN = {r['id']: r['name'] for r in P['roads']}; STP = {st['id']: st for st in P['bus']['stops']}
A(f"<h3>אוטובוס — {len(P['routes']['bus'])} קווים חדשים, כולם מהמסוף ב-E3</h3><p class='mut small'>כל הקווים תוכננו מחדש על הרשת החדשה. האורך — של הקו בכיוון אחד (בטבעת — סיבוב שלם). "
  f"המרווח בשניות של המשחק, כמו בחלק ה; מספר האוטובוסים לפי {P['bus']['speed_px_s']} פיקסלים לשנייה עם העצירות ו-{P['bus']['layover_s']} שנ׳ בקצה — "
  f"{sum(l['buses'] for l in P['routes']['bus'])} בסך הכול — המספר הזה מחליף את ההערכה של D‑243 (49); היום במשחק יש {sum(n for _, _, _, n in TODAY_FLEET)} (בטבלה למטה). כל תחנה — מפרץ של 15 מ׳ ועוד כניסה ויציאה של 4 מ׳, לפחות 20 מ׳ ממרכז הצומת, לא על מעבר חצייה ולא מול כניסה.</p>")
A("<div class='wrap'><table><tr><th>קו</th><th>שם</th><th>המסלול</th><th>אורך</th><th>תחנות</th><th>מרווח</th><th>אוטובוסים</th><th>למה</th></tr>")
for l in P['routes']['bus']:
    seq = ' ← '.join(e(RDN[r]) for r in l['road_seq'])
    stn = [STP[i] for i in l['stop_ids']]
    A(f"<tr><td><span class='tag' style='background:{l['color']}'>{e(l['id'])}</span></td><td>{e(l['name'])}<div class='small mut'>{'בשני הכיוונים' if l['twoway'] else 'לולאה בכיוון אחד'}</div></td>"
      f"<td class='small'>{seq}</td><td>{l['len_km']} ק\"מ</td><td class='small'><b>{len(stn) + 1}</b>: מסוף E3 · {e(' · '.join(x['name'] for x in stn))}</td>"
      f"<td>כל {l['headway_s']} שנ׳</td><td>{l['buses']}</td><td class='small'>{e(l['why'])}</td></tr>")
A("</table></div>")
# 1.11 (R-45, the review 10:45): one table — the number of a line today, its number on the map, and when it changes (D‑337)
LN = {l['id']: l for l in P['routes']['bus']}
A("<h3>מספרי הקווים והצי — היום ובמפה (R-45)</h3><p class='mut small'>המפה לוקחת את המספרים של המשחק של היום, כמו שהוחלט ב-D‑243: קווים 1–4 נשארים, קו 5 — המרינה, החוף והאי, קו 6 — המערב. "
  "לכן אף מספר לא מתחלף במשחק, וקו 4 נשאר קו השדה. מספר האוטובוסים: היום — הספירה במשחק; במפה — לפי האורך והמרווח של כל קו. ההערכה הישנה של D‑243 (49) לא בתוקף. ברירת מחדל לאישורך (D‑337).</p>"
  "<div class='wrap'><table><tr><th>קו</th><th>המסלול היום</th><th>אוטובוסים היום</th><th>במפה</th><th>אוטובוסים במפה</th><th>מה מתחלף ומתי</th></tr>")
TF = {t[0]: t for t in TODAY_FLEET}
for l in P['routes']['bus']:
    t = TF.get(l['id'])
    A(f"<tr><td><span class='tag' style='background:{l['color']}'>{e(l['id'])}</span></td><td class='small'>{e(t[1]) if t else 'אין היום'}</td><td>{t[3] if t else '—'}</td>"
      f"<td>{e(l['name'])}</td><td>{l['buses']}</td><td class='small'>{e(t[2]) if t else 'קו חדש — כשהאזורים שלו נבנים'}</td></tr>")
A(f"<tr><td></td><td><b>סך הכול</b></td><td><b>{sum(t[3] for t in TODAY_FLEET)}</b></td><td></td><td><b>{sum(l['buses'] for l in P['routes']['bus'])}</b></td><td></td></tr>")
A("</table></div><h3>התחנות</h3><div class='wrap'><table><tr><th>תחנה</th><th>שם</th><th>על</th><th>קווים</th><th>המפרצים</th></tr>")
for st in P['bus']['stops']:
    bays = '<br>'.join(f"לכיוון {e(bb['toward'])} — {bb['to_junction_m']} מ׳ ממרכז הצומת" for bb in st['bay_list']) or 'תחנה סופית — ברחבה / במעגל הסיבוב, בלי מפרץ'
    on_ = f"{e(RDN[st['road']])} <span class='id small'>({e(st['seg'])})</span>" if st.get('road') else f"<span class='id'>{e(st['node'])}</span> <span class='small mut'>{e(N[st['node']]['label'])}</span>"
    A(f"<tr><td class='id'>{e(st['id'])}</td><td>{e(st['name'])}</td><td>{on_}</td>"
      f"<td>{' '.join(f"<span class='tag' style='background:{next(l['color'] for l in P['routes']['bus'] if l['id'] == i)}'>{e(i)}</span>" for i in sorted(st['lines'], key=int))}</td><td class='small'>{bays}</td></tr>")
A("</table></div>")
for kind, he in (('truck', 'משאיות'), ('emergency', 'חירום')):
    A(f"<h3>{he}</h3><div class='wrap'><table><tr><th>קו</th><th>שם</th><th>דרך</th><th>למה</th></tr>")
    for rt in P['routes'][kind]:
        A(f"<tr><td class='id'>{e(rt['id'])}</td><td>{e(rt['name'])}</td><td class='id small'>{e(' → '.join(rt['path']))}</td><td>{e(rt['why'])}</td></tr>")
    A("</table></div>")
A("<h2>גישה</h2><div class='wrap'><table><tr><th>אל</th><th>דרך</th><th>למה</th></tr>")
for a in P['access']: A(f"<tr><td>{e(a['what'])}</td><td class='id'>{e(', '.join(a['via']))}</td><td>{e(a['why'])}</td></tr>")
A("</table></div>")
A("<h2>הבלוקים מול טבלת השימושים</h2><p class='mut small'>השטח הנטו — בלי חצי הרוחב של כל דרך שגובלת בבלוק. "
  "המבנים עם מידה בטבלת השימושים (בית חולים, בית ספר, סופר, כבאות, משטרה, מלון, דירות, בתים, וילות, תחנת דלק) נבדקים מול 85% מהשטח; השאר נמדדים בשלב שלהם.</p>")
A("<div class='wrap'><table><tr><th>אזור</th><th>בלוקים (נטו, מ׳)</th><th>שטח נטו</th><th>מבנים + חניה</th><th>חלק</th><th>נמדדים בשלב שלהם</th></tr>")
BL = {b['id']: b for b in P['blocks']}
for f in P['fit']:
    bl = ', '.join(f"{b} {BL[b]['net_m'][0]:.0f}×{BL[b]['net_m'][1]:.0f}" for b in f['blocks'])
    sh = f"<span class='{'ok' if f['ok'] else 'bad'}'>{round((f['share'] or 0) * 100)}%</span>"
    A(f"<tr><td class='id'>{e(f['zone'])}</td><td class='small'>{e(bl)}</td><td>{f['area_m2']:,} מ״ר</td><td>{f['need_m2']:,} מ״ר</td><td>{sh}</td><td class='small'>{e(', '.join(USE_HE.get(x, x) for x in f['measured_in_stage']))}</td></tr>")
A("</table></div>")
A("<h2>לכל אזור — השרטוט והכבישים שלו</h2><div class='grid'>")
for z, Z in P['zones'].items():
    if not Z['roads']: continue
    rl = ', '.join(Z['roads'])
    A(f"<div class='zc'>{SV.zone_svg(P, M, z, Z)}<b>{e(z)}</b> <span class='pill'>{e(Z['purpose'].replace('Approach', 'נתיב הגישה'))} · שלב {e(Z['stage'] or '—')}</span>"
      f"<div class='small id' style='white-space:normal'>{e(rl)}</div>"
      + (f"<div class='small'>רמזורים: {e(', '.join(Z['signals']))}</div>" if Z['signals'] else '') + (f"<div class='small'>כיכרות: {e(', '.join(Z['roundabouts']))}</div>" if Z['roundabouts'] else '') + "</div>")
A("</div>")

SZ = {}
for i in P.get('sites', []): SZ.setdefault(i['zone'], []).append(i)
A("<h2>בתוך האזורים שעוד לא בנויים</h2><p class='mut small'>הדרכים הפנימיות, הכניסות, המבנים, המגרשים, החניונים והמנחתים לפי ה-uses, במידה האמיתית (10 px = 1 מ׳). "
  "כל דרך פנימית וכל כניסה מצוירת כמו כל דרך ברשת — 1+1 או נתיב אחד — והכניסה חוצה את המדרכה עד הכביש (הנמכת שפה). כניסה למגרש היא לא צומת ושומרת 18 מ׳ לפחות מצומת. "
  "לכל מבנה, חניון, חצר ומגרש כתוב מאיזו דרך מגיעים אליו. מנחת: עיגול לבן, ומסביבו קו אדום מקווקו של שטח הבטיחות.</p>")
for z in ['A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B5', 'B6', 'C1', 'C3', 'D1', 'D3', 'D5']:
    if z not in SZ: continue
    A(f"<h3>{e(z)} — {e(P['zones'].get(z, {}).get('purpose', '').replace('Approach', 'נתיב הגישה'))}</h3><div class='grid2'><div class='zc sm'>{SV.site_svg(P, M, z)}</div><div class='wrap'><table><tr><th>פריט</th><th>מה ובאיזה גודל</th><th>למה</th></tr>")
    for i in SZ[z]:
        if i['kind'] == 'pad': sz = f"Ø {2 * i['r'] / 10:.0f} מ׳ (בטיחות Ø {2 * i['safety'] / 10:.0f})"
        elif i['kind'] == 'site': sz = f"דרך פנימית — {'נתיב אחד' + (' חד-סטרי' if i.get('oneway') else '') if i.get('lanes') == '1' else '1+1'}, רוחב {2 * i['hw'] / 10:.1f} מ׳"
        elif i['kind'] == 'path': sz = f"שביל להולכי רגל, רוחב {2 * i['hw'] / 10:.0f} מ׳"
        else: x0, y0, x1, y1 = i['rect']; sz = f"{(x1 - x0) / 10:.1f} × {(y1 - y0) / 10:.1f} מ׳" + (f" · {i['floors']} קומות" if i.get('floors') else '') + (f" · {i['stalls']} מקומות" if i.get('stalls') else '')
        if i['kind'] == 'house': continue
        ac = i.get('access'); acs = ''
        if ac: acs = f"<div class='small'>הגישה מ{e(ac['road_name'])} <span class='id'>({e(ac['road'])})</span> — {e(ac['via'])}" + (f", דרך {e(ac['through'])}" if ac['through'] else '') + "</div>"
        A(f"<tr><td class='id'>{e(i['id'])}</td><td>{e(i['label'])}<div class='small mut'>{e(sz)}</div>{acs}</td><td class='small'>{e(i['why'])}</td></tr>")
    for d in P.get('driveways', []):
        if d['zone'] == z: A(f"<tr><td class='id'>{e(d['id'])}</td><td>{e(d['label'])}<div class='small mut'>כניסה {'בנתיב אחד' if d.get('lanes') == '1' else '1+1'} מ-{e(d['road'])} · {d.get('to_junction_m', '—')} מ׳ מצומת</div></td><td class='small'>{e(d['why'])}</td></tr>")
    A("</table></div></div>")
A("<h3>הגישה ב-A2, A3 ו-A4 — לרכב ולהולך רגל, לכל פריט</h3><p class='mut small'>הבעלים (1.11): לכל מבנה, מגרש ספורט, חניון ומנחת — דרך לרכב (כביש, דרך שירות לחירום, רחבה או החניון שלידו) "
  "ושביל להולך רגל מהמדרכה או מהחניון. השבילים מצוירים בבהיר עם קו מקווקו; דרכי השירות — באפור, נתיב אחד.</p><div class='wrap'><table><tr><th>פריט</th><th>מה</th><th>לרכב</th><th>להולך רגל</th></tr>")
for a_ in P.get('access_az', []):
    A(f"<tr><td class='id'>{e(a_['id'])}</td><td>{e(a_['label'])}</td><td class='small'>{e(a_['vehicle'] or '✗')}</td><td class='small'>{e(a_['walk'] or '✗')}</td></tr>")
A("</table></div>")

A(f"<h2>המעבר — אזור אחרי אזור</h2><div class='box'>{e(P['transition']['why'])} בכל שלב בודקים שהרשת כולה (חדשה, ישנה וזמנית) מחוברת. "
  "חיבור זמני נבחר רק כשצריך: המשך טבעי של רחוב ישן (עד 15 מ׳), שני חיבורים לכל חלק חדש של הרשת, ורחוב ישן שאחרת היה נשאר ללא מוצא.</div>")
A("<div class='grid st' style='margin-top:10px'>" + ''.join(f"<div class='zc'>{SV.stage_svg(P, M, k)}<b class='id'>{e(t['stage'])}</b> <span class='pill'>{e(t['why'])}</span></div>" for k, t in enumerate(P['transition']['stages'])) + "</div><p class='mut small'>אותו מקרא כמו במפת העתיד: בצבע וברוחב האמיתי — הדרכים החדשות שכבר נבנו; רק כאן מופיעים גם הרחובות של היום שעוד נשארים (קו אפור דק ומקווקו) והחיבורים הזמניים (ורוד במסגרת סגולה, המעוין — הצומת הזמני); מסגרת כחולה — האזורים של השלב.</p>")
A("<div class='wrap'><table><tr><th>שלב</th><th>אזורים</th><th>למה בסדר הזה</th><th>קטעים חדשים</th><th>רחובות ישנים שיוצאים</th><th>זמניים שנפתחים</th><th>זמניים שנסגרים</th></tr>")
for t in P['transition']['stages']:
    A(f"<tr><td class='id'>{e(t['stage'])}</td><td class='id'>{e(', '.join(t['zones']))}</td><td>{e(t['why'])}</td><td>{len(t['new_segments'])}</td><td>{len(t['removed'])}</td>"
      f"<td class='tmp'>{e(', '.join(a['id'] for a in t['temp_added'])) or '—'}</td><td>{e(', '.join(t['temp_removed'])) or '—'}</td></tr>")
A("</table></div><h3>החיבורים הזמניים — רשימה נפרדת</h3><div class='wrap'><table><tr><th>מזהה</th><th>מהרחוב הישן</th><th>אל</th><th>אורך</th><th>למה</th><th>R-15</th><th>נסגר ב</th></tr>")
for t in P['transition']['stages']:
    for a in t['temp_added']:
        r15 = (f"<span class='bad'>חריגה זמנית: {a['spacing_m']} מ׳ מצומת</span>" if a['exempt_R15'] else ('צומת קיים' if not a['new_junction'] else f"{a['spacing_m']} מ׳ מצומת"))
        A(f"<tr><td class='id tmp'>{e(a['id'])}</td><td><span class='id'>{e(a['old_node'])}</span> <span class='small mut'>{e(a['old_label'])}</span></td><td class='id'>{e(a['to'])}</td><td>{a['len_m']:.0f} מ׳</td><td>{e(a['why'])}</td><td class='small'>{r15}</td><td class='id'>{e(a['until'])}</td></tr>")
A("</table></div>")
jn = [j for t in P['transition']['stages'] for j in t['joins']]
if jn: A("<p class='small mut'>חיבורים קבועים לשדה (אותה נקודה, לא זמניים): " + e('; '.join(f"{j['old_node']} ↔ {j['at']}" for j in jn)) + "; שער המטען AP2 ‏(4800, 1250) — דרך המטען מגיעה אליו בשלב S8.</p>")
R7 = P.get('r7', {})
if R7:
    ZH = {'A0': 'A0 — הרכס', 'A1': 'A1 — היער'}
    A("<h2>סבב 7 — מה נוסף למפה, אזור אחרי אזור</h2><p class='mut small'>כל פריט שהיה חסר או חלקי בטבלת ההתאמה מול תוכנית האב (R-64). כל אחד בגודל האמיתי (10 פיקסלים למטר), עם הגישה שלו — כביש, שביל, מזח או המגרש שלידו — ונבדק בבדיקות הקבועות שבסוף הדף. "
      "המצופים, המעברים המסומנים וקווי הגובה — בספירה בלבד.</p><div class='wrap'><table><tr><th>אזור</th><th>פריט</th><th>מה ובאיזה גודל</th><th>גישה</th><th>למה</th></tr>")
    SKIP = ('buoy', 'xmark', 'contour', 'fishstand', 'cblock', 'corner')
    for it in sorted(R7['items'], key=lambda i: (i['zone'][1:], i['zone'][0], i['id'])):
        if it['kind'] in SKIP: continue
        if it.get('rect'):
            x0, y0, x1, y1 = it['rect']; sz = f"{(x1 - x0) / 10:g} × {(y1 - y0) / 10:g} מ׳"
        elif it.get('pts') and it['kind'] != 'lights': sz = f"{sum(math.hypot(it['pts'][k + 1][0] - it['pts'][k][0], it['pts'][k + 1][1] - it['pts'][k][1]) for k in range(len(it['pts']) - 1)) / 10:.0f} מ׳, רוחב {2 * it.get('hw', 10) / 10:g} מ׳"
        elif it['kind'] == 'lights': sz = f"{len(it['pts'])} נקודות"
        else: sz = ''
        A(f"<tr><td class='id'>{e(it['zone'])}</td><td class='id'>{e(it['id'])}</td><td>{e(it['label'])}<div class='small mut'>{e(sz)}</div></td><td class='small'>{e(it.get('access_txt') or '—')}</td><td class='small'>{e(it['why'])}</td></tr>")
    from collections import Counter as _C
    cn = _C(i['kind'] for i in R7['items'])
    A(f"</table></div><p class='small mut'>ועוד: {cn['buoy']} מצופים בנתיבים, {cn['xmark']} מעברים מסומנים בצד האווירי (המטוס קודם), {cn['contour']} קווי גובה ב-A0, {cn['fishstand']} עמדות דיג, {cn['cblock']} בלוקי מכולות ו-{cn['corner']} פינות לסמי.</p>")
    A("<h3>R-61 — טבלת המנחתים (ברירת מחדל, לאישורך)</h3><p class='mut small'>המנחת המצויר — בקוטר הרוטור של המסוק שנוחת בו, מעוגל למעלה; טבעת בטיחות מקווקוות דקה — פי 1.5 מאורך המסוק; ועל כל מנחת המסוק עצמו בגודל אמיתי.</p>"
      "<div class='wrap'><table><tr><th>מסוק</th><th>רוטור</th><th>אורך</th><th>המנחת המצויר</th><th>הטבעת</th></tr>")
    for k_, h_ in R7['heli'].items(): A(f"<tr><td>{e(h_['he'])}</td><td>{h_['rotor']} מ׳</td><td>{h_['length']} מ׳</td><td><b>{h_['pad']} מ׳</b></td><td><b>{h_['ring']:g} מ׳</b></td></tr>")
    A("</table></div><div class='wrap' style='margin-top:8px'><table><tr><th>מנחת</th><th>אזור</th><th>מסוק</th><th>מנחת / טבעת</th><th>איפה</th></tr>")
    for r_ in R7['pads']: A(f"<tr><td class='id'>{e(r_['id'])}</td><td class='id'>{e(r_['zone'])}</td><td>{e(r_['he'])}</td><td>{r_['pad']} / {r_['ring']:g} מ׳</td><td class='small'>{e(r_['label'])}{' — על הגג' if r_['roof'] else ''}</td></tr>")
    A("</table></div><h3>R-65 — המלונות (ברירת מחדל, לאישורך)</h3><div class='wrap'><table><tr><th>אזור</th><th>מגרש</th><th>מה</th><th>מידות</th></tr>")
    for h_ in R7['hotels']: A(f"<tr><td class='id'>{e(h_['zone'])}</td><td class='id'>{e(h_['id'])}</td><td>{e(h_['label'])}</td><td>{h_['m'][0]} × {h_['m'][1]} מ׳</td></tr>")
    A("</table></div><h3>תחנות בלי מקום לפי הכלל — סיבה וברירת מחדל (R-46, ‏R-63)</h3><div class='wrap'><table><tr><th>תחנה</th><th>שם</th><th>מקצה הצומת (לפנים / מאחור)</th><th>למה</th><th>ברירת מחדל</th><th>החלופה</th></tr>")
    for x_ in R7.get('stop_exc', []): A(f"<tr><td class='id'>{e(x_['id'])}</td><td>{e(x_['name'])}</td><td>{x_['near']} / {x_['far']} מ׳</td><td class='small'>{e(x_['why'])}</td><td class='small'>{e(x_['default'])}</td><td class='small'>{e(x_['alt'])}</td></tr>")
    A("</table></div><h3>לאישורך — ברירות המחדל של סבב 7</h3><div class='wrap'><table><tr><th>מקור</th><th>הנושא</th><th>ברירת המחדל במפה</th><th>החלופה</th></tr>")
    for d_ in R7['decisions']: A(f"<tr><td class='id'>{e(d_['code'])}</td><td>{e(d_['what'])}</td><td><b>{e(d_['default'])}</b> — לאישורך</td><td class='small'>{e(d_['alt'])}</td></tr>")
    A("</table></div>")
A("<h2>הבדיקות</h2><div class='wrap'><table><tr><th></th><th>בדיקה</th><th>תוצאה</th></tr>")
for c in P['checks']: A(f"<tr><td class='{'ok' if c['ok'] else 'bad'}'>{'✓' if c['ok'] else '✗'}</td><td>{e(c['name'])}</td><td class='small'>{e(c['det'])}</td></tr>")
A("</table></div><h2>מה צריך במשחק</h2><div class='wrap'><table><tr><th>מה</th><th>במשחק</th></tr>")
for m in P['impl']: A(f"<tr><td>{e(m['what'])}</td><td>{e(m['game'])}</td></tr>")
A("</table></div><h2>שאלות לבעלים</h2><div class='box'><ol>")
for q in P['questions']: A(f"<li>{e(q['q'])} <span class='mut'>(ברירת מחדל: {e(q['default'])})</span></li>")
A("</ol></div>")
A(f"<h2>הבסיס</h2><div class='box small'><ul>" + ''.join(f"<li>{e(x)}</li>" for x in P['basis']['owner']) + f"<li>{e(P['basis']['coordinator'])}</li><li>השטח: {e(P['basis']['terrain'])}</li>"
  + ''.join(f"<li>קבוע: {e(x)}</li>" for x in P['basis']['fixed']) + f"<li>{e(P['basis']['background'])}</li><li>{e(P['basis']['today'])}</li></ul>"
  "<p class='mut'>הדף נבנה מארבעה קבצים: הרשת והמשפטים; הבדיקות, הבלוקים והמעבר (שכותב את קובץ התוכנית); המפות; והדף עצמו.</p></div>")
A("</main>" + SV.hover_data(P, GR, M) + SV.ZOOM_JS + "</body></html>")
# Hebrew only (R-03): the few words of the data that are not codes or file names
HTML = '\n'.join(out)
for a_, b_ in (('(ה-uses)', '(טבלת השימושים)'), ('לפי ה-uses', 'לפי טבלת השימושים'), ('ה-uses', 'טבלת השימושים'), ('(10 px = 1 מ׳)', '(10 פיקסלים למטר)'),
               ("<td class='id'>airport</td>", "<td>השדה</td>"), ('Rail–Air', 'רכבת–שדה'), ('Approach', 'נתיב הגישה'), ('(uses; ', '(טבלת השימושים; '), ('(uses)', '(טבלת השימושים)'), ('uses: ', 'טבלת השימושים: '), (' uses', ' טבלת השימושים'), ('ה-uses', 'טבלת השימושים')):
    HTML = HTML.replace(a_, b_)
# 1.11 round 6ו (R-55): the visible text of the page has no English — the codes that are a word of Latin letters only get their Hebrew name
import re as _re
_HEB_IDS = [('EAST', 'המסילה המזרחית'), ('SPUR', 'השלוחה'), ('SIDING', 'מסילת הצד'), ('BYPASS', 'העקיפה'), ('XOVER', 'מעבר פסים'), ('XN', 'מעבר הפסים הצפוני'),
            ('XS', 'מעבר הפסים הדרומי'), ('BOAT', 'מעגן'), ('BRH', 'ראש הגשר'), ('IL', 'כיכר האי'), ('FIBA', 'איגוד הכדורסל'), ('ITF', 'איגוד הטניס'), ('TMP', 'זמני'),
            ('D/E', 'D ו-E'), ('px', 'פיקסלים')]
def _heb_text(t):
    for a_, b_ in _HEB_IDS: t = _re.sub(r'(?<![A-Za-z0-9_\-‑])' + _re.escape(a_) + r'(?![A-Za-z0-9_\-‑])', b_, t)
    return t
_HEB_IDS += [('AIRSIDE', 'הצד האווירי'), ('CH', 'C‑H')]   # 2.11 round 7
_PRE = [('(GA)', '(התעופה הכללית)'), ('ה-GA', 'התעופה הכללית'), ('ל-GA', 'לתעופה הכללית'), (' GA', ' התעופה הכללית')]
def _heb_text2(t):
    for a_, b_ in _PRE: t = t.replace(a_, b_)
    return _heb_text(t)
_parts = _re.split(r'(<script.*?</script>|<style.*?</style>)', HTML, flags=_re.S)
def _hover(q):   # 2.11 round 7: the hover cards are visible text too
    if 'window.__MAP=' not in q: return q
    m_ = _re.search(r'window\.__MAP=(\{.*\});</script>', q, _re.S); D_ = json.loads(m_.group(1).replace('<\\/', '</'))
    D_['info'] = [_re.sub(r'>([^<]+)<', lambda mm: '>' + _heb_text2(mm.group(1)) + '<', '<x>' + h_ + '</x>')[3:-4] for h_ in D_['info']]
    return "<script>window.__MAP=" + json.dumps(D_, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ";</script>"
HTML = ''.join(_hover(q) if q.startswith('<script') else (q if q.startswith('<style') else _re.sub(r'>([^<]+)<', lambda mm: '>' + _heb_text2(mm.group(1)) + '<', q)) for q in _parts)
open(W + '/city_plan.html', 'w').write(HTML)
print('page', sum(len(x) for x in out))
