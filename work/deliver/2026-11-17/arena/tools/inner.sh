#!/bin/bash
# כל הבדיקות של arena במקום אחד בתור (bslot.sh bash inner.sh <try-part1> [try-part2]) — בלי לחכות בתור בין בדיקה לבדיקה
W=/home/user/tc_root/tc/pkg/work; T=$1; T2=$2; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/arena/qa/$T; mkdir -p $O; cd $W
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
r(){ echo "$1 rc=$2 $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/rc.txt; }
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/rc.txt
timeout 900 node deliver/2026-11-17/arena/tools/shot_ht.js $B $SP/ht_$T > $SP/ht_$T.json 2>&1; r shot_ht $?
timeout 1500 node qa_tools/probe_c2.js $B deliver/2026-11-17/arena/tools/q_arena.js $O/q_arena.json 2>$O/q_arena.err; r q_arena $?
timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err; r q_ingame $?
timeout 1500 node qa_tools/probe_c2.js $B deliver/2026-11-17/stadium/tools/q_stadium3.js $O/stadium3.json 2>$O/stadium3.err; r stadium3 $?
timeout 1500 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; r rules_gate $?
timeout 1500 node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; r people_on_road $?
timeout 2400 node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; r stuckmax $?
timeout 1500 node qa_tools/people_on_road.js $B $O/people2.json > $O/people2.out 2>&1; r people_on_road_again $?
timeout 1500 node qa_tools/probe_c2.js $B deliver/2026-11-17/stadium/tools/q_stadium3.js $O/stadium3b.json 2>$O/stadium3b.err; r stadium3_again $?
echo "done $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/rc.txt
bash deliver/2026-11-17/arena/tools/inner_bk.sh try7527 try7528
