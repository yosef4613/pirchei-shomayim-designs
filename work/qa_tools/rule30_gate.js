// rule30_gate.js <game.html> <out.json> [out.md] — כלל 30 (D‑494), בדיקה חוסמת: עוברים על כל נקודות ה-F בעיר, "לוחצים F" (interactNearbyPoi — מה שמקש F קורא),
// 10.11 (סוכן המיזוג, לפי המתאם): גם 43 המקומות של S12 (S12_POIS — כל אחד חייב לפתוח את מסך המקום, מהעותק deliver/2026-11-10/s12/tools/rule30_s12.js) וגם המקומות של S14 (S14_INTERACTIONS, מהעותק של S14). בבנייה שאין בה אותם — T() מדלג. הגרסה הקודמת: _to_delete/rule30_gate_1110_before_s12_s14.js
// ונכשלים אם נפתח הטלפון, או חלון שאינו מסך מלא. בדוח: כל הנקודות ומה נפתח בכל אחת. בונה השלבים 7, 5.11.
// מסך מלא: מסך המקום (p651, ‏__TC_PLACE — רוחב וגובה ≥ 98%, בלי מסגרת הטלפון), מסוף הטיסות (#g77Ff ≥ 98%), חלון הדיג של בונה 7 (≥ 80% × 75%).
// יציאה 1 = נכשל. רץ דרך nolock.sh, דפדפן אחד.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, md] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(4000);
  const res = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{
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
   const rows=[];for(const q of pts){reset();PlayerProfile.mode='walk';State.mapQa=false;PlayerPed.x=q.x;PlayerPed.y=q.y;let r=false,err=null;T(()=>{document.getElementById('toast').textContent=''});try{r=interactNearbyPoi()}catch(e){err=String(e&&e.message||e).slice(0,120)}
    const L=look(r);rows.push({...q,...L,err,ret:!!r})}
   // the taxi: a taxi waits by the player (as after a call), F
   T(()=>{reset();PlayerProfile.mode='walk';const car=TRAFFIC_CARS.find(c=>taxiAvailable(c));if(!car){rows.push({group:'מונית',id:'TAXI',label:'מונית שמחכה',kind:'לא נבדק — אין מונית פנויה',full:false});return}
    PlayerPed.x=car.x;PlayerPed.y=car.y+14;beginTaxiCall(car,'hail');if(State.taxiRide)State.taxiRide.phase='waiting';PlayerPed.x=car.x;PlayerPed.y=car.y+14;let r=false;try{r=interactNearbyPoi()}catch(e){}
    rows.push({group:'מונית',id:'TAXI',label:'מונית שמחכה ליד השחקן',x:Math.round(car.x),y:Math.round(car.y),...look(r),ret:!!r});reset();State.taxiRide=null});
   reset();
   const isWin=k=>k==='מסך המקום'||k==='טלפון'||k==='מסך מלא משלו'||k==='חלון הדיג',bad=rows.filter(q=>q.kind==='טלפון'||(isWin(q.kind)&&!q.full)||q.err||(q.group==='S12'&&q.kind!=='מסך המקום'));
   return JSON.stringify({s12:rows.filter(q=>q.group==='S12').length,s12full:rows.filter(q=>q.group==='S12'&&q.kind==='מסך המקום'&&q.full).length,s14:rows.filter(q=>q.group==='S14').length,points:rows.length,opened:rows.filter(q=>isWin(q.kind)).length,fail:bad.length,bad:bad.map(q=>q.id+' '+q.kind),rows})})()`));
  const R = JSON.parse(res); R.pageErrors = errs; R.build = path.basename(file);
  R.missionActions = [
    ['ew2MissionAction', 'צעד במשימות ההדרכה של שדה התעופה (גרירה, ניתוק, חיבור) — רק במשימה פעילה; הודעה קצרה על המסך, בלי חלון'],
    ['forkliftMissionAction', 'משמרת המלגזה ב-D5 — הרמה והורדה של משטח; הודעה קצרה, בלי חלון'],
    ['actInteract', 'משמרת סריקה — סריקת פריט ליד השחקן; הודעה קצרה, בלי חלון'],
    ['hailNearestTaxi', 'עצירת מונית חולפת — המונית עוצרת ליד השחקן; F ליד המונית שמחכה — מסך המונית (מסך המקום)'],
    ['startFishingFromSetup', 'הטלת החכה, כשחלון הדיג כבר פתוח (בונה 7)']];
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  if (md) { const by = {}; for (const q of R.rows) (by[q.kind] = by[q.kind] || []).push(q);
    let t = `# כלל 30 — בדיקת נקודות ה-F · ${R.build}\n\n**${R.fail ? 'נכשל' : 'עובר'}** · ${R.points} נקודות · ${R.opened} נפתחו בחלון · ${R.fail} נכשלו\n\n`;
    for (const k of Object.keys(by)) { t += `## ${k} (${by[k].length})\n`; for (const q of by[k]) t += `- ${q.group} · ${q.label} (${q.id})${q.w ? ` · ${q.w}×${q.h}` : ''}${q.kind === 'מסך המקום' || q.kind === 'הודעה בלבד' ? ' · ' + (q.head || '').slice(0, 60) : ''}${(q.kind !== 'אין F כאן' && q.kind !== 'פעולה בלי חלון' && q.kind !== 'הודעה בלבד' && !q.full) ? ' · **לא מסך מלא**' : ''}\n`; t += '\n' }
    t += '## פעולות משימה (לא מקום)\n' + R.missionActions.map(([f, d]) => `- ${f}: ${d}`).join('\n') + '\n'; fs.writeFileSync(md, t) }
  console.log(`rule30_gate ${R.fail ? 'נכשל' : 'עובר'} · ${R.points} נקודות · ${R.opened} חלונות · ${R.fail} נכשלו ${R.bad.slice(0, 8).join(' | ')} · שגיאות דף ${errs.length}`);
  await b.close(); process.exit(R.fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2) });
