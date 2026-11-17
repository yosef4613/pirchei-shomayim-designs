#!/bin/bash
# ft2_exp2.sh — fieldthru2: D‑701 במחולל (A3 החדש + המראה הפוכה) מעל העולם עם P6 (14 טיסות, 70 תנועות)
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ft2/exp; mkdir -p $SP
WD=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ft2/world_p6.json
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru2/tools
run(){ n=$1; shift; o=$1; shift; echo "== $n $(TZ=Asia/Jerusalem date +%H:%M:%S)"; env "$@" timeout 1800 python3 ft2_gen.py $WD $WD $SP/$n.json $o > $SP/$n.log 2>&1; grep -v '^world\|^occV' $SP/$n.log | cut -c1-300; }
run x1_ga_d701 GA4,GA5,GA7 FT2_D701=1
run x2_r3_d701 R3 FT2_D701=1 FT2_NOR3NIGHT=1
run x3_all_d701 GA4,GA5,GA7,R3 FT2_D701=1 FT2_NOR3NIGHT=1
run x4_ga_27only GA4,GA5,GA7 FT2_D701=1 FT2_EXITS=
echo "== done $(TZ=Asia/Jerusalem date +%H:%M:%S)"
