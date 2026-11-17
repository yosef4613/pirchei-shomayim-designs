#!/bin/bash
# שימוש: run_suite2.sh tryNNNN [secs] [quick]
W=/home/user/tc_root/tc/pkg/work; mkdir -p $W/deliver/2026-11-17/island/qa/$1; echo "בתור $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $W/deliver/2026-11-17/island/qa/$1/log.txt
bash $W/tools_pack/bslot.sh bash $W/deliver/2026-11-17/island/tools/suite2_inner.sh "$@"
