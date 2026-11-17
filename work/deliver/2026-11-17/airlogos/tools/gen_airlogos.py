#!/usr/bin/env python3
# gen_airlogos.py — airlogos 17.11: מייצר את parts/074v_airlogos.js מחבילת המותגים של השדה (set7_share/airport) — הציור של המעצב כמו שהוא
#  (renderer.js: rr / path / line / ellipse / fitText / light / emblem / sign), עם שלושה שינויים בלבד: הלוגו של נמל התעופה וההשכרה — מטבלת המותגים
#  של המשחק (TC_BRANDS, הצייר TCB, במקום הקבצים library/brands), עברית בלבד (כלל 1: שמות חברות התעופה מ-S15GR_AL, בלי DEPARTURES / TERMINAL),
#  והטבלה — רק השדות של השלט. usage: python3 gen_airlogos.py <share dir> <template> <out part>
import sys, json, re
SH, TPL, OUT = sys.argv[1:4]
s = open(SH + '/airport/catalog.js', encoding='utf-8').read(); cat = json.loads(s[s.index('['):s.rindex(']') + 1])
R = open(SH + '/airport/renderer.js', encoding='utf-8').read()
def fn(name):
    i = R.index('  function ' + name + '('); j = R.index('\n  function ', i + 5); return R[i:j].strip()
code = '\n'.join(fn(n) for n in ('rr', 'path', 'line', 'ellipse', 'fitText', 'light', 'emblem', 'sign'))
# (1) הלוגואים — מטבלת המותגים של המשחק
code = code.replace("if((m.signType==='rental'||m.id==='rental')&&original('rental')){var p=original('rental').parts.logo;var scale=Math.min((W-8)/p.w,(H-8)/p.h);part(c,p,(W-p.w*scale)/2,(H-p.h*scale)/2,p.w*scale,p.h*scale);}",
                    "if((m.signType==='rental'||m.id==='rental')&&logo('rental',c,4,4,W-8,H-8,true)){}")
code = code.replace("airportEmblem(c,8,8,ew,H-16);", "logo('airport',c,8,8,ew,H-16);")
# (2) עברית בלבד
code = code.replace("fitText(c,'DEPARTURES',left,H*.78,(right-left)*.42,H*.18,accent,'left',700,'ltr');", "")
code = code.replace("fitText(c,'TURBO CITY TERMINAL',right,H*.78,right-left,H*.18,accent,'right',700,'ltr');", "fitText(c,'נמל התעופה',right,H*.8,right-left,H*.2,accent,'right',700,'rtl');")
for bad in ('original(', 'part(c', 'airportEmblem', 'DEPARTURES', 'TERMINAL'):
    assert bad not in code, bad
KEEP = ('name', 'group', 'color', 'ink', 'signType')
rows = []
for r in cat:
    if 'sign' not in r['formats'] and r['group'] != 'airlines': continue
    f = r['formats'].get('sign') or {'w': 28, 'h': 6}   # Mirage Jet / Confetti Air — בחבילה רק מודעה; השלט — באותה מידה של שאר חברות התעופה
    rows.append([r['id']] + [r.get(k) or '' for k in KEEP] + [f['w'], f['h'], r['sourceIds']])
t = open(TPL, encoding='utf-8').read()
t = t.replace('/*@CAT@*/', json.dumps(rows, ensure_ascii=False, separators=(',', ':')))
t = t.replace('/*@DRAW@*/', code)
open(OUT, 'w', encoding='utf-8', newline='').write(t)
print('airlogos:', len(rows), 'שלטים בטבלה ·', len(code), 'תווים של ציור ·', OUT)
