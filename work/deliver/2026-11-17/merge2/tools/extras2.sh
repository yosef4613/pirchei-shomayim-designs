#!/bin/bash
# extras2.sh <build.html> <outdir> — הבדיקות של הענפים שנכנסו לגל 2 (הכלים שלהם, בלי שינוי), על המועמד: 4 שרשראות במקביל, כל אחת דרך התור (BSLOT_MERGE=1).
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; D=$W/deliver/2026-11-17; G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); cd $W; L=$O/runs.tsv
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); BSLOT_MERGE=1 timeout $tmo bash $W/tools_pack/bslot.sh "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
( run seatrees 2400 node $D/seatrees/tools/tree_sweep.js $G $O/seatrees.json; run mbsmoke 1200 node $Q/probe_c2.js $G $D/missions/tools/q_mb_smoke.js $O/mbsmoke.json; run kiosk 1500 node $D/signs/tools/signs12_kiosk.js $G $O/kiosk.json $O/kiosk ) &
sleep 10; ( run signs12 2400 node $D/signs/tools/signs12_probe.js $G $O/signs12.json $D/signs/tools/review_ids.json; run gst 1800 node $D/garage/tools/gst_probe.js $G $O/gst 0; run voice 1500 node $D/voiceint/tools/q_voiceint.js $G $O/voice.json ) &
sleep 10; ( run sact 1500 node $Q/probe_c2.js $G $D/actions/tools/q_actions.js $O/sact.json; run pier 1800 node $Q/probe_c2.js $G $D/pier/tools/q_all.js $O/pier.json; run e2e 2400 node $D/actions/tools/e2e_actions.js $G $O/e2e.json $O/e2e_shots ) &
sleep 10; ( run evt 2400 node $D/events/tools/evt_test.js $G $O/evt.json $O/evt_shots 130 420; run liv 1500 node $D/fieldfix/tools/probe_liv.js $G $O/liv cand300x ) &
wait; echo EXTRASDONE >> $L
