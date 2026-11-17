// טורבו סיטי — ניסוי תלת־ממד: B4 לפי המפה, רכב אחד, המצלמה של המשחק. Three.js (MIT) מוטמע; בלי תמונות ובלי קבצים חיצוניים.
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import DATA from '../b4_data.json';
import { makeSim } from './sim.js';
import { Acc, PAL, buildWorld, buildLots } from './build_world.js';
import { makeWorldManager } from './world_manager.js';

const $ = id => document.getElementById(id);
const T0 = performance.now();
const K = 0.6, TILT = Math.atan(K), STRETCH = 1 / Math.cos(TILT);   // 30.96°, ‏×1.166 — ההיטל של המשחק
const WM = makeWorldManager({ money: 2500 }).addCity('turbo', 'three').addZone('turbo', 'B4', DATA); WM.enter('turbo');
const SIM = makeSim(DATA), ST = SIM.st, car = ST.car;
let low = /low/.test(location.hash), night = false, mode = 'game', ppm = 9;

const canvas = $('view');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: !low, powerPreference: 'high-performance' });
renderer.setPixelRatio(low ? 1 : Math.min(2, devicePixelRatio));
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = !low; renderer.shadowMap.type = THREE.PCFShadowMap; renderer.shadowMap.autoUpdate = false;
const scene = new THREE.Scene(); scene.background = new THREE.Color('#9fc3d6');
const pmrem = new THREE.PMREMGenerator(renderer); const ENV = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;   // השתקפות בקוד — סצנה פנימית, לא תמונה

// אור: שמש מדרום־מזרח, גבוהה — הצללים לצפון־מערב כמו במשחק
const hemi = new THREE.HemisphereLight('#dbe9ff', '#5d7048', 1.25); scene.add(hemi);
const sun = new THREE.DirectionalLight('#fff3dc', 2.6); sun.position.set(110, 140, 120); sun.target.position.set(65, 0, 40); scene.add(sun, sun.target);
sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -110, right: 110, top: 110, bottom: -110, near: 10, far: 420 }); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.04;

// חומרים — מעט מאוד, כל הצבעים בקודקודים
const M = {
  ground: new THREE.MeshLambertMaterial({ vertexColors: true }),
  solid: new THREE.MeshLambertMaterial({ vertexColors: true }),
  glass: new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .12, metalness: .35, envMap: ENV, envMapIntensity: .9 }),
  glassLit: new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .2, metalness: .1, envMap: ENV, emissive: '#ffcf7a', emissiveIntensity: 0 }),
  leaf: new THREE.MeshLambertMaterial({ flatShading: true }),
  trunk: new THREE.MeshLambertMaterial({ color: PAL.trunk }),
  metal: new THREE.MeshLambertMaterial({ color: '#4b5560' }),
  lampHead: new THREE.MeshLambertMaterial({ color: '#f5efd8', emissive: '#ffdf9a', emissiveIntensity: 0 }),
  pool: new THREE.MeshBasicMaterial({ color: '#ffcf80', transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }),
};
M.ground.polygonOffset = true; M.ground.polygonOffsetFactor = -1;

// העולם
const A = new Acc(); const W = buildWorld(DATA, A); W.signs = [];
const litCount = buildLots(DATA, A, W);
const world = new THREE.Group(); scene.add(world);
for (const m of A.build(M)) { m.receiveShadow = true; m.castShadow = m.name !== 'ground'; world.add(m) }

