/* g2_core.js — טורבו סיטי · ניסוי הגרפיקה 17.11 (gfxlib) · הליבה של הצייר החדש "G2".
   אותה מצלמה של המשחק (C34 / A34 / P34): עולם במטרים, x מזרח, y דרום, z למעלה; מסך = (x·s, (y − K·z)·s), ‏K = 0.6;
   אותה שמש (LD), אותו אור סביבה (AMB .62 + DIF .38), אותו כיוון צל (SUN .25 / .32 לכל מטר גובה).
   מה חדש לעומת הישן: (1) משטחים "חלקים" — נורמל לכל קודקוד, וכל מצולע נצבע במעבר צבע בין הקודקוד הבהיר לכהה (גורו מקורב);
   (2) חומרים: צבע מבריק עם השתקפות שמיים לפי פרנל, הברקה (Blinn‑Phong), זכוכית, גומי, מתכת; (3) צל רך מאוחד + צל מגע (AO);
   (4) מדבקות (פנסים, חלונות, לוחיות) וקווים (תפרי דלתות) על המשטחים, עם מבחן "פונה למצלמה" משלהם.
   בלי תמונות, בלי ספרייה חיצונית: Canvas 2D בלבד, ואפשר גם לפלוט SVG (G2.svg). */
(function (G) {
'use strict';
const K = 0.6, AMB = 0.62, DIF = 0.38, SUN = { x: 0.25, y: 0.32 };
const nrm = v => { const l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / l, v[1] / l, v[2] / l] };
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const crs = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const LD = nrm([-0.42, -0.55, 0.72]);
const VC = nrm([0, K, 1]);                     // the view direction of the cars' / aircraft's camera (toward the viewer)
const HV = nrm([LD[0] + VC[0], LD[1] + VC[1], LD[2] + VC[2]]);
// ---- colours ----
const CC = new Map();
function rgb(h) { let c = CC.get(h); if (c) return c; let s = String(h).trim();
  if (s[0] === '#') { if (s.length === 4) s = '#' + s[1] + s[1] + s[2] + s[2] + s[3] + s[3]; const n = parseInt(s.slice(1, 7), 16); c = [n >> 16 & 255, n >> 8 & 255, n & 255] }
  else { const m = s.match(/[\d.]+/g) || [0, 0, 0]; c = [+m[0], +m[1], +m[2]] }
  CC.set(h, c); return c }
const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const css = (c, a) => { const r = Math.max(0, Math.min(255, Math.round(c[0]))), g = Math.max(0, Math.min(255, Math.round(c[1]))), b = Math.max(0, Math.min(255, Math.round(c[2])));
  return a == null || a >= 1 ? 'rgb(' + r + ',' + g + ',' + b + ')' : 'rgba(' + r + ',' + g + ',' + b + ',' + (+a).toFixed(3) + ')' };
const lum = c => .299 * c[0] + .587 * c[1] + .114 * c[2];
// the sky that a glossy surface reflects (as the game's daylight: a pale horizon, a blue zenith) and the ground below
const SKY_H = [226, 234, 238], SKY_Z = [120, 160, 205], GROUND = [96, 102, 92];
function env(R) { if (R[2] >= 0) { const t = Math.pow(R[2], .55); return mix(SKY_H, SKY_Z, t) } return mix(SKY_H, GROUND, Math.min(1, -R[2] * 3)) }
// ---- materials: c (colour), sp (highlight strength), gl (its exponent), rf (reflection at the grazing angle), f0 (at the normal), a (alpha) ----
const MAT = {
  paint: { sp: .55, gl: 60, rf: .55, f0: .05 },
  metal: { sp: .8, gl: 30, rf: .6, f0: .45 },
  chrome: { sp: 1, gl: 80, rf: .9, f0: .7 },
  glass: { sp: 1, gl: 120, rf: .85, f0: .12 },
  rubber: { sp: .08, gl: 8, rf: .05, f0: .02 },
  plastic: { sp: .2, gl: 20, rf: .12, f0: .03 },
  matte: { sp: .05, gl: 6, rf: .04, f0: .02 },
  lamp: { sp: .9, gl: 90, rf: .6, f0: .2 },
  skin: { sp: .12, gl: 14, rf: .06, f0: .02 },
  cloth: { sp: .03, gl: 4, rf: .03, f0: .01 },
  hair: { sp: .25, gl: 24, rf: .06, f0: .02 },
  leather: { sp: .4, gl: 40, rf: .15, f0: .04 }
};
function shade(col, mk, n, V) {
  const m = MAT[mk] || MAT.matte, b = rgb(col), d = Math.max(0, dot(n, LD)), nv = Math.max(0, dot(n, V));
  let c = [b[0] * (AMB + DIF * d * 1.15), b[1] * (AMB + DIF * d * 1.15), b[2] * (AMB + DIF * d * 1.15)];
  // a little sky from above (the ambient is not flat: the faces turned down are darker — the occlusion of the ground)
  const up = n[2]; c = mix(c, [c[0] * .78, c[1] * .8, c[2] * .86], Math.max(0, -up) * .6);
  if (m.rf > 0) { const R = [2 * nv * n[0] - V[0], 2 * nv * n[1] - V[1], 2 * nv * n[2] - V[2]], f = m.f0 + (1 - m.f0) * Math.pow(1 - nv, 5);
    c = mix(c, env(R), Math.min(1, m.rf * f)) }
  if (m.sp > 0) { const H = nrm([LD[0] + V[0], LD[1] + V[1], LD[2] + V[2]]), s = Math.pow(Math.max(0, dot(n, H)), m.gl) * m.sp * 255;
    c = [c[0] + s, c[1] + s, c[2] + s] }
  return c }
// ---- the geometry: polygons {P: points, N: normals per point (smooth) | null, c, m, bias, two, line, w, a} ----
function polyNormal(P) { let n = [0, 0, 0]; for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length]; n[0] += (a[1] - b[1]) * (a[2] + b[2]); n[1] += (a[2] - b[2]) * (a[0] + b[0]); n[2] += (a[0] - b[0]) * (a[1] + b[1]) } return nrm(n) }
// a lofted surface: rings[i][j] (i along, j around); the normals of the grid; quads; mat(i, j, centre) → [colour, material] or null (a hole)
function loft(rings, mat, o) { o = o || {}; const out = [], NI = rings.length, NJ = rings[0].length, closed = o.closed !== false;
  const nAt = (i, j) => { const i0 = Math.max(0, i - 1), i1 = Math.min(NI - 1, i + 1), j0 = closed ? (j - 1 + NJ) % NJ : Math.max(0, j - 1), j1 = closed ? (j + 1) % NJ : Math.min(NJ - 1, j + 1);
    let n = crs(sub(rings[i1][j], rings[i0][j]), sub(rings[i][j1], rings[i][j0])); if (o.flip) n = [-n[0], -n[1], -n[2]]; return nrm(n) };
  const NN = rings.map((r, i) => r.map((p, j) => nAt(i, j)));
  const JM = closed ? NJ : NJ - 1, RC = rings.map(r => o.center ? o.center(r) : r.reduce((a, p) => [a[0] + p[0] / r.length, a[1] + p[1] / r.length, a[2] + p[2] / r.length], [0, 0, 0]));
  for (let i = 0; i < NI - 1; i++) for (let j = 0; j < JM; j++) { const j1 = (j + 1) % NJ;
    const P = [rings[i][j], rings[i + 1][j], rings[i + 1][j1], rings[i][j1]], N = [NN[i][j], NN[i + 1][j], NN[i + 1][j1], NN[i][j1]];
    const cen = [(P[0][0] + P[2][0]) / 2, (P[0][1] + P[2][1]) / 2, (P[0][2] + P[2][2]) / 2];
    // outward: away from the centre line of the loft (the centres of the two rings); the corner normals agree with the face
    const rc = RC[i], rc1 = RC[i + 1], mc = [(rc[0] + rc1[0]) / 2, (rc[1] + rc1[1]) / 2, (rc[2] + rc1[2]) / 2];
    let n = polyNormal(P); if (dot(n, sub(cen, o.inward ? [2 * cen[0] - mc[0], 2 * cen[1] - mc[1], 2 * cen[2] - mc[2]] : mc)) < 0) { P.reverse(); N.reverse(); n = [-n[0], -n[1], -n[2]] }
    for (let k = 0; k < 4; k++) if (dot(N[k], n) < 0) N[k] = [-N[k][0], -N[k][1], -N[k][2]];
    const mm = mat(i, j, cen, n); if (!mm) continue;
    out.push({ P, N: o.flat ? null : N, c: mm[0], m: mm[1], bias: o.bias || 0, two: o.two, g: o.g }) }
  const cenOf = r => r.reduce((a, p) => [a[0] + p[0] / r.length, a[1] + p[1] / r.length, a[2] + p[2] / r.length], [0, 0, 0]);
  const axis = sub(cenOf(rings[NI - 1]), cenOf(rings[0]));
  const cap = (ring, sign, mm) => { let P = ring.slice(); if (dot(polyNormal(P), axis) * sign < 0) P.reverse(); out.push({ P, N: null, c: mm[0], m: mm[1], bias: o.bias || 0, g: o.g }) };
  if (o.capStart) cap(rings[0], -1, o.capStart);
  if (o.capEnd) cap(rings[NI - 1], 1, o.capEnd);
  return out }
