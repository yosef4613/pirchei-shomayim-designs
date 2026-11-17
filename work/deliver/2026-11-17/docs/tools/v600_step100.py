#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""17.11 · v7.01 — הבעלים 16.11: "התוכנית בכלל לא מעודכנת" (v7.00 נבנתה ב-11.11 19:25 על S7F295).
S7F298 בראש (S7F296 – S7F298 נמסרו); ההתקדמות של השלבים — המעבר של audit2 על S7F295, ומעליו המעבר שלי על ההבדל S7F295 → S7F298
(git diff S7F295 S7F298 — 29 חלקים; קובץ:פונקציה לכל שינוי); ההחלטות D‑685 – D‑698; הבקשות החדשות — 10 שלבים חדשים (S17, ‏S18, ‏W27 – W34)
עם הערכת שעות (לאישורך); "מחכה לך"; "כמה נשאר" — לפי הקצב של 11.11 (8% → 97.8%); הקישורים — גם גיטהב.
Idempotent; the data before: _to_delete/*_before_step100.json.  usage: STEP_AT='17.11.2026 05:45' python3 tools/v600_step100.py"""
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); WORK = os.path.dirname(ROOT)
P = lambda p: os.path.join(ROOT, p); W = lambda p: os.path.join(WORK, p)
sys.path.insert(0, HERE); sys.path.insert(0, W('tools_pack'))
import v600_heb as HEB, plan_sync
for f_ in ('data/new.json', 'data/masterplan.json', 'data/stages.json', 'data/schedule_s7_s16.json'):
    b = P('_to_delete/' + os.path.basename(f_).replace('.json', '_before_step100.json'))
    if not os.path.exists(b): shutil.copy(P(f_), b)
    b2 = W('_to_delete/plan600_' + os.path.basename(f_).replace('.json', '_before_step100.json'))
    if not os.path.exists(b2): shutil.copy(b, b2)
L_ = lambda n: json.load(open(P('_to_delete/' + n + '_before_step100.json'), encoding='utf-8'))
N = L_('new'); MP = L_('masterplan'); S = L_('stages'); SCH = L_('schedule_s7_s16')
AT = os.environ.get('STEP_AT', '17.11.2026 05:45')
Q0, Q1 = 8.0, 97.8          # 11.11: 8% at ~07:00 → 97.8% at the delivery of S7F298 (12.11 03:15; HANDOFF_1111 02:45 — "97.8%")
WEEK = 98.0                 # D‑688: up to 98% in a week
BUILD = W('clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F298.html')
assert N['meta']['title'] == 'תוכנית אב v7.00', N['meta']['title']
N['meta']['title'] = 'תוכנית אב v7.01'; N['meta']['at'] = AT[:10]
r1 = lambda v: ('%.1f' % v).rstrip('0').rstrip('.')
c1 = lambda v: format(round(v, 1), ',.1f')
SS = N['stageSys']; NB = {s['id']: s for s in SS['stages']}
OLD_TOT = round(sum(s['hours'] for s in SS['stages']), 2)
DONE0 = round(sum(s['hours'] * (s['progress'] or 0) / 100 for s in SS['stages']), 2)      # v7.00 (S7F295): 876.6
DONE_V699 = 744.8                                                                          # v6.99 (S7F288) — the start of 11.11
# ---------------- 1 · the pass over S7F295 → S7F298 (git diff S7F295 S7F298 -- parts: 29 parts, +1,555 / −30) ----------------
# id: (progress on S7F298, with the ready branches, what entered, the code, what is left — replaces the list; None = the same list)
AU = {
 'W17': (55.0, 55.0,
         ['22 הדגמים נדלקו — stage2 ברירת המחדל מ-S7F296 (D‑685)', 'SP-01 על במת הסיבוב — עיצוב מחדש מלא, קופה פאסטבק (sp01, ‏S7F297)',
          'ליטוש 4 (HB-01, ‏SD-01, ‏SD-02, ‏PR-01) ו-12 התוספות (PR-05 … MV-04) — 40 דגמים, דלתות ותא מטען בכל דגם (cars14, ‏S7F297, ‏D‑686)',
          'מכונית־העל SP-05 "טריז" — דלתות מספריים, 2 בעיר ואחת באולם (sp05, ‏S7F297)', 'אולם התצוגה D3 — השורה חיה בכל פריים (kit34, ‏S7F296)'],
         ['063a_cars70_prop.js:r70mode0 = stage2', '012b_cars14_models.js · 063b_cars14_prop.js:X14 · 074y3_cars14_city.js:C14C', '012c_sp05_asset.js · 063c_sp05.js:X5 · 074y4_sp05_city.js:SP5C', '032_D3_C4_C3_p416.js (kit34)'],
         ['שלב המידות (D‑389): אורך לכל דגם — מעטפת, חניות, תנועה ושמירות; רוחב הגררים', 'כ-24 סוגים חדשים של D‑392: עירייה ובנייה, משאיות קופסה, מיניבוס, הסעת תלמידים, טנדר משטרה ועוד',
          'הלימוזינה נוסעת בעיר (סוג במעטפת + מסלול)', 'השחקן קונה ונוהג באופנוע / ג׳יפ (D‑340); לעלות על כל כלי — 15 כלים של w17 לא רשומים (הביקורת, חלק 2)',
          'SP-05 ושאר מכוניות העל בקטלוג של הסוכנות (היום 6 דגמים) ומכירה', 'מכונית־על נוספת, שונה מאוד מ-SP-05 (הבקשות 12.11 — w17 בסבב 17.11)']),
 'W16': (88.0, 88.0,
         ['כל 34 המותגים של סטים 6–10, סבב 5 והפוסטרים — 32 מוארים בלילה על 38 שלטים (brands6, ‏S7F297, ‏D‑687)'],
         ['074m6_brands6_data.js', '074n_brands_game.js:tcbrSign / TCBR_BY_PLACE', '074n3_posters.js:TCPO'],
         ['המוסך בעיר — בנייה מחדש (D‑380, מאושר ב-D‑695; garage בסבב 17.11) — מסך F מסתובב ותצוגה מקדימה: W31', 'הזהות על משאית הקופסה ועל השקיות (R25‑N‑13)',
          'סט 12 — זהות ושילוט לכל העיר (463 רשומות, 184 משטחים; לא במשחק — signs בסבב 17.11)', 'סט 11 של המעצב — 10 פוסטרים במסגרות של 074n3 (posters בסבב 17.11)',
          'בסיס האמבולנסים, בית הזיקוק, הכיבוי A4, המגדל — בלי שלט (D‑631)', 'להאזין לפס הקול — הבעלים']),
 'S15': (82.0, 83.0,
         ['הפרופורציות — אוטובוס הרחבה 13.5 × 3.0 מ׳, משאית המדרגות 7.5 מ׳; הנוסעים עולים על הגרם (s15p, ‏S7F297)', 'העבודה ליד המסוע ברצף — העובד למעלה תופס ומכניס, 2.2 שנ׳ (s15bag, ‏S7F297)',
          'הסטופ־בר הישן — 27 נורות, אדום / ירוק לפי האישור של הבקר (blueline, ‏S7F297)', 'המטוסים הקטנים — 12 צבעים, צבע קבוע לכל מזהה (gacolor, ‏S7F297)'],
         ['074k2_S15p_dims.js:S15P_DIM', '074r2_S15p_stairs.js:S15P', '074r2_S15bag_belt.js:S15BAG', '074zb_s15_stopbar.js:S15SB', '074zn_gacolor.js:GACOLOR', 's15pax:53605df (ענף — s15pax_flow נכשל)'],
         ['23 היפוכים של 180° בדרכים', 'משמרת מנהל צוותי הקרקע — R26‑8 (grep "M-G2-RAMP": 0 גם ב-S7F298)', 'AB-R1 / SH-R2 — לעצור בטרמינל', 'חלון ל-AC-AM-01 ב-S15SIM',
          'הלוח הישן עם הטיסות של היום — s15pax (ענף, לא במאסטר)', 'שתי סימולציות שדה רצות (045:aptOpsTick הישנה) — regress', 'הקו הכחול מעל המטוסים — לא נמצא',
          'החישוב מחדש, העמדות והצי — S18']),
 'W10': (57.0, 59.0,
         ['קו 5 — line5c במאסטר, כבוי (?l5on); ‏ISE-0 ו-IL תוקנו (S7F297)', 'המסוף E3 — 3 מקורות הקיפאון תוקנו, 6/6 לילות 0 (e3fix, ‏S7F297)'],
         ['074l5_line5_run.js:L5R (כבוי)', '074l7_ise0_routes.js:L5C7', '074g_linesB_term.js:lbDwell · 074p_linesE.js (16) / (21) — e3fix', 'traffic:e6a1004 (ענף, כבוי)'],
         ['קו 5 דולק — יוצא עם האי החדש (D‑694, ‏S17)', 'האוטובוסים מול המכוניות — "פושים ועוצרים סתם" (buses בסבב 17.11)', 'מנגנוני שחרור התקיעות — מה כפול ומה לא עובד',
          'הפרסומות בצד האוטובוס — פי 4, חצי שקוף (posters בסבב 17.11)', 'התנועה לפי שעה ורובע — traffic e6a1004 (כבוי)', 'לילות הקווים לא נבדקו על S7F297 / S7F298', '49 אוטובוסים לפי חלק ה — לא נבדק']),
 'W11': (60.0, 60.0,
         ['התדלוק של מכוניות העיר — דולק כברירת מחדל (fuel3 ‏S7F296 + fuel4 ‏S7F297): בלי פרסה בכניסה ב-D3, ויתור אחרי 20 שנ׳'],
         ['074w2_fuel2.js:LGF / F4.def=true'],
         ['הדלק לשדה (S15)', 'הזרמים של D6, ‏C1, ‏E4 / E6', 'המנופים והקרונות בנמל (GATE‑82)', 'הנפט מהאונייה בצינור לבית הזיקוק — שרשרת כמות (sealife בסבב 17.11)',
          'הפריקה של מוביל הרכבים ב-D3 — הרוורס מערבה, צפונה, ואז דרומה (carrier בסבב 17.11)', 'משאיות בלילה — 2/5 לא עברו (המקור לא הוכח)']),
 'W9': (63.0, 72.0,
         ['המפות — כל 80 האזורים מוצגים, בלי קווקוו "עתידי"; המקרא של M (S7F298)', 'נקודות המשימות על שלוש המפות — 78 נקודות, נעול / פתוח (minimap, ‏S7F297)'],
         ['028_C2_D2_D3_p332.js:MAP_SHOWN_IDS / drawMapZones', '074zn_map_missions.js:MMIS', 'ui7a:1579c35 (ענף — הקלפים 5 / 7)'],
         ['קלפי הישג ושיא דיג (R26‑2) — ui7a 1579c35, ‏5 / 7 בדיקות', 'האייקון של המשחק — אין (shell.html בלי rel=icon; ‏0 גם ב-S7F298)', 'לחיצה על המיני־מפה פותחת את M',
          'אפליקציות כפולות בטלפון (מצב / כרטיס) — 19 אפליקציות', 'F — 153 כותרות "עסקי תעשייה קלה", 73 מסכים בלי כפתור (הביקורת, חלק 2)', 'R26‑5 — 4 מצבים לכל פריט בחנות — לא נבדק']),
 'W22': (57.0, 57.0,
         ['סיפורי האזורים מתחילים בשעה שלהם — השעה NaN תוקנה + שומר של 5 דקות (zsfix, ‏S7F296)'],
         ['074zt_story_hours.js:ZSFIX_HOURS', '038a_E4E5_s9_live.js:clockH'],
         ['פרק 5 "העיר צריכה אותך" — טיוטה (תלוי בסערה, במסוק הרפואי)', 'פרק 6 "העיר שלי" והסיום "פסטיבל העיר"', 'חדשות העיר — שלב ג',
          'הסצנות של הסיפור — W29', 'הקולות לחברים ולמשימות (D‑692; voiceint בסבב 17.11)']),
 'W25': (83.0, 83.0,
         ['השעה של סיפורי האזורים — zsfix במאסטר (S7F296)'],
         ['074zt_story_hours.js'],
         ['D‑500 — רשימת השטחים בלי ייעוד', 'K‑255 — מה שבמפה ולא במשחק', 'E3-PB 15 → 20 חניות; ‏D4S / D4B', 'העצים בים — B8 / C8 / D8 (seatrees בסבב 17.11) — W34']),
 'S13': (92.0, 92.0,
         ['line5c (S7F297) — קו 5 כבוי; האי ננעל גם בלי קו 5 (ferry2 — לא מוכן)'],
         ['074l7_ise0_routes.js', 'ferry2:4223475 (ענף, לא מוכן)'],
         ['האי מתוכנן מחדש מאפס — S17 (D‑694); הפקקים של האי הנוכחי לא מתוקנים (D‑694)']),
}
CHG = []
for i, (pa, pb, done, ev, rem) in AU.items():
    s = NB[i]; old = s['progress'] or 0
    s['progress'] = pa; s['progressWithBranches'] = pb
    dn = s.setdefault('done', [])
    head = 'המעבר על S7F298 (17.11): %s%% (היה %s%% ב-S7F295)%s' % (r1(pa), r1(old), ('; עם הענפים — %s%%' % r1(pb)) if pb != pa else '')
    if head not in dn: dn.append(head)
    for x in done:
        if x not in dn: dn.append(x)
    s['evidence'] = list(ev)
    e2 = 'בקוד של S7F298: ' + ' · '.join(ev)
    if e2 not in dn: dn.append(e2)
    if rem is not None: s['remaining'] = list(rem)
    s['auditKind'] = 'נבדק בקוד של S7F298'
    if abs(old - pa) > 1e-9: CHG.append((i, old, pa))
for s in SS['stages']:     # the ready branches that entered — "with branches" is now the code
    if s['id'] not in AU and s.get('progressWithBranches', s['progress']) != s['progress'] and s['id'] in ('W8', 'W26', 'W15', 'S16'):
        s['progressWithBranches'] = s['progress']
DONE1 = round(sum(s['hours'] * (s['progress'] or 0) / 100 for s in SS['stages']), 2)
DONEB = round(sum(s['hours'] * (s.get('progressWithBranches', s['progress']) or 0) / 100 for s in SS['stages']), 2)
# ---------------- 2 · the new requests → 10 new stages (the hours — an estimate, for your approval) ----------------
T = lambda **k: k
NEWST = [
 T(id='S17', name='S17 — האי מחדש מאפס: E9–H9, ‏H8 ומרינה על חצי D9 — ‏5.5 אזורים (D‑694)', gate='האי החדש', hours=32.0, zones=['E9', 'F9', 'G9', 'H9', 'H8', 'D9'],
   purpose='תכנון ועיצוב מחדש של האי, יחד עם הכבישים, המסילות, התחנות, המטען, הרציפים והרכבל; הפקקים של האי הנוכחי לא מתוקנים — הם יוצאים עם התכנון החדש.',
   builds='הגשר המתרומם; תחנות אוטובוס לפי חישוב (לפחות 4, בזוגות); הרכבל — 8 קרונות לפחות; רכבת נוסעים של 4–5 קרונות ורכבת משא עם אזור פריקה; המעבורת; אסדת הגז ב-H8; ‏F עם תוכן בכל מקום',
   behavior='נתיבי השיט מזרח ↔ מערב, ואחרי D — לדרום־מערב (בין B ל-C); האוניות לא נעלמות ולא עוברות ביבשה',
   remaining=['הציור והחישוב של התחנות (כלל 13) → בקר התוכניות (כלל 20) — island בסבב 17.11', 'הבנייה', 'קו 5 דולק על האי החדש', 'בדיקת נעילה: גשר, כביש, מסילה ואוניות'],
   acceptance=['רשת שאפשר לנסוע בה בלי נעילה; כל תחנה עם גישה', 'האוניות בנתיבים מזרח / מערב, בלי היעלמות (s13DrawLiftLow)', 'לפי הציור שאושר (D‑605)'], src='D‑694'),
 T(id='S18', name='S18 — השדה: בירור הלוגיסטיקה הישנה, חישוב לניצול מרבי, ומה וכמה צריך (הבעלים 13.11)', gate='השדה המחושב', hours=24.0, zones=['E0', 'F0', 'G0', 'E1', 'F1', 'G1', 'E2', 'F2', 'G2'],
   purpose='קודם חישוב, אחר כך עמדות: הבירור של הישן (S7F272), החישוב של החדש — לפחות פי 2 מהישן — ומזה כמה צריך מכל דבר.',
   builds='מטריצת שירות לכל סוג מטוס; 4–5 עמדות כבודה (היום 1, בישן 3); ניצול כל 19 העמדות + R3; חניות הצי אחרי ההרחבה דרומה; נחיתת האמפיבי במים בדרום',
   behavior='תמהיל מלא (מנהלים, הענקים P1/P6, מטען, GA); בלילה — הרצת מנועים ותחזוקה במחזור; כל טיסה מקבלת בדיוק את מה שהסוג שלה צריך',
   remaining=['הבירור והמטריצה — fieldcalc בסבב 17.11', 'הצבעים 3/4, ‏R3, התמהיל, s15pax, החניונים של S16 — fieldfix בסבב 17.11', 'הציור → הבקר → הבנייה → בדיקת עומס מול החישוב'],
   acceptance=['יותר טיסות מהישן (יעד: 88–92 תנועות בחצי שעה, אם הקיבולת מאפשרת)', 'בדיקה חוסמת לכל שירות שחסר לטיסה', 'אין חפיפות, אין מטוס או נוסע שנעלמים'], src='13.11'),
 T(id='W27', name='המשימות — D‑693, מצב משימה אחד, פעולות אמיתיות, דיוקנאות אנשי הקשר', gate='המשימות', hours=24.0, zones=[],
   purpose='סיפור 1–3 וצד 4–6 בו זמנית; 2–3 משימות משנה בכל סדר; הודעה, כרטיס, סמן וניווט על אותו מצב; פעולות משחק אמיתיות במקום "הגעה + לחיצה".',
   builds='מגבלה אחת להודעות, לסמנים, לכרטיסים ולניווט; הרמה / נשיאה / מסירה / תיקון עם אנימציה ותוצאה נראית (156 / 228 שלבים); צבע וסמל לכרטיסים; תמונה לכל איש קשר — מצוירת בקוד',
   behavior='כשמשימות הצד יורדות מתחת ל-4 — מופיעה חדשה, בשטח הפתוח', remaining=['missions, ‏actions, ‏portraits — בסבב 17.11'],
   acceptance=['הספירה של D‑693 נשמרת כל הזמן', 'כל שלב קורה בעולם ונראה, ורק אז התקדמות'], src='D‑693'),
 T(id='W28', name='משחק חדש — שמירה חדשה, הדרכה, נעילה פיזית וניווט חוקי, המזח ו-M-F2-PICKUP', gate='המסלול הראשון', hours=10.0, zones=[],
   purpose='שמירה חדשה היא מסלול ברור שאפשר להשלים, בלי טלפורט ובלי הצפת טלפון; אזור נעול — נעול באמת, בכל אמצעי התחבורה.',
   builds='g77NmSkip / G77_OT.on — ההדרכה; נעילה פיזית; ניווט רק בשטח הפתוח; המזח, ‏M-F2-PICKUP, ‏F מתוך רכב', behavior='', remaining=['newgame, ‏locks, ‏pier — בסבב 17.11', 'בדיקת מסירה משמירה נקייה'],
   acceptance=['שחקן חדש מסיים פתיחה ומשימה מודרכת ברצף', 'אין דרך לאזור נעול'], src='הביקורת 12.11'),
 T(id='W29', name='סרטון הפתיחה, סצנות הסיפור, מסך הפתיחה ומסך הטעינה — במנוע, בקוד', gate='הסרטונים', hours=22.0, zones=[],
   purpose='דרישת חובה של הבעלים (12.11): סרטון פתיחה במנוע, סצנה לכל פרק, "שהכול יקרה באמת", מסך פתיחה ומסך טעינה מעוצבים — בלי וידאו ובלי תמונות (כלל 17).',
   builds='מצלמה מונפשת, כותרות ומוזיקה; מסך טעינה עם איורים וטיפים מתחלפים שמצוירים בפריים הראשון, בכל טעינה, עם התקדמות אמיתית',
   behavior='אפשר לדלג; רק במשחק חדש, ואפשר לצפות שוב מהתפריט', remaining=['opening, ‏cutscenes, ‏loading — בסבב 17.11 (על 074zc_opening.js:TCO, ‏009b_opening_logo.js, ‏074ze — מנוע הסיפור)'],
   acceptance=['0 קובצי תמונה ו-0 data:image', 'מסך הטעינה מופיע בכל טעינה, לא רק בפתיחה'], src='12.11'),
 T(id='W30', name='אירועים אקראיים בעולם — אש וכבאית, נפילה ואמבולנס, בורח ושוטר עד המעצר', gate='האירועים', hours=8.0, zones=[],
   purpose='אירועים שקורים באמת בשטח הפתוח, לא צפוף (תקרה), עם הודעה קצרה וסמן; אפשר לצפות.',
   builds='על צי החירום של A4 (025: A4_FLEET_CFG / updateA4Fleet), מסוק הכיבוי והמרדף (074x_citysvc), נתיב המיון (A2-ER-LANE)', behavior='הכבאית מכבה; האמבולנס מפנה ל-A2; השוטר מביא לתחנה A5',
   remaining=['events — בסבב 17.11'], acceptance=['כל רכב — של הסימולציה, עם מקור ויעד (כללים 25 ו-32)'], src='12.11'),
 T(id='W31', name='המוסך — מסך F: הרכב גדול ומסתובב, תצוגה מקדימה לפני הקנייה (גם בבית ובסוכנות)', gate='מסך המוסך', hours=6.0, zones=[],
   purpose='כשלוחצים F במוסך — הרכב של השחקן גדול באמצע המסך ומסתובב (כמו במת הסיבוב ב-D3, דרך C34), ואפשר לעצור ולסובב ביד; כל שינוי — לראות לפני הקנייה.',
   builds='צבע, חישוקים, גג, שדרוגים — על הרכב המסתובב; "קנה" מחיל ומחייב, "ביטול" מחזיר', behavior='', remaining=['garage — בסבב 17.11 (המוסך עצמו — W16)'],
   acceptance=['אותו מסך במוסך בעיר, בבית ובסוכנות'], src='13.11 · D‑695'),
 T(id='W32', name='ניסוי התלת־ממד וניסוי ספריות הגרפיקה — בעותקים נפרדים (D‑697)', gate='הניסויים', hours=10.0, zones=[],
   purpose='הערכה כנה של turbo-city-b4, השוואה של מנועים וערכות דגמים, אב־טיפוס אחד; ושלושה ניסויים בספריות (מכונית, מטוס, הולך רגל) — בלי לגעת במשחק הראשי.',
   builds='דוח השוואה, אב־טיפוס, ותוכנית ל-4 אזורים', behavior='', remaining=['threed, ‏gfxlib — בסבב 17.11', 'ההחלטה של הבעלים אם ממשיכים'],
   acceptance=['כל סוג קובץ חדש — דף בדיקה קטן קודם (כלל 17ב)'], src='D‑697 · 15.11'),
 T(id='W33', name='גיטהב — הקישור הקבוע: המשחק והתוכנית בכל מסירה', gate='גיטהב', hours=2.0, zones=[],
   purpose='הבעלים מריץ את המשחק מגיטהב (yosef4613.github.io/pirchei-shomayim-designs/turbo-city/); הפרסום כאן — גיבוי. התוכנית ליד המשחק — turbo-city/plan.html.',
   builds='turbo-city/index.html + version.json + plan.html בכל מסירה, ובדיקה שה-sha1 שווה', behavior='',
   remaining=['plan.html — v7.01 מוכן (docs, ‏17.11); הדחיפה — המתאם', 'בכל מסירה מ-S7F299 — המשחק והתוכנית יחד'],
   acceptance=['אותו sha1 בגיטהב ובבנייה'], src='16.11', prog=50.0,
   done=['S7F298 עלה לגיטהב (cc660ab, ‏16.11) — הקישור נבדק, אותו sha1 (d7aa59d9b47b)']),
 T(id='W34', name='הביקורת של 12.11 — התיקונים באזורים ובמערכות שכבר נבנו (56 ממצאים + חלק 2)', gate='הביקורת', hours=40.0, zones=[],
   purpose='כל מה שהבעלים והבודק מצאו באזורים שסומנו "גמור" — לאמת בקוד ובעין (כלל 19), ולשדרג את הקיים (19א). בלי מה שכבר בשלב אחר (W17, ‏S17, ‏S18, ‏W27 – W31).',
   builds='', behavior='',
   remaining=['F9 — האירועים והאזורים (f9fix)', 'תוצאות האצטדיון לפי שעון המשחק (stadium)', 'העצים בים ב-B8–D8 + בדיקה חוסמת (seatrees)', 'המפות — H0–H3 / G3, היער הצפוני, 4 משימות שדה בלי POI (mapfix)',
              'האוניות, הגוררות, הנפט, ferry2 (sealife)', 'החקלאות — חממות, שדות, תות (farm)', 'קנס רק כשנתפסים + רישיון טיס והטסה (police, ‏D‑691)', 'ביצועים וזיכרון בזומים (perf)',
              'האייקון, סט 12, סט 11 והפרסומות פי 4 (signs, ‏posters)', 'צבעי המטוסים ב-3/4 (fieldfix)', 'הרכבל — 8 קרונות; פנים הבית; השינה בבית; הצגות והפסקה; צפייה במשחק באצטדיון — עוד לא שובצו'],
   acceptance=['כל ממצא — "מצאתי" בקוד, תיקון, ובדיקה בעין'], src='הביקורת 12.11'),
]
for t in NEWST:
    if t['id'] in NB: SS['stages'].remove(NB[t['id']])
    pr = t.get('prog', 0.0)
    st = {'id': t['id'], 'name': t['name'], 'gate': t['gate'], 'hours': t['hours'], 'status': 'active' if pr > 0 else 'planned', 'progress': pr, 'progressWithBranches': pr,
          'purpose': t['purpose'], 'builds': t['builds'], 'behavior': t['behavior'], 'why': 'בקשה חדשה של הבעלים (%s) — נוספה ב-v7.01; השעות — הערכה, לאישורך' % t['src'],
          'done': list(t.get('done', [])), 'remaining': t['remaining'], 'issues': [], 'acceptance': t['acceptance'], 'merged': '', 'next': '', 'zones': [], 'from': [],   # the zones stay in the zone table's stage (ט2: a zone in one stage only); here — only in the text
          'zonesText': t['zones'],
          'history': [], 'evidence': [], 'auditKind': 'שלב חדש — v7.01'}
    SS['stages'].append(st); NB[t['id']] = st
ids_new = [t['id'] for t in NEWST]
for a, b in zip(ids_new, ids_new[1:] + ['W23']): NB[a]['next'] = b
TOT = round(sum(s['hours'] for s in SS['stages']), 2); NEW_H = round(TOT - OLD_TOT, 2)
DONE1 = round(sum(s['hours'] * (s['progress'] or 0) / 100 for s in SS['stages']), 2)
DONEB = round(sum(s['hours'] * (s.get('progressWithBranches', s['progress']) or 0) / 100 for s in SS['stages']), 2)
DONE_OLD = round(sum(s['hours'] * (s['progress'] or 0) / 100 for s in SS['stages'] if s['id'] not in ids_new), 2)
LEFT = round(TOT - DONE1, 2); LEFTB = round(TOT - DONEB, 2)
PCT, PCTB, PCT_OLD = DONE1 / TOT * 100, DONEB / TOT * 100, DONE_OLD / OLD_TOT * 100
# ---------------- 3 · how much is left — the rate of 11.11 (v6.99 744.8 → S7F298; the quota 8% → 97.8%) ----------------
DONE_DAY = round(DONE_OLD - DONE_V699, 2); QD = Q1 - Q0
per_pct = DONE_DAY / QD
need_e = LEFT / per_pct; need_l = LEFT * 2.5 / per_pct
wk_e, wk_l = need_e / WEEK, need_l / WEEK
big = lambda i: '%s ~%d' % (i, round(NB[i]['hours'] * (1 - NB[i]['progress'] / 100)))
BIG = sorted(((NB[i]['hours'] * (1 - NB[i]['progress'] / 100), i) for i in NB), reverse=True)
HOWLONG = ('כמה נשאר (17.11 %s, אחרי S7F298): בשלבים של v7.00 נעשו %s שע׳ מתוך %s (%s%%) — לפי המעבר של audit2 על S7F295 והמעבר על ההבדל S7F295 → S7F298 (29 חלקים). '
           'נוספו 10 שלבים חדשים לבקשות של 12.11–16.11 (S17, ‏S18, ‏W27 – W34): ‏%s שע׳ — הערכה, לאישורך. עם החדשים: נעשו %s מתוך %s (%s%%); עם הענפים המוכנים — %s (%s%%). '
           'נשארו %s שע׳ (עם הענפים — %s). הגדולים: %s, ‏%s, ‏%s, ‏%s. '
           'הקצב של 11.11 (מ-v6.99: %s שע׳ → %s ב-S7F298): %s שע׳ של התוכנית, והמכסה עלתה מ-%s%% ל-%s%% — כ-%s שע׳ של התוכנית לכל 1%% מכסה. '
           'בקצב הזה צריך עוד %d%% עד %d%% מכסה — %s עד %s שבועות של מכסה (עד 98%% בשבוע — D‑688). המכסה של השבוע הזה התחילה ב-17.11 05:15 מ-0%%. '
           'המוקדם — בקצב של 11.11; המאוחר — פי 2.5 (מה שנשאר קשה יותר: W7, ‏W17, האי מאפס, השדה המחושב, הבטא). '
           'מה שנבנה היום (סבב 17.11, ‏32 סוכנים) — ייכנס בעדכון אחרי S7F299.') % (
    AT[-5:], c1(DONE_OLD), c1(OLD_TOT), r1(PCT_OLD), r1(NEW_H), c1(DONE1), c1(TOT), r1(PCT), c1(DONEB), r1(PCTB),
    r1(LEFT), r1(LEFTB), big(BIG[0][1]), big(BIG[1][1]), big(BIG[2][1]), big(BIG[3][1]),
    r1(DONE_V699), r1(DONE_OLD), r1(DONE_DAY), r1(Q0), r1(Q1), r1(per_pct),
    round(need_e), round(need_l), r1(wk_e), r1(wk_l))
# ---------------- 4 · the decisions D‑685 – D‑698 ----------------
D = N['decisions']; NEW = []
txt = open(W('DECISIONS_1110.md'), encoding='utf-8').read()
NOW_ = {'D‑685': 'בוצע — stage2 ברירת המחדל מ-S7F296; ‏SP-01 נבנה מחדש (sp01, ‏S7F297)',
        'D‑686': 'בתוקף — cars14 ו-sp05 נכנסו ב-S7F297 אחרי הבדיקות; כל רכב חדש נכנס כברירת מחדל',
        'D‑687': 'בוצע — brands6: כל 34 המותגים, סבב 5 והפוסטרים (S7F297)',
        'D‑688': 'בתוקף — עד 98% עובדים; ב-98% מסיימים; ב-98.5% עוצרים הכול',
        'D‑689': 'בתוקף — כלל 19 ו-19א: "מצאתי" בראש כל החזרה',
        'D‑690': 'בוצע — S7F297 (int297h, הבדיקה המקוצרת)',
        'D‑691': 'בעבודה — הקנס רק כשנתפסים ורישיון הטיס: police בסבב 17.11 ("נרשם כחוב" עדיין ב-074x_citysvc.js)',
        'D‑692': 'בעבודה — 32 / 45 בקשות הוקלטו (12.11); ההכנסה למשחק — voiceint בסבב 17.11',
        'D‑693': 'בעבודה — missions בסבב 17.11; שלב W27',
        'D‑694': 'בעבודה — island בסבב 17.11 (ציור וחישוב התחנות קודם); שלב S17',
        'D‑695': 'בתוקף — המוסך נבנה (garage, ‏17.11); בקר התוכניות (planrev) רץ במקביל, לא עוצר',
        'D‑696': 'בתוקף — טבלת החלוקה deliver/2026-11-17/model_plan.md (35 סוכנים)',
        'D‑697': 'בתוקף — כלל 17ב; הסוגים של B4 מאושרים; כל סוג אחר — דף בדיקה קודם',
        'D‑698': 'בתוקף — הסבב של 17.11: 32 סוכנים + 3 בגל השני; אופוס, המאמץ לפי הקושי'}
OPEN_ = {'D‑686', 'D‑688', 'D‑689', 'D‑691', 'D‑692', 'D‑693', 'D‑694', 'D‑695', 'D‑696', 'D‑697', 'D‑698'}
for m in re.finditer(r'^## (D‑(6\d\d))(.*?)\n(.*?)(?=^## |\Z)', txt, re.M | re.S):
    if not 685 <= int(m.group(2)) <= 698: continue
    h = m.group(3).strip()
    if h.startswith('('): when, topic = h[1:].split(')', 1)[0], h.split(') — ', 1)[-1]
    else: parts = h.lstrip('— ').split(' — ', 1); when, topic = parts[0], parts[-1]
    NEW.append((m.group(1), when.replace('‏', '').strip(), topic.strip(), re.sub(r'\s+', ' ', m.group(4).replace('**', '')).strip()[:600]))
assert len(NEW) == 14, [x[0] for x in NEW]
for k, when, topic, body in NEW:
    now = NOW_[k]
    D[:] = [x for x in D if x['id'] != k]
    D.append({'id': k, 'topic': topic, 'text': 'הבעלים %s · %s' % (when, body), 'status': now + ' · ההחלטה של הבעלים — בתוקף', 'now': now,
              'stages': {'D‑693': ['W27'], 'D‑694': ['S17'], 'D‑695': ['W16', 'W31'], 'D‑697': ['W32'], 'D‑691': ['W15', 'W18'], 'D‑685': ['W17'], 'D‑686': ['W17'], 'D‑687': ['W16']}.get(k, []),
              'open': k in OPEN_, 'pend': ''})
D.sort(key=lambda d: int(re.sub(r'\D', '', d['id']) or 0))
for d in D:    # D‑683 was replaced by D‑688
    if d['id'] == 'D‑683': d['now'] = 'הוחלף ב-D‑688 (עד 98%)'; d['open'] = False; d['status'] = 'הוחלף ב-D‑688 · ' + d['status']
# ---------------- 5 · "waiting for you" ----------------
ASK = N['ownerPendingV692']
UPD = [('22 הדגמים הפרטיים', 'נכנסו — stage2 ברירת המחדל מ-S7F296 (D‑685)'),
       ('הפוסטרים — סט 11', 'הפוסטרים של 074n3 במאסטר (brands6, ‏S7F297); סט 11 של המעצב (12.11, ‏10 פוסטרים) — posters בסבב 17.11'),
       ('הקולות — Voice3', 'מאושר (D‑692) — 32 / 45 בקשות הוקלטו; ההכנסה — voiceint בסבב 17.11'),
       ('zsfix / fuel3', 'נכנסו ב-S7F296; התדלוק דולק מ-S7F297 (fuel4)'), ('זספיקס / fuel3', 'נכנסו ב-S7F296; התדלוק דולק מ-S7F297 (fuel4)'),
       ('בית לגרר / המוסך', 'המוסך מאושר (D‑695) — garage בסבב 17.11'),
       ('המזוודות בדלתות', 'עדיין — TS על נתיב בלי מזוודה'),
       ('קווים ה — D‑629', 'נבנה — S7F295; ‏E3 תוקן ב-S7F297 (e3fix); ‏D‑629 והירוק — עדיין לאישורך')]
for a in ASK:
    for k, v in UPD:
        if a['what'].startswith(k): a['now'] = v
NEWASK = [
 ('השעות של 10 השלבים החדשים (S17, ‏S18, ‏W27 – W34) — %s שע׳ בסך הכול' % r1(NEW_H), 'כמו בטבלת השלבים (הערכה לפי הגודל של שלבים דומים)', 'v7.01', 'נכנס לסך הכול'),
 ('האי (D‑694): S13 נשאר בחשבון כמו שנבנה (92%), והאי החדש — שלב חדש S17 מ-0%', 'כך', 'S13 · S17', 'island — הציור בסבב 17.11'),
 ('התוכנית בגיטהב — turbo-city/plan.html, אותו דף כמו כאן', 'המתאם דוחף בכל מסירה, עם המשחק', 'W33', 'v7.01 מוכן'),
 ('המוסך: הבנייה נשארת ב-W16, ומסך F המסתובב — שלב W31', 'כך', 'W16 · W31', 'garage בסבב 17.11'),
 ('הביקורת של 12.11 — שלב אחד (W34, ‏40 שע׳) לכל מה שלא שובץ בשלב אחר', 'כך; כל ממצא — לאמת בקוד', 'W34', 'רוב הסעיפים בעבודה בסבב 17.11')]
for w, df, wh, nw in NEWASK:
    ASK[:] = [a for a in ASK if not a['what'].startswith(w[:30])]
    ASK.append({'what': w, 'dflt': df, 'where': wh, 'sub': False, 'now': nw})
# ---------------- 6 · the blocks that are left, in % of the quota ----------------
def left_of(*ids): return round(sum(NB[i]['hours'] * (1 - (NB[i]['progress'] or 0) / 100) for i in ids if i and i in NB), 1)
BL = [('מעבר העיצוב השני — האנשים, המטוסים, הרכבות והאוניות ב-3/4 (W7)', ['W7']),
      ('כלי הרכב (W17) — שלב המידות, כ-24 סוגים חדשים, לעלות על כל כלי, הסוכנות', ['W17']),
      ('הביקורת של 12.11 באזורים שנבנו (W34)', ['W34']),
      ('הבטא, האיזון והגרסה הסופית (W23)', ['W23']),
      ('השדה — S15, ‏S16 והחישוב מחדש (S18)', ['S15', 'S16', 'S18']),
      ('האי מאפס (S17)', ['S17']),
      ('המשימות, המסלול הראשון והסיפור (W27, ‏W28, ‏W22)', ['W27', 'W28', 'W22']),
      ('הסרטונים, מסך הפתיחה ומסך הטעינה (W29)', ['W29']),
      ('הקווים והלוגיסטיקה (W10, ‏W11)', ['W10', 'W11']),
      ('הממשק (W9), השמע (W20), החנויות (W16), שירותי העיר (W15), הקריירות (W18), האירועים (W30), מסך המוסך (W31)', ['W9', 'W20', 'W16', 'W15', 'W18', 'W30', 'W31']),
      ('הניסויים וגיטהב (W32, ‏W33)', ['W32', 'W33'])]
used = {i for _, ids in BL for i in ids}
rest = [i for i in NB if i not in used and NB[i]['progress'] < 100 and NB[i]['hours'] > 0]
BL.append(('השאר — %s' % ', '.join(rest), rest))
ROWS = []
for i, (nm, ids) in enumerate(BL):
    lh = left_of(*ids); pe = lh / per_pct; pl = lh * 2.5 / per_pct
    ROWS.append({'n': str(i + 1), 'step': nm, 'when': 'כ-%d%% עד %d%% מכסה' % (round(pe), round(pl)), 'dur': '%s שע׳ של התוכנית' % r1(lh), 'gate': False})
assert abs(sum(float(r['dur'].split()[0]) for r in ROWS) - LEFT) < 0.6, (sum(float(r['dur'].split()[0]) for r in ROWS), LEFT)
N['next15'] = {'title': 'הצעדים הבאים — %d' % len(ROWS), 'note': HOWLONG, 'rows': ROWS}
SCH['at'] = AT; SCH['pct'] = 0
for r in SCH['rows']:
    if r['id'] in NB and NB[r['id']]['progress'] >= 100: r['done'] = True
SCH['note'] = HOWLONG
wk = lambda h: (r1(h / per_pct / WEEK), r1(h * 2.5 / per_pct / WEEK))
air = wk(left_of('S15', 'S16', 'S18')); isl = wk(left_of('S17'))
N['milestones'] = [['התכנון גמור (W1–W6)', N['milestones'][0][1], '01.11', '01.11'],
                   ['הרובעים בנויים (S1–S13)', N['milestones'][1][1], 'S7F289 – S7F298 (S12 ‏95%, ‏S13 ‏92%, ‏S10 ‏90%)', 'S7F289 – S7F298 (S12 ‏95%, ‏S13 ‏92%, ‏S10 ‏90%)'],
                   ['הים (S14)', N['milestones'][2][1], '10.11 (S7F287)', '10.11 (S7F287)'],
                   ['השדה גמור (S15, ‏S16, ‏S18)', N['milestones'][3][1], 'כ-%s שבועות של מכסה' % air[0], 'עד %s שבועות של מכסה' % air[1]],
                   ['האי החדש (S17, ‏D‑694)', '%g' % NB['S17']['hours'], 'כ-%s שבועות של מכסה' % isl[0], 'עד %s שבועות של מכסה' % isl[1]],
                   ['כל השלבים — הגרסה הסופית', '%g' % TOT, 'כ-%s שבועות של מכסה' % r1(wk_e), 'כ-%s שבועות של מכסה' % r1(wk_l)]]
KIND = {'built': 'כמו בתוכנית — גמור', 'partial': 'נבדק בקוד של S7F295', 'unchecked': 'לא נבדק — כמו בתוכנית'}
rows10 = []
for s in SS['stages']:
    dn = round(s['hours'] * (s['progress'] or 0) / 100, 2); pb = s.get('progressWithBranches', s['progress'])
    ck = s.get('auditKind', '')
    ck = ck if ck in ('נבדק בקוד של S7F298', 'שלב חדש — v7.01') else (KIND.get(ck) or {'בנוי': 'כמו בתוכנית — גמור', 'לא נבדק': 'לא נבדק — כמו בתוכנית'}.get(ck, 'נבדק בקוד של S7F295'))
    if s['progress'] >= 100 and s['id'] not in AU: ck = 'כמו בתוכנית — גמור'
    if s['id'] in ('W1', 'W7', 'W13'): ck = 'לא נבדק — כמו בתוכנית'
    if s['id'] in ('W12', 'W21', 'W23', 'W24'): ck = 'לא התחיל'
    rows10.append({'n': s['id'], 'step': s['name'], 'check': ck, 'tot': '%g' % s['hours'], 'done': '%g' % dn, 'left': '%g' % round(s['hours'] - dn, 2),
                   'leftWhat': ('עם הענפים: %s%% (%g שע׳)' % (r1(pb), round(s['hours'] * pb / 100, 2))) if pb != s['progress'] else '', 'end': '',
                   'state': {'done': 'הושלם', 'active': 'פעיל', 'planned': 'מתוכנן'}[s['status']]})
tt = sum(float(r['tot']) for r in rows10); dd = sum(float(r['done']) for r in rows10)
rows10.append({'n': '', 'sum': True, 'step': 'סך הכול (לפי S7F298, עם 10 השלבים החדשים)', 'check': '', 'tot': '%g' % round(tt, 2), 'done': ('%.2f' % dd).rstrip('0').rstrip('.'), 'left': ('%.2f' % (tt - dd)).rstrip('0').rstrip('.'),
               'leftWhat': 'שווה לשעות שנשארו בתוכנית · בלי החדשים: %s%% (%s / %s) · עם הענפים: נעשו %s, נשארו %s (%s%%)' % (r1(PCT_OLD), r1(DONE_OLD), '%g' % OLD_TOT, r1(DONEB), r1(LEFTB), r1(PCTB)), 'end': '', 'state': ''})
N['next10']['rows'] = rows10
N['next10']['title'] = 'השלבים — %d שלבים: נעשה ונשאר' % len(SS['stages'])
TOP = 'עודכן 17.11 — S7F298 · נעשו כ-%d מתוך %s שע׳ — %s%% (%s / %s), עם 10 השלבים החדשים; בשלבים של v7.00 — %s%% (%s / %s); %s%% עם הענפים' % (
    int(dd + 0.5), '%g' % round(tt, 2), r1(PCT), c1(DONE1), c1(TOT), r1(PCT_OLD), c1(DONE_OLD), c1(OLD_TOT), r1(PCTB))
stx = N['meta']['statusText']
stx, n_ = re.subn(r'^עודכן 11\.11 — S7F295 · .*? עם הענפים \([\d.,]+\) · ', '', stx)
assert n_ == 1 and 'נעשו כ-' not in stx, stx[:300]
N['meta']['statusText'] = TOP + ' · ' + stx
# ---------------- 7 · the build, the links, the log of builds, the changes ----------------
PUB = json.load(open(W('deliver/published.json'), encoding='utf-8'))
pg = [e for e in PUB if e['page'] == 'S7F298']
if pg: N['buildPageOverride'] = {'sha1': pg[-1]['sha1'], 'size': pg[-1]['size'], 'file': pg[-1]['file']}
BB = {b['id']: b for b in N['bands2']}
LK = BB['links']['rows']
for r in LK:
    if r[0].startswith('מפת הדרכים'): r[2] = 'סבב 9ק מול S7F288 (לא עודכנה ל-S7F298)'
    if r[0].startswith('הבנייה האחרונה'): r[2] = 'המשחק שנמסר — S7F298 (דף הגרסאות 8VUftq9eJ3z8Nc3ZB4rPcX v108 — loader + g1.txt / g2.txt); הגיבוי של גיטהב'
ADDL = [['המשחק בגיטהב (הקישור הקבוע)', 'https://yosef4613.github.io/pirchei-shomayim-designs/turbo-city/', 'S7F298 (cc660ab, אותו sha1 d7aa59d9b47b) — מכאן מריצים (16.11)'],
        ['התוכנית בגיטהב', 'https://yosef4613.github.io/pirchei-shomayim-designs/turbo-city/plan.html', 'אותו דף כמו התוכנית כאן — מתעדכן בכל מסירה (מ-v7.01, אחרי הדחיפה של המתאם)'],
        ['ניסוי B4 — תלת־ממד', 'https://yosef4613.github.io/pirchei-shomayim-designs/turbo-city-b4/', 'הניסוי של הבעלים (16.11) — נקודת המוצא של W32'],
        ['כלי הרכב 14 חי', 'https://claude.ai/artifact/HFu2BrdpkUWRLVm1a3e4DA', 'cars14 — ליטוש 4 ו-12 התוספות, במשחק עצמו'],
        ['ציור כלי הרכב 14', 'https://claude.ai/artifact/Rv8QvYEsAutkv9pmCT997z', 'cars14 — היה / צריך'],
        ['SP-05 חי', 'https://claude.ai/artifact/Bcax8hMWLnuhnpq8GrpTkV', 'מכונית־העל SP-05 "טריז"'],
        ['המותגים 6 חי', 'https://claude.ai/artifact/3vEVVgPvkRV8eNbc1UDgKs', 'brands6 — כל 34 המותגים, סבב 5 והפוסטרים'],
        ['המיני־מפה חי', 'https://claude.ai/artifact/2SSF6t3rsKLQRGa1K82rkK', 'הנקודות של המשימות על שלוש המפות'],
        ['המטוסים הקטנים חי', 'https://claude.ai/artifact/6pha3cii8UgioUQqphAqSt', 'gacolor — צבע, פס וזנב לכל מטוס'],
        ['מה היה ואבד', 'https://claude.ai/artifact/HBcCeKQfVwwgHqECKsxBLr', 'regress — S7F284 מול S7F296: אבד 13, כפול 10'],
        ['סט 11 — הפוסטרים', 'https://claude.ai/artifact/Q24FJsWwHSPZ9EvTpmdFoc', 'הסט של המעצב (12.11) — 10 פוסטרים בקוד'],
        ['ציור המוסך', 'https://claude.ai/artifact/5W8ZTDVxKC8Dkg1Cq3hL2N', 'D‑380 — המוסך בעיר מחדש, היה ← צריך (מאושר ב-D‑695)']]
for a in reversed(ADDL):
    LK[:] = [r for r in LK if r[0] != a[0]]
    i = next((k for k, r in enumerate(LK) if r[0].startswith('מפת הדרכים')), len(LK))
    LK.insert(i, a)
DONE_ROWS = list(N['doneLog'])
for st_, wh in (('S7F296 — fix295 (J12_42), ‏zsfix (שעת הסיפורים), ‏fuel3 (התדלוק כבוי), ‏kit34 (אולם התצוגה), ‏22 הדגמים — stage2 ברירת מחדל (D‑685)', '11.11 22:00'),
                ('S7F297 — sp01, ‏cars14 (40 דגמים), ‏fuel4 (התדלוק דולק), ‏line5c (קו 5 כבוי), ‏sp05, ‏gacolor, ‏minimap, ‏brands6 (34 מותגים + סבב 5 + הפוסטרים), ‏blueline (הסטופ־בר), ‏e3fix, ‏s15p, ‏s15bag', '12.11 01:50'),
                ('S7F298 — המפות: כל 80 האזורים מוצגים, בלי קווקוו "עתידי"; המקרא של M', '12.11 03:15'),
                ('גיטהב — S7F298 עלה לקישור הקבוע (cc660ab)', '16.11 11:10'),
                ('התוכנית v7.01 — S7F298, ‏D‑685 – D‑698, ‏10 שלבים חדשים לבקשות 12.11–16.11 — המסמכים (docs)', '17.11 ' + AT[-5:])):
    if not any(r['step'] == st_ for r in DONE_ROWS): DONE_ROWS.append({'n': str(len(DONE_ROWS) + 1), 'step': st_, 'when': 'נעשה · ' + wh, 'dur': '—', 'gate': False})
N['doneLog'] = DONE_ROWS
dl = BB['doneLog']; dl['rows'] = [[r['n'], r['step'], r['when'].replace('נעשה · ', '')] for r in DONE_ROWS]; dl['title'] = 'מה נעשה — יומן הבניות והגרסאות (%d שורות)' % len(DONE_ROWS)
R = plan_sync.sync(N, BUILD, '12.11.2026 03:15', what='S7F297 + המפות (80 אזורים); S7F296 – S7F297: כלי הרכב, המותגים, התדלוק, המסוף E3, השדה, המיני־מפה', v692=True)
N['meta']['runLine'] = N['meta']['runLine'].replace(' · הדף הקבוע: ', ' · הדף הקבוע (דף הגרסאות 8VUftq9eJ3z8Nc3ZB4rPcX v108 — loader + g1.txt / g2.txt, זהים בית-בית לבנייה; ובגיטהב — cc660ab): ', 1)
N['zoneSync']['at'] = AT
A = N['audit']; UPDT = ' · עדכון 17.11 %s (v7.01): S7F296 – S7F298; ‏D‑685 – D‑698; ההתקדמות לפי S7F298; ‏10 שלבים חדשים; כמה נשאר; גיטהב.' % AT[-5:]
if UPDT not in A['summary']: A['summary'] += UPDT
CH = N['changes']
if not any(c.get('v') == 'v7.01' for c in CH):
    for c in CH: c['order'] = c.get('order', 0) + 1
    CH.insert(0, {'v': 'v7.01', 'order': 0, 'at': AT, 'done': ['S7F296 – S7F298', 'גיטהב — cc660ab'],
                  'changed': ['ההתקדמות לפי S7F298 (audit2 על S7F295 + המעבר על ההבדל S7F295 → S7F298): בשלבים של v7.00 — %s%% (%s / %s)' % (r1(PCT_OLD), c1(DONE_OLD), c1(OLD_TOT)),
                              '%d שלבים זזו: ' % len(CHG) + ', '.join('%s %s → %s' % (i, r1(o), r1(n)) for i, o, n in CHG),
                              '10 שלבים חדשים (S17, ‏S18, ‏W27 – W34) — %s שע׳; הסך הכול %s → %s; ‏%s%% עם החדשים' % (r1(NEW_H), c1(OLD_TOT), c1(TOT), r1(PCT)),
                              'D‑685 – D‑698', '"כמה נשאר" — %s שע׳; הקצב של 11.11 (%s שע׳ לכל 1%%)' % (r1(LEFT), r1(per_pct)), '"מחכה לך" — %d נושאים חדשים' % len(NEWASK), 'הקישורים — גיטהב'],
                  'found': [], 'fixed': [], 'decided': ['D‑688 — עד 98% (מחליף את D‑683)', 'D‑694 — האי מאפס', 'D‑695 — המוסך מאושר; בקר התוכניות', 'D‑697 — כלל 17ב'],
                  'tests': ['sync_check.py מול S7F298', 'הבדיקה בדפדפן (headcheck)'], 'active': []})
N = HEB.walk(N); MP = HEB.walk(MP)
json.dump(N, open(P('data/new.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(MP, open(P('data/masterplan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S, open(P('data/stages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(SCH, open(P('data/schedule_s7_s16.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
OUT = {'meta': {'base': 'S7F298 (int298 7c2d0be)', 'from': 'audit2 (S7F295) + git diff S7F295 S7F298 -- parts', 'at': AT, 'old_total': OLD_TOT, 'old_done': DONE_OLD, 'old_pct': round(PCT_OLD, 2),
                'new_hours': NEW_H, 'total': TOT, 'done': DONE1, 'pct': round(PCT, 2), 'done_with_branches': DONEB, 'pct_with_branches': round(PCTB, 2), 'left': LEFT, 'per_pct': round(per_pct, 3)},
       'moved': [{'id': i, 'from': o, 'to': n} for i, o, n in CHG],
       'stages': [{'id': s['id'], 'hours': s['hours'], 'progress': s['progress'], 'progress_with_branches': s.get('progressWithBranches', s['progress']), 'status': s['status'],
                   'evidence': s.get('evidence', []), 'remaining': s.get('remaining', [])} for s in SS['stages']]}
os.makedirs(W('deliver/2026-11-17/docs'), exist_ok=True)
json.dump(OUT, open(W('deliver/2026-11-17/docs/stages_update_S7F298.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('step100 ok', R['build'], R['sha'], R['size'], 'old %.2f → %.2f of %.2f (%.1f%%); with new %.2f of %.2f (%.1f%%), branches %.2f; left %.2f; new hours %.1f' % (DONE0, DONE_OLD, OLD_TOT, PCT_OLD, DONE1, TOT, PCT, DONEB, LEFT, NEW_H),
      'new decisions', len(NEW), 'waiting', R['waiting'])
print(N['meta']['statusText'][:300]); print(HOWLONG)
for r in ROWS: print(' ', r['n'], r['dur'], '|', r['when'], '|', r['step'][:70])
print('moved:', CHG)