// עצים, דקלים, פנסים, ספסלים — מופעים (InstancedMesh): קריאת ציור אחת לכל סוג
const mx = new THREE.Matrix4(), q = new THREE.Quaternion(), v3 = new THREE.Vector3(), sc = new THREE.Vector3(), col = new THREE.Color();
function inst(geo, mat, list, f, cast = true) { const im = new THREE.InstancedMesh(geo, mat, Math.max(1, list.length)); list.forEach((o, i) => { f(o, i); im.setMatrixAt(i, mx) }); im.count = list.length; im.castShadow = cast; im.receiveShadow = true; world.add(im); return im }
const crownG = mergeGeometries([new THREE.IcosahedronGeometry(1.6, 1).translate(0, 4.2, 0), new THREE.IcosahedronGeometry(1.2, 1).translate(.9, 3.6, .4), new THREE.IcosahedronGeometry(1.15, 1).translate(-.8, 3.7, -.3)]);
const trunkG = new THREE.CylinderGeometry(.16, .24, 3.2, 6).translate(0, 1.6, 0);
const crowns = inst(crownG, M.leaf, W.trees, (o, i) => { const s = (o.s || 1) * (o.bush ? .55 : 1); mx.compose(v3.set(o.x, o.bush ? -1.6 : 0, o.z), q.setFromAxisAngle(sc.set(0, 1, 0), i * 1.7), sc.set(s, s * (o.bush ? .7 : 1), s)) });
W.trees.forEach((o, i) => crowns.setColorAt(i, col.set(PAL.leaf[i % 4])));
inst(trunkG, M.trunk, W.trees.filter(o => !o.bush), o => mx.compose(v3.set(o.x, 0, o.z), q.identity(), sc.set(o.s || 1, o.s || 1, o.s || 1)));
// דקל: גזע גבוה + 8 כפות
const frond = new THREE.ConeGeometry(.55, 3.4, 4); frond.rotateZ(-Math.PI / 2 + .35); frond.scale(1, 1, .35); frond.translate(1.7, 0, 0);
const palmCrown = mergeGeometries(Array.from({ length: 8 }, (_, i) => frond.clone().rotateY(i * Math.PI / 4).translate(0, 7.2, 0)));
const palmTrunk = new THREE.CylinderGeometry(.2, .32, 7.3, 7).translate(0, 3.65, 0);
inst(palmTrunk, new THREE.MeshLambertMaterial({ color: '#8a6b47' }), W.palms, o => mx.compose(v3.set(o.x, .2, o.z), q.identity(), sc.setScalar(o.big ? 1.15 : 1)));
const palmLeaves = inst(palmCrown, new THREE.MeshLambertMaterial({ color: '#4f8a3a', flatShading: true }), W.palms, (o, i) => mx.compose(v3.set(o.x, .2, o.z), q.setFromAxisAngle(sc.set(0, 1, 0), i * .9), sc.setScalar(o.big ? 1.15 : 1)));
const lampPost = mergeGeometries([new THREE.CylinderGeometry(.07, .1, 6, 6).translate(0, 3, 0), new THREE.BoxGeometry(.1, .1, 1.6).translate(0, 5.95, .75)]);
inst(lampPost, M.metal, W.lamps, o => mx.compose(v3.set(o.x, .15, o.z), q.setFromAxisAngle(sc.set(0, 1, 0), o.dir), sc.setScalar(1)));
inst(new THREE.BoxGeometry(.45, .14, .8).translate(0, 5.85, 1.45), M.lampHead, W.lamps, o => mx.compose(v3.set(o.x, .15, o.z), q.setFromAxisAngle(sc.set(0, 1, 0), o.dir), sc.setScalar(1)), false);
const pools = inst(new THREE.CircleGeometry(5.5, 24).rotateX(-Math.PI / 2), M.pool, W.lamps, o => mx.compose(v3.set(o.x + Math.sin(o.dir) * 1.4, .2, o.z + Math.cos(o.dir) * 1.4), q.identity(), sc.setScalar(1)), false); pools.receiveShadow = false;
const benchG = mergeGeometries([new THREE.BoxGeometry(1.8, .08, .45).translate(0, .45, 0), new THREE.BoxGeometry(1.8, .4, .06).translate(0, .75, -.22), new THREE.BoxGeometry(.08, .45, .4).translate(-.8, .22, 0), new THREE.BoxGeometry(.08, .45, .4).translate(.8, .22, 0)]);
inst(benchG, new THREE.MeshLambertMaterial({ color: '#8a5a32' }), W.benches, o => mx.compose(v3.set(o.x, .12, o.z), q.setFromAxisAngle(sc.set(0, 1, 0), o.r), sc.setScalar(1)));

