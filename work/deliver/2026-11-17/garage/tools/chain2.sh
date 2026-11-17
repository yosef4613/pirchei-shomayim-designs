#!/bin/bash
# שרשרת 2 (garage): הבסיס S7F298 ב-stuckmax 150 (להשוואה — כלל 4), ואז try6767: המסך, האולם, והבדיקות החוסמות
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/garage/qa; cd $W; T=try6767
while pgrep -f "after_chain.sh|gh_shot.js" >/dev/null; do sleep 5; done
mkdir -p $Q/base298; bash tools_pack/bslot.sh node qa_tools/stuckmax.js clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F298.html 150 base298 > $Q/base298/stuck.out 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gst_probe.js clean_r2b_025637/out/_try/$T.html $Q/p_$T > $Q/p_$T.log 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gh_shot.js clean_r2b_025637/out/_try/$T.html $Q/h_$T 0 > $Q/h_$T.log 2>&1
bash deliver/2026-11-17/garage/tools/gates.sh $T
