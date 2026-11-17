#!/bin/bash
# slot4.sh — perf 17.11 (המתאם 14:20): try7164 (d73630c — הקול אחרי הקליק, החימום, ההד והרעשים בהצגה) במקום אחד בתור:
#  (1) q_start2 / q_start2w — startMission הראשונה ו-TCSND.ensure, על try7164 ועל cand302x (הבסיס); (2) q_voiceint ו-q_nv (nfkiss — הפענוח של ההקלטות) על try7164 ועל try7164r (המשוחרר, release_strip);
#  (3) q_ingame, rules_gate, people_on_road, stuckmax 150, זום ×20 על try7164.
W=/home/user/tc_root/tc/pkg/work; cd $W; S=deliver/2026-11-17/perf; O=$S/qa/try7164; X=clean_r2b_025637/out/_try; L=$O/runs.tsv; N=deliver/2026-11-17/nfkiss/tools; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
run(){ local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo "$@" > $O/$nm.log 2>&1; printf '%s\t%s\t%s\t%s\n' $nm $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
printf 'slot\t-\t-\t%s\n' "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L
for b in try7164 cand302x; do run start2_$b 300 node qa_tools/probe_c2.js $X/$b.html $S/tools/q_start2.js $O/start2_$b.json; run start2w_$b 300 node qa_tools/probe_c2.js $X/$b.html $S/tools/q_start2w.js $O/start2w_$b.json; done
for b in try7164 try7164r; do run voiceint_$b 900 node deliver/2026-11-17/voiceint/tools/q_voiceint.js $X/$b.html $O/voiceint_$b.json; run nv_$b 900 node qa_tools/probe_c2.js $X/$b.html $N/q_nv.js $O/nv_$b.json; done
run ingame 1500 node qa_tools/probe_c2.js $X/try7164.html qa_tools/q_ingame.js $O/ingame.json
run rules 1500 node qa_tools/rules_gate.js $X/try7164.html $O/rules.json
run people 1800 node qa_tools/people_on_road.js $X/try7164.html $O/people.json
run stuck 1800 node qa_tools/stuckmax.js $X/try7164.html 150 perf_try7164
QX=$W/$S/tools/q_nav.js run zc 1500 node $S/tools/zoomcycle.js $X/try7164.html $O/zc.json $SP/zc_try7164 20
echo done >> $L
