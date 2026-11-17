// r3_offline.js <sim_dump.json> — fieldfix: הבדיקה ffR3Audit מחוץ לדפדפן, על הסימולציה כמו שרצה במשחק (dump), עם הקוד של 074zo כמו שהוא
const fs = require('fs'), P = '/home/user/tc_root/tc/pkg/work/src_game_t17_fieldfix/parts/';
const sim = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const k = fs.readFileSync(P + '074k_S15_buildings.js', 'utf8'), i = k.indexOf('/*S15B_L*/') + 10;
let depth = 0, j = i; for (; j < k.length; j++) { if (k[j] === '{') depth++; else if (k[j] === '}') { depth--; if (!depth) break } }
const m19 = fs.readFileSync(P + '019m_S15_draw.js', 'utf8');
const grab = re => m19.match(re)[0];
let src = 'var S15B_L=' + k.slice(i, j + 1) + ';\n' + grab(/const S15_HGR=\{[^;]*;/) + '\n' + grab(/const S15_LPX=\{[^}]*\};/) + '\n' + grab(/function s15PoseLeg\(g,t\)\{[\s\S]*?return null\}/) + '\n' + grab(/function s15PoseAt\(a,tc\)\{[\s\S]*?return null\}/) + '\nvar S15_FL={};for(const a of S15SIM.flights)S15_FL[a.id]=a;\n';
src += 'function s15HgrPose(){return{p:null}};function s15bAc(){};function s15StaticList(){return STAT};function roadAudit(){return{checks:[]}};\n';
src += fs.readFileSync(P + '074zo_fieldfix.js', 'utf8') + '\nreturn ffR3Audit();';
const LPX = { 'AC-LG-01': 668, 'AC-NB-01': 376, 'AC-RJ-01': 317, 'AC-CG-01': 549, 'AC-TB-01': 120, 'AC-LT-01': 91, 'AC-PR-01': 83, 'AC-BJ-01': 144, 'AC-CN-01': 144, 'AC-TP-01': 272 };
const STAT = sim.stat.map(o => Object.assign({}, o, { r: LPX[o.id] || 120 }));
const window = {};
const r = new Function('S15SIM', 'S15D', 'STAT', 'window', src)(sim, { spots: sim.spots, stands: sim.stands }, STAT, window);
console.log(JSON.stringify(r, null, 1));
