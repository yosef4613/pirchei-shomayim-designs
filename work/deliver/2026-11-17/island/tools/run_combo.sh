#!/bin/bash
# מקום אחד בתור: הבדיקות החוסמות של המועמד ($1), ואחריהן הבדיקה המהירה של הניסיון הבא ($2: q_east + l5a_run) — דפדפן אחד בכל רגע
W=/home/user/tc_root/tc/pkg/work; T=$W/deliver/2026-11-17/island/tools
for x in $1 $2; do mkdir -p $W/deliver/2026-11-17/island/qa/$x; echo "בתור $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $W/deliver/2026-11-17/island/qa/$x/log.txt; done
bash $W/tools_pack/bslot.sh bash -c "bash $T/suite_inner.sh $1; bash $T/suite2_inner.sh $2 ${3:-1440} quick"
