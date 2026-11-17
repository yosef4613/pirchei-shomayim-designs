#!/bin/bash
# ft2_exp4.sh — fieldthru2: הדרום מחדש עם D‑701 (A3 החדש, המראה הפוכה מ-A3 / A4, שני נתיבים ב-B; R3 ביום) — כמה טיסות נכנסות לדרום כשמתכננים אותו יחד
# (העולם: עם P6, בלי 5 הטיסות של הדרום של היום ובלי רכבי הדרום — רק להערכה; ה-GA1 של fieldfix נשאר)
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ft2/exp; WD=$SP/../world_south0.json
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru2/tools
for s in 0 1 2 3; do for d in 1 0; do n=z_s${s}_d$d; echo "== $n $(TZ=Asia/Jerusalem date +%H:%M:%S)"
  if [ $d = 1 ]; then E="FT2_D701=1 FT2_NOR3NIGHT=1"; else E="FT2_NOR3NIGHT=1"; fi
  env $E FT_SEED=$s FT_SHUF=1 FT_FRESH=PT-GA,PT-R,PT-HGR timeout 1800 python3 ft2_gen.py $WD $WD $SP/$n.json R2,R1,GA6,GA2,GA3,GA4,GA5,GA7,R3 > $SP/$n.log 2>&1; grep 'טיסות' $SP/$n.log | tail -1 | cut -c1-200; grep -c 'נכנס' $SP/$n.log; done; done
echo "== done $(TZ=Asia/Jerusalem date +%H:%M:%S)"
