#!/bin/bash
# 29.10 · אימות השחזור של המסירה v6.29 בתיקייה ריקה: R23 (שלושת החלקים) ועליו ה-SP של v628 → repro.sh → v600_replay.sh;
# משווים את ה-sha1 לבניות ולתוכניות שנמסרו. רץ אחרי שהבדיקות המלאות של S7F139 נגמרו, ולא בזמן מדידה. מריצים מקובץ בלבד.
set -e
W=/home/claude/work; V=$W/verify_v628_$(date +%H%M); mkdir -p $V; cd $V; echo "dir $V"
for p in 1 2 3; do python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall('.')" $W/deliver/s7f111_r23/Turbo_City_v1_96_GATE77_S7F111_source_R23_part$p.zip; done; echo "R23 $(date +%H:%M)"
python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall('.')" $W/deliver/v628/Turbo_City_GATE77_v628_R23_plus_SP.zip; echo "SP $(date +%H:%M)"
bash tools/repro.sh > repro.log 2>&1; echo "repro $? $(date +%H:%M)"
for b in S7F117 S7F122 S7F128 S7F132 S7F133 S7F134 S7F135 S7F136 S7F137 S7F138 S7F139; do echo "$b $(sha1sum out/Turbo_City_v1_96_GATE77_$b.html | cut -c1-12) $(stat -c %s out/Turbo_City_v1_96_GATE77_$b.html)"; done
bash docs_plan/tools/v600_replay.sh > replay.log 2>&1; echo "replay $? $(date +%H:%M)"
for v in 6_23 6_24 6_25 6_26 6_27b 6_28 6_29; do echo "v$v $(sha1sum docs_plan/out/Turbo_City_Master_Plan_v$v.html | cut -c1-12) $(stat -c %s docs_plan/out/Turbo_City_Master_Plan_v$v.html)"; done
echo "VERIFY DONE $(date +%H:%M)"
