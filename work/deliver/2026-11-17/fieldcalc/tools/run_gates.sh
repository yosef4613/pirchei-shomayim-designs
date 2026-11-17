#!/bin/bash
# run_gates.sh <tryNNNN> — הבדיקות החוסמות (כלל 5 של BRIEF_COMMON) + המדידה של __TC_FC, כל אחת דרך התור
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; Q=$W/deliver/2026-11-17/fieldcalc/qa; cd $W
echo "== $T $(TZ=Asia/Jerusalem date +%H:%M)"
[ -n "$NO_FCH" ] || bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B deliver/2026-11-17/fieldcalc/tools/q_fch.js $Q/fch_$T.json 2> $Q/fch_$T.log; echo "fch rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
[ -n "$NO_FC" ] || bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B deliver/2026-11-17/fieldcalc/tools/q_fc_report.js $Q/fc_report_$T.json 2> $Q/fc_report_$T.err; echo "fc_report rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame_$T.json 2> $Q/q_ingame_$T.err; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $Q/rules_$T.json > $Q/rules_$T.log 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $Q/people_$T.json > $Q/people_$T.log 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 fc_$T > $Q/stuck_$T.log 2>&1; echo "stuckmax rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
echo "== done $(TZ=Asia/Jerusalem date +%H:%M)"
