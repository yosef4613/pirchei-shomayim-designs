#!/bin/bash
# f9fix: עובד בתוך מקום אחד של התור — מריץ את העבודות שנשארו בתיקייה, אחת אחרי השנייה (mv = תפיסה אטומית)
J=$1; cd /home/user/tc_root/tc/pkg/work
while :; do f=$(ls $J/*.job 2>/dev/null | head -1); [ -z "$f" ] && exit 0; r=${f%.job}.run; mv "$f" "$r" 2>/dev/null || continue
  echo "$(TZ=Asia/Jerusalem date +%T) start $$" >> "$r.log"; bash "$r"; echo "$(TZ=Asia/Jerusalem date +%T) rc=$?" >> "$r.log"; mv "$r" "${f%.job}.done"; done
