# -*- coding: utf-8 -*-
# ft2_ch.py — fieldthru2: המדידה של CH (C1 + C2 יחד) למשא הענק AC-HC-01 — אותן בדיקות של fieldcalc (fc_stands.py:check — המעטפת, הכיסים, דרכי השירות,
# הכנפיים מול השכנים) על הגאומטריה של fc_calc.py; בלי לכתוב על stands_matrix.json של fieldcalc — הפלט: ch_matrix.json (שורה ל-CH, באותו מבנה)
import os, sys, json, importlib.util, io, contextlib
FCD = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldcalc/tools'
spec = importlib.util.spec_from_file_location('fc', os.path.join(FCD, 'fc_calc.py')); FC = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(FC)
sys.argv = _a
D = FC.D; ST = FC.ST; DIM = FC.DIM; AC = FC.AC
ROADS = [(q['id'], q['rect']) for q in D['service']]
def foot(cx, m, ny): L, W = DIM[m]; return [cx - W / 2, ny - L, cx + W / 2, ny]
def shape(cx, m, ny):
    L, W = DIM[m]; fw = max(20, .12 * W); wc = ny - .45 * L; ch = .18 * L
    return [[cx - fw / 2, ny - L, cx + fw / 2, ny], [cx - W / 2, wc - ch / 2, cx + W / 2, wc + ch / 2], [cx - .19 * W, ny - L, cx + .19 * W, ny - .88 * L]]
def check(rect, cx, m, ny, skip):
    why = []; f = foot(cx, m, ny)
    if not FC.inside(f, [rect[0] - 1, rect[1] - 1, rect[2] + 1, rect[3] + 1]): why.append('מחוץ למלבן %s' % [round(v) for v in f])
    sh = shape(cx, m, ny)
    for pk, pr in D['pockets'].items():
        if any(FC.rint(pr, q) for q in sh): why.append('כיס ' + pk.replace('AIR-GSE-', ''))
    for rid, rr in ROADS:
        if any(FC.rint(rr, q) for q in sh): why.append('דרך ' + rid.replace('AIR-', ''))
    for s2, q in ST.items():
        if s2 in skip: continue
        m2 = q.get('type')
        if not m2 or m2 not in DIM: continue
        g = FC.rgap(f, foot(q['cx'], m2, q['nose']))
        if g < 30: why.append('כנף מול %s %.1f מ׳' % (s2, g / 10))
    return why
m = 'AC-HC-01'; out = {}
q = ST['CH']; print('CH', q['rect'], 'cx', q['cx'], 'nose', q['nose'], 'HC', DIM[m], 'APRON', D.get('apron'))
for name, rect in (('CH — המלבן של היום', q['rect']), ('CH — עד קצה הרחבה (y 1033, ‏D.FENCE)', [q['rect'][0], q['rect'][1], q['rect'][2], 1033]), ('CH — עד הגדר של המשחק היום (019m:S15_POLY — y 725)', [q['rect'][0], -55, q['rect'][2], 725])):
    for cx in (q['cx'], 5250, (4810 + 5690) / 2):
        best = None
        for ny in range(int(rect[3]), 600, -5):
            w = check(rect, cx, m, ny, {'CH', 'C1', 'C2'})
            if not w: best = ny; break
        out[name + ' cx %d' % cx] = dict(ok=best is not None, ny=best, why=check(rect, cx, m, q['nose'], {'CH', 'C1', 'C2'}))
        print(name, 'cx', cx, '→', ('נכנס, האף ב-y %d' % best) if best else 'לא נכנס', '· באף של העמדה (940):', check(rect, cx, m, q['nose'], {'CH', 'C1', 'C2'}))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ch_matrix.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# הזנב מול A: מטוס על A (y ‏−170) — חצי מוטה של הגדול (LG ‏648) מגיע עד y 154; הזנב של HC כשהאף ב-y:
for ny in (940, 715):
    print('HC עם האף ב-y %d — הזנב ב-y %d · הכנף של LG על A מגיעה עד y %d · של צר-גוף עד y %d' % (ny, ny - DIM[m][0], -170 + DIM['AC-LG-01'][1] / 2, -170 + DIM['AC-NB-01'][1] / 2))
