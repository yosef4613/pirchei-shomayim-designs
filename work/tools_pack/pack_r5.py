#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""27.10 · חבילת המקור R5 (S7F84). העץ הנקי בלי build/ ו-out/ ובלי קובצי ה-ZIP הכבדים של הצילומים; ועוד: הודעות הבעלים מאז 25.10,
קבצי ההמשך (NEXT, PROGRESS, NOTES), מפת הדרכים R2, ותיקיית התוכנית החדשה (docs_plan/: הכלים, הנתונים, v5.62 המקורית, v6.00, הזהות).
לא מוחק כלום: מעתיק לתיקייה חדשה ואורז ממנה.
usage: pack_r4.py <out.zip>"""
import sys, os, shutil, glob, hashlib, zipfile, time
W = '/home/claude/work'; OUT = os.path.abspath(sys.argv[1]); T = os.path.join(W, 'pack_r5_' + time.strftime('%H%M%S')); os.makedirs(T)
def ign(d, names):
    out = set()
    rel = os.path.relpath(d, os.path.join(W, 'clean_r2b_025637'))
    if rel == '.': out |= {'build', 'out', '_to_delete'}
    out |= {n for n in names if n.startswith('owner_zones_') and n.endswith('.zip')}
    return out
shutil.copytree(os.path.join(W, 'clean_r2b_025637'), T, ignore=ign, dirs_exist_ok=True)
for f in glob.glob(os.path.join(W, 'src/docs_study/owner_2026-10-2[5-7]_*.txt')):
    dst = os.path.join(T, 'docs_study', os.path.basename(f))
    if not os.path.exists(dst): shutil.copy2(f, dst)
for f in ['study/NEXT_2026-10-27.md', 'study/PROGRESS_2026-10-27.md', 'study/NOTES.md', 'deliver/sp5/Turbo_City_ROADMAP_R2.md']:
    shutil.copy2(os.path.join(W, f), os.path.join(T, 'docs_study', os.path.basename(f)))
shutil.copytree(os.path.join(W, 'plan600'), os.path.join(T, 'docs_plan'), ignore=lambda d, n: ({'shots'} if d.endswith('/out') else set()) | ({'_to_delete'} if d.rstrip('/').endswith('plan600') else set()), dirs_exist_ok=True)
n = 0
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(T):
        dirs.sort()
        for fn in sorted(files):
            p = os.path.join(root, fn); z.write(p, os.path.relpath(p, T)); n += 1
b = open(OUT, 'rb').read()
print(T); print(OUT, hashlib.sha1(b).hexdigest(), len(b), 'bytes', n, 'files')
