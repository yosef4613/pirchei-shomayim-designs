#!/bin/bash
# 29.10 · מסירה — התוכנית v6.26, דף המפות v626, ובנייה האחרונה S7F134 (לבדיקה), עם חבילת פתיחה: R23 ועוד SP חדש — כל הקבצים של ה-SP
# הקודם (s7f132_v624) בגרסה הנוכחית שלהם, ועוד כל מה שנוסף מאז (p378, ‏p379, ספריית ה-3/4, הבדיקות של S7F133–S7F134, צעדי התוכנית 32–33,
# השרטוטים, הדמויות והמטוס לדוגמה, מסמך ההמשך R31, לוח העבודה, רישום המחיקות והודעות הבעלים). מעתיק לתיקיית מסירה חדשה — לא מוחק כלום.
# שימוש: bash tools_pack/nolock.sh bash tools_pack/deliver_v626.sh
set -e
W=/home/claude/work; G=$W/clean_r2b_025637; P=$W/plan600; D=$W/deliver/v626; mkdir -p $D
B=Turbo_City_v1_96_GATE77_S7F134
cp $G/out/$B.html $D/
(cd $D && python3 -c "import zipfile;z=zipfile.ZipFile('${B}_game.zip','w',zipfile.ZIP_DEFLATED);z.write('$B.html');z.close()")
cp $P/out/Turbo_City_Master_Plan_v6_26.html $P/out/Turbo_City_Maps_v625.html $D/
cp $W/study/PERF_BUDGET.md $W/study/PROGRESS_2026-10-27.md $W/study/Turbo_City_CONTINUE_R31.md $W/BOARD.md $W/DELETIONS.md $D/
(cd $W && python3 - <<'PY'
import zipfile, os, glob
G = 'clean_r2b_025637/'; OUT = 'deliver/v626/Turbo_City_GATE77_v626_R23_plus_SP.zip'
prev = zipfile.ZipFile('deliver/s7f132_v624/Turbo_City_GATE77_S7F132_R23_plus_SP.zip').namelist()
# the map of an archive name back to its source on disk (the layout of the previous SP)
def src_of(arc):
    if arc.startswith('docs_plan/'): return 'plan600/' + arc[len('docs_plan/'):]
    if arc.startswith('docs_study/'): return 'study/' + arc[len('docs_study/'):]
    if arc.startswith('tools_pack/'): return arc
    return G + arc
F = []; miss = []
for arc in prev:
    s = src_of(arc)
    if os.path.isfile(s): F.append((s, arc))
    else: miss.append(arc)
# what was added since S7F132
for pat in ['tools/patches/p378_*.py', 'tools/patches/p379_*.py', 'tools/patches/p380_*.py', 'tools/patches/x34/*.js', 'tools/post_s7f13[3-9].txt',
            'tools/dev/*s7f13[3-9]*', 'tools/dev/c34*.js', 'tools/dev/c34*.py', 'tools/dev/cmp_seeds12.py', 'tools/dev/gpu_who.js', 'tools/dev/w30measure.sh', 'tools/dev/w29measure.sh',
            'tools/repro.sh', 'inbox/*.md']:
    for p in glob.glob(G + pat):
        if os.path.isfile(p): F.append((p, p[len(G):]))
for d in ['qa/s7f133', 'qa/s7f134', 'qa/s7f135']:
    for p in glob.glob(G + d + '/**/*', recursive=True):
        if os.path.isfile(p) and not p.endswith('.png'): F.append((p, p[len(G):]))
for f in ['tools/v600_step32.py', 'tools/v600_step33.py', 'tools/maps3.py', 'tools/maps_page.py', 'tools/maps2.py', 'tools/build_v600.py', 'tools/v600_replay.sh',
          'data/stages.json', 'data/new.json', 'data/maps2.json', 'data/maps3.json', 'data/maps_e3.json', 'data/uses.json', 'data/owner_0218_E3_note.md']:
    if os.path.isfile('plan600/' + f): F.append(('plan600/' + f, 'docs_plan/' + f))
for p in glob.glob('study/e3/*') + glob.glob('study/pages/*.py') + glob.glob('study/pages/*.json') + glob.glob('study/pages/*.md'):
    if os.path.isfile(p) and '__pycache__' not in p: F.append((p, 'docs_study/' + p[len('study/'):]))
for f in ['study/Turbo_City_CONTINUE_R31.md', 'study/PERF_BUDGET.md', 'study/PROGRESS_2026-10-27.md']: F.append((f, 'docs_study/' + f[len('study/'):]))
for f in ['BOARD.md', 'DELETIONS.md']: F.append((f, 'docs_study/' + f))
for p in glob.glob('inbox_owner/*'): F.append((p, 'docs_study/' + p))
for p in glob.glob('exp34/people/*.py') + glob.glob('exp34/people/*.js') + glob.glob('exp34/people/p34_sample2.html') + glob.glob('exp34/air/*.py') + glob.glob('exp34/air/*.js') + glob.glob('exp34/air/air34_sample.html') + glob.glob('exp34/car/*.js') + glob.glob('exp34/car/*.py'):
    if os.path.isfile(p): F.append((p, p))
for f in ['tools_pack/nolock.sh', 'tools_pack/deliver_v626.sh']: F.append((f, f))
seen = set(); z = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED); n = 0
for s, arc in F:
    if arc in seen: continue
    seen.add(arc); z.write(s, arc); n += 1
z.close()
print('SP', OUT, n, 'files ·', os.path.getsize(OUT), 'bytes · missing from the previous SP:', len(miss), miss[:8])
PY
)
cd $D && sha1sum * | cut -c1-12,41- && ls -l | awk '{print $5, $9}'
