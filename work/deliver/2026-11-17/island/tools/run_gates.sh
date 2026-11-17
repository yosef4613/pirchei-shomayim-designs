#!/bin/bash
# הבדיקות החוסמות לניסיון (BRIEF_COMMON סעיף 5) — אחת אחרי השנייה, דרך התור. שימוש: run_gates.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; mkdir -p $O; cd $W
echo "התחלה $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $O/log.txt
(cd deliver/2026-11-17/island/tools && QMAX=4000 bash /home/user/tc_root/tc/pkg/work/tools_pack/bslot.sh node isl_shot.js $B /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl/shots_$TRY --q q_isl.js --q q_isl2.js "h8:9000,6700,0.55" "cable:7650,7450,0.42") > $O/q_isl.out 2>&1; echo "q_isl rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; echo "rules_gate rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; echo "people_on_road rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; echo "stuckmax rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt
echo "סוף" >> $O/log.txt
