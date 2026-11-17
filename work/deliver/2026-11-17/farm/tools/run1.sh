cd /home/user/tc_root/tc/pkg/work
bash tools_pack/bslot.sh node qa_tools/probe_c2.js clean_r2b_025637/out/_try/try7122.html deliver/2026-11-17/farm/tools/farm_q.js deliver/2026-11-17/farm/qa/farm_q_7122.json > deliver/2026-11-17/farm/qa/farm_q_7122.log 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/farm/tools/gshot.js clean_r2b_025637/out/_try/try7122.html /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/farm 7122 > deliver/2026-11-17/farm/qa/gshot_7122.log 2>&1
bash tools_pack/bslot.sh node qa_tools/probe_c2.js clean_r2b_025637/out/_try/try7120.html deliver/2026-11-17/farm/tools/farm_q.js deliver/2026-11-17/farm/qa/farm_q_7120b.json > deliver/2026-11-17/farm/qa/farm_q_7120b.log 2>&1
bash tools_pack/bslot.sh node deliver/2026-11-17/farm/tools/gshot.js clean_r2b_025637/out/_try/try7120.html /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/farm 7120 > deliver/2026-11-17/farm/qa/gshot_7120.log 2>&1
echo done > deliver/2026-11-17/farm/qa/run1.done
