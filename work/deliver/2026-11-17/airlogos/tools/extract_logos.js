// extract_logos.js <dir with master parts> <out.json> — airlogos: הלוגואים של 62 המותגים מטבלת המותגים של המשחק (master, הקידוד של S7F301 —
//  בלי תנועות), רק החלק logo + שדות הזהות + השלטים (signs) — לדף של הבעלים. גם הטקסט של המפענח TCB.
const fs = require('fs'), vm = require('vm'), D = process.argv[2];
const a = fs.readFileSync(D + '/074m_brands_data.js', 'utf8'), b = fs.readFileSync(D + '/074m6_brands6_data.js', 'utf8');
const ctx = { window: {}, document: {}, performance: { now: () => 0 }, Path2D: function () { }, console }; vm.createContext(ctx);
vm.runInContext(a.replace(/^var TCB =/m, 'globalThis.TCB =').replace(/^var TC_BRANDS =/m, 'globalThis.TC_BRANDS ='), ctx); vm.runInContext(b, ctx);
const B = ctx.TC_BRANDS, out = { brands: {}, tcb: '' };
for (const k in B) { const r = B[k]; out.brands[k] = { name: r.name, kind: r.kind, shop: r.shop, at: r.at || [], deep: r.deep, accent: r.accent, light: r.light, set: r.set || null, signs: r.signs || [], logo: r.parts.logo } }
const i0 = a.indexOf('var TCB = (function'), i1 = a.indexOf('})();', i0) + 5; out.tcb = a.slice(i0, i1);
fs.writeFileSync(process.argv[3], JSON.stringify(out)); console.log(Object.keys(B).length, 'מותגים', JSON.stringify(out).length, 'בתים');
