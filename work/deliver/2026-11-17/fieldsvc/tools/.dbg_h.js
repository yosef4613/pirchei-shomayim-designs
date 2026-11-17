// fs_harness.js — fieldsvc: המתכנן של 074zz5 מחוץ לדפדפן, על dump מהמשחק (dump_game.js עם S15D מלא ו-fsx — המקומות ליד המטוס).
// הפונקציות של הבדיקה (s15w4Clear / s15kSample / s15kHits / s15Boxes / s15PoseAt …) — מועתקות מהחלקים עצמם (חילוץ לפי שם), לא כתובות מחדש.
// שימוש: node fs_harness.js <dump.json> <src_game_dir> [out.json]
const fs=require('fs'),path=require('path');
const [dumpF,src,outF]=process.argv.slice(2);const D=JSON.parse(fs.readFileSync(dumpF,'utf8'));
// המצב שלפני התכנון: בלי הרכבים של fieldsvc (fsv) ובלי המפרצים שלו
{const mine=new Set(D.veh.filter(v=>v.fsv).map(v=>v.id));D.veh=D.veh.filter(v=>!v.fsv);for(const [k,sp] of Object.entries(D.S15D.spots))if(sp.fsv)delete D.S15D.spots[k];
 D.moving=D.moving.filter(id=>!mine.has(id)||D.veh.some(v=>v.id===id));D.S15SIM={T:D.T,flights:D.flights,veh:D.veh,sched:D.sched,ngf:D.ngf,tows:D.tows};D.S15D.spots=Object.assign({},D.S15D.spots)}
function grab(file,names){const s=fs.readFileSync(path.join(src,'parts',file),'utf8');let out='';
 for(const nm of names){const re=new RegExp('(^|\\n)\\s*(function\\s+'+nm+'\\s*\\(|const\\s+'+nm+'\\s*=|var\\s+'+nm+'\\s*=|let\\s+'+nm+'\\s*=)');const m=re.exec(s);if(!m)throw new Error('לא נמצא '+nm+' ב-'+file);
  let i=m.index+m[1].length;let j=i,depth=0,started=false,q=null;
  for(;j<s.length;j++){const ch=s[j];if(q){if(ch==='\\'){j++;continue}if(ch===q)q=null;continue}
   if(ch==='"'||ch==="'"||ch==='`'){q=ch;continue}if(ch==='/'&&s[j+1]==='/'){while(j<s.length&&s[j]!=='\n')j++;if(started&&depth===0)break;continue}if(ch==='/'&&s[j+1]==='*'){j=s.indexOf('*/',j+2)+1;continue}
   if(ch==='{'||ch==='['||ch==='('){depth++;started=true}else if(ch==='}'||ch===']'||ch===')'){depth--;if(started&&depth===0){if(/^\s*function/.test(s.slice(i,i+12))&&ch==='}'){j++;break}}}
   else if(ch===';'&&depth===0&&started&&!/^\s*function/.test(s.slice(i,i+12))){j++;break}
   else if(ch==='\n'&&depth===0&&started&&!/^\s*function/.test(s.slice(i,i+12))){break}}
  out+=s.slice(i,j)+'\n'}return out}