// רמזורים — עמוד, זרוע, ראש עם 3 עדשות; העדשות נדלקות לפי הסימולציה
const sigHeads = [];
const offMat = c => new THREE.MeshLambertMaterial({ color: c, emissive: c, emissiveIntensity: .05 });
for (const s of W.signals) {
  const g = new THREE.Group(); g.position.set(s.x, .15, s.z); world.add(g);
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(.09, .11, 5.6, 6).translate(0, 2.8, 0), M.metal); g.add(pole);
  const arm = new THREE.Mesh(new THREE.BoxGeometry(.1, .1, s.reach).translate(0, 5.5, -s.reach / 2), M.metal); arm.rotation.y = Math.atan2(-s.ax, -s.az); g.add(arm);
  const hd = new THREE.Group(); hd.position.set(s.ax * s.reach, 0, s.az * s.reach); hd.rotation.y = Math.atan2(s.fx, s.fz); g.add(hd);
  const box = new THREE.Mesh(new THREE.BoxGeometry(.42, 1.2, .3).translate(0, 4.85, 0), new THREE.MeshLambertMaterial({ color: '#1d2329' })); hd.add(box);
  const lens = ['#ff3b2f', '#ffbf2f', '#3bdc6a'].map((c, i) => new THREE.Mesh(new THREE.CircleGeometry(.15, 12).translate(0, 5.23 - i * .38, .16), offMat(c))); hd.add(...lens);
  pole.castShadow = arm.castShadow = box.castShadow = true;
  sigHeads.push({ s, lens, node: SIM.st.signals.find(x => x.id === s.node) });
}

// שלטים על המבנים — מצוירים בקנבס בקוד (טקסט), לא תמונה שנטענת
for (const s of W.signs) {
  const cv = document.createElement('canvas'); cv.width = 512; cv.height = 96; const c = cv.getContext('2d');
  c.fillStyle = s.accent; c.fillRect(0, 0, 512, 96); c.fillStyle = '#ffffff22'; c.fillRect(0, 0, 512, 10); c.fillStyle = '#fff'; c.font = 'bold 50px Arial'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.direction = 'rtl'; c.fillText(s.text, 256, 52, 490);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const w = Math.max(5, s.w * .7), m = new THREE.Mesh(new THREE.PlaneGeometry(w, w * 96 / 512), new THREE.MeshLambertMaterial({ map: tex, emissive: '#ffffff', emissiveMap: tex, emissiveIntensity: .15 }));
  m.position.set(s.x, s.y + .3, s.z + .02); world.add(m); s.mesh = m;
}

