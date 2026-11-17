#!/bin/bash
# 6.11.2026 · בנייה מחדש מחבילת העבודה (Turbo_City_HANDOFF_1106_core.tar.gz), בתיקייה ריקה, ובדיקה שהכול יוצא זהה.
# שימוש: mkdir -p /home/claude && cd /home/claude && tar xzf Turbo_City_HANDOFF_1106_core.tar.gz && cd tc/pkg/work && bash REBUILD_LEAN_1106.sh
# בונה: S7F265 (הבנייה האחרונה שנמסרה) ואת התוכנית v6.91 מהנתונים. משווה כל sha1 לערך הצפוי. צריך python3 ו-node. היציאה: מספר ההבדלים.
H=$PWD; bad=0
check() { local f=$1 want=$2; local got=$(sha1sum "$f" 2>/dev/null | cut -c1-12); if [ "$got" = "$want" ]; then echo "זהה  $f $got"; else echo "שונה $f $got (צפוי $want)"; bad=$((bad+1)); fi; }
cd $H/clean_r2b_025637 && mkdir -p out build
env S6R_POST="$(tr -d '\n' < tools/post_s7f265.txt)" BUILD_SUFFIX=-s7f265 python3 tools/build_s6r.py out/_rebuild_S7F265.html > build_rebuild_s7f265.log 2>&1
check out/_rebuild_S7F265.html 56754fb61661
cd $H/plan600 && mkdir -p out && python3 tools/build_v600.py out/_rebuild_v6_91.html > build_rebuild_plan.log 2>&1
check out/_rebuild_v6_91.html 8078967d1cb5
echo "REBUILD_LEAN_1106 DONE $(date +%H:%M) · הבדלים: $bad"; exit $bad