// a box (x0..x1, y0..y1, z0..z1) as six faces
function box(x0, x1, y0, y1, z0, z1, c, m, o) { o = o || {}; const f = [
  [[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], [[x0, y1, z0], [x1, y1, z0], [x1, y0, z0], [x0, y0, z0]],
  [[x0, y1, z0], [x0, y1, z1], [x1, y1, z1], [x1, y1, z0]].reverse(), [[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1]].reverse(),
  [[x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1]], [[x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0]]];
  return f.map(P => ({ P, N: null, c: (o.top && P[0][2] === z1 && P[1][2] === z1 && P[2][2] === z1) ? o.top : c, m, bias: o.bias || 0, g: o.g })) }
// a tapered capsule-like limb between a and b (radii ra, rb), n sides, with round ends (for the people)
function limb(a, b, ra, rb, c, m, n, o) { o = o || {}; n = Math.max(5, Math.round((n || 8) * G2.detail)); const ax = nrm(sub(b, a)); let t = Math.abs(ax[2]) < .9 ? [0, 0, 1] : [1, 0, 0];
  const u = nrm(crs(ax, t)), v = crs(ax, u), L = Math.hypot(...sub(b, a)), rings = [], NR = o.rings || 5;
  for (let k = 0; k <= NR; k++) { const s = k / NR; let r, off;
    // the end caps: a quarter circle at each end (k = 0, NR the poles)
    const e = o.cap === false ? 0 : 1; const tt = s; r = ra + (rb - ra) * tt; off = L * tt;
    if (e && k === 0) { r = ra * .35; off = -ra * .55 } else if (e && k === 1 && NR > 3) { r = ra * .92 + (rb - ra) * tt; off = L * tt - ra * .15 }
    if (e && k === NR) { r = rb * .35; off = L + rb * .55 } else if (e && k === NR - 1 && NR > 3) { r = rb * .92 + (ra - rb) * (1 - tt) * 0 + (ra - rb) * (1 - tt); off = L * tt + rb * .15 }
    const ring = [], sq = o.sq || 1; for (let j = 0; j < n; j++) { const th = j / n * Math.PI * 2, cu = Math.cos(th) * r * sq, sv = Math.sin(th) * r;
      ring.push([a[0] + ax[0] * off + u[0] * cu + v[0] * sv, a[1] + ax[1] * off + u[1] * cu + v[1] * sv, a[2] + ax[2] * off + u[2] * cu + v[2] * sv]) }
    rings.push(ring) }
  return loft(rings, () => [c, m], { g: o.g, bias: o.bias, flip: true }) }
// an ellipsoid (centre, radii, rotation about z) — the heads, the torsos
function ellipsoid(cen, rx, ry, rz, c, m, o) { o = o || {}; const NI = Math.max(3, Math.round((o.ni || 8) * G2.detail)), NJ = Math.max(6, Math.round((o.nj || 12) * G2.detail)), rings = [], rot = o.rot || 0, cr = Math.cos(rot), sr = Math.sin(rot);
  for (let i = 0; i <= NI; i++) { const ph = -Math.PI / 2 + Math.PI * i / NI, cz = Math.sin(ph), cp = Math.cos(ph), ring = [];
    for (let j = 0; j < NJ; j++) { const th = j / NJ * Math.PI * 2; let x = Math.cos(th) * cp * rx, y = Math.sin(th) * cp * ry; const z = cz * rz;
      ring.push([cen[0] + x * cr - y * sr, cen[1] + x * sr + y * cr, cen[2] + z]) }
    rings.push(ring) }
  const f = o.mat || (() => [c, m]); return loft(rings, f, { g: o.g, bias: o.bias }) }
// ---- the scene → a picture ----
function rotZ(p, c, s) { return [p[0] * c - p[1] * s, p[0] * s + p[1] * c, p[2]] }
/* render(polys, heading, s, res, opt) → { cv, ox, oy, ms, n } — heading 0 = east, clockwise on the screen (the game's ctx.rotate);
   s = world px per metre; res = device px per world px; opt.ky — the depth of the body (the people's camera: .4), opt.shadow, opt.ao */
function render(polys, heading, s, res, opt) { opt = opt || {}; const t0 = performance.now(); const c = Math.cos(heading), sn = Math.sin(heading), S = s * res;
  const ky = opt.ky || 1, V = nrm([0, K, ky]);
  const kz = opt.kyz, pr = kz ? p => [p[0] * S, (p[1] * kz(p[2]) - K * p[2]) * S] : p => [p[0] * S, (p[1] * ky - K * p[2]) * S], gy = kz ? 1 : ky;
  const L = [];
  for (const q of polys) { const P = q.P.map(p => rotZ(p, c, sn)); let n = q.line ? null : polyNormal(P);
    let N = q.N ? q.N.map(v => rotZ(v, c, sn)) : null;
    if (q.ln) { const nn = rotZ(q.ln, c, sn); if (dot(nn, V) <= .02) continue; if (n && dot(n, nn) < 0) n = [-n[0], -n[1], -n[2]] }
    let back = false;
    if (!q.ln && n) { let vis = dot(n, V); if (vis <= 1e-4) { if (!q.two) continue; back = true; n = [-n[0], -n[1], -n[2]]; if (N) N = N.map(v => [-v[0], -v[1], -v[2]]); vis = -vis } }
    let d = 0; for (const p of P) d += p[1] * K + p[2] * ky; d = d / P.length + (back && q.bb != null ? q.bb : (q.bias || 0));
    L.push({ q, P, n, N, d, back }) }
  L.sort((a, b) => a.d - b.d);
  // the bounds (the pieces and their shadow)
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; const grow = (X, Y) => { if (X < x0) x0 = X; if (X > x1) x1 = X; if (Y < y0) y0 = Y; if (Y > y1) y1 = Y };
  for (const e of L) for (const p of e.P) { const a = pr(p); grow(a[0], a[1]); if (opt.shadow !== false) grow((p[0] + p[2] * SUN.x) * S, (p[1] + p[2] * SUN.y) * gy * S) }
  const pad = Math.ceil(4 + (opt.ao || 0) * S * .6); x0 = Math.floor(x0) - pad; y0 = Math.floor(y0) - pad; x1 = Math.ceil(x1) + pad; y1 = Math.ceil(y1) + pad;
  const W = Math.max(2, x1 - x0), H = Math.max(2, y1 - y0), cv = mk(W, H); let g = cv.getContext('2d'); g.translate(-x0, -y0); g.lineJoin = 'round';
  // the shadow: every piece flattened on the ground in one picture (no darker overlaps), then at its strength; the contact shadow under it
  if (opt.shadow !== false) { const sc = mk(W, H), h = sc.getContext('2d'); h.translate(-x0, -y0); h.fillStyle = '#000'; h.strokeStyle = '#000'; h.lineWidth = 1; h.lineJoin = 'round'; h.beginPath();
    // the faces turned to the sun, flattened along its rays: they all keep one winding, so one path filled 'nonzero' is their union (one fill)
    const SD = [-SUN.x, -SUN.y, 1]; h.beginPath();
    for (const q of polys) { if (q.noShadow || q.line || q.ln) continue; const P = q.P.map(p => rotZ(p, c, sn)), n = polyNormal(P); let o = dot(n, SD); if (Math.abs(o) < 1e-3) continue;
      const Q = o > 0 ? P : P.slice().reverse(); Q.forEach((p, i) => { const X = (p[0] + p[2] * SUN.x) * S, Y = (p[1] + p[2] * SUN.y) * gy * S; i ? h.lineTo(X, Y) : h.moveTo(X, Y) }); h.closePath() }
    h.fill('nonzero');
    if (opt.ao && opt.foot) { const OFF = 20000; h.save(); h.shadowColor = 'rgba(0,0,0,1)'; h.shadowBlur = opt.ao * S * .5; h.shadowOffsetX = -OFF; h.beginPath();   // only the blur: the shape itself far away
      for (const f of opt.foot) { const P = f.map(p => rotZ([p[0], p[1], 0], c, sn)); P.forEach((p, i) => i ? h.lineTo(p[0] * S + OFF, p[1] * gy * S) : h.moveTo(p[0] * S + OFF, p[1] * gy * S)); h.closePath() }
      h.fill(); h.restore() }
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = opt.shAlpha || .3; g.drawImage(sc, 0, 0); g.restore() }
  // the pieces, back to front, on their own layer (for the rim); a smooth piece — a ramp along the slope of its corner colours
  const g0 = g; let lay = null; if (opt.rim) { lay = mk(W, H); g = lay.getContext('2d'); g.translate(-x0, -y0); g.lineJoin = 'round' }
  for (const e of L) { const q = e.q, P2 = e.P.map(pr);
    if (q.line) { g.strokeStyle = q.c; g.lineWidth = Math.max(.5, (q.w || .02) * S); g.beginPath(); P2.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); if (q.closed) g.closePath(); g.stroke(); continue }
    let fill, a = e.back && q.ba != null ? q.ba : q.a != null ? q.a : (MAT[q.m] && MAT[q.m].a) || 1;
    if (e.N && !opt.flat) { const C = e.N.map(nn => shade(q.c, q.m, nn, V)); fill = ramp(g, P2, C, a) }
    else fill = css(shade(q.c, q.m, e.n, V), a);
    g.fillStyle = fill; g.beginPath(); P2.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); g.fill();
    if (a >= 1 && !q.noSeam) { g.strokeStyle = fill; g.lineWidth = .6; g.stroke() } }
  // a thin dark rim around the figure (as the game's people have): its silhouette, dark, a device pixel around it, under it
  if (lay) { const sil = mk(W, H), sc2 = sil.getContext('2d'); sc2.drawImage(lay, 0, 0); sc2.globalCompositeOperation = 'source-in'; sc2.fillStyle = opt.rimC || 'rgba(18,22,28,.7)'; sc2.fillRect(0, 0, W, H);
    g0.save(); g0.setTransform(1, 0, 0, 1, 0, 0); const r = opt.rim; for (const [dx, dy] of [[r, 0], [-r, 0], [0, r], [0, -r], [r * .7, r * .7], [-r * .7, r * .7], [r * .7, -r * .7], [-r * .7, -r * .7]]) g0.drawImage(sil, dx, dy);
    g0.drawImage(lay, 0, 0); g0.restore(); g = g0 }
  return { cv, ox: -x0, oy: -y0, ms: performance.now() - t0, n: L.length, res } }
