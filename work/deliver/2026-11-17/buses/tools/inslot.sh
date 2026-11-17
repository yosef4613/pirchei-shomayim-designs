#!/bin/bash
# inslot.sh <try> — buses (17.11): כל הבדיקות של הניסיון במקום אחד של התור (bash tools_pack/bslot.sh bash inslot.sh <try>) — דפדפן אחד בכל פעם, אחת אחרי השנייה,
# כדי לא לחכות בתור 8 פעמים (36 ממתינים ב-07:41). הסדר: הבדיקות החוסמות → המדידה (בסיס ← ניסיון) → הלילה של הקווים → stuckmax 1500 → הלילה של הבסיס.
W=/home/user/tc_root/tc/pkg/work; T=$1; D=$W/deliver/2026-11-17/buses; Q=$D/qa; cd $W
# הפניה (17.11 12:50): כשיש qa/redirect_<try> — בודקים את הניסיון שכתוב בו (קודם הכיכרות: rbslot.sh), באותו מקום בתור
[ -s $Q/redirect_$T ] && { T=$(cat $Q/redirect_$T); bash $D/tools/rbslot.sh $T $W/clean_r2b_025637/out/_try/$T.html; }
B0=$W/clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F299.html; B=$W/clean_r2b_025637/out/_try/$T.html; G=$Q/${T}_gate.txt
r(){ local name=$1; shift; local t0=$(date +%s); timeout 2400 "$@"; echo "$name rc=$? $(( $(date +%s)-t0 ))s $(TZ=Asia/Jerusalem date +%H:%M)" >> $G; }
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
r ingame node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/${T}_ingame.json > $Q/${T}_ingame.log 2>&1
r rules node qa_tools/rules_gate.js $B $Q/${T}_rules.json > $Q/${T}_rules.log 2>&1
r stuck150 node qa_tools/stuckmax.js $B 150 $T > $Q/${T}_stuck150.json 2>&1
r people node qa_tools/people_on_road.js $B $Q/${T}_people.json > $Q/${T}_people.log 2>&1
echo "gate-done" >> $G
[ -s $Q/beh_base299.json ] || r beh-base node $D/tools/q_busbeh.js $B0 $Q/beh_base299.json 420 600 > $Q/beh_base299.log 2>&1
r beh node $D/tools/q_busbeh.js $B $Q/beh_${T}.json 420 600 > $Q/beh_${T}.log 2>&1
r night node $D/tools/lines_night_tr2.js $B $Q/${T}_night.json > $Q/${T}_night.log 2>&1
r stuck1500 node $D/tools/stuckmax_bus.js $B 1500 $T > $Q/${T}_stuck1500.json 2>&1
[ -s $Q/base299_night.json ] || r base-night node $D/tools/lines_night_tr2.js $B0 $Q/base299_night.json > $Q/base299_night.log 2>&1
echo "chain-done $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
