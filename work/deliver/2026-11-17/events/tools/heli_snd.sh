#!/bin/bash
# המסוקים + הנפילה (evt_heli.js) ואחריה הסירנה (evt_snd.js), באותו מקום של התור: bash bslot.sh bash heli_snd.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/qa/events/$T; mkdir -p $O; cd $W
echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/hs.log
node deliver/2026-11-17/events/tools/evt_heli.js $B $O/heli.json $O/shots 300 > $O/heli.log 2>&1; echo "heli rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/hs.log
node deliver/2026-11-17/events/tools/evt_snd.js $B $O/snd.json > $O/snd.log 2>&1; echo "snd rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/hs.log
echo ALLDONE >> $O/hs.log
