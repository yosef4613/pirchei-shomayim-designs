#!/bin/bash
# מקום אחד בתור: הבדיקה המהירה של המזרח (q_east + l5a_run) ואז הבדיקות החוסמות — לניסיון אחד ($1)
W=/home/user/tc_root/tc/pkg/work; T=$W/deliver/2026-11-17/island/tools
mkdir -p $W/deliver/2026-11-17/island/qa/$1; echo "בתור $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $W/deliver/2026-11-17/island/qa/$1/log.txt
bash $W/tools_pack/bslot.sh bash $T/suite2_inner.sh $1 ${2:-1440}
