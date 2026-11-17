#!/bin/bash
# fwhm2.sh — merge3: q_fwhm.js על S7F301 (cand301z) ועל S7F302 (cand302x), ברצף במקום אחד בתור.
W=/home/user/tc_root/tc/pkg/work; O=$W/deliver/2026-11-17/merge3/qa; cd $W
for n in cand301z cand302x; do t0=$(date +%s); timeout 600 node qa_tools/probe_c2.js clean_r2b_025637/out/_try/$n.html deliver/2026-11-17/merge3/tools/q_fwhm.js $O/fwhm_$n.json > $O/fwhm_$n.log 2>&1; printf 'fwhm_%s\t%s\t%s\t%s\n' $n $? $(( $(date +%s)-t0 )) "$(TZ=Asia/Jerusalem date +%H:%M)" >> $O/fwhm_runs.tsv; done
