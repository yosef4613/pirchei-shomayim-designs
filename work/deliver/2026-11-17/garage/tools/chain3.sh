#!/bin/bash
# שרשרת 3 (garage): צילומי הבסיס S7F298 באותן נקודות (לפני / אחרי, כלל 16), ואז המסך על try6768
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/garage/qa; cd $W
while pgrep -f "chain2.sh" >/dev/null; do sleep 5; done
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gh_shot.js clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F298.html $Q/h_base298 0 > $Q/h_base298.log 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/garage/tools/gst_probe.js clean_r2b_025637/out/_try/try6768.html $Q/p_try6768 > $Q/p_try6768.log 2>&1
