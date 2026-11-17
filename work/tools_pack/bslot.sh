#!/bin/bash
# תור לדפדפן (11.11): המכונה — 4 ליבות ו-15 ג"ב; 12 דפדפנים יחד → קריסות (המותגים, 09:40).
# שימוש:  bash W/tools_pack/bslot.sh node qa_tools/xxx.js ...      (כל הרצה עם Chromium)
# המיזוג:  BSLOT_MERGE=1 bash W/tools_pack/bslot.sh ...            (עוקף את התור; מקום 6 שמור לו)
# 17.11 09:50: OOM עם 8 דפדפנים (merge2) — דף של 26–29 מ"ב מגיע ל-~3 ג"ב.
# 17.11 13:40 (המתאם, בקשת הבעלים "להגדיל באחד או שניים"): (1) תור הוגן — מי שחיכה ראשון נכנס ראשון (כרטיסים ב-q/);
#   קודם כל ממתין ניסה באקראי כל 5 שנ׳, וחלק חיכו שעתיים. (2) מקום 5 לכולם — רק כשיש בזיכרון לפחות BSLOT_MEMK (6.5 ג"ב פנויים).
#   מקום 6 — רק למיזוג, באותו תנאי זיכרון. מקומות 1–4 תמיד.
D=/tmp/tc_bslot; Q=$D/q; mkdir -p $Q
MEMK=${BSLOT_MEMK:-7000000}; MEMK6=${BSLOT_MEMK6:-6000000}   # 13:25: שני OOM של הקבוצה (13:10, 13:13) עם 6 דפדפנים — סף מחמיר
t0=$(date +%s)
memok(){ [ "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" -ge "$MEMK" ]; }
TK=""
if [ "$BSLOT_MERGE" != 1 ]; then TK=$Q/$(date +%s%N).$$; : > "$TK"; trap 'rm -f "$TK"' EXIT; fi
first(){ # הכרטיס הוותיק שהתהליך שלו עוד חי
  local f
  for f in $(ls "$Q" 2>/dev/null | sort); do
    if kill -0 "${f##*.}" 2>/dev/null; then echo "$Q/$f"; return; fi
    rm -f "$Q/$f"
  done
}
while :; do
  if [ "$BSLOT_MERGE" = 1 ]; then SL="6 1 2 3 4 5"; else SL=""; [ "$(first)" = "$TK" ] && SL="1 2 3 4 5"; fi
  for i in $SL; do
    if [ "$i" = 5 ] && ! memok; then continue; fi; if [ "$i" = 6 ] && [ "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" -lt "$MEMK6" ]; then continue; fi
    exec 9>$D/$i.lock
    if flock -n 9; then
      [ -n "$TK" ] && rm -f "$TK"
      w=$(( $(date +%s) - t0 )); [ $w -gt 5 ] && echo "[bslot] מקום $i אחרי ${w} שנ׳" >&2
      "$@"; rc=$?; flock -u 9; exit $rc
    fi
    exec 9>&-
  done
  sleep 3
done
