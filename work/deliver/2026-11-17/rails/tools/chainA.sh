#!/bin/bash
# rails 17.11 — שרשרת בדיקות א׳ (דרך התור): rails_check → q_ingame → rules_gate
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/rails/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
cd $W
bash tools_pack/bslot.sh node deliver/2026-11-17/rails/tools/rails_check.js $B $O/${T}_rails.json $SP/${T} > $O/${T}_rails.log 2>&1
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/${T}_qingame.json > $O/${T}_qingame.log 2>&1
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/${T}_rules.json > $O/${T}_rules.log 2>&1
echo done
