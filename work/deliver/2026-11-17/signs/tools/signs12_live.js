// signs12_live.js <game.html> <out.json> — סט 12 שלב 4 (17.11): "מידע חי" ב-23 המקומות של signs (F_owners_128.tsv).
// לכל מקום: השחקן בנקודה, "לוחץ F" (interactNearbyPoi), ובודק: מסך המקום נפתח, יש כרטיס "עכשיו כאן" עם שורות, ויש כפתור בגוף המסך; ואז "רענון".
// ועוד: לילה (gameClockSet 23:00) — במקום אחד, שהשורות מתחלפות (השעה). דפדפן אחד, דרך bslot.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(3000);
  const R = JSON.parse(await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const T=f=>{try{return f()}catch(e){return null}};T(()=>{if(PlayerProfile.mode!=='walk')exitVehicle()});
    const ids=Object.keys(__TC_SIGNS12.live||{}),R=navPoiRegistry(),rows=[];
    for(const id of ids){T(()=>setPhoneOpen(false));const q=R[id];if(!q){rows.push({id,err:'no-nav'});continue}PlayerProfile.mode='walk';PlayerPed.x=q.x;PlayerPed.y=q.y;let err=null;try{interactNearbyPoi()}catch(e){err=String(e&&e.message||e).slice(0,120)}
     const body=document.getElementById('phoneBody'),L=body&&body.querySelector('.tcs12Live'),kv=L?[...L.querySelectorAll('div,li,tr')].map(e=>e.textContent.trim()).filter(Boolean):[];
     const btn=body?body.querySelectorAll('button').length:0,rb=L&&L.querySelector('button[data-tcs12-live]');let again=false;if(rb){rb.click();again=!!document.querySelector('#phoneBody .tcs12Live')}
     rows.push({id,opened:!!(PLACE.on&&State.phoneOpen&&PLACE.on.id===id),live:!!L,rows:__TC_SIGNS12.liveRows(id),buttons:btn,refresh:again,text:L?L.textContent.replace(/\\s+/g,' ').slice(0,220):null,err})}
    T(()=>setPhoneOpen(false));T(()=>gameClockSet(23,0));
    return JSON.stringify({ids:ids.length,rows,stats:__TC_SIGNS12.stats()})})()`)));
  await p.waitForTimeout(2500); R.night = JSON.parse(await p.evaluate(() => window.__TC_DEV.ev(`JSON.stringify(__TC_SIGNS12.liveRows('C1-H1'))`)));
  R.pageErrors = errs; R.build = path.basename(file);
  const bad = R.rows.filter(r => !r.opened || !r.live || !(r.buttons > 0) || !r.refresh || r.err);
  const lit = (R.night || []).some(r => r[0] === 'האור בבית' && r[1] === 'דולק'); R.nightLit = lit;
  R.ok = R.ids === 23 && !bad.length && !errs.length && lit; R.bad = bad.map(r => r.id);
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(`signs12_live ${R.ok ? 'עובר' : 'נכשל'} · ${R.ids} מקומות · עם "עכשיו כאן" ${R.rows.filter(r => r.live).length} · עם כפתור ${R.rows.filter(r => r.buttons > 0).length} · רענון ${R.rows.filter(r => r.refresh).length} · בלילה האור ${lit ? 'דולק' : 'לא נדלק'} · עם אנשים ${R.rows.filter(r => (r.rows||[]).some(q => q[0]==='בסביבה' && !/^0 אנשים/.test(q[1]))).length}${bad.length ? ' · נכשלו: ' + R.bad.join(', ') : ''} · שגיאות דף ${errs.length}`);
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2) });
