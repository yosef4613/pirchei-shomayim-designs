#!/bin/bash
# כל הבדיקות של ניסיון אחד ברצף, בתוך מקום אחד בתור (garage, 17.11): bash tools_pack/bslot.sh bash chain_in_slot.sh tryNNNN
# (דפדפן אחד בכל פעם; בלי לחכות לתור בין בדיקה לבדיקה). הסדר: העבודה בתא, המסך, האולם, ואז החוסמות.
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/garage/qa; cd $W; T=$1; B=clean_r2b_025637/out/_try/$T.html; O=$Q/$T; mkdir -p $O
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" > $O/gates.log
node deliver/2026-11-17/garage/tools/gsvc_probe.js $B $Q/v_$T > $Q/v_$T.log 2>&1; echo "gsvc rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
node deliver/2026-11-17/garage/tools/gst_probe.js $B $Q/p_$T > $Q/p_$T.log 2>&1; echo "gst rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
node deliver/2026-11-17/garage/tools/gh_shot.js $B $Q/h_$T 0 > $Q/h_$T.log 2>&1; echo "ghall rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2> $O/q_ingame.err; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; echo "rules_gate rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
echo done >> $O/gates.log