let code='';
code+=grab('019m_S15_draw.js',['s15PoseLeg','s15PoseAt']);
code+=grab('074j_S15_live.js',['s15ObbHit','s15Boxes']);
code+=grab('074o_S15h_gse.js',['s15w4Round','s15w4Len','s15w4Clear','S15W4_AC','s15w4AcBoxes','s15w4Col']);
code+=grab('074r_S15k_fleet.js',['S15K_VT','s15kType','s15kVmax','s15kDims','s15kNC','S15K_DT','s15kObb','s15kGap','s15kSample','s15kStatic','s15kHits']);
code+=grab('074k_S15c_ground.js',['s15grDims','s15grType']);
// החלק שלי — כולו, עם תחליפים לציור ולמשחק
const mine=fs.readFileSync(path.join(src,'parts','074zz5_fieldsvc.js'),'utf8');
const pre=`var S15SIM=D.S15SIM,S15D=D.S15D;var S15_FL={};for(const a of S15SIM.flights)S15_FL[a.id]=a;var S15_MOVING=new Set(D.moving);
var S15W4={RR:D.W4.RR,vF:D.W4.vF,vR:D.W4.vR,jobs:{}},S15W4S={jobs:{}},S15GR={PX:D.GR.PX,VK:D.GR.VK},S15GR_CART=D.CART,S6A_TYPES=D.S6A,S15GR_T=D.GRT,S15K={v4:D.v4||{}},S15K_PXK=1,AF={VMAX:{}};
var S15G={ids:new Set()};var location={hash:''};var window={};var performance={now:()=>Date.now()};var process_=1;
function setTimeout(){};function s15kErr(){};function s15w4Err(){};
var s15grKit=function(){},s15DrawVeh=function(){},s15Live=function(){},roadAudit=function(){return{}};
var __TC_FC={NEED:{}};var APT_Y={LS:0},APTT_SPEC=1;var S15GR_BRP=D.BRP||{P1:[6599,910],P2:[7127,739],P3:[7470,691],P4:[7853,679],P5:[8286,763],P6:[8874,910]};
`;
const post=`
// המקום והזמנים — מהמשחק (fsx), כי הם תלויים במנוע הישן (g77SvcSpot / afPos / s15w4CatSpot)
fsvOldSpot=function(A,kind){const r=D.fsx[A.f.id];return r&&r.old&&r.old[kind]||null};
fsvFuelSpot=function(A){const r=D.fsx[A.f.id];return r&&(r.fuel||(r.sp&&r.sp.FT))||null};
fsvDoorR1=function(A){const r=D.fsx[A.f.id];return r&&(r.door||(r.sp&&r.sp.AL&&r.sp.AL.D))||null};
s15w4CatSpot=function(A){const r=D.fsx[A.f.id];return r&&(r.cat||(r.sp&&r.sp.CT))||null};
s15w4Hold=function(sid,ac,fid){const r=D.fsx[fid];return r&&r.cathold||120};
s15kVmax=function(t){return (D.vmax&&D.vmax[t])||0};
const _act=fsvActOf;fsvActOf=function(v,c){return FSV.own.has(v.id)?'fieldsvc':(_act(v,c)||'(בחלק אחר)')};
console.log('חתימה',fsvSig(),'במשחק',D.fspre&&JSON.parse(D.fspre).sig);
FSV.budget=+(process.env.FSB||60000);FSV.jobBudget=+(process.env.FSJ||4000);FSV.dbg=[];const AS=fsvStands();const A=AS.find(a=>a.f.id===process.env.FID);const c=process.env.CODE;const S=fsvSpot(A,c);const out=[];out.push('S '+JSON.stringify(S));const [L,W]=fsvDims(c);const tm=fsvTiming(A,c);for(const src of fsvSources(A,c).slice(0,3)){const HA=fsvHomeAccess(src.H);for(const ha of HA)for(const ap of fsvApproaches(S,A,S.th!=null).slice(0,4)){FSV.why='';const tr=fsvTrip(src.H,ha,ap,S,tm.hold,A.ob+30,40);if(!tr){out.push(src.id+' '+ha.s.id+'→'+ap.s.id+' null '+FSV.whyF);continue}const hit=fsvStaticHit(tr,L,W,src.kind!=='bay'?src.id:null);out.push(src.kind+':'+(src.id||src.pk)+' H'+[src.H.x,src.H.y,src.H.h.toFixed(2)]+' '+ha.s.id+'→'+ap.s.id+' hit='+hit+' '+FSV.why+' | '+tr.legs.filter(g=>g.f===1).map(g=>(g.r?'R':'F')+'['+g.p[0].map(Math.round)+'→'+g.p[g.p.length-1].map(Math.round)+']').join(' '))}}console.log(out.join('\n'));return{FSV,audit:{full:0,flights:0,missing:[],wheelchairW:0},veh:[]};`;
const body=pre.replace('var process_=1;','var process={env:'+JSON.stringify({FSONLY:process.env.FSONLY||''})+'};')+code+mine+post;
const t0=Date.now();let R;
try{R=new Function('D','s15eSk','s15eSd','g77SvcSpot','afPos','s15grDoors','s15grDoorW','s15ePost','apttAcGeom','s15grLive','c34Now','C34','s15gAct',body.replace(/^function s15w4CatSpot/m,'var _cs=function').replace('var __TC_FC','var s15w4CatSpot,s15w4Hold;var __TC_FC'))(D,()=>10/7.47,()=>({}),()=>null,()=>null,()=>[],()=>[0,0],()=>null,()=>({F:[0,0,0,0]}),()=>false,()=>false,{},()=>{})}
catch(e){console.error('שגיאה:',e.stack.split('\n').slice(0,6).join('\n'));process.exit(1)}
const A=R.audit;console.log('זמן',Date.now()-t0,'מ״ש · נסיעות',R.FSV.trips,'· מועמדים',JSON.stringify(R.FSV.n),'· שגיאה',R.FSV.err);
console.log('מלאות',A.full,'/',A.flights,'· כיסא',A.wheelchairW);for(const m of A.missing)console.log('  ',m);
console.log('יומן:');for(const l of R.FSV.log)console.log('  ',l);
if(outF)fs.writeFileSync(outF,JSON.stringify({audit:A,log:R.FSV.log,veh:R.veh,made:R.FSV.made,dbg:R.FSV.dbg}));
const W={};for(const l of R.FSV.dbg){const k=l.split(' → ')[1].replace(/ @\d+.*/,'').replace(/\d+,\d+/,'');W[k]=(W[k]||0)+1}console.log('סיבות:',JSON.stringify(Object.entries(W).sort((a,b)=>b[1]-a[1]).slice(0,25)));
