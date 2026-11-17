// lab_smoke.js <lab.html> — closezoom: בדיקת עשן בלי דפדפן — מריץ את הסקריפטים של דף הניסוי עם קנבס מדומה (רושם מטריצה בלבד) ובודק שאין חריגות,
// שהפנים החדשות נעשות בזום 11 / 16 ולא בזום 5.5, ושאין משאבים טעונים.
const fs = require('fs'); const html = fs.readFileSync(process.argv[2], 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function M(a = 1, b = 0, c = 0, d = 1, e = 0, f = 0) { return { a, b, c, d, e, f } }
const mul = (m, n) => M(m.a * n.a + m.c * n.b, m.b * n.a + m.d * n.b, m.a * n.c + m.c * n.d, m.b * n.c + m.d * n.d, m.a * n.e + m.c * n.f + m.e, m.b * n.e + m.d * n.f + m.f);
function ctx2d(cv) { let T = M(), st = []; const noop = () => { }; const g = { addColorStop: noop };
  return new Proxy({ canvas: cv, getTransform: () => ({ ...T }), setTransform: (a, b, c, d, e, f) => { T = typeof a === 'object' ? M(a.a, a.b, a.c, a.d, a.e, a.f) : M(a, b, c, d, e, f) }, transform: (a, b, c, d, e, f) => { T = mul(T, M(a, b, c, d, e, f)) },
    translate: (x, y) => { T = mul(T, M(1, 0, 0, 1, x, y)) }, scale: (x, y) => { T = mul(T, M(x, 0, 0, y, 0, 0)) }, rotate: r => { T = mul(T, M(Math.cos(r), Math.sin(r), -Math.sin(r), Math.cos(r), 0, 0)) },
    save: () => st.push(T), restore: () => { T = st.pop() || M() }, createRadialGradient: () => g, createLinearGradient: () => g, measureText: () => ({ width: 10 }), getImageData: () => ({ data: new Uint8ClampedArray(4) }) },
    { get: (o, k) => k in o ? o[k] : (typeof k === 'string' && /^[a-z]/.test(k) ? noop : undefined), set: (o, k, v) => { o[k] = v; return true } }) }
class Canvas { constructor(w, h) { this.width = w || 300; this.height = h || 150 } getContext() { return this._c || (this._c = ctx2d(this)) } getBoundingClientRect() { return { width: 300, height: 340 } } }
global.OffscreenCanvas = Canvas;
const els = []; const el = tag => { const e = { tag, children: [], className: '', style: {}, dataset: {}, classList: { toggle() { }, add() { } }, appendChild(c) { this.children.push(c); return c }, querySelector() { return el('div') }, querySelectorAll() { return [] }, addEventListener() { }, set innerHTML(v) { this._h = v }, get innerHTML() { return this._h || '' } };
  if (tag === 'canvas') { const c = new Canvas(); Object.assign(c, e); return c } els.push(e); return e };
global.document = { createElement: el, getElementById: () => el('div'), querySelectorAll: () => [], documentElement: {} };
global.window = global; global.devicePixelRatio = 1; let frames = 0; const rafQ = [];
global.requestAnimationFrame = f => { rafQ.push(f) }; global.performance = { now: () => frames * 16.7 };
for (const s of scripts) (0, eval)(s);
for (let i = 0; i < +(process.env.NF || 30) && rafQ.length; i++) { frames++; const f = rafQ.shift(); const t0 = Date.now(); f(frames * 16.7); if (i < 3 || i % 10 === 0) console.error("frame", i, Date.now() - t0, "ms") }
const L = window.__LAB; console.log(JSON.stringify({ frames, cz: L.TCCZ.n, err: L.TCCZ.err, p34err: window.P34X && P34X.err, stats: L.P34.stats(), cells: L.cells.length, looks: L.CH.map(c => ({ k: c.key, hat: c.now.hat && c.now.hat.t, b: c.now.czF && c.now.czF.b, gl: c.now.glasses || '' })) }));
// the face only at the new zooms: one picture at 5.5 and at 16
const f0 = L.TCCZ.n.face; L.P34.spriteAt(L.CH[1].now, { k: 'stand' }, Math.PI / 2, 0, 5.5, 0); const at55 = L.TCCZ.n.face - f0; L.P34.spriteAt(L.CH[1].now, { k: 'stand' }, Math.PI / 2, 0, 8, 0); const at8 = L.TCCZ.n.face - f0 - at55;
console.log('face at 5.5:', at55, '· at 8:', at8, '· no loaded images:', !/data:image|<img|new Image\(|url\(/.test(html));
process.exit(0);
