#!/bin/bash
# הכול במקום אחד בתור (17.11 אחרי 07:08): הבדיקה של הלוח — ואם היא נכשלת, עוצרים (לא תופסים מקום בתור לחינם); אחרת q_ingame, החוסמות, יום המשחק, הצילומים, הכרטיס מול סצנה והדף החי. ‎$1 = מספר הניסיון, ‎$2 = הדף החי
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/missions; B=$W/clean_r2b_025637/out/_try/try$1.html; cd $W
node qa_tools/probe_c2.js $B $D/tools/q_mb_smoke.js $D/runs/smoke_$1.json > $D/runs/smoke_$1.log 2>&1; echo "smoke rc=$?" >> $D/runs/smoke_$1.log
python3 -c "import json,sys;d=json.load(open('$D/runs/smoke_$1.json'));sys.exit(0 if d['mb']['ok'] and d['story']['ok'] else 3)" || { echo "stop: smoke" >> $D/runs/smoke_$1.log; exit 3; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $D/runs/qin_$1.json > $D/runs/qin_$1.log 2>&1; echo "q_ingame rc=$?" >> $D/runs/qin_$1.log
bash $D/tools/run_gate.sh $1
node $D/tools/mb_shot.js $B $D/runs/shot_$1 > $D/runs/shot_$1.log 2>&1; echo "shot rc=$?" >> $D/runs/shot_$1.log
bash $D/tools/run_cut.sh $1 $2
