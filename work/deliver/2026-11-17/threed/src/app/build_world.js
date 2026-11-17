// בונה את העולם בתלת־ממד מתוך נתוני B4 — הכול גאומטריה בקוד, צבע לכל קודקוד, ומאוחד לכמה רשתות בלבד (מעט קריאות ציור).
import * as THREE from 'three';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

export const PAL = {   // הצבעים של טורבו סיטי (מתוך הקוד של המשחק: 062 grass, ‏019 asph, ‏008 LD/NAVY)
  grass: '#5f9150', grass2: '#6c9b51', grassFar: '#567f47', asph: '#474c52', asph2: '#55595f', walk: '#c9c5ba', curb: '#e2ded3',
  line: '#f2f0e6', yellow: '#e8c440', park: '#7fae5f', path: '#d9c79c', court: '#b9653a', courtLine: '#f4efe2',
  gold: '#d4af37', navy: '#1b2b45', roof: '#a9a59b', trunk: '#6b4a2f', leaf: ['#3f7a3a', '#4c8a3e', '#5a963f', '#3a6e43'],
};
const C = new THREE.Color();
function colorize(g, hex) { const n = g.attributes.position.count, a = new Float32Array(n * 3); C.set(hex).convertSRGBToLinear(); for (let i = 0; i < n; i++) { a[i * 3] = C.r; a[i * 3 + 1] = C.g; a[i * 3 + 2] = C.b } g.setAttribute('color', new THREE.BufferAttribute(a, 3)); return g }
function norm(g) { g = g.index ? g.toNonIndexed() : g; for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'color'].includes(k)) g.deleteAttribute(k); return g }

