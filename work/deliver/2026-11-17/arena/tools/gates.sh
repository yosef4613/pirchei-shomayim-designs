#!/bin/bash
# הבדיקות החוסמות של ניסיון אחד (arena 17.11): gates.sh tryNNNN   (כל דפדפן — דרך התור)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/arena/qa/$T; mkdir -p $O; cd $W
S="bash tools_pack/bslot.sh"
$S timeout 1500 node qa_tools/probe_c2.js $B deliver/2026-11-17/arena/tools/q_arena.js $O/q_arena.json 2>$O/q_arena.err; echo "q_arena rc=$? $(date +%H:%M)" >> $O/rc.txt
$S timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err; echo "q_ingame rc=$? $(date +%H:%M)" >> $O/rc.txt
$S timeout 1500 node qa_tools/probe_c2.js $B deliver/2026-11-17/stadium/tools/q_stadium3.js $O/stadium3.json 2>$O/stadium3.err; echo "stadium3 rc=$? $(date +%H:%M)" >> $O/rc.txt
$S timeout 1500 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules_gate rc=$? $(date +%H:%M)" >> $O/rc.txt
$S timeout 1500 node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; echo "people_on_road rc=$? $(date +%H:%M)" >> $O/rc.txt
$S timeout 2400 node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; echo "stuckmax rc=$? $(date +%H:%M)" >> $O/rc.txt
echo "done $(date +%H:%M)" >> $O/rc.txt
