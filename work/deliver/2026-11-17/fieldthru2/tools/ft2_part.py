# -*- coding: utf-8 -*-
# ft2_part.py <seq.json> <src_game_dir> — fieldthru2: כותב את parts/074zv1_ft_types.js (מגוון סוגים בכל עמדה — FTY) מתוך הסבב שנבדק (ft2_seq.py), ומכניס ל-manifest
import sys, os, json, subprocess
S = json.load(open(sys.argv[1], encoding='utf-8')); G = sys.argv[2]
SEATS = {'AC-PR-01': 4, 'AC-LT-01': 6, 'AC-BJ-01': 12, 'AC-CN-01': 6, 'AC-AM-01': 4, 'AC-TB-01': 0, 'AC-TP-01': 70, 'AC-RJ-01': 76, 'AC-QJ-01': 100, 'AC-NB-01': 180, 'AC-MW-01': 300, 'AC-CG-01': 0, 'AC-LG-01': 420, 'AC-HC-01': 0}
add = {}
for fid, s in S['seqs'].items():
    used = sorted(set(j for j in s['seq'] if j))
    if not used: continue
    mp = {0: 0}; vars_ = [None]
    for j in used:
        v = s['vars'][j]; mp[j] = len(vars_)
        vars_.append(dict(ac=v['ac'], L=v['L'], W=v['W'], legs=v['legs'], park=v['park'], tugs={k: x['trip'] for k, x in v['tugs'].items()}))
    add[fid] = dict(stand=s['stand'], base=s['base'], seq=[mp[j] for j in s['seq']], vars=vars_)
