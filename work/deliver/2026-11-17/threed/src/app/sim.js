// הסימולציה — בלי שום ציור ובלי Three.js. מקבלת את נתוני העולם (b4_data.json) ומחזיקה את המצב: הרכב, הרמזורים, השעון.
// זה החלק שעובר לכל מצייר (2D של היום או תלת־ממד) — הבסיס ל-World Manager.
export function makeSim(DATA) {
  const solids = [];                     // מבנים — מלבנים שאסור לנסוע לתוכם
  for (const s of DATA.sites) if (s.kind === 'building') solids.push(s.rect);
  for (const c of DATA.context || []) solids.push(c.rect);
  const W = DATA.window;
  const signals = DATA.nodes.filter(n => n.kind === 'signal').map((n, i) => ({ id: n.id, p: n.p, off: i * 7 }));
  // מחזור רמזור: צפון–דרום ירוק 18 שנ׳, צהוב 3, אדום לכולם 1, מזרח–מערב ירוק 12, צהוב 3, אדום לכולם 1
  const CYC = [['NS', 'g', 18], ['NS', 'y', 3], ['-', 'r', 1], ['EW', 'g', 12], ['EW', 'y', 3], ['-', 'r', 1]];
  const CT = CYC.reduce((a, c) => a + c[2], 0);
  function sigState(sig, t) {
    let u = ((t + sig.off) % CT + CT) % CT;
    for (const [ax, col, d] of CYC) { if (u < d) return { NS: ax === 'NS' ? col : 'r', EW: ax === 'EW' ? col : 'r' }; u -= d }
    return { NS: 'r', EW: 'r' };
  }
  const car = { x: 57.9, y: 40, h: -Math.PI / 2, v: 0, steer: 0, L: 2.75, len: 4.6, wid: 1.84, hit: 0 };  // h: כיוון (0 = מזרח, ‎−π/2 = צפון)
  const st = { t: 0, clock: 16.3, car, signals, input: { up: 0, down: 0, left: 0, right: 0, brake: 0 } };
  function collides(x, y, h) {
    const c = Math.cos(h), s = Math.sin(h), hl = car.len / 2, hw = car.wid / 2;
    const pts = [[hl, hw], [hl, -hw], [-hl, hw], [-hl, -hw], [0, hw], [0, -hw]].map(([a, b]) => [x + a * c - b * s, y + a * s + b * c]);
    for (const r of solids) for (const [px, py] of pts) if (px > r[0] && px < r[2] && py > r[1] && py < r[3]) return true;
    return false;
  }
  function step(dt) {
    st.t += dt; st.clock = (st.clock + dt / 60) % 24;   // דקה במשחק לכל שנייה
    const I = st.input, maxV = 16, acc = 6.5, brk = 14, drag = 0.45;
    if (I.up) car.v += acc * dt; else if (I.down) car.v -= (car.v > 0.3 ? brk : acc * 0.6) * dt;
    if (I.brake) car.v -= Math.sign(car.v) * Math.min(Math.abs(car.v), brk * dt);
    car.v -= car.v * drag * dt * (I.up || I.down ? 0.2 : 1);
    car.v = Math.max(-5, Math.min(maxV, car.v)); if (Math.abs(car.v) < 0.02 && !I.up && !I.down) car.v = 0;
    const target = (I.left ? -1 : 0) + (I.right ? 1 : 0), maxS = 0.55 - Math.min(0.3, Math.abs(car.v) * 0.018);
    car.steer += (target * maxS - car.steer) * Math.min(1, dt * 6);
    const nh = car.h + car.v / car.L * Math.tan(car.steer) * dt;
    const nx = car.x + Math.cos(nh) * car.v * dt, ny = car.y + Math.sin(nh) * car.v * dt;
    const inWin = nx > W[0] - 60 && nx < W[2] + 60 && ny > W[1] - 60 && ny < W[3] + 60;
    if (!collides(nx, ny, nh) && inWin) { car.x = nx; car.y = ny; car.h = nh }
    else { car.v = -car.v * 0.25; car.hit = st.t }
  }
  return { st, step, sigState, collides, solids };
}
