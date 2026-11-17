#!/bin/bash
# people_on_road שוב: try7008 ואז הבסיס cand300x (S7F300), באותו מקום בתור
W=/home/user/tc_root/tc/pkg/work; O=$W/deliver/2026-11-17/w17/qa/por2; mkdir -p $O; cd $W
for T in try7008 cand300x; do node qa_tools/people_on_road.js clean_r2b_025637/out/_try/$T.html $O/$T.json > $O/$T.out 2>&1; echo "$T rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S) $(head -c 160 $O/$T.out | head -1)" >> $O/por2.log; done
echo ALLDONE >> $O/por2.log
