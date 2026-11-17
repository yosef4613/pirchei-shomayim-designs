#!/usr/bin/env python3
# fc_calc.py — fieldcalc 17.11.2026: השדה — מטריצת שירות, חישוב קיבולת (מסלול, הקישור הדרומי B/C, עמדות, אולמות כבודה),
# "כמה צריך" (רכבים, צוותים, נוסעים ומושבים), ובדיקת מרווחים אוטומטית לפריסה המוצעת.
# הקלט: s15_base.json (S15D / S15SIM מהקוד), ‏new_ops.json (מהמשחק, S7F298), ‏old_ops_summary.json (המתכנן הישן, S7F272, 3 זרעים),
#        s15j_L.json (הטרמינל — המושבים), ‏ac_types.json (מידות המטוסים, plan600 part_f_geo).
# הפלט: fc_result.json. קוד יציאה 1 — אם בדיקת המרווחים נכשלת או שהיעד (≥ 2× הישן) לא הושג בתרחיש הנבחר. אין ok=true קבוע: כל בדיקה מחושבת.
import json, math, sys, os, collections as C

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f), encoding='utf-8'))
B = J('s15_base.json'); D = B['S15D']; SIM = B['S15SIM']
NEW = J('new_ops.json'); OLD = J('old_ops_summary.json'); TL = J('s15j_L.json'); ACT = J('ac_types.json')
T = 720                     # המחזור של S15SIM (שניות עולם; ‏0.5 דקת משחק לשנייה — 6 שעות משחק)
PXM = 10                    # 10 פיקס׳ עולם למטר (S15)

# ---------------------------------------------------------------- 1. המטוסים: מידות (part_f_geo), מחלקה, נוסעים, כבודה
DIM = {t[0]: (t[2] * PXM, t[3] * PXM) for t in ACT['types']}          # אורך, מוטה — פיקס׳
HE = ACT['he']
HEAVY = {'AC-LG-01', 'AC-MW-01', 'AC-CG-01', 'AC-HC-01'}               # מערבולת: מי שבא אחריהם מחכה עוד
EXIT_A2 = {'AC-RJ-01', 'AC-TP-01', 'AC-QJ-01', 'AC-BJ-01', 'AC-CN-01', 'AC-LT-01', 'AC-PR-01', 'AC-TB-01'}  # יציאה מהירה ב-A2 (x 7150)
# מושבים × מקדם תפוסה (הנחה — לאישורך; צר-גוף 180 × 0.81 = 146 כמו הטיסה הישנה שהבודק מצא), יחידות כבודה חזותיות לכל כיוון
AC = {
 'AC-PR-01': dict(seats=4,   lf=.6,  bag=0,  hand=True,  cls='GA'),
 'AC-LT-01': dict(seats=6,   lf=.6,  bag=0,  hand=True,  cls='GA'),
 'AC-BJ-01': dict(seats=12,  lf=.6,  bag=2,  hand=True,  cls='EXEC'),
 'AC-CN-01': dict(seats=6,   lf=.6,  bag=1,  hand=True,  cls='EXEC'),
 'AC-AM-01': dict(seats=4,   lf=.6,  bag=0,  hand=True,  cls='AMPH'),
 'AC-TP-01': dict(seats=70,  lf=.8,  bag=6,  hand=True,  cls='REG'),
 'AC-RJ-01': dict(seats=76,  lf=.8,  bag=8,  hand=True,  cls='REG'),
 'AC-QJ-01': dict(seats=100, lf=.8,  bag=8,  hand=True,  cls='REG'),
 'AC-NB-01': dict(seats=180, lf=.81, bag=12, hand=False, cls='NB'),
 'AC-MW-01': dict(seats=300, lf=.8,  bag=24, hand=False, cls='WIDE'),
 'AC-LG-01': dict(seats=400, lf=.8,  bag=32, hand=False, cls='WIDE'),
 'AC-TB-01': dict(seats=0,   lf=0,   bag=0,  hand=False, cls='CARGO', uld=2),
 'AC-CG-01': dict(seats=0,   lf=0,   bag=0,  hand=False, cls='CARGO', uld=8),
 'AC-HC-01': dict(seats=0,   lf=0,   bag=0,  hand=False, cls='CARGO', uld=14),
}
VIS = 5                     # נוסע מצויר אחד לכל 5 (היום בפועל: 12–14 לצר-גוף ≈ 1:11; הנחה — לאישורך)

# ---------------------------------------------------------------- 2. מטריצת השירות: לכל סוג — כל שירות, הרכב, כמה רכבים, משך ליד המטוס (שנ׳ עולם)
# המקור למשכים: S15SIM (מהמשחק, new_ops.json — הרגליים f8) והמתכנן הישן (svcQ בהרצה של S7F272) — ראו 'src'.
SVC_HE = {'push': 'גרירה לאחור', 'marshal': 'מכוון / עקוב אחריי', 'chocks': 'סדי גלגלים וקונוסים', 'gpu': 'כוח קרקע', 'bridge': 'שרוול',
          'stairs': 'מדרגות', 'bus': 'אוטובוס רחבה', 'bags': 'רכבת כבודה', 'belt': 'מסוע', 'uld': 'מכולות (מעמיס + עגלות)', 'fuel': 'דלק',
          'cater': 'קייטרינג', 'water': 'מים', 'lav': 'שירותים', 'clean': 'ניקיון', 'pax_walk': 'הליכה ברגל / רכב לטרקלין', 'dock': 'עגינה וקשירה',
          'arff': 'כבאות בהמתנה (תדלוק עם נוסעים)'}
VEH = {'push': 'PT', 'gpu': 'GP', 'stairs': 'MS', 'bus': 'AB', 'bags': 'BT', 'belt': 'BL', 'uld': 'HL', 'fuel': 'FT', 'cater': 'CT', 'water': 'WT',
       'lav': 'LV', 'clean': 'SVC', 'marshal': 'SV', 'uld2': 'TG'}
VEH_HE = {'PT': 'גרר מטוסים', 'GP': 'מחולל קרקע', 'MS': 'מדרגות נעות', 'AB': 'אוטובוס רחבה', 'BT': 'טרקטור כבודה + עגלות', 'BL': 'מסוע',
          'HL': 'מעמיס מכולות', 'TG': 'גרר עגלות מכולות', 'FT': 'מכלית דלק', 'FTs': 'מתדלק קטן (GA / מסוקים / אמפיבי)', 'CT': 'משאית קייטרינג',
          'WT': 'מכלית מים', 'LV': 'רכב שירותים', 'SVC': 'רכב ניקיון', 'SV': 'רכב "עקוב אחריי"', 'SH': 'הסעת צוות'}
