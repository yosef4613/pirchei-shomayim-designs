/* g2_car.js — ניסוי 1: מכונית פרטית (סדאן, כמו VH-SD-02 במשחק) בצייר החדש G2.
   מידות אמיתיות של סדאן בינונית: אורך 4.85 מ׳, רוחב 1.84, גובה 1.45, בסיס גלגלים 2.83, שלוחה קדמית 0.95, גלגל 0.335 (225/45 R17).
   הגוף — "לופט" (חתכים לאורך הרכב, כל חתך סופר‑אליפסה) עם קשתות גלגלים אמיתיות; תא הנוסעים — לופט פתוח עם שיפוע צד (tumblehome);
   החלונות, העמודים והגג — לפי הנורמל של כל משטח; פנסים, גריל, לוחיות צהובות, ידיות, מראות, תפרי דלתות — מדבקות על המשטח;
   גלגלים — צמיג עם דופן ופסי מגע, חישוק 5 חישורים כפולים, טבור. 16 כיוונים מדויקים — אותו דגם תלת־ממדי מסובב, לא ציור לכל כיוון. */
(function (G) {
'use strict';
const { loft, box, render, cached } = G.G2;
// a smooth curve through keyframes [x, v] (Catmull–Rom, clamped)
function curve(K) { return x => { if (x <= K[0][0]) return K[0][1]; if (x >= K[K.length - 1][0]) return K[K.length - 1][1];
  let i = 0; while (x > K[i + 1][0]) i++; const p0 = K[Math.max(0, i - 1)], p1 = K[i], p2 = K[i + 1], p3 = K[Math.min(K.length - 1, i + 2)], t = (x - p1[0]) / (p2[0] - p1[0]);
  const m1 = (p2[1] - p0[1]) / (p2[0] - p0[0]) * (p2[0] - p1[0]), m2 = (p3[1] - p1[1]) / (p3[0] - p1[0]) * (p2[0] - p1[0]), t2 = t * t, t3 = t2 * t;
  return (2 * t3 - 3 * t2 + 1) * p1[1] + (t3 - 2 * t2 + t) * m1 + (-2 * t3 + 3 * t2) * p2[1] + (t3 - t2) * m2 } }
const SPEC = {
  'VH-SD-02': { name: 'סדאן', L: 4.85, W: 1.84, H: 1.45, wb: 2.83, fo: .95, r: .335, tw: .225, track: 1.58, rim: .225,
    zt: [[-2.425, .80], [-2.39, .93], [-2.25, 1.0], [-1.6, 1.025], [-1.0, 1.0], [.7, .985], [1.3, .94], [2.0, .865], [2.32, .80], [2.425, .64]],
    zb: [[-2.425, .40], [-2.36, .26], [-2.1, .21], [2.1, .21], [2.36, .27], [2.425, .40]],
    roof: [[-1.5, 1.0], [-1.32, 1.17], [-1.0, 1.38], [-.62, 1.45], [.02, 1.45], [.3, 1.37], [.5, 1.22], [.76, 1.0]],
    hwF: .78, hwR: .84, belt: [-1.5, .76], glass: [-1.08, .46], bpil: [-.33, -.25], doors: [.66, -.37, -1.36] }
};
// lod 1 — the full mesh (close-ups), 0 — about a third of the pieces (a car under ~120 device px long: the game's zooms)
function model(id, lod) { const D = SPEC[id] || SPEC['VH-SD-02'], LK = '__m' + (lod === 0 ? 0 : 1); if (D[LK]) return D[LK]; const Q = n => lod === 0 ? Math.max(4, Math.round(n * .45)) : n;
  const { L, W, r } = D, X0 = -L / 2, X1 = L / 2, xf = X1 - D.fo, xr = xf - D.wb, zt = curve(D.zt), zb0 = curve(D.zb), roof = curve(D.roof), ra = r + .075;
  const zb = x => { let z = zb0(x); for (const xa of [xf, xr]) { const d = x - xa; if (Math.abs(d) < ra) z = Math.max(z, r - .01 + Math.sqrt(ra * ra - d * d)) } return z };
  const hw = x => { let h = W / 2; if (x > 1.85) { const t = (x - 1.85) / (X1 - 1.85); h *= 1 - (1 - D.hwF / (W / 2) * 1) * Math.pow(t, 2.4) }
    if (x < -1.95) { const t = (-1.95 - x) / (-1.95 - X0); h *= 1 - (1 - D.hwR / (W / 2)) * Math.pow(t, 2.6) } return h };
  // the stations along the body: dense at the ends and over the wheel arches
  const XS = []; const NS = Q(56); for (let i = 0; i <= NS; i++) { const t = i / NS; XS.push(X0 + L * (t - Math.sin(2 * Math.PI * t) / (2 * Math.PI) * .55)) }
  for (const xa of [xf, xr]) { const NA = lod === 0 ? 3 : 6; for (let k = -NA; k <= NA; k++) XS.push(xa + k / NA * ra * .98) }
  XS.sort((a, b) => a - b); const XU = XS.filter((x, i) => i === 0 || x - XS[i - 1] > .012);
  const M = Q(28), p = 4.2, rings = XU.map(x => { const h = hw(x), z0 = zb(x), z1 = zt(x), zc = (z0 + z1) / 2, hz = (z1 - z0) / 2, ring = [];
    for (let j = 0; j < M; j++) { const th = j / M * Math.PI * 2, c = Math.cos(th), s = Math.sin(th);
      // the upper half a little rounder (the shoulder), the lower half flatter (the sill)
      const pp = s > 0 ? p + 2.2 : p + 1.2; ring.push([x, h * Math.sign(c) * Math.pow(Math.abs(c), 2 / pp), zc + hz * Math.sign(s) * Math.pow(Math.abs(s), 2 / pp)]) }
    return ring });
  const surfY = (x, z) => { const z0 = zb(x), z1 = zt(x), zc = (z0 + z1) / 2, hz = (z1 - z0) / 2, t = Math.min(1, Math.abs((z - zc) / hz)), pp = z > zc ? p + 2.2 : p + 1.2; return hw(x) * Math.pow(Math.max(0, 1 - Math.pow(t, pp)), 1 / pp) };
  const paint = '__PAINT__', polys = [];
  polys.push(...loft(rings, (i, j, c, n) => {
    if (n[2] < -.55) return ['#1b1e22', 'matte'];                                  // the underbody
    if (c[2] < zb(c[0]) + .085 && Math.abs(n[1]) > .3) return ['#2a2e33', 'plastic'];   // the sills
    if ((c[0] > X1 - .09 || c[0] < X0 + .09) && c[2] < .42) return ['#24282d', 'plastic'];   // the lower bumpers
    return [paint, 'paint'] }, { capStart: ['#2a2e33', 'plastic'], capEnd: ['#2a2e33', 'plastic'] }));
  // the glass house: an open loft from belt to belt (the tumblehome toward the roof), all of it painted; the glass — panels laid on it
  const zbelt = x => zt(x) + .005, hwb = x => hw(x) - .06, hwr = x => hw(x) - .25;
  const ghp = (x, a) => { const zr = Math.max(zbelt(x) + .002, roof(x)), ca = Math.cos(a), sa = Math.max(0, Math.sin(a)), w = Math.pow(sa, 1.6);
    return [x, ca * (hwb(x) + (hwr(x) - hwb(x)) * w), zbelt(x) + (zr - zbelt(x)) * Math.pow(sa, .32)] };
  const GN = Q(64), MG = Q(37) | 1, AJ = j => Math.PI * (1 - j / (MG - 1));
  // the panes, over the parameters (x, a) of the glass house: [x from, x to (both by a), a from, a to]
  const eA = a => (Math.abs(Math.cos(a)) - Math.cos(.42)) / (Math.cos(.07) - Math.cos(.42));   // 1 at the belt, 0 at the top of the side glass
  const PANES = [[() => .17, a => .735 - .02 * Math.abs(Math.cos(a)), .5, Math.PI - .5], [() => -1.45, () => -1.02, .52, Math.PI - .52]];
  for (const [a0, a1] of [[.07, .42], [Math.PI - .42, Math.PI - .07]]) PANES.push([() => -.235, a => .30 + .3 * eA(a), a0, a1], [a => -.98 - .2 * eA(a), () => -.34, a0, a1]);
  const inPane = (x, a) => PANES.some(([xl, xr, a0, a1]) => a >= a0 && a <= a1 && x >= xl(a) && x <= xr(a));
  const XG = i => D.belt[0] + (D.belt[1] - D.belt[0]) * i / GN;
  const grings = []; for (let i = 0; i <= GN; i++) { const x = XG(i), ring = []; for (let j = 0; j < MG; j++) ring.push(ghp(x, AJ(j))); grings.push(ring) }
  const gc = r => [r[0][0], 0, zbelt(r[0][0]) - .3];
  polys.push(...loft(grings, (i, j) => j === 0 || j === MG - 2 ? ['#15181b', 'plastic'] : [paint, 'paint'], { closed: false, center: gc }));
  // a glass panel over the parameters (x, a) of the glass house: x between xl(a) and xr(a), a from a0 to a1; 8 mm outward
  // a pane: a fine grid over its parameters, 8 mm out, opaque (the reflection of the sky makes it read as glass); a black frit band around it
  const panel = (xl, xr, a0, a1, col) => { const pt = (x, a) => { const p = ghp(x, a), d = G.G2.nrm(G.G2.sub(p, [x, 0, zbelt(x) - .3])); return [p[0] + d[0] * .008, p[1] + d[1] * .008, p[2] + d[2] * .008] };
    const NU = Q(12), NV = Q(8), rows = []; for (let i = 0; i <= NU; i++) { const u = i / NU, row = []; for (let j = 0; j <= NV; j++) { const a = a0 + (a1 - a0) * j / NV; row.push(pt(xl(a) + (xr(a) - xl(a)) * u, a)) } rows.push(row) }
    const B = []; for (let i = 0; i <= NU; i++) B.push(rows[i][0]); for (let j = 1; j <= NV; j++) B.push(rows[NU][j]); for (let i = NU - 1; i >= 0; i--) B.push(rows[i][NV]); for (let j = NV - 1; j >= 0; j--) B.push(rows[0][j]);
    const mid = rows[NU >> 1][NV >> 1], n2 = G.G2.nrm(G.G2.sub(mid, [mid[0], 0, zbelt(mid[0]) - .3]));
    return [...loft(rows, () => [col, 'glass'], { closed: false, center: gc, bias: .2 }), { P: B, line: 1, c: '#0e1013', w: .05, bias: .21, ln: n2 }] };
  for (const [xl, xr, a0, a1] of PANES) polys.push(...panel(xl, xr, a0, a1, '#18232e'));
  // the details on the surfaces (each with its own facing test: ln — its outward normal)
  const dec = (P, c, m, ln, bias) => polys.push({ P, N: null, c, m, bias: bias == null ? .06 : bias, ln, two: false, dec: 1 });
  const ln = (P, c, w, nrm) => polys.push({ P, line: 1, c, w, ln: nrm, bias: .07 });
  for (const s of [1, -1]) {
    // headlamps (on the turn from the hood to the face) and the tail lamps (wrapping around the rear corners)
    const hz = zt(X1 - .1);
    dec([[X1 - .015, s * .40, hz - .05], [X1 - .015, s * .70, hz - .02], [X1 - .1, s * .80, zt(X1 - .1) + .02], [X1 - .2, s * .78, zt(X1 - .2) + .012], [X1 - .07, s * .42, hz + .01]].map(q => s > 0 ? q : q).sort(() => 0), '#e9eef2', 'lamp', [1, s * .3, .4]);
    dec([[X1 - .012, s * .46, hz - .045], [X1 - .012, s * .66, hz - .025], [X1 - .06, s * .70, hz], [X1 - .06, s * .48, hz - .01]], '#9fb3c6', 'chrome', [1, 0, .3], .07);
    const tz = zt(X0 + .05);
    for (const yy of [.5, .6]) { const P = []; for (let k = 0; k < 10; k++) { const t = k / 10 * Math.PI * 2; P.push([X1 - .04, s * (yy + Math.cos(t) * .035), hz - .025 + Math.sin(t) * .02]) } dec(s > 0 ? P : P.reverse(), '#ffffff', 'chrome', [1, 0, .3], .09) }
    dec([[X0 + .006, s * .48, tz - .12], [X0 + .006, s * .80, tz - .10], [X0 + .006, s * .80, tz - .02], [X0 + .006, s * .48, tz - .03]], '#b3141c', 'lamp', [-1, 0, 0]);
    dec([[X0 + .03, s * .83, tz - .1], [X0 + .2, s * .9, tz - .06], [X0 + .2, s * .9, tz - .01], [X0 + .03, s * .83, tz - .02]], '#b3141c', 'lamp', [0, s, 0]);
    // the mirrors: on the door at the base of the A pillar — a stalk, a housing in the paint, the glass toward the back
    { const xm = D.belt[1] - .2, zm = zbelt(xm) + .03, yb = hwb(xm) - .01, y1 = yb + .17, Y = (u, v) => [Math.min(s * u, s * v), Math.max(s * u, s * v)];
      polys.push(...box(xm - .05, xm + .02, ...Y(yb, yb + .07), zm, zm + .04, '#15181b', 'plastic'));
      polys.push(...box(xm - .08, xm + .04, ...Y(yb + .06, y1), zm + .01, zm + .11, paint, 'paint', { top: paint }).map(q => Object.assign(q, { bias: .02 })));
      dec([[xm - .082, s * (yb + .075), zm + .02], [xm - .082, s * (y1 - .01), zm + .02], [xm - .082, s * (y1 - .01), zm + .1], [xm - .082, s * (yb + .075), zm + .1]], '#2c3a48', 'glass', [-1, 0, 0]) }
    // the arch liners (dark, behind the tyres)
    for (const xa of [xf, xr]) { const P = []; for (let k = 0; k <= 12; k++) { const t = Math.PI * k / 12; P.push([xa + Math.cos(t) * ra, s * (hw(xa) - .14), r + Math.sin(t) * ra]) } P.push([xa - ra, s * (hw(xa) - .14), .12], [xa + ra, s * (hw(xa) - .14), .12]);
      polys.push({ P: s > 0 ? P.slice().reverse() : P, N: null, c: '#0d0f11', m: 'matte', ln: [0, s, 0], bias: -.45, noShadow: 1 }) }
    // the door seams, the handles
    for (const xd of D.doors) { const zz = []; for (let k = 0; k <= 6; k++) { const z = zb(xd) + .05 + (zt(xd) - zb(xd) - .06) * k / 6; zz.push([xd, s * (surfY(xd, z) + .006), z]) } ln(zz, 'rgba(10,14,20,.55)', .012, [0, s, 0]) }
    
    for (const xh of [.12, -.86]) dec([[xh, s * (surfY(xh, .86) + .012), .86], [xh - .16, s * (surfY(xh, .86) + .012), .86], [xh - .16, s * (surfY(xh, .9) + .012), .9], [xh, s * (surfY(xh, .9) + .012), .9]], '#c9d0d6', 'chrome', [0, s, 0])
    // the side repeater, the shoulder line (a light crease)
    { const cl = []; for (let k = 0; k <= 20; k++) { const x = 1.9 - 4 * k / 20, z = zt(x) - .1; cl.push([x, s * (surfY(x, z) + .004), z]) } ln(cl, 'rgba(255,255,255,.22)', .012, [0, s, .3]) }
  }
  // the grille, the intake and the plates (yellow, as in the country) on the front and the rear
  dec([[X1 + .005, -.42, .55], [X1 + .005, .42, .55], [X1 + .005, .36, .635], [X1 + .005, -.36, .635]], '#14171a', 'plastic', [1, 0, 0]);
  ln([[X1 + .008, -.42, .55], [X1 + .008, .42, .55], [X1 + .008, .36, .635], [X1 + .008, -.36, .635], [X1 + .008, -.42, .55]], '#c9d0d6', .018, [1, 0, 0]);
  for (const zz of [.578, .606]) ln([[X1 + .008, -.37, zz], [X1 + .008, .37, zz]], '#5d656e', .012, [1, 0, 0]);
  ln([[X1 + .008, -.55, .34], [X1 + .008, .55, .34]], '#14171a', .05, [1, 0, 0]);
  dec([[X1 + .006, -.26, .40], [X1 + .006, .26, .40], [X1 + .006, .26, .51], [X1 + .006, -.26, .51]], '#f2c51c', 'plastic', [1, 0, 0], .08);
  dec([[X0 - .006, .26, .55], [X0 - .006, -.26, .55], [X0 - .006, -.26, .66], [X0 - .006, .26, .66]], '#f2c51c', 'plastic', [-1, 0, 0], .08);
  { const tz = zt(X0 + .05); ln([[X0 - .008, -.5, tz - .07], [X0 - .008, .5, tz - .07]], '#c01d25', .03, [-1, 0, 0]); ln([[X0 - .008, -.62, .42], [X0 - .008, .62, .42]], '#15181b', .05, [-1, 0, 0]) }
  // the wheels: the tyre (tread, shoulders, sidewalls), the rim, the hub — a ring loft about the axle
  const wheels = [];
  for (const xa of [xf, xr]) for (const s of [1, -1]) wheels.push(...wheel(xa, s * D.track / 2, s, r, D.tw, D.rim, lod === 0 ? 14 : 22));
  polys.push(...wheels);
  // the footprint for the contact shadow
  const foot = [[[X0 + .15, -W / 2 + .1], [X1 - .15, -W / 2 + .1], [X1 - .15, W / 2 - .1], [X0 + .15, W / 2 - .1]]];
  D[LK] = { D, polys, foot }; return D[LK] }
function wheel(xc, yc, s, r, tw, rr, NW) { const out = [], N = NW || 22, prof = [[-tw / 2, rr * .98], [-tw / 2, r * .86], [-tw / 2 + .02, r * .98], [-tw / 2 + .05, r], [tw / 2 - .05, r], [tw / 2 - .02, r * .98], [tw / 2, r * .86], [tw / 2, rr * .98]];
  const rings = prof.map(([dy, rad]) => { const ring = []; for (let j = 0; j < N; j++) { const a = j / N * Math.PI * 2; ring.push([xc + Math.cos(a) * rad, yc + s * dy, r + Math.sin(a) * rad]) } return ring });
  out.push(...loft(rings, (i, j, c, n) => [i === 3 ? '#222529' : '#17191c', 'rubber'], { center: rg => [xc, rg[0][1], r] }));
  // the rim on the outer face: the dish, five double spokes, the hub
  const yo = yc + s * (tw / 2 + .002), disc = (rad, k0, k1) => { const P = []; for (let j = 0; j < N; j++) { const a = j / N * Math.PI * 2; P.push([xc + Math.cos(a) * rad, yo, r + Math.sin(a) * rad]) } return P };
  const dsk = disc(rr, 0, 0); if (s < 0) dsk.reverse(); out.push({ P: dsk, N: null, c: '#3b4047', m: 'metal', bias: .01, ln: [0, s, 0] });
  for (let k = 0; k < 5; k++) for (const o of [-.13, .13]) { const a = k / 5 * Math.PI * 2 + o, b = a + .16, P = [[xc + Math.cos(a) * rr * .3, yo + s * .004, r + Math.sin(a) * rr * .3], [xc + Math.cos(a - .04) * rr * .95, yo + s * .004, r + Math.sin(a - .04) * rr * .95], [xc + Math.cos(b) * rr * .95, yo + s * .004, r + Math.sin(b) * rr * .95], [xc + Math.cos(b - .08) * rr * .3, yo + s * .004, r + Math.sin(b - .08) * rr * .3]];
    if (s < 0) P.reverse(); out.push({ P, N: null, c: '#c7ced5', m: 'chrome', bias: .02, ln: [0, s, 0] }) }
  const hub = disc(rr * .26); hub.forEach(p => p[1] = yo + s * .008); if (s < 0) hub.reverse(); out.push({ P: hub, N: null, c: '#aab2ba', m: 'chrome', bias: .03, ln: [0, s, 0] });
  return out }
// a picture: id, paint colour, heading (radians, 0 = east, clockwise), s (world px per metre), res (device px per world px), dirs
// wf: the game's width contract (the road cars are drawn ×1.25 wide in the game) — 1 = the real proportions
function sprite(id, col, heading, s, res, dirs, wf) { const N = dirs || 16, k = ((Math.round(heading / (Math.PI * 2) * N) % N) + N) % N, h = k / N * Math.PI * 2; wf = wf || 1;
  return cached('car|' + id + '|' + col + '|' + N + '|' + k + '|' + s + '|' + res + '|' + wf, () => { const m = model(id, s * res * (SPEC[id] || SPEC['VH-SD-02']).L < 120 ? 0 : 1), W = p => [p[0], p[1] * wf, p[2]], WN = n => G.G2.nrm([n[0], n[1] / wf, n[2]]);
    const P = m.polys.map(q => { const o = Object.assign({}, q, { P: wf === 1 ? q.P : q.P.map(W), N: q.N && wf !== 1 ? q.N.map(WN) : q.N }); if (q.c === '__PAINT__') o.c = col; return o });
    const e = render(P, h, s, res, { ao: .35, foot: m.foot, shAlpha: .32, rim: Math.max(.6, res * .5), rimC: 'rgba(14,18,24,.45)' }); e.k = k; return e }) }
G.G2.car = { SPEC, model, sprite, curve, len: id => (SPEC[id] || SPEC['VH-SD-02']).L };
})(typeof window !== 'undefined' ? window : globalThis);
