#!/bin/bash
# gate_in.sh <tryNNNN> [quick] — fieldthru: בתוך מקום אחד בתור (bash bslot.sh bash gate_in.sh ...): ה-dump של השדה (+ __TC_FC + FTS), ואז הבדיקות החוסמות אחת אחרי השנייה
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/fieldthru/qa/$T; mkdir -p $O; cd $W
st(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S) rc=$2" >> $O/runs.tsv; }
echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/runs.tsv
echo "data:image $(grep -c 'data:image' $B) · <img $(grep -o '<img' $B | wc -l)" > $O/static.txt
timeout 900 node deliver/2026-11-17/fieldthru/tools/dump_sim.js $B $O/sim.json > $O/dump.log 2>&1; st dump $?
timeout 120 node deliver/2026-11-17/fieldthru/tools/page_shot.js deliver/2026-11-17/fieldthru/Fieldthru_plan.html /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/page > $O/page.log 2>&1; st page $?
timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json > $O/ingame.log 2>&1; st ingame $?
[ "$2" = quick ] && { echo done >> $O/runs.tsv; exit 0; }
timeout 900 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; st rules $?
timeout 1200 node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; st people $?
timeout 1500 node qa_tools/stuckmax.js $B 150 ft_$T > $O/stuck.log 2>&1; st stuck $?
echo done >> $O/runs.tsv
