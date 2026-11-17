#!/bin/bash
# all6928.sh — buses (17.11): במקום אחד של התור — הכיכרות בבסיס (עם הסיבות) ← הכיכרות ב-try6928 ← כל הבדיקות של try6928 (inslot.sh).
D=/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/buses
bash $D/tools/rbslot.sh base299d /home/user/tc_root/tc/pkg/work/clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F299.html
bash $D/tools/rbslot.sh try6928 /home/user/tc_root/tc/pkg/work/clean_r2b_025637/out/_try/try6928.html
bash $D/tools/inslot.sh try6928
bash $D/tools/inslot.sh try6930
bash $D/tools/inslot2.sh try6931
