/* g2_plane.js — ניסוי 2: מטוס (צר‑גוף, AC-NB-01 במשחק = Airbus A320ceo עם sharklets) בצייר החדש G2.
   המידות האמיתיות מטבלת המשחק (A34.TYPES): אורך 37.57 מ׳, מוטה 35.80, גובה 11.76, גוף 3.95 × 4.14, מיתר שורש 6.4, קצה 1.5, הסטת חץ 9 מ׳,
   דיהדרל 6°, מנועים ב-34% מהמוטה (CFM56: קוטר 2.2, אורך 4.4), גלגלים ראשיים 1.17 מ׳.
   הגוף — לופט של חתכים אליפטיים (אף אוגיבי שיורד מעט, זנב שעולה); הכנף, הזנב והמייצב — לופט של פרופיל אווירודינמי (NACA 4 ספרות)
   כך שהצד העליון מקבל מעבר אור אמיתי; מנוע — נצל עם שפת כניסה, מאוורר, קונוס פליטה ופילון; כנפונים, מסילות המדפים, אורות הניווט;
   חלונות, חלונות התא, דלתות ופס הצבע — מדבקות על הגוף; כן הנסע — רגליים, בולמים וגלגלים. 16 כיוונים מדויקים — אותו דגם מסובב. */
(function (G) {
'use strict';
const { loft, box, render, cached, nrm } = G.G2;
const LIV = { aurelia: { b: '#f4f6f8', u: '#d9dde2', s: '#1f5aa6', t: '#1f5aa6', m: '#f2c230', w: '#c3cad1' } };
const T = { 'AC-NB-01': { L: 37.57, WS: 35.8, fw: 3.95, fh: 4.14, wc: 6.4, tc: 1.5, sw: 9, nl: .1, tl: .22, zb: 1.65, H: 11.76, dih: 6, eng: .34, ed: 2.2, el: 4.4,
  win: [.17, .84, 28], doors: [.116, .88], wing: [.45, .62], winglet: 2.2, tire: [.585, .38], ntire: [.38, .25], liv: 'aurelia' } };
// NACA 00xx half thickness at u (0 … 1 of the chord)
const nt = (u, t) => 5 * t * (.2969 * Math.sqrt(u) - .126 * u - .3516 * u * u + .2843 * u * u * u - .1036 * u * u * u * u);
const US = [0, .012, .04, .09, .17, .28, .42, .58, .74, .88, 1];
// an airfoil ring at a station: le (the leading edge point), chord, thickness ratio, the chord's direction (−x), the thickness axis
function foil(le, c, t, up, camber) { const ring = [];
  for (let i = US.length - 1; i >= 0; i--) { const u = US[i], h = nt(u, t) * c, cb = (camber || 0) * c * 4 * u * (1 - u); ring.push([le[0] - u * c, le[1] + up[1] * (h + cb), le[2] + up[2] * (h + cb)]) }
  for (let i = 1; i < US.length - 1; i++) { const u = US[i], h = nt(u, t) * c, cb = (camber || 0) * c * 4 * u * (1 - u); ring.push([le[0] - u * c, le[1] - up[1] * (h - cb), le[2] - up[2] * (h - cb)]) }
  return ring }
function model(id) { const D = T[id] || T['AC-NB-01']; if (D.__m) return D.__m; const C = LIV[D.liv];
  const L = D.L, XN = L / 2, XT = -L / 2, ry = D.fw / 2, rz = D.fh / 2, Z0 = D.zb + rz, nl = D.nl * L, tl = D.tl * L, polys = [];
  // ---- the fuselage ----
  const sc = x => { if (x > XN - nl) { const t = (x - (XN - nl)) / nl; return Math.pow(Math.max(0, 1 - Math.pow(t, 2.1)), .5) }
    if (x < XT + tl) { const t = (XT + tl - x) / tl; return 1 - .84 * Math.pow(t, 1.45) } return 1 };
  const zc = x => { let z = Z0; if (x > XN - nl) { const t = (x - (XN - nl)) / nl; z -= .42 * rz * t * t } if (x < XT + tl) { const t = (XT + tl - x) / tl; z += .78 * rz * Math.pow(t, 1.35) } return z };
  const XS = []; for (let i = 0; i <= 64; i++) { const t = i / 64; XS.push(XT + L * (t - Math.sin(2 * Math.PI * t) / (2 * Math.PI) * .5)) }
  const NJ = 36, rings = XS.map((x, i) => { const s = Math.max(i === XS.length - 1 ? 0.002 : .03, sc(x)), ring = []; for (let j = 0; j < NJ; j++) { const a = j / NJ * Math.PI * 2; ring.push([x, Math.cos(a) * ry * s, zc(x) + Math.sin(a) * rz * s * (Math.sin(a) < 0 ? .96 : 1)]) } return ring });
  const fin0 = XT + .9, fin1 = XT + 6.8;
  polys.push(...loft(rings, (i, j, c) => { const x = c[0], s = Math.max(.03, sc(x)), zr = (c[2] - zc(x)) / (rz * s);
    if (x < XT + .35) return ['#3a3f46', 'metal'];                                        // the APU exhaust
    if (zr < -.52) return [C.u, 'paint'];                                                // the belly
    if (zr > -.4 && zr < -.16 && x < XN - 2.6 && x > XT + 4) return [C.s, 'paint'];                   // the cheat line
    if (x < XT + 5.5 && zr > .25) return [C.t, 'paint'];                                // the tail colour runs onto the fuselage under the fin
    return [C.b, 'paint'] }, { capStart: ['#2b3036', 'metal'], center: r => [r[0][0], 0, zc(r[0][0])] }));
  // ---- the wings (low, swept, dihedral; inner trailing edge straight to the kink) ----
  const b = D.WS / 2, yr = ry * .8, ykink = b * D.eng, xle0 = 3.0, zr0 = Z0 - .62 * rz, dz = Math.tan(D.dih * Math.PI / 180);
  const leX = y => xle0 - D.sw * (y - yr) / (b - yr), teX = y => y < ykink ? -3.4 - .25 * (y - yr) / (ykink - yr) : -3.65 + ((leX(b) - D.tc) - (-3.65)) * (y - ykink) / (b - ykink);
  const wz = y => zr0 + (y - yr) * dz;
  for (const s of [1, -1]) { const ST = []; for (let k = 0; k <= 12; k++) ST.push(yr + (b - yr) * k / 12); ST.push(ykink); ST.sort((p, q) => p - q);
    const wr = ST.map(y => { const c = leX(y) - teX(y), t = .15 - .045 * (y - yr) / (b - yr); return foil([leX(y), s * y, wz(y)], c, t, [0, 0, 1], .02) });
    polys.push(...loft(wr, (i, j, c, n) => [n[2] > .2 ? C.w : '#b9c0c7', n[2] > .2 ? 'paint' : 'matte'], { capEnd: [C.w, 'paint'], center: r => { const x = r.reduce((a, p) => a + p[0], 0) / r.length; return [x, r[0][1], r.reduce((a, p) => a + p[2], 0) / r.length] } }));
    // the sharklet: a blended fin up from the tip
    const tip = [leX(b), s * b, wz(b)], wl = [];
    for (let k = 0; k <= 4; k++) { const u = k / 4, h = D.winglet * u, c = D.tc * (1 - .72 * u), out = .25 * u * u; wl.push(foil([tip[0] - .35 * u - .9 * u * u, s * (b + out), tip[2] + .05 + h], c, .1, [0, s, 0])) }
    polys.push(...loft(wl, () => [C.t, 'paint'], { capEnd: [C.t, 'paint'], center: r => [r.reduce((a, p) => a + p[0], 0) / r.length, s * (b + .2), r[0][2]] }));
    // the nav light (red to port — the left, green to starboard)
    polys.push(...box(tip[0] - .2, tip[0] + .05, s * b - .06, s * b + .06, tip[2] + .02, tip[2] + .14, s > 0 ? '#2fd06a' : '#e0353a', 'lamp').map(q => Object.assign(q, { bias: .05 })));
    // the flap track fairings (canoes) under the wing
    for (const f of [.42, .62, .8]) { const y = yr + (b - yr) * f, x0 = teX(y) + .4, x1 = teX(y) - 1.4, zz = wz(y) - .08, cr = [];
      for (let k = 0; k <= 6; k++) { const u = k / 6, x = x0 + (x1 - x0) * u, rr = .22 * Math.sin(Math.PI * Math.min(1, u * 1.15 + .02)) + .01, ring = []; for (let j = 0; j < 8; j++) { const a = j / 8 * Math.PI * 2; ring.push([x, s * y + Math.cos(a) * rr * .7, zz - .1 + Math.sin(a) * rr]) } cr.push(ring) }
      polys.push(...loft(cr, () => ['#c3c9cf', 'paint'], {})) }
    // ---- the engine: the nacelle, the lip, the fan, the exhaust cone, the pylon ----
    const ye = s * ykink, xf = leX(ykink) + 2.75, xe = xf - D.el, ze = wz(ykink) - .2 - D.ed * .62, R = D.ed / 2, nr = [];
    const NP = [[0, .9], [.02, .99], [.08, 1.04], [.3, 1.0], [.6, .92], [.85, .8], [1, .66]];
    for (const [u, f] of NP) { const ring = []; for (let j = 0; j < 20; j++) { const a = j / 20 * Math.PI * 2; ring.push([xf - u * D.el, ye + Math.cos(a) * R * f, ze + Math.sin(a) * R * f * (Math.sin(a) < 0 ? .92 : 1)]) } nr.push(ring) }
    polys.push(...loft(nr, (i, j, c) => [i === 0 ? '#c7cdd3' : C.b, i === 0 ? 'metal' : 'paint'], { center: r => [r[0][0], ye, ze] }));
    { const fan = []; for (let j = 0; j < 20; j++) { const a = j / 20 * Math.PI * 2; fan.push([xf - .05, ye + Math.cos(a) * R * .86, ze + Math.sin(a) * R * .86]) } polys.push({ P: fan, N: null, c: '#20252b', m: 'metal', ln: [1, 0, 0], bias: .02 });
      const sp = []; for (let j = 0; j < 12; j++) { const a = j / 12 * Math.PI * 2; sp.push([xf - .03, ye + Math.cos(a) * R * .26, ze + Math.sin(a) * R * .26]) } polys.push({ P: sp, N: null, c: '#d8dde2', m: 'chrome', ln: [1, 0, 0], bias: .04 });
      const cone = []; for (const [u, f] of [[0, .5], [.5, .32], [1, .04]]) { const ring = []; for (let j = 0; j < 14; j++) { const a = j / 14 * Math.PI * 2; ring.push([xe - u * 1.1, ye + Math.cos(a) * R * f, ze + Math.sin(a) * R * f]) } cone.push(ring) }
      polys.push(...loft(cone, () => ['#6b7178', 'metal'], { center: r => [r[0][0], ye, ze] })) }
    polys.push(...box(xe + .3, xf - 1.0, ye - .18, ye + .18, ze + R * .85, wz(ykink) + .05, C.b, 'paint').map(q => Object.assign(q, { bias: .01 })));
    // ---- the horizontal stabiliser ----
    const hb = 6.2, hle0 = XT + 6.2, hz0 = zc(XT + 4.4) - .25, hs = [];
    for (let k = 0; k <= 5; k++) { const u = k / 5, y = .5 + (hb - .5) * u, c = 3.7 - 2.4 * u; hs.push(foil([hle0 - 3.6 * u, s * y, hz0 + (y - .5) * dz], c, .1, [0, 0, 1])) }
    polys.push(...loft(hs, (i, j, c, n) => [n[2] > .2 ? C.w : '#b9c0c7', 'paint'], { capEnd: [C.w, 'paint'], center: r => [r.reduce((a, p) => a + p[0], 0) / r.length, r[0][1], r[0][2]] }));
    // ---- the windows, the doors ----
    const [w0, w1, nw] = D.win, phi = .2, cy = Math.cos(phi), sz = Math.sin(phi);
    for (let k = 0; k < nw; k++) { const xw = XN - L * (w0 + (w1 - w0) * k / (nw - 1)); if (Math.abs(xw - (xle0 - 3.6)) < .45) continue; const hw = .12, hh = .17, y = s * (ry * cy + .015), z = zc(xw) + rz * sz;
      polys.push({ P: [[xw + hw, y, z - hh], [xw - hw, y, z - hh], [xw - hw, y, z + hh], [xw + hw, y, z + hh]], N: null, c: '#1b2633', m: 'glass', a: 1, ln: [0, s * cy, sz], bias: .3 }) }
    for (const fd of D.doors) { const xd = XN - L * fd, y = s * (ry + .012), z0 = zc(xd) - .35, z1 = z0 + 1.85;
      polys.push({ P: [[xd + .41, y, z0], [xd - .41, y, z0], [xd - .41, y, z1], [xd + .41, y, z1], [xd + .41, y, z0]], line: 1, c: 'rgba(40,50,60,.6)', w: .04, ln: [0, s, 0], bias: .06 });
      polys.push({ P: [[xd + .3, y, z0 + 1.1], [xd + .12, y, z0 + 1.1], [xd + .12, y, z0 + 1.3], [xd + .3, y, z0 + 1.3]], N: null, c: '#1b2633', m: 'glass', a: 1, ln: [0, s, 0], bias: .06 }) }
    // the cockpit windows: three panes a side on the surface of the nose (x, the angle from the top φ), the dark glass and its frame
    const fz = (x, ph) => { const k = Math.max(.03, sc(x)); return [x, s * Math.sin(ph) * ry * k * 1.012, zc(x) + Math.cos(ph) * rz * k * 1.012] };
    { const xa = XN - 3.5, xb = XN - 1.95, lo = u => 1.1 - .5 * u, up = u => .8 - .74 * u, B = [];   // one band from the rear pane (u = 0) to the front pane (u = 1)
      for (let k = 0; k <= 8; k++) B.push(fz(xa + (xb - xa) * k / 8, lo(k / 8))); for (let k = 8; k >= 0; k--) B.push(fz(xa + (xb - xa) * k / 8, up(k / 8)));
      const nn = [.45, s * .75, .5]; polys.push({ P: B, N: null, c: '#121a24', m: 'glass', a: 1, ln: nn, bias: .3, two: true });
      polys.push({ P: B.concat([B[0]]), line: 1, c: '#2c3138', w: .07, ln: nn, bias: .31 });
      for (const u of [.33, .66]) { const x = xa + (xb - xa) * u; polys.push({ P: [fz(x, lo(u)), fz(x, up(u))], line: 1, c: '#2c3138', w: .09, ln: nn, bias: .31 }) } }
  }
  // ---- the fin, with the accent band ----
  { const fr = [], ztop = x => zc(x) + rz * Math.max(.03, sc(x)) - .05;
    for (let k = 0; k <= 6; k++) { const u = k / 6, c = 5.9 - 4.0 * u, h = (D.H - (Z0 + rz)) * u, x = fin1 - 4.6 * u; fr.push(foil([x, 0, ztop(x - c / 2) + h], c, .11, [0, 1, 0])) }
    polys.push(...loft(fr, (i, j, c) => [i === 1 || i === 2 ? (c[2] > ztop(c[0]) + 1.5 && c[2] < ztop(c[0]) + 2.1 ? C.m : C.t) : C.t, 'paint'], { capEnd: [C.t, 'paint'], center: r => [r.reduce((a, p) => a + p[0], 0) / r.length, 0, r[0][2]] })) }
  // ---- the gear: the nose leg (two tyres), the main legs (two tyres each) ----
  const tyre = (x, y, z, r, w) => { const N = 16, out = [], rr = [[-w / 2, r * .55], [-w / 2, r * .9], [-w / 2 + .05, r], [w / 2 - .05, r], [w / 2, r * .9], [w / 2, r * .55]].map(([dy, rad]) => { const ring = []; for (let j = 0; j < N; j++) { const a = j / N * Math.PI * 2; ring.push([x + Math.cos(a) * rad, y + dy, z + Math.sin(a) * rad]) } return ring });
    out.push(...loft(rr, () => ['#1a1c1f', 'rubber'], { center: r0 => [x, r0[0][1], z] }));
    for (const s of [1, -1]) { const P = []; for (let j = 0; j < N; j++) { const a = j / N * Math.PI * 2; P.push([x + Math.cos(a) * r * .55, y + s * (w / 2 + .005), z + Math.sin(a) * r * .55]) } out.push({ P, N: null, c: '#aeb5bc', m: 'metal', ln: [0, s, 0], bias: .01 }) }
    return out };
  const xn = XN - 5.1, [nr0, nw0] = D.ntire;
  polys.push(...box(xn - .09, xn + .09, -.09, .09, nr0, D.zb + .1, '#c9ced3', 'metal'));
  for (const s of [1, -1]) polys.push(...tyre(xn, s * .2, nr0, nr0, nw0));
  const xm = xle0 - 4.6, [mr, mw] = D.tire;
  for (const s of [1, -1]) { const y = s * 3.8; polys.push(...box(xm - .13, xm + .13, y - .13, y + .13, mr, wz(3.8) - .1, '#c9ced3', 'metal'));
    for (const o of [-.27, .27]) polys.push(...tyre(xm, y + o, mr, mr, mw)) }
  // the beacons
  polys.push(...box(-1, -.6, -.15, .15, Z0 + rz - .02, Z0 + rz + .12, '#e0353a', 'lamp').map(q => Object.assign(q, { bias: .05 })));
  const foot = [[[XT + 4, -ry], [XN - 3, -ry], [XN - 3, ry], [XT + 4, ry]], [[leX(yr), -b * .7], [leX(yr) + 1, -yr], [teX(yr), -yr], [teX(b * .7), -b * .7]], [[leX(yr), b * .7], [leX(yr) + 1, yr], [teX(yr), yr], [teX(b * .7), b * .7]]];
  D.__m = { D, polys, foot }; return D.__m }
// heading: radians, 0 = east (the nose to the east), clockwise; s — world px per metre (the field: 7.47); res — device px per world px
function sprite(id, heading, s, res, dirs) { const N = dirs || 16, k = ((Math.round(heading / (Math.PI * 2) * N) % N) + N) % N, h = k / N * Math.PI * 2;
  return cached('ac|' + id + '|' + N + '|' + k + '|' + s + '|' + res, () => { const m = model(id); const e = render(m.polys, h, s, res, { ao: 1.4, foot: m.foot, shAlpha: .26 }); e.k = k; return e }) }
G.G2.plane = { T, LIV, model, sprite };
})(typeof window !== 'undefined' ? window : globalThis);
