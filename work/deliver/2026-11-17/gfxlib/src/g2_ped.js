/* g2_ped.js — ניסוי 3: הולך רגל בצייר החדש G2 — שלד עם מפרקים, הליכה וריצה, 16 כיוונים, מגוון דמויות.
   השלד (מטרים, לגובה 1.76; פרופורציות אנתרופומטריות): ירך 0.43, שוק 0.43, קרסול 0.07, כתפיים 0.40, זרוע 0.33, אמה 0.26, כף יד 0.10.
   התנועה: לכל רגל — שלב עמידה (כף הרגל נטועה בקרקע ונעה אחורה בדיוק במהירות הגוף, כך שאינה מחליקה) ושלב תנופה (קשת קדימה,
   הרמה, עקב / בהונות); הברך — IK של שתי עצמות (פתרון סגור); אגן שעולה ויורד ומסתובב, כתפיים בסיבוב נגדי, ידיים בתנופה נגדית;
   ריצה — שלב עמידה קצר (38%), שלב ריחוף, הטיה קדימה, מרפקים כפופים ~80°. כל חלק — גליל מתחדד / אליפסואיד מוצלל (גורו מקורב);
   השיער, הזקן, הכובע והכיפה — אזורים של הראש או חלקים משלהם; עיניים וגבות — מדבקות שרואים רק כשהפנים לכיוון המצלמה.
   המצלמה של האנשים במשחק (P34): עומק הגוף ב‑0.4, כפות הרגליים בעומק מלא (שלא יחליקו). */
