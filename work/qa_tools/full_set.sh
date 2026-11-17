#!/bin/bash
# full_set.sh <game.html> <outdir> [base_outdir] — הסט המלא של הבדיקות, אחת אחרי השנייה, דפדפן אחד בכל פעם (בונה S7F266, 8.11).
# הכלים: qa_tools/*.js (העותקים של הסביבה הזו), ‏tools_pack/xw_gate.py ו-signal_gate.py (מריצים, לא משנים), ‏vinv עם probe_c2.js.
# base_outdir — סט קודם (הבסיס): המעברים שנוספו ושיצאו (‎--prev‎), והשוואה "אין החמרה" בסוף summary.txt.
# משתנים: PLAN — קובץ מפת הדרכים לבדיקת המעברים (ברירת מחדל: study/roads/city_plan.json; לשתי הריצות — אותו עותק),
#          VINV_ZONES, ‏ZA_ZONES (האזורים של zoneaudit), ‏PEOPLE_RUNS (ברירת מחדל 3), ‏STUCK_SECS (ברירת מחדל 150).
# היציאה: מספר הבדיקות שנכשלו. הסיכום: <outdir>/summary.txt (עברית).
set -u
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; T=$W/tools_pack; NL=$T/nolock.sh
G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); BASE=${3:-}
[ -f "$G" ] || { echo "אין קובץ משחק: $1"; exit 9; }
PLAN=${PLAN:-$W/study/roads/city_plan.json}
VZ=${VINV_ZONES:-B4,B3,A3,A4,C3,D3,C4,D4,C5,D5,E3}; ZA=${ZA_ZONES:-E3,C5}; PR=${PEOPLE_RUNS:-3}; SS=${STUCK_SECS:-150}
cd $W
L=$O/runs.tsv; : > $L
echo "$(basename $G) $(sha1sum $G | cut -c1-12) $(stat -c%s $G)" > $O/build.txt
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo bash $NL "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" >> $L; echo "$nm $rc $(( $(date +%s)-t0 ))s $(date +%H:%M)"; }
run ingame   900  node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json
run rules    1200 node $Q/rules_gate.js $G $O/rules.json
run live     2400 node $Q/live_audit.js $G $O/live.json
for i in $(seq 1 $PR); do run people$i 2400 node $Q/people_on_road.js $G $O/people$i.json; done
run xwdump   900  node $Q/xw_dump.js $G $O/xw_dump.json
XA=""; [ -n "$BASE" ] && [ -f "$BASE/xw_dump.json" ] && XA="--prev $BASE/xw_dump.json"
python3 $T/xw_gate.py $O/xw_dump.json $O/xw.json $XA --md $O/xw.md --plan $PLAN > $O/xw.log 2>&1; printf 'xw\t%s\t0\n' $? >> $L
python3 $T/signal_gate.py $O/xw_dump.json $O/signal.json --md $O/signal.md > $O/signal.log 2>&1; printf 'signal\t%s\t0\n' $? >> $L
run rule30   2400 node $Q/rule30_gate.js $G $O/rule30.json $O/rule30.md
run a4fleet  2400 node $Q/a4fleet_cycle.js $G $O/a4fleet.json 900
run a4fleet2 2400 node $Q/a4fleet_cycle2.js $G $O/a4fleet2.json 900
run stuck    1800 node $Q/stuckmax_why.js $G $SS stuck   # 10.11: עם הסיבה של המנוע לכל עמידה (מהסוכן של הכיכרות)
run story    900  node $Q/probe_c2.js $G $Q/qa_story5.js $O/story.json
run zoneaudit 2400 node $Q/zoneaudit.js $G $O/zoneaudit $ZA
t0=$(date +%s); timeout 1500 bash $Q/vinv/run_vinv_zones.sh $G $O/vinv.json 300 "$VZ" > $O/vinv.log 2>&1; rc=$?; printf 'vinv\t%s\t%s\n' $rc $(( $(date +%s)-t0 )) >> $L; echo "vinv $rc $(date +%H:%M)"
python3 $Q/full_set_summary.py $O ${BASE:+$BASE} > /dev/null; F=$?
echo "הסט המלא: $(basename $G) · כישלונות $F · $O/summary.txt"; exit $F
