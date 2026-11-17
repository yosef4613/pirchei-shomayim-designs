#!/bin/bash
W=/home/user/tc_root/tc/pkg/work; cd $W; S=deliver/2026-11-17/sealife
timeout 900 node $S/tools/sl_ship.js clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F299.html $S/qa/ship_base.json > $S/qa/ship_base.log 2>&1
timeout 900 node $S/tools/sl_ship.js clean_r2b_025637/out/_try/$1.html $S/qa/ship_$1.json > $S/qa/ship_$1.log 2>&1
echo done > $S/qa/ship_ab.done
