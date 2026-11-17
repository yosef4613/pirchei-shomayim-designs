// h8_shots.js — בית השחקן (house8, 17.11): צילום אמיתי של המגרש C3-PH בכל אחת מ-8 הרמות, ונתוני הרמות (C3LV / C3PH_B) לציור.
// node h8_shots.js <game.html> <out_dir> [zoom=1.0] [levels=1-8]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, z0, lv0] = process.argv.slice(2); const Z = +z0 || 1.0; fs.mkdirSync(out, { recursive: true });
  const LV = (lv0 || '1-8').split('-').map(Number); const levels = []; for (let n = LV[0]; n <= (LV[1] || LV[0]); n++) levels.push(n);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 2100, height: 1100 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const R = { zoom: Z, levels: {} };
  R.data = JSON.parse(await ev(`(()=>{const lot=C3_LOTS.find(l=>l.kind==='player');return {lot:lot&&{x:lot.x,y:lot.y,w:lot.w,h:lot.h,parts:lot.parts,label:lot.label},
    base:{gate:C3D.gate,ph:C3D.ph,start:C3D.start,turn:C3D.turn},prices:HOME_UPGRADE_PRICES,cap:HOME_GARAGE_CAPACITY,max:HOME_UPGRADE_ACTIVE_MAX,he:HOME_LV,
    lv:C3LV.map((L,i)=>({n:L.n,he:L.he,garage:L.garage,price:L.price,pool:L.pool,pad:L.pad,flag:L.flag,drive:L.drive,stalls:L.stalls,props:L.props,trees:L.trees.length,lamps:L.lamps.length,flowers:L.flowers.length,
      b:C3PH_B[i].map(o=>({id:o.id,label:o.label,type:L.buildings.find(q=>q.id===o.id).type,x:Math.round(o.x),y:Math.round(o.y),w:Math.round(o.w),h:Math.round(o.h),ent:L.buildings.find(q=>q.id===o.id).ent}))}))}})()`));
  // the frame: everything any level puts on the lot
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; const add = (a, b2, c, d) => { x0 = Math.min(x0, a); y0 = Math.min(y0, b2); x1 = Math.max(x1, c); y1 = Math.max(y1, d) };
  for (const L of R.data.lv) { for (const o of L.b) add(o.x, o.y - 40, o.x + o.w, o.y + o.h); for (const s of L.stalls) add(s.x, s.y, s.x + s.w, s.y + s.h); if (L.pad) add(L.pad.c[0] - L.pad.safety, L.pad.c[1] - L.pad.safety, L.pad.c[0] + L.pad.safety, L.pad.c[1] + L.pad.safety); if (L.pool) add(...L.pool) }
  x0 -= 30; y0 -= 30; x1 += 30; y1 += 30; R.frame = [x0, y0, x1, y1]; const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  R.night0 = await ev('+window.__TC_NIGHT||0'); R.lv0 = await ev('c3Lv()');
  for (const n of levels) {
    await ev(`PlayerProfile.home.homeLevel=${n};PlayerProfile.home.garageCapacity=HOME_GARAGE_CAPACITY[${n}];PlayerProfile.mode='walk';const L=C3LV[${n}-1],b=L.buildings.find(q=>/-H$/.test(q.id))||L.buildings[0];PlayerPed.x=b.ent[0];PlayerPed.y=b.ent[1]+14;Camera.x=${cx};Camera.y=${cy};Camera.zoom=${Z};1`);
    await p.waitForTimeout(3500);
    await ev(`Camera.x=${cx};Camera.y=${cy};Camera.zoom=${Z};1`); await p.waitForTimeout(900);
    const box = JSON.parse(await p.evaluate(([cx, cy, x0, y0, x1, y1]) => { const cs = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height), c = cs[0];
      for (const el of document.body.querySelectorAll('*')) if (el !== c && !el.contains(c)) el.style.visibility = 'hidden';
      const r = c.getBoundingClientRect(), z = +window.__TC_DEV.ev('Camera.zoom'), cxx = +window.__TC_DEV.ev('Camera.x'), cyy = +window.__TC_DEV.ev('Camera.y'); const W = r.width, H = r.height;
      const sx = q => r.left + W / 2 + (q - cxx) * z, sy = q => r.top + H / 2 + (q - cyy) * z;
      const X0 = Math.max(r.left, sx(x0)), Y0 = Math.max(r.top, sy(y0)), X1 = Math.min(r.left + W, sx(x1)), Y1 = Math.min(r.top + H, sy(y1));
      return JSON.stringify({ z, cam: [cxx, cyy], W, H, clip: { x: X0, y: Y0, width: X1 - X0, height: Y1 - Y0 } }) }, [cx, cy, x0, y0, x1, y1]));
    const f = path.join(out, 'L' + n + '.png'); await p.screenshot({ path: f, clip: box.clip });
    R.levels[n] = { box, lv: await ev('c3Lv()'), night: await ev('+window.__TC_NIGHT||0'), solid: await ev(`C3PH_B[${n}-1].map(o=>o.id).join(',')`) };
    await p.evaluate(() => { for (const el of document.body.querySelectorAll('*')) el.style.visibility = '' });
  }
  R.errs = errs; fs.writeFileSync(path.join(out, 'h8_shots.json'), JSON.stringify(R, null, 1));
  console.log(JSON.stringify({ frame: R.frame, night0: R.night0, lv: Object.fromEntries(Object.entries(R.levels).map(([k, v]) => [k, [v.lv, v.night, v.box.cam, v.box.clip]])), errs }).slice(0, 2500));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