def svc_matrix():
    M = {}
    for m, a in AC.items():
        c = a['cls']; S = {}
        S['marshal'] = dict(d=30, n=1, veh=None, note='מכוון ברגל בכל עמדה; "עקוב אחריי" למרוחקות ול-GA')
        S['chocks'] = dict(d=10, n=0, veh=None, note='העובד של הרחבה')
        if c in ('GA', 'EXEC'):
            S['push'] = dict(d=40, n=1, veh='PT', note='גרר קטן (PT-GA); BJ / CN — גרר')
            S['fuel'] = dict(d=40, n=1, veh='FTs', note='FT-GA — 40 ש׳ (S15SIM)')
            if c == 'EXEC':
                S['gpu'] = dict(d=180, n=1, veh='GP', note='מנהלים — מזגן בעמידה (הישן: BJ / CN עם קייטרינג ושירותים)')
                S['cater'] = dict(d=60, n=1, veh='CT', note='הישן: BJ 7 / CN 5 ביקורים בחצי שעה (svcQ)')
                S['lav'] = dict(d=30, n=1, veh='LV', note='הישן: BJ / CN — שירותים')
                S['clean'] = dict(d=60, n=1, veh='SVC', note='רכב ניקיון קטן')
                S['water'] = dict(d=30, n=1, veh='WT', note='מנהלים — מים (הבקר 17.11)')
            S['pax_walk'] = dict(d=60, n=0, veh=None, note='הנוסעים ברגל אל הטרקלין של ה-GA; מנהלים — לימוזינה עד המטוס: רכב של העיר דרך השער G-STAFF, ‏XC_E / ‏XC_W (fc_calc2.py)')
        elif c == 'AMPH':
            S['dock'] = dict(d=20, n=0, veh=None, note='קשירה למזח הצף — עובד המזח')
            S['fuel'] = dict(d=40, n=1, veh='FTs', note='משאבה במזח / מתדלק קטן')
            S['pax_walk'] = dict(d=60, n=0, veh=None, note='על המזח אל החוף')
        elif c in ('REG', 'NB', 'WIDE'):
            heavy = c == 'WIDE'
            S['push'] = dict(d=75, n=1, veh='PT', note='PT: 7 ש׳ חיבור + 75 ש׳ דחיפה (S15SIM PT-P2 / P3)')
            S['bridge'] = dict(d=20, n=0, veh=None, note='בעמדות P (שרוול; LG — 2 שרוולים בתכנון); בעמדה מרוחקת — מדרגות + אוטובוס')
            S['gpu'] = dict(d=300, n=1, veh='GP', note='מרוחקות (R) ובלי שרוול; בשרוול — כוח מהשרוול (בלי רכב)', remote_only=True)
            S['stairs'] = dict(d=200, n=2 if c != 'REG' else 1, veh='MS', note='מרוחקות: 2 מדרגות לצר / רחב (קדמי + אחורי); TP / RJ — מדרגות מובנות', remote_only=True,
                               skip=m in ('AC-TP-01',))
            S['bus'] = dict(d=165, n=2 if heavy else 1, veh='AB', note='מרוחקות: אוטובוס לכל 60 מצוירים (AB-R1 ‏167 ש׳)', remote_only=True)
            if a['hand']:
                S['bags'] = dict(d=120, n=1, veh='BT', note='טעינה ביד (S6A_HAND: RJ / QJ / TP) — רכבת אחת, 2 עגלות')
            else:
                S['bags'] = dict(d=230 if not heavy else 260, n=1 if not heavy else 2, veh='BT', note='רכבת 2 עגלות ליד המטוס 208–230 ש׳ (S15SIM BT-P2 / P3 / P4)')
                S['belt'] = dict(d=250 if not heavy else 280, n=1 if not heavy else 2, veh='BL', note='מסוע 228–285 ש׳ (BL-P2 / P3); רחב — קדמי + אחורי')
            S['fuel'] = dict(d=70 if not heavy else 140, n=1, veh='FT', note='FT-1 ליד P4 — 70 ש׳; רחב — כפול')
            S['cater'] = dict(d=130 if not heavy else 260, n=1 if not heavy else 2, veh='CT', note='CT-P3 ‏132 / CT-P1 ‏264 ש׳; הישן 130')
            S['water'] = dict(d=30, n=1, veh='WT', note='WT-P4 ‏30 ש׳ (הישן 30)', skip=m == 'AC-TP-01')
            S['lav'] = dict(d=30, n=1, veh='LV', note='LV-P5 ‏30 ש׳ (הישן 30)')
            S['clean'] = dict(d=84 if not heavy else 120, n=1, veh='SVC', note='SVC-P2 / P3 ‏84 ש׳ (הישן 57–110)')
        elif c == 'CARGO':
            S['push'] = dict(d=75, n=1, veh='PT', note='PT-C (S15SIM)')
            S['gpu'] = dict(d=300, n=1, veh='GP', note='הישן: CG / TB — GPU (GC)')
            S['fuel'] = dict(d=70 if m == 'AC-TB-01' else 140, n=1, veh='FT', note='FT-3 — "משא"')
            S['uld'] = dict(d=90 if m == 'AC-TB-01' else 300, n=1 if m != 'AC-HC-01' else 2, veh='HL', note='HL-C1 ‏90 ש׳ (S15SIM); הישן CG ‏690 ש׳ — מקוצר ל-300 עם 2 גררי עגלות')
            S['uld2'] = dict(d=45, n=1 if m == 'AC-TB-01' else 2, veh='TG', note='TG-C ‏40–50 ש׳ × 2 לכל ביקור (S15SIM)')
        S = {k: v for k, v in S.items() if not v.get('skip')}
        M[m] = S
    return M
MATRIX = svc_matrix()

# ---------------------------------------------------------------- 3. המסלול: הקינמטיקה של S15SIM (מדודה במשחק, new_ops.json)
F0 = NEW['flights'][0]
K = dict(roll=round(F0['liftoff'] - F0['rollStart'], 2),       # 6.85 — ריצת ההמראה
         climb=round(F0['climbEnd'] - F0['liftoff'], 2),        # 5.7  — הטיפוס עד שיוצאים מהעולם
         lineup=round(F0['rollStart'] - F0['rwyOcc'][0], 2),    # 8.25 — מקו ההמתנה אל הקו האמצעי
         app=round(F0['touch'] - F0['appStart'], 2),            # 10.8 — הגישה מקצה העולם
         roll_out=round(F0['rollEnd'] - F0['touch'], 2))        # 10   — הגלגול עד A3
ROT = {'A3': round(.5 + K['roll_out'] + 5.0, 1), 'A2': round(.5 + 2 * 1750 / (700 + 60) + 5.0, 1)}   # מהסף עד שהזנב עבר את קו ההמתנה ביציאה
SEP = dict(AA=2, AD=2, DA=3, DD=4, wake=8)                                                           # מרווחים (שנ׳); מערבולת אחרי כבד: +8
def rot(m): return ROT['A2'] if m in EXIT_A2 else ROT['A3']

# ---------------------------------------------------------------- 4. העמדות והדרכים (S15D) + ההצעה
ST = D['stands']
TAXI_V = 55.0               # פיקס׳ / שנ׳ — ההסעה (S15SIM: TAXI 60, הפניות לאט יותר)
PUSH_V = 16.0
A1X, A2X, A3X, TBX, TACY, TCCY = 5250, 7150, 9190, D['tbcx'], D['tacy'], D['tccy']
SOUTH = {k for k in ST if k.startswith('GA') or k.startswith('R')}
def nose_xy(s): return ST[s]['cx'], ST[s]['nose']
TB_T = (TCCY - TACY) / TAXI_V + 4          # ‏B: מ-A (y −170) עד C (y 1850) — 2020 פיקס׳ + פנייה (הערכה)
# כויל לפי המדידה במשחק (try6641, ‏__TC_FC.link): ‏FL-R2 / FL-GA6 על B — צפונה 48 ש׳, דרומה 60 ש׳ (עם ההאטה והפניות)
TB_T_N0, TB_T_S0 = 48.0, 60.0
# בתוכנית: הסעה ב-B בקטע הישר — 90 פיקס׳/ש׳ (≈ 9 מ׳/ש׳, 17 קשר — כמו בשדה אמיתי; היום 60): הפניות וההאטה נשארות כמו שנמדדו (לאישורך)
PLAN_TAXI_B = 90.0
TB_T_N = TB_T_N0 - ((TCCY - TACY) / 60.0 - (TCCY - TACY) / PLAN_TAXI_B)
TB_T_S = TB_T_S0 - ((TCCY - TACY) / 60.0 - (TCCY - TACY) / PLAN_TAXI_B)
def tc_t(cx): return (TBX - cx) / TAXI_V + 4
def taxi_in(s, m):          # מהיציאה מהמסלול ועד העצירה; לדרום — החלונות על B ועל C (יחסית לפינוי)
    cx, ny = nose_xy(s); ex = A2X if m in EXIT_A2 else A3X
    if s in SOUTH:
        a = abs(TBX - A3X) / TAXI_V                 # לדרום — תמיד A3 (ליד B)
        b0, b1 = a, a + TB_T_S; c1 = b1 + tc_t(cx)
        rest = (ny - TCCY) / 30 + 6
        return c1 + rest, dict(B=(b0, b1), C=(b1, c1), x=cx)
    return abs(ex - cx) / TAXI_V + (ny - TACY) / 40 + 10, None
def taxi_out(s, m):         # מהדחיפה ועד קו ההמתנה של A1; לדרום — החלונות על C ועל B (יחסית לדחיפה)
    cx, ny = nose_xy(s); L = DIM[m][0]
    push = (L + 120) / PUSH_V + 14
    if s in SOUTH:
        c0 = push; c1 = c0 + tc_t(cx); b1 = c1 + TB_T_N
        a = (TBX - A1X) / 60 + 8
        return b1 + a, dict(C=(c0, c1), B=(c1, b1), x=cx)
    return push + abs(cx - A1X) / 60 + 12, None

# ההצעה: הסבב של 720 ש׳ — כל השורות (עמדה, דגם, כמה פעמים במחזור, השהיה מינימלית בעמדה). ברירת מחדל — לאישורך; התמהיל המדויק — fieldfix.
DWELL = {'AC-LG-01': 470, 'AC-MW-01': 450, 'AC-NB-01': 400, 'AC-QJ-01': 360, 'AC-RJ-01': 340, 'AC-TP-01': 300, 'AC-CG-01': 440, 'AC-HC-01': 520,
         'AC-TB-01': 300, 'AC-BJ-01': 260, 'AC-CN-01': 240, 'AC-LT-01': 180, 'AC-PR-01': 170}
