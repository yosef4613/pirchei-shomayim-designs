#!/bin/bash
# כל הבדיקות של ניסיון אחד במקום אחד בתור (דפדפן אחד בכל רגע, אחת אחרי השנייה): bash all1.sh tryNNNN
# מריצים כך: bash W/tools_pack/bslot.sh bash W/deliver/2026-11-17/cutscenes/tools/all1.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; Q=$W/deliver/2026-11-17/cutscenes/qa; O=$Q/$T; mkdir -p $O; L=$Q/gates_${T#try}.log
cd $W
t(){ TZ=Asia/Jerusalem date +%H:%M:%S; }
echo "== cut $(t)" >> $L; node deliver/2026-11-17/cutscenes/tools/cut_check.js $B $Q/cut_${T#try}.json $O/shots > $Q/cut_${T#try}.log 2>&1; echo "cut rc=$? $(t)" >> $L
echo "== q_ingame $(t)" >> $L; node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json > $O/ingame.log 2>&1; echo "ingame rc=$? $(t)" >> $L
echo "== rules $(t)" >> $L; node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; echo "rules rc=$? $(t)" >> $L
echo "== people $(t)" >> $L; node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; echo "people rc=$? $(t)" >> $L
echo "== stuck $(t)" >> $L; node qa_tools/stuckmax.js $B 150 $T > $O/stuck.log 2>&1; echo "stuck rc=$? $(t)" >> $L
echo "== done $(t)" >> $L
