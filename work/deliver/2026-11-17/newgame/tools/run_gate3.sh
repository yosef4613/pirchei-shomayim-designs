#!/bin/bash
# סוכן newgame: הבדיקות של ניסיון אחד, אחת אחרי השנייה (דפדפן אחד בכל פעם), כל אחת דרך התור. ‏timeout — רק על הריצה עצמה, לא על ההמתנה בתור.
# bash run_gate.sh NNNN [steps...]   (ברירת מחדל: play ingame rules people stuck skip)
W=/home/user/tc_root/tc/pkg/work; N=$1; shift; B=clean_r2b_025637/out/_try/try$N.html; O=deliver/2026-11-17/newgame/qa$N; mkdir -p $W/$O; cd $W
S=${@:-play ingame rules people stuck skip}
for s in $S; do
  echo "== $s · $(TZ=Asia/Jerusalem date +%H:%M:%S)"
  case $s in
    play)   bash tools_pack/bslot.sh timeout 1200 node deliver/2026-11-17/newgame/tools/ng_play.js $B $O/play.json > $O/play.log 2>&1; echo "rc=$?";;
    resume) bash tools_pack/bslot.sh timeout 1500 node deliver/2026-11-17/newgame/tools/ng_play.js $B $O/play_resume.json resume > $O/play_resume.log 2>&1; echo "rc=$?";;
    open)   bash tools_pack/bslot.sh timeout 1200 node deliver/2026-11-17/newgame/tools/ng_play.js $B $O/play_open.json open > $O/play_open.log 2>&1; echo "rc=$?";;
    filmskip) bash tools_pack/bslot.sh timeout 1200 node deliver/2026-11-17/newgame/tools/ng_play.js $B $O/play_filmskip.json filmskip > $O/play_filmskip.log 2>&1; echo "rc=$?";;
    skip)   bash tools_pack/bslot.sh timeout 900 node deliver/2026-11-17/newgame/tools/ng_play.js $B $O/play_skip.json skip > $O/play_skip.log 2>&1; echo "rc=$?";;
    ingame) bash tools_pack/bslot.sh timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.log 2>&1; echo "rc=$?";;
    rules)  bash tools_pack/bslot.sh timeout 1500 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; echo "rc=$?";;
    people) bash tools_pack/bslot.sh timeout 1500 node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; echo "rc=$?";;
    stuck)  bash tools_pack/bslot.sh timeout 2400 node qa_tools/stuckmax.js $B 150 t17newgame$N > $O/stuck.log 2>&1; echo "rc=$?";;
  esac
  echo "== $s נגמר · $(TZ=Asia/Jerusalem date +%H:%M:%S)"
done
echo "== הכול נגמר"
