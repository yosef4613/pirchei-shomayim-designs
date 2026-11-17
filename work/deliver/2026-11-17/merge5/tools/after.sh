#!/bin/bash
# after.sh — merge5 (17.11, גל 5): אחרי השרשרת על המועמד — stuckmax שלישי על cand304x (ההרצה השנייה: AI-CAR-15 ב-D2-ARN ‏6.5 שנ׳),
# ו-q_e9r על cand303x (S7F303) — האם ה-roadAudit שבתוך q_e9r (25 שנ׳ אחרי הטעינה) נכשל גם בבסיס באותן 3 בדיקות של התנועה / האמפיבי. במקום אחד בתור, ברצף.
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; D=$W/deliver/2026-11-17; O=$D/merge5/qa/cand304x; B=$D/merge5/qa/cand303x_ref; mkdir -p $B; cd $W; L=$O/runs.tsv
run() { local nm=$1 tmo=$2 out=$3; shift 3; local t0=$(date +%s); timeout $tmo "$@" > $out 2>&1; printf '%s\t%s\t%s\t%s\n' "$nm" "$?" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
run stuck3 1800 $O/stuck3.log node $Q/stuckmax.js $W/clean_r2b_025637/out/_try/cand304x.html 150 cand304x_3
run e9r_303x 1500 $B/e9r.log bash -c "cd $D/island/tools && QMAX=12000 SHOT_WAIT=1500 node isl_shot.js $W/clean_r2b_025637/out/_try/cand303x.html $B/e9shots --wait 25000 --q ../tools4/q_e9r.js --q q_e9.js term:5470,7090,1.6"
echo "AFTERDONE" >> $L
