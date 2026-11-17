#!/bin/bash
# השוואה: מה חוסם את המדרכה של הגשר — try6738 בלי שחרור (_src) מול המועמד cand302x (master + גל 3, בלי הצומת)
W=/home/user/tc_root/tc/pkg/work; O=$W/deliver/2026-11-17/island/qa/pole; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl/pole; mkdir -p $O $SH; cd $W/deliver/2026-11-17/island/tools
for B in try6738_src cand302x; do QMAX=4000 node isl_shot.js $W/clean_r2b_025637/out/_try/$B.html $SH/$B --wait 20000 --q q_pole.js > $O/$B.out 2>&1; echo "$B rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; done
