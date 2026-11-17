#!/usr/bin/env python3
# fc_stands.py — fieldcalc 17.11 11:10 (הבעלים: "ציור ברור של כל העמדות וכמה סוגי מטוסים יכולים לחנות בכל עמדה"):
# לכל עמדה × כל סוג — נכנס / לא נכנס והסיבה, בעצירה של העמדה ובקווי עצירה לפי סוג (כמו בשדה אמיתי: קו עצירה לכל משפחה),
# השירות (שרוול / מדרגות + אוטובוס / הליכה / לימוזינה / מטען), הדחיפה, ומי בלוח היום (S15SIM + fieldfix + fieldthru, res_try7406).
# הבדיקה מחושבת (לא ok=true קבוע): המעטפת בתוך העמדה, לא על דרך שירות, בלי כיס ציוד מתחת לגוף / לכנף / לזנב, ‏3 מ׳ (קלים — 2) מקצה הכנף של השכנים
# כשהם בסוג שלהם (S15D.stands.type), והשרוול — מהמדידה במשחק (q_bridges, רק בעצירה של העמדה). הפלט: stands_matrix.json; הדף — fc_stands_page.py.
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('fc', os.path.join(HERE, 'fc_calc.py')); FC = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(FC)
sys.argv = _a
D = FC.D; ST = FC.ST; DIM = FC.DIM; AC = FC.AC
BR = json.load(open(os.path.join(HERE, '..', 'qa', 'bridges_try6649.json'), encoding='utf-8'))
BRS = {r['stand'] for r in BR['rows']}
TYPES = [m for m in ['AC-PR-01', 'AC-LT-01', 'AC-BJ-01', 'AC-CN-01', 'AC-AM-01', 'AC-TB-01', 'AC-TP-01', 'AC-RJ-01', 'AC-QJ-01', 'AC-NB-01', 'AC-MW-01', 'AC-CG-01', 'AC-LG-01', 'AC-HC-01'] if m in DIM]
NAME = {'AC-PR-01': 'פרטי קטן (מדחף)', 'AC-LT-01': 'פרטי דו-מנועי', 'AC-BJ-01': 'מנהלים — סילון', 'AC-CN-01': 'מנהלים — קנרד', 'AC-AM-01': 'אמפיבי', 'AC-TB-01': 'מטען קטן (זנב כפול)',
        'AC-TP-01': 'טורבו-פרופ אזורי', 'AC-RJ-01': 'סילון אזורי', 'AC-QJ-01': 'אזורי 4 מנועים', 'AC-NB-01': 'צר-גוף', 'AC-MW-01': 'רחב-גוף 3 מנועים', 'AC-CG-01': 'מטען סילון',
        'AC-LG-01': 'נוסעים גדול', 'AC-HC-01': 'מטען כבד'}
def size(m):
    w = DIM[m][1] / FC.PXM
    return 'S' if w < 20 else 'M' if w < 40 else 'L' if w < 60 else 'XL'
def shape_at(s, m, ny):
    cx = ST[s]['cx']; L, Wd = DIM[m]; ga = AC[m]['cls'] in ('GA', 'EXEC', 'AMPH'); fw = max(20, .12 * Wd)
    wc = ny - (.35 if ga else .45) * L; ch = (.15 if ga else .18) * L
    return [[cx - fw / 2, ny - L, cx + fw / 2, ny], [cx - Wd / 2, wc - ch / 2, cx + Wd / 2, wc + ch / 2], [cx - .19 * Wd, ny - L, cx + .19 * Wd, ny - .88 * L]]
def foot_at(s, m, ny):
    cx = ST[s]['cx']; L, Wd = DIM[m]; return [cx - Wd / 2, ny - L, cx + Wd / 2, ny]
ROADS = [(q['id'], q['rect']) for q in D['service']]
DESIGN = {s: ST[s].get('type') for s in ST}
# הלוח היום: S15SIM (019l) + FL-GA1 (fieldfix, ‏074zp_ff_flights) + FL-C2 (074p) + הטיסות החדשות של fieldthru (res_try7406 — 13 טיסות במחזור)
USE = {}
B = json.load(open(os.path.join(HERE, 's15_base.json'), encoding='utf-8'))['S15SIM']
for f in B['flights']: USE.setdefault(f['home'], []).append((f['model'], 'S15SIM'))
USE.setdefault('GA1', []).append(('AC-BJ-01', 'fieldfix')); USE.setdefault('C2', []).append(('AC-TB-01', '074p'))
try:
    FT = json.load(open(os.path.join(HERE, '..', '..', 'fieldthru', 'tools', 'res_try7406.json'), encoding='utf-8'))
    for q in FT['sched']: USE.setdefault(q[0], []).append((q[1], 'fieldthru'))
except Exception as e: FT = None
def neighbors(s):
    r = ST[s]['rect']; out = []
    for s2, q in ST.items():
        if s2 == s or s2 == 'CH' or (s == 'CH' and s2 in ('C1', 'C2')) or (s in ('C1', 'C2') and s2 == 'CH'): continue
        r2 = q['rect']
        if r2[0] <= r[2] + 400 and r[0] <= r2[2] + 400 and r2[1] <= r[3] + 400 and r[1] <= r2[3] + 400: out.append(s2)
    return out
