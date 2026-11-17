#!/bin/bash
# 1.11.2026 · הרכבת חבילת העבודה מהקבצים של הדף "חבילת העבודה טורבו סיטי", ובנייה מחדש.
# שימוש: בתיקייה שאליה נקראו כל קובצי הדף, במבנה התיקיות שלהם: bash REBUILD_FROM_PAGE.sh
# 1. מחבר חלקים (X.partN → X), מפענח כל *.tgz.b64 ומחלץ לתיקייה work/.
# 2. מעתיק את קבצי השורש ל-work/.
# 3. בודק כל קובץ מול MANIFEST.json (sha1 וגודל).
# 4. מריץ את work/REBUILD_LEAN.sh — S7F177, ‏S7F178, ‏S7F179, ‏B4A והתוכנית v6.41, ומשווה ל-sha1 הצפוי.
set -e
H=$PWD; W=$H/work; mkdir -p $W
python3 - "$H" "$W" <<'PY'
import os, sys, glob, base64, tarfile, io, json, hashlib, shutil, re
H, W = sys.argv[1], sys.argv[2]
parts = {}
for p in glob.glob(H + '/**/*.tgz.b64.part*', recursive=True):
    m = re.match(r'(.*)\.part(\d+)$', p); parts.setdefault(m.group(1), []).append((int(m.group(2)), p))
blobs = {}
for base, ps in parts.items(): blobs[base] = b''.join(open(p, 'rb').read() for _, p in sorted(ps))
for p in glob.glob(H + '/**/*.tgz.b64', recursive=True):
    if p.startswith(W): continue
    blobs[p] = open(p, 'rb').read()
n = 0
for p, b in sorted(blobs.items()):
    with tarfile.open(fileobj=io.BytesIO(base64.decodebytes(b)), mode='r:gz') as t:
        t.extractall(W); n += len(t.getmembers())
for f in ('BOARD.md', 'DELETIONS.md', 'Turbo_City_HANDOFF_2026-11-01.md', 'REBUILD_LEAN.sh'):
    shutil.copy(os.path.join(H, f), os.path.join(W, f)); n += 1
M = json.load(open(os.path.join(H, 'MANIFEST.json'), encoding='utf-8'))['files']
bad = [f for f, (s, z, _) in M.items() if not os.path.isfile(os.path.join(W, f)) or os.path.getsize(os.path.join(W, f)) != z or hashlib.sha1(open(os.path.join(W, f), 'rb').read()).hexdigest() != s]
print('חולצו %d קבצים · ברשימה %d · לא תואמים: %d' % (n, len(M), len(bad)), bad[:10])
sys.exit(1 if bad else 0)
PY
cd $W && bash REBUILD_LEAN.sh
