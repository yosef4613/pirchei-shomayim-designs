#!/bin/bash
# ft2_exp6.sh — fieldthru2: כל הלוח מאפס (16 עמדות; בלי GA1 / C2 — לא במחולל של fieldthru) — עם D‑701 ובלי, כמה טיסות נכנסות כשמתכננים הכול יחד
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ft2/exp; WD=$SP/../world_empty.json
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru2/tools
ALLT=PT-GA,PT-R,PT-HGR,PT-P1,PT-P2,PT-P3,PT-P4,PT-P5,PT-P6,PT-C
for d in 1 0; do for s in 0 1; do n=full_d${d}_s$s; echo "== $n $(TZ=Asia/Jerusalem date +%H:%M:%S)"
  if [ $d = 1 ]; then E="FT2_D701=1 FT2_NOR3NIGHT=1"; else E="FT2_NOR3NIGHT=1"; fi
  env $E FT_SEED=$s FT_SHUF=1 FT_KEEP=6 FT_FRESH=$ALLT FT_TYPES=P6=AC-RJ-01 timeout 2400 python3 ft2_gen.py $WD $WD $SP/$n.json P2,P3,P4,P5,P1,P6,C1,R2,R1,GA6,GA2,GA3,GA4,GA5,GA7,R3 > $SP/$n.log 2>&1; grep 'טיסות' $SP/$n.log | tail -1 | cut -c1-200; grep -c ' נכנס ' $SP/$n.log; done; done
echo "== done $(TZ=Asia/Jerusalem date +%H:%M:%S)"