# מקור: הישן — צר 419–562 (חציון 480), רחב MW ‏659–711, ‏CG ‏870–1030 (עם תורים לרכבים), GA ‏380–574; החדש — צר 398–420 בשרוול.
# הקיצור אצל הרחבים והמטען — רק עם רכבים כפולים (מסוע ×2, רכבת ×2, קייטרינג ×2, ‏HL + 2 ‏TG) — זה חלק מ"כמה צריך".
PLAN = [  # (עמדה, דגם, חברה, פעמים במחזור)
 ('P1', 'AC-LG-01', 'Aurelia Air', 1), ('P2', 'AC-NB-01', 'Sunbeak', 1), ('P3', 'AC-NB-01', 'Tidewind Air', 1), ('P4', 'AC-RJ-01', 'Skyline Regional', 1),
 ('P5', 'AC-NB-01', 'Zebrano', 1), ('P6', 'AC-LG-01', 'Mirage Jet', 1), ('C1', 'AC-CG-01', 'Crateway Cargo', 1), ('C2', 'AC-TB-01', 'Turbo Cargo', 1),
 ('R1', 'AC-RJ-01', 'Confetti Air', 1), ('R2', 'AC-NB-01', 'Coral Coast', 1), ('R3', 'AC-CN-01', 'Executive', 1),
 ('GA1', 'AC-BJ-01', 'Executive', 1), ('GA2', 'AC-LT-01', 'GA', 1), ('GA3', 'AC-PR-01', 'GA', 1), ('GA4', 'AC-LT-01', 'GA', 1),
 ('GA5', 'AC-PR-01', 'GA', 1), ('GA6', 'AC-LT-01', 'GA', 1), ('GA7', 'AC-PR-01', 'GA', 1),
]
# GA2–GA7: האף ב-y 2028 (הכביש AIR-TAIL_ROAD / GA_SPUR חוצה את העמדה — S15 D‑650) → נכנסים רק דו-מנועי קל ומטוס קל; מטוס המנהלים — GA1 (וגם R3 ביום)
PLAN_R3_EXEC = ('R3', 'AC-CN-01', 'Executive', 1)
EXTRA = [('GA2', 'AC-LT-01', 'GA', 1), ('GA3', 'AC-PR-01', 'GA', 1), ('GA4', 'AC-LT-01', 'GA', 1), ('GA5', 'AC-PR-01', 'GA', 1)]   # סבב שני בעמדות הקלות — רק אם הקישור מאפשר

# ---------------------------------------------------------------- 5. המתזמן המחזורי (720 ש׳): מסלול, קישור דרומי, עמדה
def cyc(t): return t % T
def overlap(a0, a1, b0, b1, pad=0):
    for k in (-T, 0, T):
        if a0 < b1 + k + pad and b0 + k < a1 + pad: return True
    return False
def rwy_ok(ev, E):
    # ev: ('A', a_thr, a_vac, model) או ('D', r_roll, r_lift, model)
    for e in E:
        for k in (-T, 0, T):
            x0, x1 = e[1] + k, e[2] + k
            hv = e[3] in HEAVY; nh = ev[3] in HEAVY
            if ev[0] == 'A' and e[0] == 'A':
                w1 = SEP['AA'] + (SEP['wake'] if hv and not nh else 0); w2 = SEP['AA'] + (SEP['wake'] if nh and not hv else 0)
                if not (ev[1] >= x1 + w1 or x0 >= ev[2] + w2): return False
            elif ev[0] == 'A' and e[0] == 'D':
                if not (ev[1] >= x1 + SEP['DA'] or x0 >= ev[2] + SEP['AD']): return False
            elif ev[0] == 'D' and e[0] == 'A':
                if not (ev[1] >= x1 + SEP['AD'] or x0 >= ev[2] + SEP['DA']): return False
            else:
                w1 = SEP['DD'] + (SEP['wake'] if hv and not nh else 0); w2 = SEP['DD'] + (SEP['wake'] if nh and not hv else 0)
                if not (ev[1] >= x1 + w1 or x0 >= ev[2] + w2): return False
    return True
def link_ok(w, L, b2=False):
    # w: dict(dir 'S'|'N', B=(t0,t1), C=(t0,t1), x=cx, m=model) — B: כיוונים מנוגדים לא נחפפים (+3); ‏C: מנוגדים לא נחפפים כשהקטעים [x, 9400] נחתכים;
    # אותו כיוון — 10 ש׳ בין הכניסות ובין היציאות, ובלי עקיפה. ‏b2: מסלול הסעה מקביל לקלים (LT / PR) לאורך הגדר המזרחית — הקלים לא נחסמים ב-B.
    lt = ('AC-LT-01', 'AC-PR-01')
    for q in L:
        for seg in ('B', 'C'):
            a0, a1 = w[seg]; b0, b1 = q[seg]
            if seg == 'C' and w['dir'] != q['dir']:
                xs = max(w['x'], q['x']); sub = (TBX - xs) / TAXI_V + 4          # רק הקטע המשותף [xs, 9400] — ליד הפינה של B
                def part(z, t0, t1): return (t0, min(t1, t0 + sub)) if z['dir'] == 'S' else (max(t0, t1 - sub), t1)
                a0, a1 = part(w, a0, a1); b0, b1 = part(q, b0, b1)
            if w['dir'] != q['dir']:
                if seg == 'B' and b2 and (w['m'] in lt or q['m'] in lt) and not (w['m'] in HEAVY or q['m'] in HEAVY): continue
                if overlap(a0, a1, b0, b1, 3): return False
            else:
                for k in (-T, 0, T):
                    if abs(a0 - (b0 + k)) < 10 or abs(a1 - (b1 + k)) < 10: return False
                    if (a0 - (b0 + k)) * (a1 - (b1 + k)) < 0: return False     # עקיפה
    return True
def lw_at(dirn, t, li, m):
    return dict(dir=dirn, B=(t + li['B'][0], t + li['B'][1]), C=(t + li['C'][0], t + li['C'][1]), x=li['x'], m=m)
def schedule(plan, b2=False, step=2, wait_max=60):
    E, L, SO, out, miss = [], [], C.defaultdict(list), [], []
    rows = []
    for s, m, al, n in plan:
        for i in range(n): rows.append((s, m, al, i, n))
    # הסדר: הדרום (הקישור) קודם — הוא המשאב הצר; אחר כך הגדולים; אחר כך השאר
    rows.sort(key=lambda r: (0 if r[0] in SOUTH else 1, -DIM[r[1]][0]))
    for k, (s, m, al, i, n) in enumerate(rows):
        dw = DWELL[m]; ti, li = taxi_in(s, m); to_, lo = taxi_out(s, m); R = rot(m)
        best = None
        for base in range(0, T, step):
            tp = cyc(base + k * 37)
            # היציאה: הדחיפה ב-tp, ההמראה ב-r (המתנה בקו עד wait_max)
            r_min = tp + to_
            for wait in range(0, wait_max + 1, 2):
                r = r_min + wait
                dev = ('D', r, r + K['roll'], m)
                if not rwy_ok(dev, E): continue
                lw = lw_at('N', tp, lo, m) if lo else None
                if lw and not link_ok(lw, L, b2): continue
                # הנחיתה: הנגיעה אחרי ההמראה; העמידה (מהעצירה עד הדחיפה הבאה) ≥ dwell
                ok_a = None
                for gap in range(20, T, 4):
                    a = r + K['roll'] + gap
                    ob = a + R + ti
                    if tp + T - ob < dw: break                       # העמידה: מהעצירה ועד הדחיפה של אותו מטוס במחזור הבא
                    if n > 1 and tp + T - ob > T / n - 40: continue  # שני מטוסים בעמדה: כל אחד עומד עד חצי מחזור
                    aev = ('A', a, a + R, m)
                    if not rwy_ok(aev, E + [dev]): continue
                    law = lw_at('S', a + R, li, m) if li else None
                    if law and not link_ok(law, L + ([lw] if lw else []), b2): continue
                    if SO[s]:   # שני מטוסים באותה עמדה — העמידות לא נחפפות (30 ש׳ פינוי)
                        win = (ob, tp + T)
                        if any(overlap(win[0], win[1] + 30, p[0], p[1] + 30) for p in SO[s]): continue
                    ok_a = (a, ob, aev, law); break
                if not ok_a: continue
                a, ob, aev, law = ok_a
                stay_w = (ob, tp + T)
                best = dict(stand=s, model=m, airline=al, i=i, push=round(cyc(tp), 1), roll=round(cyc(r), 1), lift=round(cyc(r + K['roll']), 1),
                            hold_wait=wait, thr=round(cyc(a), 1), vac=round(cyc(a + R), 1), onblock=round(cyc(ob), 1),
                            dwell=round(stay_w[1] - stay_w[0], 1), taxi_in=round(ti, 1), taxi_out=round(to_, 1),
                            link_out=dict(B=[round(cyc(x), 1) for x in lw['B']], C=[round(cyc(x), 1) for x in lw['C']]) if lw else None,
                            link_in=dict(B=[round(cyc(x), 1) for x in law['B']], C=[round(cyc(x), 1) for x in law['C']]) if law else None)
                E += [dev, aev]
                if lw: L.append(lw)
                if law: L.append(law)
                SO[s].append(stay_w)
                break
            if best: break
        if best: out.append(best)
        else: miss.append((s, m, i))
    return out, miss, E, L

def rwy_stats(E):
    occ = 0
    for e in E:
        occ += (e[2] - e[1]) + (K['lineup'] if e[0] == 'D' else 0)
    ev = sorted(cyc(e[1]) for e in E); gaps = [(ev[(i + 1) % len(ev)] - ev[i]) % T for i in range(len(ev))] if ev else []
    return dict(moves=len(E), per1800=round(len(E) * 1800 / T, 1), occ=round(occ), util=round(occ / T * 100, 1),
                gap_min=round(min(gaps), 1) if gaps else None, gap_max=round(max(gaps), 1) if gaps else None)
def link_stats(L):
    busy = 0; segs = sorted([(cyc(q['B'][0]), cyc(q['B'][0]) + (q['B'][1] - q['B'][0])) for q in L])
    # איחוד חלונות (אותו כיוון נחפף מותר)
    merged = []
    for a, b in segs:
        if merged and a <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], b)
        else: merged.append([a, b])
    busy = sum(b - a for a, b in merged)
    return dict(traversals=len(L), busy=round(busy), util=round(busy / T * 100, 1))

