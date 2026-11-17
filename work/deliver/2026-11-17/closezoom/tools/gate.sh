#!/bin/bash
# gate.sh <tryNNNN> <what...> — closezoom 17.11: הבדיקות במקום אחד של התור (bash W/tools_pack/bslot.sh bash gate.sh ...), כמו perf/tools/gate.sh.
# what: cz (czcheck — הזום הקרוב: רמות, גלגלת 5.5↔16, רכב, qa) · czn (אותו דבר במסך צר 412×860) · zc (perf: זום ×20 + מסך צר) · ingame · rules · people · stuck
W=/home/user/tc_root/tc/pkg/work; cd $W; S=deliver/2026-11-17/closezoom; T=$1; shift; B=clean_r2b_025637/out/_try/$T.html; O=$S/qa/$T; mkdir -p $O; L=$O/runs.tsv
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
run(){ local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo "$@" > $O/$nm.log 2>&1; printf '%s\t%s\t%s\t%s\n' $nm $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
for w in "$@"; do case $w in
 cz) run cz 1200 node $S/tools/czcheck.js $B $O/cz.json $SP/cz_$T 10;;
 czn) run czn 1200 node $S/tools/czcheck.js $B $O/czn.json $SP/czn_$T 4 412 860 1;;
 czd2) run czd2 1200 node $S/tools/czcheck.js $B $O/czd2.json $SP/czd2_$T 4 1280 720 2;;
 zc) run zc 1500 node deliver/2026-11-17/perf/tools/zoomcycle.js $B $O/zc.json $SP/zc_$T 20;;
 ingame) run ingame 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json;;
 rules) run rules 1500 node qa_tools/rules_gate.js $B $O/rules.json;;
 people) run people 1800 node qa_tools/people_on_road.js $B $O/people.json;;
 stuck) run stuck 1800 node qa_tools/stuckmax.js $B 150 cz_$T;;
esac; done
echo done >> $O/DONE
