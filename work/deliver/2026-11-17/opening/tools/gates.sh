#!/bin/bash
# הבדיקות החוסמות לניסיון אחד, בזו אחר זו (דפדפן אחד בכל פעם, דרך התור). שימוש: bash gates.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/opening/qa/$T; mkdir -p $O; cd $W
echo "התחלה $(TZ=Asia/Jerusalem date +%H:%M)" > $O/log.txt
bash tools_pack/bslot.sh node deliver/2026-11-17/opening/tools/film_flow.js $B $O/film_flow.json > $O/film_flow.out 2>&1; echo "film_flow rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
echo "סוף" >> $O/log.txt
