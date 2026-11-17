#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""17.11 · v7.03 — עדכון ממוקד מעל v7.02 (docs2, ‏הבעלים 22:30: "דף התוכנית מעודכן?").
(1) המסירות S7F299 – S7F304 (S7F305 — גל 6, עוד לא נמסרה); (2) D‑699 – D‑705; (3) 66 המשימות ו-98 הנקודות לפי ledger3 (ledger.json);
(4) תוכנית הסבב הבא לפי הסדר. האחוזים בשעות — כמו v7.02 (המעבר על S7F299); לא חושבו מחדש.
Idempotent; the data before: _to_delete/*_before_step102.json.  usage: STEP_AT='17.11.2026 22:50' python3 tools/v600_step102.py"""
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); WORK = os.path.dirname(ROOT)
P = lambda p: os.path.join(ROOT, p); W = lambda p: os.path.join(WORK, p)
sys.path.insert(0, HERE)
import v600_heb as HEB
b = P('_to_delete/new_before_step102.json')
if not os.path.exists(b): shutil.copy(P('data/new.json'), b)
b2 = W('_to_delete/plan600_new_before_step102.json')
if not os.path.exists(b2): shutil.copy(b, b2)
N = json.load(open(b, encoding='utf-8'))
LG = json.load(open(W('deliver/2026-11-17/ledger/ledger.json'), encoding='utf-8'))
AT = os.environ.get('STEP_AT', '17.11.2026 22:50')
assert N['meta']['title'] == 'תוכנית אב v7.02', N['meta']['title']
N['meta']['title'] = 'תוכנית אב v7.03'; N['meta']['at'] = AT[:10]

# ---------------- 1 · the deliveries of 17.11 ----------------
DEL = [
 ['S7F299', '07:05', 'int299 930919a · 14a90a1cffb9 · 21.1 מ"ב',
  '15 ענפים: f9fix (F9 עובד), ‏stadium (לפי שעון המשחק), ‏posters (האייקון + סט 11), ‏seatrees, ‏mapfix (80 אזורים במפה), ‏garage (מסך F מסתובב), ‏portraits (104 דיוקנאות), ‏pier (M-F2-PICKUP), ‏loading, ‏locks (קיר פיזי), ‏newgame (הדרכה 7 צעדים), ‏cutscenes (17 סצנות), ‏missions (D‑693), ‏fieldcalc, ‏fieldfix',
  'q_ingame 330/330 · rules_gate · stuckmax 150 · people_on_road · q_stadium3'],
 ['S7F300', '09:50', 'int300 17664a9 · 751e269ec95e · 26.7 מ"ב',
  '11 ענפים: seatrees, ‏signs (סט 12 — 45 שלטי זהות), ‏pier, ‏missions (הכרטיס לא מעל סצנה), ‏carrier (הפריקה ב-D3), ‏garage (המוסך בעיר), ‏events (אש, נופל, בורח), ‏voiceint (311 הקלטות), ‏actions (140 שלבים), ‏fieldfix (G3 / H0–H3 חי), ‏fieldcalc (5 עמדות כבודה)',
  'q_ingame 336/336 · החוסם עבר · NetFree חסם → גיטהב בחלקים'],
 ['S7F301', '12:20', 'hotfix301 5e81076 · 34b531092196 · 29.4 מ"ב',
  'S7F300 + תיקוני הסינון בלבד: release_strip (הערות JS, מחרוזות hex), kiss→drop, מותגים באלפבית; deliver_rel.sh + split_any 1.3 (24 חלקים)',
  'הבעלים: t9 — "הכל עבר"'],
 ['S7F302', '13:35', 'int302 8df9421 · c7ce0602ad9d · 29.5 מ"ב',
  '10 ענפים: f9fix, ‏missions (TCBUSY — סדר השכבות האחד), ‏actions (חפץ חסום, תצפיות), ‏cutscenes (הגוררת, אליהו), ‏newgame, ‏garage (העבודה בתא), ‏police (קנס רק כשנתפסים, רישיון טיס — D‑691), ‏fieldcalc, ‏island (מזרח האי, רכבת המשא), ‏seatrees',
  'q_ingame 343/343 · t10 — "עברה ללא חסימות" · q_stadium3 נכשל בעיגול — תוקן ב-S7F303'],
 ['S7F303', '16:25', 'int303 41d3604 · cc441f18836b · 29.7 מ"ב',
  '7 ענפים: perf (בלי קפיצות ירוק בזום), ‏events (מסוקי חירום, סירנה), ‏island (צומת מרומזר, E9 — שלב 2ג-1), ‏sealife (הגוררות, הנפט לבית הזיקוק), ‏w17 (לעלות על כל כלי, SP-06), ‏loading, ‏fieldthru (65 תנועות / 30 דק׳ מול 44–45 בישן)',
  'q_ingame 346/346 · t11 — "הכל עבר"'],
 ['S7F304', '19:30', 'int304 a8857ec · d048bb32d3b4 · 29.8 מ"ב',
  '5 ענפים: home (HOME-01 — שינה מ-F ב-8 הרמות, "הצץ", מסוק עומד — D‑700), ‏airlogos (הלוגואים והשילוט של השדה), ‏island (מסוף המעבורת ב-E9, 2ג-2א / 2ג-2ב-1, "צוק הים"), ‏perf (NPR), ‏fieldthru2 (סוג לכל ביקור, D‑701 במפה)',
  'q_ingame 348/348 · t12 — "הכל עבר בסינון" · זיכרון +1 מ"ב'],
 ['S7F305', 'גל 6 — עוד לא נמסרה', 'merge6 — בתור (merge6_queue.txt)',
  'בתור: farm (20 חלקות), ‏opening (סרטון פתיחה 73 שנ׳), ‏story2 (המפה שלי), ‏perf ‏94554b2 (משימה ראשונה 4.4 מ"ש), ‏posters, ‏actions, ‏terminal, ‏actions2 (17 תנוחות), ‏buses, ‏airfront ‏d3127b3, ‏story56 (פרקים 5–6 והסוף), ‏arena, ‏home ‏df5f891 (HOME-02 — פנים 8 הרמות), ‏closezoom (D‑705), ‏rails ‏f6104e8, ‏brandin ‏61f7993 (D‑703). בחוץ: locks ‏a8f4ee0 (rules_gate)',
  'כשתימסר — עדכון v7.04'],
]
BAND_DEL = {'id': 'deliv1117', 'title': 'המסירות של 17.11 — S7F299 עד S7F304 (6 מסירות; S7F305 בדרך)',
            'note': 'מה נכנס בכל מסירה — לפי HANDOFF_1111.md וההחזרות של merge – merge5. בכל אחת עבר הסט החוסם (q_ingame, ‏rules_gate, ‏stuckmax 150, ‏people_on_road, ‏0 שגיאות, ‏0 data:image). מ-S7F301 — משוחרר לסינון, בגיטהב ב-24 חלקים.',
            'cols': ['המסירה', 'מתי', 'הבנייה', 'מה נכנס', 'הבדיקות'], 'rows': DEL}
# ---------------- 2 · D‑699 – D‑705 ----------------
DEC = [
 ('D‑699', 'ניסוי ספריות הגרפיקה — לא מאמצים', 'הבעלים 17.11 ~11:55: "המכוניות והמטוסים והאנשים החדש הרבה פחות מוצלח". G2 (וגם Zdog / SVG.js) לא נכנס; נשארים עם C34 / A34 / P34; t17_gfxlib בארכיון (lab/).', 'בתוקף — בוצע (לא נכנס)'),
 ('D‑700', 'בית השחקן: סטודיו, מסוק עומד, "הצץ"', 'הבעלים 17.11 ~14:30: סטודיו העיצוב ברמה 6 עם F; המסוק ברמות 7–8 עומד בלי רוטור; "הצץ" לרמה לפני קנייה. מבצע: home.', 'בוצע ברובו — S7F304 (HOME-01); HOME-02 — בגל 6; Esc וחזית — הסבב הבא'),
 ('D‑701', 'השדה — העומס ב-B', 'הבעלים 17.11 ~15:05 / 15:10: נתיב שני במעבר B (יוצא / נכנס; גדול → אחד-אחד); מחבר A3 חדש בין A2 ל-A3, הקיים → A4; המראה הפוכה רק כשפנוי לגמרי. מבצע: fieldthru2.', 'בוצע — S7F304 (fieldthru2, במפה); P6 והגדולים — הסבב הבא'),
 ('D‑702', 'השדה — שירות 100% לכל טיסה', 'הבעלים 17.11 ~15:35: מזוודות, קייטרינג, דלק, גרר — 100%; בלי שרוול — מדרגות + אוטובוס; מים / שירותים לפי אורך הטיסה ≥60%; כל רכב מתמלא בתחנה שלו (חוות דלק, מים, ניקוז, מטבח). מבצע: fieldsvc.', 'בעבודה — fieldsvc2: 6/13 (46%), לא מוכן; הסבב הבא'),
 ('D‑703', 'חידוש 01 של המעצב — מאושר', 'הבעלים 17.11 ~19:00: ששת מזנוני השדה — לוגו מאויר ושלט אופקי במקום הזמניים. מבצע: brandin.', 'בגל 6 — brandin ‏61f7993 (488 "לשמור" נכנסו)'),
 ('D‑704', 'השדה והמסילות — "הכל לאשר"', 'הבעלים 17.11 ~19:30: (1) יציאה מהירה בזווית מהמסלול; (2) גדר רחבת המשא דרומה (y ~1000) — HC על CH ו-CG; (3) מספריים בתחנת החוף E4 במקום D‑536; (4) story2 — תזכורת כל 6–9 דק׳, ההצעה ב"מפה שלי". הגדולים ב-P6 — אחרי היציאה המהירה.', '(4) בגל 6 (story2); (3) rails — בגל 6; (1)–(2) fieldexit — עצר בהחזרה, הסבב הבא'),
 ('D‑705', 'המשחק למחשב בלבד', 'הבעלים 17.11 ~21:55: "זה לשימוש במחשב בלבד" — מסך צר / טלפון אינו יעד ביצועים; זום קרוב ברגל — עד 16.', 'בגל 6 אם בחלון (closezoom), אחרת הסבב הבא'),
]
ids = {d['id'] for d in N['decisions']}
for i, t, x, st in DEC:
    if i not in ids:
        N['decisions'].append({'id': i, 'topic': t, 'text': x, 'status': st + ' · ההחלטה של הבעלים — בתוקף', 'now': st, 'stages': [], 'open': True, 'pend': ''})
BAND_DEC = {'id': 'dec1117', 'title': 'ההחלטות של 17.11 — D‑699 עד D‑705', 'note': 'מ-DECISIONS_1110.md; "המצב עכשיו" — לפי המסירות וההחזרות עד 22:30. הן גם ברשימת ההחלטות.',
            'cols': ['ההחלטה', 'הנושא', 'מה הוחלט', 'המצב עכשיו'], 'rows': [[i, t, x, st] for i, t, x, st in DEC]}
# ---------------- 3 · the ledger (ledger3) ----------------
S3 = LG['s3']; K = {'G': 'במשחק', 'W': 'בעבודה', 'N': 'לא התחיל', 'O': 'לאישורך', 'D': 'מחוץ למשחק'}
fmt = lambda d: ' · '.join('%s %d' % (K[k], v) for k, v in d.items())
pct = lambda d: '%d%%' % round(100.0 * d.get('G', 0) / sum(d.values()))
LROWS = [['66 המשימות (Turbo_City_after_S16_tasks)', str(sum(S3['plan66'].values())), fmt(S3['plan66']), pct(S3['plan66'])],
         ['98 הנקודות של הביקורת', str(sum(S3['points98'].values())), fmt(S3['points98']), pct(S3['points98'])],
         ['194 הפריטים של הרשימה המרוכזת', str(sum(S3['items'].values())), fmt(S3['items']), pct(S3['items'])],
         ['הבקשות של 17.11 (37)', str(sum(S3['owner17'].values())), fmt(S3['owner17']), pct(S3['owner17'])]]
for ph in S3['phases']:
    LROWS.append(['%s — %s' % (ph['id'], ph['title']), str(sum(ph['counts'].values())), fmt(ph['counts']), pct(ph['counts'])])
BAND_LG = {'id': 'ledger1117', 'title': 'איפה אוחזים — 66 המשימות ו-98 הנקודות (ledger3)',
           'note': 'מ-deliver/2026-11-17/ledger/ledger.json (%s; ‏%s) — סטטוס מאומת מול git: "במשחק" = ה-commit בתגית שנמסרה. מה שנכנס ב-S7F304 וגל 6 עוד לא נספר כאן. הרשימה המלאה: https://claude.ai/artifact/KYUAkit4Pz8b7bjCieM2Qa' % (LG['version'], LG['base']),
           'cols': ['מה', 'כמה', 'הפירוט', 'במשחק'], 'rows': LROWS}
TROWS = [[p['id'], p['phase'], p['title'], p.get('st_label', ''), p.get('have', '') or '', p.get('miss', '') or ''] for p in LG['plan']]
BAND_T = {'id': 'tasks66', 'title': '66 המשימות — שורה לכל משימה (ledger3)', 'note': 'הסטטוס, מה יש במשחק ומה חסר — לפי ledger3 (אחרי S7F303).',
          'cols': ['המשימה', 'הגוש', 'מה', 'הסטטוס', 'מה יש', 'מה חסר'], 'rows': TROWS}
# ---------------- 4 · the next round, in order ----------------
NX = [
 ['1', 'השדה', 'P6 פעילה (s15pax / fc_bridge_types); יציאה מהירה מהמסלול וגדר רחבת המשא (D‑704, ‏fieldexit); הדרום — 88–92 תנועות (מתכנן עם חזרה אחורה); משא ענק — CG ב-C1 ו-HC על CH; השירותים ל-100% (D‑702, ‏fieldsvc2: היום 6/13); התחנות — חוות דלק, מים, ניקוז, מטבח, והמחזור', 'fieldexit, ‏fieldsvc2, ‏fieldthru2, ‏airfront (S16C / S16R)', 'S15, ‏S16, ‏S18'],
 ['2', 'קווים 5 / 5א ולקו 4', 'קווים 5 / 5א — 2–3 שע׳ (401 חונה במקום של הקואץ׳ ב-L5); קו 4 — להעביר 2 מקו 1 או להוסיף 2 לחניון (לאישורך)', 'buses', 'W10'],
 ['3', 'הלוגיסטיקה', 'מדידת 13 הזרמים של תוכנית הסחורות (ס-10, ‏D‑378) — מה זורם באמת במשחק מול התוכנית', 'לוגיסטיקה (סוכן חדש)', 'W11'],
 ['4', 'האי', 'המרינה, ההר, הגשר (BR-I) — המשך D‑694 אחרי 2ג-2ב-1; פקק IS-W / BR-I; האולם של arena מוצק', 'island5', 'S17'],
 ['5', 'הנעילות', 'locks ‏a8f4ee0 — rules_gate נכשל ב-build_texts וב-lock_reach (סף הזמן); לתקן ולמזג; E3 → פרק 1, ‏F7 → פרק 5 (לאישורך)', 'locks', 'W28'],
 ['6', 'הבית', 'Esc (ca20778), החזית / הגדר (מנגנון ב-030, BLD40), "לנוח בבית" בסיפור, תוצרת החווה במזווה', 'home', 'W16 / HOME'],
 ['7', 'הכיכרות (RBF)', 'התור ההוגן בכיכרות — בנוי וכבוי (RBF.on); 3 בדיקות (~45 דק׳) ואז להדליק; רמזור כניסה לכיכר — לאישורך', 'buses', 'W10'],
 ['8', 'ה-probes של TCBUSY', 'לעדכן את הבדיקות לסדר השכבות האחד (TCBUSY) — opening, story2 (s15j_terminal / fieldfix_r3), cutscenes', 'missions / leftovers', 'W27 / W29'],
 ['9', '67 שורות להקלטה', '67 שורות קול חדשות של פרקים 5–6 והסוף (story56/voice_lines_to_record.txt; הקולות לפי הדמויות) — להקלטה ב-voice3', 'voice3 / story56', 'W27'],
]
BAND_NX = {'id': 'next1118', 'title': 'הסבב הבא — לפי הסדר (9 גושים)', 'note': 'הסדר של המתאם (17.11 22:30). לפני כל גוש — ציור / חישוב, ואחריו הסט החוסם. מה שבגל 6 (S7F305) — נכנס קודם.',
            'cols': ['#', 'הגוש', 'מה', 'הסוכן', 'השלב'], 'rows': NX}
NEWB = [BAND_DEL, BAND_DEC, BAND_LG, BAND_NX, BAND_T]
keep = [x for x in N['bands2'] if x['id'] not in {y['id'] for y in NEWB}]
N['bands2'] = NEWB + keep
# ---------------- 5 · the top line, the log, the links, the changes ----------------
g66 = S3['plan66']; g98 = S3['points98']
TOP = ('עודכן 17.11 %s — S7F304 (המסירה ה-6 של היום; S7F305 — גל 6, בדרך) · 66 המשימות: במשחק %d, בעבודה %d, לא התחיל %d · 98 הנקודות: %d / %d / %d (ledger3) · '
       'בשעות — כמו v7.02 (לפי S7F299): ' % (AT[-5:], g66['G'], g66['W'], g66['N'], g98['G'], g98['W'], g98['N']))
st = N['meta']['statusText']
st = re.sub(r'^עודכן 17\.11 [^·]*— S7F304 [^·]*· 66 המשימות[^·]*· 98 הנקודות[^·]*· בשעות — כמו v7\.02 \(לפי S7F299\): ', '', st)
st = st.replace('עודכן 17.11 — S7F299 · ', '', 1)
N['meta']['statusText'] = TOP + st
N['meta']['build'] = 'S7F304'
N['meta']['runLine'] = 'נמסרה: S7F304 (d048bb32d3b4 · 29,841,462 — משוחרר, בגיטהב 63de163 ב-24 חלקים; 17.11 19:30) · מצב האזורים והסנכרון — עדיין על S7F299'
for r in next(x for x in N['bands2'] if x['id'] == 'links')['rows']:
    if r[0].startswith('הבנייה האחרונה'): r[2] = 'המשחק שנמסר — S7F304 (d048bb32d3b4; גיטהב 63de163, 24 חלקים)'
    if r[0] == 'המשחק בגיטהב (הקישור הקבוע)': r[2] = 'מכאן מריצים; ‏S7F304 — 63de163 (24 חלקים, split_any 1.3)'
DONE_ROWS = list(N['doneLog'])
for st_, wh in [('S7F300 — 11 ענפים: seatrees, signs, pier, missions, carrier, garage, events, voiceint, actions, fieldfix, fieldcalc', '17.11 09:50'),
                ('S7F301 — תיקוני הסינון (release_strip, kiss→drop); גיטהב ב-24 חלקים', '17.11 12:20'),
                ('S7F302 — 10 ענפים: f9fix, missions (TCBUSY), actions, cutscenes, newgame, garage, police, fieldcalc, island, seatrees', '17.11 13:35'),
                ('S7F303 — 7 ענפים: perf, events, island, sealife, w17, loading, fieldthru', '17.11 16:25'),
                ('S7F304 — 5 ענפים: home (HOME-01), airlogos, island, perf, fieldthru2', '17.11 19:30'),
                ('התוכנית v7.03 — המסירות S7F299 – S7F304, ‏D‑699 – D‑705, ‏ledger3, הסבב הבא — המסמכים (docs2)', '17.11 ' + AT[-5:])]:
    if not any(r['step'] == st_ for r in DONE_ROWS): DONE_ROWS.append({'n': str(len(DONE_ROWS) + 1), 'step': st_, 'when': 'נעשה · ' + wh, 'dur': '—', 'gate': False})
N['doneLog'] = DONE_ROWS
dl = next(x for x in N['bands2'] if x['id'] == 'doneLog')
dl['rows'] = [[r['n'], r['step'], r['when'].replace('נעשה · ', '')] for r in DONE_ROWS]; dl['title'] = 'מה נעשה — יומן הבניות והגרסאות (%d שורות)' % len(DONE_ROWS)
CH = N['changes']
if not any(c.get('v') == 'v7.03' for c in CH):
    for c in CH: c['order'] = c.get('order', 0) + 1
    CH.insert(0, {'v': 'v7.03', 'order': 0, 'at': AT, 'done': ['S7F300', 'S7F301', 'S7F302', 'S7F303', 'S7F304'],
                  'changed': ['טבלת המסירות של 17.11 (S7F299 – S7F304)', 'D‑699 – D‑705 — נוספו, עם המצב עכשיו',
                              '66 המשימות / 98 הנקודות לפי ledger3 — טבלה', 'הסבב הבא — 9 גושים לפי הסדר', 'האחוזים בשעות — לא חושבו מחדש (כמו v7.02)'],
                  'found': [], 'fixed': [], 'decided': ['D‑699 – D‑705'], 'tests': ['הבדיקה בדפדפן (headcheck)'], 'active': []})
A = N['audit']; U = ' · עדכון 17.11 %s (v7.03): S7F300 – S7F304, ‏D‑699 – D‑705, ‏ledger3.' % AT[-5:]
if U not in A['summary']: A['summary'] += U
N = HEB.walk(N)
json.dump(N, open(P('data/new.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('step102 ok', N['meta']['statusText'][:300])
