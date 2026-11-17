#!/usr/bin/env python3
# split_any.py (מ-split_pub.py) <דף הבנייה .html> <תיקיית פרסום> [N] — כשהדף מעל 16 מ"ב (מגבלת Artifact לקובץ):
# כותב loader.html קטן + g1.txt … gN.txt (חיתוך בשורה, UTF-8 תקין), שנטענים ב-fetch ומוצגים ב-document.write.
# הפרסום: Artifact publish file_path=<dir>/loader.html, files={"g1.txt": "<dir>/g1.txt", ...}, url=8VUftq…
# אחרי הפרסום: read paths g1..gN → cat | cmp מול דף הבנייה. (המתאם, 11.11.2026 — S7F295 היה הראשון)
import sys, os, re
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
# split_any (17.11): חיתוך בכל תו (לא רק בסוף שורה) לחלקים של עד MAXMB מ"ב — NetFree חוסם קובץ עם הרבה אודיו (074zv_side_vrec_data 5.4MB), חלקים של ~0.5MB עוברים
maxb = int(float(sys.argv[3] if len(sys.argv) > 3 else 1.3) * 1_000_000)
parts, cur, size = [], [], 0
for ch_i in range(0, len(s), 50_000):
    blk = s[ch_i:ch_i+50_000]; bl = len(blk.encode('utf-8'))
    if size and size + bl > maxb: parts.append(''.join(cur)); cur, size = [], 0
    cur.append(blk); size += bl
if cur: parts.append(''.join(cur))
names = []
for i, p in enumerate(parts, 1):
    nm = f'g{i}.txt'; names.append(nm)
    open(os.path.join(out, nm), 'w', encoding='utf-8', newline='').write(p)
m = re.search(r'<title>(.*?)</title>', s, re.S); title = m.group(1).strip() if m else 'טורבו סיטי'
loader = ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>%s</title>\n'
 '<style>:root{color-scheme:dark;--bg:#081018;--ink:#f3f7fa}:root:not([data-theme="light"]){--bg:#081018}:root[data-theme="dark"]{--bg:#081018}html,body{margin:0;height:100%%;background:var(--bg);color:var(--ink);font:16px "Segoe UI","Noto Sans Hebrew",Arial,sans-serif}#ld{display:grid;place-items:center;height:100%%;padding:0 16px;text-align:center}</style></head>\n'
 '<body><div id="ld">טוען את טורבו סיטי…</div>\n<script>\n(async()=>{try{\n const parts=await Promise.all(%s.map(u=>fetch(u,{cache:\'no-cache\'}).then(r=>{if(!r.ok)throw new Error(u+\' \'+r.status);return r.text()})));\n'
 ' document.open();document.write(parts.join(\'\'));document.close();\n}catch(e){document.getElementById(\'ld\').textContent=\'הטעינה נכשלה: \'+e.message}})();\n</script></body></html>\n') % (title, str(names).replace("'", "'"))
open(os.path.join(out, 'loader.html'), 'w', encoding='utf-8').write(loader)
assert ''.join(open(os.path.join(out, nm), encoding='utf-8').read() for nm in names) == s
for nm in names + ['loader.html']: print(nm, os.path.getsize(os.path.join(out, nm)))
print('ok: החלקים יחד = דף הבנייה')
