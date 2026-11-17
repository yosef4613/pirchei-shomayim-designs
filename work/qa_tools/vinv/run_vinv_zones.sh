#!/bin/bash
# 2.11 (R-67): "0 רכבים מזויפים בכל אזור בנוי" — run_vinv_zones.sh <build.html> <out.json> [seconds=300] [rebuilt zones, comma-separated]
# נכשל (יציאה 1) כשבאזור שנבנה מחדש יש רכב שמופיע או נעלם, קופץ, או חונה בלי דרך לכביש / בתוך מבנה. האזורים הישנים — מדווחים, לא נכשלים.
D=$(cd "$(dirname "$0")" && pwd); SP=/tmp/claude-0/-home-claude/7bb7c82b-9a44-5cd6-ab8f-054dc66a801d/scratchpad
B=$(readlink -f "$1"); OUT="$2"; T="${3:-300}"; Z="${4:-B4,B3,A3,A4,C3,D3,C4,D4}"
PROBE="$D/../probe_c2.js"; [ -f "$PROBE" ] || PROBE="$SP/probe_c2.js"
Q=$(mktemp "$D/q_run_XXXX.js"); { echo "window.__VINV_T=$T;window.__VINV_REBUILT='$Z'.split(',');"; cat "$D/vinv_lib.js" "$D/vinv_static.js" "$D/vinv_check.js" "$D/q_zones_body.js"; } > "$Q"
timeout 1200 bash /home/user/tc_root/tc/pkg/work/tools_pack/nolock.sh node "$PROBE" "$B" "$Q" > "$OUT"; rc=$?
mv "$Q" /home/user/tc_root/tc/pkg/work/_to_delete/ 2>/dev/null
[ $rc -ne 0 ] && { echo "vinv: הבדיקה לא רצה ($rc)"; exit 2; }
python3 - "$OUT" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print('vinv', 'עובר' if d['ok'] else 'נכשל', '· אזורים בנויים', ','.join(d['rebuilt']), '· T', d['T'], 'שנ׳ · רכבים עומדים', d['vehiclesChecked'])
for k in ('rebuiltAppear','rebuiltJumps','rebuiltParked'):
    for x in d[k][:12]: print('  ', k, json.dumps(x, ensure_ascii=False)[:220])
print('  אזורים ישנים (לא נכשל):', sum(d['oldAppearBySource'].values()), 'הופעות/היעלמויות ·', d['oldJumps'], 'קפיצות ·', len(d['oldParked']), 'חונים')
for k,v in sorted(d['oldAppearBySource'].items()): print('    ', k, v)
print('  חריגים מוכרים:', len(d['allowed']))
sys.exit(0 if d['ok'] else 1)
PY
