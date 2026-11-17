#!/bin/bash
# inslot2.sh <try> — buses (17.11 13:10): כמו inslot.sh, בסדר אחר — קודם החוסמות (לשורת "מוכן למיזוג"), אחר כך הכיכרות (q_rb), ואז המדידה, הלילה של הקווים ו-stuckmax 1500.
W=/home/user/tc_root/tc/pkg/work; T=$1; D=$W/deliver/2026-11-17/buses; Q=$D/qa; cd $W
B=$W/clean_r2b_025637/out/_try/$T.html; G=$Q/${T}_gate.txt
r(){ local name=$1; shift; local t0=$(date +%s); timeout 2400 "$@"; echo "$name rc=$? $(( $(date +%s)-t0 ))s $(TZ=Asia/Jerusalem date +%H:%M)" >> $G; }
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
r ingame node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/${T}_ingame.json > $Q/${T}_ingame.log 2>&1
r rules node qa_tools/rules_gate.js $B $Q/${T}_rules.json > $Q/${T}_rules.log 2>&1
r stuck150 node qa_tools/stuckmax.js $B 150 $T > $Q/${T}_stuck150.json 2>&1
r people node qa_tools/people_on_road.js $B $Q/${T}_people.json > $Q/${T}_people.log 2>&1
echo "gate-done" >> $G
r rb node $D/tools/q_rb.js $B $Q/rb_$T.json 420 1500 > $Q/rb_$T.log 2>&1
r beh node $D/tools/q_busbeh.js $B $Q/beh_${T}.json 420 600 > $Q/beh_${T}.log 2>&1
r night node $D/tools/lines_night_tr2.js $B $Q/${T}_night.json > $Q/${T}_night.log 2>&1
r stuck1500 node $D/tools/stuckmax_bus.js $B 1500 $T > $Q/${T}_stuck1500.json 2>&1
echo "chain-done $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
r beh-base302 node $D/tools/q_busbeh.js $W/clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F302.html $Q/beh_base302.json 420 600 > $Q/beh_base302.log 2>&1; echo "base302-done $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
r night-base302 node $D/tools/lines_night_tr2.js $W/clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F302.html $Q/base302_night.json > $Q/base302_night.log 2>&1; echo "base302-night-done $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