# התיאורטי: רצף מתחלף נחיתה-המראה, בלי כבדים
def rwy_theory(m_a='AC-NB-01'):
    pair = rot(m_a) + SEP['AD'] + K['roll'] + SEP['DA']
    return dict(pair_s=round(pair, 1), moves_per720=round(2 * T / pair, 1), moves_per1800=round(2 * 1800 / pair, 1))

# ---------------------------------------------------------------- 6. השירותים בפועל לפי הלוח → כמה רכבים צריך (שיא בו זמנית)
POCKET_OF = {}
for k, sp in D['spots'].items():
    POCKET_OF.setdefault(sp['t'], []).append(sp)
def rect_c(r): return ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
FUEL_FARM = rect_c([7958, 1308, 8138, 1503])
VEH_V = 40.0
def travel(s, vt):
    cx, ny = nose_xy(s)
    if vt in ('FT',): bx, by = FUEL_FARM
    elif s in SOUTH: bx, by = (8900, 2480)
    elif s in ('C1', 'C2', 'CH'): bx, by = (5300, 600)
    else: bx, by = (cx, 730)
    return (abs(cx - bx) + abs(ny - by)) / VEH_V + 10
def svc_windows(fl):
    """לכל טיסה: חלונות של כל רכב (כולל הנסיעה מהבסיס ואליו), יחסית ל-onblock ול-push של הסבב."""
    s, m = fl['stand'], fl['model']; S = MATRIX[m]; ob = fl['onblock']; tp = fl['push'] if fl['push'] > ob else fl['push'] + T
    if tp - ob < 60: tp += T
    remote = s.startswith('R') or s.startswith('C')
    W = []
    def add(key, t0, d, n=None):
        v = S.get(key)
        if not v or not v.get('veh'): return
        if v.get('remote_only') and not remote: return
        vt = v['veh']; tr = travel(s, vt)
        for j in range(n if n is not None else v['n']): W.append((vt, t0 - tr, t0 + d + tr, key))
    add('marshal', ob - 40, 40) if s in SOUTH else None
    add('gpu', ob + 15, max(60, tp - ob - 40), None)
    add('stairs', ob + 10, max(60, tp - ob - 30))
    add('bus', ob + 20, S['bus']['d']) if 'bus' in S else None
    add('bus', tp - 30 - S['bus']['d'], S['bus']['d']) if 'bus' in S else None
    if 'bags' in S:
        bd = S['bags']['d']; half = bd / 2
        add('bags', ob + 25, half); add('bags', tp - 30 - half, half)
    if 'belt' in S: add('belt', ob + 20, S['belt']['d'] * .5); add('belt', tp - 25 - S['belt']['d'] * .5, S['belt']['d'] * .5)
    if 'uld' in S: add('uld', ob + 30, S['uld']['d'])
    if 'uld2' in S: add('uld2', ob + 30, S['uld2']['d'], S['uld2']['n']); add('uld2', ob + 30 + S['uld']['d'] - S['uld2']['d'], S['uld2']['d'], S['uld2']['n'])
    if 'fuel' in S: add('fuel', ob + 60, S['fuel']['d'])
    if 'cater' in S: add('cater', ob + 70, S['cater']['d'])
    if 'water' in S: add('water', ob + 60, S['water']['d'])
    if 'lav' in S: add('lav', ob + 100, S['lav']['d'])
    if 'clean' in S: add('clean', ob + 40, S['clean']['d'])
    if 'push' in S: add('push', tp - 10, S['push']['d'])
    return W
def peak(W):
    pts = []
    for (_, a, b, _k) in W:
        a, b = a % T, (a % T) + (b - a)
        pts += [(a, 1), (b, -1), (a + T, 1), (b + T, -1)]
    pts.sort(); c = m = 0
    for _, d in pts:
        c += d; m = max(m, c)
    return m
def svc_jobs(fl):
    """כל שירות כעבודה עם חלון: שחרור (המוקדם ביותר), יעד (המאוחר ביותר לסיום) ומשך (כולל הנסיעה הלוך וחזור מהבסיס)."""
    s, m = fl['stand'], fl['model']; S = MATRIX[m]; ob = fl['onblock']; tp = fl['push'] if fl['push'] > ob else fl['push'] + T
    if tp - ob < 60: tp += T
    remote = s.startswith('R') or s.startswith('C'); Jb = []
    def job(key, r, d, p, n=None):
        v = S.get(key)
        if not v or not v.get('veh'): return
        if v.get('remote_only') and not remote: return
        tr = travel(s, v['veh'])
        for j in range(n if n is not None else v['n']): Jb.append((v['veh'], r - tr, d + tr, p + 2 * tr, key, s))
    if s in SOUTH: job('marshal', ob - 40, ob, 40)
    if 'gpu' in S: job('gpu', ob + 15, tp - 20, tp - ob - 35)
    if 'stairs' in S: job('stairs', ob + 10, tp - 20, tp - ob - 30)
    if 'bus' in S:
        bd = S['bus']['d']; job('bus', ob + 20, ob + 20 + bd + 60, bd); job('bus', tp - 30 - bd - 90, tp - 30, bd)
    if 'bags' in S:   # רכבת אחת לכל סבב (2 עגלות, כמו BT-P2 של היום): האולם — טעינת היוצאות לעגלה ב׳ → המטוס — פריקת הנכנסות לעגלה א׳ וטעינה מעגלה ב׳ → האולם — פריקת עגלה א׳
        bd = S['bags']['d']; hv = HALL['prep'] + HALL['entry'] + AC[m]['bag'] / S['bags']['n'] * HALL['cad'] + HALL['exit']
        job('bags', ob + 25 - hv - 35, tp - 30 + 35 + hv, hv + 35 + bd + 35 + hv)
    if 'belt' in S:
        d = S['belt']['d'] * .5; job('belt', ob + 20, ob + 20 + d + 60, d); job('belt', ob + 60, tp - 25, d)
    if 'uld' in S: job('uld', ob + 30, tp - 60, S['uld']['d'])
    if 'uld2' in S: job('uld2', ob + 30, tp - 60, S['uld2']['d'] * 2, S['uld2']['n'])
    for k, off in (('fuel', 60), ('cater', 70), ('water', 60), ('lav', 100), ('clean', 40)):
        if k in S: job(k, ob + off, tp - 60, S[k]['d'])
    if 'push' in S: job('push', tp - 10, tp - 10 + S['push']['d'], S['push']['d'])
    return Jb
def kmin(J):
    # המספר הקטן ביותר של רכבים שבו כל העבודות נכנסות בחלונות שלהן (שיבוץ חמדני לפי השחרור, 3 מחזורים)
    import heapq
    jobs = sorted([(r + c * T, d + c * T, p) for (_, r, d, p, _k, _s) in J for c in range(3)])
    for k in range(1, 40):
        # EDF: כשרכב מתפנה — העבודה ששוחררה עם היעד המוקדם ביותר
        free = [jobs[0][0] if jobs else 0] * k; i = 0; ready = []; ok = True; n = len(jobs); done = 0
        while done < n:
            m = min(range(k), key=lambda q: free[q]); t = free[m]
            while i < n and jobs[i][0] <= t + 1e-9: heapq.heappush(ready, (jobs[i][1], jobs[i][0], jobs[i][2])); i += 1
            if not ready:
                t = jobs[i][0]; free[m] = t; continue
            d, r, p = heapq.heappop(ready); st = max(t, r)
            if st + p > d + 1e-6 and r >= T and r < 2 * T: ok = False; break
            free[m] = st + p; done += 1
        if ok: return k
    return 99
def fleet_need(fl):
    JB = [j for f in fl for j in svc_jobs(f)]
    byJ = C.defaultdict(list)
    for j in JB: byJ[j[0]].append(j)
    W = [w for f in fl for w in svc_windows(f)]
    by = C.defaultdict(list)
    for w in W: by[w[0]].append(w)
    out = {}
    have = C.Counter(NEW.get('spotTypes') or {sp['t']: 0 for sp in D['spots'].values()})   # החניות במשחק (S7F298, אחרי 074r_S15k)
    have_sched = C.Counter(v['model'] for v in NEW['veh'])
    old_fleet = OLD['seeds'][0]['fleet']
    for vt, L in sorted(by.items()):
        pk = peak(L); busy = sum(b - a for _, a, b, _k in L); km = kmin(byJ.get(vt, []))
        need = km + (1 if km >= 3 or busy / T / max(1, km) > .8 else 0)      # רזרבה: מ-3 ומעלה, או כשהרכב היחיד עסוק מעל 80% (הבקר 17.11)
        stands = sorted(set(j[5] for j in byJ.get(vt, [])))
        out[vt] = dict(he=VEH_HE.get(vt, vt), trips=len(L), busy_s=round(busy), util=round(busy / T / max(1, need) * 100), peak=pk, kmin=km, need=need, stands=stands,
                       today_spots=have.get({'FTs': 'FT', 'TG': 'TG', 'HL': 'HL'}.get(vt, vt), 0),
                       old=(old_fleet.get({'SV': 'SVC', 'FTs': 'FW', 'TG': 'CU'}.get(vt, vt)) or {}).get('n'))
    return out, W

