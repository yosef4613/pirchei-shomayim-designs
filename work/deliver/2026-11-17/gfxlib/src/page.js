/* page.js — דף ההשוואה: הישן (הקוד של המשחק היום, מילה במילה) מול החדש (G2) ומול הספרייה (Zdog), באותו גודל ובאותה זווית. */
(function () {
'use strict';
const $ = s => document.querySelector(s), DPR = Math.min(2, window.devicePixelRatio || 1);
const ERR = []; window.addEventListener('error', e => ERR.push(String(e.message)));
window.TurboCity = window.TurboCity || { get: () => null };
const OK = { c34: false, p34: false, a34: false };
try { OK.c34 = c34LibInit() } catch (e) { ERR.push('C34 ' + e.message) }
try { OK.p34 = p34LibInit() } catch (e) { ERR.push('P34 ' + e.message) }
try { OK.a34 = a34LibInit() } catch (e) { ERR.push('A34 ' + e.message) }
G2.domCanvas = false;
const ST = { zoom: 2, dirs: 16, anim: true, wide: false, car: 'VH-SD-02', col: '#2f6fd0' };
const CAR_COLS = [['כחול', '#2f6fd0'], ['אדום', '#d23a3a'], ['לבן', '#f4f6f8'], ['שחור', '#22262b'], ['כסף', '#c3c9cf']];
function cvs(el, w, h) { el.width = Math.round(w * DPR); el.height = Math.round(h * DPR); el.style.width = w + 'px'; el.style.height = h + 'px'; const g = el.getContext('2d'); g.setTransform(DPR, 0, 0, DPR, 0, 0); return g }
const pic = (g, e, x, y, res) => g.drawImage(e.cv, x - e.ox / res, y - e.oy / res, e.cv.width / res, e.cv.height / res);
function ground(g, w, h) { g.fillStyle = getComputedStyle(document.body).getPropertyValue('--ground') || '#9aa58c'; g.fillRect(0, 0, w, h) }
function label(g, t, x, y) { g.save(); g.font = '600 12px system-ui, sans-serif'; g.fillStyle = 'rgba(20,24,30,.75)'; g.textAlign = 'center'; g.fillText(t, x, y); g.restore() }
// ---------- the old painters, as the game calls them ----------
function oldCar(g, x, y, h, Z) { const r = Z * DPR, s = C34.sprite(ST.car, ST.col, h, r, ST.dirs); g.save(); g.translate(x, y); g.scale(Z, Z); g.drawImage(s.cv, -s.ox / r, -s.oy / r, s.cv.width / r, s.cv.height / r);
  try { C34.wheels(g, ST.car, 0, 0, s.k, ST.dirs, 0, -1, 1) } catch (e) { } g.restore() }
const A34_PXM = 7.47;
function a34Rot(p, phi) { const c = Math.cos(phi), sn = Math.sin(phi), R = q => [q[0] * c - q[1] * sn, q[0] * sn + q[1] * c, q[2]];   // the game's a34Rot (068_core.js), copied
  const rf = f => { const g = Object.assign({}, f); if (f.P) g.P = f.P.map(R); if (f.n) g.n = R(f.n); if (f.g) g.g = f.g.map(R); if (f.at) g.at = R(f.at); if (f.gax) g.gax = f.gax.map(R); if (f.g4) g.g4 = f.g4.map(R); return g };
  const q = Object.assign({}, p, { faces: p.faces.map(rf), decor: (p.decor || []).filter(d => !d.text || Math.abs(sn) < .01).map(rf) });
  if (p.tyres) q.tyres = p.tyres.map(t => Object.assign({}, t, { x: t.x * c - t.y * sn, y: t.x * sn + t.y * c })); if (p.legs) q.legs = p.legs.map(l => Object.assign({}, l, { x: l.x * c - l.y * sn, y: l.x * sn + l.y * c }));
  return A34.bounds(q) }
const OAC = new Map(); let OAM = null;
// the game's a34SetPrep + a34Step (068_core.js) in one synchronous pass: the shadow, then the pieces in the game's order
function oldPlane(id, heading, S) { const key = id + '|' + heading.toFixed(4) + '|' + S; let e = OAC.get(key); if (e) return e; const t0 = performance.now();
  if (!OAM) OAM = A34.build(id, null, { lod: 1, noBand: 1 });
  const phi = heading - Math.PI / 2, hdeg = ((-phi * 180 / Math.PI) % 360 + 360) % 360, hb = Math.round(hdeg / 22.5) % 16, mb = A34.bandFor(OAM, hb * 22.5), K = A34.K, P = [];
  let sb = [1e9, 1e9, -1e9, -1e9]; const sx = A34.SHX, sy = A34.SHY;
  for (const p0 of mb.pieces) { const p = a34Rot(p0, phi), b = A34.bboxPiece(p, { X: 0, Y: 0, s: S }); P.push({ p, b, k: (p.yMax + p.zMin / K) * A34_PXM, kind: p.kind, side: p.side || 0 });
    for (const f of p.faces) for (const q of f.P) { const X = (q[0] + q[2] * sx) * S, Y = (q[1] + q[2] * sy) * S; sb = [Math.min(sb[0], X), Math.min(sb[1], Y), Math.max(sb[2], X), Math.max(sb[3], Y)] } }
  const bd = P.find(q => q.kind === 'body'), kB = bd ? bd.k : 0, south = q => q.side * Math.sin(phi) > .3;
  for (const q of P) { if (q.kind === 'gear') q.k = Math.min(q.k, kB - 2); else if (q.kind !== 'body') q.k = south(q) ? Math.max(q.k, kB + 1) : Math.min(q.k, kB - 1) }
  for (const q of P) if (q.kind === 'engine') { const w = P.find(r => r.kind === 'wing' && r.side === q.side); if (w) q.k = Math.min(q.k, w.k - .5) }
  let x0 = sb[0], y0 = sb[1], x1 = sb[2], y1 = sb[3]; for (const q of P) { x0 = Math.min(x0, q.b[0]); y0 = Math.min(y0, q.b[1]); x1 = Math.max(x1, q.b[2]); y1 = Math.max(y1, q.b[3]) }
  x0 = Math.floor(x0) - 3; y0 = Math.floor(y0) - 3; const W = Math.ceil(x1 - x0) + 6, H = Math.ceil(y1 - y0) + 6, cv = document.createElement('canvas'); cv.width = W; cv.height = H; const c = cv.getContext('2d');
  const sh = document.createElement('canvas'); sh.width = W; sh.height = H; const hc = sh.getContext('2d'); hc.fillStyle = '#0c1016'; for (const q of P) A34.shadowPiece(hc, q.p, { X: -x0, Y: -y0, s: S });
  c.globalAlpha = .24; c.drawImage(sh, 0, 0); c.globalAlpha = 1; const M = { X: -x0, Y: -y0, s: S }, o = { zoom: 1 };
  for (const q of P.slice().sort((a, b) => a.k - b.k)) { if (q.p.tyres) A34.drawPiece(c, { kind: q.kind, tyres: q.p.tyres, legs: q.p.legs, faces: [] }, M, .6, o);
    A34.drawFaces(c, q.p.faces, M, .6, o); const d = q.p.decor || []; A34.drawDecor(c, d.filter(x => !x.late), M, o); A34.drawDecor(c, d.filter(x => x.late), M, o) }
  e = { cv, ox: -x0, oy: -y0, ms: performance.now() - t0 }; OAC.set(key, e); return e }
const OLD_LOOKS = [
  { h: 1.78, skin: '#e0b089', hair: { t: 'short', c: '#2b2018' }, top: { t: 'shirt', c: '#f2f4f6', tie: '#2a4f8a', long: 1 }, legs: { t: 'suit', c: '#2b3240' }, shoes: { t: 'leather', c: '#16181b' } },
  { h: 1.66, skin: '#c99068', hair: { t: 'short', c: '#1c1612' }, hat: { t: 'cap', c: '#c8372d' }, top: { t: 'tee', c: '#d84a3a' }, legs: { t: 'jeans', c: '#3b5a8a' }, shoes: { t: 'sneaker', c: '#eceff2' } },
  { h: 1.8, w: 1.08, skin: '#b47c56', hair: { t: 'short', c: '#2a2420' }, hat: { t: 'helmet', c: '#f3c623' }, top: { t: 'tee', c: '#4a5058', long: 1 }, vest: '#ff7a1a', legs: { t: 'trousers', c: '#5a5f66' }, shoes: { t: 'leather', c: '#3a2a1e' } },
  { h: 1.72, skin: '#e8bf9c', hair: { t: 'short', c: '#c9c9c9' }, beard: { c: '#cfcfcf' }, glasses: '#1a1a1a', top: { t: 'coat', c: '#b59a74', long: 1 }, legs: { t: 'trousers', c: '#6a6458' }, shoes: { t: 'leather', c: '#4a3020' } },
  { h: 1.74, skin: '#d9a77f', hair: { t: 'short', c: '#3a2a1c' }, top: { t: 'tee', c: '#2f5fa8', long: 1 }, legs: { t: 'trousers', c: '#20242a' }, shoes: { t: 'sneaker', c: '#2a2d31' } },
  { h: 1.8, skin: '#8a5a3c', hair: { t: 'short', c: '#141010' }, top: { t: 'tee', c: '#2fae62' }, legs: { t: 'shorts', c: '#1f2328' }, shoes: { t: 'sneaker', c: '#f2f4f6' } }];
// ---------- the scales: the same world px for both (the old car's own length; the field's 7.47 px/m; the people's 11.25 px/m) ----------
const carS = () => C34.len(ST.car) / G2.car.len(ST.car), PED_S = 10 * 1.125;
// ---------- the sections ----------
function drawCars() { const Z = ST.zoom, N = ST.dirs, cw = 64 * Z, w = Math.min(document.body.clientWidth - 40, cw * 8 + 120), per = Math.max(1, Math.floor((w - 110) / cw)), rows = Math.ceil(N / per);
  const rowH = 54 * Z, H = (rowH * rows) * 3 + 30, g = cvs($('#cvCars'), w, H); ground(g, w, H); const s = carS(), res = Z * DPR, t0 = performance.now();
  let y = 20; const tm = { old: 0, neu: 0, zd: 0 };
  for (const [nm, f] of [['ישן · C34', 'old'], ['חדש · G2', 'neu'], ['ספרייה · Zdog', 'zd']]) { label(g, nm, 50, y + rowH * .5);
    for (let i = 0; i < N; i++) { const h = i / N * Math.PI * 2, x = 110 + (i % per) * cw + cw / 2, yy = y + Math.floor(i / per) * rowH + rowH * .55, t = performance.now();
      if (f === 'old') oldCar(g, x, yy, h, Z);
      else if (f === 'neu') { const e = G2.car.sprite(ST.car, ST.col, h, s * Z, DPR, N, ST.wide ? 1.25 : 1); pic(g, e, x, yy, DPR) }
      else if (window.ZD && window.Zdog) { const k = 'zdc|' + i + '|' + N + '|' + Z + '|' + ST.col; let e = ZDC.get(k); if (!e) { e = ZD.car(ST.col, h, s * Z, DPR); ZDC.set(k, e) } pic(g, e, x, yy, DPR) }
      tm[f] += performance.now() - t }
    y += rowH * rows }
  }
const ZDC = new Map();
// the big pair: the same direction, side by side, turning (or fixed)
let spin = 0.39;
function drawPair() { const Z = Math.max(4, ST.zoom * 2.5), w = Math.min(document.body.clientWidth - 40, 980), H = 64 * Z * .95, g = cvs($('#cvPair'), w, H); ground(g, w, H);
  const N = ST.dirs, k = Math.round(spin / (Math.PI * 2) * N), h = k / N * Math.PI * 2;
  oldCar(g, w * .27, H * .5, h, Z); const e = G2.car.sprite(ST.car, ST.col, h, carS() * Z, DPR, N, ST.wide ? 1.25 : 1); pic(g, e, w * .73, H * .5, DPR);
  label(g, 'ישן', w * .27, 16); label(g, 'חדש', w * .73, 16); label(g, 'כיוון ' + ((k % N + N) % N + 1) + ' מתוך ' + N, w * .5, H - 8) }
function drawPlanes() { const w = Math.min(document.body.clientWidth - 40, 1000), ZP = Math.max(.4, Math.min(ST.zoom, (w - 80) / 3 / (1.3 * 38 * A34_PXM))), S = A34_PXM * ZP;
  const cw = (w - 80) / 3, bandH = 38 * S * 1.35 + 20, H = bandH * 2 + 20, g = cvs($('#cvPlanes'), w, H); ground(g, w, H); let tO = 0, tN = 0;
  // three directions (of the 16) in two bands: old (top), new (bottom) — the exact same angle; every direction — the slider below
  [2, 6, 11].forEach((k, i) => { const h = k / 16 * Math.PI * 2, x = 80 + i * cw + cw / 2; let t = performance.now(); const o = oldPlane('AC-NB-01', h, S * DPR); tO += performance.now() - t; pic(g, o, x, 10 + bandH * .56, DPR);
    t = performance.now(); const e = G2.plane.sprite('AC-NB-01', h, S, DPR, 16); tN += performance.now() - t; pic(g, e, x, 10 + bandH * 1.56, DPR) });
  label(g, 'ישן · A34', 40, 10 + bandH * .5); label(g, 'חדש · G2', 40, 10 + bandH * 1.5);
  $('#tPlanes').textContent = 'קנה מידה ×' + ZP.toFixed(2) + ' · יצירה (3 כיוונים): ישן ' + tO.toFixed(0) + ' מ"ש · חדש ' + tN.toFixed(0) + ' מ"ש' }
let planeDir = 3;
function drawPlaneBig() { const w = Math.min(document.body.clientWidth - 40, 1000), Z = Math.max(.4, Math.min(2, (w / 2 - 20) / (1.25 * 38 * A34_PXM))), S = A34_PXM * Z, H = 38 * S * 1.45 + 30, g = cvs($('#cvPlaneBig'), w, H); ground(g, w, H);
  const h = planeDir / 16 * Math.PI * 2; pic(g, oldPlane('AC-NB-01', h, S * DPR), w * .26, H * .56, DPR); pic(g, G2.plane.sprite('AC-NB-01', h, S, DPR, 16), w * .74, H * .56, DPR);
  label(g, 'ישן', w * .26, 16); label(g, 'חדש', w * .74, 16); label(g, 'כיוון ' + (planeDir + 1) + ' מתוך 16', w * .5, H - 8) }
// the people: walking / running in place, every direction; the old library has 8 directions and no run
let pedT = 0;
function drawPeds() { const Z = Math.max(2, ST.zoom * 1.5), w = Math.min(document.body.clientWidth - 40, 1100), H = 3 * 34 * Z + 30, g = cvs($('#cvPeds'), w, H); ground(g, w, H);
  const act = $('#pedAct').value, look = +$('#pedLook').value, n = ST.dirs, cw = (w - 110) / n, res = Z * DPR, cyc = G2.ped.cycle(look, act === 'stand' ? 'walk' : act);
  const ph = (pedT / 1000 * (act === 'run' ? 1.45 : .95)) % 1;
  for (let i = 0; i < n; i++) { const h = i / n * Math.PI * 2, x = 110 + i * cw + cw / 2;
    g.save(); g.translate(x, 20 + 34 * Z * .85); g.scale(Z, Z); try { P34.draw(g, 0, 0, OLD_LOOKS[look], { k: act === 'run' ? 'walk' : act }, h, ph, res) } catch (e) { } g.restore();
    const e = G2.ped.sprite(look, act, h, ph, PED_S * Z, DPR, n); pic(g, e, x, 20 + 34 * Z * 1.85, DPR);
    if (window.ZD && window.Zdog) { const k = 'zdp|' + look + '|' + act + '|' + i + '|' + n + '|' + Math.floor(ph * 12) + '|' + Z; let z = ZDC.get(k); if (!z) { z = ZD.ped(G2.ped.LOOKS[look], act, h, Math.floor(ph * 12) / 12, PED_S * Z, DPR); ZDC.set(k, z) } pic(g, z, x, 20 + 34 * Z * 2.85 - 2, DPR) } }
  label(g, 'ישן · P34', 50, 20 + 34 * Z * .6); label(g, 'חדש · G2', 50, 20 + 34 * Z * 1.6); label(g, 'Zdog', 50, 20 + 34 * Z * 2.6) }
// the lineup: every look, old and new, walking toward the camera (south-east)
function drawLineup() { const Z = Math.max(3, ST.zoom * 2), w = Math.min(document.body.clientWidth - 40, 1100), H = 2 * 30 * Z + 40, g = cvs($('#cvLineup'), w, H); ground(g, w, H);
  const cw = (w - 100) / 6, ph = (pedT / 1000 * .95) % 1, act = $('#pedAct').value, h = $('#pedDir') ? +$('#pedDir').value / 16 * Math.PI * 2 : 2.35;
  for (let L = 0; L < 6; L++) { const x = 100 + L * cw + cw / 2;
    g.save(); g.translate(x, 20 + 30 * Z * .9); g.scale(Z, Z); try { P34.draw(g, 0, 0, OLD_LOOKS[L], { k: act === 'run' ? 'walk' : act }, h, ph, Z * DPR) } catch (e) { } g.restore();
    pic(g, G2.ped.sprite(L, act, h, ph, PED_S * Z, DPR, 16), x, 20 + 30 * Z * 1.95, DPR); label(g, G2.ped.LOOKS[L].name, x, H - 6) }
  label(g, 'ישן', 40, 20 + 30 * Z * .6); label(g, 'חדש', 40, 20 + 30 * Z * 1.6) }
// a live scene: a car going round a loop and three people walking (one running) round a smaller one — the turn through all the directions,
// the steps advanced by the distance walked (the planted feet); old on the right half, new on the left (the page is right to left)
let liveT = 0;
function drawLive() { const Z = Math.max(2, ST.zoom), w = Math.min(document.body.clientWidth - 40, 1000), H = 300, g = cvs($('#cvLive'), w, H); ground(g, w, H);
  const t = liveT / 1000, half = w / 2, R = 95, r2 = 45, LZ = 2;
  for (const side of [0, 1]) { const cx = side ? half * .5 : half * 1.5, cy = H / 2; g.save(); g.strokeStyle = 'rgba(60,64,70,.55)'; g.lineWidth = 26; g.beginPath(); g.arc(cx, cy, R, 0, 7); g.stroke();
    g.strokeStyle = 'rgba(230,230,220,.6)'; g.setLineDash([8, 10]); g.lineWidth = 1.5; g.beginPath(); g.arc(cx, cy, R, 0, 7); g.stroke(); g.restore();
    const items = [];
    const a = t * .45, x = cx + Math.cos(a) * R, y = cy + Math.sin(a) * R, h = a + Math.PI / 2; items.push({ y, f: () => { if (side) { const e = G2.car.sprite(ST.car, ST.col, h, carS() * LZ, DPR, 32, ST.wide ? 1.25 : 1); pic(g, e, x, y, DPR) } else { const r = LZ * DPR, o = C34.sprite(ST.car, ST.col, h, r, 32); g.save(); g.translate(x, y); g.scale(LZ, LZ); g.drawImage(o.cv, -o.ox / r, -o.oy / r, o.cv.width / r, o.cv.height / r); try { C34.wheels(g, ST.car, 0, 0, o.k, 32, t * 40, -1, 1) } catch (e) { } g.restore() } } });
    for (let k = 0; k < 3; k++) { const run = k === 2, sp = run ? .55 : .3, b = -t * sp + k * 2.1, px = cx + Math.cos(b) * r2, py = cy + Math.sin(b) * r2, hh = b - Math.PI / 2, look = [0, 4, 5][k];
      const dist = t * sp * r2 / (PED_S * LZ), ph = ((dist / G2.ped.cycle(look, run ? 'run' : 'walk')) % 1 + 1) % 1;
      items.push({ y: py, f: () => { if (side) pic(g, G2.ped.sprite(look, run ? 'run' : 'walk', hh, ph, PED_S * LZ, DPR, 16), px, py, DPR);
        else { g.save(); g.translate(px, py); g.scale(LZ, LZ); try { P34.draw(g, 0, 0, OLD_LOOKS[look], { k: 'walk' }, hh, ph, LZ * DPR) } catch (e) { } g.restore() } } }) }
    items.sort((p, q) => p.y - q.y).forEach(i => i.f()); label(g, side ? 'חדש' : 'ישן', cx, 16) } }
// ---------- the measurements ----------
function bench() { const out = []; const T = f => { const t = performance.now(); f(); return performance.now() - t };
  G2.clear(); try { C34.clear && C34.clear() } catch (e) { } try { P34.clear() } catch (e) { } OAC.clear(); OAM = null;
  const s = carS(), MBof = a => +(a.reduce((n, e) => n + e.cv.width * e.cv.height * 4, 0) / 1048576).toFixed(2), mem = {}; let A = [], B = [];
  const cars = { old: T(() => { for (let i = 0; i < 16; i++) A.push(C34.sprite(ST.car, '#2f6fd0', i / 16 * 6.283, 2, 16)) }), neu: T(() => { for (let i = 0; i < 16; i++) B.push(G2.car.sprite(ST.car, '#2f6fd0', i / 16 * 6.283, s, 2, 16)) }) }; mem.cars = [MBof(A), MBof(B)]; A = []; B = [];
  const planes = { old: T(() => { for (let i = 0; i < 16; i++) A.push(oldPlane('AC-NB-01', i / 16 * 6.283, A34_PXM * 2)) }), neu: T(() => { for (let i = 0; i < 16; i++) B.push(G2.plane.sprite('AC-NB-01', i / 16 * 6.283, A34_PXM, 2, 16)) }) }; mem.planes = [MBof(A), MBof(B)]; A = []; B = [];
  const cg = document.createElement('canvas').getContext('2d');
  const g2b = G2.stats().MB, peds = { old: T(() => { for (let i = 0; i < 8; i++) for (let f = 0; f < 12; f++) P34.draw(cg, 50, 50, OLD_LOOKS[0], { k: 'walk' }, i / 8 * 6.283, f / 12, 2) }), neu: T(() => { for (let i = 0; i < 16; i++) for (let f = 0; f < 12; f++) G2.ped.sprite(0, 'walk', i / 16 * 6.283, f / 12, PED_S, 2, 16) }) }; mem.peds = [P34.stats().MB, +(G2.stats().MB - g2b).toFixed(2)];
  // a frame of the game's kind: 300 cached pictures drawn (the cost per frame after the pictures exist)
  const fc = document.createElement('canvas'); fc.width = 1280; fc.height = 800; const fg = fc.getContext('2d');
  const so = [], sn = []; for (let i = 0; i < 16; i++) { so.push(C34.sprite(ST.car, '#2f6fd0', i / 16 * 6.283, 2, 16)); sn.push(G2.car.sprite(ST.car, '#2f6fd0', i / 16 * 6.283, s, 2, 16)) }
  const frame = arr => T(() => { for (let r = 0; r < 20; r++) for (let i = 0; i < 300; i++) { const e = arr[i % 16]; fg.drawImage(e.cv, (i * 37) % 1200, (i * 53) % 760, e.cv.width / 2, e.cv.height / 2) } }) / 20;
  const fr = { old: frame(so), neu: frame(sn) };
  // SVG.js: the same 300 cars as SVG elements (the DOM), moved once — the cost of the retained-mode route
  let svgms = null; if (window.SVG) { const host = document.createElement('div'); host.style.cssText = 'position:absolute;left:-9999px;width:1280px;height:800px'; document.body.appendChild(host);
    const dr = SVG().addTo(host).size(1280, 800); const sv = G2.svg(G2.car.model(ST.car).polys.map(q => q.c === '__PAINT__' ? Object.assign({}, q, { c: '#2f6fd0' }) : q), .39, s); const sym = dr.symbol().svg(sv.body);
    const us = []; for (let i = 0; i < 300; i++) us.push(dr.use(sym).move((i * 37) % 1200, (i * 53) % 760));
    svgms = T(() => { for (let r = 0; r < 5; r++) { for (let i = 0; i < 300; i++) us[i].move((i * 37 + r * 3) % 1200, (i * 53) % 760); host.getBoundingClientRect() } }) / 5;
    host.remove() }
  return { cars, planes, peds, fr, svgms, mem } }
function showBench() { $('#benchOut').textContent = 'מודד…'; setTimeout(() => { const r = bench(), f = v => v == null ? '—' : v.toFixed(1);
  $('#benchOut').innerHTML = '<table><tr><th></th><th>ישן</th><th>חדש (G2)</th></tr>' +
    '<tr><td>מכונית — 16 כיוונים, יצירה (מ"ש)</td><td>' + f(r.cars.old) + '</td><td>' + f(r.cars.neu) + '</td></tr>' +
    '<tr><td>מטוס — 16 כיוונים, יצירה (מ"ש)</td><td>' + f(r.planes.old) + '</td><td>' + f(r.planes.neu) + '</td></tr>' +
    '<tr><td>הולך רגל — כל ההליכה (ישן 8×12, חדש 16×12), יצירה (מ"ש)</td><td>' + f(r.peds.old) + '</td><td>' + f(r.peds.neu) + '</td></tr>' +
    '<tr><td>פריים: 300 מכוניות מוכנות על המסך (מ"ש לפריים)</td><td>' + f(r.fr.old) + '</td><td>' + f(r.fr.neu) + '</td></tr>' +
    '<tr><td>אותן 300 מכוניות כ-SVG ב-SVG.js (מ"ש לפריים)</td><td colspan="2">' + f(r.svgms) + '</td></tr>' +
    '<tr><td>זיכרון התמונות שנוצרו (מ"ב): מכונית · מטוס · הולך רגל</td><td>' + r.mem.cars[0] + ' · ' + r.mem.planes[0] + ' · ' + r.mem.peds[0] + '</td><td>' + r.mem.cars[1] + ' · ' + r.mem.planes[1] + ' · ' + r.mem.peds[1] + '</td></tr></table>';
  window.__bench = r }, 30) }
// ---------- the controls ----------
function redraw() { try { drawLive(); drawCars(); drawPair(); drawPlanes(); drawPlaneBig(); drawPeds(); drawLineup() } catch (e) { ERR.push('draw ' + e.message); console.error(e) } $('#errs').textContent = ERR.length ? 'שגיאות: ' + ERR.join(' | ') : '' }
function init() {
  const cs = $('#carCol'); CAR_COLS.forEach(([n, c]) => { const o = document.createElement('option'); o.value = c; o.textContent = n; cs.appendChild(o) });
  const pl = $('#pedLook'); G2.ped.LOOKS.forEach((L, i) => { const o = document.createElement('option'); o.value = i; o.textContent = L.name; pl.appendChild(o) });
  $('#zoom').oninput = e => { ST.zoom = +e.target.value; $('#zoomV').textContent = '×' + ST.zoom; redraw() };
  $('#dirs').onchange = e => { ST.dirs = +e.target.value; redraw() };
  cs.onchange = e => { ST.col = e.target.value; ZDC.clear(); redraw() };
  $('#wide').onchange = e => { ST.wide = e.target.checked; redraw() };
  $('#anim').onchange = e => { ST.anim = e.target.checked };
  $('#pedAct').onchange = () => redraw(); pl.onchange = () => redraw(); $('#pedDir').oninput = () => drawLineup();
  $('#planeDir').oninput = e => { planeDir = +e.target.value; drawPlaneBig() };
  $('#benchBtn').onclick = showBench;
  redraw();
  let last = performance.now(), acc = 0;
  const tick = now => { const dt = now - last; last = now; if (ST.anim && !document.hidden) { pedT += dt; liveT += dt; acc += dt; try { drawLive() } catch (e) { ERR.push(e.message) } spin += dt / 1000 * .5; if (acc > 110) { acc = 0; try { drawPair(); drawPeds(); drawLineup() } catch (e) { ERR.push(e.message) } } } requestAnimationFrame(tick) };
  requestAnimationFrame(tick);
  window.__res = { ok: OK, errs: ERR, g2: G2.stats() };
}
window.addEventListener('resize', () => redraw());
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
