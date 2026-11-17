#!/bin/bash
# 27.10 · חבילת המקור R4 (S7F83): העץ הנקי בלי build/ ו-out/, בלי קובצי ה-ZIP הגדולים של הצילומים; ועוד: הודעות הבעלים מאז 25.10,
# קבצי ההמשך (NEXT, PROGRESS, NOTES), מפת הדרכים R2, ותיקיית התוכנית החדשה (docs_plan/: הכלים, הנתונים, v5.62 המקורית, v6.00, הזהות).
# שימוש: bash tools_pack/pack_r4.sh <out.zip>   — לא מוחק כלום; עובד על עותק בתיקייה חדשה.
set -e
OUT=$(readlink -f "$1"); W=/home/claude/work; T=$W/pack_r4_$(date +%H%M%S); mkdir -p $T
cd $W/clean_r2b_025637
# העץ הנקי (בלי build/ out/ והצילומים הכבדים)
find . -type f ! -path './build/*' ! -path './out/*' ! -name 'owner_zones_*.zip' ! -path './_to_delete/*' -print0 | cpio -0 -pdm --quiet $T
# הודעות הבעלים ומסמכי ההמשך
cp -n $W/src/docs_study/owner_2026-10-2[5-7]_*.txt $T/docs_study/ 2>/dev/null || true
cp $W/study/NEXT_2026-10-27.md $W/study/PROGRESS_2026-10-27.md $W/study/NOTES.md $T/docs_study/
cp $W/deliver/sp5/Turbo_City_ROADMAP_R2.md $T/docs_study/
# התוכנית החדשה
mkdir -p $T/docs_plan && cd $W/plan600 && find . -type f ! -path './out/shots/*' -print0 | cpio -0 -pdm --quiet $T/docs_plan
cd $T && zip -q -X -r "$OUT" . && echo "$T" && sha1sum "$OUT" && stat -c '%s bytes' "$OUT" && unzip -l "$OUT" | tail -1
