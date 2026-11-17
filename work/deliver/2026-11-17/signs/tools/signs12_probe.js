// signs12_probe.js <game.html> <out.json> <ids.json> — סט 12 (17.11): לכל נקודת F — מה הכותרת, הסוג והלוגו של מסך המקום.
// הנקודות — כמו rule30_gate (העתק של האיסוף), ועוד כל נקודה של navPoiRegistry; "לוחצים F" (interactNearbyPoi) ובודקים את PLACE.meta.
// נכשל אם במסך כלשהו "תעשייה קלה" בכותרת של מקום שאינו C4, או "עסקי C4" / "עסק" כשם. דפדפן אחד, דרך bslot.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, idsf] = process.argv.slice(2); const IDS = idsf ? JSON.parse(fs.readFileSync(idsf, 'utf8')) : [];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(4000);
  const res = await p.evaluate(ids => window.__TC_DEV.ev(`(()=>{const IDS=${JSON.stringify(ids)};
   const pts=[],add=(group,id,label,x,y)=>{if(isFinite(x)&&isFinite(y))pts.push({group,id,label:label||id,x:Math.round(x),y:Math.round(y)})},T=f=>{try{f()}catch(e){}};
   T(()=>{for(const q of Object.values(A6_POIS))add('A6',q.id,q.label,q.x,q.y);add('A6',G8_FERRY_POI.id,G8_FERRY_POI.label,G8_FERRY_POI.x,G8_FERRY_POI.y)});
   T(()=>{for(const q of LOT_POIS)add('חניון',q.id,q.label,q.x,q.y)});
   T(()=>{for(const q of Object.values(C5_POIS))if(q.r)add('C5',q.id,q.label,q.x,q.y)});
   T(()=>{for(const q of Object.values(A4_POIS))if(q.r)add('A4',q.id,q.label,q.x,q.y)});
   T(()=>{for(const o of B5_BUILDINGS){const q=B5_POIS[o.id];if(q)add('B5',o.id,q.label,q.x,q.y)}});
   T(()=>{for(const q of Object.values(S14_INTERACTIONS))add('S14',q.id,q.label,q.x,q.y)});T(()=>{for(const q of B2_FISH_SPOTS)add('דיג',q.id,q.label||q.name,q.x,q.y)});T(()=>{for(const q of B6_FISH_SPOTS)add('דיג',q.id,q.label||q.name,q.x,q.y)});
   T(()=>{for(const q of Object.values(B2_INTERACTIONS))add('B2',q.id,q.label,q.x,q.y)});
   T(()=>{for(const q of Object.values(S12_POIS))add('S12',q.id,q.label,q.x,q.y)});   /* S12 — הצפון */
   T(()=>{const q=playerHomeServicePoint();add('C3','PLAYER-HOME','בית השחקן',q.x,q.y)});
   T(()=>{for(const o of [...C2_BUILDINGS,...B4_BUILDINGS]){if(!RETAIL_POIS[o.id])continue;const q=retailBuildingPoint(o);if(q)add(o.id.slice(0,2),o.id,o.label,q.x,q.y)}});
   T(()=>{for(const q of Object.values(C4_INTERACTIONS))add('C4',q.id,q.label,q.x,q.y)});
   for(const [g,n] of [['E3','E3_INTERACTIONS'],['E4','E4_INTERACTIONS'],['E5','E5_INTERACTIONS'],['דירות','APT_INTERACTIONS'],['נמל','PORT_INTERACTIONS'],['D5','D5_INTERACTIONS'],['D2','D2_INTERACTIONS'],['D4','D4_INTERACTIONS']])
    T(()=>{for(const q of Object.values(eval(n)))if(!q.phoneOnly)add(g,q.id,q.label,q.x,q.y)});
   T(()=>{for(const o of D3_SERVICES){const q=d3ServicePoints(o)[0];add('D3',o.id,o.label,q.x,q.y)}});
   T(()=>{for(const g of PG_GATES)if(g.intercom)add('שער הנמל',g.id,g.label,g.intercom[0],g.intercom[1])});
   T(()=>{for(const d of g77FfDoors())add('שדה התעופה','FIDS-'+d.term,'מסוף הטיסות '+d.term,d.x,d.y)});
   const vis=e=>!!e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().width>0;
   const reset=()=>{T(()=>{if(G77_FF.open)g77FfClose()});T(()=>{if(State.fishingSetup)closeFishingSetup()});T(()=>setPhoneOpen(false));State.fishingSpot=null};
   const look=r=>{const pl=window.__TC_PLACE(),ff=document.getElementById('g77Ff'),fp=document.getElementById('fishingSetupPanel');let kind,full=false,w=0,h=0,app=null,id=null;
    if(pl.open&&pl.place){kind='מסך המקום';full=pl.full&&!pl.phoneFrame;w=pl.w;h=pl.h;app=pl.place.app;id=pl.place.id}
    else if(pl.open){kind='טלפון';app=State.phoneApp}
    else if(vis(ff)){const q=ff.getBoundingClientRect();kind='מסך מלא משלו';w=Math.round(q.width);h=Math.round(q.height);full=w>=innerWidth*.98&&h>=innerHeight*.98}
    else if(State.fishingSetup&&vis(fp)){const q=fp.getBoundingClientRect();kind='חלון הדיג';w=Math.round(q.width);h=Math.round(q.height);full=w>=innerWidth*.8&&h>=innerHeight*.75}
    else{const tt=String(document.getElementById('toast')?.textContent||'').trim();kind=tt?'הודעה בלבד':r?'פעולה בלי חלון':'אין F כאן';if(tt)return{kind,full:false,w:0,h:0,app:null,place:null,head:tt.slice(0,80)}}
    return{kind,full,w,h,app,place:id,head:pl.head||''}};
   T(()=>{if(typeof exitVehicle==='function'&&PlayerProfile.mode!=='walk')exitVehicle()});PlayerProfile.money=Math.max(PlayerProfile.money,5000);T(()=>{PlayerProfile.licenses['LIC-11']={state:'owned',acquiredAt:'rule30_gate',source:'rule30_gate'};ensureFishingSchema().licenseState='owned'});   /* the gate's player holds the fishing licence (else the fishing spots only toast) */
   
   T(()=>{const R=navPoiRegistry(),have=new Set(pts.map(q=>q.id));for(const [id,q] of Object.entries(R))if(!have.has(id))add('nav',id,q.label,q.x,q.y)});
   T(()=>{if(typeof exitVehicle==='function'&&PlayerProfile.mode!=='walk')exitVehicle()});PlayerProfile.money=Math.max(PlayerProfile.money,5000);
   const rows=[];for(const q of pts){reset();PlayerProfile.mode='walk';State.mapQa=false;PlayerPed.x=q.x;PlayerPed.y=q.y;let r=false,err=null;try{r=interactNearbyPoi()}catch(e){err=String(e&&e.message||e).slice(0,120)}
    const m=PLACE.on&&State.phoneOpen?(PLACE.meta||null):null;const hd=document.getElementById('placeHead'),h1=hd&&hd.querySelector('h1'),sm=hd&&hd.querySelector('.plNm small');
    rows.push({group:q.group,id:q.id,label:q.label,opened:m?PLACE.on.id:null,app:m?PLACE.on.app:null,name:m?m.name:null,kind:m?m.kind:null,tcb:m?(m.tcb||null):null,brand:m?(m.brand||null):null,
     h1:h1?h1.textContent:null,small:sm?sm.textContent:null,title:String(document.getElementById('phoneTitle')?.textContent||''),err})}
   reset();
   const op=rows.filter(q=>q.opened),gen=q=>/תעשייה קלה|עסקי C4/.test(q.h1||'')&&!/^C4-/.test(q.opened||''),bad=op.filter(gen);
   const genKind=op.filter(q=>q.small==='עסק');const mono=op.filter(q=>!q.tcb);
   const want=IDS.filter(id=>!op.some(q=>q.opened===id));
   return JSON.stringify({points:rows.length,opened:op.length,generic:bad.length,genericIds:bad.map(q=>q.opened+' '+q.h1),kindBusiness:genKind.length,withLogo:op.length-mono.length,monogram:mono.length,
    s12:typeof __TC_SIGNS12!=='undefined'?__TC_SIGNS12.stats():null,idsNotOpened:want,rows})})()`), IDS);
  const R = JSON.parse(res); R.pageErrors = errs; R.build = path.basename(file);
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(`signs12_probe ${R.generic ? 'נכשל' : 'עובר'} · ${R.points} נקודות · ${R.opened} מסכים · כותרת כללית ${R.generic} · סוג "עסק" ${R.kindBusiness} · עם לוגו ${R.withLogo} · סימן ${R.monogram} · שגיאות דף ${errs.length}`);
  await b.close(); process.exit(R.generic || errs.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2) });
