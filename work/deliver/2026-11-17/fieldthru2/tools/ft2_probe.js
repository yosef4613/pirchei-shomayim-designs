// ft2_probe.js — fieldthru2: מדידה במשחק (קריאה בלבד): השרוול של כל עמדת שרוול × סוג בקו העצירה של הסוג (FC_STOPS של fieldcalc — לא בקו של העמדה),
// כמו FCBR.matrix של 074zr2 (אותן פונקציות: s15grAcEnv / s15grBrPose / g77K72Parts / g77PolyGap), והעלות של בנייה מחדש של התוכניות (נוסעים / מכוון).
// node ft2_probe.js <build> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  if (/try7412\.html$/.test(file) && process.env.FT2_DISPATCH !== '0') {   // המקום בתור שנלקח ב-13:51 — מנוצל לבדיקה המהירה של הניסיון האחרון (gate2.sh quick)
    const cp = require('child_process'); try { cp.execSync('bash ' + __dirname + '/gate2.sh ' + (process.env.FT2_NEXT || 'try8080') + ' quick', { stdio: 'inherit', timeout: 870000 }) } catch (e) { console.error('gate2 ' + String(e).slice(0, 200)) }
    return;
  }
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(8000);
  const s = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const R={rows:[],accept:null,cost:{},err:[]};
   try{R.accept=FCBR.matrix(true).accept}catch(e){R.err.push('matrix '+e)}
   const TY=['AC-NB-01','AC-RJ-01','AC-QJ-01','AC-TP-01','AC-MW-01','AC-LG-01','AC-CG-01'],LIM={door:.35,dock:1.0,rest:2.4},Sk=10/A34_PXM;
   const lpx=ac=>(typeof S15_LPX!=='undefined'&&S15_LPX[ac])||({'AC-LG-01':668,'AC-NB-01':376,'AC-RJ-01':317})[ac]||300,j=(a,c)=>Math.hypot(a[0]-c[0],a[1]-c[1]);
   const snap=new Map(S15GR.bpar);
   try{for(const b of S15D.bridges){try{s15grBrPose(b,null,0)}catch(e){}const snap2=new Map(S15GR.bpar);
    for(const ac of TY){const s=S15D.stands[b.stand],ng=(S15SIM.ngf&&S15SIM.ngf[ac])||.12,ny=(FC_STOPS[b.stand]||{})[ac];const r={stand:b.stand,ac,ny:ny==null?null:ny,nose:s.nose};
     try{if(ny==null){r.ok=false;r.why=['אין קו עצירה'];R.rows.push(r);continue}
      for(const fresh of [0,1]){if(fresh){S15GR.bpar.delete(b.stand+'|L')}
      const A={ac,x:s.cx,y:ny-ng*lpx(ac),th:Math.PI/2,sid:b.stand,stat:true},env=s15grAcEnv(ac,[A.x,A.y,A.th],Sk),R0=s.rect,o={};
      o.inStand=env.every(E=>E.every(p=>p[0]*Sk>=R0[0]-1&&p[0]*Sk<=R0[2]+1&&p[1]*Sk>=R0[1]-1&&p[1]*Sk<=R0[3]+1));
      for(const [k,e] of [['dock',1],['rest',0]]){const P=s15grBrPose(b,A,e);if(!P){o[k]=null;continue}const Q=g77K72Parts(P);let mf=1e9;
       for(const [nm,pp] of [['A',Q.A],['B',Q.Bt],['bel2',Q.bel2],['cab',Q.cab]]){if(k==='dock'&&(nm==='cab'||nm==='bel2'))continue;for(const E of env)mf=Math.min(mf,g77PolyGap(pp,E))}
       o[k]={docked:!!P.docked,door:P.door?+(j(P.front,P.door)/A34_PXM).toFixed(2):null,clr:+(mf/A34_PXM).toFixed(2),L:+(P.L/A34_PXM).toFixed(1)}}
      const why=[];if(!o.inStand)why.push('לא בעמדה');if(!o.dock||!o.dock.docked||o.dock.door==null||o.dock.door>LIM.door)why.push('התא '+(o.dock&&o.dock.door!=null?o.dock.door:'—')+' מ׳');
      if(o.dock&&o.dock.clr<LIM.dock)why.push('המנהרה '+o.dock.clr);if(!o.rest||o.rest.clr<LIM.rest)why.push('מנוחה '+(o.rest?o.rest.clr:'—'));
      o.ok=!why.length;o.why=why;r[fresh?'fresh':'cached']=o}
      r.ok=r.fresh.ok}catch(e){r.ok=false;r.why=['שגיאה '+String(e).slice(0,120)]}
     R.rows.push(r);S15GR.bpar.clear();for(const [k,v] of snap2)S15GR.bpar.set(k,v)}}}
   catch(e){R.err.push('rows '+e)}finally{S15GR.bpar.clear();for(const [k,v] of snap)S15GR.bpar.set(k,v)}
   try{const t0=performance.now();const keep=S15J.plan;S15J.plan=null;S15J.planTry=0;S15J.planNext=0;const P=s15jPlanBuild();R.cost.pax=+(performance.now()-t0).toFixed(1);R.pax=P.flights.map(f=>({g:f.g,code:f.code,nA:f.nA,nD:f.nD,dur:f.dur}));S15J.plan=keep}catch(e){R.err.push('pax '+e)}
   try{const t0=performance.now();const keep=S15E.plans;S15E.plans=null;const P=s15ePlans();R.cost.marshal=+(performance.now()-t0).toFixed(1);R.marshal=P.length;S15E.plans=keep}catch(e){R.err.push('marshal '+e)}
   try{R.models={};for(const id of ['AC-HC-01','AC-MW-01','AC-CG-01','AC-LG-01','AC-QJ-01','AC-TP-01']){const a=TurboCity.get(id);R.models[id]=a?{ok:true,res:a.res||null,info:(()=>{try{const I=TurboCity.info(id,{scale:1,rot:0});return{w:I.w,h:I.h}}catch(e){return String(e).slice(0,80)}})()}:{ok:false}}}catch(e){R.err.push('models '+e)}
   try{R.ftv=window.__TC_FTV?{made:__TC_FTV.made(),log:__TC_FTV.log(),audit:__TC_FTV.audit()}:null}catch(e){R.err.push('ftv '+e)}
   try{R.sched=S15SIM.sched;R.lpx=typeof S15_LPX!=='undefined'?S15_LPX:null}catch(e){}
   return JSON.stringify(R)})()`));
  const o = JSON.parse(s); o.errs = errs; fs.writeFileSync(out, JSON.stringify(o)); console.log('ok', s.length, 'errs', errs.length); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
