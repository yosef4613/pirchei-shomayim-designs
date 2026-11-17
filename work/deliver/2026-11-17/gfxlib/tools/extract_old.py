#!/usr/bin/env python3
# מחלץ מהמקור של המשחק (עותק העבודה) את שלוש הספריות של התצוגה 3/4 כמו שהן, מילה במילה:
# C34 (המכוניות, c34LibInit), ‏P34 (האנשים, p34LibInit), ‏A34 (המטוסים, a34LibInit) — לקובץ old_libs.js לדף ההשוואה.
import json, sys, os, re
src = sys.argv[1] if len(sys.argv) > 1 else '/home/user/tc_root/tc/pkg/work/src_game_t17_gfxlib'
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', 'src', 'old_libs.js')
m = json.load(open(os.path.join(src, 'manifest.json')))
blk = ''.join(open(os.path.join(src, 'parts', p['name']), encoding='utf8').read() for p in m['parts'] if p['block'] == 12)
def cut(start, end):
    i = blk.index(start); j = blk.index(end, i) + len(end); return blk[i:j]
c34 = cut('function c34LibInit(){', '\nreturn true}')
p34 = cut('function p34LibInit(){', '\nreturn true}')
a34 = cut('function a34LibInit(){', '\nreturn !!window.A34}')
# a34LibInit מחכה ל-C34G.armed של המשחק — בדף ההשוואה אין לולאת משחק
a34 = a34.replace('if(!C34G.armed)return false;', '', 1)
sizes = {'C34': len(c34.encode()), 'P34': len(p34.encode()), 'A34': len(a34.encode())}
hdr = '/* old_libs.js — נוצר אוטומטית ע"י extract_old.py מתוך %s (הענף %s). הקוד הישן של המשחק מילה במילה. גדלים: %s */\n' % (src, os.popen('git -C %s rev-parse --short HEAD' % src).read().strip(), json.dumps(sizes))
open(out, 'w', encoding='utf8').write(hdr + c34 + '\n' + p34 + '\n' + a34 + '\nwindow.__OLD_SIZES=' + json.dumps(sizes) + ';\n')
print(out, sizes)
