#!/bin/bash
# home (17.11): רץ בתוך מקום אחד של התור (נקרא מסוף home_q.js — כבר מחזיק מקום): בדיקת הפנים על ניסיון B, והבדיקות החוסמות על ניסיון A. דפדפן אחד בכל פעם.
# שימוש: bash chain_in_slot.sh <tryA> [tryB]
W=/home/user/tc_root/tc/pkg/work; A=$1; B=$2; cd $W; [ -s deliver/2026-11-17/home/qa/next_in.txt ] && B=$(cat deliver/2026-11-17/home/qa/next_in.txt); O=$W/deliver/2026-11-17/home/qa; SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad
T(){ TZ=Asia/Jerusalem date +%H:%M; }
if [ -n "$B" ] && [ -f clean_r2b_025637/out/_try/$B.html ]; then mkdir -p $O/$B; echo "home_in $B start $(T)" >> $O/chain.log
  timeout 900 node deliver/2026-11-17/home/tools/home_in_q.js clean_r2b_025637/out/_try/$B.html $O/$B/home_in.json $SP/sh_$B > $O/$B/home_in.out 2>&1; echo "home_in $B rc=$? $(T)" >> $O/chain.log; fi
if [ -n "$A" ]; then G=$O/$A; mkdir -p $G; BA=clean_r2b_025637/out/_try/$A.html; echo "gates $A start $(T)" >> $O/chain.log
  node qa_tools/probe_c2.js $BA qa_tools/q_ingame.js $G/q_ingame.json 2> $G/q_ingame.err; echo "q_ingame rc=$? $(T)" >> $O/chain.log
  node qa_tools/rules_gate.js $BA $G/rules_gate.json > $G/rules_gate.out 2>&1; echo "rules_gate rc=$? $(T)" >> $O/chain.log
  node qa_tools/people_on_road.js $BA $G/people.json > $G/people.out 2>&1; echo "people rc=$? $(T)" >> $O/chain.log
  node qa_tools/stuckmax.js $BA 150 $A > $G/stuck.out 2>&1; echo "stuck rc=$? $(T)" >> $O/chain.log; fi
echo "done $(T)" >> $O/chain.log
