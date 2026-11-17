#!/bin/bash
# extras.sh <build.html> <outdir> — הבדיקות של הענפים שנכנסו (הכלים שלהם, בלי שינוי), על המועמד: 4 במקביל, כל אחד דרך התור (BSLOT_MERGE=1).
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; D=$W/deliver/2026-11-17; G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); cd $W; L=$O/runs.tsv
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); BSLOT_MERGE=1 timeout $tmo bash $W/tools_pack/bslot.sh "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
( run f9quick 1200 node $Q/probe_c2.js $G $D/f9fix/tools/q_f9_quick.js $O/f9quick.json; run icon 900 node $Q/probe_c2.js $G $D/posters/tools/q_icon.js $O/icon.json; run p11 1500 node $D/posters/tools/p11_check.js $G $O/p11.json $O/p11.png ) &
sleep 10; ( run mbsmoke 1200 node $Q/probe_c2.js $G $D/missions/tools/q_mb_smoke.js $O/mbsmoke.json; run tut 900 node $Q/probe_c2.js $G $D/newgame/tools/q_tut.js $O/tut.json; run pier 1500 node $Q/probe_c2.js $G $D/pier/tools/q_all.js $O/pier.json ) &
sleep 10; ( run seatrees 2400 node $D/seatrees/tools/tree_sweep.js $G $O/seatrees.json; run gst 1800 node $D/garage/tools/gst_probe.js $G $O/gst 0 ) &
sleep 10; ( run cut 2400 node $D/cutscenes/tools/cut_check.js $G $O/cut.json; run por 1800 node $D/portraits/tools/por_check.js $G $O/por.json ) &
wait; echo EXTRASDONE >> $L
