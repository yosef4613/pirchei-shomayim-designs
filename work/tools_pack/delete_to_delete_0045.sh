#!/bin/bash
# 28.10 00:44 · הבעלים כתב "כן אני זמין למחיקה עכשיו" — מחיקת תיקיות _to_delete/ בלבד. רץ אחרי שהמדידה של S7F105 נגמרת (כדי לא להפריע לה).
cd /home/claude/work
until grep -q "MEASURE DONE" clean_r2b_025637/qa/s6p67/measure.log 2>/dev/null; do sleep 15; done
echo "before $(df -h . | tail -1 | awk '{print $4}') $(date +%H:%M)"
for d in ./_to_delete ./plan600/_to_delete ./clean_r2b_025637/_to_delete ./audit_v600_r7/_to_delete ./repro_step19/docs_plan/_to_delete ./verify_r19_2311/docs_plan/_to_delete ./audit_v600_r6/repro_s1/_to_delete ./audit_v600_r6/snap/_to_delete ./audit_v600_r6/repro_s2/_to_delete; do
  [ -d "$d" ] && du -sh "$d" && rm -rf "$d"
done
echo "after $(df -h . | tail -1 | awk '{print $4}') $(date +%H:%M)"
