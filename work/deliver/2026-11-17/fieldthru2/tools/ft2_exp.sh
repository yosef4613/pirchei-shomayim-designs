#!/bin/bash
# ft2_exp.sh — fieldthru2: מה מוסיף כל שינוי במחולל (מעל העולם של try7412 — 13 טיסות, 65 תנועות)
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ft2/exp; mkdir -p $SP
WD=/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/qa/try7412/sim.json
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru2/tools
run(){ n=$1; shift; o=$1; shift; echo "== $n $(TZ=Asia/Jerusalem date +%H:%M:%S)"; env "$@" timeout 1500 python3 ft2_gen.py $WD $WD $SP/$n.json $o > $SP/$n.log 2>&1; grep -v '^world\|^occV' $SP/$n.log | cut -c1-260; }
run e1_p6 P6 FT_TYPES=P6=AC-RJ-01
run e2_r3 R3 FT2_NOR3NIGHT=1
run e3_ga GA4,GA5,GA7 X=1
run e4_ga_b2 GA4,GA5,GA7 FT2_B2=9545
run e5_all P6,R3,GA4,GA5,GA7 FT_TYPES=P6=AC-RJ-01 FT2_NOR3NIGHT=1 FT2_B2=9545
echo "== done $(TZ=Asia/Jerusalem date +%H:%M:%S)"
