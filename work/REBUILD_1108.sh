#!/bin/bash
# 8.11.2026 · הבנייה מחדש ובדיקה: (1) S7F265 משרשרת הטלאים, (2) S7F265 מהחיבור של src_game (התגית S7F265), (3) התוכנית — v6.91 מהגיבויים ו-v6.92 (rebuild_plan_1108.sh). היציאה: מספר ההבדלים.
H=$PWD; bad=0
check() { local f=$1 want=$2; local got=$(sha1sum "$f" 2>/dev/null | cut -c1-12); if [ "$got" = "$want" ]; then echo "זהה  $f $got"; else echo "שונה $f $got (צפוי $want)"; bad=$((bad+1)); fi; }
bash REBUILD_LEAN_1106.sh >/dev/null 2>&1; check clean_r2b_025637/out/_rebuild_S7F265.html 56754fb61661; bash plan600/tools/rebuild_plan_1108.sh >/dev/null 2>&1; r=$?; [ $r -eq 0 ] && echo 'זהה  התוכנית: v6.91 מהגיבויים ו-v6.92 מהצעד 91' || { echo "שונה התוכנית ($r הבדלים — plan600/tools/rebuild_plan_1108.sh)"; bad=$((bad+r)); }
mkdir -p build_join && [ -e build_join/_src_s7f265 ] && { git -C src_game worktree remove --force ../build_join/_src_s7f265 2>/dev/null || mv build_join/_src_s7f265 _to_delete/_src_s7f265_$(date +%s); }; git -C src_game worktree add -f ../build_join/_src_s7f265 S7F265 >/dev/null 2>&1 || cp -r src_game build_join/_src_s7f265
BUILD_SUFFIX=-s7f265 python3 tools_pack/join_game.py build_join/_src_s7f265 build_join/_rebuild_join_S7F265.html >/dev/null; check build_join/_rebuild_join_S7F265.html 56754fb61661
echo "REBUILD_1108 DONE $(TZ=Asia/Jerusalem date +%H:%M) · הבדלים: $bad"; exit $bad
