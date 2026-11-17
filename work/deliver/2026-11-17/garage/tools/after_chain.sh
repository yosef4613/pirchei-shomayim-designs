#!/bin/bash
# אחרי השרשרת: דגימה של מי שעובר באזור הקבלה (150 שנ׳) על try6764 — כלל 4
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/garage/qa; cd $W
while pgrep -f "chain.sh try6764" >/dev/null; do sleep 5; done
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gh_shot.js clean_r2b_025637/out/_try/try6764.html $Q/s_try6764 150 > $Q/s_try6764.log 2>&1
