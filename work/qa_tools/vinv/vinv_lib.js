// vinv_lib.js — ספריית המלאי (נטענת לתוך המשחק דרך probe_c2.js; הקובץ הזה הוא חלק מהביטוי שנשלח)
// מתקין עטיפה על a.draw של כל נכס רכב (Vehicles, Heavy & Service Vehicles) ומריץ את כל פונקציות הציור של העולם
// על קנבס קטן עם טרנספורמציה של זהות (קואורדינטות עולם), VIEW_OVR על כל העולם — כך כל רכב שמצויר נרשם עם המקור שלו.
var VINV = window.VINV || (window.VINV = (function () {
  const VCAT = new Set(['Vehicles', 'Heavy & Service Vehicles']);
  const S = { on: false, rec: [], src: '', stackOn: true };
  const ACAT = new Map(); for (const a of TurboCity.assets) ACAT.set(a.id, a);
  let inTC = 0;
  function rec(c, a, lw, lh, how, sc) {
    const M = c.getTransform(), x = M.a * lw + M.c * lh + M.e, y = M.b * lw + M.d * lh + M.f, fp = a.fp || [0, 0, a.w, a.h];
    const L = fp[2] * sc * Math.hypot(M.a, M.b), W = fp[3] * sc * Math.hypot(M.c, M.d);
    let st = '';
    if (S.stackOn) { const L = String(new Error().stack).split('\n').slice(3, 14).map(l => (l.match(/at (?:Object\.|Array\.)?([A-Za-z0-9_$.<>]+) /) || [, '?'])[1]).filter(n => !/^(draw|Object\.draw|eval|\?|rec|TurboCity\.draw)$/.test(n)); st = L.slice(0, 5).join('<'); }
    S.rec.push({ src: S.src, asset: a.id, cat: a.cat, x: Math.round(x), y: Math.round(y), h: +Math.atan2(M.b, M.a).toFixed(3), al: +(c.globalAlpha).toFixed(2), L: +L.toFixed(1), W: +W.toFixed(1), how, st });
  }
  // (1) TurboCity.draw — the common path (the sprite cache sits under it, so a.draw is not called on a cache hit)
  if (!TurboCity.__vinv) { const d0 = TurboCity.draw; TurboCity.__vinv = 1;
    TurboCity.draw = function (c, id, x, y, o) { const a = S.on && ACAT.get(id);
      if (a && VCAT.has(a.cat)) { const sc = (o && o.scale) || 1; rec(c, a, x + a.w * sc / 2, y + a.h * sc / 2, 'TC', sc) }
      inTC++; try { return d0.apply(this, arguments) } finally { inTC-- } } }
  // (2) a.draw called directly (not through TurboCity.draw)
  for (const a of TurboCity.assets) {
    if (!VCAT.has(a.cat) || a.__vinv) continue;
    const f = a.draw; a.__vinv = 1;
    a.draw = function (c, St, t) { if (S.on && !inTC) { const sc = (St && St.scale) || 1; rec(c, a, a.w * sc / 2, a.h * sc / 2, 'direct', sc) } return f.apply(this, arguments) };
  }
  // the world's draw passes: (1) the static layers as WTC records them (WTC_MODE=1), (2) every live pass of render() (WTC_MODE=0)
  const STATIC = [['wtcPaintL1', n => wtcPaintL1(n)], ['wtcPaintLP', n => wtcPaintLP(n)], ['wtcPaintLO', n => wtcPaintLO(n)]];
  const LIVE = [
    ['wtcLiveUnder', n => wtcLiveUnder(n)], ['wtcLiveOver', n => wtcLiveOver(n)], ['wtcPropsLive', n => wtcPropsLive(n)], ['wtcCoolingLive', n => wtcCoolingLive(n)],
    ['b4Live', n => b4Live(n)], ['b3Live', n => b3Live(n)], ['c3Live', n => c3Live(n)], ['d3NLive', n => d3NLive(n)], ['c4NLive', n => c4NLive(n)], ['wtcAptLive', n => wtcAptLive(n)],
    ['drawFreightTrains', n => drawFreightTrains(n)], ['drawParkedCars', n => drawParkedCars(n)],
    ['drawTrafficCars', n => drawTrafficCars(n)], ['drawA4Fleet', n => { try { if (/drawA4Fleet\(now\)/.test(render.toString())) drawA4Fleet(n) } catch (e) {} }],   /* 2.11: רק כש-render() מצייר אותה (p494) */ ['drawFlowTrucks', n => drawFlowTrucks(n)], ['drawD4MovingSemis', n => drawD4MovingSemis(n)],
    ['D3LOOK.flushCars', n => { if (window.D3LOOK && D3LOOK.flushCars) D3LOOK.flushCars() }],
    ['drawBusLineVehicles', n => drawBusLineVehicles(n)], ['drawC5FleetCargo', n => drawC5FleetCargo(n)], ['drawActivityWorld', n => drawActivityWorld(n)],
    ['wtcOverLive', n => wtcOverLive(n)], ['D3LOOK.flushRoofs', n => { if (window.D3LOOK && D3LOOK.flushRoofs) D3LOOK.flushRoofs() }],
  ];
  function capture(now, o) {
    o = o || {};
    const g = document.createElement('canvas'); g.width = 32; g.height = 32; const G = g.getContext('2d'); G.setTransform(1, 0, 0, 1, 0, 0);
    const pc = ctx, pv = VIEW_OVR, pm = WTC_MODE, pcap = Targets.capture, pr = WTC.recording, pb = WTC.ctxBuilding, err = {}, ms = {};
    ctx = G; VIEW_OVR = { cx: 4800, cy: 3900, hw: 5400, hh: 5200 }; Targets.capture = []; S.rec = []; S.on = true; S.stackOn = o.stack !== false;
    const run = (list, mode) => { for (const [k, f] of list) { S.src = k; WTC_MODE = mode; const t0 = performance.now(); try { f(now) } catch (e) { err[k] = String(e && e.message || e).slice(0, 120) } ms[k] = Math.round(performance.now() - t0) } };
    try {
      if (o.static !== false) { WTC.recording = null; WTC.ctxBuilding = G; run(STATIC, 1); WTC.ctxBuilding = pb; WTC.recording = pr }
      if (o.live !== false) run(LIVE, 0);
    } finally { S.on = false; ctx = pc; VIEW_OVR = pv; WTC_MODE = pm; WTC.recording = pr; WTC.ctxBuilding = pb; var tg = Targets.capture; Targets.capture = pcap }
    // one row per drawn vehicle (a vehicle drawn twice at the same place by two passes — once)
    const seen = new Map(), U = [];
    for (const r of S.rec) { const k = r.asset + '@' + Math.round(r.x / 3) + ',' + Math.round(r.y / 3); const q = seen.get(k); if (q) { if (!q.srcs.includes(r.src)) q.srcs.push(r.src); continue } r.srcs = [r.src]; seen.set(k, r); U.push(r) }
    return { rec: U, raw: S.rec.length, err, ms, targets: tg };
  }
  function zone(x, y) { const z = tcZoneAt(x, y); return z ? z.code : '-' }
  function stepSim(sec) { const L = SIM_LOOP, H = L.h; if (L.simNow == null) L.simNow = performance.now(); const n = Math.round(sec / H); for (let i = 0; i < n; i++) { simStep(H, L.simNow + H * 1000); L.simNow += H * 1000 } return L.simNow }
  return { S, capture, zone, stepSim, STATIC, LIVE };
})());
