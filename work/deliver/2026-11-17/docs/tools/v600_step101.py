#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""17.11 · v7.02 — העדכון אחרי S7F299 (int299 930919a · cand299x · 14a90a1cffb9 · 21,094,749; ‏15 ענפים של סבב 17.11 — deliver/2026-11-17/merge/handback.txt).
מעל v7.01 (v600_step100.py): S7F299 בראש; ההתקדמות של השלבים שזזו — לפי ההבדל S7F298 → S7F299 (git diff — 30 חלקים, 16 חדשים) והבדיקות של המיזוג;
ההחלטות D‑691 – D‑695 — "המצב עכשיו"; "מחכה לך" — האיחוד של missions; היומן; "כמה נשאר".
Idempotent; the data before: _to_delete/*_before_step101.json.  usage: STEP_AT='17.11.2026 07:20' python3 tools/v600_step101.py"""
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); WORK = os.path.dirname(ROOT)
P = lambda p: os.path.join(ROOT, p); W = lambda p: os.path.join(WORK, p)
sys.path.insert(0, HERE); sys.path.insert(0, W('tools_pack'))
import v600_heb as HEB, plan_sync
for f_ in ('data/new.json', 'data/masterplan.json', 'data/stages.json', 'data/schedule_s7_s16.json'):
    b = P('_to_delete/' + os.path.basename(f_).replace('.json', '_before_step101.json'))
    if not os.path.exists(b): shutil.copy(P(f_), b)
    b2 = W('_to_delete/plan600_' + os.path.basename(f_).replace('.json', '_before_step101.json'))
    if not os.path.exists(b2): shutil.copy(b, b2)
L_ = lambda n: json.load(open(P('_to_delete/' + n + '_before_step101.json'), encoding='utf-8'))
N = L_('new'); MP = L_('masterplan'); S = L_('stages'); SCH = L_('schedule_s7_s16')
AT = os.environ.get('STEP_AT', '17.11.2026 07:20')
Q0, Q1, WEEK, DONE_V699 = 8.0, 97.8, 98.0, 744.8      # the rate of 11.11, as in v7.01
BUILD = W('clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F299.html')
assert N['meta']['title'] == 'תוכנית אב v7.01', N['meta']['title']
N['meta']['title'] = 'תוכנית אב v7.02'; N['meta']['at'] = AT[:10]
r1 = lambda v: ('%.1f' % v).rstrip('0').rstrip('.')
c1 = lambda v: format(round(v, 1), ',.1f')
SS = N['stageSys']; NB = {s['id']: s for s in SS['stages']}
NEWIDS = ['S17', 'S18', 'W27', 'W28', 'W29', 'W30', 'W31', 'W32', 'W33', 'W34']
OLD_IDS = [s['id'] for s in SS['stages'] if s['id'] not in NEWIDS]
D0 = round(sum(s['hours'] * (s['progress'] or 0) / 100 for s in SS['stages']), 2)
# ---------------- 1 · the pass over S7F298 → S7F299 (git diff S7F298 S7F299 -- parts: 30 parts, 16 new) ----------------
# id: (progress, with the ready branches, what entered, the code, what is left — None = drop the items that entered)
AU = {
 'W27': (45.0, 45.0,
         ['D‑693 — לוח המשימות: צד 4–6 והצעה אחת, סיפור 1–3 (2–3 משימות בכל סדר), הסמנים רק מהלוח; ההודעה, הכרטיס, הסמן והניווט על אותו מצב (missions, ‏S7F299)',
          'דיוקן מצויר בקוד לכל איש קשר (104), צבע וסמל לכרטיסים (portraits, ‏S7F299)'],
         ['074zu_mission_board.js', '074ze_story_engine.js (open / next / focus / MAXOPEN)', '038a_E4E5_s9_live.js:S9STORY.start', '074zp_portraits.js'],
         ['פעולות משחק אמיתיות — הרמה / נשיאה / מסירה / תיקון (156 / 228 שלבים) — actions, לא מוכן למיזוג ב-06:47', 'יום משחק מלא עם הלוח (mb_day) — לא נבדק על המועמד',
          'הכרטיס של הלוח מעל סצנה שמתנגנת — להסתיר כש-TCCUT.playing() (merge)']),
 'W28': (75.0, 75.0,
         ['שמירה חדשה נפתחת נקי + הדרכה מובנית — 7 צעדים, "הבית של סבא" (newgame, ‏S7F299)', 'נעילה פיזית — קיר בגבול אזור נעול לרגל, לרכב ולסירה; ניווט ומונית רק בקטעים פתוחים (locks, ‏S7F299)',
          'מזח הגוררות — הליכה רציפה ל-5 המקומות על המזחים; ‏F מתוך רכב עומד (pier, ‏S7F299)'],
         ['074zu_newgame_tut.js', '055_G2_F2_p296.js', '074zu_locks_phys.js', '074zp_pier_pickup.js'],
         ['ng_play מקצה לקצה על הבנייה המאוחדת — לא נבדק', 'F מתוך רכב — 13 מתוך 23 מקומות', 'pier ‏6bab6c9 — "בבדיקה" (הגל הבא)']),
 'W29': (60.0, 60.0,
         ['סצנות הסיפור במנוע — 17 סצנות: הפתיחה, הטנדר, הנחיתה, הגוררת; Esc מדלג; צפייה חוזרת ביומן וב-F9 (cutscenes, ‏S7F299)',
          'מסך הטעינה בפריים הראשון — 10 איורים וטיפים ב-SVG בקוד, התקדמות אמיתית (MAPBASE, אריחים, C34, השדה), בכל טעינה (loading, ‏S7F299)'],
         ['074zu_cutscenes.js:TCCUT', '009c_loading.js:TCLD', '074zf9_loading_hooks.js'],
         ['סרטון הפתיחה במנוע — opening, לא מוכן למיזוג ב-06:47', 'הפס של מסך הפתיחה יורד באפייה השנייה של mapfix (B.rebake מאפס את MAPBASE.next)', 'loading ‏db999f9 — הגל הבא']),
 'W31': (80.0, 80.0,
         ['מסך F של המוסך — הרכב על במה מסתובבת, סל, "קנה" (garage, ‏S7F299; gst_probe: המוסך והבית)'],
         ['074zz2_garage_studio.js'],
         ['אותו מסך בסוכנות — לא נבדק', 'המוסך בעיר עצמו (הבנייה מחדש) — garage ‏0ebac85, אחרי המיזוג (W16)']),
 'W34': (28.0, 28.0,
         ['F9 — האירועים והאזורים עובדים: 58 כפתורי אירועים, 58 אזורים, 0 תקולים; הבדיקה f9_panel ב-roadAudit (f9fix)', 'תוצאות האצטדיון לפי שעון המשחק — השלט, הטלפון, F9 (stadium)',
          'בלי עצים על מים — שומר אחד לכל העולם (seatrees)', 'המפות — השדה ב-G3 / H0–H3, האסדה ב-H8, היער, המקרא, משימות השדה (mapfix)', 'האייקון של המשחק — בקנבס, קישור blob (posters)'],
         ['074_F9.js · 074zz9_f9_audit.js', '074f_league4.js · 024_A3_A4_p549.js · 074v_places.js', '074zh2_seatrees.js', '028_C2_D2_D3_p332.js · 074zp_mapfix.js', '074n3_posters.js (האייקון)'],
         ['3 עצים בשולי מגרש B4 (tree_sweep על המועמד) — seatrees / mapfix', 'האייקון — toBlob בלי ניסיון חוזר תחת עומס (posters)',
          'האוניות, הגוררות, הנפט, ferry2 (sealife)', 'החקלאות (farm)', 'קנס רק כשנתפסים + רישיון טיס (police, ‏D‑691)', 'ביצועים וזיכרון בזומים (perf)', 'סט 12 והפרסומות פי 4 (signs, ‏buses)',
          'הרכבל — 8 קרונות; פנים הבית; השינה בבית; הצגות והפסקה; צפייה במשחק באצטדיון — עוד לא שובצו']),
 'S18': (15.0, 15.0,
         ['המדידה מול החישוב — __TC_FC (תנועות המסלול, השירותים של כל טיסה מול המטריצה, הכבודה) — קריאה בלבד (fieldcalc, ‏S7F299)',
          'R3 ומחזור ההאנגרים בלילה (fieldfix, ‏S7F299)'],
         ['074zq_fieldcalc.js:__TC_FC', '074zo_fieldfix.js', '019m_S15_draw.js'],
         ['הלוח החדש לפי החישוב — יותר טיסות מהישן (הישן 44–45 תנועות בחצי שעה; היום 30)', 'עמדות הכבודה, הצי, ההרחבה דרומה, האמפיבי — הציור → הבקר → הבנייה']),
 'S15': (84.0, 84.0,
         ['הצבעים במבט 3/4 כמו מלמעלה — 4 הסגנונות המלאים (068:liveryFns)', 'הלוח הישן עם הטיסות של היום, הזרם בשרוול, הבגדים (s15pax ‏074x3, ‏S7F299)'],
         ['068_core.js:liveryFns', '074x3_S15pax.js', '051_F1_p190.js'],
         ['23 היפוכים של 180° בדרכים', 'משמרת מנהל צוותי הקרקע — R26‑8', 'AB-R1 / SH-R2 — לעצור בטרמינל', 'חלון ל-AC-AM-01 ב-S15SIM', 'שתי סימולציות שדה רצות (045:aptOpsTick הישנה)', 'החישוב מחדש — S18']),
 'S16': (78.0, 78.0,
         ['M-F2-PICKUP — מפרץ "הורדה ואיסוף" + נוסע אמיתי מטיסה נוחתת דרך הדלת D5 (pier, ‏S7F299)'],
         ['074zp_pier_pickup.js'], None),
 'W16': (89.0, 89.0,
         ['סט 11 של המעצב — 10 פוסטרים במסכי המקום, ב-7 המסגרות של הקולנוע והתיאטרון ובמוזיאון (posters, ‏S7F299)'],
         ['074n3s_posters_set11.js:TC_EVENT_POSTERS'], None),
 'W9': (65.0, 72.0,
         ['האייקון של המשחק (posters, ‏S7F299)', 'המקרא של M בטלפון — בשוליים (mapfix, ‏S7F299)'],
         ['074n3_posters.js (האייקון, blob)', '074zp_mapfix.js'], None),
}
DROP = {'S16': ['M-F2-PICKUP'], 'W16': ['סט 11 של המעצב'], 'W9': ['האייקון של המשחק']}
CHG = []
for i, (pa, pb, done, ev, rem) in AU.items():
    s = NB[i]; old = s['progress'] or 0
    s['progress'] = pa; s['progressWithBranches'] = max(pb, pa)
    if pa > 0 and s['status'] == 'planned': s['status'] = 'active'
    dn = s.setdefault('done', [])
    head = 'המעבר על S7F299 (17.11): %s%% (היה %s%% ב-S7F298)%s' % (r1(pa), r1(old), ('; עם הענפים — %s%%' % r1(pb)) if pb > pa else '')
    if head not in dn: dn.append(head)
    for x in done:
        if x not in dn: dn.append(x)
    s['evidence'] = list(dict.fromkeys(list(s.get('evidence') or []) + list(ev)))
    e2 = 'בקוד של S7F299: ' + ' · '.join(ev)
    if e2 not in dn: dn.append(e2)
    if rem is not None: s['remaining'] = list(rem)
    else: s['remaining'] = [x for x in s.get('remaining', []) if not any(k in x for k in DROP.get(i, []))]
    s['auditKind'] = 'נבדק בקוד של S7F299'
    if abs(old - pa) > 1e-9: CHG.append((i, old, pa))
TOT = round(sum(s['hours'] for s in SS['stages']), 2); OLD_TOT = round(sum(NB[i]['hours'] for i in OLD_IDS), 2)
DONE1 = round(sum(s['hours'] * (s['progress'] or 0) / 100 for s in SS['stages']), 2)
DONEB = round(sum(s['hours'] * (s.get('progressWithBranches', s['progress']) or 0) / 100 for s in SS['stages']), 2)
DONE_OLD = round(sum(NB[i]['hours'] * (NB[i]['progress'] or 0) / 100 for i in OLD_IDS), 2)
LEFT = round(TOT - DONE1, 2); LEFTB = round(TOT - DONEB, 2)
PCT, PCTB, PCT_OLD = DONE1 / TOT * 100, DONEB / TOT * 100, DONE_OLD / OLD_TOT * 100
NEW_H = round(TOT - OLD_TOT, 2)
per_pct = (899.7 - DONE_V699) / (Q1 - Q0)          # the rate of 11.11, the same number as v7.01 (v6.99 → S7F298)
need_e = LEFT / per_pct; need_l = LEFT * 2.5 / per_pct; wk_e, wk_l = need_e / WEEK, need_l / WEEK
BIG = sorted(((NB[i]['hours'] * (1 - NB[i]['progress'] / 100), i) for i in NB), reverse=True)
big = lambda i: '%s ~%d' % (i, round(NB[i]['hours'] * (1 - NB[i]['progress'] / 100)))
HOWLONG = ('כמה נשאר (17.11 %s, אחרי S7F299): נעשו %s שע׳ מתוך %s (%s%%), עם 10 השלבים של v7.01 (S17, ‏S18, ‏W27 – W34 — %s שע׳, הערכה — לאישורך); '
           'בשלבים של v7.00 — %s מתוך %s (%s%%); עם הענפים המוכנים — %s (%s%%). ב-S7F299 (15 ענפים של הבוקר) נוספו %s שע׳ של התוכנית. '
           'נשארו %s שע׳ (עם הענפים — %s). הגדולים: %s, ‏%s, ‏%s, ‏%s. '
           'הקצב — של 11.11 (כ-%s שע׳ של התוכנית לכל 1%% מכסה): צריך עוד %d%% עד %d%% מכסה — %s עד %s שבועות של מכסה (עד 98%% בשבוע — D‑688). '
           'המוקדם — בקצב של 11.11; המאוחר — פי 2.5. הקצב של הבוקר (32 סוכנים מ-05:15) — במסירה הבאה, כשיהיה מספר של המכסה.') % (
    AT[-5:], c1(DONE1), c1(TOT), r1(PCT), r1(NEW_H), c1(DONE_OLD), c1(OLD_TOT), r1(PCT_OLD), c1(DONEB), r1(PCTB), r1(DONE1 - D0),
    r1(LEFT), r1(LEFTB), big(BIG[0][1]), big(BIG[1][1]), big(BIG[2][1]), big(BIG[3][1]),
    r1(per_pct), round(need_e), round(need_l), r1(wk_e), r1(wk_l))
# ---------------- 2 · the decisions: the state now ----------------
NOW2 = {'D‑693': 'בוצע ברובו — לוח המשימות נכנס ב-S7F299 (missions); הפעולות האמיתיות — actions, בגל הבא',
        'D‑694': 'בעבודה — island (הציור והחישוב קודם); שלב S17',
        'D‑695': 'בתוקף — מסך F של המוסך נכנס ב-S7F299; המוסך בעיר — garage ‏0ebac85, בגל הבא; בקר התוכניות (planrev) רץ במקביל',
        'D‑691': 'בעבודה — police (עוד לא מוכן למיזוג ב-06:47); "נרשם כחוב" עדיין ב-074x_citysvc.js'}
for d in N['decisions']:
    if d['id'] in NOW2:
        d['now'] = NOW2[d['id']]; d['status'] = NOW2[d['id']] + ' · ההחלטה של הבעלים — בתוקף'
# ---------------- 3 · "waiting for you" ----------------
ASK = N['ownerPendingV692']
w = 'המיזוג של missions ב-S7F299 — שלוש שורות שבהן שני ענפים שינו דברים שונים (074zn, ‏038a, ‏074ze): איחוד של שני הצדדים'
ASK[:] = [a for a in ASK if a['what'] != w]
ASK.append({'what': w, 'dflt': 'האיחוד (נבדק: כל צד נשאר); החלופה — בלי missions', 'where': 'merge · S7F299', 'sub': False, 'now': 'נכנס ב-S7F299'})
# ---------------- 4 · the blocks, the table, the top line ----------------
def left_of(*ids): return round(sum(NB[i]['hours'] * (1 - (NB[i]['progress'] or 0) / 100) for i in ids if i in NB), 1)
ROWS = []
for r in N['next15']['rows']:
    ids = re.findall(r'\b([SW]\d+[a-z]?(?:\.\d)?)\b', r['step']) if not r['step'].startswith('השאר') else [x.strip() for x in r['step'].split('—', 1)[1].split(',')]
    lh = left_of(*ids); r = dict(r); r['dur'] = '%s שע׳ של התוכנית' % r1(lh); r['when'] = 'כ-%d%% עד %d%% מכסה' % (round(lh / per_pct), round(lh * 2.5 / per_pct)); ROWS.append(r)
assert abs(sum(float(r['dur'].split()[0]) for r in ROWS) - LEFT) < 0.8, (sum(float(r['dur'].split()[0]) for r in ROWS), LEFT)
N['next15'] = {'title': 'הצעדים הבאים — %d' % len(ROWS), 'note': HOWLONG, 'rows': ROWS}
SCH['at'] = AT; SCH['note'] = HOWLONG
wk = lambda h: (r1(h / per_pct / WEEK), r1(h * 2.5 / per_pct / WEEK))
air = wk(left_of('S15', 'S16', 'S18')); isl = wk(left_of('S17'))
MS = N['milestones']
MS[1][2] = MS[1][3] = 'S7F289 – S7F299 (S12 ‏95%, ‏S13 ‏92%, ‏S10 ‏90%)'
MS[3][2], MS[3][3] = 'כ-%s שבועות של מכסה' % air[0], 'עד %s שבועות של מכסה' % air[1]
MS[4][2], MS[4][3] = 'כ-%s שבועות של מכסה' % isl[0], 'עד %s שבועות של מכסה' % isl[1]
MS[5][1], MS[5][2], MS[5][3] = '%g' % TOT, 'כ-%s שבועות של מכסה' % r1(wk_e), 'כ-%s שבועות של מכסה' % r1(wk_l)
rows10 = []
for r in N['next10']['rows']:
    if r.get('sum'): continue
    s = NB[r['n']]; dn = round(s['hours'] * (s['progress'] or 0) / 100, 2); pb = s.get('progressWithBranches', s['progress'])
    r = dict(r); r.update({'done': '%g' % dn, 'left': '%g' % round(s['hours'] - dn, 2), 'state': {'done': 'הושלם', 'active': 'פעיל', 'planned': 'מתוכנן'}[s['status']],
                           'leftWhat': ('עם הענפים: %s%% (%g שע׳)' % (r1(pb), round(s['hours'] * pb / 100, 2))) if pb != s['progress'] else ''})
    if s['id'] in AU: r['check'] = 'נבדק בקוד של S7F299'
    rows10.append(r)
tt = sum(float(r['tot']) for r in rows10); dd = sum(float(r['done']) for r in rows10)
rows10.append({'n': '', 'sum': True, 'step': 'סך הכול (לפי S7F299, עם 10 השלבים של v7.01)', 'check': '', 'tot': '%g' % round(tt, 2), 'done': ('%.2f' % dd).rstrip('0').rstrip('.'), 'left': ('%.2f' % (tt - dd)).rstrip('0').rstrip('.'),
               'leftWhat': 'שווה לשעות שנשארו בתוכנית · בלי החדשים: %s%% (%s / %s) · עם הענפים: נעשו %s, נשארו %s (%s%%)' % (r1(PCT_OLD), r1(DONE_OLD), '%g' % OLD_TOT, r1(DONEB), r1(LEFTB), r1(PCTB)), 'end': '', 'state': ''})
N['next10']['rows'] = rows10
TOP = 'עודכן 17.11 — S7F299 · נעשו כ-%d מתוך %s שע׳ — %s%% (%s / %s), עם 10 השלבים החדשים; בשלבים של v7.00 — %s%% (%s / %s); %s%% עם הענפים' % (
    int(dd + 0.5), '%g' % round(tt, 2), r1(PCT), c1(DONE1), c1(TOT), r1(PCT_OLD), c1(DONE_OLD), c1(OLD_TOT), r1(PCTB))
stx, n_ = re.subn(r'^עודכן 17\.11 — S7F298 · .*? עם הענפים · ', '', N['meta']['statusText'])
assert n_ == 1 and 'נעשו כ-' not in stx, N['meta']['statusText'][:300]
N['meta']['statusText'] = TOP + ' · ' + stx
# ---------------- 5 · the build, the links, the log ----------------
N.pop('buildPageOverride', None)
BB = {b['id']: b for b in N['bands2']}
for r in BB['links']['rows']:
    if r[0].startswith('הבנייה האחרונה'): r[2] = 'המשחק שנמסר — S7F299 (14a90a1cffb9; דף הגרסאות — כשהמתאם מפרסם); הגיבוי של גיטהב'
    if r[0].startswith('מפת הדרכים'): r[2] = 'סבב 9ק מול S7F288 (לא עודכנה ל-S7F299)'
    if r[0] == 'המשחק בגיטהב (הקישור הקבוע)': r[2] = 'מכאן מריצים (16.11); ‏S7F298 — cc660ab; ‏S7F299 — כשהמתאם דוחף'
DONE_ROWS = list(N['doneLog'])
for st_, wh in (('S7F299 — 15 ענפים של סבב 17.11: f9fix, ‏stadium, ‏posters (האייקון + סט 11), ‏seatrees, ‏mapfix, ‏garage (מסך F), ‏portraits, ‏pier, ‏loading, ‏locks, ‏newgame, ‏cutscenes, ‏missions (D‑693), ‏fieldcalc, ‏fieldfix', '17.11 07:01'),
                ('התוכנית v7.02 — S7F299: ההתקדמות של 10 שלבים — המסמכים (docs)', '17.11 ' + AT[-5:])):
    if not any(r['step'] == st_ for r in DONE_ROWS): DONE_ROWS.append({'n': str(len(DONE_ROWS) + 1), 'step': st_, 'when': 'נעשה · ' + wh, 'dur': '—', 'gate': False})
N['doneLog'] = DONE_ROWS
dl = BB['doneLog']; dl['rows'] = [[r['n'], r['step'], r['when'].replace('נעשה · ', '')] for r in DONE_ROWS]; dl['title'] = 'מה נעשה — יומן הבניות והגרסאות (%d שורות)' % len(DONE_ROWS)
R = plan_sync.sync(N, BUILD, '17.11.2026 07:01', what='15 ענפים של 17.11: F9, האצטדיון, האייקון וסט 11, העצים בים, המפות, מסך המוסך, הדיוקנאות, המזח, מסך הטעינה, הנעילות, ההדרכה, הסצנות, המשימות, השדה', v692=True)
N['meta']['runLine'] = re.sub(r' · הדף הקבוע: [^·]*', ' · הדף הקבוע (דף הגרסאות) — מתעדכן כשהמתאם מפרסם את S7F299 ', N['meta']['runLine'])
N['zoneSync']['at'] = AT
A = N['audit']; UPDT = ' · עדכון 17.11 %s (v7.02): S7F299 — 15 ענפים; ההתקדמות של 10 שלבים.' % AT[-5:]
if UPDT not in A['summary']: A['summary'] += UPDT
CH = N['changes']
if not any(c.get('v') == 'v7.02' for c in CH):
    for c in CH: c['order'] = c.get('order', 0) + 1
    CH.insert(0, {'v': 'v7.02', 'order': 0, 'at': AT, 'done': ['S7F299'],
                  'changed': ['ההתקדמות לפי S7F299: %s%% (%s / %s); בשלבים של v7.00 — %s%%' % (r1(PCT), c1(DONE1), c1(TOT), r1(PCT_OLD)),
                              '%d שלבים זזו: ' % len(CHG) + ', '.join('%s %s → %s' % (i, r1(o), r1(n)) for i, o, n in CHG),
                              '"כמה נשאר" — %s שע׳' % r1(LEFT), 'D‑691, ‏D‑693 – D‑695 — המצב עכשיו', '"מחכה לך" — האיחוד של missions'],
                  'found': [], 'fixed': [], 'decided': [], 'tests': ['sync_check.py מול S7F299', 'הבדיקה בדפדפן (headcheck, ‏viewcheck2)'], 'active': []})
N = HEB.walk(N); MP = HEB.walk(MP)
json.dump(N, open(P('data/new.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(MP, open(P('data/masterplan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S, open(P('data/stages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(SCH, open(P('data/schedule_s7_s16.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
OUT = {'meta': {'base': 'S7F299 (int299 930919a)', 'from': 'v7.01 + git diff S7F298 S7F299 -- parts + merge/handback.txt', 'at': AT, 'total': TOT, 'done': DONE1, 'pct': round(PCT, 2),
                'old_total': OLD_TOT, 'old_done': DONE_OLD, 'old_pct': round(PCT_OLD, 2), 'done_with_branches': DONEB, 'pct_with_branches': round(PCTB, 2), 'left': LEFT},
       'moved': [{'id': i, 'from': o, 'to': n} for i, o, n in CHG],
       'stages': [{'id': s['id'], 'hours': s['hours'], 'progress': s['progress'], 'progress_with_branches': s.get('progressWithBranches', s['progress']), 'status': s['status'],
                   'evidence': s.get('evidence', []), 'remaining': s.get('remaining', [])} for s in SS['stages']]}
json.dump(OUT, open(W('deliver/2026-11-17/docs/stages_update_S7F299.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('step101 ok', R['build'], R['sha'], R['size'], '%.2f → %.2f of %.2f (%.1f%%); old %.2f of %.2f (%.1f%%); branches %.2f; left %.2f' % (D0, DONE1, TOT, PCT, DONE_OLD, OLD_TOT, PCT_OLD, DONEB, LEFT), 'waiting', R['waiting'])
print(N['meta']['statusText'][:260]); print(HOWLONG)
for r in ROWS: print(' ', r['n'], r['dur'], '|', r['when'], '|', r['step'][:60])
print('moved:', CHG)
