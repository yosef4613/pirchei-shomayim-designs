#!/bin/bash
# הכול בתוך מקום אחד בתור: bash bslot.sh bash all4.sh tryNNNN — השכבות (evt_busy) → הסט החוסם (gates2) → המסוקים והסירנה (heli_snd) → אבחון רכב שעומד (evt_still, מידע בלבד)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/qa/events/$T; D=$W/deliver/2026-11-17/events/tools; mkdir -p $O; cd $W
echo "busy start $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/busy.log
node $D/evt_busy.js $B $O/busy.json >> $O/busy.log 2>&1; echo "busy rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/busy.log
grep -q '^{"ok":true' $O/busy.log || { echo "busy not ok — stop" >> $O/busy.log; exit 3; }
bash $D/gates2.sh $T
bash $D/heli_snd.sh $T
mkdir -p $O/still; node $D/evt_still.js $B $O/still/still.json 300 $O/still/shots > $O/still/still.log 2>&1; echo "still rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/busy.log
echo ALL4DONE >> $O/busy.log