// הרכב — סדאן 4.6 × 1.84 × 1.45 מ׳, בקוד: פרופיל צד מוחלק, תא זכוכית, גלגלים, פנסים
const carG = new THREE.Group(); scene.add(carG);
const paint = new THREE.MeshStandardMaterial({ color: '#c8352b', roughness: .28, metalness: .45, envMap: ENV, envMapIntensity: 1.1 });
const glassM = new THREE.MeshStandardMaterial({ color: '#1b2633', roughness: .05, metalness: .6, envMap: ENV, envMapIntensity: 1.4 });
function profile(pts) { const s = new THREE.Shape(); s.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) s.lineTo(pts[i][0], pts[i][1]); return s }
const bodyS = profile([[-2.3, .32], [2.3, .32], [2.32, .62], [2.18, .78], [1.15, .9], [-1.9, .92], [-2.3, .82]]);
const body = new THREE.ExtrudeGeometry(bodyS, { depth: 1.64, bevelEnabled: true, bevelThickness: .1, bevelSize: .09, bevelSegments: 3, curveSegments: 4 }); body.translate(0, 0, -.82);
const cabS = profile([[-1.55, .9], [1.1, .9], [.45, 1.42], [-1.05, 1.44]]);
const cab = new THREE.ExtrudeGeometry(cabS, { depth: 1.4, bevelEnabled: true, bevelThickness: .05, bevelSize: .05, bevelSegments: 2 }); cab.translate(0, 0, -.7);
const roof = new THREE.BoxGeometry(1.3, .06, 1.38).translate(-.3, 1.47, 0);
const bodyM = new THREE.Mesh(body, paint), cabM = new THREE.Mesh(cab, glassM), roofM = new THREE.Mesh(roof, paint);
const carInner = new THREE.Group(); carInner.add(bodyM, cabM, roofM); carInner.rotation.y = 0; carG.add(carInner);
for (const [x, z] of [[-.75, .71], [-.75, -.71], [.15, .74], [.15, -.74]]) { const p = new THREE.Mesh(new THREE.BoxGeometry(.07, .5, .03).translate(x, 1.15, z), paint); carInner.add(p) }
const tireG = new THREE.CylinderGeometry(.33, .33, .24, 18).rotateX(Math.PI / 2), rimG = new THREE.CylinderGeometry(.21, .21, .25, 10).rotateX(Math.PI / 2);
const tireM = new THREE.MeshStandardMaterial({ color: '#1a1a1a', roughness: .9 }), rimM = new THREE.MeshStandardMaterial({ color: '#c9ced3', roughness: .25, metalness: .9, envMap: ENV });
const wheels = [];
for (const [x, z] of [[1.4, .83], [1.4, -.83], [-1.42, .83], [-1.42, -.83]]) { const w = new THREE.Group(); w.position.set(x, .33, z); const t = new THREE.Mesh(tireG, tireM), r = new THREE.Mesh(rimG, rimM); w.add(t, r); carInner.add(w); wheels.push(w) }
const headM = new THREE.MeshStandardMaterial({ color: '#fffbe8', emissive: '#fff4c8', emissiveIntensity: .3 }), tailM = new THREE.MeshStandardMaterial({ color: '#7a0d0d', emissive: '#ff2020', emissiveIntensity: .25 });
for (const z of [.6, -.6]) { carInner.add(new THREE.Mesh(new THREE.BoxGeometry(.06, .13, .38).translate(2.4, .66, z), headM)); carInner.add(new THREE.Mesh(new THREE.BoxGeometry(.06, .12, .42).translate(-2.39, .72, z), tailM)) }
carInner.add(new THREE.Mesh(new THREE.BoxGeometry(.04, .14, .55).translate(2.42, .45, 0), new THREE.MeshLambertMaterial({ color: '#f2c200' })));   // לוחית צהובה
carInner.add(new THREE.Mesh(new THREE.BoxGeometry(.04, .14, .55).translate(-2.41, .5, 0), new THREE.MeshLambertMaterial({ color: '#f2c200' })));
const grille = new THREE.Mesh(new THREE.BoxGeometry(.05, .14, .9).translate(2.41, .55, 0), new THREE.MeshLambertMaterial({ color: '#222' })); carInner.add(grille);
carG.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = false } });
const blob = new THREE.Mesh(new THREE.PlaneGeometry(5.4, 2.4).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: '#000', transparent: true, opacity: .28, depthWrite: false })); blob.position.y = .045; carG.add(blob);
const head = new THREE.SpotLight('#fff1cc', 0, 45, .55, .6, 1.2); head.position.set(2.3, .8, 0); head.target.position.set(14, 0, 0); carG.add(head, head.target);
const headPool = new THREE.Mesh(new THREE.CircleGeometry(1, 24).rotateX(-Math.PI / 2).scale(9, 1, 3.6).translate(9, .07, 0), new THREE.MeshBasicMaterial({ color: '#ffe9b8', transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending })); carG.add(headPool);

// מצלמות
const camO = new THREE.OrthographicCamera(-1, 1, 1, -1, -500, 1500);
const camP = new THREE.PerspectiveCamera(50, 1, .3, 1500);
const orbit = new OrbitControls(camP, canvas); orbit.enabled = false; orbit.enableDamping = true; orbit.maxPolarAngle = 1.45; orbit.target.set(65, 0, 40);
let gameRot = 0;   // "מבט המשחק" — אפשר גם לסובב ב-Q/E ברבעים (90°), כמו כפתורי המצלמה של המשחק
function resize() { const w = innerWidth, h = innerHeight; renderer.setSize(w, h, false); camP.aspect = w / h; camP.updateProjectionMatrix() }
addEventListener('resize', resize); resize();
const camTarget = new THREE.Vector3(car.x, 0, car.y);
function placeGameCam() {
  const w = innerWidth, h = innerHeight; camO.left = -w / 2 / ppm; camO.right = w / 2 / ppm; camO.top = h / 2 / (ppm * STRETCH); camO.bottom = -h / 2 / (ppm * STRETCH); camO.updateProjectionMatrix();
  const d = 300, a = gameRot * Math.PI / 2; camO.position.set(camTarget.x + Math.sin(a) * Math.sin(TILT) * d, Math.cos(TILT) * d, camTarget.z + Math.cos(a) * Math.sin(TILT) * d); camO.up.set(0, 1, 0); camO.lookAt(camTarget);
}
function setMode(m) { mode = m; orbit.enabled = m === 'free'; if (m === 'chase') camP.position.set(car.x - Math.cos(car.h) * 11, 5.2, car.y - Math.sin(car.h) * 11); if (m === 'free') { camP.position.set(camTarget.x + 70, 80, camTarget.z + 110); orbit.target.copy(camTarget) } document.querySelectorAll('[data-mode]').forEach(b => b.classList.toggle('on', b.dataset.mode === m)); $('modeText').textContent = { game: 'מבט המשחק — ההיטל המדויק של טורבו סיטי (31° + ×1.166) · גלגלת לזום · Q/E סיבוב ברבעים', chase: 'מעקב — מאחורי הרכב', free: 'חופשי — גרירה לסיבוב, גלגלת לזום' }[m] }
canvas.addEventListener('wheel', e => { if (mode === 'game') { e.preventDefault(); ppm = Math.max(3, Math.min(40, ppm * (e.deltaY > 0 ? .9 : 1.1))) } }, { passive: false });

