#!/bin/bash
# gates.sh <tryNNNN> — terminal: הבדיקות החוסמות (BRIEF_COMMON סעיף 5 + term_bags / term_shuttle) בדפדפן אחד אחרי השני, בתוך מקום אחד בתור:
#   bash tools_pack/bslot.sh bash deliver/2026-11-17/terminal/tools/gates.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; Q=$W/deliver/2026-11-17/terminal/qa/$T; mkdir -p $Q; cd $W
echo "== $T $(TZ=Asia/Jerusalem date +%H:%M)"
node deliver/2026-11-17/terminal/tools/tsess.js $B $Q/term "${SHOTS:-[]}" > $Q/term.log 2>&1; echo "term rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame.json 2> $Q/q_ingame.err; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
node qa_tools/rules_gate.js $B $Q/rules.json > $Q/rules.log 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
node qa_tools/people_on_road.js $B $Q/people.json > $Q/people.log 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
node qa_tools/stuckmax.js $B 150 term_$T > $Q/stuck.log 2>&1; echo "stuckmax rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
grep -c 'data:image' $B > $Q/dataimage.txt; echo "data:image $(cat $Q/dataimage.txt)"
echo "== done $(TZ=Asia/Jerusalem date +%H:%M)"
