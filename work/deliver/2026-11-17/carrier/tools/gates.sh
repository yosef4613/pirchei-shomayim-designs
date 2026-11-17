#!/bin/bash
# gates.sh <tryNNNN> <phase...> — הבדיקות של carrier (17.11) על ניסיון אחד, אחת אחרי השנייה, דרך התור (bslot)
#   phases: flow ingame rules people stuck
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; BS=$W/tools_pack/bslot.sh; CT=$W/deliver/2026-11-17/carrier/tools
N=$1; shift; G=$W/clean_r2b_025637/out/_try/$N.html; O=$W/deliver/2026-11-17/carrier/qa/$N; mkdir -p $O; cd $W; L=$O/runs.tsv
echo "$N $(sha1sum $G | cut -c1-12) $(stat -c%s $G) data:image=$(grep -c 'data:image' $G)" > $O/build.txt
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo bash $BS "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
for ph in "$@"; do case $ph in
 flow)   run flow 5400 node $CT/q_import_flow_d3.js $G $O/flow.json 3300;;
 ingame) run ingame 3600 node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json;;
 rules)  run rules 3600 node $Q/rules_gate.js $G $O/rules.json;;
 people) run people 6000 node $Q/people_on_road.js $G $O/people.json;;
 stuck)  run stuck 6000 node $Q/stuckmax.js $G 150 t17carrier;;
esac; done
echo "done $*" >> $O/DONE
