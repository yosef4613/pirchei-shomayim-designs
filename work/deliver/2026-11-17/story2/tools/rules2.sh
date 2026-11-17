#!/bin/bash
# story2: rules_gate שוב על try$1, ועל הבסיס S7F303 להשוואה (בדיקות העולם של השדה — s15j_terminal / fieldfix_r3)
W=/home/user/tc_root/tc/pkg/work; R=$W/deliver/2026-11-17/story2/runs; cd $W
node qa_tools/rules_gate.js clean_r2b_025637/out/_try/try$1.html $R/rules2_$1.json > $R/rules2_$1.log 2>&1; echo "rules2 rc=$?" >> $R/rules2_$1.log
node qa_tools/rules_gate.js clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F303.html $R/rules_s7f303.json > $R/rules_s7f303.log 2>&1; echo "base rc=$?" >> $R/rules_s7f303.log
