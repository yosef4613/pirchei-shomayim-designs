#!/bin/bash
# 29.10 14:35 · R-13 — הרשימה הקבועה של בדיקות אוטומטיות לפני כל מסירה (המתאם מריץ, לא סוכן).
# 31.10 21:47: התיקייה full נוצרת עכשיו בתחילת הסקריפט — ב-S7F176 היא לא הייתה, ו-run_full לא רץ (הלוג לא נפתח).
# שימוש: bash tools_pack/predeliver.sh <NNN> <PREV>      למשל: bash tools_pack/predeliver.sh 143 141
# 1. sha1 וגודל.  2. הבדיקות המלאות (run_full.sh), אם עוד לא רצו.  3. בדיקות Chromium אחת אחרי השנייה, דרך nolock.sh:
#    c34smoke, p34smoke, census של מה שמצויר מלמעלה (D-274), המבנים (D-275), הסמי, השניות הראשונות, היפוכי אנשים, המטוסים.
# 4. השוואה מול הבנייה הקודמת → qa/s7fNNN/predeliver.md. היציאה: מספר הכישלונות.
# חשבון התוכנית נבדק בסקריפט השלב (v600_stepNN.py) ובשחזור (verify_v6NN.sh) — לא כאן.
set -u
N=$1; P=$2; R=/home/claude/work/clean_r2b_025637; cd $R || exit 9
G=out/Turbo_City_v1_96_GATE77_S7F$N.html; [ -f $G ] || { echo "אין בנייה: $G"; exit 9; }
Q=qa/s7f$N; D=$Q/pre; mkdir -p $D $Q/full; NL=/home/claude/work/tools_pack/nolock.sh; DEV=tools/dev
[ -e /home/claude/work/PERF_LOCK ] && { echo "LOCKED — לא עכשיו"; exit 3; }
echo "S7F$N $(sha1sum $G | cut -c1-12) · $(stat -c%s $G) · $(date +%H:%M)" | tee $D/sha.txt
[ -f $Q/full/qa.json ] || bash tools/qa/run_full.sh $G $Q/full > $Q/full/run_full.log 2>&1 || true
# 17:35: zoomLevels נכשל פעמיים בתוך הריצה המלאה תחת עומס (gestures 0) ועבר לבד 4 / 4 — אם נכשל, מריצים אותו שוב פעמיים לבד ורושמים
if ! grep -q '"ok": true' $Q/full/zoomLevels.json 2>/dev/null; then for i in 1 2; do TC_READY_MS=600000 bash $NL python3 tools/s6r/evaljs_out.py $G $Q/full/qa_zoomLevels.js $Q/full/zoomLevels_rerun$i.json > $Q/full/zoomLevels_rerun$i.log 2>&1; done; fi
run() { local nm=$1; shift; timeout ${TMO:-1800} $NL "$@" > $D/$nm.log 2>&1; echo "$nm $? $(date +%H:%M)"; }
run c34smoke   node $DEV/c34smoke.js   $G $D/c34smoke.png
run p34smoke   node $DEV/p34smoke.js   $G $D/p34smoke.png
run census3    node $DEV/c34census3.js $G $D/census3.json   # 15:25: census3 (סוכן 1) — רק מה שבאמת מצויר מלמעלה, במקום census2
run bldshadow  node $DEV/bldshadow_qa.js $G $D/bld
run c34semiqa2 node $DEV/c34semiqa2.js $G $D/semi.json 60 300
run c34firstqa node $DEV/c34firstqa.js $G $D/first
run p34flipqa  node $DEV/p34flipqa.js  $G $D/flip
# 31.10 (R-35): מוני השגיאות של כל המודולים אחרי סיבוב מצלמה בעיר, בנמל ובשדה — שגיאה שנתפסת ונספרת היא עדיין שגיאה
[ -f $DEV/errtour.js ] && run errtour node $DEV/errtour.js $G $D/errtour.json
# 1.11 (R-53): a train on every rail bridge (RB-74, the port bridges, the island bridge) is drawn OVER its deck — a counter and one picture per bridge
[ -f $DEV/bridge_trains_check.js ] && run bridges node $DEV/bridge_trains_check.js $G $D/bridges
# 1.11 (R-54, R-51): the special stalls of the city and the F4 bar — inside roadAudit (special_stalls_d333, f4_bar_zones_and_keys), run by t1
# 1.11 (הבעלים 31.10 23:46): 0 אוטובוסים ממתינים על הכביש ליד המסוף E3 — termwait.js; עד שהמסוף החדש נבנה (12 מפרצים ומקום המתנה) — מדווח, לא חוסם
[ -f $DEV/termwait.js ] && run termwait node $DEV/termwait.js $G 150 $D/termwait.json   # 1.11: the seconds come before the output — without them the check sampled 0 times and "passed"
# 2.11 (הביקורת 05:30): כללי הכרטיס — כבישים כמו במפה, מפרץ בכל תחנה, התאים לפי תנאי הקבלה (R-62/63/64); חוסם
[ -f $DEV/rules_gate.js ] && run rules node $DEV/rules_gate.js $G $D/rules.json
# 2.11 (R-67): 0 רכבים מזויפים בכל אזור שנבנה מחדש — מופיע/נעלם, קופץ, חונה בלי דרך לכביש או בתוך מבנה (5 דקות סימולציה); חוסם. האזורים: VINV_ZONES
[ -f $DEV/vinv/run_vinv_zones.sh ] && { timeout 1500 bash $DEV/vinv/run_vinv_zones.sh $G $D/vinv.json 300 "${VINV_ZONES:-B4,B3,A3,A4,C3,D3,C4,D4}" > $D/vinv.log 2>&1; echo "vinv $? $(date +%H:%M)"; }
# 3.11 (המבקר על S7F210): בדיקות האזור של S6 (Z-01…Z-09, כולל Z-09), הפרטים החיים (liveAudit — 8 מ-4 בכל אזור בנוי), מדריך הסגנון (כלל 18), "מה שהבעלים אהב" (כלל 19) — חוסמים
[ -f $DEV/s6_zone_checks2.js ] && for z in ${ZCHK_ZONES:-C5 D5}; do run zchk_$z node $DEV/s6_zone_checks2.js $G $z $D/zchk_$z.json; done
[ -f $DEV/live_audit.js ] && run live node $DEV/live_audit.js $G $D/live.json
{ timeout 900 bash $NL node /tmp/claude-0/-home-claude/7bb7c82b-9a44-5cd6-ab8f-054dc66a801d/scratchpad/probe_c2.js $(readlink -f $G) /home/claude/work/tools_pack/style_dump.js > $D/style_dump.json 2> $D/style_dump.err && python3 /home/claude/work/tools_pack/style_check.py ${STYLE_ZONES:-B4 B3 A3 A4 C3 D3 C4 D4 C5 D5} --game clean_r2b_025637/$G --dump $(readlink -f $D/style_dump.json) --json $(readlink -f $D)/style.json --quiet > $D/style.log 2>&1; echo "style $? $(date +%H:%M)"; }
python3 /home/claude/work/tools_pack/liked_check.py $G $D/liked.json > $D/liked.log 2>&1; echo "liked $? $(date +%H:%M)"
# 3.11 (R-76, ‏D‑404): אנשים בכביש — דוגמים את כל האנשים בעיר לאורך כמה דקות; אדם על נתיב שלא בתוך מעבר — כישלון (חוסם)
[ -f $DEV/people_on_road.js ] && run people node $DEV/people_on_road.js $G $D/people.json
# 3.11 23:33 (הביקורת 23:16, אחרי מה שהבעלים מצא ב-AIR-W0 / J46_16): מעברי החצייה — שתי בדיקות, שתיהן חוסמות: (1) בכל צומת עם רמזור מעבר בכל זרוע
#   (החריגים: צומת T לפי D‑439, וחריג רשום לפי D‑427 / D‑430 ב-tools_pack/xw_exceptions.json); (2) כל מעבר של מפת הדרכים בצומת שבנוי במשחק — גם במשחק.
#   הרשימה של המעברים שנוספו ושיצאו, לפי צומת וזרוע, מול הבנייה הקודמת (xw.md)
[ -f $DEV/xw_dump.js ] && { run xwdump node $DEV/xw_dump.js $G $D/xw_dump.json; XP=qa/s7f$P/pre/xw_dump.json; [ -f $XP ] && XA="--prev $XP" || XA=""; python3 /home/claude/work/tools_pack/xw_gate.py $D/xw_dump.json $D/xw.json $XA --md $D/xw.md > $D/xw.log 2>&1; echo "xw $? $(date +%H:%M)"; }
# 4.11 00:52 (הבעלים 00:25, D‑459): צי החירום של A4 — כל יציאה חוזרת לתא, ואף רכב בשדרה לא עומד 90 שנ׳ (900 שנ׳ סימולציה מהירה); חוסם
[ -f $DEV/a4fleet_cycle.js ] && run a4fleet node $DEV/a4fleet_cycle.js $G $D/a4fleet.json 900
if grep -q '__TC_A34' $G; then run a34qa node $DEV/a34qa.js $G $D/a34; run a34count node $DEV/a34count.js $G; fi
python3 /home/claude/work/tools_pack/predeliver_cmp.py $Q qa/s7f$P $Q/predeliver.md > /dev/null; F=$?
echo "PREDELIVER S7F$N מול S7F$P: כישלונות $F · $Q/predeliver.md · $(date +%H:%M)"; exit $F
