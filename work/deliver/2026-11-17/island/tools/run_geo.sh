#!/bin/bash
W=/home/user/tc_root/tc/pkg/work; T=$W/deliver/2026-11-17/island/tools; B=$W/clean_r2b_025637/out/_try/$1.html; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl/geo_$1; mkdir -p $SH
cd $T && bash $W/tools_pack/bslot.sh env QMAX=200 node isl_shot.js $B $SH --q q_geo.js "wh:9060,7520,1.1" "shop:8590,7360,1.3" "plaza:8450,7330,0.8"
