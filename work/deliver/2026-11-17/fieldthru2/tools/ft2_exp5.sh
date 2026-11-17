#!/bin/bash
# ft2_exp5.sh — fieldthru2: D‑701 + המתנה בדרך (plan_flight2) + שני נתיבים ב-B וב-C — מעל הלוח עם P6
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ft2/exp; WD=$SP/../world_p6.json
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru2/tools
run(){ n=$1; shift; o=$1; shift; echo "== $n $(TZ=Asia/Jerusalem date +%H:%M:%S)"; env "$@" timeout 2400 python3 ft2_gen.py $WD $WD $SP/$n.json $o > $SP/$n.log 2>&1; grep -v '^world\|^occV' $SP/$n.log | cut -c1-300; }
run w1_seg_d701 GA4,GA5,GA7,R3 FT2_D701=1 FT2_NOR3NIGHT=1 FT_SEG=1 FT_LINKS=A1,A2,A3N,A4 FT_EXITS=A3,A2,A3N
run w2_seg GA4,GA5,GA7,R3 FT2_NOR3NIGHT=1 FT_SEG=1
echo "== done $(TZ=Asia/Jerusalem date +%H:%M:%S)"
