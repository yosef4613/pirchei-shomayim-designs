#!/bin/bash
# home (17.11): בדיקת הפנים והבדיקות החוסמות על ניסיון אחד (B), במקום אחד של התור. B — מ-qa/next_in.txt אם קיים.
W=/home/user/tc_root/tc/pkg/work; B=$1; cd $W; O=$W/deliver/2026-11-17/home/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
[ -s $O/next_in3.txt ] && B=$(cat $O/next_in3.txt); T(){ TZ=Asia/Jerusalem date +%H:%M; }; L=$O/chain3.log; echo "start B=$B $(T)" >> $L; mkdir -p $O/$B; G=$O/$B; BX=clean_r2b_025637/out/_try/$B.html
timeout 1200 node deliver/2026-11-17/home/tools/home_in_q.js $BX $G/home_in.json $SP/sh_$B > $G/home_in.out 2>&1; echo "home_in $B rc=$? $(T)" >> $L
node qa_tools/probe_c2.js $BX qa_tools/q_ingame.js $G/q_ingame.json 2> $G/q_ingame.err; echo "q_ingame $B rc=$? $(T)" >> $L
node qa_tools/rules_gate.js $BX $G/rules_gate.json > $G/rules_gate.out 2>&1; echo "rules_gate $B rc=$? $(T)" >> $L
node qa_tools/people_on_road.js $BX $G/people.json > $G/people.out 2>&1; echo "people $B rc=$? $(T)" >> $L
node qa_tools/stuckmax.js $BX 150 $B > $G/stuck.out 2>&1; echo "stuck $B rc=$? $(T)" >> $L
# the second run of stuckmax on the HOME-01 build (the first: AI-CAR-19 at AIR-FRONT 42.7 s — far from the house)
[ -f clean_r2b_025637/out/_try/try8126.html ] && { node qa_tools/stuckmax.js clean_r2b_025637/out/_try/try8126.html 150 try8126b > $O/try8126/stuck2.out 2>&1; echo "stuck2 try8126 rc=$? $(T)" >> $L; }
echo "done $(T)" >> $L
