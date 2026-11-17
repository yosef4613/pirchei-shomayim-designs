# -*- coding: utf-8 -*-
# sync_flights.py <flights.json> <part.js> — fieldfix: החלק 074zp_ff_flights.js מהתוצאה של ff_flights.py (הטיסות החדשות, הלו״ז והגררים) — נכנס אחרי s15k (setTimeout), כמו שנבדק
import sys, json
R = json.load(open(sys.argv[1], encoding='utf-8'))
def rnd(o):
    if isinstance(o, float): return round(o, 2)
    if isinstance(o, list): return [rnd(x) for x in o]
    if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
    return o
add = [dict(sid=a['sid'], flight=rnd(a['flight']), sched=rnd(a['sched']), veh=rnd(a['veh']), window=a['window']) for a in R['add']]
log = ' · '.join(R['log'])
js = '''/* ==== fieldfix 17.11 · (3) תמהיל הטיסות (מהביקורת של הבעלים 12.11: "מנהלים AC-BJ-01, הענקים P1/P6, מטען") ====
   מצאתי: ‏019l:S15SIM — 6 טיסות במחזור של 720 ש׳ (P2, P3, P4, R2, GA6 ו-C2 של s15i); P1 / P6 (הענקים), GA1 (המנהלים) ו-C1 (המשא הגדול) — חונים בלי טיסה.
   הכלל של המסלול — של fieldcalc (for_fieldfix_rwy_rule.txt; המתאם 17.11: גובר על הכלל של s15_sim.py, שספר את כל רגל הגישה + 8 ש׳ מכל צד):
   'תפוס' רק כשהמטוס על המסלול ונמוך מ-40, מרווח 3 ש׳ ועוד 8 אחרי מטוס כבד. זמן העמידה — לפחות כל השירותים (מטריצת השירות של fieldcalc: מנהלים 250, ‏LG ‏470, ‏CG ‏440).
   הטיסות נוצרו בכלי של S15 (s15_sim.py: departure / takeoff / arrival / tug / ac_conflict — כמו FL-C2 של s15i), מול הסימולציה כמו שהיא רצה במשחק
   (dump של try6682 — אחרי כל העטיפות, כולל הגרירות של R3), כל שנייה. הכלי: deliver/2026-11-17/fieldfix/tools/ff_flights.py.
   ''' + log + '''
   הנכנס — אחרי כל העיבוד של השדה (074p / 074q / 074r: setTimeout אחרי s15kRun), כי הבדיקה נעשתה מול המצב הזה בדיוק: הטיסה, הלו״ז, והגרר
   (הלו״ז שלו כמו שרץ במשחק + הנסיעה הנוספת). S15_FL / S15_MOVING / S15_STAT מתעדכנים. FFFL.on=false — בלי. ==== */
var FFFL={on:true,n:0,err:'',add:''' + json.dumps(add, ensure_ascii=False, separators=(',', ':')) + '''};
function ffflInject(){if(!FFFL.on||FFFL.n)return;try{for(const A of FFFL.add){if(S15SIM.flights.some(f=>f.id===A.flight.id))continue;S15SIM.flights.push(A.flight);S15_FL[A.flight.id]=A.flight;S15SIM.sched.push(A.sched);
  for(const v of A.veh){const i=S15SIM.veh.findIndex(w=>w.id===v.id);if(i>=0)S15SIM.veh[i].legs=v.legs;else{S15SIM.veh.push(v);S15_MOVING.add(v.id)}ffflPtStop(v)}
  // המטוס החונה של העמדה יוצא מהרשימה השמורה (בלי לאפס אותה — 074q כבר תיקן אותה, והתיקון שלו רץ פעם אחת)
  try{if(S15_STAT){const k=S15_STAT.findIndex(o=>o.key==='PK-'+A.sid);if(k>=0)S15_STAT.splice(k,1)}}catch(e){}FFFL.n++}}catch(e){FFFL.err=String(e)}}
// הגרר: כמו כל הגררים של השדה אחרי s15i (074p:s15iRetargetAll / s15iTugAttach — רצים בטעינה, לפני שהטיסה הזאת נכנסת): בדחיפה הגרר צמוד לאף במרחק s15iPtA,
// לכן העצירה לפני הדחיפה = המקום שבו הוא יהיה ברגע החיבור (בלי קפיצה), והעצירה שאחרי הניתוק (והתחלת הנסיעה הבאה) זזות באותו הפרש
function ffflPtStop(v){try{if(!/^PT/.test(v.id)||typeof s15iPtA!=='function'||typeof S15I_PX==='undefined')return;const pose=(b,t)=>{const T=S15SIM.T;return s15PoseAt(b,((t%T)+T)%T)};
  for(let j=0;j<v.legs.length;j++){const g=v.legs[j];if(!g.att)continue;const b=S15_FL[g.att];if(!b)continue;const o1=s15iPtA(b.model)*S15I_PX,o0=S15SIM.ngf[b.model]*b.L+v.L/2+4;
   const Q0=pose(b,g.t0+1e-4),S=v.legs[j-1],P=v.legs[j-2];if(Q0&&S&&S.h!=null&&S.p.length===1){const E=[+(Q0[0]+o1*Math.cos(Q0[2])).toFixed(1),+(Q0[1]+o1*Math.sin(Q0[2])).toFixed(1)];
    FFFL.ptShift=(FFFL.ptShift||[]).concat([v.id+' לפני '+Math.hypot(E[0]-S.p[0][0],E[1]-S.p[0][1]).toFixed(1)]);S.p=[E];if(P&&P.p&&P.p.length){P.p[P.p.length-1]=[E[0],E[1]];try{s15iFit(P)}catch(e){}}}
   const Q1=pose(b,g.t1-1e-4),n=v.legs[j+1],m=v.legs[j+2];if(Q1&&n&&n.h!=null){const dx=(o1-o0)*Math.cos(Q1[2]),dy=(o1-o0)*Math.sin(Q1[2]);n.p=[[+(n.p[0][0]+dx).toFixed(1),+(n.p[0][1]+dy).toFixed(1)]];
    if(m&&m.h==null&&m.p.length){m.p[0]=[n.p[0][0],n.p[0][1]];try{s15iFit(m)}catch(e){}}FFFL.ptShift.push(v.id+' אחרי '+Math.hypot(dx,dy).toFixed(1))}}
  try{if(S15GR&&S15GR.path)S15GR.path.clear()}catch(e){}}catch(e){FFFL.err='pt '+e}}
setTimeout(ffflInject,0);   // אחרי ה-setTimeout של 074r (s15kRun) — נרשם אחריו
window.__TC_FIELDFIX=Object.assign(window.__TC_FIELDFIX||{},{flights:()=>({n:FFFL.n,err:FFFL.err,add:FFFL.add.map(A=>A.sched)})});
'''
open(sys.argv[2], 'w', encoding='utf-8').write(js); print('ok', len(js), [a['sid'] for a in add])
