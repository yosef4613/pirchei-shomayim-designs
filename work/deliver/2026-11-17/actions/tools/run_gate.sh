#!/bin/bash
# הבדיקות החוסמות לניסיון אחד, אחת אחרי השנייה (דפדפן אחד בכל פעם — דרך התור): הפעולות, מקצה לקצה, q_ingame, הכללים, אנשים בכביש, stuckmax 150
# שימוש: bash run_gate.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/actions/gate_$T; mkdir -p $O; cd $W
echo "התחלה $(TZ=Asia/Jerusalem date +%H:%M)" > $O/log.txt
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B deliver/2026-11-17/actions/tools/q_actions.js $O/actions.json 2>$O/actions.err; echo "actions $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node deliver/2026-11-17/actions/tools/e2e_actions.js $B $O/e2e.json $W/deliver/2026-11-17/actions/shots > $O/e2e.out 2>&1; echo "e2e $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err; echo "q_ingame $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; echo "people $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; echo "stuck $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
echo "סוף $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
