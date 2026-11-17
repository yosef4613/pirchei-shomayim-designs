#!/bin/bash
# 28.10 23:20 · המסירה של S7F132 / v6.24 ואחריה האימות בתיקייה ריקה. מריצים מקובץ בלבד.
W=/home/claude/work
until [ ! -e $W/PERF_LOCK ]; do sleep 10; done
bash $W/tools_pack/deliver_s7f132.sh > $W/deliver_s7f132.log 2>&1; echo "deliver $? $(date +%H:%M)"
bash $W/tools_pack/verify_s7f132.sh > $W/verify_s7f132.log 2>&1; echo "verify $? $(date +%H:%M)"
echo "DELIVER132 DONE $(date +%H:%M)"
