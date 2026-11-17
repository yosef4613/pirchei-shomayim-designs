#!/bin/bash
# gates.sh <tryNNNN> — fieldsvc: כל הבדיקות במקום אחד בתור (bash tools_pack/bslot.sh bash gates.sh tryNNNN): dump + __TC_FS, ‏q_ingame, ‏rules_gate, ‏people_on_road, ‏stuckmax 150
W=/home/user/tc_root/tc/pkg/work; T=$1; [ "$T" = LATEST ] && T=$(cat $W/deliver/2026-11-17/fieldsvc/qa/latest.txt); B=$W/clean_r2b_025637/out/_try/$T.html; Q=$W/deliver/2026-11-17/fieldsvc/qa/$T; mkdir -p $Q; cd $W
echo "== $T $(TZ=Asia/Jerusalem date +%H:%M)"
node deliver/2026-11-17/fieldsvc/tools/dump_game.js $B $Q/dump.json > $Q/dump.log 2>&1; echo "dump rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
[ -n "$ONLY_DUMP" ] && { echo "== done (dump) $(TZ=Asia/Jerusalem date +%H:%M)"; exit 0; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame.json 2> $Q/q_ingame.err; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
node qa_tools/rules_gate.js $B $Q/rules.json > $Q/rules.log 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
node qa_tools/people_on_road.js $B $Q/people.json > $Q/people.log 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
node qa_tools/stuckmax.js $B 150 fs_$T > $Q/stuck.log 2>&1; echo "stuckmax rc=$? $(TZ=Asia/Jerusalem date +%H:%M)"
echo "== done $(TZ=Asia/Jerusalem date +%H:%M)"
