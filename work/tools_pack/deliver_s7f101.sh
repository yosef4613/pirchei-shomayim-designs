#!/bin/bash
# 27.10 · מסירת 23:30 — דף הסיכום, S7F101, ‏v6.13, ‏R19. מעתיק לתיקיית מסירה חדשה (לא מוחק כלום) ומדפיס את טבלת הקבצים (sha1 · בתים).
# שימוש: bash tools_pack/deliver_s7f101.sh <R19.zip>
set -e
W=/home/claude/work; G=$W/clean_r2b_025637; P=$W/plan600; D=$W/deliver/s7f101_v613; mkdir -p $D
cp $G/out/Turbo_City_v1_96_GATE77_S7F101.html $D/
(cd $D && python3 -c "import zipfile;z=zipfile.ZipFile('Turbo_City_v1_96_GATE77_S7F101_game.zip','w',zipfile.ZIP_DEFLATED);z.write('Turbo_City_v1_96_GATE77_S7F101.html');z.close()")
cp $P/out/Turbo_City_Master_Plan_v6_13.html $D/
cp $W/deliver/summary_2330/Turbo_City_Summary_27-10.html $D/
cp $G/qa/stage6/shots/Turbo_City_fence_S7F100_vs_S7F101.png $D/
cp $W/study/PERF_BUDGET.md $W/study/PROGRESS_2026-10-27.md $D/
cp $W/study/Turbo_City_v1_96_GATE77_S7F101_RESUME_R21.md $D/
[ -n "$1" ] && mv "$1" $D/
(cd $W && python3 - <<'EOF'
import zipfile
F=['clean_r2b_025637/tools/patches/p337_sizetable.py','clean_r2b_025637/tools/patches/p338_carsizes.py','clean_r2b_025637/tools/patches/p339_carwidths.py',
   'clean_r2b_025637/tools/patches/p340_heavysizes.py','clean_r2b_025637/tools/patches/p341_fenceline.py','clean_r2b_025637/tools/post_s7f100.txt','clean_r2b_025637/tools/post_s7f101.txt',
   'clean_r2b_025637/tools/repro.sh','clean_r2b_025637/tools/dev/w6measure.sh','clean_r2b_025637/tools/dev/w7measure.sh','clean_r2b_025637/tools/dev/s7f101_check.sh',
   'clean_r2b_025637/tools/dev/fitcheck2.js','clean_r2b_025637/tools/dev/gpu_why.js',
   'plan600/tools/v600_step19.py','plan600/tools/v600_step20.py','plan600/tools/v600_replay.sh','plan600/data/audit7_findings.json',
   'study/PERF_BUDGET.md','audit_v600_r7/report.md','audit_v600_r7/findings.json','audit_v600_r7/closure_step19.md']
z=zipfile.ZipFile('deliver/s7f101_v613/Turbo_City_GATE77_S7F101_patches_SP.zip','w',zipfile.ZIP_DEFLATED)
for f in F: z.write(f)
z.close(); print(len(F),'files in patches_SP')
EOF
)
echo "| קובץ | sha1 | בתים |"; echo "|---|---|---|"
for f in $(ls $D | sort); do printf '| `%s` | `%s` | %s |\n' "$f" "$(sha1sum $D/$f | cut -c1-12)" "$(stat -c %s $D/$f | python3 -c 'import sys;print(format(int(sys.stdin.read()),","))')"; done
