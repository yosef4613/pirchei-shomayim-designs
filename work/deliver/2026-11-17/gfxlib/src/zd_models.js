/* zd_models.js — הניסוי עם ספרייה: אותה מכונית ואותו הולך רגל (אותן מידות, אותו שלד ואותה תנועה של G2) בספריית Zdog 1.1.3 (MIT, 29.7 ק"ב).
   מה שמצאתי: המצלמה של המשחק (x, y − 0.6·z) שווה בדיוק למבט אורתוגרפי מוטה ב-atan(0.6) ≈ 31° ומתיחה אנכית פי 1/cos(31°) ≈ 1.166 —
   כך Zdog (וגם כל מנוע תלת־ממד אורתוגרפי) מקבל את זווית המשחק בלי לשנות את הספרייה. Zdog מצייר בצבעים שטוחים (בלי תאורה ובלי מעברי צבע),
   ולכן הצבע של כל פאה מחושב כאן מהשמש של המשחק (G2.shade) — זה המקסימום שהספרייה נותנת. */
(function (G) {
'use strict';
const TH = Math.atan(.6), ST = 1 / Math.cos(TH);
function scene(w, h, zoom) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h;
  const illo = new Zdog.Illustration({ element: cv, zoom, resize: false }); const root = new Zdog.Anchor({ addTo: illo, rotate: { x: TH } }); return { cv, illo, root } }
// the canvas of Zdog (orthographic, tilted) → the game's picture: stretched up/down by 1 / cos θ
function finish(S, w, h, gz) { S.illo.updateRenderGraph(); const out = document.createElement('canvas'); out.width = w; out.height = Math.round(h * ST); const g = out.getContext('2d'); g.drawImage(S.cv, 0, 0, w, out.height); return { cv: out, ox: w / 2, oy: out.height / 2 + (gz || 0) } }
// a flat colour for a face whose world normal is n (after the heading) — the game's sun, the G2 materials
const fc = (col, m, n) => G.G2.css(G.G2.shade(col, m, G.G2.nrm(n), G.G2.VC));
// the car (the sedan of G2: 4.85 × 1.84 × 1.45, wheels 0.335) — boxes with Zdog's round strokes, cylinders for the wheels
function car(col, heading, s, res) { const z = s * res, w = Math.ceil(5.6 * z) + 8, h = Math.ceil(5.6 * z) + 8, S = scene(w, h, z), c = Math.cos(heading), sn = Math.sin(heading);
  // Zdog: x right, y down, z toward the viewer = the world's x (east), y (south), z (up); the car turns about z by the heading
  const car = new Zdog.Anchor({ addTo: S.root, rotate: { z: heading } });
  const R = v => [v[0] * c - v[1] * sn, v[0] * sn + v[1] * c, v[2]];
  const face = (n, cc, m) => fc(cc, m || 'paint', R(n));
  const bx = (o) => new Zdog.Box(Object.assign({ addTo: car, stroke: .08, fill: true }, o));
  // Zdog's box faces: front = +z (up here), rear = −z, left / right = ∓x (rear / nose), top / bottom = ∓y (north / south side)
  bx({ width: 4.7, height: 1.76, depth: .62, translate: { z: .55 }, color: face([0, 0, 1], col), frontFace: face([0, 0, 1], col), rearFace: false,
    leftFace: face([-1, 0, 0], col), rightFace: face([1, 0, 0], col), topFace: face([0, -1, 0], col), bottomFace: face([0, 1, 0], col) });
  bx({ width: 2.1, height: 1.42, depth: .42, translate: { x: -.42, z: 1.08 }, color: face([0, 0, 1], col), frontFace: face([0, 0, 1], col), rearFace: false,
    leftFace: face([-1, 0, .3], '#1d2b38', 'glass'), rightFace: face([1, 0, .3], '#1d2b38', 'glass'), topFace: face([0, -1, .3], '#1d2b38', 'glass'), bottomFace: face([0, 1, .3], '#1d2b38', 'glass') });
  for (const [x, y] of [[1.475, .79], [1.475, -.79], [-1.355, .79], [-1.355, -.79]]) new Zdog.Cylinder({ addTo: car, diameter: .67, length: .22, translate: { x, y, z: .335 }, rotate: { x: Math.PI / 2 }, color: '#17191c', backface: '#2a2d31', frontFace: '#9aa3ab', stroke: false });
  new Zdog.Rect({ addTo: car, width: .5, height: .1, translate: { x: 2.36, z: .45 }, rotate: { y: Math.PI / 2 }, color: '#f2c51c', fill: true, stroke: .02 });
  for (const y of [.6, -.6]) new Zdog.Rect({ addTo: car, width: .14, height: .26, translate: { x: 2.38, y, z: .72 }, rotate: { y: Math.PI / 2 }, color: '#e9eef2', fill: true, stroke: .02 });
  return finish(S, w, h, 0) }
// the person: the G2 skeleton of the same frame (G2.ped.pose), drawn with Zdog's round strokes (capsules) — flat colours
function ped(L, act, heading, phase, s, res) { const z = s * res, w = Math.ceil(2.4 * z) + 6, h = Math.ceil(2.4 * z) + 6, S = scene(w, h, z), J = G.G2.ped.pose(L, act, phase), sc = J.s;
  const P = new Zdog.Anchor({ addTo: S.root, rotate: { z: heading }, translate: { z: -0.95 } });
  const v = p => ({ x: p[0], y: p[1], z: p[2] });
  const seg = (a, b, wdt, col) => new Zdog.Shape({ addTo: P, path: [v(a), v(b)], stroke: wdt, color: col });
  for (const sd of [1, -1]) { seg(J['hip' + sd], J['kn' + sd], .15 * sc, L.legs); seg(J['kn' + sd], J['ank' + sd], .1 * sc, L.shorts ? L.skin : L.legs);
    const a = J['ank' + sd]; seg([a[0] - .06, a[1], .05], [a[0] + .18, a[1], .05], .09 * sc, L.shoes) }
  const pz = J.pel[2], lean = J.lean || 0, at = (zz) => [Math.sin(lean) * (zz - pz), 0, zz];
  seg(at(pz + .05), at(pz + .42), .34 * sc, L.top);
  for (const sd of [1, -1]) { const shd = [at(pz + .5)[0], sd * .19 * sc, pz + .5 * sc], a = J.armA[sd], e = J.elb[sd], el = [shd[0] + Math.sin(a) * .32 * sc, shd[1], shd[2] - Math.cos(a) * .32 * sc], wr = [el[0] + Math.sin(a + e) * .26 * sc, el[1], el[2] - Math.cos(a + e) * .26 * sc];
    seg(shd, el, .09 * sc, L.top); seg(el, wr, .075 * sc, L.sleeve === 'long' ? L.top : L.skin); seg(wr, wr, .08 * sc, L.skin) }
  const hc = at(pz + .7 * sc); new Zdog.Shape({ addTo: P, translate: v(hc), stroke: .22 * sc, color: L.skin });
  new Zdog.Hemisphere({ addTo: P, translate: { x: hc[0] - .01, y: 0, z: hc[2] + .02 }, diameter: .23 * sc, color: L.cap || L.helmet || L.hair, backface: L.hair, stroke: false });
  return finish(S, w, h, .6 * .95 * z) }
G.ZD = { car, ped, TH, ST };
})(typeof window !== 'undefined' ? window : globalThis);