(function (G) {
'use strict';
const { limb, ellipsoid, box, render, cached, nrm, sub, crs, dot } = G.G2;
const H0 = 1.76, TH = .43, SH = .43, ANK = .075, HIPW = .092, SHW = .195, UA = .32, FA = .255;
const LOOKS = [
  { id: 'office', name: 'פקיד', skin: '#e0b089', hair: '#2b2018', hc: 'short', top: '#f2f4f6', tie: '#2a4f8a', sleeve: 'long', legs: '#2b3240', shoes: '#16181b', h: 1.78, build: 1 },
  { id: 'teen', name: 'נער עם תיק', skin: '#c99068', hair: '#1c1612', hc: 'short', cap: '#c8372d', top: '#d84a3a', sleeve: 'short', legs: '#3b5a8a', shoes: '#eceff2', bag: '#2f4a3a', h: 1.66, build: .92 },
  { id: 'worker', name: 'פועל', skin: '#b47c56', hair: '#2a2420', hc: 'short', top: '#ff7a1a', vest: 1, sleeve: 'long', under: '#4a5058', legs: '#5a5f66', shoes: '#3a2a1e', helmet: '#f3c623', h: 1.8, build: 1.08 },
  { id: 'elder', name: 'מבוגר', skin: '#e8bf9c', hair: '#c9c9c9', hc: 'side', beard: '#cfcfcf', glasses: 1, top: '#b59a74', jacket: 1, sleeve: 'long', legs: '#6a6458', shoes: '#4a3020', h: 1.72, build: 1.05 },
  { id: 'student', name: 'תלמיד', skin: '#d9a77f', hair: '#3a2a1c', hc: 'short', kippah: '#1d2a6a', top: '#2f5fa8', hood: 1, sleeve: 'long', legs: '#20242a', shoes: '#2a2d31', h: 1.74, build: .96 },
  { id: 'runner', name: 'רץ', skin: '#8a5a3c', hair: '#141010', hc: 'buzz', top: '#2fae62', sleeve: 'short', legs: '#1f2328', shorts: 1, shoes: '#f2f4f6', sock: '#f2f4f6', h: 1.8, build: .98 }
];
const ACT = { walk: { fr: 12, beta: .61, D: 1.42, lift: .11, bob: .022, lean: .05, arm: .36, elbow: .32, rot: .09 },
              run: { fr: 10, beta: .38, D: 2.7, lift: .3, bob: .05, lean: .2, arm: .55, elbow: 1.5, rot: .14 },
              stand: { fr: 1 } };
const ss = t => t * t * (3 - 2 * t);
// two-bone IK in the sagittal plane of the leg: hip → ankle, the knee bends forward (+x)
function knee(hp, an, l1, l2) { const dx = an[0] - hp[0], dz = an[2] - hp[2], d = Math.min(l1 + l2 - 1e-4, Math.hypot(dx, dz)), a = Math.atan2(dz, dx);
  const c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), b = Math.acos(Math.max(-1, Math.min(1, c))), t = a + b;   // + b: the knee in front
  return [hp[0] + Math.cos(t) * l1, (hp[1] + an[1]) / 2, hp[2] + Math.sin(t) * l1] }
// the pose of a frame: joints in metres, the person facing +x, the ground point at the origin
function pose(L, act, u) { const s = L.h / H0, A = ACT[act] || ACT.stand, J = { s };
  const hip0 = (ANK + (TH + SH) * .985) * s;
  if (act === 'stand') { J.pel = [0, 0, hip0]; J.lean = 0; J.rot = 0;
    for (const sd of [1, -1]) { const hp = [0, sd * HIPW * s, hip0], an = [0, sd * (HIPW + .01) * s, ANK * s]; J['hip' + sd] = hp; J['ank' + sd] = an; J['kn' + sd] = knee(hp, an, TH * s, SH * s); J['ft' + sd] = 0 }
    J.armA = { '1': .04, '-1': .04 }; J.elb = { '1': .15, '-1': .15 }; return J }
  const D = A.D * s, beta = A.beta, run = act === 'run';
  let bob = run ? A.bob * Math.cos(4 * Math.PI * (u - .1)) : -A.bob * Math.cos(4 * Math.PI * (u - beta / 2 + .25)) ;
  const pel = [0, 0, hip0 - (run ? .06 * s : .015 * s) + bob]; J.pel = pel; J.lean = A.lean; J.rot = A.rot * Math.sin(2 * Math.PI * u);
  for (const sd of [1, -1]) { const ul = ((u + (sd > 0 ? 0 : .5)) % 1 + 1) % 1; let fx, fz, pitch;
    if (ul < beta) { const t = ul / beta; fx = D * beta / 2 - D * beta * t; fz = 0; pitch = t > .7 ? -(t - .7) / .3 * (run ? .9 : .6) : (t < .12 ? (.12 - t) / .12 * .25 : 0);
      if (t > .7) fz = Math.sin((t - .7) / .3 * Math.PI / 2) * .06 * s }
    else { const t = (ul - beta) / (1 - beta); fx = -D * beta / 2 + D * beta * ss(t); fz = A.lift * s * Math.sin(Math.PI * Math.pow(t, .8)); pitch = t < .3 ? -.6 + t * 2 : t > .8 ? (t - .8) * 1.2 : 0 }
    const hp = [Math.sin(J.rot) * -sd * HIPW * s * .5, sd * HIPW * s, pel[2]], an = [fx, sd * (HIPW - .005) * s, ANK * s + fz];
    J['hip' + sd] = hp; J['ank' + sd] = an; J['kn' + sd] = knee(hp, an, TH * s, SH * s); J['ft' + sd] = pitch }
  // the arms swing against the legs; the elbows bend more forward
  J.armA = {}; J.elb = {}; for (const sd of [1, -1]) { const ph = Math.sin(2 * Math.PI * (u + (sd > 0 ? .5 : 0))); J.armA[sd] = A.arm * ph - (run ? .08 : 0); J.elb[sd] = A.elbow + (run ? .1 : .18) * Math.max(0, ph) }
  return J }
function parts(L, act, u) { const J = pose(L, act, u), s = J.s, b = L.build || 1, out = [], P = J.pel, lean = J.lean || 0;
  const add = a => { for (const q of a) out.push(q) };
  const at = (z, x) => [P[0] + (x || 0) + Math.sin(lean) * (z - P[2]), 0, z];   // the spine leans forward about the hips
  // the legs: thigh, shin, foot (the trousers / the shorts and the socks), the shoes
  for (const sd of [1, -1]) { const hp = J['hip' + sd], kn = J['kn' + sd], an = J['ank' + sd], pt = J['ft' + sd];
    const tc = L.legs, sc = L.shorts ? L.skin : L.legs, sk = L.shorts ? 'skin' : 'cloth';
    add(limb(hp, kn, .078 * b * s, .056 * s, tc, 'cloth', 9, { rings: 4 }));
    if (L.shorts) { const mid = [kn[0] + (hp[0] - kn[0]) * .35, kn[1], kn[2] + (hp[2] - kn[2]) * .35]; add(limb(mid, kn, .056 * s, .048 * s, L.skin, 'skin', 8, { rings: 3 })) }
    add(limb(kn, an, (L.shorts ? .046 : .054) * s, (L.shorts ? .032 : .044) * s, sc, sk, 8, { rings: 4 }));
    if (L.sock) add(limb([an[0], an[1], an[2] + .06 * s], an, .036 * s, .034 * s, L.sock, 'cloth', 8, { rings: 2 }));
    // the shoe: from the heel to the toe, along the heading, pitched about the ball of the foot
    const fl = .245 * s, cp = Math.cos(pt), sp = Math.sin(pt), heel = [an[0] - .065 * s, an[1], an[2] - .045 * s], toe = [heel[0] + fl * cp, an[1], heel[2] - fl * sp * .6 + (pt < 0 ? -pt * .02 : 0)];
    add(limb([heel[0], heel[1], Math.max(.035 * s, heel[2])], [toe[0], toe[1], Math.max(.03 * s, toe[2])], .046 * s, .04 * s, L.shoes, 'leather', 8, { rings: 4, sq: .85 })) }
  // the hips and the torso (an abdomen and a chest; the shirt, the vest / the jacket over it)
  const top = L.top, tm = 'cloth';
  add(ellipsoid(at(P[2] + .02 * s), .115 * b * s, .165 * b * s, .11 * s, L.shorts ? L.legs : L.legs, 'cloth', { ni: 6, nj: 12 }));
  const chZ = P[2] + .36 * s, abZ = P[2] + .15 * s, rot = -J.rot * .8;
  add(ellipsoid(at(abZ), .12 * b * s, .165 * b * s, .16 * s, top, tm, { ni: 7, nj: 14, rot: rot * .5,
    mat: L.vest ? (i, j, c, n) => [Math.abs(n[1]) > .8 && L.vest ? L.under : top, tm] : null }));
  add(ellipsoid(at(chZ), .125 * b * s, .2 * b * s, .19 * s, top, tm, { ni: 8, nj: 16, rot,
    mat: (i, j, c, n) => { const lx = c[0] - at(chZ)[0];
      if (L.vest && (c[2] - chZ) > .06 * s && Math.abs(n[1]) < .5) return [L.under, tm];
      if (L.vest && c[2] < chZ - .05 * s && c[2] > chZ - .09 * s) return ['#d9dde2', 'chrome'];   // the reflective band
      if (L.jacket && lx > .08 * s && Math.abs(c[1]) < .045 * s && c[2] > chZ - .02 * s) return ['#efe9dd', tm];   // the shirt in the jacket's opening
      return [top, tm] } }));
  if (L.tie) add(limb([at(chZ + .14 * s)[0] + .122 * s, 0, chZ + .14 * s], [at(abZ)[0] + .118 * s, 0, abZ - .02 * s], .016 * s, .028 * s, L.tie, 'cloth', 6, { rings: 2, sq: .35, bias: .02 }));
  if (L.hood) add(ellipsoid([at(chZ + .2 * s)[0] - .1 * s, 0, chZ + .17 * s], .07 * s, .12 * s, .07 * s, top, tm, { ni: 5, nj: 10 }));
  if (L.bag) add(box(at(chZ)[0] - .26 * s, at(chZ)[0] - .1 * s, -.15 * s, .15 * s, abZ - .05 * s, chZ + .14 * s, L.bag, 'cloth', { top: L.bag }).map(q => Object.assign(q, { bias: -.01 })));
  // the arms: from the shoulder, the swing about the shoulder's axis (y), the elbow forward; sleeves long / short; the hands
  const shZ = P[2] + .5 * s;
  for (const sd of [1, -1]) { const sh = [at(shZ)[0] + Math.sin(rot) * sd * SHW * s * .6, sd * SHW * b * s, shZ], a = J.armA[sd], e = J.elb[sd];
    const el = [sh[0] + Math.sin(a) * UA * s, sh[1] + sd * .02 * s, sh[2] - Math.cos(a) * UA * s], wr = [el[0] + Math.sin(a + e) * FA * s, el[1] + sd * .005 * s, el[2] - Math.cos(a + e) * FA * s];
    const sl = L.vest ? L.under : top, long = L.sleeve === 'long';
    add(limb(sh, el, .052 * b * s, .043 * s, long || true ? sl : L.skin, 'cloth', 8, { rings: 3 }));
    if (!long) { const m = [sh[0] + (el[0] - sh[0]) * .5, sh[1] + (el[1] - sh[1]) * .5, sh[2] + (el[2] - sh[2]) * .5]; add(limb(m, el, .04 * s, .037 * s, L.skin, 'skin', 8, { rings: 2 })) }
    add(limb(el, wr, (long ? .041 : .035) * s, (long ? .034 : .028) * s, long ? sl : L.skin, long ? 'cloth' : 'skin', 8, { rings: 3 }));
    const hd = [wr[0] + Math.sin(a + e) * .05 * s, wr[1], wr[2] - Math.cos(a + e) * .05 * s];
    add(ellipsoid(hd, .035 * s, .025 * s, .05 * s, L.skin, 'skin', { ni: 4, nj: 8 })) }
  // the neck, the head (the hair, the beard cut from it), the face, the hat / the helmet / the kippah, the glasses
  const nk = at(shZ + .02 * s), hc = [at(P[2] + .7 * s)[0] + .015 * s, 0, P[2] + .7 * s], rx = .1 * s, ry = .082 * s, rz = .118 * s;
  add(limb([nk[0], 0, shZ - .04 * s], [hc[0] - .01 * s, 0, hc[2] - .06 * s], .045 * s, .043 * s, L.skin, 'skin', 8, { rings: 2 }));
  add(ellipsoid(hc, rx, ry, rz, L.skin, 'skin', { ni: 9, nj: 16, mat: (i, j, c, n) => { const lx = (c[0] - hc[0]) / rx, lz = (c[2] - hc[2]) / rz, ly = Math.abs(c[1] - hc[1]) / ry;
    const hairLine = L.hc === 'buzz' ? .45 : L.hc === 'side' ? .5 : .3;
    if (L.hc === 'side' && lz > .55 && lx > -.2) return [L.skin, 'skin'];               // the bald crown (with hair at the sides)
    if (lz > hairLine + (lx > .5 ? .18 : 0) || (lx < -.3 && lz > -.35) || (ly > .78 && lz > .05 && lx < .25)) return [L.hair, 'hair'];
    if (L.beard && lz < -.05 && lx > -.15) return [L.beard, 'hair'];
    return [L.skin, 'skin'] } }));
  // the ears, the eyes, the brows, the nose (seen only toward the camera)
  for (const sd of [1, -1]) { add(ellipsoid([hc[0] - .01 * s, sd * ry * .98, hc[2] - .005 * s], .018 * s, .012 * s, .03 * s, L.skin, 'skin', { ni: 3, nj: 6 }));
    const ex = hc[0] + rx * .9, ey = sd * .034 * s, ez = hc[2] + .015 * s;
    out.push({ P: [[ex, ey - .011 * s, ez - .006 * s], [ex, ey + .011 * s, ez - .006 * s], [ex, ey + .011 * s, ez + .006 * s], [ex, ey - .011 * s, ez + .006 * s]], N: null, c: '#1b1410', m: 'matte', ln: [1, 0, 0], bias: .03 });
    out.push({ P: [[ex - .004 * s, ey - .016 * s, ez + .02 * s], [ex - .004 * s, ey + .016 * s, ez + .022 * s]], line: 1, c: L.hair === '#c9c9c9' ? '#9a9a9a' : '#2a1e16', w: .008 * s, ln: [1, 0, 0], bias: .03 });
    if (L.glasses) out.push({ P: [[ex + .006 * s, ey - .02 * s, ez - .014 * s], [ex + .006 * s, ey + .02 * s, ez - .014 * s], [ex + .006 * s, ey + .02 * s, ez + .014 * s], [ex + .006 * s, ey - .02 * s, ez + .014 * s], [ex + .006 * s, ey - .02 * s, ez - .014 * s]], line: 1, c: '#1a1a1a', w: .006 * s, ln: [1, 0, 0], bias: .04 }) }
  out.push({ P: [[hc[0] + rx * 1.02, 0, hc[2] + .005 * s], [hc[0] + rx * 1.12, 0, hc[2] - .03 * s], [hc[0] + rx * .98, 0, hc[2] - .038 * s]], N: null, c: L.skin, m: 'skin', ln: [1, 0, 0], bias: .03, two: true });
  if (L.cap) { add(ellipsoid([hc[0] - .005 * s, 0, hc[2] + .05 * s], rx * 1.06, ry * 1.08, rz * .62, L.cap, 'cloth', { ni: 5, nj: 14, mat: (i, j, c) => c[2] > hc[2] + .03 * s ? [L.cap, 'cloth'] : null }));
    add(box(hc[0] + .05 * s, hc[0] + .16 * s, -.075 * s, .075 * s, hc[2] + .035 * s, hc[2] + .047 * s, L.cap, 'cloth', { top: L.cap })) }
  if (L.helmet) { add(ellipsoid([hc[0], 0, hc[2] + .045 * s], rx * 1.18, ry * 1.2, rz * .75, L.helmet, 'plastic', { ni: 5, nj: 14, mat: (i, j, c) => c[2] > hc[2] + .03 * s ? [L.helmet, 'plastic'] : null }));
    add(box(hc[0] + .06 * s, hc[0] + .15 * s, -.08 * s, .08 * s, hc[2] + .03 * s, hc[2] + .04 * s, L.helmet, 'plastic', { top: L.helmet })) }
  if (L.kippah) add(ellipsoid([hc[0] - .03 * s, 0, hc[2] + rz * .9], .055 * s, .055 * s, .022 * s, L.kippah, 'cloth', { ni: 3, nj: 10, mat: (i, j, c) => c[2] > hc[2] + rz * .9 ? [L.kippah, 'cloth'] : null }));
  return out }
// the people's camera: the body's depth at .4, the feet at the world's (the planted foot does not slide on the screen)
const KYC = .4, KF = .62, kyz = z => z >= .5 ? KYC : z <= .08 ? KF : KF + (KYC - KF) * ss((z - .08) / .42);   // the feet at .62: a compromise between the clean figure (.4) and the planted foot (1)
function frameOf(act, phase) { const F = (ACT[act] || ACT.stand).fr || 1; return F > 1 ? ((Math.floor(phase * F) % F) + F) % F : 0 }
// a picture: look (index or object), act ('stand' | 'walk' | 'run'), heading (radians, 0 = east, clockwise), phase 0…1, s (world px per m), res
function sprite(look, act, heading, phase, s, res, dirs) { const L = typeof look === 'number' ? LOOKS[look] : look, N = dirs || 16, k = ((Math.round(heading / (Math.PI * 2) * N) % N) + N) % N, fr = frameOf(act, phase), F = (ACT[act] || ACT.stand).fr || 1;
  return cached('ped|' + L.id + '|' + act + '|' + N + '|' + k + '|' + fr + '|' + s + '|' + res, () => { const small = s * res * L.h < 70; G.G2.detail = small ? .6 : 1; let P; try { P = parts(L, act, fr / F) } finally { G.G2.detail = 1 }   // a small figure (under 70 device px): fewer sides
    const e = render(P, k / N * Math.PI * 2, s, res, { ky: KYC, kyz, rim: Math.max(.8, res * .9), ao: .25, foot: [[[-.12, -.14], [.16, -.14], [.16, .14], [-.12, .14]]], shAlpha: .3 }); e.k = k; return e }) }
// world metres per cycle (for the planted feet: the phase advances by the distance walked / cycle)
const cycle = (look, act) => { const L = typeof look === 'number' ? LOOKS[look] : look; return (ACT[act] && ACT[act].D || 1.4) * L.h / H0 };
G.G2.ped = { LOOKS, ACT, pose, parts, sprite, cycle, kyz };
})(typeof window !== 'undefined' ? window : globalThis);
