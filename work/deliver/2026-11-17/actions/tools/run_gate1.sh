#!/bin/bash
# כמו run_gate.sh, אבל כל הבדיקות במקום אחד בתור (דפדפן אחד בכל פעם — אחת אחרי השנייה, בלי לחכות לתור בין בדיקה לבדיקה)
# שימוש: bash run_gate1.sh tryNNNN [skip_actions]
W=/home/user/tc_root/tc/pkg/work; T=$1; cd $W; O=$W/deliver/2026-11-17/actions/gate_$T; mkdir -p $O
echo "התחלה (מקום אחד) $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
bash tools_pack/bslot.sh bash deliver/2026-11-17/actions/tools/gate_inner.sh $T $2
echo "סוף $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
