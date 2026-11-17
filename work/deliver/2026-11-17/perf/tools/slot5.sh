#!/bin/bash
# slot5.sh — perf 17.11 15:20: A/B ל-AIR-FRONT — stuckmax 150 לסירוגין: try7164 (NPR פועל) / try7165 (אותו קוד, NPR כבוי), 3 × כל אחד.
W=/home/user/tc_root/tc/pkg/work; cd $W; O=deliver/2026-11-17/perf/qa/try7164; X=clean_r2b_025637/out/_try; L=$O/runs_ab.tsv
printf 'slot\t-\t-\t%s\n' "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L
i=0; for b in try7165 try7164 try7165 try7164 try7165 try7164; do i=$((i+1)); t0=$(date +%s); timeout 900 node qa_tools/stuckmax.js $X/$b.html 150 ab_${b}_$i > $O/ab_${b}_$i.log 2>&1; printf 'ab-%s-%s\t%s\t%s\t%s\n' $b $i $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; done
echo done >> $L
