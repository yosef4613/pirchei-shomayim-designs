// oilcycle.js <074zv_sealife_oil.js> — sealife: המחזור של "אורה" (ריקה → המתנה → מטען חדש → הזרמה) ב-3 ימי משחק; הכמות נשמרת (כולל bal.load)
const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');let MIN=420;
const f=new Function('MINF',`var S10D={pipe:{x:2728,z_m:8.6}},S10KIT={over(){},c6d6:{shipOf(){return{x:2728,y:5638,B:203}}}},S9_HOOKS={over:[]},WTC_LP=0;function simStep(){};function wtcOverLive(){};function lgMinOfDay(){return MINF()%1440};var window={};`+src+`;return OILX;`);
const O=f(()=>MIN);const S=O.S;const sum=()=>S.ship+S.ref[0]+S.ref[1]+S.buf[0]+S.buf[1];const s0=sum();let pl=0,pumpMin=0,flowHours=new Set(),seen=[];
for(let i=0;i<3*1440*2;i++){const b=S.dayPlant;O.step(.5);MIN+=.5;pl+=S.dayPlant-b;if(S.q>1){pumpMin+=.5;flowHours.add(Math.floor(MIN/60))}if(seen[seen.length-1]!==S.ph)seen.push(S.ph)}
const ph=seen.filter(p=>['empty','refill'].includes(p));
const r={diff:+(s0+S.bal.load-sum()-pl).toFixed(4),loads:S.loads,pumpH:+(pumpMin/60).toFixed(1),hoursWithShipFlow:flowHours.size,of:72,refills:ph.join('>'),st:O.state()};
r.ok=Math.abs(r.diff)<1e-3&&S.loads>=1&&!S.ERR&&r.hoursWithShipFlow>=36;console.log(JSON.stringify(r).slice(0,900));
