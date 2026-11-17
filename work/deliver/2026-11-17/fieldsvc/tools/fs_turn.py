#!/usr/bin/env python3
# fs_turn.py — fieldsvc 17.11: סבב הקרקע לכל סוג מטוס (השירותים, הסדר, הזמנים, המקום ליד המטוס) + כמה רכבים צריך לכל לו״ז.
# המקורות: הזמנים של המנוע הישן (042:g77SvcPlan — מים 24 / שירותים 34 / ניקיון 12+הליכה / קייטרינג 20+ / חשמל 4 / מסוע 6 / מעמיס 8;
# 050:G77_AMB — אמבוליפט after 6 / before 24, הרמה 6, מעבר 9), מטריצת השירות של fieldcalc (fc_calc.py:svc_matrix + 074zq:NEED), זמני העמידה (fieldcalc).
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.abspath(os.path.join(HERE, '../../../..'))
FC = os.path.join(W, 'deliver/2026-11-17/fieldcalc/tools')

# הקטגוריות של הבעלים → הסוג המייצג, זמן עמידה (fieldcalc), נוסעים (מושבים × תפוסה), העמדות
CATS = [
 dict(k='giant', he='ענק', ac='AC-LG-01', also='AC-MW-01', D=470, pax=320, stands='P1 / P6 — שני שרוולים', bridge=True, remote=False),
 dict(k='large', he='גדול', ac='AC-NB-01', also='', D=400, pax=146, stands='P2–P5 — שרוול; R2 — מרוחקת (מדרגות + אוטובוס)', bridge=True, remote=True),
 dict(k='medium', he='בינוני', ac='AC-RJ-01', also='AC-QJ-01', D=340, pax=61, stands='P4 / P5 — שרוול; P6 / R1 / R3 בקו עצירה — מרוחקת', bridge=True, remote=True),
 dict(k='small', he='קטן', ac='AC-TP-01', also='AC-TB-01 (משא קטן)', D=340, pax=56, stands='R1 / R3 / P4 — מדרגות מובנות', bridge=False, remote=True),
 dict(k='exec', he='מנהלים', ac='AC-BJ-01', also='AC-CN-01', D=250, pax=7, stands='GA1 / R1 / R3 (ביום)', bridge=False, remote=False, ga=True),
 dict(k='private', he='פרטי', ac='AC-LT-01', also='AC-PR-01', D=175, pax=4, stands='GA2–GA7', bridge=False, remote=False, ga=True),
 dict(k='cargo', he='מטען', ac='AC-TB-01', also='AC-CG-01; המשא הענק HC — על שתי עמדות, הכול כפול (מעמיס בדלת הצד ובאף)', D=440, pax=0, stands='C1 / C2', bridge=False, remote=False, cargo=True),
 dict(k='heli', he='מסוק', ac='AC-HL-06', also='', D=120, pax=5, stands='H1–H3 (המנחתים)', bridge=False, remote=False, heli=True),
]
PRM = 0.01   # שיעור הנוסעים בכיסא גלגלים (הנחה — לאישורך): 1 ל-100 נוסעים; אמבוליפט כשהצפי ≥ 0.5 ובעמדה בלי שרוול

