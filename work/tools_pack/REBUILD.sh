#!/bin/bash
# 1.11.2026 · בנייה מחדש מהחבילה המלאה (Turbo_City_v648_FULL.zip), בתיקייה ריקה, ובדיקה שהכול יוצא זהה.
# שימוש: unzip Turbo_City_v648_FULL.zip -d new && cd new && bash REBUILD.sh
# 1. פורס את שלושת חלקי R23 ואת ה-SP לתיקייה work/.
# 2. tools/repro.sh — כל הבניות; docs_plan/tools/v600_replay.sh — כל גרסאות התוכנית.
# 3. משווה כל sha1 לערך שרשום בהערה "# → <sha1>" באותו קובץ. היציאה: מספר ההבדלים.
set -e
H=$PWD; W=$H/work; mkdir -p $W; cd $W
for p in 1 2 3; do python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall('.')" $H/source_R23/Turbo_City_v1_96_GATE77_S7F111_source_R23_part$p.zip; done; echo "R23 $(date +%H:%M)"
python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall('.')" $H/Turbo_City_GATE77_v648_R23_plus_SP.zip; echo "SP $(date +%H:%M)"
set +e
bash tools/repro.sh > repro.log 2>&1; echo "repro $? $(date +%H:%M)"
bash docs_plan/tools/v600_replay.sh > replay.log 2>&1; echo "replay $? $(date +%H:%M)"
python3 - <<'PY'
import re, hashlib, os, sys
def sha(p): return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:12]
bad = 0; n = 0
# the same lists as tools_pack/verify_v648.sh (older builds and plans are not reproducible byte for byte — they were never compared)
B = 'S7F117 S7F122 S7F128 S7F132 S7F133 S7F134 S7F135 S7F136 S7F137 S7F138 S7F139 S7F140 S7F141 S7F143 S7F146 S7F149 S7F150 S7F152 S7F153 S7F155 S7F156 S7F157 S7F158 S7F161 S7F162 S7F163 S7F164 S7F165 S7F166 S7F167 S7F169 S7F171 S7F172 S7F173 S7F174 S7F175 S7F176 S7F177 S7F178 S7F179'.split()
V = '6_23 6_24 6_25 6_26 6_27b 6_28 6_29 6_30 6_31b 6_32b 6_33 6_34 6_35 6_36 6_37 6_38 6_39 6_40 6_41'.split()
KEEP = ['GATE77_%s.html' % b for b in B] + ['Master_Plan_v%s.html' % v for v in V]
for src, root, pat in (('tools/repro.sh', '.', r'(out/Turbo_City_v1_96_GATE77_S7F\d+\.html)\s+# → ([0-9a-f]{12})'),
                       ('docs_plan/tools/v600_replay.sh', 'docs_plan', r'(out/Turbo_City_Master_Plan_v[0-9_a-z]+\.html)\s+# → ([0-9a-f]{12})')):
    for m in re.finditer(pat, open(src, encoding='utf-8').read()):
        f = os.path.join(root, m.group(1))
        if not any(k in f for k in KEEP): continue
        n += 1
        if not os.path.exists(f): print('חסר', f); bad += 1; continue
        if sha(f) != m.group(2): print('שונה', f, sha(f), 'צפוי', m.group(2)); bad += 1
print('נבדקו %d קבצים · הבדלים: %d' % (n, bad))
for f in ('out/Turbo_City_v1_96_GATE77_S7F177.html', 'docs_plan/out/Turbo_City_Master_Plan_v6_41.html'):
    print(f, sha(f) if os.path.exists(f) else 'חסר')
sys.exit(min(bad, 100))
PY
R=$?; echo "REBUILD DONE $(date +%H:%M) · הבדלים: $R"; exit $R
