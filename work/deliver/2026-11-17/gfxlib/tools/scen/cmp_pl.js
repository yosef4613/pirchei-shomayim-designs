a34LibInit();p34LibInit();
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
  x0 = Math.floor(x0) - 3; y0 = Math.floor(y0) - 3; const W = Math.ceil(x1 - x0) + 6, H = Math.ceil(y1 - y0) + 6, cv = new OffscreenCanvas(2,2); cv.width = W; cv.height = H; const c = cv.getContext('2d');
  const sh = new OffscreenCanvas(2,2); sh.width = W; sh.height = H; const hc = sh.getContext('2d'); hc.fillStyle = '#0c1016'; for (const q of P) A34.shadowPiece(hc, q.p, { X: -x0, Y: -y0, s: S });
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

[1,6].forEach((k,i)=>{const h=k/16*Math.PI*2+Math.PI/16;const o=oldPlane('AC-NB-01',h,7.47*1.6);dr(o,250+i*560,170,1);const e=G2.plane.sprite('AC-NB-01',h,7.47*1.6,1,16);dr(e,250+i*560,470,1)});
for(let L=0;L<6;L++){const h=2.36,ph=.3;g.save();g.translate(1150+(L%3)*150,120+Math.floor(L/3)*330);g.scale(6,6);P34.draw(g,0,0,OLD_LOOKS[L],{k:'walk'},h,ph,6);g.restore();
 const e=G2.ped.sprite(L,'walk',h,ph,11.25*6,1,16);dr(e,1150+(L%3)*150,260+Math.floor(L/3)*330,1)}
