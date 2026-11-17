#!/bin/bash
# gate.sh <tryNNNN> <what...> — sealife: הכול במקום אחד של התור (bash W/tools_pack/bslot.sh bash gate.sh ...). what: shipbase ship tugs ingame rules people stuck
W=/home/user/tc_root/tc/pkg/work; cd $W; S=deliver/2026-11-17/sealife; T=$1; shift; B=clean_r2b_025637/out/_try/$T.html; O=$S/qa/$T; mkdir -p $O; L=$O/runs.tsv
run(){ local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo "$@" > $O/$nm.log 2>&1; printf '%s\t%s\t%s\t%s\n' $nm $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
for w in "$@"; do case $w in
 shipbase) run shipbase 900 node $S/tools/sl_ship.js clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F299.html $O/shipbase.json;;
 ship) run ship 900 node $S/tools/sl_ship.js $B $O/ship.json;;
 tugs) mkdir -p $O/shots; run tugs 2400 node $S/tools/sl_tugs.js $B $O/tugs.json 6000 $O/shots;;
 oil) run oil 1200 node $S/tools/sl_oil.js $B $O/oil.json $O/shots;;
 ingame) run ingame 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json;;
 rules) run rules 1500 node qa_tools/rules_gate.js $B $O/rules.json;;
 people) run people 1800 node qa_tools/people_on_road.js $B $O/people.json;;
 stuck) run stuck 1800 node qa_tools/stuckmax.js $B 150 sl_$T;;
esac; done
echo done >> $O/DONE