function ramp(g, P2, C, a) { const n = P2.length; let mx = 0, my = 0; for (const p of P2) { mx += p[0] / n; my += p[1] / n }
  let sxx = 0, sxy = 0, syy = 0; const Lm = C.map(lum); let ml = 0; for (const l of Lm) ml += l / n; let sxl = 0, syl = 0;
  for (let i = 0; i < n; i++) { const dx = P2[i][0] - mx, dy = P2[i][1] - my, dl = Lm[i] - ml; sxx += dx * dx; sxy += dx * dy; syy += dy * dy; sxl += dx * dl; syl += dy * dl }
  const det = sxx * syy - sxy * sxy; const mc = [0, 0, 0]; for (const c of C) { mc[0] += c[0] / n; mc[1] += c[1] / n; mc[2] += c[2] / n }
  if (Math.abs(det) < 1e-6) return css(mc, a);
  const bx = (sxl * syy - syl * sxy) / det, by = (syl * sxx - sxl * sxy) / det, bl = Math.hypot(bx, by); if (bl < 1e-3) return css(mc, a);
  const ux = bx / bl, uy = by / bl; let t0 = 1e9, t1 = -1e9; for (const p of P2) { const t = (p[0] - mx) * ux + (p[1] - my) * uy; if (t < t0) t0 = t; if (t > t1) t1 = t }
  if (t1 - t0 < .5) return css(mc, a);
  // each channel: its own slope along u (least squares in one variable t)
  const T = P2.map(p => (p[0] - mx) * ux + (p[1] - my) * uy); let st = 0; for (const t of T) st += t * t;
  const at = t => [0, 1, 2].map(k => { let sk = 0; for (let i = 0; i < n; i++) sk += T[i] * (C[i][k] - mc[k]); return mc[k] + sk / (st || 1) * t });
  const gr = g.createLinearGradient(mx + ux * t0, my + uy * t0, mx + ux * t1, my + uy * t1); gr.addColorStop(0, css(at(t0), a)); gr.addColorStop(1, css(at(t1), a)); return gr }
