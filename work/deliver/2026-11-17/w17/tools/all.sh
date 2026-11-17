#!/bin/bash
# הכול בתור אחד: הבדיקה שלי (w17t) ואז הבדיקות החוסמות — bash bslot.sh bash all.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; cd $W
node deliver/2026-11-17/w17/tools/w17t.js clean_r2b_025637/out/_try/$T.html deliver/2026-11-17/w17/qa_${T#try}.json /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/s${T#try} > deliver/2026-11-17/w17/qa_${T#try}.log 2>&1
bash deliver/2026-11-17/w17/tools/gates.sh $T
