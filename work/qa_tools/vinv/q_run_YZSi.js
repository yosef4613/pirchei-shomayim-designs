window.__VINV_T=300;window.__VINV_REBUILT='A3,A4,B3,B4'.split(',');
// vinv_lib.js — ספריית המלאי (נטענת לתוך המשחק דרך probe_c2.js; הקובץ הזה הוא חלק מהביטוי שנשלח)
// מתקין עטיפה על a.draw של כל נכס רכב (Vehicles, Heavy & Service Vehicles) ומריץ את כל פונקציות הציור של העולם
// על קנבס קטן עם טרנספורמציה של זהות (קואורדינטות עולם), VIEW_OVR על כל העולם — כך כל רכב שמצויר נרשם עם המקור שלו.
var VINV = window.VINV || (window.VINV = (function () {
  const VCAT = new Set(['Vehicles', 'Heavy & Service Vehicles']);
  const S = { on: false, rec: [], src: '', stackOn: true };
  const ACAT = new Map(); for (const a of TurboCity.assets) ACAT.set(a.id, a);
  let inTC = 0;
  function rec(c, a, lw, lh, how, sc) {
    const M = c.getTransform(), x = M.a * lw + M.c * lh + M.e, y = M.b * lw + M.d * lh + M.f, fp = a.fp || [0, 0, a.w, a.h];
    const L = fp[2] * sc * Math.hypot(M.a, M.b), W = fp[3] * sc * Math.hypot(M.c, M.d);
    let st = '';
    if (S.stackOn) { const L = String(new Error().stack).split('\n').slice(3, 14).map(l => (l.match(/at (?:Object\.|Array\.)?([A-Za-z0-9_$.<>]+) /) || [, '?'])[1]).filter(n => !/^(draw|Object\.draw|eval|\?|rec|TurboCity\.draw)$/.test(n)); st = L.slice(0, 5).join('<'); }
    S.rec.push({ src: S.src, asset: a.id, cat: a.cat, x: Math.round(x), y: Math.round(y), h: +Math.atan2(M.b, M.a).toFixed(3), al: +(c.globalAlpha).toFixed(2), L: +L.toFixed(1), W: +W.toFixed(1), how, st });
  }
  // (1) TurboCity.draw — the common path (the sprite cache sits under it, so a.draw is not called on a cache hit)
  if (!TurboCity.__vinv) { const d0 = TurboCity.draw; TurboCity.__vinv = 1;
    TurboCity.draw = function (c, id, x, y, o) { const a = S.on && ACAT.get(id);
      if (a && VCAT.has(a.cat)) { const sc = (o && o.scale) || 1; rec(c, a, x + a.w * sc / 2, y + a.h * sc / 2, 'TC', sc) }
      inTC++; try { return d0.apply(this, arguments) } finally { inTC-- } } }
  // (2) a.draw called directly (not through TurboCity.draw)
  for (const a of TurboCity.assets) {
    if (!VCAT.has(a.cat) || a.__vinv) continue;
    const f = a.draw; a.__vinv = 1;
    a.draw = function (c, St, t) { if (S.on && !inTC) { const sc = (St && St.scale) || 1; rec(c, a, a.w * sc / 2, a.h * sc / 2, 'direct', sc) } return f.apply(this, arguments) };
  }
  // the world's draw passes: (1) the static layers as WTC records them (WTC_MODE=1), (2) every live pass of render() (WTC_MODE=0)
  const STATIC = [['wtcPaintL1', n => wtcPaintL1(n)], ['wtcPaintLP', n => wtcPaintLP(n)], ['wtcPaintLO', n => wtcPaintLO(n)]];
  const LIVE = [
    ['wtcLiveUnder', n => wtcLiveUnder(n)], ['wtcLiveOver', n => wtcLiveOver(n)], ['wtcPropsLive', n => wtcPropsLive(n)], ['wtcCoolingLive', n => wtcCoolingLive(n)],
    ['b4Live', n => b4Live(n)], ['b3Live', n => b3Live(n)], ['c3Live', n => c3Live(n)], ['d3NLive', n => d3NLive(n)], ['c4NLive', n => c4NLive(n)], ['wtcAptLive', n => wtcAptLive(n)],
    ['drawFreightTrains', n => drawFreightTrains(n)], ['drawParkedCars', n => drawParkedCars(n)],
    ['drawTrafficCars', n => drawTrafficCars(n)], ['drawA4Fleet', n => { try { if (/drawA4Fleet\(now\)/.test(render.toString())) drawA4Fleet(n) } catch (e) {} }],   /* 2.11: רק כש-render() מצייר אותה (p494) */ ['drawFlowTrucks', n => drawFlowTrucks(n)], ['drawD4MovingSemis', n => drawD4MovingSemis(n)],
    ['D3LOOK.flushCars', n => { if (window.D3LOOK && D3LOOK.flushCars) D3LOOK.flushCars() }],
    ['drawBusLineVehicles', n => drawBusLineVehicles(n)], ['drawC5FleetCargo', n => drawC5FleetCargo(n)], ['drawActivityWorld', n => drawActivityWorld(n)],
    ['wtcOverLive', n => wtcOverLive(n)], ['D3LOOK.flushRoofs', n => { if (window.D3LOOK && D3LOOK.flushRoofs) D3LOOK.flushRoofs() }],
  ];
  function capture(now, o) {
    o = o || {};
    const g = document.createElement('canvas'); g.width = 32; g.height = 32; const G = g.getContext('2d'); G.setTransform(1, 0, 0, 1, 0, 0);
    const pc = ctx, pv = VIEW_OVR, pm = WTC_MODE, pcap = Targets.capture, pr = WTC.recording, pb = WTC.ctxBuilding, err = {}, ms = {};
    ctx = G; VIEW_OVR = { cx: 4800, cy: 3900, hw: 5400, hh: 5200 }; Targets.capture = []; S.rec = []; S.on = true; S.stackOn = o.stack !== false;
    const run = (list, mode) => { for (const [k, f] of list) { S.src = k; WTC_MODE = mode; const t0 = performance.now(); try { f(now) } catch (e) { err[k] = String(e && e.message || e).slice(0, 120) } ms[k] = Math.round(performance.now() - t0) } };
    try {
      if (o.static !== false) { WTC.recording = null; WTC.ctxBuilding = G; run(STATIC, 1); WTC.ctxBuilding = pb; WTC.recording = pr }
      if (o.live !== false) run(LIVE, 0);
    } finally { S.on = false; ctx = pc; VIEW_OVR = pv; WTC_MODE = pm; WTC.recording = pr; WTC.ctxBuilding = pb; var tg = Targets.capture; Targets.capture = pcap }
    // one row per drawn vehicle (a vehicle drawn twice at the same place by two passes — once)
    const seen = new Map(), U = [];
    for (const r of S.rec) { const k = r.asset + '@' + Math.round(r.x / 3) + ',' + Math.round(r.y / 3); const q = seen.get(k); if (q) { if (!q.srcs.includes(r.src)) q.srcs.push(r.src); continue } r.srcs = [r.src]; seen.set(k, r); U.push(r) }
    return { rec: U, raw: S.rec.length, err, ms, targets: tg };
  }
  function zone(x, y) { const z = tcZoneAt(x, y); return z ? z.code : '-' }
  function stepSim(sec) { const L = SIM_LOOP, H = L.h; if (L.simNow == null) L.simNow = performance.now(); const n = Math.round(sec / H); for (let i = 0; i < n; i++) { simStep(H, L.simNow + H * 1000); L.simNow += H * 1000 } return L.simNow }
  return { S, capture, zone, stepSim, STATIC, LIVE };
})());
// vinv_static.js — בדיקת הרכבים שעומדים (סוג ג) ושל המסלולים המצוירים (סוג ב): בתוך מבנה? על אספלט? יש דרך מהכביש?
// נטען אחרי vinv_lib.js. VINV.staticAudit(opts) מחזיר {rows, stats}.
VINV.AIRPORT = new Set(['E0', 'F0', 'G0', 'H0', 'E1', 'F1', 'G1', 'H1', 'E2', 'F2', 'G2', 'H2', 'G3', 'H3']);
VINV.paved = function () {
  if (VINV._pv) return VINV._pv;
  const CS = 5, X0 = 0, Y0 = -850, NX = Math.ceil(9600 / CS), NY = Math.ceil(8600 / CS), G = new Uint8Array(NX * NY);   // bit1 road (carriageway), bit2 paved (lot/yard/cut/stall/apron)
  const fill = (x0, y0, x1, y1, bit) => { const i0 = Math.max(0, Math.floor((x0 - X0) / CS)), i1 = Math.min(NX - 1, Math.floor((x1 - X0) / CS)), j0 = Math.max(0, Math.floor((y0 - Y0) / CS)), j1 = Math.min(NY - 1, Math.floor((y1 - Y0) / CS));
    for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) { const cx = X0 + (i + .5) * CS, cy = Y0 + (j + .5) * CS; if (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) G[j * NX + i] |= bit } };
  const disc = (x, y, r, bit) => { const i0 = Math.max(0, Math.floor((x - r - X0) / CS)), i1 = Math.min(NX - 1, Math.floor((x + r - X0) / CS)), j0 = Math.max(0, Math.floor((y - r - Y0) / CS)), j1 = Math.min(NY - 1, Math.floor((y + r - Y0) / CS));
    for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) { const cx = X0 + (i + .5) * CS, cy = Y0 + (j + .5) * CS; if (Math.hypot(cx - x, cy - y) <= r) G[j * NX + i] |= bit } };
  const seg = (ax, ay, bx, by, h, bit) => { const L = Math.hypot(bx - ax, by - ay), n = Math.max(1, Math.ceil(L / CS)); for (let k = 0; k <= n; k++) disc(ax + (bx - ax) * k / n, ay + (by - ay) * k / n, h, bit) };
  // the roads, exactly as pointRoad() sees them
  for (const e of EDGES) { const a = byNode[e.a], b = byNode[e.b]; if (!a || !b) continue; const h = roadType(e).width / 2;
    if (Math.abs(a.y - b.y) < .01) fill(Math.min(a.x, b.x), a.y - h, Math.max(a.x, b.x), a.y + h, 1);
    else if (Math.abs(a.x - b.x) < .01) fill(a.x - h, Math.min(a.y, b.y), a.x + h, Math.max(a.y, b.y), 1);
    else seg(a.x, a.y, b.x, b.y, h, 1) }
  for (const n of NODES) { const I = incident(n.id); if (I.length > 1) disc(n.x, n.y, Math.max(...I.map(e => roadType(e).width / 2)), 1) }
  // every paved list of the game: lots, accesses, cuts, yards, stalls, aprons, pads, drives
  const NAMES = 'A4_ACCESS A4_LOTS A4_STALLS A6_ACCESS A6_LOTS A6_STALLS B2_ACCESS B2_PARKING B3N_LOTS B3N_STALLS B3_CURB_CUTS B3_PARKING B3_SVC_LOT B4_LOTS B4_STALLS B5_ACCESS B5_PARKING B5_STALLS B6_ACCESS B6_CURB_CUTS B6_PARKING B6_STALLS C2_ACCESS C2_CURB_CUTS C2_LOTS C2_PADS C2_PARKING C2_STALLS C3_LOTS C3_STALLS C4_ACCESS C4_STALLS C4_YARDS C5_ACCESS C5_LOTS C5_STAFF_STALLS C5_TRUCK_STALLS D2_ACCESS D2_PARKING D2_STALLS D3N_STALLS D3_CURB_CUTS D3_DISPLAY_STALLS D3_PARKING D4_STAFF_STALLS D4_STALLS D5_ACCESS D5_IMPORT_STALLS D5_YARDS E3_LOTS E4_ACCESS E4_STALLS E5_ACCESS E5_STALLS PORT_STALLS PORT_YARDS PWN_STALLS RA_CUTS RA_STAFF_STALLS EW2_DRIVES EW2_LOT EW2_STALLS EW2_TRAIN_ACCESS EW2_TRAIN_YARD G77_YARD'.split(' ');
  const used = {}, rect = q => {
    if (!q) return null;
    if (Array.isArray(q) && q.length >= 4 && q.slice(0, 4).every(v => typeof v === 'number')) return q[2] > q[0] && q[3] > q[1] ? [q[0], q[1], q[2], q[3]] : null;
    if (typeof q.x === 'number' && typeof q.w === 'number') return [q.x, q.y, q.x + q.w, q.y + q.h];
    if (typeof q.x === 'number' && q.asset) { try { const I = TurboCity.info(q.asset, { scale: q.scale, rot: q.rot || 0 }); return [q.x, q.y, q.x + I.w, q.y + I.h] } catch (e) { return null } }
    if (q.rect) return rect(q.rect); return null };
  for (const nm of NAMES) { let L = null; try { L = eval(nm) } catch (e) { used[nm] = 'missing'; continue } if (!L) { used[nm] = 'null'; continue }
    const arr = Array.isArray(L) ? L : [L]; let n = 0; for (const q of arr) { const r = rect(q); if (r) { fill(r[0], r[1], r[2], r[3], 2); n++ } } used[nm] = n }
  // 2.11 (S6): the asphalt of the C5 / D5 module (C5ND.asph, D5ND.asph — what c5d5look paints)
  for (const nm of ['C5ND', 'D5ND']) { let d = null; try { d = eval(nm) } catch (e) { } if (d && Array.isArray(d.asph)) for (const r of d.asph) fill(r[0], r[1], r[2], r[3], 2) }
  // 3.11 (S7F210): C5 v6/v7 — what C5D5LOOK5 paints as asphalt / concrete (C5V6: the aprons, the yard by the workshop, the truck park with its aisle,
  // and the refinery's paved yard where the tanker drives from the gate to the filling bay); C5ND.asph is empty since v6
  try { const V = eval('C5V6'); for (const r of (V.aprons || [])) fill(r[0], r[1], r[2], r[3], 2); for (const q of [V.mid && V.mid.yard && V.mid.yard.rect, V.mid && V.mid.trucks && V.mid.trucks.rect, V.mid && V.mid.trucks && V.mid.trucks.aisle, V.refinery && V.refinery.rect]) if (q) fill(q[0], q[1], q[2], q[3], 2) } catch (e) { }
  // the modules' own paved surfaces (C3, D3N, C4N/D4N) — through parkingInfoAt in their boxes
  for (const B of [[2392, 1700, 1208, 860], [3590, 1690, 1150, 940], [2600, 2550, 1900, 800], [2500, 3150, 2200, 1100]]) {   /* 3.11: + C5/D5 (v6/v7 — their paved surfaces answer parkingInfoAt; C5ND.asph is empty now) */
    for (let y = B[1]; y < B[1] + B[3]; y += CS) for (let x = B[0]; x < B[0] + B[2]; x += CS) { const cx = x + CS / 2, cy = y + CS / 2; try { if (parkingInfoAt(cx, cy)) G[Math.floor((cy - Y0) / CS) * NX + Math.floor((cx - X0) / CS)] |= 2 } catch (e) { } } }
  // each parked car's own stall
  for (const o of allParkedCars().map(parkedCarInfo)) { const r = o.slotRect; if (r) fill(r.x, r.y, r.x + r.w, r.y + r.h, 2) }
  // the port terminal (inPortZone) — its whole ground is a paved yard
  let portN = 0; for (let j = 0; j < NY; j++) { const cy = Y0 + (j + .5) * CS; if (cy < 3300 || cy > 5300) continue; for (let i = 0; i < NX; i++) { const cx = X0 + (i + .5) * CS; if (cx < 2300 || cx > 6200) continue; try { if (inPortZone(cx, cy)) { G[j * NX + i] |= 4; portN++ } } catch (e) { } } }
  return VINV._pv = { CS, X0, Y0, NX, NY, G, used, portN, at(x, y) { const i = Math.floor((x - X0) / CS), j = Math.floor((y - Y0) / CS); return i < 0 || j < 0 || i >= NX || j >= NY ? 0 : G[j * NX + i] } };
};
// the oriented box of a vehicle (center x,y, heading h, length L, width W) — its corners, and the cells inside it
VINV.obbHas = function (v, px, py, pad) { const c = Math.cos(v.h), s = Math.sin(v.h), dx = px - v.x, dy = py - v.y, u = dx * c + dy * s, w = -dx * s + dy * c; return Math.abs(u) <= v.L / 2 + (pad || 0) && Math.abs(w) <= v.W / 2 + (pad || 0) };
VINV.staticAudit = function (opts) {
  opts = opts || {}; const t0 = performance.now(), PV = VINV.paved(), CS = PV.CS, NX = PV.NX, NY = PV.NY, X0 = PV.X0, Y0 = PV.Y0;
  const now = SIM_LOOP.simNow + (typeof SIM_BENCH_OFS !== 'undefined' ? SIM_BENCH_OFS : 0);
  const C = VINV.capture(now, { stack: true });
  // ids for what is drawn: the parked cars, the equipment lists, the D3/C4 look data
  const P = allParkedCars().map(parkedCarInfo), EQ = [];
  for (const [nm, L] of [['D4_EQUIPMENT', D4_EQUIPMENT], ['E5_EQUIPMENT', E5_EQUIPMENT], ['PORT_EQUIPMENT', PORT_EQUIPMENT]]) for (const e of L) EQ.push({ list: nm, id: e.id, x: e.x, y: e.y, path: e.path || null, label: e.label || '' });
  const near = (L, x, y, d) => { let b = null, bd = d; for (const o of L) { const q = Math.hypot(o.x - x, o.y - y); if (q < bd) { bd = q; b = o } } return b };
  const ROAD_SRC = new Set(['drawTrafficCars', 'drawFlowTrucks', 'drawD4MovingSemis', 'drawBusLineVehicles']);
  const V = [];
  for (const r of C.rec) {
    const z = VINV.zone(r.x, r.y); if (VINV.AIRPORT.has(z) || /(^|<)apt/i.test(r.st) || r.srcs.includes('wtcAptLive')) continue;
    if (ROAD_SRC.has(r.srcs[0])) continue;
    const v = { asset: r.asset, x: r.x, y: r.y, h: r.h, L: Math.max(8, r.L), W: Math.max(6, r.W), zone: z, src: r.srcs.join('+'), st: r.st, id: null, kind: 'ג', ref: null, label: '' };
    if (r.srcs.includes('drawParkedCars')) { const o = near(P, r.x, r.y, 12); if (o) { v.id = o.id; v.ref = o.ref; v.label = o.label || '' } }
    if (!v.id) { const e = near(EQ, r.x, r.y, 60); if (e) { v.id = e.id; v.label = e.label; v.list = e.list; if (e.path) { v.kind = 'ב'; v.path = e.path } } }
    if (!v.id && r.srcs.includes('D3LOOK.flushCars')) { const D = Math.hypot(r.x - 4436, r.y - 2264) < 40 ? 'D3-TURNTABLE-CAR' : (D3ND.garage && Math.abs(r.x - (D3ND.garage.lift[0] + D3ND.garage.lift[2]) / 2) < 30 && Math.abs(r.y - (D3ND.garage.lift[1] + D3ND.garage.lift[3]) / 2) < 40) ? 'D3-LIFT-CAR' : null; if (D) { v.id = D; v.kind = 'ב' } else continue }   // the fuel trips: in the time series
    if (!v.id && /carNow/.test(r.st)) { v.id = 'D3-DISPLAY-' + r.asset + '@' + r.x + ',' + r.y; v.list = 'D3ND.display_cars' }
    if (!v.id) v.id = r.srcs[0] + ':' + r.asset + '@' + r.x + ',' + r.y;
    V.push(v);
  }
  // the other vehicles, as obstacles: every static vehicle's box, grown by the half-width of a car
  const occN = new Uint8Array(NX * NY), occI = new Int32Array(NX * NY), DIL = 8;
  V.forEach((v, k) => { const R = Math.hypot(v.L, v.W) / 2 + DIL, i0 = Math.max(0, Math.floor((v.x - R - X0) / CS)), i1 = Math.min(NX - 1, Math.floor((v.x + R - X0) / CS)), j0 = Math.max(0, Math.floor((v.y - R - Y0) / CS)), j1 = Math.min(NY - 1, Math.floor((v.y + R - Y0) / CS));
    for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) { const cx = X0 + (i + .5) * CS, cy = Y0 + (j + .5) * CS; if (VINV.obbHas(v, cx, cy, DIL)) { const q = j * NX + i; if (occN[q] < 255) occN[q]++; occI[q] = k + 1 } } });
  // the buildings (footprints), for "inside a building"
  const BLD = []; for (const o of (typeof C4_BUILDINGS !== 'undefined' ? C4_BUILDINGS : [])) { const f = o.info && o.info.fp; if (f) BLD.push({ id: o.id, x: o.x + f[0], y: o.y + f[1], w: f[2], h: f[3] }) }
  const memo = [new Map(), new Map()], blk = (q, cls, r) => { const M = memo[cls]; let b = M.get(q); if (b === undefined) { const i = q % NX, j = (q - i) / NX; try { b = blockedAt(X0 + (i + .5) * CS, Y0 + (j + .5) * CS, r) || '' } catch (e) { b = 'ERR' } M.set(q, b) } return b };
  const rows = [], MAXN = opts.maxCells || 30000;
  V.forEach((v, k) => {
    const row = { id: v.id, asset: v.asset, ref: v.ref, label: v.label, zone: v.zone, x: v.x, y: v.y, h: v.h, L: v.L, W: v.W, kind: v.kind, src: v.src, list: v.list || (v.src.includes('drawParkedCars') ? 'PARKED_CARS' : ''), path: v.path || null, issues: [] };
    // (1) inside a building: the box against every building footprint (more than 4 px both ways)
    const c = Math.cos(v.h), s = Math.sin(v.h), hx = Math.abs(c) * v.L / 2 + Math.abs(s) * v.W / 2, hy = Math.abs(s) * v.L / 2 + Math.abs(c) * v.W / 2;
    const poses = v.path ? v.path.map(p => [p[0], p[1]]).concat([[v.x, v.y]]) : [[v.x, v.y]];
    for (const [px, py] of poses) for (const b of BLD) { const ox = Math.min(px + hx, b.x + b.w) - Math.max(px - hx, b.x), oy = Math.min(py + hy, b.y + b.h) - Math.max(py - hy, b.y); if (ox > 4 && oy > 4) { row.issues.push('בתוך מבנה ' + b.id + ' (' + Math.round(ox) + '×' + Math.round(oy) + ')' + (v.path ? ' ב-' + Math.round(px) + ',' + Math.round(py) : '')); break } }
    // (2) on what it stands: the center and the two ends — road / paved / port yard; and what blocks it there (pole, tree, fence, building)
    const ends = [[v.x, v.y], [v.x + c * v.L * .4, v.y + s * v.L * .4], [v.x - c * v.L * .4, v.y - s * v.L * .4]];
    const surf = ends.map(p => PV.at(p[0], p[1])); row.surface = surf.map(b => b & 1 ? 'road' : b & 2 ? 'paved' : b & 4 ? 'port' : 'none').join('/');
    if (surf.some(b => !b)) row.issues.push('לא על אספלט (מדרכה / דשא) ב-' + ends.filter((p, i) => !surf[i]).map(p => Math.round(p[0]) + ',' + Math.round(p[1])).join(' '));
    const hits = new Set(); for (const p of ends) { let b = ''; try { b = blockedAt(p[0], p[1], Math.min(6, v.W / 2)) || '' } catch (e) { } if (b && b !== 'WORLD' && !String(b).startsWith(v.id)) hits.add(b) } if (hits.size) row.issues.push('חופף מכשול: ' + [...hits].join(', '));
    // (3) access: from its own box, through paved cells clear of obstacles (a car's half-width) and of the other vehicles, to a road cell
    const cls = v.W > 24 ? 1 : 0, rr = cls ? 12 : 8, own = q => { const i = q % NX, j = (q - i) / NX; return VINV.obbHas(v, X0 + (i + .5) * CS, Y0 + (j + .5) * CS, 0) };
    const i0 = Math.floor((v.x - X0) / CS), j0 = Math.floor((v.y - Y0) / CS), start = j0 * NX + i0, seen = new Set([start]), Q = [start], why = {}; let found = null, n = 0, qh = 0;
    if (PV.G[start] & 1) found = start;
    if (found != null) n = 0;
    while (qh < Q.length && found == null && n < MAXN) { const q = Q[qh++]; n++; const i = q % NX;
      for (const d of [1, -1, NX, -NX]) { const p = q + d; if (p < 0 || p >= NX * NY || seen.has(p) || (d === 1 && i === NX - 1) || (d === -1 && i === 0)) continue; seen.add(p);
        const mine = own(p), g = PV.G[p];
        if (!mine) {
          if (!g) { why['לא אספלט'] = (why['לא אספלט'] || 0) + 1; continue }
          if (occN[p] >= 2 || (occN[p] === 1 && occI[p] !== k + 1)) { const o = V[(occI[p] || 1) - 1]; const w = 'רכב ' + (o && o.id === v.id ? '?' : o ? o.id : '?'); why[w] = (why[w] || 0) + 1; continue }
          if (!(g & 1)) { const b = blk(p, cls, rr); if (b && !String(b).startsWith(v.id)) { why[b] = (why[b] || 0) + 1; continue } }   // its own solid (id-S) is not in its way
        }
        if (g & 1) { found = p; break } Q.push(p) } }
    row.access = found != null ? 'כן' : 'לא'; row.cells = n;
    if (found == null) { row.issues.push('אין דרך לכביש' + (n >= MAXN ? ' (בחלון של ' + MAXN + ' תאים)' : '') + ' — חוסם: ' + Object.entries(why).sort((a, b) => b[1] - a[1]).slice(0, 4).map(e => e[0] + '×' + e[1]).join(', ')) }
    else { const i = found % NX, j = (found - i) / NX; row.roadAt = [Math.round(X0 + (i + .5) * CS), Math.round(Y0 + (j + .5) * CS)] }
    rows.push(row);
  });
  return { rows, stats: { vehicles: rows.length, ms: Math.round(performance.now() - t0), pavedUsed: PV.used, portCells: PV.portN, buildings: BLD.length, capErr: C.err } };
};
// vinv_check.js — הבדיקה האחת שאפשר להכניס לבנייה (אחרי vinv_lib.js ו-vinv_static.js):
//   "אף רכב לא מופיע ונעלם, ואף רכב חונה בלי גישה או בתוך מבנה".
// VINV.check({T:300}) → {ok, appear:[…], jumps:[…], parked:[…], allowed:[…]}
//  (1) מופיע / נעלם / קופץ: מריצים את הסימולציה T שניות (simStep), כל שנייה מציירים את כל העולם (VINV.capture) ובודקים:
//      · לכל מקור ציור ונכס: רכב בלי שכן (אותו נכס, עד 220 פיקס׳) שנייה לפני — "הופיע"; שנייה אחרי — "נעלם"; ציור בשקיפות (alpha<1) — "הופעה בשקיפות".
//      · לכל רשימת רכבים (TRAFFIC_CARS, BUS_VEHICLES, D4_YARD_SEMIS, FL_ACTIVE, a4FleetActors, C5_SIM.fleet): id חדש / id שנעלם / קפיצה (יותר מהמהירות × 1.6 + 260 פיקס׳ בשנייה).
//      מסירה מוכרת (ALLOW_HANDOFF): רכב שיוצא ממפרץ ורכב חונה מאותו נכס נעלם מאותו מקום (עד 45 פיקס׳) — לא נספר.
//  (2) חונה: VINV.staticAudit — בתוך מבנה, לא על אספלט, חופף מכשול, אין דרך לכביש. חריגים מוכרים — ALLOW (id → סיבה).
//  שדה התעופה (E0–H1, E2, F2, G2, H2, G3, H3) — לא נבדק כאן (שלבים 8–9).
VINV.ALLOW = {
  'D3-TURNTABLE-CAR': 'מכונית למכירה על הבמה המסתובבת של הסוכנות (D3) — תצוגה',
  'D3-DISPLAY-VH-SU-03@4423,2142': 'מכונית למכירה על משטח התצוגה של הסוכנות (D3)',
  'D3-DISPLAY-VH-SP-02@4423,2196': 'מכונית למכירה על משטח התצוגה של הסוכנות (D3)',
  'wtcPropsLive:LV-CM-01': 'קומביין בשדה החיטה (A6) — עובד בשדה, לא על אספלט',
  'wtcPropsLive:LV-TR-01': 'טרקטור בשדה התירס (A6) — עובד בשדה, לא על אספלט',
  // 2.11 (R-67, לאישורך): חניה בטור בשביל של בית פרטי (תקן החניה: 2 לבית) — המכונית האחורית יוצאת אחרי הקדמית
  'PC-B3-2': 'חניה בטור בשביל של בית פרטי ב-B3 (2 לבית) — לאישורך',
  'PC-B3-8': 'חניה בטור בשביל של בית פרטי ב-B3 (2 לבית) — לאישורך',
  'PC-B3-14': 'חניה בטור בשביל של בית פרטי ב-B3 (2 לבית) — לאישורך',
  'PC-B3-20': 'חניה בטור בשביל של בית פרטי ב-B3 (2 לבית) — לאישורך',
  'PC-D5-BUS-': 'חניון הלילה של האוטובוסים (D5): חניה בטור בנתיבים, כמו בחניון אוטובוסים אמיתי — הראשון בנתיב יוצא ראשון; לאישורך',
};
VINV.allowFor = function (id) { for (const k in VINV.ALLOW) if (id === k || id.startsWith(k + '@') || ((!/^PC-/.test(k) || k.endsWith('-')) && id.startsWith(k))) return VINV.ALLOW[k]   /* 2.11: PC- — רק התאמה מלאה (PC-B3-2 ≠ PC-B3-21) */; return null };
VINV.check = function (o) {
  o = o || {}; const T = o.T || 300, DT = 1, w0 = performance.now(), ofs = (typeof SIM_BENCH_OFS !== 'undefined' ? SIM_BENCH_OFS : 0);
  const px = PlayerCar.x, py = PlayerCar.y; PlayerCar.x = -99999; PlayerCar.y = -99999;
  const AIR = VINV.AIRPORT, out = { appear: [], jumps: [], parked: [], allowed: [], handoff: [] };
  const ARR = { TRAFFIC_CARS: () => TRAFFIC_CARS, BUS_VEHICLES: () => BUS_VEHICLES, D4_YARD_SEMIS: () => D4_YARD_SEMIS, FL_ACTIVE: () => FL_ACTIVE, a4FleetActors: () => a4FleetActors(), 'C5_SIM.fleet': () => C5_SIM.fleet };
  const last = {}; for (const k in ARR) last[k] = new Map();
  // the sources whose vehicles have ids — checked by id (new / lost / jump / not drawn), not by the neighbour rule (fast cars, zone edges)
  const IDSRC = new Set(['drawTrafficCars', 'drawFlowTrucks', 'drawD4MovingSemis', 'drawBusLineVehicles', 'drawA4Fleet']);   /* 2.11: הכבאית והאמבולנס (p494) — לפי a4FleetActors */
  const notDrawn = {};
  let prev = null, prevP = null; const seenAlpha = {};
  try {
    for (let t = 0; t <= T; t += DT) {
      if (t > 0) VINV.stepSim(DT);
      const C = VINV.capture(SIM_LOOP.simNow + ofs, { static: false, stack: false });
      const cur = {}; for (const r of C.rec) { if (AIR.has(VINV.zone(r.x, r.y))) continue; const k = r.srcs[0] + '|' + r.asset; (cur[k] = cur[k] || []).push(r);
        if (r.al < 1 && !seenAlpha[k]) { seenAlpha[k] = 1; out.appear.push({ src: k, what: 'הופעה בשקיפות', t, at: [r.x, r.y], alpha: r.al }) } }
      if (prev) {
        // births and deaths per draw source; a parked car of the same asset that vanished / came back at the same place = a hand-off
        const born = [], gone = [];
        for (const k of new Set([...Object.keys(cur), ...Object.keys(prev)])) { if (IDSRC.has(k.split('|')[0])) continue; const A = cur[k] || [], B = prev[k] || [];
          for (const r of A) if (!B.some(q => Math.hypot(q.x - r.x, q.y - r.y) < 220)) born.push({ k, r });
          for (const q of B) if (!A.some(r => Math.hypot(q.x - r.x, q.y - r.y) < 220)) gone.push({ k, r: q }) }
        const pair = (a, L) => L.findIndex(b => b.r.asset === a.r.asset && b.k !== a.k && Math.hypot(b.r.x - a.r.x, b.r.y - a.r.y) < 45);
        const bornP = born.filter(b => b.k.startsWith('drawParkedCars')), goneP = gone.filter(b => b.k.startsWith('drawParkedCars'));
        for (const b of born) { if (b.k.startsWith('drawParkedCars')) continue; const i = pair(b, goneP); if (i >= 0) { out.handoff.push({ t, src: b.k, at: [b.r.x, b.r.y], what: 'יצא מהמפרץ' }); goneP.splice(i, 1); continue } out.appear.push({ src: b.k, what: 'הופיע', t, at: [b.r.x, b.r.y] }) }
        for (const g of gone) { if (g.k.startsWith('drawParkedCars')) continue; const i = pair(g, bornP); if (i >= 0) { out.handoff.push({ t, src: g.k, at: [g.r.x, g.r.y], what: 'חזר למפרץ' }); bornP.splice(i, 1); continue } out.appear.push({ src: g.k, what: 'נעלם', t, at: [g.r.x, g.r.y] }) }
      }
      const nowP = [].concat(...Object.keys(cur).filter(k => k.startsWith('drawParkedCars')).map(k => cur[k])), wasP = prevP || nowP;
      const pkGone = wasP.filter(q => !nowP.some(r => Math.hypot(r.x - q.x, r.y - q.y) < 3)), pkBorn = nowP.filter(r => !wasP.some(q => Math.hypot(r.x - q.x, r.y - q.y) < 3));
      const pkChange = (x, y, kind) => (kind === 'gone' ? pkGone : pkBorn).some(q => Math.hypot(q.x - x, q.y - y) < 60);
      prevP = nowP;
      prev = cur;
      // the lists: new id / lost id / jump
      for (const k in ARR) { const L = ARR[k]() || [], M = last[k], seen = new Set();
        for (const v of L) { seen.add(v.id); const lp = M.get(v.id); if (AIR.has(VINV.zone(v.x, v.y))) { M.set(v.id, { x: v.x, y: v.y, sp: v.speed || 0 }); continue }
          if (!((window.SEMI_ART || (typeof SEMI_ART !== 'undefined')) && (k === 'D4_YARD_SEMIS' || k === 'FL_ACTIVE')) && !C.rec.some(r => Math.abs(r.x - v.x) < 4 && Math.abs(r.y - v.y) < 4))   /* 2.11: הסמי בשני גופים (p490) מצויר בצייר משלו */ { const nk = k + ' ' + v.id; if (!notDrawn[nk]) { notDrawn[nk] = 1; out.appear.push({ src: k, id: v.id, what: 'לא מצויר (קיים ברשימה, לא נראה)', t, at: [Math.round(v.x), Math.round(v.y)] }) } }
          if (!lp && t > 0) { if (pkChange(v.x, v.y, 'gone')) out.handoff.push({ t, src: k, id: v.id, at: [Math.round(v.x), Math.round(v.y)], what: 'יצא מהמפרץ (הרכב החונה הוסתר באותו מקום)' }); else out.appear.push({ src: k, id: v.id, what: 'id חדש', t, at: [Math.round(v.x), Math.round(v.y)] }) }
          if (lp) { const d = Math.hypot(v.x - lp.x, v.y - lp.y); if (d > Math.max(260, (Math.max(v.speed || 0, lp.sp) + 60) * DT * 1.6)) out.jumps.push({ src: k, id: v.id, t, d: Math.round(d), from: [Math.round(lp.x), Math.round(lp.y)], to: [Math.round(v.x), Math.round(v.y)] }) }
          M.set(v.id, { x: v.x, y: v.y, sp: v.speed || 0 }) }
        for (const [id, p] of M) if (!seen.has(id)) { if (!AIR.has(VINV.zone(p.x, p.y))) { if (pkChange(p.x, p.y, 'born')) out.handoff.push({ t, src: k, id, at: [Math.round(p.x), Math.round(p.y)], what: 'חזר למפרץ (הרכב החונה חזר באותו מקום)' }); else out.appear.push({ src: k, id, what: 'id נעלם', t, at: [Math.round(p.x), Math.round(p.y)] }) } M.delete(id) } }
      if (t > 0) { const H = out.handoff.filter(h => h.t === t); for (const q of pkGone) if (!H.some(h => Math.hypot(h.at[0] - q.x, h.at[1] - q.y) < 60)) out.appear.push({ src: 'drawParkedCars|' + q.asset, what: 'רכב חונה נעלם', t, at: [q.x, q.y] }); for (const q of pkBorn) if (!H.some(h => Math.hypot(h.at[0] - q.x, h.at[1] - q.y) < 60)) out.appear.push({ src: 'drawParkedCars|' + q.asset, what: 'רכב חונה הופיע', t, at: [q.x, q.y] }) }
    }
  } finally { PlayerCar.x = px; PlayerCar.y = py }
  // (2) the parked / standing vehicles
  const S = VINV.staticAudit({ maxCells: o.maxCells || 30000 });
  for (const r of S.rows) { if (!r.issues.length) continue; const a = VINV.allowFor(r.id); if (a) out.allowed.push({ id: r.id, why: a, issues: r.issues }); else out.parked.push({ id: r.id, asset: r.asset, zone: r.zone, at: [r.x, r.y], issues: r.issues }) }
  out.T = T; out.vehiclesChecked = S.rows.length; out.ms = Math.round(performance.now() - w0);
  // one line per source in the summary (the same truck spawning 40 times is one finding)
  const bySrc = {}; for (const a of out.appear) { const k = a.src + ' · ' + a.what; bySrc[k] = (bySrc[k] || 0) + 1 } out.appearBySource = bySrc;
  out.ok = !out.appear.length && !out.jumps.length && !out.parked.length;
  return out;
};
;(()=>{const T=+(window.__VINV_T||300),RB=new Set(window.__VINV_REBUILT||[]);const R=VINV.check({T});
const zAt=a=>a&&a.length===2?VINV.zone(a[0],a[1]):'-';
const ap=R.appear.map(a=>Object.assign({zone:zAt(a.at)},a)),jp=R.jumps.map(j=>Object.assign({zone:zAt(j.to)},j));
const inR=x=>RB.has(x.zone);
const out={T:R.T,ms:R.ms,vehiclesChecked:R.vehiclesChecked,rebuilt:[...RB],
 rebuiltAppear:ap.filter(inR),rebuiltJumps:jp.filter(inR),rebuiltParked:R.parked.filter(inR),
 oldAppearBySource:{},oldJumps:jp.filter(x=>!inR(x)).length,oldParked:R.parked.filter(x=>!inR(x)).map(p=>p.id+' '+p.zone),
 allowed:R.allowed.map(a=>a.id+' — '+a.why),handoff:R.handoff.length};
for(const a of ap.filter(x=>!inR(x))){const k=a.src+' · '+a.what+' · '+a.zone;out.oldAppearBySource[k]=(out.oldAppearBySource[k]||0)+1}
out.ok=!out.rebuiltAppear.length&&!out.rebuiltJumps.length&&!out.rebuiltParked.length;return JSON.stringify(out)})()
