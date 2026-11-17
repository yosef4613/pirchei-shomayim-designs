#!/bin/bash
# צילומים בלבד (לעצמי): לולאת המזרח והמפתח — try$1
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl/shots2_$TRY; mkdir -p $SH; cd $W/deliver/2026-11-17/island/tools
node isl_shot.js $B $SH --wait 15000 "loop:9190,7130,0.9" "loopz:9380,7250,1.6" "lift:6700,6060,1.6" > $SH/out.txt 2>&1; echo "rc=$?" >> $SH/out.txt
