#!/bin/bash
# שרשרת (garage): דפדפן אחד בכל פעם — מחכה לצילומי h6762, ואז הבדיקה של המסך, צילומי האולם, והבדיקות החוסמות על הניסיון
W=/home/user/tc_root/tc/pkg/work; T=$1; Q=$W/deliver/2026-11-17/garage/qa; cd $W
while pgrep -f "gh_shot.js.*h6762" >/dev/null; do sleep 5; done
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gst_probe.js clean_r2b_025637/out/_try/$T.html $Q/p_$T > $Q/p_$T.log 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gh_shot.js clean_r2b_025637/out/_try/$T.html $Q/h_$T 0 > $Q/h_$T.log 2>&1
bash deliver/2026-11-17/garage/tools/gates.sh $T
