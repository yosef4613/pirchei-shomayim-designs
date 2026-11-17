#!/bin/bash
# chain.sh <build.html> <outdir> <name...> — merge3 (17.11, גל 3): שרשרת בדיקות במקום אחד בתור (bash bslot.sh bash chain.sh ...), כל בדיקה ברצף; נרשם ב-<outdir>/runs.tsv.
# השמות: ingame rules stuck people stadium3 — הסט החוסם (כמו merge2/tools/blocking.sh); nv voiceint oldsave f2e2e — הבדיקות של nfkiss (כמו nfkiss/tools/all.sh mine);
# f9quick mbsmoke sact tut cut gsvc fly — הבדיקות של הענפים שנכנסו (הכלים שלהם, בלי שינוי).
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; D=$W/deliver/2026-11-17; NT=$D/nfkiss/tools; G=$(readlink -f "$1"); O=$(mkdir -p "$2" && readlink -f "$2"); shift 2; cd $W; L=$O/runs.tsv
run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
for t in "$@"; do case $t in
  ingame) run ingame 2400 node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json ;;
  rules) run rules 1500 node $Q/rules_gate.js $G $O/rules.json ;;
  stuck) run stuck 1800 node $Q/stuckmax.js $G 150 $(basename $G .html) ;;
  people) run people 2400 node $Q/people_on_road.js $G $O/people.json ;;
  stadium3) run stadium3 1800 node $Q/probe_c2.js $G $D/stadium/tools/q_stadium3.js $O/stadium3.json ;;
  nv) run nv 900 node $Q/probe_c2.js $G $NT/q_nv.js $O/nv.json ;;
  voiceint) run voiceint 900 node $D/voiceint/tools/q_voiceint.js $G $O/voiceint.json ;;
  oldsave) run oldsave 600 node $Q/probe_c2.js $G $NT/q_oldsave.js $O/oldsave.json ;;
  f2e2e) run f2e2e 1200 node $Q/probe_c2.js $G $D/pier/tools/q_f2e2e.js $O/f2e2e.json ;;
  f9quick) run f9quick 1200 node $Q/probe_c2.js $G $D/f9fix/tools/q_f9_quick.js $O/f9quick.json ;;
  mbsmoke) run mbsmoke 1200 node $Q/probe_c2.js $G $D/missions/tools/q_mb_smoke.js $O/mbsmoke.json ;;
  sact) run sact 1500 node $Q/probe_c2.js $G $D/actions/tools/q_actions.js $O/sact.json ;;
  tut) run tut 900 node $Q/probe_c2.js $G $D/newgame/tools/q_tut.js $O/tut.json ;;
  cut) run cut 2400 node $D/cutscenes/tools/cut_check.js $G $O/cut.json ;;
  gsvc) run gsvc 1800 node $D/garage/tools/gsvc_probe.js $G $O/gsvc 0 ;;
  fly) run fly 2400 node $Q/probe_c2.js $G $D/police/tools/q_fly.js $O/fly.json ;;
  *) echo "?? $t" >> $L ;;
esac; done
echo "CHAINDONE $*" >> $L
