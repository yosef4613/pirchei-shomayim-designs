#!/bin/bash
# הכול במקום אחד בתור: הבדיקה המהירה (הלוח, הסיפור, q_ingame), ואז החוסמות ויום המשחק. ‎$1 = מספר הניסיון
D=/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/missions
bash $D/tools/run_quick.sh $1
bash $D/tools/run_gate.sh $1 $2
