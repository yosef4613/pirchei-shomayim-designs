#!/bin/bash
# blocking.sh <build.html> <outdir> — הסט החוסם של המועמד (17.11): q_ingame, ‏rules_gate, ‏stuckmax 150, ‏people_on_road, ‏q_stadium3 — במקביל, כל אחד דרך התור (BSLOT_MERGE=1); ‏data:image בקובץ.
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); cd $W; L=$O/runs.tsv
echo "$(basename $G) $(sha1sum $G | cut -c1-12) $(stat -c%s $G)" > $O/build.txt
echo "data:image $(grep -o 'data:image' $G | wc -l) · new Image( $(grep -o 'new Image(' $G | wc -l) · <img $(grep -o '<img' $G | wc -l)" > $O/img.txt
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); BSLOT_MERGE=1 timeout $tmo bash $W/tools_pack/bslot.sh "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
run ingame 2400 node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json &
sleep 15; run rules 1500 node $Q/rules_gate.js $G $O/rules.json &
sleep 15; run people 2400 node $Q/people_on_road.js $G $O/people.json &
sleep 15; run stuck 1800 node $Q/stuckmax.js $G 150 $(basename $G .html) &
sleep 15; run stadium3 1800 node $Q/probe_c2.js $G $W/deliver/2026-11-17/stadium/tools/q_stadium3.js $O/stadium3.json &
wait
echo "BLOCKDONE" >> $L
