#!/bin/bash
# gate.sh <tryNNNN> <what...> — perf 17.11: הכול במקום אחד של התור (bash W/tools_pack/bslot.sh bash gate.sh ...).
# what: zc (זום ×20 + ניווט + מסך צר) · zcq (זום ×6 בלי מסך צר) · ingame · rules · people · stuck · nav (navday: הניווט, startMission, יום של הלוח, הדקלים) · nav4base (רק הדקלים, על הבסיס try7160) · callers (מי קורא ל-navPoiRegistry) · mem (memcmp — הזיכרון בתרחיש של people_on_road)
W=/home/user/tc_root/tc/pkg/work; cd $W; S=deliver/2026-11-17/perf; T=$1; shift; B=clean_r2b_025637/out/_try/$T.html; O=$S/qa/$T; mkdir -p $O; L=$O/runs.tsv
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
run(){ local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo "$@" > $O/$nm.log 2>&1; printf '%s\t%s\t%s\t%s\n' $nm $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
for w in "$@"; do case $w in
 zc) QX=$W/$S/tools/q_nav.js run zc 1500 node $S/tools/zoomcycle.js $B $O/zc.json $SP/zc_$T 20;;
 zcbase) QX=$W/$S/tools/q_nav.js run zcbase 1200 node $S/tools/zoomcycle.js clean_r2b_025637/out/_try/try7160.html $O/zcbase.json $SP/zcb_$T 8 1920 953 1 0;;
 zcq) QX=$W/$S/tools/q_nav.js run zcq 1200 node $S/tools/zoomcycle.js $B $O/zcq.json $SP/zcq_$T 6 1920 953 1 0;;
 nav) run nav 1200 node $S/tools/navday.js $B $O/nav.json 110;;
 nav4base) zcat clean_r2b_025637/out/_try/try7160.html.gz > $SP/try7160_base.html && ND_ONLY=ph4 run nav4base 600 node $S/tools/navday.js $SP/try7160_base.html $O/nav4base.json; rm -f $SP/try7160_base.html;;
 callers) run callers 600 node qa_tools/probe_c2.js $B $S/tools/q_callers.js $O/callers.json;;
 mem) T=300 run mem 900 node $S/tools/memcmp.js $O/memcmp.json $B;;
 acc) run acc 900 node qa_tools/probe_c2.js $B $S/tools/q_accept.js $O/accept.json;;
 ingame) run ingame 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json;;
 rules) run rules 1500 node qa_tools/rules_gate.js $B $O/rules.json;;
 people) run people 1800 node qa_tools/people_on_road.js $B $O/people.json;;
 stuck) run stuck 1800 node qa_tools/stuckmax.js $B 150 perf_$T;;
esac; done
echo done >> $O/DONE
