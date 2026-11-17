# -*- coding: utf-8 -*-
# ft2_gen.py <dump.json> <base.json> <out.json> <סדר העמדות> — fieldthru2: ההרצה של ft_gen.py של fieldthru (כלל 19א — אותו מחולל), עם "מה אם" לגאומטריה (לאישור הבעלים):
#   FT2_B2=<x>      — מסלול הסעה שני לדרום לקלים (B2, לאורך הגדר המזרחית — ההצעה של fieldcalc, fc_calc2.py): ההסעה של עמדות ה-GA ב-x הזה במקום B (TBCX)
#   FT2_NOR3NIGHT=1 — R3 פנויה ביום (הרצת המנועים בלילה עוברת למקום אחר — fieldfix): בלי המטוס של הלילה כמכשול קבוע
import sys, os, math
sys.path.insert(0, '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ft_sim as F
if os.environ.get('FT2_D701'):
    import ft2_sim   # D‑701: ‏A3 החדש + המראה הפוכה
if os.environ.get('FT2_NOR3NIGHT'):
    F.r3_night = lambda M3: []
B2 = float(os.environ.get('FT2_B2', 0) or 0)
if B2:
    _d1, _at = F.dep1, F.arr1_taxi
    def _with_b2(fn):
        def w(*a, **k):
            sid = a[0] if fn is _d1 else a[1]
            if not str(sid).startswith('GA'): return fn(*a, **k)
            keep = F.TBCX; F.TBCX = B2
            try: return fn(*a, **k)
            finally: F.TBCX = keep
        return w
    F.dep1 = _with_b2(_d1); F.arr1_taxi = _with_b2(_at)
# P1 / P6 — הגרר נוסע בשורה y 989 לכל סוג (בשורה 864 הוא עובר מתחת לאף של סוג קטן — FL-P6 × PT-P6 ב-try8084)
import inspect as _ins
_src = _ins.getsource(F.tug_trip).replace("big = a.L > 600", "big = a.L > 600 or sid in ('P1', 'P6')"); exec(compile(_src, F.__file__, 'exec'), F.__dict__)
GEN = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools/ft_gen.py'
sys.argv = [GEN] + sys.argv[1:]
exec(compile(open(GEN, encoding='utf-8').read(), GEN, 'exec'), {'__name__': '__main__', '__file__': GEN})
