#!/bin/bash
# סוכן newgame: כל הבדיקות בתוך מקום אחד בתור (דפדפן אחד בכל פעם, בלי לחזור לתור בין בדיקה לבדיקה).
# bash bslot.sh bash gate_in_slot.sh NNNN step... [-- MMMM step...]
W=/home/user/tc_root/tc/pkg/work; cd $W
run(){ N=$1; s=$2; B=clean_r2b_025637/out/_try/try$N.html; O=deliver/2026-11-17/newgame/qa$N; mkdir -p $O
  echo "== $N $s · $(TZ=Asia/Jerusalem date +%H:%M:%S)"
  case $s in
    play|skip|filmskip|resume|open) a=$s; [ $s = play ] && a=; timeout 1200 node deliver/2026-11-17/newgame/tools/ng_play.js $B $O/play${a:+_$a}.json $a > $O/play${a:+_$a}.log 2>&1;;
    ingame) timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.log 2>&1;;
    rules)  timeout 1500 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1;;
    people) timeout 1500 node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1;;
    stuck)  timeout 2400 node qa_tools/stuckmax.js $B 150 t17newgame$N > $O/stuck.log 2>&1;;
  esac
  echo "rc=$? · $N $s נגמר · $(TZ=Asia/Jerusalem date +%H:%M:%S)"; }
N=$1; shift
for s in "$@"; do if [ "$s" = -- ]; then N=; continue; fi; if [ -z "$N" ]; then N=$s; continue; fi; run $N $s; done
echo "== הכול נגמר"
