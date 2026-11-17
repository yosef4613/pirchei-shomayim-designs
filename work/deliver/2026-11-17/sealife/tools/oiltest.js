const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const f=new Function(`var S10D={pipe:{x:2728,z_m:8.6}},S10KIT={over(){},c6d6:{shipOf(){return{x:2728,y:5638,B:203}}}},S9_HOOKS={over:[]},WTC_LP=0;function simStep(){};function wtcOverLive(){};function lgMinOfDay(){return 600};var window={};`+src+`;return OILX;`);
const O=f();const S=O.S;const sum=()=>S.ship+S.ref[0]+S.ref[1]+S.buf[0]+S.buf[1];let s0=sum(),pl=0;const seen=[];
for(let i=0;i<3000;i++){const before=S.dayPlant;O.step(.5);pl+=S.dayPlant-before;if(seen[seen.length-1]!==S.ph)seen.push(S.ph)}
console.log('phases',seen.join('>'),'diff',(s0-sum()-pl).toFixed(6),JSON.stringify(O.state()).slice(0,400));
S.ship=900;const seen2=[];for(let i=0;i<600;i++){O.step(.5);if(seen2[seen2.length-1]!==S.ph+(S.boost?'+B':''))seen2.push(S.ph+(S.boost?'+B':''))}console.log(seen2.join('>'),JSON.stringify(O.state()).slice(0,300));