// יום / לילה
function setNight(v) {
  night = v; const k = v ? 1 : 0;
  sun.intensity = v ? .25 : 2.6; sun.color.set(v ? '#8aa6ff' : '#fff3dc'); hemi.intensity = v ? .32 : 1.25; hemi.color.set(v ? '#5a6f9c' : '#dbe9ff');
  scene.background.set(v ? '#0d1626' : '#9fc3d6'); M.lampHead.emissiveIntensity = 2.2 * k; M.pool.opacity = .22 * k; M.glassLit.emissiveIntensity = 1.4 * k;
  head.intensity = v ? 60 : 0; headPool.material.opacity = v ? .28 : 0; headM.emissiveIntensity = v ? 3 : .3; tailM.emissiveIntensity = v ? 2 : .25;
  for (const s of W.signs) s.mesh.material.emissiveIntensity = v ? .9 : .15; renderer.toneMappingExposure = v ? 1.25 : 1.05;
  renderer.shadowMap.needsUpdate = true; $('nightBtn').textContent = v ? '☀ יום' : '☾ לילה';
}
function setLow(v) { low = v; renderer.setPixelRatio(v ? 1 : Math.min(2, devicePixelRatio)); renderer.shadowMap.enabled = !v; world.traverse(o => { if (o.material) o.material.needsUpdate = true }); renderer.shadowMap.needsUpdate = true; $('qualBtn').textContent = v ? 'איכות: נמוכה' : 'איכות: מלאה'; resize() }

// קלט
const KEYS = { KeyW: 'up', ArrowUp: 'up', KeyS: 'down', ArrowDown: 'down', KeyA: 'left', ArrowLeft: 'left', KeyD: 'right', ArrowRight: 'right', Space: 'brake' };
addEventListener('keydown', e => { if (KEYS[e.code]) { ST.input[KEYS[e.code]] = 1; e.preventDefault() } else if (e.code === 'Digit1') setMode('game'); else if (e.code === 'Digit2') setMode('chase'); else if (e.code === 'Digit3') setMode('free'); else if (e.code === 'KeyN') setNight(!night); else if (e.code === 'KeyQ') gameRot = (gameRot + 1) % 4; else if (e.code === 'KeyE') gameRot = (gameRot + 3) % 4 });
addEventListener('keyup', e => { if (KEYS[e.code]) ST.input[KEYS[e.code]] = 0 });
document.querySelectorAll('[data-key]').forEach(b => { const k = KEYS[b.dataset.key]; const on = e => { e.preventDefault(); ST.input[k] = 1 }, off = () => ST.input[k] = 0; b.addEventListener('pointerdown', on); b.addEventListener('pointerup', off); b.addEventListener('pointerleave', off) });
document.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));
$('nightBtn').onclick = () => setNight(!night); $('qualBtn').onclick = () => setLow(!low);

