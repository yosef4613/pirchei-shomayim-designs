#!/bin/bash
# island5: צילומים ושאילתות על ניסיון (לעצמי): shots.sh tryNNNN [שאילתה נוספת]
W=/home/user/tc_root/tc/pkg/work; T=$1; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl5/s_$T; mkdir -p $SH
cd $W/deliver/2026-11-17/island/tools && QMAX=6000 SHOT_WAIT=1800 node isl_shot.js $W/clean_r2b_025637/out/_try/$T.html $SH --wait 9000 --q ../tools5/q_f6new.js ${2:+--q $2} "a:7000,5110,0.9" "b:7000,5110,0.45" "w:7000,5000,0.22" "z:7000,5160,1.6" "n:7000,5110,0.9,1" "p:6950,4650,0.4"
# הציור (לבדיקה בעין שלי): הסעיפים 0ג ו-0ד בדף קטן
node $W/deliver/2026-11-17/island/tools/page_shot.js /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl5/plan_check.html $SH/plan_check.jpg 1600 1
