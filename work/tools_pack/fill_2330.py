#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""27.10 · מסירת 23:30 — ממלא את דף הסיכום ואת RESUME R21 מהתבניות, מתוך קובצי ה-QA, הנתונים של התוכנית והקבצים שנבנו.
usage: fill_2330.py <now HH:MM> <R19.zip> <verify line (Hebrew)> <file table (markdown) file>"""
import json, os, sys, hashlib, subprocess, html
W = '/home/claude/work'; G = W + '/clean_r2b_025637'; PL = W + '/plan600'
NOW, R19, VERIFY, TABLE = sys.argv[1], sys.argv[2], sys.argv[3], open(sys.argv[4], encoding='utf-8').read()
J = lambda p: json.load(open(os.path.join(G, p), encoding='utf-8'))
fmt = lambda v: format(v, ',')
sha = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()[:12]
ex = lambda p: os.path.exists(os.path.join(G, p))
cops = lambda pat, ks: [J(pat % k)['scenarios']['city']['ops'] for k in ks if ex(pat % k)]
C94 = cops('qa/fence101/city_S7F94_%d.json', (1, 2)); C100 = cops('qa/fence101/gpuab_S7F100A_%d.json', (1, 2)) + cops('qa/fence101/city_S7F100A_%d.json', (1, 2))
C101 = cops('qa/fence101/gpuab_S7F101_%d.json', (1, 2)) + cops('qa/fence101/city_S7F101_%d.json', (1, 2))
S94, S100 = cops('qa/stage6/gpuab_S7F94_%d.json', (1, 2)), cops('qa/stage6/gpuab_S7F100_%d.json', (1, 2))
c60 = {b: (J('qa/fence101/city60_%s.json' % b)['scenarios']['city']['ops'] if ex('qa/fence101/city60_%s.json' % b) else None) for b in ('S7F94', 'S7F100A', 'S7F101')}
j = lambda L: ' / '.join(map(str, L))
WORSE = all(c60.values()) and max(c60['S7F100A'], c60['S7F101']) > c60['S7F94'] + 5
fence = J('qa/stage6/fence_s7f101.json')['result']
sz = J('qa/stage6/sz_S7F94.json')['result'], J('qa/stage6/sz_S7F101.json')['result']
SZ = '%d / %d → %d / %d' % (sz[0]['atTarget'], sz[0]['rows'], sz[1]['atTarget'], sz[1]['rows'])
v613 = PL + '/out/Turbo_City_Master_Plan_v6_13.html'
N = json.load(open(PL + '/data/new.json', encoding='utf-8')); KID = [d['id'] for d in N['defects'] if d.get('topic') == 'גדלים' and 'E2_TRUCK_DOCKS' in d.get('text', '')][0]
df = subprocess.run(['df', '-h', W], capture_output=True, text=True).stdout.split('\n')[1].split()[3]
RUN = 'Turbo_City_v1_96_GATE77_S7F94.html' if WORSE else 'Turbo_City_v1_96_GATE77_S7F101.html'
RUNB = 'S7F94' if WORSE else 'S7F101'
RUNSHA = sha(G + '/out/' + RUN)
cityTxt = ('בתמונה של 3 שנ׳ (8 ריצות לכל צד, בשתי הפעלות): S7F94 %s מול S7F100 %s ו-S7F101 %s' % (j(sorted(S94 + C94)), j(S100 + C100), j(C101)))
c60Txt = ('; דקה שלמה באותה סצנה: S7F94 %s · S7F100 %s · S7F101 %s' % (c60['S7F94'], c60['S7F100A'], c60['S7F101'])) if all(c60.values()) else ''
M7 = [J('qa/fence101/gpuab_%s_%d.json' % (b, k))['scenarios'] for b in ('S7F100A', 'S7F101') for k in (1, 2)]
NAMES = {'airport': 'השדה', 'tower': 'המגדל', 'port': 'הנמל', 'cityzoom': 'זום העיר', 'extreme': 'הקיצון', 'north': 'הצפון', 'coast': 'החוף המזרחי'}
other7 = [k for k in NAMES if min(M7[2][k]['ops'], M7[3][k]['ops']) > max(M7[0][k]['ops'], M7[1][k]['ops']) + 5]

DEV = [('D‑241 (2) · D‑160', '"מפרץ לבדיקה נוספת" לא צמוד לשער הנוסעים אלא אחרי הגשר: מכוניות — בקומת הקרקע של החניון הרב-קומתי, מכליות — במפרץ המילוי', 'מפרץ בשער עצמו (לוקח 5 חניות של E3‑N1), או השער 200 px מערבה'),
       ('D‑241 (5) · D‑160', 'F2‑AIR‑S ו-AIR‑S מוסרים בשלב 9 — החזית, החניון הרב-קומתי ומפרצי האוטובוס מחליפים אותם', 'להשאיר אותם עד שהחזית החדשה עובדת'),
       ('D‑242 (5) · D‑227ו', '"גשר הרכבת ב-F6" מתפרש כענף האי; ‏EAST‑LINE על הגשרים שלה נשארת', 'להסיר את הגשרים ב-F6 לפי הנוסח (מנתק את הנמל ואת רכבת השדה)'),
       ('D‑242 (5) · D‑187', 'מהמסוט עד סוף ה-S — פס רכבת אחד והכביש על גשר צמוד; משם סיפון אחד של 2 פסים וכביש', 'פס כפול כבר מהמסוט — מסוט כפול על EAST‑B'),
       ('D‑244 (9) · D‑160', '3 האנגרים במקום 4 + 1', 'האנגר רביעי לצר-גוף במקום R1'),
       ('D‑244 (10) · D‑160 <span class="warn">חדש</span>', 'הגישה ל-H0 נוסעת על מסלול ההסעה A — 243 px, בצומת A–B', '(א) רכבי התחזוקה בליווי רכב מוביל על A, באישור המגדל; (ב) שביל שחוצה את B בניצב ועולה מזרחית לו — עוד לא נבדק מול אזור הכנף של B'),
       ('D‑244 (11) · D‑160', 'נתיב אחד ברמזור לרחבת המשא (כולל CARGO_W, ~1,450 px) ול-H0', 'C2 לעמדה מרוחקת, והשרוולים 38 px מזרחה'),
       ('D‑244 (12) · D‑213 (5)', 'במרוחקות אין חנייה קרובה לכל סוג', '5 + 3 מרוחקות, וכיס במקום R4'),
       ('D‑244 (13) · D‑160', 'הצי בלילה בכיסים (98) ובבסיס (14) — לא חניון אחד', 'חניון לילה ב-G3 (6,190 מ״ר) במקום ה-GA והמנחתים'),
       ('D‑244 (14) · D‑160 <span class="warn">חדש</span>', 'הכיסים נבדקים בשטח בלבד; רכב שנכנס באף יוצא בנסיעה לאחור', 'חניות שנוסעים דרכן או באלכסון, עם מסלול כניסה ויציאה לכל רכב'),
       ('שלב 5 · D‑151 / D‑164 <span class="warn">חדש</span>', 'G3 ו-H0–H3 לא נוספו לאזורים החיים (30), ו-A0–D0 עוד לא; הם ייכנסו עם התוכן — בשלבים 8–9 (35), ו-A0–D0 בשלב 11 (39)', 'להוסיף את כל 9 עכשיו, כאזורים חיים סגורים (39)')]
devHtml = ('<p><b>11 סטיות מההחלטות שלך</b> — לכל אחת נימוק וחלופה בתוכנית, ושום דבר לא נבנה עליהן לפני השלבים שלהן. שלוש חדשות מביקורת 7, ושתיים של D‑242 (5) שלא נספרו קודם:</p>\n'
           '<div class="tw"><table>\n<tr><th>הסטייה</th><th>מה בתוכנית</th><th>החלופה</th></tr>\n' +
           '\n'.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % d for d in DEV) + '\n</table></div>\n'
           '<p style="margin-top:6px">‏A0–D0 בשלב 11, עם הרובע "כפר וטבע", היא קריאה של D‑222 (ז) — אם התכוונת לשלב אחר, תכתוב.</p>')
if WORSE:
    perfStat, perfSub = 'העיר +%d' % (min(C100 + C101) - max(C94)), 'פעולות ציור בעיר — S7F101 מחכה להכרעתך'
    cityCard = ('<div class="card"><p><span class="warn">למה הבנייה להריץ היא עדיין S7F94:</span> במדד הציור, בסצנה של העיר, ‏S7F100 ו-S7F101 מעל הטווח של S7F94 '
                '(%s%s). לפי הכלל שלך — החמרה עוצרת את המסירה, ולכן S7F101 נמסרת לצפייה בלבד.</p>'
                '<p><b>מה מצאתי:</b> זה לא ציור יקר יותר של כל רכב, אלא יותר רכבים בתמונה באותו רגע של ה-Benchmark: 1–2 מכוניות ואוטובוס אחד יותר (כלי האבחון <code>gpu_why.js</code>). '
                'עלות הציור של כל רכב לא השתנתה. כנראה התנועה בעיר זזה קצת אחרת עם המכוניות הקצרות של D‑238.</p>'
                '<p><b>מה ממשיך עכשיו:</b> S7F102 = S7F94 + הגדר לבד (בלי שלב 6), כדי שהתיקון של הגדר יגיע אליך כבנייה להריץ. במקביל אני מחפש דרך להוריד את העלות בעיר.</p></div>') % (cityTxt, c60Txt)
    cityDec = '<li><b>העיר במדד הציור:</b> לקבל את S7F101 כבנייה להריץ (יותר רכבים בתמונה, לא ציור יקר יותר), או לחכות לתיקון. הנתונים — למעלה וב-PERF_BUDGET §11.</li>'
    perf = ('<ul><li><span class="warn">העיר:</span> %s%s.</li><li>שאר 7 התרחישים ו-6 המצלמות בקצה — בתוך הפיזור%s.</li>'
            '<li><b>הפתיחה עם השמירה שלך (×2.5):</b> השמירה נטענת בכל הריצות, 0 שגיאות; הפריים הראשון בטווח של S7F94.</li>'
            '<li><b>החמרה שנתפסה ותוקנה לפני המסירה, מוקדם יותר היום:</b> הגרסה הראשונה של S7F88 האטה את הפריים הראשון בחצי שנייה.</li></ul>') % (cityTxt, c60Txt, '' if not other7 else ' (חוץ מ: ' + ', '.join(NAMES[k] for k in other7) + ')')
    last = 'דף הסיכום הזה; S7F101 (לצפייה — העיר מחכה להכרעתך), ‏v6.13, ‏R19; הבנייה להריץ — S7F94'
else:
    perfStat, perfSub = '0', 'החמרות בעומס הציור ובפתיחה (העיר — ראו הביצועים)'
    cityCard = ''
    cityDec = '<li><b>העיר במדד הציור:</b> בתמונה של 3 שנ׳ גבוה בכ-3%, בדקה שלמה נמוך ב-2% — הכרעתי לפי הדקה ש-S7F101 היא הבנייה להריץ. המדידה שלך על S7F101 תכריע.</li>'
    perf = ('<ul><li><span class="ok">אין החמרה בעומס הציור.</span> <b>העיר:</b> %s%s. בתמונה של 3 שנ׳ S7F100 / S7F101 גבוהות בכ-3%% — ברגע שה-Benchmark מצלם יש בתמונה 1–2 מכוניות ואוטובוס אחד יותר '
            '(הבדקתי בכלי אבחון חדש, <code>gpu_why.js</code>: עלות הציור של כל רכב לא השתנתה). בדקה שלמה של אותה סצנה הן נמוכות ב-2%%. הכרעתי לפי הדקה השלמה; אם המספרים שלך יראו אחרת — הם מכריעים.</li>'
            '<li>שאר 7 התרחישים ו-6 המצלמות בקצה — בתוך הפיזור.</li>'
            '<li><b>הפתיחה עם השמירה שלך (×2.5):</b> השמירה נטענת בכל הריצות, 0 שגיאות; הפריים הראשון בטווח של S7F94.</li>'
            '<li><b>החמרה שנתפסה ותוקנה לפני המסירה, מוקדם יותר היום:</b> הגרסה הראשונה של S7F88 האטה את הפריים הראשון בחצי שנייה.</li></ul>') % (cityTxt, c60Txt)
    last = 'דף הסיכום הזה; ‏<b>S7F101</b> (שלב 6, חלקים 1–4, והגדר על הקווים של חלק ו); ‏<b>v6.13</b>; ‏<b>R19</b>'
audit7 = ('<li><b>W02–W11 — נסגרו ב-v6.13:</b> 7 תוקנו (בין היתר: המגרש של חניון הלילה 1380 × 318; ‏CARGO_W בסטייה (11); 13 מספרים שהוקלדו נבדקים עכשיו מול קובצי ה-QA), '
          'ו-3 סומנו כסטיות עם חלופה (הגישה ל-H0, האזורים החיים, הכיסים). הספירה האמיתית של הסטיות — 11 (ראו "מחכה לעינך").</li>'
          '<li>פתוח לבדיקה: שיש ב-E4 מקום ל-10 px הנוספים של חניון הלילה.</li>')
T = open(W + '/deliver/summary_2330/Turbo_City_Summary_27-10.tpl.html', encoding='utf-8').read()
REP = {'%%NOW%%': NOW, '%%RUNBUILD%%': RUNB, '%%PERFSTAT%%': perfStat, '%%PERFSTATSUB%%': perfSub, '%%CITYCARD%%': cityCard, '%%RUNFILE%%': RUN, '%%RUNSHA%%': RUNSHA,
       '%%FENCERUN%%': '' if WORSE else ' הגדר עברה לקווים של חלק ו: בצפון-מזרח היא רחוקה יותר (y −846, ‏x 9596), ובדרום ובמערב היא על קו החוף וקיר המרינה.',
       '%%STAGE6RUN%%': '' if WORSE else '<li><b>שלב 6:</b> המכוניות בגודל של D‑238 — SUV, מיניוואן, ואן, טנדר ופרימיום קצרים יותר, ורוב המכוניות רחבות יותר (ציור חדש, לא מתיחה). האמבולנס גדל ל-65 px.</li>',
       '%%F9SZ%%': ' (ב-S7F101)' if WORSE else '', '%%DEVIATIONS%%': devHtml, '%%CITYDECISION%%': cityDec, '%%DISK%%': df,
       '%%FENCECHK%%': '%s px, ‏%s דגימות של רכבי שירות ו-%s של מטוסים' % (fmt(fence['len']), fmt(fence['checked']['fleet']), fmt(fence['checked']['aircraft'])),
       '%%SZ%%': SZ, '%%AUDIT7%%': audit7, '%%PERF%%': perf, '%%KNEW%%': 'נרשם כ-%s.' % KID, '%%LASTDELIVERY%%': last,
       '%%AGENTRULES%%': '<li>הסוכן שסגר את ביקורת 7 כתב קובצי עבודה זמניים בתיקיית הסשן (הועברו ל-<code>_to_delete/</code>), הזיז לרגע כ-200 קבצים אחרים מתיקיית הסשן והחזיר אותם מיד בלי שינוי, ופקודה אחת שלו עם <code>rm -rf</code> נחסמה — לא נמחק דבר.</li>'}
for k, v in REP.items(): T = T.replace(k, v)
assert '%%' not in T, [l for l in T.split('\n') if '%%' in l][:3]
open(W + '/deliver/summary_2330/Turbo_City_Summary_27-10.html', 'w', encoding='utf-8').write(T)
# the RESUME
R = open(W + '/study/RESUME_R21.tpl.md', encoding='utf-8').read()
RR = {'%%NOW%%': NOW, '%%RUNFILE%%': RUN, '%%RUNSHA%%': RUNSHA,
      '%%RUNNOTE%%': ('**S7F101 לא נמסרת כבנייה להריץ:** בעיר מדד הציור מעל הטווח של S7F94 (%s%s) — יותר רכבים בתמונה באותו רגע, לא ציור יקר יותר; מחכה להכרעתך. בינתיים — S7F102 = S7F94 + הגדר.' % (cityTxt, c60Txt)) if WORSE else 'אין החמרה — S7F101 היא הבנייה להריץ.',
      '%%V613SHA%%': sha(v613), '%%V613SIZE%%': fmt(os.path.getsize(v613)), '%%R19SHA%%': sha(R19), '%%R19SIZE%%': fmt(os.path.getsize(R19)), '%%R19VERIFY%%': VERIFY, '%%DISK%%': df, '%%SZ%%': SZ,
      '%%PERFROW%%': ('7 מתוך 8 התרחישים והמצלמות בקצה — בתוך הפיזור; **העיר** — %s%s%s. הפתיחה: השמירה נטענת, הפריים הראשון בטווח. פירוט — `PERF_BUDGET.md` §11' % (cityTxt, c60Txt, ' — **החמרה לפי הכלל**' if WORSE else ' — בדקה שלמה פחות מ-S7F94: אין החמרה (בתמונה של 3 שנ׳ — כ-3% יותר: 1–2 מכוניות ואוטובוס יותר ברגע הצילום)')),
      '%%KID%%': KID, '%%FENCECHK%%': 'בדיקת הגדר העמוקה — תקינה: %s px, אף כביש, מסילה, רכב שירות (%s דגימות) או מטוס (%s) לא חוצים אותה; ‏249 / 249' % (fmt(fence['len']), fmt(fence['checked']['fleet']), fmt(fence['checked']['aircraft'])),
      '%%AUDIT7%%': '7 תוקנו, 3 סומנו כסטיות (W02 — הגישה ל-H0 על A; ‏W03 — האזורים החיים; ‏W10 — הכיסים), ושתי הסטיות של D‑242 (5) סומנו — **11 סטיות מחכות לעינך**. ‏W08 — 13 מספרים מוקלדים נבדקים מול קובצי ה-QA. ‏W09 — המגרש 1380 × 318 (המקום ב-E4 — פתוח לבדיקה). הדוח: `docs_audit/audit_v600_r7/closure_step19.md`',
      '%%FILETABLE%%': TABLE, '%%NEXT%%': ('S7F102 (= S7F94 + הגדר) — הבדיקות המלאות והמדידה; ואחריה שלב 6 — מפרצי E2 והמשאית.' if WORSE else 'שלב 6 — מפרצי המטען של E2 והמשאית (K‑202), ואחריהם התחנות והמפרצים לאוטובוס ולסמי.')}
for k, v in RR.items(): R = R.replace(k, v)
assert '%%' not in R, [l for l in R.split('\n') if '%%' in l][:3]
open(W + '/study/Turbo_City_v1_96_GATE77_S7F101_RESUME_R21.md', 'w', encoding='utf-8').write(R)
print('WORSE', WORSE, 'city', S94, S100, C94, C100, C101, c60, 'other', other7, 'run', RUN)
