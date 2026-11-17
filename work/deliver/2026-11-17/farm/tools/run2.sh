cd /home/user/tc_root/tc/pkg/work
B=clean_r2b_025637/out/_try/try7122.html; Q=deliver/2026-11-17/farm/qa/t7122; mkdir -p $Q
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B deliver/2026-11-17/farm/tools/farm_q.js $Q/farm_q.json > $Q/farm_q.log 2>&1
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame.json > $Q/q_ingame.log 2>&1
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $Q/rules_gate.json > $Q/rules_gate.log 2>&1
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $Q/people.json > $Q/people.log 2>&1
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 farm7122 > $Q/stuckmax.log 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/farm/tools/gshot.js $B /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/farm 7122 > $Q/gshot.log 2>&1
echo done > $Q/run2.done
