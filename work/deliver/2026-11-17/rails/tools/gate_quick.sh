#!/bin/bash
# rails 17.11 — על הניסיון האחרון: rails_check, q_ingame, rules_gate, people_on_road, וצילומים קרובים לפני (S7F303) / אחרי — במקום אחד בתור
W=/home/user/tc_root/tc/pkg/work; T=$1; [ "$T" = try8217 ] || [ "$T" = next ] && T=$(ls $W/clean_r2b_025637/out/_try/ | grep -E '^try82(1[7-9]|[2-4][0-9])\.html$' | sort | tail -1 | sed 's/\.html//')
B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/rails/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
cd $W
echo "testing $T" > $O/quick_target.txt
node deliver/2026-11-17/rails/tools/rails_check.js $B $O/${T}_rails.json $SP/${T} > $O/${T}_rails.log 2>&1
node deliver/2026-11-17/rails/tools/shots.js $B $SP/close_${T} > $O/${T}_shots.log 2>&1
node deliver/2026-11-17/rails/tools/shots.js clean_r2b_025637/out/_try/raw_S7F303.html $SP/close_S7F303 > $O/S7F303_shots.log 2>&1
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/${T}_qingame.json > $O/${T}_qingame.log 2>&1
node qa_tools/rules_gate.js $B $O/${T}_rules.json > $O/${T}_rules.log 2>&1
node qa_tools/people_on_road.js $B $O/${T}_people.json > $O/${T}_people.log 2>&1
echo done > $O/${T}_qdone
