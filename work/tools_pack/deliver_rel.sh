#!/bin/bash
# deliver_rel.sh <NNN> <ענף> <מועמד משוחרר שנבדק> "<כותרת>" — כמו deliver_1110.sh, אבל עם שלב השחרור (17.11: הסינון של הבעלים —
# join_game ואחריו nfkiss/tools/release_strip.js: בלי הערות, נתונים מקודדים ב-hex). מוודא שהבנייה הרשמית המשוחררת זהה בית-בית למועמד.
set -e
W=/home/user/tc_root/tc/pkg/work; N=$1; BR=$2; CAND=$3; LINE=$4; n=$(echo "$N" | tr 'A-Z' 'a-z')
cd $W
git -C src_game merge -q --ff-only "$BR"
git -C src_game tag "S7F$N"
RAW=clean_r2b_025637/out/_try/raw_S7F$N.html; OUT=clean_r2b_025637/out/Turbo_City_v1_96_GATE77_S7F$N.html
BUILD_SUFFIX=-s7f$n python3 tools_pack/join_game.py src_game $RAW | tail -1
node deliver/2026-11-17/nfkiss/tools/release_strip.js $RAW $OUT clean_r2b_025637/out/_try/strip_S7F$N.json | tail -1
cmp $OUT "$CAND" && echo "הבנייה הרשמית המשוחררת זהה למועמד שנבדק"
D=deliver/2026-11-10/int$N; mkdir -p $D
python3 study/pages/make_build_page.py $OUT $D/Turbo_City_v1_96_GATE77_S7F$N.html "$LINE"
python3 tools_pack/page_wrap.py wrap $D/Turbo_City_v1_96_GATE77_S7F$N.html
echo "הקובץ: $(sha1sum $OUT | cut -c1-12) · $(stat -c%s $OUT) בתים"
echo "הדף:   $(sha1sum $D/Turbo_City_v1_96_GATE77_S7F${N}_page.html | cut -c1-12) · $(stat -c%s $D/Turbo_City_v1_96_GATE77_S7F${N}_page.html) בתים"
