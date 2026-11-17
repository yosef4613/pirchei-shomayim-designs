#!/bin/bash
# 28.10 · מסירה — S7F111 להרצה (שלב 7 חלקים 1–3), ‏v6.18, ‏R23 בשלושה חלקים; הלוגו של החנויות (S7F116, בבדיקות) — בתמונות. מעתיק לתיקיית מסירה חדשה (לא מוחק כלום) ומדפיס את טבלת הקבצים (sha1 · בתים).
# שימוש: bash tools_pack/deliver_r23.sh <R23.zip>   (part1 / part2 / part3 — לידו, באותו שם עם _part1 / _part2 / _part3)
set -e
W=/home/claude/work; G=$W/clean_r2b_025637; P=$W/plan600; D=$W/deliver/s7f111_r23; mkdir -p $D
cp $G/out/Turbo_City_v1_96_GATE77_S7F111.html $D/
(cd $D && python3 -c "import zipfile;z=zipfile.ZipFile('Turbo_City_v1_96_GATE77_S7F111_game.zip','w',zipfile.ZIP_DEFLATED);z.write('Turbo_City_v1_96_GATE77_S7F111.html');z.close()")
cp $P/out/Turbo_City_Master_Plan_v6_18.html $D/
cp $G/qa/stage7/brands/s7f113_sheet.png $D/Turbo_City_shop_logos.png
python3 - <<PY
from PIL import Image
G='$G/qa/stage7/brands/'; ids=['C2-MALL','C2-SUPER','C2-PHARMACY','C2-CAFE','D2-RESTO','D2-MARKET','C4-HARDWARE','B2-KIOSK','D3-FUEL']
W,H=480,300;S=Image.new('RGB',(W*3,H*3),'black')
for i,k in enumerate(ids): S.paste(Image.open(G+'s7f113_sign_%s.png'%k),((i%3)*W,(i//3)*H))
S.save('$D/Turbo_City_shop_signs.png')
PY
cp $G/qa/stage7/shots/s7f111_licenses.png $D/Turbo_City_licenses_hebrew_S7F111.png
cp $W/study/PERF_BUDGET.md $W/study/PROGRESS_2026-10-27.md $D/
cp $W/study/Turbo_City_v1_96_GATE77_S7F111_RESUME_R25.md $D/
if [ -n "$1" ]; then [ -e "$1" ] && mv "$1" $D/; for k in part1 part2 part3; do [ -e "${1%.zip}_$k.zip" ] && mv "${1%.zip}_$k.zip" $D/; done; fi
(cd $W && python3 - <<'PY'
import zipfile
F=['clean_r2b_025637/tools/patches/p349_roadnames.py','clean_r2b_025637/tools/patches/p350_signs.py','clean_r2b_025637/tools/patches/p351_uinames.py','clean_r2b_025637/tools/patches/p352_tokens.py',
   'clean_r2b_025637/tools/patches/p353_brands.py','clean_r2b_025637/tools/patches/p355_labels2.py','clean_r2b_025637/tools/patches/p356_noreadback.py','clean_r2b_025637/tools/patches/p354_nature.py','clean_r2b_025637/tools/dev/w17measure.sh','clean_r2b_025637/tools/dev/bench_gpu.js','clean_r2b_025637/tools/dev/famsheet.py',
   'clean_r2b_025637/tools/post_s7f109.txt','clean_r2b_025637/tools/post_s7f110.txt','clean_r2b_025637/tools/post_s7f111.txt','clean_r2b_025637/tools/post_s7f112.txt','clean_r2b_025637/tools/post_s7f113.txt','clean_r2b_025637/tools/post_s7f116.txt','clean_r2b_025637/tools/post_s7f117.txt','clean_r2b_025637/tools/patches/p357_logopins.py','clean_r2b_025637/tools/patches/p358_fastbb.py','clean_r2b_025637/tools/dev/w18measure.sh','tools_pack/pack_r23.py','tools_pack/perf_sec.py',
   'clean_r2b_025637/tools/repro.sh','clean_r2b_025637/tools/dev/textcensus7.js','clean_r2b_025637/tools/dev/uicensus7.py','clean_r2b_025637/tools/dev/brands7.py','clean_r2b_025637/tools/dev/shots7.py',
   'clean_r2b_025637/tools/dev/readbacks.py','clean_r2b_025637/tools/dev/bbcheck.py','clean_r2b_025637/tools/dev/drive7.py','clean_r2b_025637/tools/dev/gpu_all.js','clean_r2b_025637/tools/dev/cpuprof.js',
   'clean_r2b_025637/tools/dev/w15measure.sh',
   'plan600/tools/v600_step25.py','plan600/tools/build_v600.py','plan600/tools/v600_replay.sh','study/PERF_BUDGET.md']
z=zipfile.ZipFile('deliver/s7f111_r23/Turbo_City_GATE77_S7F111_R23_patches_SP.zip','w',zipfile.ZIP_DEFLATED)
for f in F: z.write(f)
z.close(); print(len(F),'files in patches_SP')
PY
)
echo "| קובץ | sha1 | בתים |"; echo "|---|---|---|"
for f in $(ls $D | sort); do printf '| `%s` | `%s` | %s |\n' "$f" "$(sha1sum $D/$f | cut -c1-12)" "$(stat -c %s $D/$f | python3 -c 'import sys;print(format(int(sys.stdin.read()),","))')"; done
