// signs12_kiosk.js <game.html> <out.json> [shotsdir] — סט 12 שלב 3 (17.11): הקיוסקים B2-KIOSK / E3-KIOSK — הלוגו המאושר על השלט, בסמן של המפה ובכרטיס.
// השחקן ליד כל קיוסק (יום), כמה פריימים, ואז: מה g7Logo מצייר (tcbrKeyOfBrand), כמה פעמים צויר ה-tile של המותג (TCBR.drawn), השלט של g7BrandSign, הכרטיס (g7BrandBanner) ומסך ה-F.
// צילומים — לבדיקה פנימית בלבד. דפדפן אחד, דרך bslot.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots] = process.argv.slice(2); if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(3000);
  const R = { build: path.basename(file), kiosks: [], rows: [] };
  R.kiosks = JSON.parse(await p.evaluate(() => window.__TC_DEV.ev(`JSON.stringify(__TC_SIGNS12.kiosks?__TC_SIGNS12.kiosks():null)`)));
  for (const [id, key] of [['B2-KIOSK', 'lakec'], ['E3-KIOSK', 'cafe']]) {
    const before = JSON.parse(await p.evaluate(k => window.__TC_DEV.ev(`JSON.stringify(TCBR.drawn[${JSON.stringify(k)}]||{})`), key));
    const lab = await p.evaluate(id => window.__TC_DEV.ev(`(()=>{const q=g7ShopDoor(${JSON.stringify(id)})||navPoiRegistry()[${JSON.stringify(id)}];if(!q)return 'none';try{setPhoneOpen(false)}catch(e){}PlayerProfile.mode='walk';PlayerPed.x=q.x;PlayerPed.y=q.y+40;return q.label||'דלת'})()`), id);
    await p.waitForTimeout(3000); if (shots) await p.screenshot({ path: path.join(shots, id + '_day.png') });
    const r = JSON.parse(await p.evaluate(([id, k]) => window.__TC_DEV.ev(`(()=>{const id=${JSON.stringify(id)},k=${JSON.stringify(k)},s=G7_SHOP_BRAND[id],g=s&&G7_BRANDS[s.b];
      let sign=null;for(const v of G7_SIGN.map.values())if(v&&v.id===id)sign={x:Math.round(v.x),y:Math.round(v.y),t:v.lay&&v.lay.t,w:v.lay&&Math.round(v.lay.w)};
      const ban=typeof g7BrandBanner==='function'?g7BrandBanner(id):'';const m=/data-tcp="([^"]*)"/.exec(ban);
      let f=null;try{const q=g7ShopDoor(id)||navPoiRegistry()[id];PlayerPed.x=q.x;PlayerPed.y=q.y;interactNearbyPoi();const hd=document.getElementById('placeHead');
       f={open:!!(PLACE.on&&State.phoneOpen),id:PLACE.on&&PLACE.on.id,tcb:PLACE.meta&&PLACE.meta.tcb||null,h1:hd&&hd.querySelector('h1')?.textContent||null,small:hd&&hd.querySelector('.plNm small')?.textContent||null,
        banner:!!document.querySelector('#phoneBody .g7brand'),bannerTok:document.querySelector('#phoneBody .g7brand canvas')?.dataset.tcp||null}}catch(e){f={err:String(e&&e.message||e).slice(0,120)}}
      return JSON.stringify({id,g7:s&&s.b,tcb:g&&g.tcb||null,key:g&&tcbrKeyOfBrand(g),sign,bannerTok:m&&m[1],drawn:TCBR.drawn[k]||{},f})})()`), [id, key]));
    r.label = lab; r.before = before; if (shots) await p.screenshot({ path: path.join(shots, id + '_F.png') });
    try { await p.evaluate(() => window.__TC_DEV.ev(`setPhoneOpen(false)`)) } catch (e) { }
    R.rows.push(r);
  }
  R.stats = JSON.parse(await p.evaluate(() => window.__TC_DEV.ev(`JSON.stringify(__TC_SIGNS12.stats())`))); R.pageErrors = errs;
  const ok = R.rows.length === 2 && R.rows.every(r => r.key === (r.id === 'B2-KIOSK' ? 'lakec' : 'cafe') && r.f && (r.f.tcb === r.key || /^tcp:(g7\|(lakek|stationk)|tcb\|)/.test(r.f.bannerTok || ''))) && !errs.length;
  R.ok = ok; fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(`signs12_kiosk ${ok ? 'עובר' : 'נכשל'} · ` + R.rows.map(r => `${r.id}: g7Logo→${r.key} · שלט ${r.sign ? '"' + r.sign.t + '"' : 'לא נמצא'} · tile ${(r.drawn.tile || 0) - (r.before.tile || 0)} · sign ${(r.drawn.sign || 0) - (r.before.sign || 0)} · F ${r.f && r.f.h1} / ${r.f && r.f.small} / ${r.f && r.f.tcb}`).join(' | ') + ` · שגיאות דף ${errs.length}`);
  await b.close(); process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2) });
