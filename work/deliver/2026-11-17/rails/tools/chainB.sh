#!/bin/bash
# rails 17.11 — שרשרת בדיקות ב׳ (דרך התור): people_on_road → stuckmax 150
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/rails/qa
cd $W
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/${T}_people.json > $O/${T}_people.log 2>&1
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 rails_$T > $O/${T}_stuck.log 2>&1
echo done
