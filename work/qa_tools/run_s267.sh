#!/bin/bash
# run_s267.sh <game.html> <outdir> [base_outdir] — הסט המלא (full_set.sh) ועוד: 5 ריצות נוספות של העצירות (stuckmax, ‏150 שנ׳ — 6 בסך הכול),
# הבדיקה של מה שהבעלים אהב (liked_check.py) ובדיקת הסנכרון המלאה (sync_check.py עם התוכנית). בונה S7F267, 8.11.
set -u
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; T=$W/tools_pack
G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); BASE=${3:-}
PLAN=$W/clean_r2b_025637/out/qa_s267/city_plan_snapshot.json bash $Q/full_set.sh "$G" "$O" $BASE > $O/full_set.out 2>&1; echo "full_set $?" > $O/extra.txt
for i in 2 3 4 5 6; do timeout 1200 bash $T/nolock.sh node $Q/stuckmax.js $G 150 stuck$i > $O/stuck$i.log 2>&1; echo "stuck$i $?" >> $O/extra.txt; done
python3 $T/liked_check.py $G $O/liked.json > $O/liked.log 2>&1; echo "liked $?" >> $O/extra.txt
timeout 1800 python3 $T/sync_check.py --build $G --plan $W/plan600/out/Turbo_City_Master_Plan_v6_92.html --out $O/sync.json > $O/sync.log 2>&1; echo "sync $?" >> $O/extra.txt
echo "done $(date +%H:%M)" >> $O/extra.txt
