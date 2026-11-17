#!/bin/bash
# הבדיקות של ניסיון אחד — כל אחת בתור בנפרד (מקביל דרך התור; stuckmax — היחידה הארוכה). שימוש: bash gates_par.sh tryNNNN [skip_q]
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/opening/qa/$T; mkdir -p $O; cd $W
run(){ n=$1; shift; bash tools_pack/bslot.sh "$@" > $O/$n.out 2>&1; echo "$n rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt; }
[ "$2" != skip_q ] && run q_ingame node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json &
run rules node qa_tools/rules_gate.js $B $O/rules.json &
run people node qa_tools/people_on_road.js $B $O/people.json &
run film_flow node deliver/2026-11-17/opening/tools/film_flow.js $B $O/film_flow.json &
run stuck node qa_tools/stuckmax.js $B 150 $T &
wait; echo "סוף $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
