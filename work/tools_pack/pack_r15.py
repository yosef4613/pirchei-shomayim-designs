#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""27.10 · חבילת המקור R15 (S7F88 — שלב 3, התוכנית v6.11). כמו R14, ועוד: p331–p334 (World‑a), הכלים tools/dev/w3*.py ו-worldshot.py, ‏qa/worlda/, ‏qa/s7f88/; בתוכנית — סגירת ביקורת 5 (v600_step14.py, ‏tools/swept.py, ‏tools/parkscan2.py, ‏data/parking_v2.json) ושלב 3 (v600_step15.py); ‏docs_audit/audit_v600_r5. מ-R14: חלקים ד, ה, ז אחרי ביקורת 4 (v600_step13.py, tools/dev/parkscan.py, qa/city/parking.json); מ-R13: S7F87 (p330 — השעון, tools/post_s7f87.txt, repro.sh), חלק א מגאומטריה (part_a_build.py), חלק ו אחרי ביקורת 4, v600_step12.py, ביקורת 4 (docs_audit/audit_v600_r4), qa/s7f87, qa/k86/airflow.json. R11 היה: חלק ו (docs_plan/data/part_f.json, docs_plan/tools/part_f_build.py, v600_step10.py), העובדות של השדה (qa/air, tools/dev/airgeo.js). R10 היה: חלק ה (docs_plan/data/part_e.json, docs_plan/tools/part_e_build.py, v600_step9.py), העובדות של העיר (qa/city, tools/dev/citygeo.js, peek.js). R9 היה: חלק ד (docs_plan/data/part_d.json, docs_plan/tools/part_d_build.py, v600_step8.py), העובדות של הים (qa/sea, tools/dev/seageo.js, seashots.js). R8 היה: p329 (K‑86), חלק א, הסקר הסופי. R7 היה: הביקורת השלישית (docs_audit/audit_v600_r3), כלי הסקר ונתוני הסקר (qa/survey — בלי חילוץ צילומי הזום, שנמצאים ב-ZIP של הצילומים, ובלי תמונות הביניים). R6 היה: ההודעות ששוחזרו מציטוט (ב6‑24), שתי הביקורות של v6.00 (docs_audit/). העץ הנקי בלי build/ ו-out/ ובלי קובצי ה-ZIP הכבדים של הצילומים; ועוד: הודעות הבעלים מאז 25.10,
קבצי ההמשך (NEXT, PROGRESS, NOTES), מפת הדרכים R2, ותיקיית התוכנית החדשה (docs_plan/: הכלים, הנתונים, v5.62 המקורית, v6.00, הזהות).
לא מוחק כלום: מעתיק לתיקייה חדשה ואורז ממנה.
usage: pack_r6.py <out.zip>"""
import sys, os, shutil, glob, hashlib, zipfile, time
W = '/home/claude/work'; OUT = os.path.abspath(sys.argv[1]); T = os.path.join(W, 'pack_r15_' + time.strftime('%H%M%S')); os.makedirs(T)
def ign(d, names):
    out = set()
    rel = os.path.relpath(d, os.path.join(W, 'clean_r2b_025637'))
    if rel == '.': out |= {'build', 'out', '_to_delete'}
    out |= {n for n in names if n.startswith('owner_zones_') and n.endswith('.zip')}
    if rel == os.path.join('qa', 'survey'): out |= {'zones84_zoom'}   # the zoom shots — extracted from the ZIP of the shots, which the owner has
    if rel == os.path.join('qa', 'survey', 's7f85_borders'): out |= {n for n in names if n.endswith('.jpg')}   # superseded by s7f85_borders_all (the same shots + the rest)
    if rel == os.path.join('qa', 'survey', 's7f85_activity'): out |= {n for n in names if n.endswith('.jpg')}   # the single frames; the sheets (sheets/) stay
    return out
shutil.copytree(os.path.join(W, 'clean_r2b_025637'), T, ignore=ign, dirs_exist_ok=True)
for f in glob.glob(os.path.join(W, 'src/docs_study/owner_2026-10-2[5-7]_*.txt')) + glob.glob(os.path.join(W, 'src/docs_study/owner_*_FROM_QUOTE.txt')):
    dst = os.path.join(T, 'docs_study', os.path.basename(f))
    if not os.path.exists(dst): shutil.copy2(f, dst)
for f in ['study/NEXT_2026-10-27.md', 'study/PROGRESS_2026-10-27.md', 'study/NOTES.md', 'deliver/sp5/Turbo_City_ROADMAP_R2.md']:
    shutil.copy2(os.path.join(W, f), os.path.join(T, 'docs_study', os.path.basename(f)))
shutil.copytree(os.path.join(W, 'plan600'), os.path.join(T, 'docs_plan'), ignore=lambda d, n: ({'shots'} if d.endswith('/out') else set()) | ({'_to_delete'} if d.rstrip('/').endswith('plan600') else set()), dirs_exist_ok=True)
for a in ('audit_v600', 'audit_v600_r2', 'audit_v600_r3', 'audit_v600_r4', 'audit_v600_r5'):
    if os.path.isdir(os.path.join(W, a)): shutil.copytree(os.path.join(W, a), os.path.join(T, 'docs_audit', a), ignore=lambda d, n: {'tmp', 'repro'}, dirs_exist_ok=True)   # repro/ — the auditor's own unpacked copy of the source package
n = 0
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(T):
        dirs.sort()
        for fn in sorted(files):
            p = os.path.join(root, fn); z.write(p, os.path.relpath(p, T)); n += 1
b = open(OUT, 'rb').read()
print(T); print(OUT, hashlib.sha1(b).hexdigest(), len(b), 'bytes', n, 'files')