export class Acc {   // צובר גאומטריות לפי חומר
  constructor() { this.parts = {} }
  add(mat, g, hex) { g = norm(colorize(g, hex)); (this.parts[mat] ||= []).push(g); return g }
  box(mat, x0, y0, z0, x1, y1, z1, hex) {   // x מזרח, y למעלה, z דרום (מטרים)
    const g = new THREE.BoxGeometry(Math.max(.01, x1 - x0), Math.max(.01, y1 - y0), Math.max(.01, z1 - z0)); g.translate((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); return this.add(mat, g, hex)
  }
  flat(mat, x0, z0, x1, z1, y, hex) { const g = new THREE.PlaneGeometry(x1 - x0, z1 - z0); g.rotateX(-Math.PI / 2); g.translate((x0 + x1) / 2, y, (z0 + z1) / 2); return this.add(mat, g, hex) }
  disc(mat, x, z, r, y, hex, seg = 40, r0 = 0) { const g = r0 ? new THREE.RingGeometry(r0, r, seg) : new THREE.CircleGeometry(r, seg); g.rotateX(-Math.PI / 2); g.translate(x, y, z); return this.add(mat, g, hex) }
  cyl(mat, x, y0, z, r, h, hex, seg = 10, r2) { const g = new THREE.CylinderGeometry(r2 ?? r, r, h, seg); g.translate(x, y0 + h / 2, z); return this.add(mat, g, hex) }
  geo(mat, g, hex) { return this.add(mat, g, hex) }
  build(mats) { const out = []; for (const [k, list] of Object.entries(this.parts)) { const m = new THREE.Mesh(mergeGeometries(list), mats[k]); m.name = k; out.push(m) } return out }
}

// חיסור קטעים: [a,b] פחות רשימת קטעים
function subtract(a, b, cuts) { let segs = [[a, b]]; for (const [c0, c1] of cuts) { const n = []; for (const [s0, s1] of segs) { if (c1 <= s0 || c0 >= s1) { n.push([s0, s1]); continue } if (c0 > s0) n.push([s0, c0]); if (c1 < s1) n.push([c1, s1]) } segs = n } return segs.filter(s => s[1] - s[0] > .3) }

export function buildWorld(DATA, A, opt = {}) {
  const CTX = [-70, -70, 210, 160];         // מעבר לחלון — הכבישים ממשיכים אל מחוץ לתמונה
  const lamps = [], trees = [], palms = [], signals = [], pools = [], benches = []; const W0 = { trees };
  // הקרקע
  A.flat('ground', -400, -400, 600, 500, -0.02, PAL.grassFar);
  A.flat('ground', CTX[0], CTX[1], CTX[2], CTX[3], 0, PAL.grass);
  // הכבישים — כולם מקבילים לצירים בתוכנית
  const roads = DATA.roads.map(r => {
    let [[ax, ay], [bx, by]] = r.pts; const vert = ax === bx;
    const clipA = v => Math.max(vert ? CTX[1] : CTX[0], Math.min(vert ? CTX[3] : CTX[2], v));
    let s0 = vert ? Math.min(ay, by) : Math.min(ax, bx), s1 = vert ? Math.max(ay, by) : Math.max(ax, bx);
    return { ...r, vert, c: vert ? ax : ay, s0: clipA(s0), s1: clipA(s1), hw: r.width / 2 };
  });
  const ends = new Set(DATA.nodes.filter(n => n.kind === 'end').map(n => n.p.join(',')));
  const RB = DATA.nodes.filter(n => n.kind === 'roundabout').map(n => ({ x: n.p[0], z: n.p[1], R: 14, Ri: 6 }));
  const JN = DATA.nodes.filter(n => n.kind === 'signal' || n.kind === 'roundabout');
  // רוחב החצייה של כל דרך שחוצה קו נתון
  function crossCuts(line, vertLine, pad) {   // קטעים לאורך הקו שבהם דרך ניצבת חוצה
    const cuts = [];
    for (const q of roads) if (q.vert !== vertLine && line >= q.s0 - q.hw - pad && line <= q.s1 + q.hw + pad) cuts.push([q.c - q.hw - pad, q.c + q.hw + pad]);
    return cuts;
  }
  const rbCuts = (line, vertLine, extra) => RB.filter(o => Math.abs((vertLine ? o.x : o.z) - line) < o.R + extra).map(o => { const d = (vertLine ? o.x : o.z) - line, h = Math.sqrt(Math.max(0, (o.R + extra) ** 2 - d * d)); const c = vertLine ? o.z : o.x; return [c - h, c + h] });
  for (const r of roads) {
    const ext = ends.has((r.vert ? [r.c, r.s1] : [r.s1, r.c]).join(',')) ? 0 : r.hw;   // סוף רחוב ללא מוצא — לא נמשך
    const a = r.s0 - (r.s0 > (r.vert ? CTX[1] : CTX[0]) ? r.hw : 0), b = r.s1 + (r.s1 < (r.vert ? CTX[3] : CTX[2]) ? ext : 0);
    const R = (u0, u1, v0, v1, y, hex, mat = 'ground', box) => r.vert ? (box ? A.box(mat, r.c + u0, 0, v0, r.c + u1, y, v1, hex) : A.flat(mat, r.c + u0, v0, r.c + u1, v1, y, hex)) : (box ? A.box(mat, v0, 0, r.c + u0, v1, y, r.c + u1, hex) : A.flat(mat, v0, r.c + u0, v1, r.c + u1, y, hex));
    R(-r.hw, r.hw, a, b, 0.02, PAL.asph);
    // מדרכות ואבני שפה — נקטעות בכל דרך ניצבת ובכיכר
    for (const side of [-1, 1]) {
      const lineAt = r.c + side * (r.hw + r.walk / 2);
      const cuts = [...crossCuts(lineAt, r.vert, 0), ...rbCuts(lineAt, r.vert, 0)];
      for (const [u0, u1] of subtract(a - r.walk, b + r.walk, cuts)) {
        const lo = side < 0 ? -r.hw - r.walk : r.hw, hi = side < 0 ? -r.hw : r.hw + r.walk;
        R(lo, hi, u0, u1, 0.15, PAL.walk, 'ground', true);
        const cl = side < 0 ? -r.hw - 0.02 : r.hw, ch = cl + 0.22; R(side < 0 ? -r.hw - 0.22 : r.hw, side < 0 ? -r.hw : r.hw + 0.22, u0, u1, 0.17, PAL.curb, 'ground', true);
        // פנסים כל ~26 מ׳ ועצים ביניהם
        if (r.cls !== 'arterial') for (let u = u0 + 21; u < u1 - 6; u += 26) { const off = side * (r.hw + r.walk - 0.9); W0.trees.push(r.vert ? { x: r.c + off, z: u, s: .72 } : { x: u, z: r.c + off, s: .72 }) }
        for (let u = u0 + 8; u < u1 - 4; u += 26) { const off = side * (r.hw + r.walk - 0.5); const p = r.vert ? [r.c + off, u] : [u, r.c + off]; lamps.push({ x: p[0], z: p[1], dir: r.vert ? (side < 0 ? 0 : Math.PI) : (side < 0 ? -Math.PI / 2 : Math.PI / 2) }) }
      }
    }
    // סימון נתיבים — לא בתוך צמתים
    const jcuts = [...crossCuts(r.c, r.vert, 1.5), ...rbCuts(r.c, r.vert, 2)];
    const live = subtract(a, b, jcuts);
    const dash = (off, w, on, offL, hex) => { for (const [u0, u1] of live) for (let u = u0 + 1; u < u1 - 1; u += on + offL) R(off - w / 2, off + w / 2, u, Math.min(u + on, u1 - 1), 0.035, hex) };
    const solid = (off, w, hex) => { for (const [u0, u1] of live) R(off - w / 2, off + w / 2, u0 + .5, u1 - .5, 0.035, hex) };
    if (r.median) {   // עורק: חציון מוגבה עם דשא, נתיבים, קו שפה
      for (const [u0, u1] of live) { R(-r.median / 2, r.median / 2, u0 + 1, u1 - 1, 0.18, PAL.curb, 'ground', true); R(-r.median / 2 + .25, r.median / 2 - .25, u0 + 1.3, u1 - 1.3, 0.2, PAL.grass2, 'ground', true); for (let u = u0 + 6; u < u1 - 4; u += 14) palms.push(r.vert ? { x: r.c, z: u } : { x: u, z: r.c }) }
      for (const s of [-1, 1]) { dash(s * (r.median / 2 + 3.9), .15, 3, 6, PAL.line); solid(s * (r.median / 2 + 7.8), .15, PAL.line) }
    } else { dash(0, .15, 3, 5, PAL.line); for (const s of [-1, 1]) solid(s * 3.9, .12, PAL.line) }
  }
  // הכיכר
  for (const o of RB) {
    A.disc('ground', o.x, o.z, o.R + 2.5, 0.15, PAL.walk, 48, o.R); A.disc('ground', o.x, o.z, o.R, 0.03, PAL.asph, 48);
    A.cyl('ground', o.x, 0, o.z, o.Ri, .22, PAL.curb, 40); A.cyl('ground', o.x, 0, o.z, o.Ri - .3, .26, PAL.park, 40);
    A.disc('ground', o.x, o.z, o.Ri + 1.6, 0.04, PAL.line, 48, o.Ri + 1.45);
    palms.push({ x: o.x, z: o.z, big: 1 }); for (let i = 0; i < 6; i++) trees.push({ x: o.x + Math.cos(i) * 3.6, z: o.z + Math.sin(i) * 3.6, s: .45, bush: 1 });
  }
  // מעברי חצייה וקווי עצירה — רק בצמתים (כלל 21)
  for (const n of JN) {
    const [x, z] = n.p, arms = [];
    for (const r of roads) { const along = r.vert ? z : x; if (Math.abs((r.vert ? x : z) - r.c) < .1 && along >= r.s0 - 1 && along <= r.s1 + 1) { if (r.s0 < along - 1) arms.push({ r, dir: -1 }); if (r.s1 > along + 1) arms.push({ r, dir: 1 }) } }
    const uniq = new Map(); for (const a of arms) uniq.set(a.r.vert + ':' + a.dir, a);
    for (const { r, dir } of uniq.values()) {
      let perp = 0; for (const q of roads) if (q.vert !== r.vert && Math.abs(q.c - (r.vert ? z : x)) < .1 && (r.vert ? x : z) >= q.s0 - q.hw && (r.vert ? x : z) <= q.s1 + q.hw) perp = Math.max(perp, q.hw);
      if (n.kind === 'roundabout') perp = 14.5;
      const u0 = (r.vert ? z : x) + dir * (perp + 1.2), u1 = u0 + dir * 3;
      for (let k = -r.hw + .6; k < r.hw - .5; k += 1.1) { const a0 = r.c + k, a1 = a0 + .55; if (r.median && Math.abs(k + .27) < r.median / 2) continue; r.vert ? A.flat('ground', a0, Math.min(u0, u1), a1, Math.max(u0, u1), .036, PAL.line) : A.flat('ground', Math.min(u0, u1), a0, Math.max(u0, u1), a1, .036, PAL.line) }
      if (n.kind === 'signal') {   // קו עצירה בנתיבים הנכנסים (נוסעים בימין)
        const s = r.vert ? (dir > 0 ? 1 : -1) : (dir > 0 ? -1 : 1); /* הצד הימני של התנועה שנכנסת לצומת */ const us = u1 + dir * .7, lo = r.median ? r.median / 2 : 0;
        const p0 = r.c + s * lo, p1 = r.c + s * r.hw * .9; r.vert ? A.flat('ground', Math.min(p0, p1), Math.min(us, us + dir * .5), Math.max(p0, p1), Math.max(us, us + dir * .5), .036, PAL.line) : A.flat('ground', Math.min(us, us + dir * .5), Math.min(p0, p1), Math.max(us, us + dir * .5), Math.max(p0, p1), .036, PAL.line);
        const side = s;  // עמוד הרמזור בצד הימני של הנתיב הנכנס
        const px = r.vert ? r.c + side * (r.hw + .8) : u1 + dir * 1.5, pz = r.vert ? u1 + dir * 1.5 : r.c + side * (r.hw + .8);
        signals.push({ node: n.id, x: px, z: pz, axis: r.vert ? 'NS' : 'EW', ax: r.vert ? -side : 0, az: r.vert ? 0 : -side, fx: r.vert ? 0 : dir, fz: r.vert ? dir : 0, reach: Math.min(5, r.hw * .7) });
      }
    }
  }
  // סוף רחוב ללא מוצא — מעגל סיבוב
  for (const n of DATA.nodes.filter(n => n.kind === 'end')) { A.disc('ground', n.p[0], n.p[1], 9.5, .15, PAL.walk, 40, 7.5); A.disc('ground', n.p[0], n.p[1], 7.6, .021, PAL.asph, 40) }
  return { lamps, trees, palms, signals, pools, benches, roads, RB };
}

// מבנים, חניונים, פארקים
const USE = { 'B4-N1': ['#e9dcc0', '#c96f4a'], 'B4-N0': ['#e2cfa9', '#5d8aa8'], 'B4-N2': ['#ebe2cf', '#b9563d'], 'B4-N3': ['#dcc6a0', '#4f7f6a'], 'B4-S1': ['#efe7d6', '#2f7d4f'], 'B4-S2': ['#f4f2ec', '#3b74b8'], 'B4-S3': ['#e7bd8d', '#2e5e8e'] };
export function buildLots(DATA, A, W) {
  const lit = [];
  for (const s of DATA.sites) {
    const [x0, z0, x1, z1] = s.rect;
    if (s.kind === 'parking' || s.kind === 'yard') {
      A.box('ground', x0, 0, z0, x1, .12, z1, s.kind === 'parking' ? PAL.asph2 : '#bdb6a2');
      if (s.kind === 'parking') { const wide = x1 - x0 > z1 - z0; const L = wide ? x1 - x0 : z1 - z0, n = Math.floor((L - 1) / 2.6); const depth = Math.min(5.2, (wide ? z1 - z0 : x1 - x0) / 2 - .3);
        for (let i = 0; i <= n; i++) { const u = (wide ? x0 : z0) + .5 + i * 2.6; for (const e of [0, 1]) { const d0 = e ? (wide ? z1 : x1) - depth : (wide ? z0 : x0) + .2, d1 = d0 + depth - .2; wide ? A.flat('ground', u, d0, u + .12, d1, .126, PAL.line) : A.flat('ground', d0, u, d1, u + .12, .126, PAL.line) } } }
      continue;
    }
    if (s.kind === 'park') { A.box('ground', x0, 0, z0, x1, .1, z1, PAL.park); A.box('ground', x0 + 2, 0, (z0 + z1) / 2 - 1, x1 - 2, .12, (z0 + z1) / 2 + 1, PAL.path); A.box('ground', (x0 + x1) / 2 - 3.5, 0, z0 + 3, (x0 + x1) / 2 + 3.5, .13, z0 + 9, '#d8b07a');
      playground(A, (x0 + x1) / 2, z0 + 6); for (let i = 0; i < 7; i++) W.trees.push({ x: x0 + 2 + ((i * 37) % 9), z: z0 + 11 + i * 1.3 + (i % 3) * 1.1, s: .8 + (i % 3) * .15 }); W.benches.push({ x: x0 + 3, z: (z0 + z1) / 2 + 2, r: 0 }, { x: x1 - 3, z: (z0 + z1) / 2 - 2, r: Math.PI }); continue }
    if (s.kind === 'court') { A.box('ground', x0, 0, z0, x1, .12, z1, PAL.court); const cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
      for (const [a, b, c, d] of [[x0 + 1, z0 + 1, x1 - 1, z0 + 1.12], [x0 + 1, z1 - 1.12, x1 - 1, z1 - 1], [x0 + 1, z0 + 1, x0 + 1.12, z1 - 1], [x1 - 1.12, z0 + 1, x1 - 1, z1 - 1], [cx - .06, z0 + 1, cx + .06, z1 - 1]]) A.flat('ground', a, b, c, d, .126, PAL.courtLine);
      A.disc('ground', cx, cz, 1.9, .127, PAL.courtLine, 32, 1.75); for (const e of [-1, 1]) { const hx = cx + e * ((x1 - x0) / 2 - 1.6); A.cyl('solid', hx + e * .6, 0, cz, .07, 3, '#666', 6); A.box('solid', hx - .05, 2.9, cz - .9, hx + .05, 3.95, cz + .9, '#f2f2f2') }
      continue }
    if (s.kind !== 'building') continue;
    const [wall, accent] = USE[s.id] || ['#e2d6bd', '#7a8f9e'];
    const fl = s.floors || 1, fh = s.id === 'B4-S1' ? 5 : 3.3, H = fl * fh;
    let boxes = [[x0, z0, x1, z1]];
    if (s.id === 'B4-N3') boxes = [[x0, z0, x0 + 12, z1], [x0 + 12, z0 + 9, x1, z1]];   // בניין ה-L
    for (const [a0, b0, a1, b1] of boxes) {
      A.box('solid', a0, 0, b0, a1, .5, b1, '#8d8679');            // מסד
      A.box('solid', a0 + .05, .5, b0 + .05, a1 - .05, H, b1 - .05, wall);
      for (let f = 1; f < fl; f++) A.box('solid', a0 - .08, f * fh - .12, b0 - .08, a1 + .08, f * fh + .08, b1 + .08, '#f3eee3');   // פסי קומות
      A.box('solid', a0, H, b0, a1, H + .25, b1, PAL.roof); A.box('solid', a0 - .1, H, b0 - .1, a1 + .1, H + .9, b0 + .15, '#d9d2c2'); A.box('solid', a0 - .1, H, b1 - .15, a1 + .1, H + .9, b1 + .1, '#d9d2c2'); A.box('solid', a0 - .1, H, b0, a0 + .15, H + .9, b1, '#d9d2c2'); A.box('solid', a1 - .15, H, b0, a1 + .1, H + .9, b1, '#d9d2c2');
      // חלונות בכל חזית
      const facade = (ax, az, bx, bz, nx, nz) => { const L = Math.hypot(bx - ax, bz - az), n = Math.max(1, Math.floor((L - 1.5) / 3)), ux = (bx - ax) / L, uz = (bz - az) / L;
        for (let f = 0; f < fl; f++) for (let i = 0; i < n; i++) { const t = (L - (n - 1) * 3) / 2 + i * 3; const cx = ax + ux * t + nx * .06, cz = az + uz * t + nz * .06; const y0 = f * fh + (s.id === 'B4-S1' ? .6 : 1.0), y1 = y0 + (s.id === 'B4-S1' ? 3.2 : 1.55); const w = s.id === 'B4-S1' || s.id === 'B4-S3' ? 2.4 : 1.4;
          const g = new THREE.BoxGeometry(Math.abs(ux) * w + Math.abs(nx) * .08, y1 - y0, Math.abs(uz) * w + Math.abs(nz) * .08); g.translate(cx, (y0 + y1) / 2, cz);
          const on = ((i * 7 + f * 13 + s.id.length * 3) % 5) < 2; A.geo(on ? 'glassLit' : 'glass', g, on ? '#ffd88a' : '#2a3b52'); if (on) lit.push(1);
          const fr = new THREE.BoxGeometry(Math.abs(ux) * (w + .3) + Math.abs(nx) * .05, .18, Math.abs(uz) * (w + .3) + Math.abs(nz) * .05); fr.translate(cx + nx * .03, y0 - .1, cz + nz * .03); A.geo('solid', fr, '#efe9dc');
          if (fl > 1 && f > 0 && i % 2 === 0 && nz > 0 && s.id.startsWith('B4-N')) { A.box('solid', cx - ux * 1.1 - .02, y0 - .35, cz, cx + ux * 1.1 + .02, y0 - .2, cz + 1.2, '#e8e2d4'); A.box('solid', cx - ux * 1.1, y0 - .2, cz + 1.12, cx + ux * 1.1, y0 + .7, cz + 1.2, accent) }   // מרפסות לדרום
        } };
      facade(a0, b1, a1, b1, 0, 1); facade(a1, b0, a0, b0, 0, -1); facade(a0, b0, a0, b1, -1, 0); facade(a1, b1, a1, b0, 1, 0);
      // דודי שמש וגג
      if (s.id.startsWith('B4-N')) for (let i = 0; i < Math.floor((a1 - a0) / 3.2); i++) { const x = a0 + 1.6 + i * 3.2, z = b0 + 1.6; A.box('solid', x - .9, H + .25, z, x + .9, H + .3, z + 1.8, '#2b3d55'); const tank = new THREE.CylinderGeometry(.32, .32, 1.7, 10); tank.rotateZ(Math.PI / 2); tank.translate(x, H + 1.35, z - .1); A.geo('solid', tank, '#e9e6df'); A.box('solid', x - .9, H + .3, z + 1.6, x + .9, H + 1.1, z + 1.75, '#2b3d55') }
      if (!s.id.startsWith('B4-N')) for (let i = 0; i < 3; i++) A.box('solid', a0 + 2 + i * 3, H + .25, b0 + 2, a0 + 3.6 + i * 3, H + 1.2, b0 + 3.2, '#b8b8b2');
    }
    // כניסה וגגון בצבע המבנה
    const [a0, b0, a1, b1] = boxes[boxes.length - 1]; const ex = (a0 + a1) / 2;
    A.box('solid', ex - 2.2, fh - .4, b1, ex + 2.2, fh - .2, b1 + 1.6, accent); A.box('solid', ex - 1, .5, b1 - .02, ex + 1, 2.6, b1 + .05, '#3a2e25');
    W.signs.push({ text: s.label.split(' — ')[0].split(' · ').pop().replace(/^הסופר /, ''), x: ex, y: fh + .55, z: b1 + 1.7, w: Math.min(a1 - a0 - 2, 14), accent, id: s.id });
  }
  // הסביבה — המבנים של האזורים השכנים מהמפה, ברמת פירוט נמוכה (כמו אזור שעוד לא נטען במלואו)
  for (const c of DATA.context || []) { const [x0, z0, x1, z1] = c.rect, H = c.floors * 3.3; A.box('solid', x0, 0, z0, x1, H, z1, '#cfc8b8'); A.box('solid', x0, H, z0, x1, H + .3, z1, '#9c988f') }
  for (const l of DATA.lots) { const [x0, z0, x1, z1] = l.rect; A.box('ground', x0, 0, z0, x1, .1, z1, PAL.park); A.box('ground', (x0 + x1) / 2 - .8, 0, z0, (x0 + x1) / 2 + .8, .12, z1, PAL.path);
    const n = Math.floor((x1 - x0) * (z1 - z0) / 70); for (let i = 0; i < n; i++) { const fx = ((i * 0.618) % 1), fz = ((i * 0.382 + .17) % 1); const x = x0 + 2 + fx * (x1 - x0 - 4), z = z0 + 2 + fz * (z1 - z0 - 4); if (Math.abs(x - (x0 + x1) / 2) > 2) W.trees.push({ x, z, s: .75 + (i % 4) * .12 }) } W.benches.push({ x: (x0 + x1) / 2 + 1.6, z: (z0 + z1) / 2, r: Math.PI / 2 }) }
  for (const d of DATA.driveways) { const [[ax, az], [bx, bz]] = d.pts; const h = d.w / 2; ax === bx ? A.box('ground', ax - h, 0, Math.min(az, bz), ax + h, .165, Math.max(az, bz), PAL.asph2) : A.box('ground', Math.min(ax, bx), 0, az - h, Math.max(ax, bx), .165, az + h, PAL.asph2) }
  return lit.length;
}
function playground(A, x, z) { A.box('solid', x - 2.6, 0, z - .1, x - 2.4, 2.2, z + .1, '#c0392b'); A.box('solid', x - .6, 0, z - .1, x - .4, 2.2, z + .1, '#c0392b'); A.box('solid', x - 2.6, 2.1, z - .1, x - .4, 2.3, z + .1, '#c0392b'); A.box('solid', x - 2, .6, z - .25, x - 1.4, .7, z + .25, '#333'); A.box('solid', x + 1, 0, z - .8, x + 2.4, 1.6, z + .8, '#e2a93b'); const sl = new THREE.BoxGeometry(.9, .1, 3.2); sl.rotateX(.55); sl.translate(x + 1.7, .8, z + 2.1); A.geo('solid', sl, '#2e86c1') }
