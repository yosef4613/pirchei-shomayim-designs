#!/bin/bash
# inslot.sh — airfront: רץ בתוך מקום אחד בתור (bslot) ומריץ ברצף את העבודות שבקובץ jobs.txt (שורה = פקודה); שורה שבוצעה עוברת ל-jobs_done.txt.
# כשאין עבודות — מחכה עד 90 שנ׳ לחדשות, ואז משחרר את המקום.
cd /home/user/tc_root/tc/pkg/work; T=deliver/2026-11-17/airfront/tools; J=$T/jobs.txt; idle=0
while :; do
  L=$(head -n1 $J 2>/dev/null)
  if [ -z "$L" ]; then idle=$((idle+3)); [ $idle -gt 90 ] && break; sleep 3; continue; fi
  idle=0; sed -i '1d' $J; echo "$(TZ=Asia/Jerusalem date +%H:%M:%S) start $L" >> $T/jobs_done.txt
  bash -c "$L"; echo "$(TZ=Asia/Jerusalem date +%H:%M:%S) end rc=$? $L" >> $T/jobs_done.txt
done
