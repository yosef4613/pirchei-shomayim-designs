#!/bin/bash
# all.sh — brandin: כל הבדיקות ברצף בתוך מקום אחד בתור, על הניסיון שכתוב ב-out/LATEST ברגע שהמקום מתפנה
#  (bash W/tools_pack/bslot.sh bash all.sh). אם out/ONLY_PROBE קיים — רק brandin_probe.
W=/home/user/tc_root/tc/pkg/work; O=$W/deliver/2026-11-17/brandin/out; T=$(cat $O/LATEST); B=$W/clean_r2b_025637/out/_try/$T.html; cd $W; : > $O/all_$T.txt
echo "start $(TZ=Asia/Jerusalem date +%H:%M) $T" >> $O/all_$T.txt
node deliver/2026-11-17/brandin/tools/brandin_probe.js $B $O/probe_$T.json $O/shots_$T > $O/probe_$T.log 2>&1; echo "brandin_probe rc=$? $(tail -c 900 $O/probe_$T.log)" >> $O/all_$T.txt
node deliver/2026-11-17/brandin/tools/rf_check.js deliver/2026-11-17/brandin/draw/Refined_check.html $O/rfcheck_$T.json $O/rfcheck_$T.png > $O/rfcheck_$T.log 2>&1; echo "rf_check rc=$? $(tail -c 400 $O/rfcheck_$T.log)" >> $O/all_$T.txt
[ -f $O/ONLY_PROBE ] && { echo done >> $O/all_$T.txt; exit 0; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/qin_$T.json > $O/qin_$T.log 2>&1; echo "q_ingame rc=$?" >> $O/all_$T.txt
node qa_tools/rules_gate.js $B $O/rules_$T.json > $O/rules_$T.log 2>&1; echo "rules_gate rc=$?" >> $O/all_$T.txt
node qa_tools/people_on_road.js $B $O/por_$T.json > $O/por_$T.log 2>&1; echo "people_on_road rc=$?" >> $O/all_$T.txt
node qa_tools/stuckmax.js $B 150 bi_$T > $O/stuck_$T.log 2>&1; echo "stuckmax rc=$? $(tail -c 300 $O/stuck_$T.log)" >> $O/all_$T.txt
echo "done $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/all_$T.txt
