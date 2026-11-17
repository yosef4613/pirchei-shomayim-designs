#!/bin/bash
# rbslot.sh <tag> <build.html> [stuck] — buses (17.11, הכיכרות): במקום אחד של התור — q_rb (420 + 1500 שנ׳ במהירות) ← ואם ביקשו, stuckmax_bus 1500 (אותו כלי כמו בניסיונות).
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/buses; Q=$D/qa; T=$1; B=$2; G=$Q/rb_gate.txt; cd $W
r(){ local name=$1; shift; local t0=$(date +%s); timeout 2400 "$@"; echo "$T $name rc=$? $(( $(date +%s)-t0 ))s $(TZ=Asia/Jerusalem date +%H:%M)" >> $G; }
echo "$T start $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
r rb node $D/tools/q_rb.js $B $Q/rb_$T.json 420 1500 > $Q/rb_$T.log 2>&1
[ "$3" = stuck ] && r stuck1500 node $D/tools/stuckmax_bus.js $B 1500 $T > $Q/${T}_stuck1500.json 2>&1
echo "$T done $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
