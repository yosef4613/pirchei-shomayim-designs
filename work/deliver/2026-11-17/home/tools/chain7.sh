#!/bin/bash
# home (17.11): הרצה חוזרת של בדיקת הפנים בלבד על try8137
W=/home/user/tc_root/tc/pkg/work; cd $W; O=$W/deliver/2026-11-17/home/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad; L=$O/chain7.log; T(){ TZ=Asia/Jerusalem date +%H:%M; }
echo "start $(T)" >> $L; timeout 900 node deliver/2026-11-17/home/tools/home_in_q.js clean_r2b_025637/out/_try/try8137.html $O/try8137/home_in7.json $SP/sh7_try8137 > $O/try8137/home_in7.out 2>&1; echo "home_in try8137 rc=$? $(T)" >> $L
