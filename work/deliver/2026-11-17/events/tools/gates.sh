#!/bin/bash
# הבדיקות החוסמות לניסיון אחד, בזו אחר זו (דפדפן אחד בכל פעם, דרך התור): bash gates.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/qa/events/$T; mkdir -p $O; cd $W
echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $O/gates.log
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json 2> $O/ingame.err; echo "ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/gates.log
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/gates.log
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T > $O/stuck.json 2> $O/stuck.err; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/gates.log
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/por.json > $O/por.out 2>&1; echo "por rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/gates.log
echo "data:image $(grep -c 'data:image' $B)" >> $O/gates.log
echo done >> $O/gates.log
