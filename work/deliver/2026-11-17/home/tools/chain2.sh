#!/bin/bash
# home (17.11): כל הבדיקות במקום אחד של התור (רץ דרך bslot.sh): HOME-01 על A, הפנים על B, ואז הבדיקות החוסמות על A ועל B. דפדפן אחד בכל פעם.
# שימוש: bash tools_pack/bslot.sh bash chain2.sh <tryA> <tryB>   (B יכול להתחלף: qa/next_in.txt)
W=/home/user/tc_root/tc/pkg/work; A=$1; B=$2; cd $W; O=$W/deliver/2026-11-17/home/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
[ -s $O/next_in.txt ] && B=$(cat $O/next_in.txt); [ -s $O/next_a.txt ] && A=$(cat $O/next_a.txt)
T(){ TZ=Asia/Jerusalem date +%H:%M; }; L=$O/chain2.log; echo "start A=$A B=$B $(T)" >> $L
mkdir -p $O/$A $O/$B
HOME_CHAIN=0 timeout 900 node deliver/2026-11-17/home/tools/home_q.js clean_r2b_025637/out/_try/$A.html $O/$A/home_q.json $SP/sh_$A > $O/$A/home_q.out 2>&1; echo "home_q $A rc=$? $(T)" >> $L
timeout 1200 node deliver/2026-11-17/home/tools/home_in_q.js clean_r2b_025637/out/_try/$B.html $O/$B/home_in.json $SP/sh_$B > $O/$B/home_in.out 2>&1; echo "home_in $B rc=$? $(T)" >> $L
for X in $A $B; do G=$O/$X; BX=clean_r2b_025637/out/_try/$X.html
  node qa_tools/probe_c2.js $BX qa_tools/q_ingame.js $G/q_ingame.json 2> $G/q_ingame.err; echo "q_ingame $X rc=$? $(T)" >> $L
  node qa_tools/rules_gate.js $BX $G/rules_gate.json > $G/rules_gate.out 2>&1; echo "rules_gate $X rc=$? $(T)" >> $L
  node qa_tools/people_on_road.js $BX $G/people.json > $G/people.out 2>&1; echo "people $X rc=$? $(T)" >> $L
  node qa_tools/stuckmax.js $BX 150 $X > $G/stuck.out 2>&1; echo "stuck $X rc=$? $(T)" >> $L
done; echo "done $(T)" >> $L
