#!/bin/bash
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/qa/events/$T; mkdir -p $O; cd $W
L=$O/gates.log; echo "rerun(after restart) $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/stuckmax.js $B 150 $T > $O/stuck.json 2> $O/stuck.err; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/people_on_road.js $B $O/por.json > $O/por.out 2>&1; echo "por rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
echo "data:image $(grep -c 'data:image' $B)" >> $L
echo ALLDONE >> $L
