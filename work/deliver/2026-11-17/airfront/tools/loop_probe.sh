#!/bin/bash
# loop_probe.sh <build> <secs> <n> <tag> — n הרצות של af_probe ברצף, דרך התור (דפדפן אחד בכל פעם)
cd /home/user/tc_root/tc/pkg/work; A=deliver/2026-11-17/airfront
B=$1; S=$2; N=$3; T=$4; mkdir -p $A/qa/$T
for i in $(seq 1 $N); do
  bash tools_pack/bslot.sh node $A/tools/af_probe.js $B $S $A/qa/$T/p$i.json >> $A/qa/$T/runs.log 2>&1
  echo "--- $i $(TZ=Asia/Jerusalem date +%H:%M)" >> $A/qa/$T/runs.log
done
