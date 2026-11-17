#!/bin/bash
# חלק 2 (הכדורסל) במקום אחד בתור: run_bk2.sh <try-עם-היבשה> <try-של-הענף>  — קובץ חדש לכל הרצה; לא עורכים אותו בזמן ריצה
W=/home/user/tc_root/tc/pkg/work; TL=$1; T=$2; BL=$W/clean_r2b_025637/out/_try/$TL.html; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/arena/qa/$T; OL=$W/deliver/2026-11-17/arena/qa/$TL; mkdir -p $O $OL; cd $W
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
r(){ echo "$1 rc=$2 $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/rc.txt; }
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/rc.txt
timeout 900 node deliver/2026-11-17/arena/tools/shot_bk.js $BL $SP/bk_$TL > $SP/bk_$TL.json 2>&1; r shot_bk_$TL $?
timeout 1200 node qa_tools/probe_c2.js $BL deliver/2026-11-17/arena/tools/q_bkleague.js $OL/q_bkleague.json 2>$OL/q_bkleague.err; r q_bkleague_$TL $?
timeout 1200 node qa_tools/probe_c2.js $B deliver/2026-11-17/arena/tools/q_bkleague.js $O/q_bkleague.json 2>$O/q_bkleague.err; r q_bkleague $?
timeout 1500 node qa_tools/probe_c2.js $B deliver/2026-11-17/arena/tools/q_arena.js $O/q_arena.json 2>$O/q_arena.err; r q_arena $?
timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err; r q_ingame $?
timeout 1500 node qa_tools/probe_c2.js $B deliver/2026-11-17/stadium/tools/q_stadium3.js $O/stadium3.json 2>$O/stadium3.err; r stadium3 $?
timeout 1500 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; r rules_gate $?
timeout 1500 node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; r people_on_road $?
timeout 2400 node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; r stuckmax $?
echo "done $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/rc.txt