# השירות: קוד, שם, (התחלה, משך) יחסית ל-on-block לפי D; איפה ליד המטוס; מה רואים (המצייר הישן / של S15)
def services(c, remote):
    D = c['D']; ac = c['ac']; out = []
    add = lambda code, he, t0, d, where, see, src, n=1: out.append(dict(code=code, he=he, t0=round(t0), d=round(d), where=where, see=see, src=src, n=n))
    if c.get('heli'):
        add('SV', 'מכוון', -15, 25, 'מול המנחת', 'מכוון עם מקלות; המסוק נוחת', '074q_S15e_marshal')
        add('FTs', 'מתדלק קטן', 20, 40, 'בצד המנחת', 'צינור אל פתח הדלק, קונוסים, מונה', '046:S6A_ACTS.fuel')
        return out
    add('SV', 'מכוון + סדים', -20, 30, 'מול האף; סדים בגלגל האף', 'מכוון עם מקלות מוביל לקו העצירה, שם סד וקונוסים', '074q_S15e_marshal (045:g77MarshalSpot)')
    if c.get('ga'):
        add('PT', 'גרר קטן', D - 7, 47, 'מול האף, מוט לגלגל האף', 'מוט הגרירה מתחבר, דחיפה לאחור לקו C', '074p:s15iTugAttach + 046 (D‑83)')
        add('FT', 'דלק' if c['k'] == 'exec' else 'מתדלק קטן', 40, 50 if c['k'] == 'exec' else 40, 'מתחת לכנף, בצד השירות', 'צינור מהגלגלת לצימוד בכנף, זרימה, מונה, קונוסים וכבל הארקה', '046:S6A_ACTS.fuel + s6rFuelSafety')
        if c['k'] == 'exec':
            add('GP', 'חשמל קרקע', 4, D - 54, 'מול האף, ימין', 'כבל לשקע שמתחת לאף, נורה ירוקה', '046:S6A_ACTS.gpu')
            add('CT', 'קייטרינג', 60, 60, 'הדלת הימנית', 'הארגז עולה על המספריים, הבמה לדלת, עגלה עוברת', '046:S6A_ACTS.cat / 074o')
            add('LV', 'שירותים', 30, 30, 'הלוח האחורי, ימין', 'צינור חום מהלוח למשאית, מכסה פתוח', '046:S6A_ACTS.lav')
            add('SVC', 'ניקיון', 25, 60, 'ליד הדלת', 'מנקים נכנסים עם שקיות ויוצאים', '046:s6rCleaner / 074o')
        return out
    if c.get('cargo'):
        add('GP', 'חשמל קרקע', 4, D - 54, 'מול האף', 'כבל לשקע, נורה ירוקה', '046:S6A_ACTS.gpu')
        add('HL', 'מעמיס מכולות', 8, min(300, D - 48), 'דלת המטען', 'הבמה עולה לגובה הדלת, מכולה עוברת', '046:S6A_ACTS.hl')
        add('TG', 'גרר עגלות מכולות', 20, 45, 'ליד המעמיס', 'עגלות עם מכולות מגיעות ויוצאות', '074k:s15grCarts', n=2)
        add('FT', 'דלק', 100, 70 if ac == 'AC-TB-01' else 140, 'מתחת לכנף', 'צינור לצימוד, זרימה, מונה, קונוסים', '046:S6A_ACTS.fuel')
        add('PT', 'גרר', D - 7, 82, 'מול האף', 'מוט לגלגל האף, דחיפה', '074p')
        return out
    wide = c['k'] == 'giant'; hand = c['k'] in ('medium', 'small'); br = c['bridge'] and not remote
    if br:
        add('BR', 'שרוול' + (' ×2' if wide else ''), 8, D - 28, 'הדלת השמאלית הקדמית (L1' + (' + L2' if wide else '') + ')', 'השרוול נפתח, נצמד לדלת; נוסעים יוצאים ונכנסים', '074k:s15grBrPose (047:g77K72Parts)')
        add('PW', 'חשמל 400 הרץ מהשרוול', 12, D - 32, 'מתא השרוול לשקע שמתחת לאף', 'כבל שחור, נורה ירוקה', '074n:s15gPower (047:s6rPowerDraw)')
        add('WC', 'כיסא גלגלים בשרוול', 20, 20, 'בשרוול', 'מלווה דוחף כיסא גלגלים בשרוול (בלי רכב)', 'חדש — fieldsvc')
    else:
        add('GP', 'חשמל קרקע', 4, D - 54, 'מול האף, ימין', 'כבל לשקע שמתחת לאף, נורה ירוקה', '046:S6A_ACTS.gpu')
        if c['k'] != 'small':
            add('MS', 'מדרגות' + (' ×2' if c['k'] in ('large', 'giant') else ''), 4, D - 12, 'הדלת השמאלית הקדמית' + (' + האחורית' if c['k'] in ('large', 'giant') else ''), 'המדרגות נצמדות לדלת; נוסעים עולים ויורדים על הגרם', '074r2_S15p_stairs', n=2 if c['k'] in ('large', 'giant') else 1)
        add('AB', 'אוטובוס (הגעה)', 8, 55, 'ליד המדרגות, שמאל', 'הנוסעים יורדים במדרגות ועולים לאוטובוס', '074o:s15w4RemPatch')
        add('AB', 'אוטובוס (יציאה)', D - 120, 60, 'ליד המדרגות, שמאל', 'האוטובוס מגיע מהשער, הנוסעים עולים במדרגות', '074o:s15w4RemPatch')
        if c['pax'] * PRM >= .5:
            add('AL', 'אמבוליפט (כיסא גלגלים)', 70, 36, 'הדלת הימנית הקדמית (R1)', 'הארגז עולה, הבמה לדלת; נוסע בכיסא גלגלים יורד עם מלווה, ואחר כך נוסע יוצא עולה', '050:G77_AMB / g77AmbDraw / g77DrawChair')
    if hand:
        add('BT', 'רכבת כבודה (ביד)', 20, 120, 'מתחת לבטן, ימין', 'העגלות ליד הבטן, המעמיסים מעבירים מזוודות ביד', '074p:s15iCrew')
    else:
        add('BL', 'מסוע' + (' ×2' if wide else ''), 6, D - 22, 'דלת הבטן הקדמית' + (' + האחורית' if wide else ''), 'הסרט נע, מזוודות עולות ויורדות, עובד למעלה', '074r2_S15bag_belt (052:G77_BX)', n=2 if wide else 1)
        add('BT', 'רכבת כבודה — פריקה', 20, 110 if not wide else 150, 'ליד המסוע', 'העגלות מתמלאות מהמסוע', '074p / 074zt_fc_bags', n=2 if wide else 1)
        add('BT', 'רכבת כבודה — העמסה', D - 170 if not wide else D - 210, 140 if not wide else 180, 'ליד המסוע', 'המזוודות עולות על הסרט לבטן', '074p / 074zt_fc_bags', n=2 if wide else 1)
    add('SVC', 'ניקיון', 12 + 8 + 30, min(120, max(40, 30 + c['pax'] * .3)), 'הדלת הימנית / המדרגות', 'מנקים עולים עם שקיות, יוצאים עם שקיות מלאות', '046:s6rCleaner / 074o')
    if c['ac'] != 'AC-TP-01':
        add('WT', 'מים', 24, 30, 'הלוח האחורי, ימין (as−21)', 'מכסה הלוח נפתח, צינור כחול, זרימה', '046:S6A_ACTS.water')
    add('LV', 'שירותים', 58, 30, 'הלוח האחורי, ימין (as−70)', 'צינור חום, הזרימה אל המשאית', '046:S6A_ACTS.lav')
    add('CT', 'קייטרינג' + (' ×2' if wide else ''), 30, 260 if wide else (130 if c['k'] == 'large' else 100), 'דלת המטבח האחורית, ימין, בניצב לגוף', 'הארגז עולה על המספריים, הבמה לדלת, עגלות עוברות', '046:S6A_ACTS.cat / 074o:s15w4CatDraw', n=2 if wide else 1)
    add('FT', 'דלק', 100, 140 if wide else 70, 'מתחת לכנף הימנית (אמצע הכנף)', 'קונוסים, כבל הארקה, צינור לצימוד, זרימה צהובה, המונה מתמלא', '046:S6A_ACTS.fuel / 074n')
    add('PT', 'גרר', D - 7, 82, 'מול האף, מוט לגלגל האף', 'המוט מתחבר, הסדים יוצאים, דחיפה לאחור', '074p:s15iTugAttach')
    return out