def check(s, m, ny):
    why = []; r = ST[s]['rect']; f = foot_at(s, m, ny)
    if not FC.inside(f, [r[0] - 1, r[1] - 1, r[2] + 1, r[3] + 1]): why.append('לא נכנס במלבן של העמדה')
    sh = shape_at(s, m, ny)
    for pk, pr in D['pockets'].items():
        if any(FC.rint(pr, q) for q in sh): why.append('כיס הציוד ' + pk.replace('AIR-GSE-', '') + ' מתחת למטוס')
    for rid, rr in ROADS:
        if any(FC.rint(rr, q) for q in sh):
            xm = [x for x in D['xmarks'] if x['id'].endswith('-' + s) and x['id'].startswith('XM-' + rid.replace('AIR-', '')) and any(FC.rint(x['rect'], q) for q in sh)]
            if not xm: why.append('על ' + rid.replace('AIR-', '') + ' (דרך שירות)')   # חצייה מסומנת של הדרך דרך העמדה (XM-…-<עמדה>) — מותרת: הרכב מחכה
    for s2 in neighbors(s):
        m2 = DESIGN.get(s2)
        if not m2 or m2 not in DIM: continue
        need = 30 if (AC[m]['cls'] not in ('GA', 'EXEC') or AC[m2]['cls'] not in ('GA', 'EXEC')) else 20
        g = FC.rgap(f, foot_at(s2, m2, ST[s2]['nose']))
        if g < need: why.append('כנף מול %s (%s): %.1f מ׳' % (s2, m2[3:5], g / 10))
    return why
def bridge_ok(s, m):
    b = next((q for q in BR['rows'] if q['stand'] == s and q['ac'] == m), None)
    return None if b is None else bool(b.get('ok'))
def service(s, m, shift, br):
    c = AC[m]['cls']
    if c == 'CARGO': return 'מטען: מעמיס + עגלות (HL / TG) או מסוע'
    if s.startswith('P'):
        if c in ('GA', 'EXEC', 'AMPH'): return 'הליכה (נוסעים מעטים)'
        if br and not shift: return 'שרוול'
        if m == 'AC-TP-01': return 'הליכה / מדרגות (D‑106)'
        return 'מדרגות + אוטובוס (השרוול לא מגיע בעצירה הזו)'
    if c == 'EXEC': return 'לימוזינה עד המטוס'
    if c in ('GA', 'AMPH'): return 'הליכה לטרקלין ה-GA'
    return 'מדרגות + אוטובוס רחבה'
OUT = dict(types=[dict(m=m, code=m[3:5], he=NAME.get(m, m), L=DIM[m][0] / 10, W=DIM[m][1] / 10, size=size(m), cls=AC[m]['cls'], seats=AC[m].get('seats')) for m in TYPES], stands={})
for s in ST:
    q = ST[s]; row = {}
    for m in TYPES:
        why0 = check(s, m, q['nose'])
        br = bridge_ok(s, m) if s in BRS else None
        if s in BRS and br is False and not why0 and AC[m]['cls'] not in ('GA', 'EXEC', 'AMPH', 'CARGO') and m != 'AC-TP-01': why0 = why0 + ['השרוול לא עוגן (q_bridges)']
        res = dict(ok=not why0, shift=0, why=why0)
        if why0:
            # קו עצירה לפי סוג: מזיזים את המטוס אחורה (צפונה — הרחק מהחזית של העמדה) ב-10 פיקס׳, עד שהכול פנוי
            for k in range(1, 60):
                ny = q['nose'] - 10 * k
                w2 = check(s, m, ny)
                if not w2: res = dict(ok=True, shift=10 * k, why=why0, stop=ny); break
                if any('לא נכנס' in w for w in w2): break
        res['service'] = service(s, m, res.get('shift', 0), br) if res['ok'] else ''
        res['bridge'] = br
        row[m] = res
    OUT['stands'][s] = dict(rect=q['rect'], cx=q['cx'], nose=q['nose'], design=q.get('type'), parked=D['parked'].get(s), zone=q.get('zone'),
                            use=USE.get(s, []), row=row, n_ok=sum(1 for m in TYPES if row[m]['ok']), n_now=sum(1 for m in TYPES if row[m]['ok'] and not row[m]['shift']),
                            sizes=sorted({size(m) for m in TYPES if row[m]['ok']}, key=lambda z: ['S', 'M', 'L', 'XL'].index(z)))
OUT['hangars'] = [dict(id=b['id'], label=b['label'], rect=b['rect']) for b in D['base'] if b['id'] in ('AIR-BASE-1', 'AIR-BASE-2', 'AIR-BASE-3')]
OUT['helipads'] = [dict(id=h['id'], c=h['c'], pad=h.get('pad')) for h in D['helipads']]
# בדיקה עצמית: מטוס נוסעים גדול ב-GA3 חייב להיכשל, וצר-גוף ב-P3 בעצירה של העמדה — לעבור
st_ok = (not OUT['stands']['GA3']['row']['AC-LG-01']['ok']) and OUT['stands']['P3']['row']['AC-NB-01']['ok'] and not OUT['stands']['P3']['row']['AC-NB-01']['shift']
OUT['selftest'] = st_ok
json.dump(OUT, open(os.path.join(HERE, 'stands_matrix.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for s, q in OUT['stands'].items():
    print(s, 'עכשיו', q['n_now'], 'עם קו עצירה', q['n_ok'], [m[3:5] + ('*' if q['row'][m]['shift'] else '') for m in TYPES if q['row'][m]['ok']], 'בלוח:', [u[0][3:5] for u in q['use']])
print('בדיקה עצמית:', st_ok)
sys.exit(0 if st_ok else 1)
