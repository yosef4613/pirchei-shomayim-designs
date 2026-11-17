#!/bin/bash
# הכול בתוך מקום אחד בתור: bash bslot.sh bash all3.sh tryNNNN — השכבות (evt_busy), המסוקים והסירנה (heli_snd), והסט החוסם (gates2)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/qa/events/$T; D=$W/deliver/2026-11-17/events/tools; mkdir -p $O; cd $W
echo "busy start $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/busy.log
node $D/evt_busy.js $B $O/busy.json >> $O/busy.log 2>&1; echo "busy rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/busy.log
grep -q '^{"ok":true' $O/busy.log || { echo "busy not ok — stop" >> $O/busy.log; exit 3; }
bash $D/heli_snd.sh $T
bash $D/gates2.sh $T
