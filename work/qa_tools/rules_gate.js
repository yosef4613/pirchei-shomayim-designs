// 2.11 · rules_gate — הכללים של כרטיס הכללים (RULES_CARD.md) שהבדיקות של היום לא בדקו (הביקורת 2.11 05:30): כבישים כמו במפה (R-64),
// מפרץ בכל תחנה (R-63), התאים של תחנת הכיבוי והאמבולנסים לפי תנאי הקבלה (R-62), צייר אחד לחניות המיוחדות (R-54), מנחתים לפי טבלה (R-61).
// node rules_gate.js <game.html> <out.json>   — יוצא 1 כשכלל נשבר מעבר לקו הבסיס (tools_pack/rules_baseline.json: מה שעוד בעבודה, עם שם הממצא)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const base = JSON.parse(fs.readFileSync('/home/user/tc_root/tc/pkg/work/tools_pack/rules_baseline.json', 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const o={};
   o.stopsNoBay=ALL_BUS_STOPS.filter(s=>!s.terminal&&!s.bay).map(s=>s.id);
   o.stopsNearJunction=[];for(const s of ALL_BUS_STOPS){if(s.terminal)continue;let ok=null;try{if(s.F&&typeof busSiteJunctionOk==='function')ok=busSiteJunctionOk(s.F,s.dirSign)}catch(e){}
    if(ok==null){const e=byEdge[s.edgeId];if(!e)continue;const len=trafficEdgeLen(e),d=(s.t||0)*len;ok=Math.min(d,len-d)>=200+48}if(!ok)o.stopsNearJunction.push(s.id)}   /* 2.11 (כלל 10): 20 מ׳ מצומת */
   const A=roadAudit(false),C=A.checks||[];o.mapChecks=C.filter(c=>/map/.test(c.name)&&/road|stop|bus/.test(c.name)).map(c=>({name:c.name,ok:c.ok,detail:String(c.detail||'').slice(0,200)}));
   o.auditBad=C.filter(c=>!c.ok).map(c=>c.name);
   try{o.a4={fireBays:A4_FLEET_BAYS.filter(s=>s.fleet==='fire').length,fireUnits:A4_PARKED.filter(v=>v.ref==='FireTruck').length,emsBays:A4_FLEET_BAYS.filter(s=>s.fleet==='ems').length,emsUnits:A4_PARKED.filter(v=>v.ref==='Ambulance').length}}catch(e){o.a4={err:String(e)}}
   return o})()`));
  const fails = [], notes = [];
  const newNoBay = r.stopsNoBay.filter(id => !base.stopsNoBay.includes(id)); if (newNoBay.length) fails.push('תחנות חדשות בלי מפרץ: ' + newNoBay.join(', '));
  const newNear = (r.stopsNearJunction || []).filter(id => !(base.stopsNearJunction || []).includes(id)); if (newNear.length) fails.push('תחנות חדשות קרוב מ-20 מ׳ לצומת: ' + newNear.join(', '));
  if ((r.stopsNearJunction || []).length) notes.push((r.stopsNearJunction || []).length + ' תחנות קרוב מ-20 מ׳ לצומת בקו הבסיס: ' + r.stopsNearJunction.join(', '));
  if (r.stopsNoBay.length) notes.push(r.stopsNoBay.length + ' תחנות בלי מפרץ בקו הבסיס (R-63, בעבודה): ' + r.stopsNoBay.join(', '));
  for (const c of r.mapChecks) if (!c.ok) fails.push('הכבישים או התחנות לא כמו במפה: ' + c.name);
  if (!r.mapChecks.length) fails.push('אין בדיקה של הכבישים מול המפה');
  if (r.auditBad.length) fails.push('בדיקות העולם שנכשלו: ' + r.auditBad.join(', '));
  const a = r.a4 || {}; if (a.fireBays !== 5 || a.fireUnits !== 4 || a.emsBays !== 5 || a.emsUnits !== 4) fails.push('התאים של A4 לא לפי תנאי הקבלה: ' + JSON.stringify(a));
  notes.push('R-54 (צייר אחד לחניות המיוחדות) ו-R-61 (המנחתים) — עוד לא בבדיקה; נכנסים עם התיקון');
  const res = { ok: fails.length === 0, fails, notes, data: r, baseline: base };
  fs.writeFileSync(out, JSON.stringify(res, null, 1)); console.log(JSON.stringify({ ok: res.ok, fails, notes }, null, 1)); await b.close(); process.exit(res.ok ? 0 : 1);
})();
