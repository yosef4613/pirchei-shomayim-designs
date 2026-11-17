#!/usr/bin/env python3
# build_lab.py <src_game_dir> <out.html> — closezoom 17.11: דף הניסוי (לא נוגע במשחק). הקוד של המשחק עצמו, בלי עותק ידני:
#   צייר האנשים P34 (065:p34LibInit → 066:207, כולל הוו P34X.face), הדיוקן (074zp — POR-CORE), והחלק שלי (074zz5 — CZ-CORE).
# הכול ציור בקוד (קנבס + SVG), בלי תמונות טעונות (כלל 17).
import sys, os, re
src, out = sys.argv[1], sys.argv[2]
P = lambda n: open(os.path.join(src, 'parts', n), encoding='utf-8').read()
a = P('065_core_p378.js').split('\n'); b = P('066_D0_p670.js').split('\n')
i0 = next(i for i, l in enumerate(a) if l.startswith('(function (G) {'))
i1 = next(i for i, l in enumerate(b) if l.startswith("})(typeof window !== 'undefined' ? window : globalThis);"))
lib = '\n'.join(a[i0:] + b[:i1 + 1])
por = P('074zp_portraits.js'); por = por[por.index('/*@@POR-CORE@@*/'):por.index('/*@@POR-CORE-END@@*/')]
cz = P('074zz5_closezoom.js'); cz = cz[cz.index('/*@@CZ-CORE@@*/'):cz.index('/*@@CZ-CORE-END@@*/')]
cut = P('074zu_cutscenes.js'); m = re.search(r"looks:\{(.*?)\}\},\n /\*", cut, re.S)
looks = '{' + m.group(1) + '}}'
html = open(os.path.join(os.path.dirname(__file__), 'lab_shell.html'), encoding='utf-8').read()
html = html.replace('/*@@LIB@@*/', lib).replace('/*@@POR@@*/', por).replace('/*@@CZ@@*/', cz).replace('/*@@LOOKS@@*/', looks)
for bad in ('data:image', '<img', 'new Image(', 'url('):
    assert bad not in html, bad
open(out, 'w', encoding='utf-8').write(html)
print(out, len(html.encode('utf-8')), 'בתים')
