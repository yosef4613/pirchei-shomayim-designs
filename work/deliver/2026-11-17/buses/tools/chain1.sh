#!/bin/bash
# chain1.sh <try> — buses (17.11): הבדיקות החוסמות על הניסיון, ואחריהן המדידה של האוטובוסים מול המכוניות (בסיס S7F299 מול הניסיון). דפדפן אחד בכל פעם, דרך התור.
W=/home/user/tc_root/tc/pkg/work; T=$1; D=$W/deliver/2026-11-17/buses; Q=$D/qa; cd $W
bash $D/tools/gate.sh $T
B0=$W/clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F299.html; B=$W/clean_r2b_025637/out/_try/$T.html
[ -s $Q/beh_base299.json ] || bash tools_pack/bslot.sh node $D/tools/q_busbeh.js $B0 $Q/beh_base299.json 420 600 > $Q/beh_base299.log 2>&1
bash tools_pack/bslot.sh node $D/tools/q_busbeh.js $B $Q/beh_${T}.json 420 600 > $Q/beh_${T}.log 2>&1
echo chain-done >> $Q/${T}_gate.txt
