#!/bin/bash
# chain5.sh <build.html> <outdir> <name...> — merge5 (17.11, גל 5; chain.sh + qship — היציאה של "צוק הים" ב-L2, island 84a3e7a): שרשרת בדיקות במקום אחד בתור (bash bslot.sh bash chain2.sh ...; עותק של chain.sh — + seatrees, eye), כל בדיקה ברצף; נרשם ב-<outdir>/runs.tsv.
# השמות: ingame rules stuck people stadium3 — הסט החוסם (כמו merge2/tools/blocking.sh); nv voiceint oldsave f2e2e — הבדיקות של nfkiss (כמו nfkiss/tools/all.sh mine);
# f9quick mbsmoke sact tut cut gsvc fly — הבדיקות של הענפים שנכנסו (הכלים שלהם, בלי שינוי).
# merge4: fwhm (הבאג של לוח הטיסות), evt (events), tugs / oil / ship (sealife), isl / l5a (island), w17t (w17), tcld / tb (loading) — הכלים של הענפים, בלי שינוי.
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
  seatrees) run seatrees 2400 node $D/seatrees/tools/tree_sweep.js $G $O/seatrees.json ;;
  fwhm) run fwhm 600 node $Q/probe_c2.js $G $D/merge5/tools/q_fwhm.js $O/fwhm.json ;;
  evt) run evt 1800 node $D/events/tools/evt_test.js $G $O/evt.json $O/evtshots 130 420 ;;
  tugs) mkdir -p $O/slshots; run tugs 2400 node $D/sealife/tools/sl_tugs.js $G $O/tugs.json 6000 $O/slshots ;;
  oil) mkdir -p $O/slshots; run oil 1200 node $D/sealife/tools/sl_oil.js $G $O/oil.json $O/slshots ;;
  ship) run ship 900 node $D/sealife/tools/sl_ship.js $G $O/ship.json ;;
  isl) run isl 1500 bash -c "cd $D/island/tools && QMAX=9000 node isl_shot.js $G $O/islshots --wait 20000 --q q_e9.js --q q_pole.js --q q_il.js --q q_east.js --q q_isl2.js --q q_freight.js e9:5450,7350,0.55 chan:5900,7300,0.8" ;;
  l5a) run l5a 900 bash -c "cd $D/island/tools && node l5a_run.js $G $O/l5a_run.json 300 20" ;;
  zcq) mkdir -p $O/zcshots; QX=$D/perf/tools/q_nav.js run zcq 1200 node $D/perf/tools/zoomcycle.js $G $O/zcq.json $O/zcshots 6 1920 953 1 0 ;;
  eye5) run eye5 1500 node $D/merge5/tools/eye5.js $G $O/eye5 ;;
  w17t) run w17t 1500 node $D/w17/tools/w17t.js $G $O/w17t.json $O/w17shots ;;
  tcld) run tcld 1800 node $D/loading/tools/tcld_test.js $G $O/tcld ;;
  tb) run tb 1800 node $D/loading/tools/tb_test.js $G $O/tb ;;
  eye) run eye 1500 node $D/merge4/tools/eye4.js $G $O/eye ;;
  # merge5: הכלים של הענפים של גל 5 (בלי שינוי): airlogos (airlogos_probe), home (home_q, HOME_CHAIN=0 — בלי השרשרת שלהם), island (q_e9r + q_e9 + q_fy), perf (memcmp מול S7F303)
  alp) run alp 1500 node $D/airlogos/tools/airlogos_probe.js $G $O/alp.json $O/alpshots ;;
  homeq) run homeq 1200 env HOME_CHAIN=0 node $D/home/tools/home_q.js $G $O/homeq.json $O/homeshots ;;
  e9r) run e9r 1500 bash -c "cd $D/island/tools && QMAX=12000 SHOT_WAIT=1500 node isl_shot.js $G $O/e9shots --wait 25000 --q ../tools4/q_e9r.js --q q_e9.js term:5470,7090,1.6 hotel:6100,7400,0.9" ;;
  fy) run fy 1500 bash -c "cd $D/island/tools && QMAX=9000 node isl_shot.js $G $O/fyshots --wait 15000 --q ../tools4/q_fy.js fyafter:5470,7060,1.2" ;;
  mem) run mem 1800 env T=300 node $D/perf/tools/memcmp.js $O/memcmp_303x_304x.json $W/clean_r2b_025637/out/_try/cand303x.html $G ;;
  stuck2) run stuck2 1800 node $Q/stuckmax.js $G 150 $(basename $G .html)_2 ;;
  qship) run qship 1500 bash -c "cd $D/island/tools && QMAX=6000 SHOT_WAIT=1500 node isl_shot.js $G $O/shipshots --wait 25000 --q ../tools4/q_ship.js d8:4250,6990,0.45" ;;
  *) echo "?? $t" >> $L ;;
esac; done
echo "CHAINDONE $*" >> $L