// מפה קטנה — מצייר 2D שקורא את אותם נתונים (ההפרדה של World Manager בפועל)
const mini = $('mini').getContext('2d'), MW = DATA.window, msx = 220 / (MW[2] - MW[0] + 20), mox = -MW[0] + 10, moy = -MW[1] + 10;
function drawMini() { const c = mini; c.fillStyle = '#5f9150'; c.fillRect(0, 0, 220, 150); c.save(); c.scale(msx, msx); c.translate(mox, moy);
  for (const r of DATA.roads) { c.strokeStyle = '#3d4247'; c.lineWidth = r.width; c.beginPath(); c.moveTo(...r.pts[0]); c.lineTo(...r.pts[1]); c.stroke() }
  for (const s of DATA.sites) { const [a, b, x, y] = s.rect; c.fillStyle = s.kind === 'building' ? '#e9dcc0' : s.kind === 'parking' ? '#6b7076' : s.kind === 'court' ? '#b9653a' : '#7fae5f'; c.fillRect(a, b, x - a, y - b) }
  for (const z of DATA.context || []) { const [a, b, x, y] = z.rect; c.fillStyle = '#cfc8b8'; c.fillRect(a, b, x - a, y - b) }
  c.translate(car.x, car.y); c.rotate(car.h); c.fillStyle = '#d4af37'; c.strokeStyle = '#1b2b45'; c.lineWidth = 1.2; c.beginPath(); c.moveTo(6, 0); c.lineTo(-4, 4); c.lineTo(-4, -4); c.closePath(); c.fill(); c.stroke(); c.restore() }

// הלולאה
let last = performance.now(), frames = 0, fpsT = last, fps = 0, frameN = 0;
const LC = { r: new THREE.Color('#ff3b2f'), y: new THREE.Color('#ffbf2f'), g: new THREE.Color('#3bdc6a') };
function frame(now) {
  const dt = Math.min(.05, (now - last) / 1000); last = now; SIM.step(dt);
  carG.position.set(car.x, 0, car.y); carG.rotation.y = -car.h;
  for (const w of wheels) w.children.forEach(m => m.rotation.z -= car.v * dt / .33);
  wheels[0].rotation.y = wheels[1].rotation.y = -car.steer;
  for (const h of sigHeads) { const st = SIM.sigState(h.node, ST.t)[h.s.axis]; ['r', 'y', 'g'].forEach((c, i) => { h.lens[i].material.emissiveIntensity = st === c ? (night ? 4 : 2.2) : .04 }) }
  camTarget.lerp(v3.set(car.x + Math.cos(car.h) * car.v * .6, 0, car.y + Math.sin(car.h) * car.v * .6), Math.min(1, dt * 3));
  let cam = camO;
  if (mode === 'game') placeGameCam();
  else if (mode === 'chase') { cam = camP; const back = v3.set(car.x - Math.cos(car.h) * 11, 5.2, car.y - Math.sin(car.h) * 11); camP.position.lerp(back, Math.min(1, dt * 4)); camP.lookAt(car.x + Math.cos(car.h) * 6, 1.2, car.y + Math.sin(car.h) * 6) }
  else { cam = camP; orbit.update() }
  renderer.render(scene, cam);
  frames++; frameN++; if (now - fpsT > 1000) { fps = frames * 1000 / (now - fpsT); frames = 0; fpsT = now; const i = renderer.info.render; $('fps').textContent = fps.toFixed(0); $('calls').textContent = i.calls; $('tris').textContent = (i.triangles / 1000).toFixed(0) + 'K' }
  $('speed').textContent = Math.abs(car.v * 3.6).toFixed(0); const hh = Math.floor(ST.clock), mm = Math.floor((ST.clock - hh) * 60); $('clock').textContent = String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0');
  if (frameN % 6 === 0) drawMini();
  requestAnimationFrame(frame);
}
setMode('game'); setNight(/night/.test(location.hash)); if (low) setLow(true);
renderer.shadowMap.needsUpdate = true;
requestAnimationFrame(t => { last = t; frame(t); $('loading').hidden = true; window.TD.ready = true; window.TD.buildMs = Math.round(performance.now() - T0) });
// ממשק בדיקה
window.TD = { ready: false, wm: WM, setMode, setNight, setLow, sim: SIM, teleport: (x, y, h) => { car.x = x; car.y = y; if (h !== undefined) car.h = h; car.v = 0; camTarget.set(x, 0, y) }, zoom: v => ppm = v, rot: v => gameRot = v, frames: () => frameN };
window.__TD = () => { const i = renderer.info; return { ready: window.TD.ready, buildMs: window.TD.buildMs, calls: i.render.calls, tris: i.render.triangles, geos: i.memory.geometries, tex: i.memory.textures, lamps: W.lamps.length, trees: W.trees.length, palms: W.palms.length, signals: W.signals.length, litWindows: litCount, car: { x: +car.x.toFixed(1), y: +car.y.toFixed(1), v: +car.v.toFixed(2) }, mode, night, low } };
