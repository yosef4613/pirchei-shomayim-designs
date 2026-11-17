#!/usr/bin/env python3
# fs_need.py — fieldsvc 17.11: טבלת "צריך" — לכל סוג מטוס × כל עמדה שהוא יכול לחנות בה: אילו שירותים נדרשים (ואילו לא, ולמה).
# העמדות: stands_matrix.json של fieldcalc (נכנס / לא) ∩ המדיניות לפי גודל (הבעלים 14:35: "פרטי לא יהיה ב-P1–6").
# השירותים: המטריצה של fieldcalc (074zq:NEED) לפי מצב העמדה — שרוול / מרוחקת / GA / משא — ועוד אמבוליפט לפי אחוז הנוסעים.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); FC = os.path.join(HERE, '../../fieldcalc/tools')
SMX = json.load(open(os.path.join(FC, 'stands_matrix.json')))
PAX = {'AC-NB-01':146,'AC-LG-01':320,'AC-MW-01':240,'AC-RJ-01':61,'AC-QJ-01':80,'AC-TP-01':56,'AC-BJ-01':7,'AC-CN-01':4,'AC-LT-01':4,'AC-PR-01':2,'AC-AM-01':2,'AC-TB-01':0,'AC-CG-01':0,'AC-HC-01':0}
PRM = .01
# המדיניות: איפה כל סוג חונה (מתוך מה שנכנס) — הגדולים בגדולות, נוסעים לא במשא, פרטי / מנהלים לא ב-P
POLICY = {'AC-LG-01':['P1','P6'],'AC-MW-01':['P1','P6'],'AC-NB-01':['P1','P2','P3','P4','P5','P6','R2'],'AC-QJ-01':['P1','P2','P3','P4','P5','P6','R2'],
 'AC-RJ-01':['P1','P2','P3','P4','P5','P6','R1','R2','R3'],'AC-TP-01':['P1','P2','P3','P4','P5','P6','R1','R2','R3'],'AC-CG-01':['C1'],'AC-HC-01':['C1+C2'],'AC-TB-01':['C1','C2'],
 'AC-BJ-01':['GA1','R1','R3'],'AC-CN-01':['GA1','R1','R3'],'AC-LT-01':['GA1','GA2','GA3','GA4','GA5','GA6','GA7'],'AC-PR-01':['GA1','GA2','GA3','GA4','GA5','GA6','GA7'],'AC-AM-01':[]}
NEED = {'AC-NB-01':['PT','BT','BL','FT','CT','SVC','r:GP','r:MS','r:AB'],'AC-LG-01':['PT','BT','BT','BL','BL','FT','CT','CT','SVC','r:GP','r:MS','r:MS','r:AB','r:AB'],'AC-MW-01':['PT','BT','BT','BL','BL','FT','CT','CT','SVC','r:GP','r:MS','r:MS','r:AB','r:AB'],
 'AC-RJ-01':['PT','BT','FT','CT','SVC','r:GP','r:MS','r:AB'],'AC-QJ-01':['PT','BT','FT','CT','SVC','r:GP','r:MS','r:AB'],'AC-TP-01':['PT','BT','FT','CT','SVC','r:GP','r:AB'],
 'AC-CG-01':['PT','GP','FT','HL','TG'],'AC-HC-01':['PT','GP','GP','FT','FT','HL','HL','TG','TG'],'AC-TB-01':['PT','GP','FT','HL|BL','TG'],
 'AC-BJ-01':['PT','FT','GP','CT','SVC'],'AC-CN-01':['PT','FT','GP','CT','SVC'],'AC-LT-01':['PT','FT'],'AC-PR-01':['PT','FT']}
WL = {'AC-NB-01','AC-LG-01','AC-MW-01','AC-RJ-01','AC-QJ-01','AC-TP-01','AC-BJ-01','AC-CN-01'}   # מים ושירותים — לפי אורך הטיסה (≥ 60% מכל סוג)
SMALLCAT = {'AC-BJ-01','AC-CN-01','AC-RJ-01','AC-TP-01'}   # קייטרינג קטן
OPT = ['SH', 'SV']   # מותר ולא חובה: הסעת צוות, "עקוב אחריי"
HE = dict(PT='גרר',BT='רכבת כבודה',BL='מסוע',FT='דלק',CT='קייטרינג',WT='מים',LV='שירותים',SVC='ניקיון',GP='חשמל קרקע',MS='מדרגות',AB='אוטובוס',AL='אמבוליפט',HL='מעמיס מכולות',TG='גרר מכולות')
def mode(model, stand):
    if stand.startswith('C'): return 'cargo'   # גם 'C1+C2' — המשא הענק על שתי עמדות (fieldthru2)
    if stand.startswith('GA'): return 'ga'
    if stand.startswith('P'):
        r = SMX['stands'][stand]['row'].get(model, {})
        return 'bridge' if r.get('bridge') is not False else 'remote'
    return 'remote'
def need(model, stand, short=False):
    m = mode(model, stand); rem = m == 'remote'
    n = [x.replace('r:', '') for x in NEED.get(model, []) if not x.startswith('r:') or rem]
    if model in WL and not short: n += ['WT', 'LV']
    if model in ('AC-BJ-01', 'AC-CN-01'): pass                       # מנהלים: מדרגות מובנות, לימוזינה — בלי MS / AB גם ב-R
    if rem and PAX.get(model, 0) * PRM >= .5: n.append('AL')
    return m, n
WHY_NOT = {'bridge': 'שרוול: בלי מדרגות, בלי אוטובוס, בלי חשמל קרקע (400 הרץ מהשרוול), כיסא גלגלים בשרוול', 'remote': 'מרוחקת: מדרגות (חוץ ממדרגות מובנות), אוטובוס, חשמל קרקע, אמבוליפט לפי נוסעים',
           'ga': 'GA: ברגל / לימוזינה; בלי כבודה ברכבת, בלי אוטובוס', 'cargo': 'משא: בלי נוסעים — בלי קייטרינג, מים, שירותים, ניקיון, מדרגות, אוטובוס'}
def table():
    rows = []
    for t in SMX['types']:
        m = t['m']; fits = [s for s, d in SMX['stands'].items() if d['row'].get(m, {}).get('ok')]
        pol = POLICY.get(m, []); cells = []
        for s in pol:
            if s not in fits and '+' not in s: continue
            md, n = need(m, s); cells.append(dict(stand=s, mode=md, need=n))
        rows.append(dict(m=m, code=t['code'], he=t['he'], size=t['size'], seats=t['seats'], fits=fits, policy=[c['stand'] for c in cells], not_policy=[s for s in fits if s not in pol], cells=cells))
    return rows
if __name__ == '__main__':
    R = table(); json.dump(R, open(os.path.join(HERE, 'need_table.json'), 'w'), ensure_ascii=False, indent=0)
    for r in R:
        print(r['code'], r['size'], 'חונה:', ' '.join(r['policy']) or '—', '| נכנס אבל לא לפי המדיניות:', ' '.join(r['not_policy']) or '—')
        seen = {}
        for c in r['cells']: seen.setdefault((c['mode'], ' '.join(c['need'])), []).append(c['stand'])
        for (md, n), ss in seen.items(): print('   ', md, '/'.join(ss), ':', n)
