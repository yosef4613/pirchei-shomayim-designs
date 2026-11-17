# -*- coding: utf-8 -*-
# 2.11 · R-59 — דף "הבנייה האחרונה": קובץ המשחק כמו שהוא, עם שם קבוע בעברית ושורת כותרת בעברית בראש המסך (נעלמת אחרי 15 שניות, לא תופסת לחיצות).
# usage: python3 make_build_page.py <game.html> <out.html> "<שורת הכותרת>"
import sys, re
src, out, line = sys.argv[1], sys.argv[2], sys.argv[3]
H = open(src, encoding='utf-8').read()
H, n = re.subn(r'<title>[^<]*</title>', '<title>הבנייה האחרונה טורבו סיטי</title>', H, count=1)
assert n == 1, 'no title'
BAR = ('<div id="tcBuildBar" style="position:fixed;top:0;left:0;right:0;z-index:2147483000;pointer-events:none;direction:rtl;text-align:center;'
       'font:600 13px/1.5 \'Segoe UI\',Arial,sans-serif;color:#fff;background:rgba(8,16,24,.82);padding:5px 12px;'
       'animation:tcBarOut 1.2s ease 15s forwards">' + line.replace('<', '&lt;') + '</div>'
       '<style>@keyframes tcBarOut{to{opacity:0;visibility:hidden}}</style>')
i = H.find('<body>'); assert i > 0
H = H[:i + 6] + BAR + H[i + 6:]
open(out, 'w', encoding='utf-8').write(H)
print('ok', len(H.encode('utf-8')))