info = ' · '.join('%s: %s' % (a['stand'], ' / '.join([a['base'][3:5] if j == 0 else a['vars'][j]['ac'][3:5] for j in a['seq']])) for a in add.values())
head = '''/* ==== fieldthru2 17.11 · מגוון סוגים בכל עמדה — הסוג נקבע לכל ביקור (הבעלים 17.11: "3 סוגי מטוסים הענק ו2 גדולים … חברות תעופה מגוונות ולא כל פעם אותו מטוס מאותו חברה";
   "העמדות הגדולות הם לא רק למטוסי ענק … כמה סוגי מטוסים יכולים לחנות בכל עמדה"; 14:35: "בדיקה רצינית של כל מטוס בכל עמדה … פרטי לא יהיה ב-P1–6") ====
   מצאתי: ‏019l2 (fieldthru) קובע לכל טיסה model + legs פעם אחת בטעינה, ובכל סבב מתחלפת רק החברה (074zv:ftrAt); fieldfix (074zp2:ffmxSet) — רק זהות, אותו דגם.
   כאן (כלל 19א — אותה החלפה מחוץ לעולם כמו ftrAt / ffmxSet, אותם נתונים — S15SIM.flights / veh / sched): לכל טיסה — גרסאות לסוגים אחרים שנכנסים בעמדה
   (stands_matrix של fieldcalc + הכלל של הבעלים), שנוצרו בכלי deliver/2026-11-17/fieldthru2/tools/ft2_var.py (שדרוג של ft_sim.py:variant_of): אותה המראה ואותה
   נגיעה (המסלול והספירה לא משתנים), מגיעה לקו ההמתנה באותו רגע, נעצרת בקו העצירה של הסוג (FC_STOPS), והגרר — נסיעה חדשה לגרסה; והסבב (5 סבבים = שעה) נבדק
   בכלי סבב-סבב, כל הטיסות של הסבב יחד, במדויק (ft2_seq.py). בכל סבב (720 ש׳) — ביקור אחד מסוג אחד: ההחלפה כשהמטוס מחוץ לעולם (בין ההמראה לגישה), הנסיעה של
   הגרר מתחלפת כשהוא בבית, ומתאפסים המטמונים של העמדה — השרוול (S15GR.bpar), הנוסעים (S15J.plan; המספר לפי הסוג — 074m:s15fbFlight עטוף), המכוון (S15E.plans).
   הסבב: ''' + info + '''
   לשירות (fieldsvc): FTY.onSwap(fn) — fn(טיסה, אינדקס הגרסה, הגרסה) בכל החלפה; FTY.visits(fid) — כל הסוגים של הטיסה וחלונות העמידה שלהם. ‎#fty=0 — בלי. ==== */
'''
js = head + 'var FTY={on:!/[#&]fty=0/.test(String((typeof location!=="undefined"&&location.hash)||"")),K:' + str(S.get('K', 5)) + ',seats:' + json.dumps(SEATS, separators=(',', ':')) + ',add:' + json.dumps(add, ensure_ascii=False, separators=(',', ':')) + r''',
 base:{},vbase:{},cur:{},pend:[],n:{swap:0,veh:0,vdefer:0,cb:0},log:[],err:'',cb:[]};
FTY.onSwap=function(fn){if(typeof fn==='function')FTY.cb.push(fn)};
FTY.visits=function(fid){const A=FTY.add[fid];if(!A)return null;const f=S15SIM.flights.find(x=>x.id===fid),b=FTY.base[fid]||(f?{ac:f.model,park:f.park,legs:f.legs}:null);
 return A.seq.map((j,k)=>{const v=j?A.vars[j]:b;const L=v.legs[v.legs.length-1];return{k,ac:v.ac,park:v.park||[L.t0,L.t1],cur:FTY.cur[fid]===j}})};
function ftvTrips(L){const out=[];let cur=[];for(const g of L){if(g.h!=null&&g.f===0){if(cur.length){out.push(cur);cur=[]}continue}cur.push(g)}if(cur.length)out.push(cur);return out}
function ftvBuild(trs,home,hh,T){trs=trs.slice().sort((a,b)=>a[0].t0-b[0].t0);const b0=trs[0][0].t0;
 trs=trs.map(tr=>{const d=tr[0].t0-b0>=T-1e-6?T*Math.floor((tr[0].t0-b0)/T):0;return d?tr.map(g=>Object.assign({},g,{t0:g.t0-d,t1:g.t1-d})):tr}).sort((a,b)=>a[0].t0-b[0].t0);
 const L=[],t1=trs[0][0].t0;for(let i=0;i<trs.length;i++){if(i)L.push({p:[home.slice()],t0:trs[i-1][trs[i-1].length-1].t1,t1:trs[i][0].t0,h:hh,f:0});for(const g of trs[i])L.push(g)}
 L.push({p:[home.slice()],t0:trs[trs.length-1][trs[trs.length-1].length-1].t1,t1:t1+T,h:hh,f:0});return L}
function ftvHome(v){for(let i=v.legs.length-1;i>=0;i--){const g=v.legs[i];if(g.h!=null&&g.f===0)return{p:g.p[0],h:g.h}}return null}
function ftvSnap(f){if(FTY.base[f.id])return FTY.base[f.id];const q=S15SIM.sched.find(s=>s[0]===f.home);return FTY.base[f.id]={ac:f.model,L:f.L,W:f.W,legs:f.legs,park:f.park,al:f.airline,sched:q?q.slice():null}}
// הנסיעה של הגרר לטיסה fid בגרסה (trip: מערך — הנסיעה; null — הגרר הזה לא יוצא בסבב הזה (גרר אחר מהצי, AF); undefined — כמו בלוח):
// מוחלפת / נוספת / יורדת — רק כשהרכב בבית, ולא בתוך הנסיעה הישנה / החדשה
function ftvVehTry(p,tc,force){const T=S15SIM.T,v=S15SIM.veh.find(x=>x.id===p.vid);if(!v)return true;const H=ftvHome(v);if(!H)return true;
 const trs=ftvTrips(v.legs),i=trs.findIndex(tr=>tr.some(g=>g.att===p.fid)),key=p.vid+'|'+p.fid;if(FTY.vbase[key]===undefined)FTY.vbase[key]=i>=0?trs[i]:null;
 const nw=p.trip===undefined?FTY.vbase[key]:p.trip,cur=i>=0?trs[i]:null;if(nw===cur)return true;
 if(!force){const P=s15PoseAt(v,tc);if(!P||P[4]!==0||Math.hypot(P[0]-H.p[0],P[1]-H.p[1])>2)return false;
  for(const tr of [cur,nw]){if(!tr)continue;const a=tr[0].t0,d=tr[tr.length-1].t1-a;if((((tc-a)%T)+T)%T<=d+1)return false}}
 if(i>=0){if(nw)trs[i]=nw;else trs.splice(i,1)}else if(nw)trs.push(nw);
 v.legs=trs.length?ftvBuild(trs,H.p,H.h,T):[{p:[H.p.slice()],t0:0,t1:T,h:H.h,f:0}];FTY.n.veh++;return true}
function ftvApply(f,j,force,tc){const A=FTY.add[f.id],b=ftvSnap(f),v=j?A.vars[j]:b,T=S15SIM.T;
 f.model=v.ac;f.L=v.L;f.W=v.W;f.legs=v.legs;if(v.park)f.park=v.park;else delete f.park;
 const ga=/^AC-(LT|PR|BJ|CN|AM)/;if(ga.test(v.ac))f.airline='GA';else if(ga.test(b.ac)===false&&f.airline==='GA')f.airline=b.al;else if(ga.test(b.ac))f.airline=b.al;   // מנהלים / פרטי — הצבע לפי המזהה (074zn), לא חברת נוסעים
 const q=S15SIM.sched.find(s=>s[0]===f.home);if(q){q[1]=v.ac;q[2]=f.airline;q[4]=+((((v.legs[0].t0%T)+T)%T).toFixed(2))}
 const vids=new Set();for(const w of A.vars)if(w)for(const k of Object.keys(w.tugs||{}))vids.add(k);
 for(const vid of vids){const p={vid,fid:f.id,trip:j&&v.tugs&&(vid in v.tugs)?v.tugs[vid]:undefined};FTY.pend=FTY.pend.filter(x=>!(x.vid===vid&&x.fid===f.id));if(!ftvVehTry(p,tc||0,force)){FTY.pend.push(p);FTY.n.vdefer++}}
 try{if(typeof S15GR!=='undefined'&&S15GR.bpar)S15GR.bpar.delete(f.home+'|L')}catch(e){}
 try{if(typeof S15J!=='undefined'){S15J.plan=null;S15J.planTry=0;S15J.planNext=0}}catch(e){}
 try{if(typeof S15E!=='undefined')S15E.plans=null}catch(e){}
 FTY.cur[f.id]=j;if(!force){FTY.n.swap++;FTY.log.push(f.home+' → '+v.ac);if(FTY.log.length>16)FTY.log.shift()}
 for(const fn of FTY.cb){try{fn(f,j,v);FTY.n.cb++}catch(e){}}}
function ftvWant(fid,k){const A=FTY.add[fid];return A.seq[((k%A.seq.length)+A.seq.length)%A.seq.length]}
function ftvStep(tc,clk){if(!FTY.on)return;try{if(typeof FFMX!=='undefined'&&FFMX.on&&!FFMX.pairs)return}catch(e){}   // קודם הזוגות של מחזור התחזוקה (074zp2:ffmxPairs — לפי הדגם) נקבעים על הלוח, ורק אחר כך מחליפים סוגים
 const T=S15SIM.T,k=Math.floor(clk.abs/T);
 for(const fid in FTY.add){const f=S15SIM.flights.find(x=>x.id===fid);if(!f)continue;const w=ftvWant(fid,k),c=FTY.cur[fid]||0;if(w===c)continue;
  if(s15PoseAt(f,tc))continue;ftvApply(f,w,false,tc)}
 if(FTY.pend.length)FTY.pend=FTY.pend.filter(p=>!ftvVehTry(p,tc,false))}
(function(){try{for(const f of S15SIM.flights)if(FTY.add[f.id])ftvSnap(f);if(typeof S15H==='undefined'||!S15H.live)return;
 S15H.live.air.push((now,tc,clk)=>{try{ftvStep(tc,clk)}catch(e){FTY.err=String(e).slice(0,160)}})}catch(e){FTY.err='init '+e}})();
// השרוול לפי הסוג (074k:s15grBrLen — המטמון '<עמדה>|L' נבנה מהמטוס הראשון): כשהסוג שונה מזה שבמטמון — נבנה מחדש לסוג (גם בבדיקות של שדה 2 / fieldcalc)
(function(){try{const l0=s15grBrLen;s15grBrLen=function(b,dk,A){try{const k=b.stand+'|L',C=S15GR.bpar.get(k);if(C&&A&&C.ac&&C.ac!==A.ac)S15GR.bpar.delete(k);const r=l0.apply(this,arguments);if(r&&A&&!r.ac)r.ac=A.ac;return r}catch(e){return l0.apply(this,arguments)}}}catch(e){FTY.err='br '+e}})();
// הנוסעים לפי הסוג: 074m:s15fbFlight נותן 12–18 לכל טיסה; בגרסה — לפי המושבים ביחס לסוג של הלוח (הטיסה של הלוח — בלי שינוי)
(function(){try{const f0=s15fbFlight;s15fbFlight=function(b,A,P){const r=f0.apply(this,arguments);try{if(!r||!r.pax||!A||!A.f||!FTY.add[A.f.id])return r;const B=FTY.base[A.f.id];if(!B||B.ac===A.ac)return r;
  const s0=FTY.seats[B.ac]||100,s1=FTY.seats[A.ac]||100,x=r.pax,k=Math.max(.35,Math.min(2,s1/s0)),n=Math.max(3,Math.round(x.count*k)),room=(x.dep.end-x.arr.start-4)/2,c=Math.max(1,Math.min(n,Math.floor((room-x.travel)/x.gap)+1));
  if(c!==x.count){const dur=x.travel+(c-1)*x.gap;x.count=c;x.arr={start:x.arr.start,end:x.arr.start+dur};x.dep={start:Math.max(x.arr.end+4,x.dep.end-dur),end:x.dep.end}}}catch(e){}return r}}catch(e){FTY.err='pax '+e}})();
/* הבדיקה (בתוך roadAudit) — fieldthru_types: לכל אחד מ-K הסבבים — כל הטיסות בגרסה של הסבב (והגררים שלהן): s15SimAudit — 0 חפיפות; כל עמדת שרוול עוגנת (התא ≤ 0.35 מ׳ מהדלת)
   באמצע העמידה; כל גרסה — הגרר צמוד בדחיפה; ואחרי הבדיקה — הכול חוזר בדיוק למצב שהיה (טיסות, רכבים, מטמונים) */
function ftvAudit(){const T=S15SIM.T,K=FTY.K,R={ok:true,issues:[],cycles:[],types:{},n:Object.keys(FTY.add).length};if(!FTY.on||!R.n)return Object.assign(R,{ok:!FTY.err,skip:true});
 const keepF=new Map(S15SIM.flights.map(f=>[f,{model:f.model,L:f.L,W:f.W,legs:f.legs,park:f.park}])),keepV=new Map(S15SIM.veh.map(v=>[v,v.legs])),keepC=Object.assign({},FTY.cur),keepS=S15SIM.sched.map(q=>q.slice()),keepP=FTY.pend.slice();
 const sh=ac=>String(ac).replace(/^AC-|-01$/g,'');
 try{for(let k=0;k<K;k++){const row={k:k+1,types:{},overlap:null,bridge:[],tug:[]};
   for(const fid in FTY.add){const f=S15SIM.flights.find(x=>x.id===fid);if(!f)continue;const j=ftvWant(fid,k);ftvApply(f,j,true,0);row.types[f.home]=sh(f.model);(R.types[f.home]=R.types[f.home]||new Set()).add(f.model)}
   try{const q=s15SimAudit(1);row.overlap=q.ok?0:q.issues.length;if(!q.ok)R.issues.push('סבב '+(k+1)+': חפיפות '+q.issues.slice(0,3).map(x=>typeof x==='string'?x:JSON.stringify(x)).join(' | ').slice(0,200))}catch(e){row.overlap='שגיאה';R.issues.push('סבב '+(k+1)+' s15SimAudit '+e)}
   try{if(typeof S15D!=='undefined'&&S15D.bridges&&typeof s15grBrPose==='function'){for(const b of S15D.bridges){const f=S15SIM.flights.find(x=>x.home===b.stand);if(!f||!FTY.add[f.id])continue;S15GR.bpar.delete(b.stand+'|L');
     const L=f.legs[f.legs.length-1],tm=(L.t0+L.t1)/2,A=s15grAcAt(b.stand,(((tm%T)+T)%T));const P=A&&!A.away?s15grBrPose(b,A,1):null,d=P&&P.door?Math.hypot(P.front[0]-P.door[0],P.front[1]-P.door[1])/A34_PXM:null;
     if(!P||!P.docked||d==null||d>.35){row.bridge.push(b.stand+' '+sh(f.model)+' '+(d==null?'—':d.toFixed(2)+' מ׳'));R.issues.push('סבב '+(k+1)+': השרוול ב-'+b.stand+' לא עוגן ב-'+sh(f.model))}}}}catch(e){R.issues.push('שרוול '+e)}
   for(const fid in FTY.add){const f=S15SIM.flights.find(x=>x.id===fid);if(!f)continue;const g=f.legs[0];if(!S15SIM.veh.some(v=>v.legs.some(h=>h.att===fid&&Math.abs(h.t0-g.t0)<.05))){row.tug.push(f.home);R.issues.push('סבב '+(k+1)+': בלי גרר ב-'+f.home)}}
   R.cycles.push(row)}}
 catch(e){R.issues.push(String(e).slice(0,200))}
 finally{for(const [f,o] of keepF){f.model=o.model;f.L=o.L;f.W=o.W;f.legs=o.legs;if(o.park)f.park=o.park;else delete f.park}for(const [v,L] of keepV)v.legs=L;FTY.cur=keepC;FTY.pend=keepP;
  for(let i=0;i<S15SIM.sched.length&&i<keepS.length;i++)S15SIM.sched[i]=keepS[i];try{for(const fid in FTY.add){const f=S15SIM.flights.find(x=>x.id===fid);if(f)S15GR.bpar.delete(f.home+'|L')}S15J.plan=null;S15J.planTry=0;S15E.plans=null}catch(e){}}
 const multi=Object.entries(R.types).filter(([s,v])=>v.size>1);R.multi=multi.length;R.ok=!R.issues.length&&multi.length>=Math.min(5,R.n)&&!FTY.err;if(FTY.err)R.issues.push(FTY.err);
 R.types=Object.fromEntries(Object.entries(R.types).map(([s,v])=>[s,[...v].map(sh)]));return R}
(function(){const base=roadAudit;roadAudit=function(){const r=base.apply(this,arguments);try{const A=ftvAudit(),L=r.checks||r.results;if(A.skip)return r;
 const det=(A.ok?'':'נכשל: '+A.issues.slice(0,4).join(' | ')+' · ')+'סוגים לעמדה בשעה ('+FTY.K+' סבבים): '+Object.entries(A.types).map(([s,v])=>s+' '+v.join('/')).join(', ')+' · '+A.cycles.map(c=>'סבב '+c.k+': חפיפות '+c.overlap+(c.bridge.length?' שרוול ✗ '+c.bridge.join(','):'')+(c.tug.length?' בלי גרר '+c.tug.join(','):'')).join(' · ')+' · החלפות במשחק '+FTY.n.swap+', גררים '+FTY.n.veh;
 if(Array.isArray(L))L.push({name:'fieldthru_types',id:'fieldthru_types',ok:A.ok,pass:A.ok,detail:det});if(!A.ok){r.ok=false;(r.issues||[]).push('fieldthru_types')}}catch(e){}return r}})();
window.__TC_FTY={audit:ftvAudit,visits:FTY.visits,log:()=>FTY.log,made:()=>({swap:FTY.n.swap,veh:FTY.n.veh,pend:FTY.pend.length,cur:FTY.cur}),onSwap:FTY.onSwap};
'''
p = os.path.join(G, 'parts', '074zv1_ft_types.js'); open(p, 'w', encoding='utf-8').write(js)
m = json.load(open(os.path.join(G, 'manifest.json'), encoding='utf-8')); names = [q['name'] for q in m['parts']]
if '074zv1_ft_types.js' not in names:
    i = names.index('074zv_fieldthru_audit.js'); m['parts'].insert(i + 1, dict(name='074zv1_ft_types.js', block=m['parts'][i]['block']))
    json.dump(m, open(os.path.join(G, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(subprocess.run(['python3', '/home/user/tc_root/tc/pkg/work/tools_pack/manifest_tool.py', 'refresh', G], capture_output=True, text=True).stdout.strip()[:300], len(js), 'בתים')
