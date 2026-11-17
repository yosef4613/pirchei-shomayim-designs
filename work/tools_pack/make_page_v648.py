#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1.11.2026 · חבילת העבודה כדף ("חבילת העבודה טורבו סיטי").
דף יכול להחזיק עד 511 קבצים, והחבילה הרזה היא 2,081 קבצים — לכן כל תיקייה גדולה נארזת כ-tar.gz ומקודדת ל-base64 (טקסט),
בנתיב של התיקייה שלה; קובץ מעל 15 MB מפוצל לחלקים (.part1, .part2 ...). קבצי השורש נשארים כמו שהם.
MANIFEST.txt — כל קובץ של החבילה: הנתיב, sha1, הגודל, ובאיזה קובץ בדף הוא נמצא; ובראשו ההוראות.
שימוש: python3 tools_pack/make_page_v648.py  (מ-deliver/v648/lean_root אל deliver/v648/page)"""
import os, io, tarfile, base64, hashlib, json
D = '/home/claude/work/deliver/v648'; SRC = D + '/lean_root'; OUT = D + '/page'
LIMIT = 15 * 1024 * 1024
GROUPS = [('clean_r2b_025637/tools/patches', 'clean_r2b_025637/tools/patches.tgz.b64'),
          ('clean_r2b_025637/tools/dev', 'clean_r2b_025637/tools/dev.tgz.b64'),
          ('clean_r2b_025637/tools', 'clean_r2b_025637/tools/other.tgz.b64'),        # what is left in tools after patches/ and dev/
          ('clean_r2b_025637', 'clean_r2b_025637/root.tgz.b64'),                     # the base file GATE75, the READMEs, the agents' reports
          ('plan600', 'plan600.tgz.b64'), ('study', 'study.tgz.b64'), ('exp34', 'exp34.tgz.b64'),
          ('inbox_owner', 'inbox_owner.tgz.b64'), ('tools_pack', 'tools_pack.tgz.b64')]
ROOT_FILES = ['BOARD.md', 'DELETIONS.md', 'Turbo_City_HANDOFF_2026-11-01.md', 'REBUILD_LEAN.sh']
files = []
for r, ds, fs in os.walk(SRC):
    for f in fs: files.append(os.path.relpath(os.path.join(r, f), SRC))
files.sort()
where = {}
for f in files:
    if f in ROOT_FILES: where[f] = f; continue
    for pre, arc in GROUPS:
        if f.startswith(pre + '/'): where[f] = arc; break
    else: raise SystemExit('no group for ' + f)
os.makedirs(OUT, exist_ok=True)
out_files = []
def put(arc, data):
    p = os.path.join(OUT, arc); os.makedirs(os.path.dirname(p) or OUT, exist_ok=True); open(p, 'wb').write(data); out_files.append(arc)
for pre, arc in GROUPS:
    mem = sorted(f for f in files if where[f] == arc)
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode='w:gz', format=tarfile.PAX_FORMAT) as t:
        for f in mem:
            ti = t.gettarinfo(os.path.join(SRC, f), arcname=f); ti.mtime = 1793491200; ti.uid = ti.gid = 0; ti.uname = ti.gname = ''
            t.addfile(ti, open(os.path.join(SRC, f), 'rb'))
    b64 = base64.encodebytes(bio.getvalue())
    if len(b64) <= LIMIT: put(arc, b64)
    else:
        n = 0
        for i in range(0, len(b64), LIMIT): n += 1; put('%s.part%d' % (arc, n), b64[i:i + LIMIT])
for f in ROOT_FILES: put(f, open(os.path.join(SRC, f), 'rb').read())
sha = lambda b: hashlib.sha1(b).hexdigest()
tot = sum(os.path.getsize(os.path.join(SRC, f)) for f in files)
L = ['# רשימת הקבצים — חבילת העבודה טורבו סיטי (1.11.2026)', '',
     'החבילה הרזה: %d קבצים, %s בתים. בדף: %d קבצים (התיקיות הגדולות ארוזות כ-tar.gz ב-base64, כי דף מחזיק עד 511 קבצים).' % (len(files), format(tot, ','), len(out_files) + 3), '',
     '## איך מרכיבים ובונים', '',
     '1. קוראים מהדף את כל הקבצים לתיקייה ריקה, במבנה התיקיות של הדף (בכלי הדפים: read עם paths, לפי הרשימה "קבצים בדף" למטה).',
     '2. מריצים בתיקייה הזו: bash REBUILD_FROM_PAGE.sh',
     '   הסקריפט מחבר חלקים (.partN) אם יש, מפענח כל tgz.b64 ומחלץ אותו לתיקייה work/, מעתיק את קבצי השורש,',
     '   בודק את ה-sha1 של כל קובץ מול הרשימה הזו, ומריץ את REBUILD_LEAN.sh: בונה את S7F177, ‏S7F178, ‏S7F179, ‏B4A והתוכנית v6.41, ומשווה.',
     '3. צריך python3 ו-node. התוצאה הצפויה: "הבדלים: 0".', '',
     '## קבצים בדף', '']
for a in sorted(out_files):
    b = open(os.path.join(OUT, a), 'rb').read(); L.append('%s\t%s\t%d' % (a, sha(b), len(b)))
L += ['', '## כל קובצי החבילה (נתיב · sha1 · גודל · הקובץ בדף שבו הוא נמצא)', '']
for f in files:
    b = open(os.path.join(SRC, f), 'rb').read(); L.append('%s\t%s\t%d\t%s' % (f, sha(b), len(b), where[f]))
put('MANIFEST.txt', ('\n'.join(L) + '\n').encode('utf-8'))
json.dump({'files': {f: [sha(open(os.path.join(SRC, f), 'rb').read()), os.path.getsize(os.path.join(SRC, f)), where[f]] for f in files}},
          open(os.path.join(OUT, 'MANIFEST.json'), 'w', encoding='utf-8'), ensure_ascii=False)
out_files.append('MANIFEST.json')
print('page files', len(out_files), '·', sum(os.path.getsize(os.path.join(OUT, a)) for a in out_files), 'bytes · package files', len(files), '·', tot, 'bytes')
for a in sorted(out_files): print(' ', a, os.path.getsize(os.path.join(OUT, a)))
