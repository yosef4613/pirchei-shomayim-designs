#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""17.11 · v7.04 — עדכון קצר מעל v7.03: S7F305 נמסרה (int305 f6492a7 · גיטהב b430a94); ledger4 (ledger.json, 22:40); הסבב הבא — HOME-02 ו-D‑705.
Idempotent; the data before: _to_delete/new_before_step103.json.  usage: STEP_AT='17.11.2026 23:05' python3 tools/v600_step103.py"""
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); WORK = os.path.dirname(ROOT)
P = lambda p: os.path.join(ROOT, p); W = lambda p: os.path.join(WORK, p)
sys.path.insert(0, HERE)
import v600_heb as HEB
b = P('_to_delete/new_before_step103.json')
if not os.path.exists(b): shutil.copy(P('data/new.json'), b)
b2 = W('_to_delete/plan600_new_before_step103.json')
if not os.path.exists(b2): shutil.copy(b, b2)
N = json.load(open(b, encoding='utf-8'))
LG = json.load(open(W('deliver/2026-11-17/ledger/ledger.json'), encoding='utf-8'))
AT = os.environ.get('STEP_AT', '17.11.2026 23:05')
assert N['meta']['title'] == 'תוכנית אב v7.03', N['meta']['title']
N['meta']['title'] = 'תוכנית אב v7.04'; N['meta']['at'] = AT[:10]
BB = {x['id']: x for x in N['bands2']}
# 1 · S7F305 in the deliveries
D = BB['deliv1117']; D['title'] = 'המסירות של 17.11 — S7F299 עד S7F305 (7 מסירות)'
D['rows'] = [r for r in D['rows'] if r[0] != 'S7F305'] + [[
 'S7F305', 'ערב', 'int305 f6492a7 · 597dc93c7db8 · 30.6 מ"ב · גיטהב b430a94 (25 חלקים)',
 '15 ענפים: buses (עצירה רק בסכנה; התור בכיכרות — כבוי), ‏actions2 (17 תנוחות, אין שלב שמתחיל לבד), ‏story56 (פרקים 5–6 והסוף "פסטיבל העיר"), ‏farm (20 חלקות), סרטון הפתיחה (73 שנ׳), ‏posters (פרסומות האוטובוס פי 4), ‏actions, ‏airfront (S16M), ‏story2 ("המפה שלי", D‑704), ‏perf (משימה ראשונה 4.4 מ"ש), ‏terminal (מסועים, מושבים, לוח הסעה), ‏arena (אולם כדורסל ב-E9 + ליגה, מופעי מחצית), ‏closezoom (זום 16 ברגל — D‑705), ‏rails (מספריים ב-E4 — D‑704), ‏brandin (488 "לשמור" + חידוש 01 — D‑703). בחוץ: home ‏df5f891 (HOME-02 — nf_score), ‏airfront ‏c3b9360, ‏locks',
 'q_ingame 351/351 · rules_gate · stuckmax 150 (בהרצה החוזרת 0) · people_on_road · rails_check 9/9 · nfkiss · t13']]
# 2 · the ledger (ledger4)
S3 = LG['s3']; K = {'G': 'במשחק', 'S': 'עצר להיום', 'W': 'בעבודה', 'N': 'לא התחיל', 'O': 'לאישורך', 'D': 'מחוץ למשחק', 'M': 'במיזוג'}
fmt = lambda d: ' · '.join('%s %d' % (K.get(k, k), v) for k, v in d.items())
pct = lambda d: '%d%%' % round(100.0 * d.get('G', 0) / sum(d.values()))
R = [['66 המשימות (Turbo_City_after_S16_tasks)', str(sum(S3['plan66'].values())), fmt(S3['plan66']), pct(S3['plan66'])],
     ['98 הנקודות של הביקורת', str(sum(S3['points98'].values())), fmt(S3['points98']), pct(S3['points98'])],
     ['194 הפריטים של הרשימה המרוכזת', str(sum(S3['items'].values())), fmt(S3['items']), pct(S3['items'])],
     ['הבקשות של 17.11', str(sum(S3['owner17'].values())), fmt(S3['owner17']), pct(S3['owner17'])]]
for ph in S3['phases']: R.append(['%s — %s' % (ph['id'], ph['title']), str(sum(ph['counts'].values())), fmt(ph['counts']), pct(ph['counts'])])
L = BB['ledger1117']; L['title'] = 'איפה אוחזים — 66 המשימות ו-98 הנקודות (ledger4, סוף היום)'; L['rows'] = R
L['note'] = 'מ-deliver/2026-11-17/ledger/ledger.json (%s; ‏%s) — מאומת מול git: "במשחק" = ה-commit בתגית שנמסרה; "עצר להיום" = חלקי, שמור בענף, ממשיך בסבב הבא. הרשימה המלאה: https://claude.ai/artifact/KYUAkit4Pz8b7bjCieM2Qa' % (LG['version'], LG['base'])
T = BB['tasks66']; T['title'] = '66 המשימות — שורה לכל משימה (ledger4)'; T['note'] = 'הסטטוס, מה יש במשחק ומה חסר — לפי ledger4 (אחרי S7F305).'
T['rows'] = [[p['id'], p['phase'], p['title'], p.get('st_label', ''), p.get('have', '') or '', p.get('miss', '') or ''] for p in LG['plan']]
# 3 · the next round: HOME-02 and D‑705
NX = [r for r in BB['next1118']['rows'] if r[1] not in ('הבית', 'למחשב בלבד (D‑705)')]
for r in NX:
    if r[1] == 'הנעילות': r[2] = 'locks ‏a8f4ee0 — לא הגיע ל-S7F305 (rules_gate נכשל ב-build_texts וב-lock_reach); לתקן ולמזג; E3 → פרק 1, ‏F7 → פרק 5 (לאישורך)'
for r in NX:
    if r[1].startswith('הכיכרות'): r[1] = 'הכיכרות — התור ההוגן'
    if r[1].startswith('הבדיקה של') or 'TCBUSY' in r[1]: r[1] = 'הבדיקות של סדר השכבות האחד'
i = next(k for k, r in enumerate(NX) if r[1].startswith('הכיכרות'))
NX.insert(i, ['', 'הבית', 'HOME-02 (פנים הבית ב-8 הרמות, df5f891) — יצא מ-S7F305 בגלל ציון הסינון (מילים באנגלית בנתונים); עכשיו בבדיקת הסינון t14 — אם עובר, נכנס ראשון. אחריו: Esc (ca20778), החזית / הגדר (030, BLD40), "לנוח בבית", המזווה', 'home', 'W16 / HOME'])
NX.append(['', 'למחשב בלבד (D‑705)', 'נכנס ב-S7F305: זום 16 ברגל. מעכשיו מסך צר / טלפון אינו יעד ביצועים — הבדיקות של הביצועים במסך מחשב בלבד', 'closezoom / perf', 'W25'])
FIX = [(' (על רב״ף)', ''), (' (טסביס״ו)', ''), ('— פתוח, ', '— סרטון הפתיחה, ')]
for k, r in enumerate(NX):
    r[0] = str(k + 1)
    for a_, b_ in FIX: r[2] = r[2].replace(a_, b_)
BB['next1118']['rows'] = NX; BB['next1118']['title'] = 'הסבב הבא — לפי הסדר (%d גושים)' % len(NX)
BB['next1118']['note'] = 'הסדר של המתאם (17.11 22:30, ועדכון אחרי S7F305). לפני כל גוש — ציור / חישוב, ואחריו הסט החוסם.'
# 4 · the decisions: the state now
NOW = {'D‑703': 'בוצע — S7F305 (brandin: 488 "לשמור" + ששת המזנונים)', 'D‑705': 'בוצע — S7F305 (closezoom: זום 16 ברגל)',
       'D‑704': '(3) ו-(4) בוצעו — S7F305 (rails, ‏story2); (1)–(2) — fieldexit, הסבב הבא', 'D‑700': 'HOME-01 — S7F304; HOME-02 — בבדיקת הסינון t14; Esc וחזית — הסבב הבא'}
for d in N['decisions']:
    if d['id'] in NOW: d['now'] = NOW[d['id']]; d['status'] = NOW[d['id']] + ' · ההחלטה של הבעלים — בתוקף'
for r in BB['dec1117']['rows']:
    if r[0] in NOW: r[3] = NOW[r[0]]
# 5 · the top line, build, links, log, changes
g, p = S3['plan66'], S3['points98']
TOP = ('עודכן 17.11 %s — S7F305 (המסירה ה-7 של היום) · 66 המשימות: במשחק %d, עצר להיום %d, לא התחיל %d · 98 הנקודות: %d / %d / %d (ledger4) · '
       'בשעות — כמו v7.02 (לפי S7F299): ' % (AT[-5:], g.get('G', 0), g.get('S', 0), g.get('N', 0), p.get('G', 0), p.get('S', 0), p.get('N', 0)))
st = re.sub(r'^עודכן 17\.11 [^·]*— S7F30[45] [^·]*· 66 המשימות[^·]*· 98 הנקודות[^·]*· בשעות — כמו v7\.02 \(לפי S7F299\): ', '', N['meta']['statusText'])
assert not st.startswith('עודכן 17.11 2'), st[:120]
N['meta']['statusText'] = TOP + st
N['meta']['build'] = 'S7F305'
N['meta']['runLine'] = 'נמסרה: S7F305 (597dc93c7db8 · 30,628,831 — משוחרר; גיטהב b430a94; int305 f6492a7) · מצב האזורים והסנכרון — עדיין על S7F299'
for r in BB['links']['rows']:
    if r[0].startswith('הבנייה האחרונה'): r[2] = 'המשחק שנמסר — S7F305 (597dc93c7db8; גיטהב b430a94)'
    if r[0] == 'המשחק בגיטהב (הקישור הקבוע)': r[2] = 'מכאן מריצים; ‏S7F305 — b430a94 (25 חלקים, split_any 1.3)'
DR = list(N['doneLog'])
for s_, wh in [('S7F305 — 15 ענפים: buses, actions2, story56, farm, opening, posters, actions, airfront, story2, perf, terminal, arena, closezoom, rails, brandin', '17.11 ערב'),
               ('התוכנית v7.04 — S7F305, ‏ledger4, הסבב הבא — המסמכים (docs2)', '17.11 ' + AT[-5:])]:
    if not any(r['step'] == s_ for r in DR): DR.append({'n': str(len(DR) + 1), 'step': s_, 'when': 'נעשה · ' + wh, 'dur': '—', 'gate': False})
N['doneLog'] = DR
BB['doneLog']['rows'] = [[r['n'], r['step'], r['when'].replace('נעשה · ', '')] for r in DR]; BB['doneLog']['title'] = 'מה נעשה — יומן הבניות והגרסאות (%d שורות)' % len(DR)
CH = N['changes']
if not any(c.get('v') == 'v7.04' for c in CH):
    for c in CH: c['order'] = c.get('order', 0) + 1
    CH.insert(0, {'v': 'v7.04', 'order': 0, 'at': AT, 'done': ['S7F305'],
                  'changed': ['S7F305 בטבלת המסירות (15 ענפים)', '66 המשימות / 98 הנקודות לפי ledger4: %s; %s' % (fmt(g), fmt(p)),
                              'הסבב הבא — HOME-02 בבדיקת הסינון t14; D‑705 (למחשב בלבד, זום 16)', 'D‑700, ‏D‑703 – D‑705 — המצב עכשיו'],
                  'found': [], 'fixed': [], 'decided': [], 'tests': ['הבדיקה בדפדפן (headcheck)'], 'active': []})
A = N['audit']; U = ' · עדכון 17.11 %s (v7.04): S7F305, ‏ledger4.' % AT[-5:]
if U not in A['summary']: A['summary'] += U
N = HEB.walk(N)
json.dump(N, open(P('data/new.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('step103 ok', N['meta']['statusText'][:260])
