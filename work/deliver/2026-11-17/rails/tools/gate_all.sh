#!/bin/bash
# rails 17.11 — כל הבדיקות החוסמות על ניסיון אחד, במקום אחד בתור (bslot.sh bash gate_all.sh tryNNNN): rails_check, q_ingame, rules_gate, people_on_road, stuckmax 150
W=/home/user/tc_root/tc/pkg/work; T=$1; [ "$T" = try8215 ] && [ -e $W/clean_r2b_025637/out/_try/try8216.html ] && T=try8216   # 16:35: הכרטיס של 8215 בתור בודק את 8216 (אחרי המיזוג עם S7F304)
 B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/rails/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
cd $W
node deliver/2026-11-17/rails/tools/rails_check.js $B $O/${T}_rails.json $SP/${T} > $O/${T}_rails.log 2>&1
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/${T}_qingame.json > $O/${T}_qingame.log 2>&1
node qa_tools/rules_gate.js $B $O/${T}_rules.json > $O/${T}_rules.log 2>&1
node qa_tools/people_on_road.js $B $O/${T}_people.json > $O/${T}_people.log 2>&1
node qa_tools/stuckmax.js $B 150 rails_$T > $O/${T}_stuck.log 2>&1
echo done > $O/${T}_done