# ---------------------------------------------------------------- 7. אולמות הכבודה: תור לכל מספר עמדות (1–5)
HALL = dict(prep=4, entry=10, exit=12, cad=2.2)                    # S15I_HALL: ‏cad 2.2, ‏E 4; הכניסה / הפינוי — מהבודק (9.2–27.2 ש׳)
def hall_visits(fl):
    V = []
    for f in fl:
        a = AC[f['model']]
        if not a['bag'] or a['cls'] in ('GA', 'EXEC', 'AMPH'): continue
        nA = nD = a['bag']; ob = f['onblock']; tp = f['push'] if f['push'] > ob else f['push'] + T
        half = MATRIX[f['model']]['bags']['d'] / 2; trains = MATRIX[f['model']]['bags']['n']
        for j in range(trains):
            dA = HALL['prep'] + HALL['entry'] + nA / trains * HALL['cad'] + HALL['exit']; dD = HALL['prep'] + HALL['entry'] + nD / trains * HALL['cad'] + HALL['exit']
            V.append(dict(stand=f['stand'], kind='dep', t=ob + 25 - 35 - dD + j * 6, dur=dD, units=nD // trains))            # טעינת היוצאות באולם — לפני שהרכבת יוצאת למטוס
            V.append(dict(stand=f['stand'], kind='arr', t=ob + 25 + 2 * half + 35 + j * 6, dur=dA, units=nA // trains))      # פריקת הנכנסות באולם — אחרי השירות ליד המטוס
    return V
def hall_queue(V, n):
    # תור FCFS מחזורי (3 מחזורים כדי שהמחזור יתייצב), עמדה ראשונה שמתפנה
    ev = sorted([dict(v, t=v['t'] + c * T) for v in V for c in range(3)], key=lambda v: v['t'])
    free = [0.0] * n; waits = []; busy = 0
    for v in ev:
        j = min(range(n), key=lambda i: free[i]); st = max(v['t'], free[j]); free[j] = st + v['dur']
        if v['t'] >= T: waits.append(st - v['t']); busy += v['dur'] if v['t'] < 2 * T else 0
    units = sum(v['units'] for v in V)
    return dict(stations=n, visits=len(V), units_cycle=units, units_hour=round(units * 3600 / T), util=round(busy / T / n * 100, 1),
                wait_mean=round(sum(waits) / len(waits), 1) if waits else 0, wait_max=round(max(waits), 1) if waits else 0,
                late=sum(1 for w in waits if w > 30))

# ---------------------------------------------------------------- 8. נוסעים, מושבים וצוותים
def pax(fl):
    gates = C.defaultdict(list); seats = {k: len(v) for k, v in TL['seats'].items()}
    tot = []
    for f in fl:
        a = AC[f['model']]; n = round(a['seats'] * a['lf']); vis = math.ceil(n / VIS) if n else 0
        if not vis or a['cls'] in ('GA', 'EXEC'): continue
        g = 'R' if f['stand'].startswith('R') else f['stand']
        tp = f['push'] if f['push'] > f['onblock'] else f['push'] + T
        gates[g].append((tp - 330, tp - 40, vis)); tot.append((f['stand'], f['model'], n, vis))
    res = {}
    for g, L in gates.items():
        pts = []
        for a, b, v in L: pts += [(a % T, v), ((a % T) + (b - a), -v), (a % T + T, v), ((a % T) + (b - a) + T, -v)]
        pts.sort(); c = mx = 0
        for _, d in pts: c += d; mx = max(mx, c)
        avg = sum((b - a) * v for a, b, v in L) / T
        res[g] = dict(seats=seats.get(g, 0), peak=mx, avg=round(avg, 1), ok=mx <= seats.get(g, 0))
    return dict(flights=tot, gates=res, nominal_cycle=sum(t[2] for t in tot) * 2, visual_cycle=sum(t[3] for t in tot) * 2)
CREW = {'PT': 2, 'GP': 1, 'MS': 1, 'AB': 1, 'BT': 1, 'BL': 2, 'HL': 2, 'TG': 1, 'FT': 1, 'FTs': 1, 'CT': 2, 'WT': 1, 'LV': 1, 'SVC': 3, 'SV': 1}
def crew(fleet, hallq):
    peak_staff = sum(v['peak'] * CREW.get(k, 1) for k, v in fleet.items())
    marshal = 6; hall = 2 * hallq['stations']; tower = 3; arff = 3 * 3
    tot = peak_staff + marshal + hall
    return dict(vehicles=peak_staff, marshal=marshal, hall=hall, tower=tower, arff_standby=arff, peak=tot, roster=math.ceil(tot * 1.15) + tower + arff)

# ---------------------------------------------------------------- 9. הפריסה המוצעת (הציור משתמש באותם נתונים)
CORE = D['core']; WALL = 886
# כל המדרגות והמדרגות הנעות של הטרמינל (S15J_L.stairs, כולל המשטח למטה); המדרגות של P1 — במקום החדש שבהצעה (60 דרומה, לאישורך)
P1_STAIRS_NEW = [6762, 975, 6807, 1031]     # השורש של השרוול של P1 ב-(6760, 956): המשטח ב-+4.0 בגובה השורש (y 940–975), והמדרגות יורדות דרומה לאורך הקיר המערבי
P1_LAND_NEW = [6762, 940, 6807, 975]
STAIRS = []
for st in TL['stairs']:
    r = list(st['r']); ld = st.get('land')
    if st['id'] == 'P1': r = P1_STAIRS_NEW; ld = P1_LAND_NEW
    if ld: r = [min(r[0], ld[0]), min(r[1], ld[1]), max(r[2], ld[2]), max(r[3], ld[3])]
    STAIRS.append(r)
ROOTS = [b['root'] for b in D['bridges']]
TRAIN = dict(W=26, L=38 + 2 * (31.5 + 9))                                     # טרקטור 38 + 2 עגלות (31.5 + 9) — מעטפת הציור (הבודק §7)
# 5 עמדות כבודה עצמאיות בקומת הרחבה מתחת לאגף השערים — כל אחת U משלה: דלת כניסה, נתיב, מסוע, עצירה, דלת יציאה (כמו BAG5 של היום, שנשאר BH-3)
HALLS = [
 dict(id='BH-1', he='עמדת כבודה 1 — P1 / P2 (חדשה; המדרגות של P1 עוברות לקיר המערבי ויורדות דרומה)', r=[6812, 905, 7016, 945], din=[6817, 6853], dout=[6975, 7011], lane=932, belt=[6860, 6966, 905], serves=['P1', 'P2'], needs='המדרגות של P1 → משטח [6762, 940, 6807, 975], מדרגות [6762, 975, 6807, 1031]'),
 dict(id='BH-2', he='עמדת כבודה 2 — P2 / P3 (חדשה)', r=[7165, 905, 7400, 961], din=[7175, 7215], dout=[7350, 7390], lane=945, belt=[7220, 7345, 923], serves=['P2', 'P3']),
 dict(id='BH-3', he='עמדת כבודה 3 — P3 / P4 (האולם של היום, BAG5 — נשאר כמו שהוא)', r=[7600, 905, 7820, 1015], din=[7620, 7660], dout=[7780, 7818], lane=948, belt=[7655, 7775, 921], serves=['P3', 'P4'], today=True),
 dict(id='BH-4', he='עמדת כבודה 4 — P4 / P5 (חדשה, מתחת ל-CE, ממזרח למדרגות הנעות של P4)', r=[8002, 905, 8235, 961], din=[8008, 8044], dout=[8180, 8216], lane=945, belt=[8050, 8170, 923], serves=['P4', 'P5']),
 dict(id='BH-5', he='עמדת כבודה 5 — P5 / P6 / R (חדשה: הקצה המזרחי של CE ותוספת עם גג שקוף עד שביל השירות SR_E)', r=[8314, 905, 8505, 961], din=[8318, 8352], dout=[8468, 8502], lane=948, belt=[8360, 8462, 921], serves=['P5', 'P6', 'R'], annex=[8402, 886, 8508, 961]),
]
LOUNGE_AFTER = [   # הטרקלינים אחרי (לאישורך): ברצועה הדרומית של אגף השערים, מתחת לעמדות הכבודה שבצפון; P6 ו-R — באגף מזרח (TE)
 dict(g='P1', r=[6815, 955, 7060, 1028], note='במקום הדיוטי פרי (CW-DF), שעובר לצד הדרומי של המסדרון'), dict(g='P2', r=[7065, 966, 7330, 1028]), dict(g='P3', r=[7340, 966, 7598, 1028]),
 dict(g='P4', r=[7960, 966, 8170, 1028]), dict(g='P5', r=[8180, 966, 8398, 1028]), dict(g='P6', r=[8900, 1038, 9062, 1140], note='שער P6 במערב הטרקלין (4 שורות, ליד המדרגות) + 17 המושבים של היום במזנונים; טרקלין העסקים — x 9066–9158'),
 dict(g='R', r=[8900, 1150, 9158, 1206], note='שער ההסעות (TE-BUS) — מתרחב מערבה עד החנויות (x 8900)')]
def lounge_cap(r): return int((r[2] - r[0] - 10) // 7) * int((r[3] - r[1] - 8) // 13)      # מושב כל 7 פיקס׳, שורה כל 13
try:   # הפריסה שנוצרה ב-s15j_layout_fc.py — המושבים בפועל לכל טרקלין (במקום ההערכה)
    LFC = json.load(open(os.path.join(HERE, 's15j_layout_fc.json'), encoding='utf-8'))
    GEN_SEATS = {g: len(v) for g, v in LFC['seats'].items()}
except Exception: LFC = None; GEN_SEATS = {}
VIS_Y = 950        # במבט 3/4 הקיר הצפוני של הטרמינל (15 מ׳, ‏y 1033) מסתיר את מה שמדרום ל-y ~943 (074p: S15I_HALL) — הנתיב והמסוע בצפון האולם
# ההרחבה הדרומית־מזרחית (H4, חצי אזור): בסיס צי דרומי, מזח צף לאמפיבי ומסלול מים; הגבול הצפוני — קו החוף y 2550; הדרומי — 2830 (מרווח מנתיב הסירות של המספנה)
BSHOP = dict(act=[7200, 2552, 8046, 2800], wharf=[7776, 2552, 8040, 2792], lane=[[7120, 2880], [9420, 2960]])     # 074g_boatshop.js — LIKE-08, לא זז
EXP = dict(rect=[8480, 2550, 9600, 2830], he='ההרחבה הדרומית־מזרחית — חצי אזור (H4)')
GSE_S = [dict(id='S-%s%d' % (t, i + 1), t=t, r=[8500 + j * 44, 2600, 8500 + j * 44 + (28 if t in ('FT', 'CT', 'AB', 'MS') else 22), 2600 + (100 if t in ('FT', 'AB', 'CT') else 75 if t in ('MS', 'BL') else 60)])
         for j, (t, i) in enumerate([('PT', 0), ('PT', 1), ('BT', 0), ('BT', 1), ('BL', 0), ('GP', 0), ('GP', 1), ('MS', 0), ('AB', 0), ('FT', 0), ('CT', 0),
                                     ('SVC', 0), ('WT', 0), ('LV', 0), ('SV', 0), ('BT', 2), ('PT', 2), ('GP', 2)])]
GSE_ROAD = dict(id='AIR-S-BASE', he='דרך הבסיס הדרומי (חדש)', r=[8480, 2700, 9580, 2744])
AMPH = dict(dock=[8180, 2600, 8470, 2640], ramp=[8433, 2548, 8463, 2602], lane=[7300, 3480, 9450, 3580], taxi=[[8300, 2662], [8300, 3480]],
            trawl=[7531, 3035, 9454, 3365], ship_lane_y=3620,   # שטח הדיג של TRAWL-1 (S14D.trawl + חצי הגוף) והמצופים של LANE-L1 — 17.11 09:30
            he='מזח צף ומסלול מים לאמפיבי (נוחת מערבה, מסיע צפונה, נקשר)')

# ---------------------------------------------------------------- 10. בדיקת המרווחים (נכשלת אם יש חפיפה / מרווח קטן מהנדרש)
def rint(a, b, pad=0): return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad
def rgap(a, b):
    dx = max(0, max(a[0], b[0]) - min(a[2], b[2])); dy = max(0, max(a[1], b[1]) - min(a[3], b[3])); return math.hypot(dx, dy)
def inside(a, b): return a[0] >= b[0] and a[1] >= b[1] and a[2] <= b[2] and a[3] <= b[3]
def seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; u = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy))); return math.hypot(a[0] + u * dx - p[0], a[1] + u * dy - p[1])
def rect_seg_dist(r, a, b):
    if any(r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3] for p in (a, b)): return 0
    cs = [(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])]
    d = min(seg_dist(c, a, b) for c in cs)
    for i in range(4):
        c0, c1 = cs[i], cs[(i + 1) % 4]; d = min(d, seg_dist(a, c0, c1), seg_dist(b, c0, c1))
    return d
