// q_bridges.js — fieldcalc: כל עמדת שרוול × כל סוג (QA-79 של הישן — 047/048: "every bridge stand × accepted type × state"), על השרוולים של S15 (074k: s15grBrPose / K-72)
// לכל צירוף: מטוס חונה מהסוג בעמדה (כמו s15grAcAt של מטוס שחונה קבוע), השרוול בעגינה (e=1) ובמנוחה (e=0): התא מהדלת (מ׳), המנהרה מהגוף / מהכנף (מ׳), זווית העגינה
return (()=>{const out={rows:[],err:null};try{const Sk=10/A34_PXM,K=G77_K72,j=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
 const TYPES=['AC-NB-01','AC-RJ-01','AC-LG-01','AC-QJ-01','AC-MW-01','AC-TP-01'];
 for(const b of S15D.bridges){const s=S15D.stands[b.stand];for(const ac of TYPES){const r={stand:b.stand,ac};try{
   const ng=(S15SIM.ngf&&S15SIM.ngf[ac])||.12,Lpx=(typeof S15_LPX!=='undefined'&&S15_LPX[ac])||({'AC-LG-01':668,'AC-NB-01':376,'AC-RJ-01':317})[ac]||300;
   const A={ac,x:s.cx,y:s.nose-ng*Lpx,th:Math.PI/2,sid:b.stand,stat:true};r.Lpx=Lpx;r.doors=(s15grDoors(ac)||[]).length;
   const env=s15grAcEnv(ac,[A.x,A.y,A.th],Sk);
   // המעטפת בתוך העמדה
   const R0=s.rect;r.inStand=env.every(E=>E.every(p=>p[0]*Sk>=R0[0]-1&&p[0]*Sk<=R0[2]+1&&p[1]*Sk>=R0[1]-1&&p[1]*Sk<=R0[3]+1));
   for(const [k,e] of [['dock',1],['rest',0]]){const P=s15grBrPose(b,A,e);if(!P){r[k]='אין פוזה';continue}const Q=g77K72Parts(P);let mf=1e9;
    for(const [nm,p] of [['A',Q.A],['B',Q.Bt],['bel2',Q.bel2],['cab',Q.cab]]){if(k==='dock'&&(nm==='cab'||nm==='bel2'))continue;for(const E of env)mf=Math.min(mf,g77PolyGap(p,E))}
    r[k]={docked:!!P.docked,door:P.door?+(j(P.front,P.door)/A34_PXM).toFixed(2):null,clr:+(mf/A34_PXM).toFixed(2),ang:+((P.th-P.T)*180/Math.PI).toFixed(1),L:+(P.L/A34_PXM).toFixed(1),ph:P.ph}}
   r.ok=!!(r.dock&&r.dock.docked&&r.dock.door!=null&&r.dock.door<=.35&&r.dock.clr>=1/A34_PXM*0+.1&&r.rest&&r.rest.clr>=2.4&&r.inStand)}catch(e){r.err=String(e).slice(0,200)}out.rows.push(r)}}
 }catch(e){out.err=String(e&&e.stack||e).slice(0,400)}return out})()