function mk(w, h) { const c = typeof OffscreenCanvas !== 'undefined' && !G2.domCanvas ? new OffscreenCanvas(w, h) : document.createElement('canvas'); c.width = w; c.height = h; return c }
// the same scene as SVG (for the drawing page: plain SVG in code, no pictures) — flat colours per piece
function svg(polys, heading, s, opt) { opt = opt || {}; const c = Math.cos(heading), sn = Math.sin(heading), ky = opt.ky || 1, V = nrm([0, K, ky]), out = [];
  const L = []; for (const q of polys) { const P = q.P.map(p => rotZ(p, c, sn)); let n = q.line ? null : polyNormal(P); if (q.ln) { const nn = rotZ(q.ln, c, sn); if (dot(nn, V) <= .02) continue; if (n && dot(n, nn) < 0) n = [-n[0], -n[1], -n[2]] } else if (n && dot(n, V) <= 1e-4) { if (!q.two) continue; n = [-n[0], -n[1], -n[2]] }
    let d = 0; for (const p of P) d += p[1] * K + p[2] * ky; L.push({ q, P, n, d: d / P.length + (q.bias || 0) }) }
  L.sort((a, b) => a.d - b.d); let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  const dp = s > 30 ? 0 : 1, pts = P => P.map(p => { const X = p[0] * s, Y = (p[1] * ky - K * p[2]) * s; x0 = Math.min(x0, X); x1 = Math.max(x1, X); y0 = Math.min(y0, Y); y1 = Math.max(y1, Y); return X.toFixed(dp) + ',' + Y.toFixed(dp) }).join(' ');
  for (const e of L) { const q = e.q; if (q.line) { out.push('<polyline fill="none" stroke="' + q.c + '" stroke-width="' + ((q.w || .02) * s).toFixed(2) + '" points="' + pts(e.P) + '"/>'); continue }
    const cc = shade(q.c, q.m, e.N ? nrm(e.N.reduce((a, v) => [a[0] + v[0], a[1] + v[1], a[2] + v[2]], [0, 0, 0])) : e.n, V), col = '#' + cc.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');
    out.push('<polygon fill="' + col + '" stroke="' + col + '" points="' + pts(e.P) + '"/>') }
  return { body: out.join(''), box: [x0 - 2, y0 - 2, x1 - x0 + 4, y1 - y0 + 4] } }
// a cache of pictures (as C34.sprite): key → picture, with a byte count
const CACHE = new Map(); let BYTES = 0, MADE = 0, MS = 0;
function cached(key, make) { let e = CACHE.get(key); if (e) return e; e = make(); CACHE.set(key, e); BYTES += e.cv.width * e.cv.height * 4; MADE++; MS += e.ms; return e }
const G2 = G.G2 = { K, LD, VC, SUN, MAT, rgb, css, mix, shade, nrm, dot, sub, crs, loft, box, limb, ellipsoid, polyNormal, render, svg, cached, rotZ,
  stats: () => ({ pictures: CACHE.size, MB: +(BYTES / 1048576).toFixed(2), made: MADE, ms: +MS.toFixed(1), avg: MADE ? +(MS / MADE).toFixed(2) : 0 }),
  clear: () => { CACHE.clear(); BYTES = 0; MADE = 0; MS = 0 }, domCanvas: false, detail: 1 };
})(typeof window !== 'undefined' ? window : globalThis);