def foot(s, m):
    cx, ny = nose_xy(s); L, Wd = DIM[m]; return [cx - Wd / 2, ny - L, cx + Wd / 2, ny]
def shape(s, m):
    # הצורה במבט מלמעלה (האף דרומה, אל העמדה): גוף (רוחב 12% מהמוטה, לפחות 2 מ׳), כנף (המוטה המלאה, מיתר 18% מהאורך, ב-45% מהאף; קלים — 35%),
    # זנב (38% מהמוטה, ב-12% האחרונים). המנועים מתחת לכנף — בתוך מלבן הכנף.
    cx, ny = nose_xy(s); L, Wd = DIM[m]; ga = AC[m]['cls'] in ('GA', 'EXEC', 'AMPH'); fw = max(20, .12 * Wd)
    wc = ny - (.35 if ga else .45) * L; ch = (.15 if ga else .18) * L
    return [[cx - fw / 2, ny - L, cx + fw / 2, ny], [cx - Wd / 2, wc - ch / 2, cx + Wd / 2, wc + ch / 2], [cx - .19 * Wd, ny - L, cx + .19 * Wd, ny - .88 * L]]
def clearance(plan_stands):
    R = []
    def chk(id, ok, det, kind='FAIL'): R.append(dict(id=id, ok=bool(ok), det=det, kind=kind))
    # (א) העמדות שבלוח: מעטפת המטוס (מוטה × אורך) בתוך העמדה, ומרווח קצות כנפיים בין עמדות סמוכות
    used = sorted(set(plan_stands))
    for s, m in plan_stands.items():
        f = foot(s, m); r = ST[s]['rect']
        chk('stand-in-' + s, inside(f, [r[0] - 1, r[1] - 1, r[2] + 1, r[3] + 1]), '%s %s — המעטפת %s בתוך %s' % (s, HE.get(m, m), [round(x) for x in f], r))
    ks = list(plan_stands)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = ks[i], ks[j]; fa, fb = foot(a, plan_stands[a]), foot(b, plan_stands[b])
            need = 30 if (AC[plan_stands[a]]['cls'] not in ('GA', 'EXEC') or AC[plan_stands[b]]['cls'] not in ('GA', 'EXEC')) else 20
            g = rgap(fa, fb)
            if g < 400: chk('wingtip-%s-%s' % (a, b), g >= need, '%s ↔ %s: מרווח %.0f פיקס׳ (%.1f מ׳), נדרש %d' % (a, b, g, g / PXM, need))
    # (ב) כיסי הציוד והחניות של היום מול המעטפות שבלוח (רכב חונה מתחת לכנף — אסור)
    for pk, pr in D['pockets'].items():
        for s, m in plan_stands.items():
            hit = [i for i, q in enumerate(shape(s, m)) if rint(pr, q)]
            if hit: chk('pocket-%s-%s' % (pk, s), False, 'הכיס %s חופף את %s של %s (%s)' % (pk, '/'.join(('הגוף', 'הכנף', 'הזנב')[i] for i in hit), s, HE.get(m, m)))
            elif rint(pr, foot(s, m)): chk('pocket-%s-%s' % (pk, s), True, 'הכיס %s בתוך מלבן המוטה של %s — לפני הכנף, ליד הגוף (מותר)' % (pk, s), 'INFO')
    # (ג) עמדות הכבודה: בתוך אגף השערים, בלי מדרגות ושורשי שרוולים, הדלתות רחוקות מהשורשים, הרכבת נכנסת לנתיב
    for h in HALLS:
        r = h['r']
        if h.get('annex'):
            ax = h['annex']; inC = inside([r[0], r[1], min(r[2], CORE[2]), r[3]], [CORE[0], WALL, CORE[2], CORE[3]]) and inside([max(r[0], ax[0]), r[1], r[2], r[3]], ax)
            chk(h['id'] + '-in-core', inC, '%s %s: בתוך אגף השערים עד x %d ובתוך התוספת %s' % (h['id'], r, CORE[2], ax))
            for s2, m2 in plan_stands.items():
                for q in shape(s2, m2):
                    if rint(ax, q): chk('%s-annex-%s' % (h['id'], s2), False, 'התוספת %s נוגעת במטוס של %s' % (ax, s2))
            for sv in D['service']:
                if sv['id'] in ('AIR-SR_E', 'AIR-SR_P6') and rint(ax, sv['rect']): chk('%s-annex-road-%s' % (h['id'], sv['id']), False, 'התוספת חוסמת את %s' % sv['id'])
            for pk, pr in D['pockets'].items():
                if rint(ax, pr): chk('%s-annex-pocket-%s' % (h['id'], pk), False, 'התוספת על הכיס %s' % pk)
        else:
            chk(h['id'] + '-in-core', inside(r, [CORE[0], WALL, CORE[2], CORE[3]]), '%s %s בתוך אגף השערים %s' % (h['id'], r, CORE))
        chk(h['id'] + '-visible', h['lane'] <= VIS_Y and h['belt'][2] <= VIS_Y - 20, '%s: הנתיב y %d והמסוע y %d — צפונית לקו ההסתרה של 3/4 (y %d)' % (h['id'], h['lane'], h['belt'][2], VIS_Y))
        for st in STAIRS:
            okS = not rint(r, st, 4)
            chk('%s-stairs-%d' % (h['id'], st[0]), okS or h.get('today'), '%s מול המדרגות %s — מרווח %.0f%s' % (h['id'], st, rgap(r, st), ' (קיים היום — BAG5 והמדרגות הנעות P3E; לא שונה)' if (h.get('today') and not okS) else ''), 'INFO' if (h.get('today') and not okS) else 'FAIL')
        for rt in ROOTS:
            for nm, dr in (('in', h['din']), ('out', h['dout'])):
                if rt[1] <= WALL + 2:
                    d = max(0, max(dr[0], rt[0]) - min(dr[1], rt[0]))
                    if abs(rt[0] - (dr[0] + dr[1]) / 2) < 80: chk('%s-door%s-root%d' % (h['id'], nm, rt[0]), d >= 25, '%s דלת %s %s מול שורש השרוול x %d — %.0f פיקס׳ (נדרש 25)' % (h['id'], nm, dr, rt[0], d))
        span = (h['dout'][0] + h['dout'][1]) / 2 - (h['din'][0] + h['din'][1]) / 2
        chk(h['id'] + '-train-fits', span - TRAIN['W'] >= TRAIN['L'] and h['belt'][1] - h['belt'][0] >= 100, '%s: בין הרגליים %.0f מול אורך הרכבת %.0f; המסוע %d' % (h['id'], span - TRAIN['W'], TRAIN['L'], h['belt'][1] - h['belt'][0]))
        chk(h['id'] + '-lane-depth', (h['lane'] - WALL) >= TRAIN['W'] + 20 and (r[3] - h['lane']) >= TRAIN['W'] / 2, '%s: הנתיב ב-y %d (עומק %d)' % (h['id'], h['lane'], h['lane'] - WALL))
    # הטרקלינים של השערים בקומה שמעל (S15J_L.seats): מושב בתוך הרצועה של עמדה (x של האולם, y 900–965) — צריך לזוז (כמו ב-BAG5 היום); זה שינוי נדרש, לא כישלון
    for h in HALLS:
        if h.get('today'): continue
        n = {g: sum(1 for q in v if h['r'][0] <= q[0] <= h['r'][2] and 900 <= q[1] <= 965) for g, v in TL['seats'].items()}
        n = {g: k for g, k in n.items() if k}
        if n: chk(h['id'] + '-seats', False, '%s: מעל העמדה, בקומת השערים — %s מושבים (%s) צריכים לזוז מהרצועה (רצפת זכוכית מעל העמדה, כמו מעל BAG5)' % (h['id'], sum(n.values()), ', '.join('%s %d' % kv for kv in n.items())), 'CHANGE')
    for i in range(len(HALLS)):
        for j in range(i + 1, len(HALLS)):
            A_, B_ = HALLS[i], HALLS[j]
            if A_.get('hall') and A_.get('hall') == B_.get('hall'):
                # שני נתיבים באותו אולם: הרכבת העומדת בנתיב אחד לא חוסמת את הרגליים (הכניסה והיציאה) של השני, והנתיבים רחוקים מספיק
                dl = abs(A_['lane'] - B_['lane']); xin = (A_['din'][0] + A_['din'][1]) / 2; xout = (A_['dout'][0] + A_['dout'][1]) / 2
                stopL = [A_['belt'][0], A_['belt'][1]]; free = (xout - TRAIN['W'] / 2) - (xin + TRAIN['W'] / 2)
                chk('lanes-%s-%s' % (A_['id'], B_['id']), dl >= TRAIN['W'] + 20 and free >= TRAIN['L'], '%s / %s: בין הנתיבים %d (נדרש %d); בין הרגליים %.0f — הרכבת %.0f' % (A_['id'], B_['id'], dl, TRAIN['W'] + 20, free, TRAIN['L']))
                continue
            a, b = A_['r'], B_['r']; chk('halls-%s-%s' % (A_['id'], B_['id']), rgap(a, b) >= 10, 'מרווח %.0f' % rgap(a, b))
    # אפשרות B2 (מסלול הסעה מקביל לקלים לאורך הגדר המזרחית) — נבדקת: הקו ב-x 9540, דו-מנועי קל (מוטה 11.2 מ׳): ‏≥ 3 מ׳ מהגדר (x 9600) ומ-B
    b2c = 9540; hw = DIM['AC-LT-01'][1] / 2; m_f = 9600 - (b2c + hw); m_b = (b2c - hw) - (TBX + DIM['AC-BJ-01'][1] / 2)
    chk('B2-option', m_f >= 30 and m_b >= 30, 'B2 (אפשרות): קצה הכנף 9540 ± %.0f — %.0f פיקס׳ מהגדר, %.0f ממטוס מנהלים ב-B (נדרש 30 לכל צד)' % (hw, m_f, m_b), 'OPTION')
    # הדרך אל הדלתות — שביל השירות SR_C (y 798–886) פנוי ממעטפות המטוסים בלוח
    src = next(s for s in D['service'] if s['id'] == 'AIR-SR_C')['rect']
    for h in HALLS:
        for nm, dr in (('in', h['din']), ('out', h['dout'])):
            acc = [dr[0], src[1], dr[1], WALL]
            for s, m in plan_stands.items():
                if any(rint(acc, q) for q in shape(s, m)): chk('%s-access%s-%s' % (h['id'], nm, s), False, '%s: הגישה לדלת %s עוברת מתחת ל-%s (%s)' % (h['id'], nm, s, HE.get(m, m)))
                elif rint(acc, foot(s, m)): chk('%s-access%s-%s' % (h['id'], nm, s), True, '%s: הגישה לדלת %s בתוך מלבן המוטה של %s — ליד האף, רחוק מהכנף (מותר)' % (h['id'], nm, s), 'INFO')
    # (ד) ההרחבה הדרומית: מול המספנה והמעגן (LIKE-08), מול נתיב הסירות, מול שטחי הבטיחות של המנחתים, בתוך העולם
    E = EXP['rect']
    chk('exp-boatshop', not rint(E, BSHOP['act'], 40) and not rint(E, BSHOP['wharf'], 40), 'ההרחבה %s מול המספנה %s — מרווח %.0f (נדרש 40)' % (E, BSHOP['act'], min(rgap(E, BSHOP['act']), rgap(E, BSHOP['wharf']))))
    dl = rect_seg_dist(E, *BSHOP['lane']); chk('exp-boatlane', dl >= 60, 'ההרחבה מול נתיב הסירות של המספנה — %.0f פיקס׳ (נדרש 60)' % dl)
    chk('exp-world', E[2] <= 9600, 'בתוך העולם (x ≤ 9600)')
    for hp in D['helipads']:
        chk('exp-heli-' + hp['id'], not rint(E, hp['safe']), 'ההרחבה מול שטח הבטיחות של %s' % hp['id'])
    for g in GSE_S:
        chk('gse-in-exp-' + g['id'], inside(g['r'], E), '%s בתוך ההרחבה' % g['id'])
        chk('gse-road-' + g['id'], not rint(g['r'], GSE_ROAD['r']), '%s מול דרך הבסיס הדרומי' % g['id'])
    for i in range(len(GSE_S)):
        for j in range(i + 1, len(GSE_S)):
            a, b = GSE_S[i], GSE_S[j]
            if rint(a['r'], b['r'], 6): chk('gse-%s-%s' % (a['id'], b['id']), False, 'חניות צמודות מדי (< 0.6 מ׳)')
    # (ה) האמפיבי: המזח מחוץ למספנה, מסלול המים במים (דרומית לחוף ולהרחבה, ‏≥ 150), חוצה את נתיב הסירות רק בהסעה (רשום)
    chk('amph-dock-boatshop', not rint(AMPH['dock'], BSHOP['act'], 40) and not rint(AMPH['dock'], BSHOP['wharf'], 40), 'המזח הצף %s מול המספנה — מרווח %.0f' % (AMPH['dock'], min(rgap(AMPH['dock'], BSHOP['act']), rgap(AMPH['dock'], BSHOP['wharf']))))
    chk('amph-lane-water', AMPH['lane'][1] - max(E[3], 2550) >= 150, 'מסלול המים %s — %d פיקס׳ דרומית ליבשה' % (AMPH['lane'], AMPH['lane'][1] - max(E[3], 2550)))
    dl2 = rect_seg_dist(AMPH['lane'], *BSHOP['lane']); chk('amph-lane-boatlane', dl2 >= 60, 'מסלול המים מול נתיב הסירות — %.0f פיקס׳' % dl2)
    chk('amph-lane-trawl', AMPH['lane'][1] - AMPH['trawl'][3] >= 60, 'מסלול המים מול שטח הדיג של TRAWL-1 (הגוף עד y %d) — %d פיקס׳ (נדרש ≥ 60: חצי מוטה + מרווח)' % (AMPH['trawl'][3], AMPH['lane'][1] - AMPH['trawl'][3]))
    chk('amph-lane-ships', AMPH['ship_lane_y'] - AMPH['lane'][3] >= 30, 'מסלול המים מול נתיב האוניות LANE-L1 (המצופים ב-y %d) — %d פיקס׳' % (AMPH['ship_lane_y'], AMPH['ship_lane_y'] - AMPH['lane'][3]))
    chk('amph-lane-len', AMPH['lane'][2] - AMPH['lane'][0] >= 1500, 'אורך מסלול המים %d (נדרש ≥ 1500 — ‏ICON A5 של 074zm)' % (AMPH['lane'][2] - AMPH['lane'][0]))
    # (ו) R3 בלי מטוס קבוע: ההרצה בלילה בתוך RUNUP, הסילון אל גדר הסילון בדרום
    ru = D['runup']; f = [ST['R3']['cx'] - DIM['AC-TP-01'][1] / 2, ru[1], ST['R3']['cx'] + DIM['AC-TP-01'][1] / 2, ru[1] + DIM['AC-TP-01'][0]]
    chk('R3-runup', inside(f, [ru[0] - 20, ru[1] - 60, ru[2] + 20, ru[3] + 20]), 'ההרצה (TP) %s בתוך המקום %s' % ([round(x) for x in f], ru))
    fails = [r for r in R if not r['ok'] and r['kind'] == 'FAIL']
    opt = [r for r in R if r['kind'] == 'OPTION']; chg = [r for r in R if r['kind'] == 'CHANGE']
    return dict(checks=len(R), fails=len(fails), ok=not fails, list=R, options=opt, changes=chg)

