#!/bin/bash
# שני ניסיונות במקום אחד בתור: כל הבדיקות של $1, ואחריו cut_check של $2 (למשל ניסיון בדיקה עם ענף של סוכן אחר)
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/cutscenes/qa
bash $W/deliver/2026-11-17/cutscenes/tools/all1.sh $1
T=$2; L=$Q/gates_${T#try}.log; mkdir -p $Q/$T; cd $W
echo "== cut $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L; node deliver/2026-11-17/cutscenes/tools/cut_check.js clean_r2b_025637/out/_try/$T.html $Q/cut_${T#try}.json $Q/$T/shots > $Q/cut_${T#try}.log 2>&1; echo "cut rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
echo "== done $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
