#!/bin/bash
# השוואת stuckmax: הבסיס (cand299x = master) מול try7007, באותו מקום בתור
W=/home/user/tc_root/tc/pkg/work; O=$W/deliver/2026-11-17/w17/qa/cmp; cd $W
for T in cand299x try7007 cand299x try7007; do n=$((n+1)); node qa_tools/stuckmax.js clean_r2b_025637/out/_try/$T.html 150 $T > $O/${n}_$T.json 2> $O/${n}_$T.err; echo "$n $T rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S) $(grep -o '"over5":[0-9]*,"busOver5":[0-9]*,"long":\[[^]]*' $O/${n}_$T.json | cut -c1-200)" >> $O/cmp.log; done
echo ALLDONE >> $O/cmp.log
