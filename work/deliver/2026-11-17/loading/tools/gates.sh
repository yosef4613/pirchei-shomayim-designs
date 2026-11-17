#!/bin/bash
# gates.sh <game.html> <outdir> [phase...] — הבדיקות החוסמות דרך התור (bslot): ingame rules stuck people tcld tco
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; BS=$W/tools_pack/bslot.sh; T=$W/deliver/2026-11-17/loading/tools
G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); shift 2; PH="${*:-ingame rules stuck people tcld}"; cd $W; L=$O/runs.tsv
echo "$(basename $G) $(sha1sum $G | cut -c1-12) $(stat -c%s $G)" > $O/build.txt
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); bash $BS timeout $tmo "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" >> $L; }
for ph in $PH; do case $ph in
 ingame) run ingame 3000 node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json;;
 rules)  run rules 3000 node $Q/rules_gate.js $G $O/rules.json;;
 stuck)  run stuck 6000 node $Q/stuckmax.js $G 150 t17loading;;
 people) run people 6000 node $Q/people_on_road.js $G $O/people.json;;
 tcld)   run tcld 1800 node $T/tcld_test.js $G $O/tcld;;
tcofb)  run tcofb 1800 node $T/tcofb_test.js $G $O/tcofb $TCOFB_EXP;;
tb)     run tb 1800 node $T/tb_test.js $G $O/tb;;
fp)     run fp 900 node $T/fp_test.js $G $O/fp.json;;
 tco)    run tco 3600 node $W/deliver/2026-11-10/opening/tools/tco_test.js $G $O/tco.json;;
esac; done
echo "done $PH" >> $O/DONE
