#!/bin/bash
# 28.10 23:10 · אימות השחזור של המסירה S7F132 / v6.24 בתיקייה ריקה: R23 (שלושת החלקים מ-deliver/s7f111_r23) ועליו ה-SP החדש → repro.sh → v600_replay.sh;
# משווים את ה-sha1 לתוצרים שנמסרו. מריצים מקובץ בלבד.
set -e
W=/home/claude/work; V=$W/verify_s7f132_$(date +%H%M); mkdir -p $V; cd $V; echo "dir $V"
for p in 1 2 3; do python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall('.')" $W/deliver/s7f111_r23/Turbo_City_v1_96_GATE77_S7F111_source_R23_part$p.zip; done; echo "R23 $(date +%H:%M)"
python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall('.')" $W/deliver/s7f132_v624/Turbo_City_GATE77_S7F132_R23_plus_SP.zip; echo "SP $(date +%H:%M)"
bash tools/repro.sh > repro.log 2>&1; echo "repro $? $(date +%H:%M)"
for b in S7F117 S7F119 S7F120 S7F121 S7F122 S7F123 S7F124 S7F125 S7F126 S7F127 S7F128 S7F129 S7F130 S7F131 S7F132; do echo "$b $(sha1sum out/Turbo_City_v1_96_GATE77_$b.html | cut -c1-12) $(stat -c %s out/Turbo_City_v1_96_GATE77_$b.html)"; done
bash docs_plan/tools/v600_replay.sh > replay.log 2>&1; echo "replay $? $(date +%H:%M)"
for v in 6_19 6_20 6_21 6_22 6_23 6_24; do echo "v$v $(sha1sum docs_plan/out/Turbo_City_Master_Plan_v$v.html | cut -c1-12) $(stat -c %s docs_plan/out/Turbo_City_Master_Plan_v$v.html)"; done
grep -n "→" replay.log | head -0
echo "VERIFY DONE $(date +%H:%M)"
