#!/bin/bash
# chain2.sh <try> — buses (17.11): אחרי המדידה של הבסיס — הבדיקות החוסמות, stuckmax 1500 (עם האוטובוסים של הקווים), הלילה של הקווים, המדידה של הניסיון, והלילה של הבסיס. דפדפן אחד בכל פעם, דרך התור.
W=/home/user/tc_root/tc/pkg/work; T=$1; D=$W/deliver/2026-11-17/buses; Q=$D/qa; cd $W
B0=$W/clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F299.html; B=$W/clean_r2b_025637/out/_try/$T.html
while ! grep -q "^rc=" $Q/beh_base299.log 2>/dev/null; do sleep 20; done
bash $D/tools/gate.sh $T
bash tools_pack/bslot.sh node $D/tools/stuckmax_bus.js $B 1500 $T > $Q/${T}_stuck1500.json 2>&1; echo "stuck1500 rc=$?" >> $Q/${T}_gate.txt
bash tools_pack/bslot.sh node $D/tools/lines_night_tr2.js $B $Q/${T}_night.json > $Q/${T}_night.log 2>&1; echo "night rc=$?" >> $Q/${T}_gate.txt
bash tools_pack/bslot.sh node $D/tools/q_busbeh.js $B $Q/beh_${T}.json 420 600 > $Q/beh_${T}.log 2>&1; echo "beh rc=$?" >> $Q/${T}_gate.txt
[ -s $Q/base299_night.json ] || { bash tools_pack/bslot.sh node $D/tools/lines_night_tr2.js $B0 $Q/base299_night.json > $Q/base299_night.log 2>&1; echo "base-night rc=$?" >> $Q/${T}_gate.txt; }
echo chain-done >> $Q/${T}_gate.txt
