#!/bin/bash
# chain.sh — perf 17.11 10:30: הכול במקום אחד בתור (התור הוא הגרלה — המתנה אחת במקום שלוש; ולא שני מקומות במקביל — גם בגלל ה-OOM):
#  memcmp (cand299x / cand300x) → הסט החוסם של try7162 → nav4base + nav → זום ×20 → memcmp של try7162; אחר כך, במקום נפרד — העלות של השומר של seatrees.
W=/home/user/tc_root/tc/pkg/work; cd $W; S=deliver/2026-11-17/perf; O=$S/qa/try7162; mkdir -p $O; L=$O/chain.tsv; X=clean_r2b_025637/out/_try
st(){ printf '%s\t%s\t%s\n' "$1" "$2" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
st queued -
bash tools_pack/bslot.sh bash -c "printf 'slot\t-\t%s\n' \$(TZ=Asia/Jerusalem date +%H:%M) >> $L; T=300 timeout 1500 node $S/tools/memcmp.js $O/memcmp.json $X/cand299x.html $X/cand300x.html > $O/memcmp.log 2>&1; printf 'memcmp\t%s\t%s\n' \$? \$(TZ=Asia/Jerusalem date +%H:%M) >> $L; bash $S/tools/gate.sh try7162 ingame rules people stuck zc nav4base nav; T=300 timeout 900 node $S/tools/memcmp.js $O/memcmp_7162.json $X/try7162.html > $O/memcmp_7162.log 2>&1; printf 'memcmp7162\t%s\t%s\n' \$? \$(TZ=Asia/Jerusalem date +%H:%M) >> $L"
st slotdone $?
OFF=seatBlockAsset,seatBlockKit PLACES=drive,city,coast,cityzoom SEC=6 RUNS=1 bash tools_pack/bslot.sh timeout 1200 node deliver/2026-11-10/perf/tools/perf_layers.js $O/seat_layers.json $X/try7162.html@src_game_t17_perf > $O/seat_layers.log 2>&1
st seat $?
