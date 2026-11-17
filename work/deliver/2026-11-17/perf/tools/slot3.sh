#!/bin/bash
# slot3.sh — perf 17.11 (המתאם 12:50): במקום אחד בתור — (1) פרופיל של startMission הראשונה שמתחילה באמת (cand302x המשוחרר, try7163); (2) stuckmax 150 — try7163 ×2, try7162 ×3, cand300x ×2 (לסירוגין).
W=/home/user/tc_root/tc/pkg/work; cd $W; S=deliver/2026-11-17/perf; O=$S/qa/try7163; X=clean_r2b_025637/out/_try; L=$O/runs3.tsv
for b in try7163 try7162 cand300x; do [ -f $X/$b.html ] || zcat $X/$b.html.gz > $X/$b.html; done   # someone may have compressed them (the disk)
printf 'slot\t-\t-\t%s\n' "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L
t0=$(date +%s); timeout 600 node $S/tools/prof_start.js $O/prof_start.json $X/cand302x.html $X/try7163.html > $O/prof_start.log 2>&1; printf 'prof\t%s\t%s\t%s\n' $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L
i=0; for b in try7163 try7162 cand300x try7163 try7162 cand300x try7162; do i=$((i+1)); t0=$(date +%s); timeout 900 node qa_tools/stuckmax.js $X/$b.html 150 perf3_${b}_$i > $O/stuck3_${b}_$i.log 2>&1; printf 'stuck3-%s-%s\t%s\t%s\t%s\n' $b $i $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; done
echo done >> $L
