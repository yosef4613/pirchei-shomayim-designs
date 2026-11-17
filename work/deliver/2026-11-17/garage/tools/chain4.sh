#!/bin/bash
# שרשרת (garage, אחרי ההפעלה מחדש): ניסיון אחד — המסך, האולם, והבדיקות החוסמות; דרך התור. שימוש: chain4.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/garage/qa; cd $W; T=$1
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gst_probe.js clean_r2b_025637/out/_try/$T.html $Q/p_$T > $Q/p_$T.log 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gh_shot.js clean_r2b_025637/out/_try/$T.html $Q/h_$T 0 > $Q/h_$T.log 2>&1
bash deliver/2026-11-17/garage/tools/gates.sh $T
echo "chain4 $T done $(TZ=Asia/Jerusalem date +%H:%M)" >> $Q/chain4.log