# ---------------------------------------------------------------- 11. הרצה
def run():
    out = dict(T=T, K=K, ROT=ROT, SEP=SEP, VIS=VIS, matrix=MATRIX, svc_he=SVC_HE, veh_he=VEH_HE, ac={m: dict(AC[m], he=HE.get(m, m), L=DIM[m][0] / PXM, span=DIM[m][1] / PXM, dwell=DWELL.get(m)) for m in AC})
    o = OLD['seeds']; out['old'] = dict(moves=[s['mov'] for s in o], land=[s['land'] for s in o], to=[s['to'] for s in o], heli=[s['heliLand'] + s['heliDep'] for s in o],
                                        exec_to=[sum(v for k, v in s['mixT'].items() if k in ('AC-BJ-01', 'AC-CN-01')) for s in o],
                                        stands=[s['nStands'] for s in o], turn=[s['turnBy'] for s in o], rotA=o[0]['rotA'], rotD=o[0]['rotD'], gap=[(s['gapMin'], s['gapMed']) for s in o],
                                        why=[s['why'] for s in o], fleet=o[0]['fleet'], mix=[s['mixL'] for s in o])
    nf = NEW['flights']; out['new_today'] = dict(flights=len(nf), moves1800=round(2 * len(nf) * 1800 / T, 1), veh=NEW['nVeh'], spots=NEW['spots'],
                                                 term=NEW['term']['flights'], hall=NEW['hall']['trains'], sched=NEW['sched'])
    out['rwy_theory'] = {'NB': rwy_theory('AC-NB-01'), 'RJ': rwy_theory('AC-RJ-01')}
    scen = {}
    for name, b2 in (('base', False), ('b2', True)):
        fl, miss, E, L = schedule(PLAN, b2=b2)
        scen[name] = dict(b2=b2, flights=fl, miss=miss, rwy=rwy_stats(E), link=link_stats(L))
    mx = list(PLAN); added = []
    for x in EXTRA:
        trial = [(a, b, c, (n + 1 if (a, b) == (x[0], x[1]) else n)) for a, b, c, n in mx]
        fl2, miss2, E2, L2 = schedule(trial)
        if not miss2: mx = trial; added.append(x[0])
    fl2, miss2, E2, L2 = schedule(mx)
    scen['max'] = dict(b2=False, added=added, flights=fl2, miss=miss2, rwy=rwy_stats(E2), link=link_stats(L2))
    # הבחירה: התרחיש בלי B2 אם הוא עומד ביעד; אחרת עם B2
    target = 2 * max(out['old']['moves'])
    pick = 'max' if (scen['max']['rwy']['per1800'] >= target and scen['max']['link']['util'] <= 90) else ('base' if scen['base']['rwy']['per1800'] >= target else 'b2')
    out['scen'] = {k: dict(v, flights=None) for k, v in scen.items()}
    out['pick'] = pick; out['target1800'] = target
    fl = scen[pick]['flights']; out['schedule'] = fl
    fleet, W = fleet_need(fl); out['fleet'] = fleet
    out['fleet_dedicated'] = {}
    V = hall_visits(fl); out['halls'] = [hall_queue(V, n) for n in (1, 2, 3, 4, 5)]
    out['pax'] = pax(fl)
    pick_h = next((h for h in out['halls'] if h['wait_max'] <= 30 and h['util'] <= 60), out['halls'][-1])
    out['crew'] = crew(fleet, pick_h)
    out['heli_plan'] = dict(pads=[p['id'] for p in D['helipads']], sorties720={'H2': 4, 'H3': 4, 'H4': 3, 'O2': 2, 'O1': 1.5},
                            moves1800=round(2 * (4 + 4 + 3 + 2 + 1.5) * 1800 / T, 1), old=out['old']['heli'])
    global HALLS
    keepH = HALLS; HALLS = HALLS + [dict(id='BAD-1', he='בדיקה עצמית', r=[7100, 905, 7300, 1015], din=[7110, 7150], dout=[7250, 7290], lane=950, belt=[7150, 7250, 923], serves=[])]
    bad = clearance({'GA5': 'AC-BJ-01', 'P2': 'AC-NB-01', 'P3': 'AC-NB-01'}); HALLS = keepH
    out['selftest'] = dict(fails=bad['fails'], ids=[r['id'] for r in bad['list'] if not r['ok'] and r['kind'] == 'FAIL'][:8])
    stands_used = {f['stand']: f['model'] for f in fl}
    stands_used.setdefault('R3', 'AC-TP-01')
    out['clear'] = clearance(stands_used)
    out['lounges'] = [dict(l, cap=GEN_SEATS.get(l['g']) if GEN_SEATS.get(l['g']) else lounge_cap(l['r']), gen=bool(GEN_SEATS.get(l['g'])), need=(out['pax']['gates'].get(l['g']) or {}).get('peak'), today=len(TL['seats'].get(l['g'], []))) for l in LOUNGE_AFTER]
    for l in out['lounges']:
        if l['need'] is not None and l['cap'] < l['need']: out['clear']['list'].append(dict(id='lounge-' + l['g'], ok=False, kind='FAIL', det='הטרקלין %s: %d מושבים מול שיא %d' % (l['g'], l['cap'], l['need']))); out['clear']['fails'] += 1; out['clear']['ok'] = False
        else: out['clear']['list'].append(dict(id='lounge-' + l['g'], ok=True, kind='FAIL', det='הטרקלין %s: %d מושבים (היום %d) מול שיא %s' % (l['g'], l['cap'], l['today'], l['need']))); out['clear']['checks'] += 1
        for h in HALLS:
            if rint(l['r'], h['r'], 0) and l['r'][1] < h['lane'] + TRAIN['W'] / 2: out['clear']['list'].append(dict(id='lounge-hall-%s-%s' % (l['g'], h['id']), ok=False, kind='FAIL', det='הטרקלין %s נוגע בנתיב של %s' % (l['g'], h['id']))); out['clear']['fails'] += 1; out['clear']['ok'] = False
        for st in STAIRS:
            if rint(l['r'], st): out['clear']['list'].append(dict(id='lounge-stairs-%s' % l['g'], ok=True, kind='INFO', det='הטרקלין %s ליד המדרגות %s — המדרגות נשארות, המושבים סביבן' % (l['g'], st)))
    out['layout'] = dict(stairs=STAIRS, p1_stairs_new=P1_STAIRS_NEW, p1_land_new=P1_LAND_NEW, halls=HALLS, exp=EXP, gse_s=GSE_S, gse_road=GSE_ROAD, amph=AMPH, bshop=BSHOP, train=TRAIN)
    json.dump(out, open(os.path.join(HERE, 'fc_result.json'), 'w'), ensure_ascii=False, indent=1)
    # הדפסה
    print('הישן (S7F272, 3 זרעים, 1800 ש׳): תנועות', out['old']['moves'], '· מסוקים', out['old']['heli'], '· מנהלים בהמראה', out['old']['exec_to'])
    print('החדש היום (S7F298):', out['new_today']['flights'], 'טיסות במחזור →', out['new_today']['moves1800'], 'תנועות ב-1800 ש׳')
    print('המסלול — תיאורטי:', out['rwy_theory'])
    for k, v in scen.items():
        print('תרחיש', k, 'מסלול', v['rwy'], '· קישור', v['link'], '· לא נכנסו', v['miss'])
    print('נבחר:', pick, '· יעד', target)
    print('צי (שיא קבוע / מינימום גמיש / צריך / היום / הישן):', {k: (v['peak'], v['kmin'], v['need'], v['today_spots'], v['old']) for k, v in fleet.items()})
    for h in out['halls']: print('כבודה', h)
    print('נוסעים:', out['pax']['gates'], 'בסבב (נומינלי / מצויר):', out['pax']['nominal_cycle'], out['pax']['visual_cycle'])
    print('צוות:', out['crew'])
    print('מרווחים:', out['clear']['checks'], 'בדיקות ·', out['clear']['fails'], 'כישלונות')
    for r in out['clear']['list']:
        if not r['ok']: print('  ✗', r['id'], r['det'])
    print('בדיקה עצמית (פריסה שגויה בכוונה — חייבת להיכשל):', out['selftest'])
    ok = out['clear']['ok'] and scen[pick]['rwy']['per1800'] >= target and out['selftest']['fails'] > 0
    print('תוצאה:', 'עובר' if ok else 'נכשל')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(run())
