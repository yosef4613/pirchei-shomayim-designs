#!/bin/bash
# 29.10 19:30 · v634b — אותה מסירה כמו v634, עם SP מתוקן: ב-v634 חסר tools/post_s7f150.txt (התבנית post_s7f14[0-9]), ולכן השחזור של S7F150 נכשל באימות (19:27). 29.10 19:00 · מסירה (ביניים) — S7F150 (הצי במידות האמיתיות p396, הכנה מראש p397, רכבי השדה והחווה p392; 2 בדיקות עולם נכשלות — ראו qa/s7f150/predeliver.md), התוכנית v6.32b, דף המפות v631, עם חבילת פתיחה:
# R23 ועוד SP חדש — כל הקבצים של ה-SP הקודם (v633) בגרסה הנוכחית שלהם, ועוד מה שנוסף מאז (צעד 38, הרשימה הקבועה לפני מסירה, p390 / p391 כמקור, census3, דף החרטום). לא מוחק כלום.
# שימוש: bash tools_pack/nolock.sh bash tools_pack/deliver_v634b.sh
set -e
W=/home/claude/work; G=$W/clean_r2b_025637; P=$W/plan600; D=$W/deliver/v634b; mkdir -p $D
B=Turbo_City_v1_96_GATE77_S7F150
cp $G/out/$B.html $D/
(cd $D && python3 -c "import zipfile;z=zipfile.ZipFile('${B}_game.zip','w',zipfile.ZIP_DEFLATED);z.write('$B.html');z.close()")
cp $P/out/Turbo_City_Master_Plan_v6_32b.html $P/out/Turbo_City_Maps_v631.html $D/
cp $W/study/PERF_BUDGET.md $W/study/PROGRESS_2026-10-27.md $W/study/Turbo_City_CONTINUE_R31.md $W/BOARD.md $W/DELETIONS.md $D/
(cd $W && python3 - <<'PY'
import zipfile, os, glob
G = 'clean_r2b_025637/'; OUT = 'deliver/v634b/Turbo_City_GATE77_v634b_R23_plus_SP.zip'
prev = zipfile.ZipFile('deliver/v633/Turbo_City_GATE77_v633_R23_plus_SP.zip').namelist()
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
for pat in ['tools/patches/p378_*.py', 'tools/patches/p379_*.py', 'tools/patches/p380_*.py', 'tools/patches/p38[1-9]_*.py', 'tools/patches/p39[0-9]_*.py', 'tools/patches/x34/*.js', 'tools/post_s7f13[3-9].txt', 'tools/post_s7f14[0-9].txt', 'tools/dev/*.js', 'tools/dev/*.sh',
            'tools/dev/*s7f13[3-9]*', 'tools/dev/c34*.js', 'tools/dev/*s7f13[5-9]*', 'tools/dev/c34*.py', 'tools/dev/cmp_seeds12.py', 'tools/dev/gpu_who.js', 'tools/dev/w30measure.sh', 'tools/dev/w29measure.sh',
            'tools/repro.sh', 'tools/dev/c34census3.js', 'qa/census3/*.json', 'tools/patches/x34/*.js', 'tools/post_s7f14[0-9].txt', 'tools/post_s7f1[5-9][0-9].txt', 'tools/patches/p4[0-9][0-9]_*.py', 'tools/dev/acfit.js', 'tools/dev/pushturnqa.js', 'tools/dev/r22qa.js', 'tools/dev/measure_s7f14*.sh', 'inbox/*.md']:
    for p in glob.glob(G + pat):
        if os.path.isfile(p): F.append((p, p[len(G):]))
for d in ['qa/s7f149', 'qa/s7f150', 'qa/census3', 'qa/s7f144', 'qa/s7f145', 'qa/s7f146', 'qa/s7f147', 'qa/s7f148', 'qa/r22', 'qa/s7f142', 'qa/s7f143', 'qa/s7f133', 'qa/s7f134', 'qa/s7f135', 'qa/s7f136', 'qa/s7f137', 'qa/s7f138', 'qa/s7f139', 'qa/s7f140', 'qa/s7f141', 'qa/bldshadow']:
    for p in glob.glob(G + d + '/**/*', recursive=True):
        if os.path.isfile(p) and not p.endswith('.png') and not (p.endswith('.html') and '/build/' in p): F.append((p, p[len(G):]))   # 15:20: local builds that were not delivered stay out
for f in ['tools/v600_step32.py', 'tools/v600_step33.py', 'tools/v600_step34.py', 'tools/v600_step35.py', 'tools/v600_step36.py', 'tools/v600_step37.py', 'tools/v600_step38.py', 'tools/maps3.py', 'tools/maps_page.py', 'tools/maps2.py', 'tools/build_v600.py', 'tools/v600_replay.sh',
          'data/stages.json', 'data/new.json', 'data/maps2.json', 'data/maps3.json', 'data/maps_e3.json', 'data/maps_logos.json', 'data/maps_b4.json', 'data/uses.json', 'data/owner_0218_E3_note.md']:
    if os.path.isfile('plan600/' + f): F.append(('plan600/' + f, 'docs_plan/' + f))
for f in ['tools/v600_step39.py']:
    if os.path.isfile('plan600/' + f): F.append(('plan600/' + f, 'docs_plan/' + f))
for p in glob.glob('study/e3/*') + glob.glob('study/logos/*') + glob.glob('study/b4/*.py') + glob.glob('study/b4/*.js') + glob.glob('study/b4/*.json') + glob.glob('study/pages/*.py') + glob.glob('study/pages/*.json') + glob.glob('study/pages/*.md'):
    if os.path.isfile(p) and '__pycache__' not in p: F.append((p, 'docs_study/' + p[len('study/'):]))
for f in ['study/Turbo_City_CONTINUE_R31.md', 'study/PERF_BUDGET.md', 'study/PROGRESS_2026-10-27.md']: F.append((f, 'docs_study/' + f[len('study/'):]))
for f in ['BOARD.md', 'DELETIONS.md']: F.append((f, 'docs_study/' + f))
for p in glob.glob('inbox_owner/*'): F.append((p, 'docs_study/' + p))
for p in glob.glob('exp34/people/*.py') + glob.glob('exp34/people/*.js') + glob.glob('exp34/people/p34_sample2.html') + glob.glob('exp34/air/*.py') + glob.glob('exp34/air/*.js') + glob.glob('exp34/air/air34_sample.html') + glob.glob('exp34/air/nose_sample_pub.html') + glob.glob('exp34/air/nose_options.html') + glob.glob('exp34/air/fleet_table.md') + glob.glob('exp34/air/fleet_compare_pub.html') + glob.glob('exp34/air/dev/*.py') + glob.glob('exp34/air/dev/*.js') + glob.glob('exp34/air/ref/*') + glob.glob('exp34/car/*.js') + glob.glob('exp34/car/src/*.js') + glob.glob('exp34/car/dev/*.html') + glob.glob('exp34/car/*.py') + glob.glob('exp34/kit/*.js') + glob.glob('exp34/kit/*.py') + glob.glob('exp34/kit/kit34_sample.html') + glob.glob('exp34/kit/dev/*') + glob.glob('exp34/bld/*.js') + glob.glob('exp34/bld/*.py') + glob.glob('exp34/bld/*.html'):
    if os.path.isfile(p): F.append((p, p))
for f in ['tools_pack/nolock.sh', 'tools_pack/deliver_v626.sh', 'tools_pack/deliver_v627.sh', 'tools_pack/deliver_v628.sh', 'tools_pack/deliver_v629.sh', 'tools_pack/verify_v629.sh', 'tools_pack/deliver_v631.sh', 'tools_pack/verify_v631.sh', 'tools_pack/deliver_v632.sh', 'tools_pack/verify_v632.sh', 'tools_pack/deliver_v633.sh', 'tools_pack/verify_v633.sh', 'tools_pack/deliver_v634.sh', 'tools_pack/verify_v634.sh', 'tools_pack/deliver_v634b.sh', 'tools_pack/verify_v634b.sh', 'tools_pack/predeliver.sh', 'tools_pack/predeliver_cmp.py', 'tools_pack/verify_v626.sh', 'tools_pack/verify_v627.sh', 'tools_pack/verify_v628.sh']:
    if os.path.isfile(f): F.append((f, f))
for p in glob.glob('qa/review/*.md'): F.append((p, 'docs_study/' + p))
seen = set(); z = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED); n = 0
for s, arc in F:
    if arc in seen: continue
    seen.add(arc); z.write(s, arc); n += 1
z.close()
print('SP', OUT, n, 'files ·', os.path.getsize(OUT), 'bytes · missing from the previous SP:', len(miss), miss[:8])
PY
)
cd $D && sha1sum * | cut -c1-12,41- && ls -l | awk '{print $5, $9}'
