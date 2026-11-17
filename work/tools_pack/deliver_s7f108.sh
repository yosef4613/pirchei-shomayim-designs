#!/bin/bash
# 28.10 · מסירה — S7F108 (שלב 6 חלק 8: המוסך והגגון), ‏v6.17 (סגירת ביקורת 9), ‏R22 בשני חלקים. מעתיק לתיקיית מסירה חדשה (לא מוחק כלום) ומדפיס את טבלת הקבצים (sha1 · בתים).
# שימוש: bash tools_pack/deliver_s7f108.sh <R22.zip>   (part1 / part2 — לידו, באותו שם עם _part1 / _part2)
set -e
W=/home/claude/work; G=$W/clean_r2b_025637; P=$W/plan600; D=$W/deliver/s7f108_v617; mkdir -p $D
cp $G/out/Turbo_City_v1_96_GATE77_S7F108.html $D/
(cd $D && python3 -c "import zipfile;z=zipfile.ZipFile('Turbo_City_v1_96_GATE77_S7F108_game.zip','w',zipfile.ZIP_DEFLATED);z.write('Turbo_City_v1_96_GATE77_S7F108.html');z.close()")
cp $P/out/Turbo_City_Master_Plan_v6_17.html $D/
cp $W/audit_v600_r9/report.md $D/Turbo_City_Audit9_report.md
cp $G/qa/stage6/garage/s7f106_after.png $D/Turbo_City_garage_before_S7F106.png
cp $G/qa/stage6/garage/s7f108_after.png $D/Turbo_City_garage_after_S7F108.png
cp $G/qa/stage6/garage/roof_s7f108.png $D/Turbo_City_roofrack_S7F108.png
cp $W/study/PERF_BUDGET.md $W/study/PROGRESS_2026-10-27.md $D/
cp $W/study/Turbo_City_v1_96_GATE77_S7F108_RESUME_R24.md $D/
if [ -n "$1" ]; then mv "$1" $D/; for k in part1 part2; do [ -e "${1%.zip}_$k.zip" ] && mv "${1%.zip}_$k.zip" $D/; done; fi
(cd $W && python3 - <<'PY'
import zipfile
F=['clean_r2b_025637/tools/patches/p347_garage.py','clean_r2b_025637/tools/patches/p348_roofrack.py','clean_r2b_025637/tools/post_s7f107.txt','clean_r2b_025637/tools/post_s7f108.txt',
   'clean_r2b_025637/tools/repro.sh','clean_r2b_025637/tools/dev/garage8.py','clean_r2b_025637/tools/dev/garage8_ui.py','clean_r2b_025637/tools/dev/w12measure.sh','clean_r2b_025637/tools/dev/w12b_fly.sh',
   'clean_r2b_025637/tools/dev/fitcheck2.js','clean_r2b_025637/tools/dev/famsheet.py','clean_r2b_025637/tools/dev/census7.js','clean_r2b_025637/tools/dev/textcensus7.js',
   'clean_r2b_025637/qa/stage6/people/visible_people.js','clean_r2b_025637/qa/stage6/uniforms/uniforms_full.js',
   'plan600/tools/v600_step23.py','plan600/tools/v600_step24.py','plan600/tools/fence_plan_check.py','plan600/tools/build_v600.py','plan600/tools/v600_replay.sh','plan600/data/audit9_findings.json',
   'study/PERF_BUDGET.md','audit_v600_r9/report.md','audit_v600_r9/findings.json']
z=zipfile.ZipFile('deliver/s7f108_v617/Turbo_City_GATE77_S7F108_patches_SP.zip','w',zipfile.ZIP_DEFLATED)
for f in F: z.write(f)
z.close(); print(len(F),'files in patches_SP')
PY
)
echo "| קובץ | sha1 | בתים |"; echo "|---|---|---|"
for f in $(ls $D | sort); do printf '| `%s` | `%s` | %s |\n' "$f" "$(sha1sum $D/$f | cut -c1-12)" "$(stat -c %s $D/$f | python3 -c 'import sys;print(format(int(sys.stdin.read()),","))')"; done
