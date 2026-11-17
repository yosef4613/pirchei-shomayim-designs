#!/bin/bash
# 28.10 (13:48 — הצילומים מחדש, הבדיקה הממוקדת, p365–p367) · מסירה — S7F122 להרצה (שלב 7 חלק 5: ערכת הטבע + העצים החיים מהתמונות; K‑185: המדרכות בכל המשבצות; המבדק של 33 האזורים),
# ‏v6.20, ‏RESUME R27, המפרט והמבדק (עמוד), לפני / אחרי של המדרכות, וחבילת תוספת (SP) על R23 — במבנה של החבילה (tools/, ‏qa/, ‏docs_plan/, ‏docs_study/),
# כך שפותחים את R23 ואז את ה-SP באותה תיקייה (גם ה-SP של S7F117 נכלל כאן במלואו). מעתיק לתיקיית מסירה חדשה (לא מוחק).
# שימוש: bash tools_pack/deliver_s7f122.sh
set -e
W=/home/claude/work; G=$W/clean_r2b_025637; P=$W/plan600; D=$W/deliver/s7f122_v620; mkdir -p $D
B=Turbo_City_v1_96_GATE77_S7F122
cp $G/out/$B.html $D/
(cd $D && python3 -c "import zipfile;z=zipfile.ZipFile('${B}_game.zip','w',zipfile.ZIP_DEFLATED);z.write('$B.html');z.close()")
cp $P/out/Turbo_City_Master_Plan_v6_20.html $D/
cp $W/study/zone_spec/Turbo_City_zone_spec.html $D/Turbo_City_zone_spec_and_audit.html
cp $G/qa/audit/k185_ab/Turbo_City_K185_before_after.jpg $D/
cp $W/study/PERF_BUDGET.md $W/study/PROGRESS_2026-10-27.md $W/study/Turbo_City_v1_96_GATE77_S7F122_RESUME_R27.md $D/
(cd $W && python3 - <<'PY'
import zipfile, os, glob
G='clean_r2b_025637/'; F=[]
for f in ['tools/patches/p354_nature.py','tools/patches/p359_zonenames.py','tools/patches/p360_groundheb.py','tools/patches/p361_bbfix.py',
          'tools/patches/p362_naturecache.py','tools/patches/p363_bandfill.py','tools/patches/p364_qafix.py','tools/p362_naturecache.py',
          'tools/post_s7f117.txt','tools/post_s7f118.txt','tools/post_s7f119.txt','tools/post_s7f120.txt','tools/post_s7f121.txt','tools/post_s7f122.txt',
          'tools/repro.sh','tools/qa/run_full.sh',
          'tools/dev/zoneaudit.js','tools/dev/zonegrid.py','tools/dev/nc_ab.js','tools/dev/nc_diff.py',
          'tools/dev/w19measure.sh','tools/dev/w20measure.sh','tools/dev/w21measure.sh','tools/dev/w22measure.sh',
          'tools/dev/chain_s7f117.sh','tools/dev/chain_s7f117b.sh','tools/dev/chain_audit2.sh','tools/dev/chain_audit3.sh','tools/dev/chain_s7f120.sh','tools/dev/chain_s7f121.sh','tools/dev/chain_s7f122.sh',
          'tools/dev/survey_score.py','tools/dev/survey_eye105.py','tools/dev/survey_drawinv_main.js','tools/dev/survey_merge.py','tools/dev/zone_ab.js',
          'tools/dev/w3fly.py','tools/dev/w3slow.py','tools/dev/fly_rerun.sh','tools/dev/slow_rerun.sh','tools/dev/chain_reaudit122.sh','tools/dev/cell_ab.py','tools/dev/records_s7f122.py',
          'tools/patches/p365_lampaccess.py','tools/patches/p366_stoplines.py','tools/patches/p367_lampspacing.py','tools/post_s7f123.txt','tools/post_s7f124.txt',
          'tools/dev/chain_s7f123.sh','tools/dev/chain_s7f124.sh','tools/dev/w23measure.sh','tools/dev/w24measure.sh','tools/dev/hold_for_deliver.sh',
          'qa/survey/s7f105_eye.json','qa/survey/s7f85_drawinv_main.json','qa/survey/s7f85_findings_world.json','qa/survey/cityinv_s7f117.json',
          'qa/stage7/brands/s7f117_audit.json','qa/stage7/texts_s7f117.json','qa/ownerperf/rb_S7F117.json','qa/ownerperf/ot/run.log']:
    if os.path.exists(G+f): F.append((G+f, f))
    else: print('missing', f)
for d in ['qa/s7f117','qa/s7f118','qa/s7f120','qa/s7f122','qa/s7f123','qa/survey/s7f111','qa/audit/records','qa/audit/k185_ab','qa/s7f120/ncab2']:
    for p in glob.glob(G+d+'/**/*', recursive=True):
        if os.path.isfile(p) and not p.endswith('.png'): F.append((p, p[len(G):]))
for d in glob.glob(G+'qa/audit/s7f1*'):   # the audit runs: the data and the grid shots (the raw shots stay home — the grid shots are the same with the grid)
    for p in glob.glob(d+'/*.json')+glob.glob(d+'/*.log')+glob.glob(d+'/grid/*.jpg'): F.append((p, p[len(G):]))
for p in glob.glob(G+'qa/ownerperf/ot/owner_tests_S7F117_*'): F.append((p, p[len(G):]))
for f in ['tools/v600_step26.py','tools/v600_step27.py','tools/v600_replay.sh','data/stages.json','data/new.json']: F.append(('plan600/'+f, 'docs_plan/'+f))
for f in ['PERF_BUDGET.md','PROGRESS_2026-10-27.md','Turbo_City_v1_96_GATE77_S7F117_RESUME_R26.md','Turbo_City_v1_96_GATE77_S7F122_RESUME_R27.md','PLAN_STUDY_2026-10-28.md','zone_dossier/build_dossier.py']:
    F.append(('study/'+f, 'docs_study/'+f))
for p in glob.glob('study/zone_spec/*.md')+['study/zone_spec/build_page.py','study/zone_spec/page.css']: F.append((p, 'docs_study/'+p[len('study/'):]))
F.append(('tools_pack/perf_sec.py','tools_pack/perf_sec.py')); F.append(('tools_pack/deliver_s7f117.sh','tools_pack/deliver_s7f117.sh')); F.append(('tools_pack/deliver_s7f122.sh','tools_pack/deliver_s7f122.sh'))
seen=set(); z=zipfile.ZipFile('deliver/s7f122_v620/Turbo_City_GATE77_S7F122_R23_plus_SP.zip','w',zipfile.ZIP_DEFLATED)
for src,arc in F:
    if arc in seen: continue
    seen.add(arc); z.write(src, arc)
z.close(); print(len(seen),'files in the SP')
PY
)
echo "| קובץ | sha1 | בתים |"; echo "|---|---|---|"
for f in $(ls $D | sort); do printf '| `%s` | `%s` | %s |\n' "$f" "$(sha1sum $D/$f | cut -c1-12)" "$(stat -c %s $D/$f | python3 -c 'import sys;print(format(int(sys.stdin.read()),","))')"; done
