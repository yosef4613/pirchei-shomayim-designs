#!/bin/bash
# מקום אחד בתור: $1 — מהיר + החוסמות; ואחריו $2 — מהיר בלבד
W=/home/user/tc_root/tc/pkg/work; T=$W/deliver/2026-11-17/island/tools
for x in $1 $2; do mkdir -p $W/deliver/2026-11-17/island/qa/$x; echo "בתור $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $W/deliver/2026-11-17/island/qa/$x/log.txt; done
bash $W/tools_pack/bslot.sh bash -c "bash $T/suite2_inner.sh $1 1440; bash $T/suite2_inner.sh $2 1440 quick"
