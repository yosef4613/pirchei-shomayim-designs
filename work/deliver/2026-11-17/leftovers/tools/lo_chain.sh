#!/bin/bash
# lo_chain.sh — leftovers (17.11): שרשרת בדיקות במקום אחד בתור (bash bslot.sh bash lo_chain.sh). קורא את jobs.txt בכל סיבוב (אפשר להוסיף עבודות בזמן הריצה);
# שורה: <שם> <tryNNNN> <תיקיית המקור> <סיומת המזהה> <בדיקות...>  — בונה את הניסיון (join_game), ואז הבדיקות ברצף; התוצאות: qa/<try>/runs.tsv; עבודה שנגמרה — done.txt.
# הבדיקות: ingame rules stuck people (הסט החוסם) · film tcofb tut (opening; tcofb — הכלי של loading) · farmq · icon p11 · sact · flow tugs (carrier; tugs — sl_tugs של sealife)
W=/home/user/tc_root/tc/pkg/work; Q=$W/qa_tools; D=$W/deliver/2026-11-17; LO=$D/leftovers; J=$LO/tools/jobs.txt; DN=$LO/tools/done.txt; touch $J $DN; cd $W
echo "lo_chain התחיל $(TZ=Asia/Jerusalem date +%H:%M)" >> $LO/tools/chain.log
while :; do
 line=$(grep -v '^#' $J | grep -v '^$' | while read -r a; do k=$(echo "$a" | awk '{print $2}'); grep -qx "$k" $DN || { echo "$a"; break; }; done)
 [ -z "$line" ] && break
 set -- $line; NM=$1; T=$2; SRC=$3; SUF=$4; shift 4
 G=$W/clean_r2b_025637/out/_try/$T.html; O=$LO/qa/$T; mkdir -p $O; L=$O/runs.tsv
 BUILD_SUFFIX=-$T-$SUF python3 tools_pack/join_game.py $SRC $G > $O/build.txt 2>&1
 echo "$(git -C $SRC log --oneline -1 | cut -c1-60) · tree $(git -C $SRC rev-parse HEAD^{tree} | cut -c1-12) · data:image=$(grep -c 'data:image' $G) · new Image(=$(grep -c 'new Image(' $G) · kiss=$(grep -ci kiss $G)" >> $O/build.txt
 run() { local nm=$1 tmo=$2; shift 2; local t0=$(date +%s); timeout $tmo "$@" > $O/$nm.log 2>&1; local rc=$?; printf '%s\t%s\t%s\t%s\n' "$nm" "$rc" "$(( $(date +%s)-t0 ))" "$(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
 for t in "$@"; do case $t in
  ingame) run ingame 2400 node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json ;;
  rules) run rules 1500 node $Q/rules_gate.js $G $O/rules.json ;;
  stuck) run stuck 1800 node $Q/stuckmax.js $G 150 $T ;;
  people) run people 2400 node $Q/people_on_road.js $G $O/people.json ;;
  film) run film 1500 node $D/opening/tools/film_flow.js $G $O/film_flow.json ;;
  tcofb) run tcofb 1800 node $D/loading/tools/tcofb_test.js $G $O/tcofb film ;;
  ofbusy) run ofbusy 900 node $Q/probe_c2.js $G $LO/tools/q_of_busy.js $O/of_busy.json ;;
  tut) run tut 900 node $Q/probe_c2.js $G $D/newgame/tools/q_tut.js $O/tut.json ;;
  farmq) run farmq 1500 node $Q/probe_c2.js $G $D/farm/tools/farm_q.js $O/farm_q.json ;;
  icon) run icon 900 node $Q/probe_c2.js $G $D/posters/tools/q_icon.js $O/icon.json ;;
  p11) run p11 1200 node $D/posters/tools/p11_check.js $G $O/p11.json $O/p11.png ;;
  sact) run sact 1500 node $Q/probe_c2.js $G $D/actions/tools/q_actions.js $O/sact.json ;;
  flow) run flow 5400 node $D/carrier/tools/q_import_flow_d3.js $G $O/flow.json 3300 ;;
  tugs) mkdir -p $O/slshots; run tugs 3000 node $D/sealife/tools/sl_tugs.js $G $O/tugs.json 6000 $O/slshots ;;
  *) echo "?? $t" >> $L ;;
 esac; done
 echo "CHAINDONE $*" >> $L; echo "$T" >> $DN
 # הדיסק: רק 3 הניסיונות האחרונים שלי כ-html
 ls -t $W/clean_r2b_025637/out/_try/try81[6-9][0-9].html 2>/dev/null | tail -n +4 | while read f; do gzip -1 "$f"; done
done
echo "lo_chain נגמר $(TZ=Asia/Jerusalem date +%H:%M)" >> $LO/tools/chain.log
