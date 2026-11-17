#!/bin/bash
# 1.11 · רק בדיקות ה-Chromium של predeliver.sh (החלק "pre"), לבנייה שהבדיקות המלאות שלה כבר רצו. שימוש: bash tools_pack/prechecks_only.sh <NNN>
set -u
N=$1; R=/home/claude/work/clean_r2b_025637; cd $R || exit 9
G=out/Turbo_City_v1_96_GATE77_S7F$N.html; Q=qa/s7f$N; D=$Q/pre; mkdir -p $D; NL=/home/claude/work/tools_pack/nolock.sh; DEV=tools/dev
run() { local nm=$1; shift; timeout ${TMO:-1800} $NL "$@" > $D/$nm.log 2>&1; echo "$nm $? $(date +%H:%M)"; }
run c34smoke   node $DEV/c34smoke.js   $G $D/c34smoke.png
run p34smoke   node $DEV/p34smoke.js   $G $D/p34smoke.png
run census3    node $DEV/c34census3.js $G $D/census3.json
run bldshadow  node $DEV/bldshadow_qa.js $G $D/bld
run c34semiqa2 node $DEV/c34semiqa2.js $G $D/semi.json 60 300
run c34firstqa node $DEV/c34firstqa.js $G $D/first
run p34flipqa  node $DEV/p34flipqa.js  $G $D/flip
[ -f $DEV/errtour.js ] && run errtour node $DEV/errtour.js $G $D/errtour.json
[ -f $DEV/termwait.js ] && run termwait node $DEV/termwait.js $G 150 $D/termwait.json
if grep -q '__TC_A34' $G; then run a34qa node $DEV/a34qa.js $G $D/a34; run a34count node $DEV/a34count.js $G; fi
echo "PRECHECKS S7F$N DONE $(date +%H:%M)"
