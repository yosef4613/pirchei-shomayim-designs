#!/bin/bash
# משמיט את הסט החוסם של try8009 (הבנייה הקודמת) — רק התהליכים של qa_tools על try8009.html
for i in $(seq 1 600); do for p in $(pgrep -f "qa_tools/(probe_c2|rules_gate|people_on_road|stuckmax).js .*try8009.html"); do kill $p; done; grep -q "התחלה (המשך של try8009)" /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/qa/try8010/log.txt 2>/dev/null && exit 0; sleep 3; done
