#!/bin/bash
# מקום אחד בתור: try6733 (הענף — מהיר + החוסמות), ואחריו try6734 (השילוב עם fieldfix — השאילתות + q_ingame)
W=/home/user/tc_root/tc/pkg/work; T=$W/deliver/2026-11-17/island/tools
for x in try6733 try6734; do mkdir -p $W/deliver/2026-11-17/island/qa/$x; echo "בתור $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $W/deliver/2026-11-17/island/qa/$x/log.txt; done
bash $W/tools_pack/bslot.sh bash -c "bash $T/suite2_inner.sh try6733 1440; bash $T/cmb_inner.sh try6734"
