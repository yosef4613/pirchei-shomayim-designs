#!/bin/bash
# home (17.11): רק בדיקת הפנים על ניסיון אחד (B — מ-qa/next_in5.txt אם קיים), במקום אחד של התור
W=/home/user/tc_root/tc/pkg/work; B=$1; cd $W; O=$W/deliver/2026-11-17/home/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
[ -s $O/next_in5.txt ] && B=$(cat $O/next_in5.txt); T(){ TZ=Asia/Jerusalem date +%H:%M; }; L=$O/chain6.log; echo "start B=$B $(T)" >> $L; mkdir -p $O/$B
timeout 1200 node deliver/2026-11-17/home/tools/home_in_q.js clean_r2b_025637/out/_try/$B.html $O/$B/home_in5.json $SP/sh5_$B > $O/$B/home_in5.out 2>&1; echo "home_in $B rc=$? $(T)" >> $L
G=$O/$B; BX=clean_r2b_025637/out/_try/$B.html
node qa_tools/probe_c2.js $BX qa_tools/q_ingame.js $G/q_ingame.json 2> $G/q_ingame.err; echo "q_ingame $B rc=$? $(T)" >> $L
node qa_tools/rules_gate.js $BX $G/rules_gate.json > $G/rules_gate.out 2>&1; echo "rules_gate $B rc=$? $(T)" >> $L
node qa_tools/people_on_road.js $BX $G/people.json > $G/people.out 2>&1; echo "people $B rc=$? $(T)" >> $L
node qa_tools/stuckmax.js $BX 150 $B > $G/stuck.out 2>&1; echo "stuck $B rc=$? $(T)" >> $L
echo "done $(T)" >> $L
