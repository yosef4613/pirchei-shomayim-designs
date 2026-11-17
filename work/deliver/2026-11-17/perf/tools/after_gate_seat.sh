#!/bin/bash
# after_gate_seat.sh <tryNNNN> — perf 17.11: אחרי הסט החוסם (DONE) — העלות של השומר של seatrees (seatBlockAsset / seatBlockKit) לפריים: perf_layers מ-10.11, פועל / כבוי באותו דף.
W=/home/user/tc_root/tc/pkg/work; cd $W; T=$1; O=deliver/2026-11-17/perf/qa/$T
while [ ! -f $O/DONE ]; do sleep 20; done
OFF=seatBlockAsset,seatBlockKit PLACES=drive,city,coast,cityzoom SEC=6 RUNS=1 bash tools_pack/bslot.sh timeout 1200 node deliver/2026-11-10/perf/tools/perf_layers.js $O/seat_layers.json clean_r2b_025637/out/_try/$T.html@src_game_t17_perf > $O/seat_layers.log 2>&1
echo "seat $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/DONE
