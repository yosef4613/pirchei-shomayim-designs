#!/bin/bash
# quick.sh <build.html> <outdir> — הבדיקה המהירה של המיזוג (17.11): q_ingame ו-rules_gate במקביל, כל אחד דרך התור (BSLOT_MERGE=1).
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); cd $W; L=$O/runs.tsv
echo "$(basename $G) $(sha1sum $G | cut -c1-12) $(stat -c%s $G)" > $O/build.txt
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); BSLOT_MERGE=1 timeout $tmo bash $W/tools_pack/bslot.sh "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
run ingame 2400 node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json &
sleep 20; run rules 1500 node $Q/rules_gate.js $G $O/rules.json &
wait; echo "QUICKDONE" >> $L
