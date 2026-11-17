#!/bin/bash
# 28.10 · מסירה — S7F117 להרצה (שלב 7 חלק 4: הלוגו; הקריאה החוזרת כברירת מחדל והקופסה במתג ב-F9; התיקון p361 לבאג של S7F116 ובדיקת tileEmpty;
# שמות האזורים בעברית גם בקוד), ‏v6.19, ‏RESUME R26 וחבילת תוספת (SP) על R23 — במבנה של החבילה (tools/, ‏qa/, ‏docs_plan/, ‏docs_study/),
# כך שפותחים את R23 ואז את ה-SP באותה תיקייה. מעתיק לתיקיית מסירה חדשה (לא מוחק).
# שימוש: bash tools_pack/deliver_s7f117.sh
set -e
W=/home/claude/work; G=$W/clean_r2b_025637; P=$W/plan600; D=$W/deliver/s7f117_v619; mkdir -p $D
B=Turbo_City_v1_96_GATE77_S7F117
cp $G/out/$B.html $D/
(cd $D && python3 -c "import zipfile;z=zipfile.ZipFile('${B}_game.zip','w',zipfile.ZIP_DEFLATED);z.write('$B.html');z.close()")
cp $P/out/Turbo_City_Master_Plan_v6_19.html $D/
cp $G/qa/stage7/brands/s7f117_sheet.png $D/Turbo_City_shop_logos_S7F117.png
python3 - <<PY
from PIL import Image
G='$G/qa/stage7/brands/'; ids=['C2-MALL','C2-SUPER','C2-PHARMACY','C2-CAFE','D2-RESTO','D2-MARKET','C4-HARDWARE','B2-KIOSK','D3-FUEL']
W,H=480,300;S=Image.new('RGB',(W*3,H*3),'black')
for i,k in enumerate(ids): S.paste(Image.open(G+'s7f117_sign_%s.png'%k).resize((W,H)),((i%3)*W,(i//3)*H))
S.save('$D/Turbo_City_shop_signs_S7F117.png')
PY
cp /tmp/claude-0/-home-claude/69dec702-2549-5179-bc7b-228edcb84e74/scratchpad/bugshot/bug_ab.jpg $D/Turbo_City_S7F116_bug_vs_S7F117.jpg
cp $W/study/PERF_BUDGET.md $W/study/PROGRESS_2026-10-27.md $W/study/Turbo_City_v1_96_GATE77_S7F117_RESUME_R26.md $D/
(cd $W && python3 - <<'PY'
import zipfile, os, glob
G='clean_r2b_025637/'; F=[]
for f in ['tools/patches/p354_nature.py','tools/patches/p359_zonenames.py','tools/patches/p360_groundheb.py','tools/patches/p361_bbfix.py',
          'tools/post_s7f117.txt','tools/post_s7f118.txt','tools/post_s7f119.txt','tools/repro.sh','tools/qa/run_full.sh',
          'tools/dev/survey_score.py','tools/dev/survey_eye105.py','tools/dev/survey_drawinv_main.js','tools/dev/survey_merge.py','tools/dev/zone_ab.js',
          'tools/dev/w18measure.sh','tools/dev/w19measure.sh','tools/dev/w18b_rerun.sh','tools/dev/post_w18b.sh','tools/dev/chain_s7f117.sh',
          'qa/survey/s7f105_eye.json','qa/survey/s7f85_drawinv_main.json','qa/stage7/brands/s7f117_audit.json','qa/stage7/texts_s7f117.json','tools/dev/zoneaudit.js','tools/dev/zonegrid.py',
          'qa/ownerperf/rb_S7F117.json','qa/ownerperf/ot/run.log']:
    F.append((G+f, f))
for d in ['qa/s7f116','qa/s7f117','qa/survey/s7f111']:
    for p in glob.glob(G+d+'/**/*', recursive=True):
        if os.path.isfile(p): F.append((p, p[len(G):]))
for p in glob.glob(G+'qa/ownerperf/ot/owner_tests_S7F117_*'): F.append((p, p[len(G):]))
for p in glob.glob(G+'qa/ownerperf/zoomC_*.json'): F.append((p, p[len(G):]))
for f in ['tools/v600_step26.py','tools/v600_replay.sh','data/stages.json','data/new.json']: F.append(('plan600/'+f, 'docs_plan/'+f))
for f in ['PERF_BUDGET.md','PROGRESS_2026-10-27.md','Turbo_City_v1_96_GATE77_S7F117_RESUME_R26.md']: F.append(('study/'+f, 'docs_study/'+f))
for f in ['PLAN_STUDY_2026-10-28.md','zone_dossier/build_dossier.py']: F.append(('study/'+f, 'docs_study/'+f))
F.append(('tools_pack/perf_sec.py','tools_pack/perf_sec.py')); F.append(('tools_pack/deliver_s7f117.sh','tools_pack/deliver_s7f117.sh'))
z=zipfile.ZipFile('deliver/s7f117_v619/Turbo_City_GATE77_S7F117_R23_plus_SP.zip','w',zipfile.ZIP_DEFLATED)
for src,arc in F: z.write(src, arc)
z.close(); print(len(F),'files in the SP')
PY
)
echo "| קובץ | sha1 | בתים |"; echo "|---|---|---|"
for f in $(ls $D | sort); do printf '| `%s` | `%s` | %s |\n' "$f" "$(sha1sum $D/$f | cut -c1-12)" "$(stat -c %s $D/$f | python3 -c 'import sys;print(format(int(sys.stdin.read()),","))')"; done
