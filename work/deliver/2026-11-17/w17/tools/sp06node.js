// sp06node.js — טוען ב-Node את C34 (עם 063c ו-063d) ואת הנתונים של 012c / 012d (בלי דפדפן): ציור על קנבס מדומה של כל 16 הכיוונים, הדלתות, והבדיקה של R‑70
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const S5 = require('/home/user/tc_root/tc/pkg/work/deliver/2026-11-11/sp05/tools/sp05node.js');
const L70 = require('/home/user/tc_root/tc/pkg/work/deliver/2026-11-11/cars70/tools/c34node.js');
function data(src, f, k) { const s = fs.readFileSync(path.join(src, 'parts', f), 'utf8'), g = { VD_M: {}, VM: [], regVs() { }, vm: (a, e) => Object.assign(a, e), veh() { }, PAL: [], Math, JSON, Object, Array };
  g.window = g; vm.createContext(g); vm.runInContext(s, g); return g[k] }
const src = process.argv[2];
const mk = () => { const ctx = new Proxy({}, { get: (o, k) => { if (k in o) return o[k]; if (k === 'canvas') return cv; if (k === 'getImageData') return () => ({ data: new Uint8ClampedArray(4) }); if (k === 'getTransform') return () => ({ a: 1, b: 0, c: 0, d: 1, e: 0, f: 0 }); if (k === 'measureText') return () => ({ width: 1 });
  if (/^create(Linear|Radial)Gradient$|^createPattern$/.test(k)) return () => ({ addColorStop() { } }); return typeof k === 'string' && /^[a-z]/.test(k) && !/Style$|^line(Width|Cap|Join|DashOffset)$|^global|^font|^filter|^image|^textAlign|^textBaseline|^shadow/.test(k) ? () => { } : undefined }, set: (o, k, v) => (o[k] = v, true) });
  const cv = { width: 1, height: 1, getContext: () => ctx, style: {} }; return cv };
const g = L70.load(src, { __R70_MODE: 'stage2', TC_SP05: data(src, '012c_sp05_asset.js', 'TC_SP05'), TC_SP06: data(src, '012d_sp06_asset.js', 'TC_SP06'), document: { createElement: () => mk() }, Path2D: function () { this.moveTo = this.lineTo = this.closePath = this.rect = this.arc = this.ellipse = this.bezierCurveTo = this.quadraticCurveTo = () => { } } });
const C = g.C34, err = []; let n = 0, sz = [];
for (const md of ['stage2', 'proto', 'all', 'stage2']) { C.r70(md); for (const id of ['VH-SP-06', 'VH-SP-05', 'VH-SP-02']) for (let k = 0; k < 16; k++) for (const o of [null, { cargo: { key: id === 'VH-SP-06' ? 'sp6d' : 'sp5d' } }]) { try { const r = C.render(id, '#d23a3a', k, 16, 1, o); n++; if (id === 'VH-SP-06' && md === 'stage2' && !o) sz.push([k, r.cv.width, r.cv.height]) } catch (e) { err.push(md + ' ' + id + ' k' + k + ' ' + (e && e.stack || e).toString().split('\n').slice(0, 3).join(' | ')) } } }
C.r70('stage2');
let ck = null; try { ck = C.sp06Check() } catch (e) { ck = 'ERR ' + e }
console.log(JSON.stringify({ renders: n, nErr: err.length, err: err.slice(0, 6), sp06: ck, sp06err: C.sp06 && C.sp06.err, sp05err: C.sp05 && C.sp05.err, sizes: sz.slice(0, 6), sp05: C.sp05Check() }, null, 1));
