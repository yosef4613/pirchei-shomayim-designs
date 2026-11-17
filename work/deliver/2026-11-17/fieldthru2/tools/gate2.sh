#!/bin/bash
# gate2.sh NEXT — fieldthru2: בתוך מקום אחד בתור: q_ingame על הניסיון (qa/next.txt), ואם הוא לא עובר — על החלופה (qa/next2.txt); המדידה (ft2_probe) על הראשון;
# ואז הבדיקות החוסמות על מי שעבר: dump, ‏rules_gate, ‏people_on_road, ‏stuckmax 150
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/fieldthru2/qa; cd $W
T1=$1; [ "$T1" = NEXT ] && T1=$(cat $Q/next.txt); T2=$(cat $Q/next2.txt 2>/dev/null)
st(){ echo "$2 $1 $(TZ=Asia/Jerusalem date +%H:%M:%S) rc=$3" >> $Q/$2/runs.tsv; }
ing(){ T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$Q/$T; mkdir -p $O; echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/runs.tsv
  echo "data:image $(grep -c 'data:image' $B) · <img $(grep -o '<img' $B | wc -l)" > $O/static.txt
  timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json > $O/ingame.log 2>&1; st ingame $T $?
  python3 -c "import json,sys;R=json.load(open('$O/ingame.json'));a=R['roadAudit'];sys.exit(0 if a['passed']==a['total'] and not (R.get('errors') or []) else 1)"; }
ing $T1; ok1=$?
FT2_DISPATCH=0 timeout 900 node deliver/2026-11-17/fieldthru2/tools/ft2_probe.js $W/clean_r2b_025637/out/_try/$T1.html $Q/$T1/probe.json > $Q/$T1/probe.log 2>&1; st probe $T1 $?
T=$T1; if [ $ok1 != 0 ] && [ -n "$T2" ]; then ing $T2; T=$T2; fi
B=$W/clean_r2b_025637/out/_try/$T.html; O=$Q/$T; echo "full $T" >> $Q/$T1/runs.tsv
timeout 900 node deliver/2026-11-17/fieldthru/tools/dump_sim.js $B $O/sim.json > $O/dump.log 2>&1; st dump $T $?
timeout 900 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; st rules $T $?
timeout 1200 node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; st people $T $?
timeout 1500 node qa_tools/stuckmax.js $B 150 ft2_$T > $O/stuck.log 2>&1; st stuck $T $?
echo done >> $O/runs.tsv; [ "$T" != "$T1" ] && echo done >> $Q/$T1/runs.tsv
