#!/bin/bash
# 1.11.2026 · חבילת העבודה הרזה למסירה לבונה החדש — רק מה שצריך כדי לבנות מחדש ולעבוד:
#   המקור והבסיס (clean_r2b_025637/tools כולו + קובץ הבסיס GATE75), הטלאים וקובצי ה-post, סקריפטי הבנייה, כלי הבדיקה,
#   נתוני התוכנית והמחולל (plan600/data, plan600/tools), המקור של הדפים (study, exp34 — קבצי מקור בלבד), העבודה הפתוחה,
#   יומן ההחלטות (plan600/data/new.json), הודעות הבעלים, מסמך המסירה ו-REBUILD_LEAN.sh.
#   בלי בניות ישנות, בלי תוצאות בדיקות, בלי צילומים. נמצא במעקב strace (1.11 01:40): בניית המשחק קוראת רק את tools/ ואת קובץ הבסיס;
#   בניית התוכנית קוראת רק את plan600/data ו-plan600/tools.
set -e
W=/home/claude/work; D=$W/deliver/v648; OUT=$D/Turbo_City_v648_LEAN.zip
cd $W && python3 - <<'PY'
import zipfile, os
W = '/home/claude/work'; OUT = W + '/deliver/v648/Turbo_City_v648_LEAN.zip'
SRC = ('.py', '.js', '.md', '.json', '.sh', '.txt', '.css', '.mjs', '.cjs')
MAXB = 5 * 1024 * 1024
F = []
def add(p, arc=None):
    if os.path.isfile(p) and '__pycache__' not in p: F.append((p, arc or p))
def walk(d, exts=None, maxb=None, skip=('/_to_delete', '/node_modules', '/.git')):
    for r, ds, fs in os.walk(d):
        if any(s in r for s in skip): continue
        for f in fs:
            p = os.path.join(r, f)
            if exts and not f.endswith(exts): continue
            if maxb and os.path.getsize(p) > maxb: continue
            add(p)
G = 'clean_r2b_025637'
walk(G + '/tools')                                   # all of it — the patches, posts, build scripts, check tools (13 MB)
for f in ('Turbo_City_v1_96_GATE75_PORT_SOUTH_ACCESS_CONTROL.html', 'README_S6R.md', 'README_S6R_M4.md'): add(G + '/' + f)
for f in ('qa/b4/STOP_REPORT_1g_2026-11-01.md', 'qa/fleet176/report_1b_final.md'): add(G + '/' + f)
walk('plan600/tools'); walk('plan600/data')
for f in ('plan600/notes_v640.md', 'plan600/notes_v641.md', 'plan600/_to_delete/stages_before_step40.json', 'plan600/_to_delete/new_before_step40.json'): add(f)
walk('study', SRC, MAXB)
for f in ('study/roads/city_plan_stage1.html', 'study/roads/city_plan_stage2.html', 'study/roads/city_plan_stage3.html', 'study/roads/city_plan_stage4.html', 'study/roads/city_plan.html', 'study/roads/city_plan_pub.html',
          'exp34/b4/b4_v3.html', 'exp34/b4/b4_v3_pub.html', 'exp34/bld38/bld38_sample.html', 'exp34/bld38/bld38_pub.html', 'exp34/fleet/fleet_props_pub.html', 'exp34/fleet/fleet7c.html'): add(f)
walk('exp34', SRC, MAXB)
walk('inbox_owner'); walk('tools_pack')
for f in ('BOARD.md', 'DELETIONS.md'): add(f)
add('study/Turbo_City_HANDOFF_2026-11-01.md', 'Turbo_City_HANDOFF_2026-11-01.md')
add('tools_pack/REBUILD_LEAN.sh', 'REBUILD_LEAN.sh')
seen = set(); z = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, allowZip64=True); n = 0; raw = 0
for s, a in F:
    if a in seen: continue
    seen.add(a); z.write(s, a); n += 1; raw += os.path.getsize(s)
z.close()
print('LEAN', OUT, n, 'קבצים ·', raw, 'בתים לפני דחיסה ·', os.path.getsize(OUT), 'בתים')
PY
cd $D && sha1sum Turbo_City_v648_LEAN.zip
