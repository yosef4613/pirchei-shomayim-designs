// בדיקה מקומית בלי דפדפן (לעצמי בלבד, צילום לא נכנס לדף): node nrender.js <what> <out.png>
// דורש @napi-rs/canvas ב-NODE_PATH (לא חלק מהדף ולא מהמשחק).
const C = require('@napi-rs/canvas'), fs = require('fs'), vm = require('vm'), path = require('path');
const ctx0 = { console, performance, Math, JSON, Map, Set, Array, Object, Number, String, Symbol, Error, Float32Array, Uint8ClampedArray, setInterval: () => 0, setTimeout: () => 0, Path2D: C.Path2D, devicePixelRatio: 1 };
ctx0.OffscreenCanvas = function (w, h) { return C.createCanvas(w, h) };
ctx0.document = { createElement: () => { const c = C.createCanvas(2, 2); c.nodeName = 'CANVAS'; c.style = {}; c.setAttribute = () => 0; return c } }; ctx0.self = ctx0; ctx0.addEventListener = ctx0.removeEventListener = () => 0;
ctx0.window = ctx0; ctx0.globalThis = ctx0; ctx0.TurboCity = { get: () => null };
vm.createContext(ctx0);
const S = path.join(__dirname, '..', 'src');
for (const f of (process.env.FILES || 'g2_core.js,g2_car.js,g2_plane.js,g2_ped.js').split(',')) vm.runInContext(fs.readFileSync(path.join(S, f), 'utf8'), ctx0, { filename: f });
const [what, out] = process.argv.slice(2), W = +(process.env.W || 1600), H = +(process.env.H || 1000);
const cv = C.createCanvas(W, H), g = cv.getContext('2d'); g.fillStyle = '#9aa58c'; g.fillRect(0, 0, W, H);
ctx0.g = g; ctx0.W = W; ctx0.H = H;
ctx0.dr = (e, x, y, R) => g.drawImage(e.cv, x - e.ox / R, y - e.oy / R, e.cv.width / R, e.cv.height / R);
vm.runInContext(fs.readFileSync(what, 'utf8'), ctx0);
fs.writeFileSync(out, cv.toBuffer('image/png')); console.log(JSON.stringify(ctx0.G2 && ctx0.G2.stats()));