TRANSIT = dict(FT=75, AL=80, GP=45, CT=45, WT=45, LV=45, SVC=45, BT=60, BL=40, MS=30, AB=70, PT=40, HL=40, TG=50, SV=30, FTs=50)
CODES_VEH = ['PT', 'FT', 'FTs', 'CT', 'WT', 'LV', 'SVC', 'GP', 'BT', 'BL', 'MS', 'AB', 'AL', 'HL', 'TG']
def cat_of(model, stand):
    for c in CATS:
        if model in (c['ac'],) or model in str(c['also']).split(' '): 
            if c['k'] == 'small' and model == 'AC-TB-01' and stand.startswith('C'): continue
            return c
    m = {'AC-MW-01': 'giant', 'AC-QJ-01': 'medium', 'AC-CN-01': 'exec', 'AC-PR-01': 'private', 'AC-CG-01': 'cargo', 'AC-HC-01': 'cargo', 'AC-TB-01': 'cargo'}
    return next(c for c in CATS if c['k'] == m.get(model, 'large'))

def fleet(sched, T=720):
    """sched: [(stand, model, onblock)] → לכל קוד: ביקורים, זמן עסוק, שיא בו-זמני (מעגלי), כמה צריך (+עתודה כשניצול רכב > 80%)"""
    occ = {}
    for st, model, ob in sched:
        c = cat_of(model, st); remote = st[0] in 'RC' and not c.get('cargo') or (st == 'P6' and model in ('AC-RJ-01', 'AC-NB-01'))
        for s in services(c, remote):
            code = s['code']
            if code not in CODES_VEH: continue
            if code == 'FT' and c.get('ga') and c['k'] == 'private': code = 'FTs'
            a = ob + s['t0'] - TRANSIT.get(code, 40); b = ob + s['t0'] + s['d'] + TRANSIT.get(code, 40)
            for k in range(s['n']): occ.setdefault(code, []).append((a % T, (b - a)))
    out = {}
    for code, L in occ.items():
        peak = 0
        for t in range(0, T, 2):
            n = sum(1 for a, d in L if ((t - a) % T) < d)
            peak = max(peak, n)
        busy = sum(d for a, d in L)
        need = peak + (1 if busy / max(1, peak) > .8 * T else 0)
        out[code] = dict(visits=len(L), busy=round(busy), util=round(100 * busy / T / max(1, peak)), peak=peak, need=need)
    return out

if __name__ == '__main__':
    fc = json.load(open(os.path.join(FC, 'fc_result.json')))
    S18 = [(s['stand'], s['model'], s['onblock']) for s in fc['schedule']]
    print(json.dumps(fleet(S18), ensure_ascii=False))
