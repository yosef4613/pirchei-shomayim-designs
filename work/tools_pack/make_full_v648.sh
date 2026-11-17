#!/bin/bash
# 1.11.2026 · החבילה המלאה למסירה לבונה החדש: R23 (שלושת החלקים) + ה-SP של v648 + הבנייה + התוכנית + הדפים להורדה + מסמך המסירה + REBUILD.sh.
# הקבצים הפנימיים שכבר דחוסים נשמרים בלי דחיסה נוספת (ZIP_STORED). שימוש: bash tools_pack/make_full_v648.sh
set -e
W=/home/claude/work; D=$W/deliver/v648; OUT=$D/Turbo_City_v648_FULL.zip
cd $W && python3 - <<'PY'
import zipfile, os
W = '/home/claude/work'; D = W + '/deliver/v648'; OUT = D + '/Turbo_City_v648_FULL.zip'
R23 = W + '/deliver/s7f111_r23'
items = [(R23 + '/Turbo_City_v1_96_GATE77_S7F111_source_R23_part%d.zip' % p, 'source_R23/Turbo_City_v1_96_GATE77_S7F111_source_R23_part%d.zip' % p, zipfile.ZIP_STORED) for p in (1, 2, 3)]
items += [(D + '/Turbo_City_GATE77_v648_R23_plus_SP.zip', 'Turbo_City_GATE77_v648_R23_plus_SP.zip', zipfile.ZIP_STORED),
          (D + '/Turbo_City_v1_96_GATE77_S7F177.html', 'Turbo_City_v1_96_GATE77_S7F177.html', zipfile.ZIP_DEFLATED),
          (D + '/Turbo_City_Master_Plan_v6_41.html', 'Turbo_City_Master_Plan_v6_41.html', zipfile.ZIP_DEFLATED),
          (W + '/study/Turbo_City_HANDOFF_2026-11-01.md', 'Turbo_City_HANDOFF_2026-11-01.md', zipfile.ZIP_DEFLATED),
          (W + '/tools_pack/REBUILD.sh', 'REBUILD.sh', zipfile.ZIP_DEFLATED)]
for f in sorted(os.listdir(W + '/downloads_0105')):
    if f.endswith('.html') and not f.startswith('Turbo_City_v1_96') and not f.startswith('Turbo_City_Master_Plan'):
        items.append((W + '/downloads_0105/' + f, 'pages/' + f, zipfile.ZIP_DEFLATED))
z = zipfile.ZipFile(OUT, 'w', allowZip64=True)
for src, arc, how in items:
    z.write(src, arc, compress_type=how)
z.close()
print('FULL', OUT, len(items), 'קבצים ·', os.path.getsize(OUT), 'בתים')
PY
cd $D && sha1sum Turbo_City_v648_FULL.zip
