#!/bin/bash
# deliver_1110.sh <NNN> <ענף האיחוד> <קובץ המועמד שנבדק> "<שורת הכותרת>" — מסירה רשמית (המתאם, 10.11.2026)
# מקדם את master (ff) לענף האיחוד, שם תגית S7F<NNN>, בונה את הבנייה הרשמית, מוודא שהיא זהה בית-בית למועמד שעבר את הסט המלא,
# ומכין את דף ההורדה העטוף. הפרסום והשליחה לבעלים — אחר כך, ביד (Artifact + SendUserFile), ואז page_wrap.py log.
set -e
W=/home/user/tc_root/tc/pkg/work; N=$1; BR=$2; CAND=$3; LINE=$4; n=$(echo "$N" | tr 'A-Z' 'a-z')
cd $W
git -C src_game merge -q --ff-only "$BR"
git -C src_game tag "S7F$N"
OUT=clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F$N.html
BUILD_SUFFIX=-s7f$n python3 tools_pack/join_game.py src_game $OUT | tail -1
cmp $OUT "$CAND" && echo "הבנייה הרשמית זהה למועמד שנבדק"
D=deliver/2026-11-10/int$N; mkdir -p $D
python3 study/pages/make_build_page.py $OUT $D/Turbo_City_v1_96_GATE77_S7F$N.html "$LINE"
python3 tools_pack/page_wrap.py wrap $D/Turbo_City_v1_96_GATE77_S7F$N.html
echo "הקובץ: $(sha1sum $OUT | cut -c1-12) · $(stat -c%s $OUT) בתים"
echo "הדף:   $(sha1sum $D/Turbo_City_v1_96_GATE77_S7F${N}_page.html | cut -c1-12) · $(stat -c%s $D/Turbo_City_v1_96_GATE77_S7F${N}_page.html) בתים"
