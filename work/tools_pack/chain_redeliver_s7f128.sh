#!/bin/bash
# 28.10 20:04 · the package of S7F128 again, with the replay fix (REC_DIR — step28 reads the records of 16:30, step29 those of 19:33), and the
# verification in an empty folder again — after the rerun of the opening ("RERUN DONE"), so neither runs during a measurement. מריצים מקובץ בלבד.
W=/home/claude/work
until grep -q "RERUN DONE" $W/clean_r2b_025637/qa/chain_bootsave_rerun.log 2>/dev/null; do sleep 15; done; until [ ! -e $W/PERF_LOCK ]; do sleep 10; done
bash $W/tools_pack/deliver_s7f128.sh > $W/deliver_s7f128b.log 2>&1; echo "deliver $? $(date +%H:%M)"
bash $W/tools_pack/verify_s7f128.sh > $W/verify_s7f128b.log 2>&1; echo "verify $? $(date +%H:%M)"
echo "REDELIVER DONE $(date +%H:%M)"
