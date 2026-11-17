#!/bin/bash
# 1.11.2026 · בנייה מחדש מחבילת העבודה הרזה (Turbo_City_v648_LEAN.zip), בתיקייה ריקה, ובדיקה שהכול יוצא זהה.
# שימוש: unzip Turbo_City_v648_LEAN.zip -d new && cd new && bash REBUILD_LEAN.sh
# בונה: S7F177 (הבנייה האחרונה שנמסרה), S7F178 ו-S7F179 (נבנו ולא נמסרו), B4A (העבודה הפתוחה של B4, בנייה מקומית),
# והתוכנית v6.41 מהנתונים. משווה כל sha1 לערך הצפוי. צריך python3 ו-node. היציאה: מספר ההבדלים.
H=$PWD; bad=0
check() { local f=$1 want=$2; local got=$(sha1sum "$f" 2>/dev/null | cut -c1-12); if [ "$got" = "$want" ]; then echo "זהה  $f $got"; else echo "שונה $f $got (צפוי $want)"; bad=$((bad+1)); fi; }
cd $H/clean_r2b_025637 && mkdir -p out build
for x in 177:6621a0cee449 178:b599c02dcf5c 179:62d013078d76; do n=${x%%:*}; s=${x#*:}
  env S6R_POST="$(tr -d '\n' < tools/post_s7f$n.txt)" BUILD_SUFFIX=-s7f$n python3 tools/build_s6r.py out/Turbo_City_v1_96_GATE77_S7F$n.html > build_s7f$n.log 2>&1
  check out/Turbo_City_v1_96_GATE77_S7F$n.html $s; done
# B4A — the open work of B4 (tools/dev/build_b4a.sh builds it to qa/b4/build); here straight from its post
env S6R_POST="$(tr -d '\n' < tools/post_b4a.txt)" BUILD_SUFFIX=-b4a python3 tools/build_s6r.py out/B4A_local.html > build_b4a.log 2>&1
check out/B4A_local.html 8a8653dfc626
cd $H/plan600 && mkdir -p out && python3 tools/build_v600.py out/Turbo_City_Master_Plan_v6_41.html > build_plan.log 2>&1
check out/Turbo_City_Master_Plan_v6_41.html 2608ebb1eafb
echo "REBUILD_LEAN DONE $(date +%H:%M) · הבדלים: $bad"; exit $bad
