// 17.11 · portraits — דף הציור (כלל 13): כל הדיוקנאות + משפחות הכרטיסים, SVG סטטי שנוצר מאותו קוד של המשחק (074zp_portraits.js, בין הסימונים POR-CORE).
// node mk_page.js <src_game_dir> <por.json (מ-por_check.js)> <out.html>
const fs = require('fs'), path = require('path'), vm = require('vm');
const [src, pj, out] = process.argv.slice(2);
const part = fs.readFileSync(path.join(src, 'parts/074zp_portraits.js'), 'utf8');
const core = part.split('/*@@POR-CORE@@*/')[1].split('/*@@POR-CORE-END@@*/')[0];
const p055 = fs.readFileSync(path.join(src, 'parts/055_G2_F2_p296.js'), 'utf8');
const ico = p055.match(/^function g77MsgIco\(k\)\{[\s\S]*?\}\)\[k\]\|\|''\}/m)[0];
const ctx = {}; vm.createContext(ctx); vm.runInContext(ico + '\n' + core + '\n;this.TCPOR=TCPOR;this.tcPorLook=tcPorLook;this.tcPorDraw=tcPorDraw;this.TCPOR_FAM=TCPOR_FAM;this.tcPorEsc=tcPorEsc;this.tcPorFamIc=tcPorFamIc', ctx);
const all = JSON.parse(fs.readFileSync(pj, 'utf8')).all;
const svg = (id, C, px) => '<svg viewBox="0 0 64 64" width="' + px + '" height="' + px + '">' + ctx.tcPorDraw(C.look || ctx.tcPorLook(id, C)) + '</svg>';
const AGE = { boy: 'נער', man: 'גבר', elder: 'מבוגר' }, HAT = { kippah: 'כיפה', cap: 'כובע מצחייה', hard: 'קסדת עבודה', helmet: 'קסדת כבאי', police: 'כובע שוטר', pilot: 'כובע טייס', chef: 'כובע שף', bucket: 'כובע דייגים', straw: 'כובע קש', beanie: 'כובע גרב', none: 'בלי כובע' };
const story = all.filter(c => /^st-|^s9-yossi|^s9-avi|^s9-moshe/.test(c.id) && c.id !== 'st-test');
const zones = all.filter(c => !story.includes(c) && c.id !== 'st-test');
const card = c => { const L = c.look; const sub = L.thing ? 'סמל: ' + L.thing : [AGE[L.age], HAT[L.hat]].filter(Boolean).join(' · ');
  return '<figure><div class="ring">' + svg(c.id, c, 88) + '</div><figcaption><b>' + ctx.tcPorEsc(c.name) + '</b><small>' + ctx.tcPorEsc(sub) + '</small><code>' + ctx.tcPorEsc(c.id) + '</code></figcaption></figure>' };
const fams = Object.entries(ctx.TCPOR_FAM).map(([k, F]) => '<div class="fam" style="--fam:' + F[0] + '">' + ctx.tcPorFamIc(k, 40) + '<b>' + F[1] + '</b><code>' + k + '</code></div>').join('');
const html = `<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>דיוקנאות אנשי הקשר</title>
<style>:root{--bg:#0b141c;--card:#132230;--ink:#eef5fa;--mut:#9fb0bd;--line:#ffffff1a}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 "Segoe UI",Arial,sans-serif;padding:16px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:26px 0 10px;color:#ffd36a}p{color:var(--mut);margin:4px 0;max-width:900px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 8px;text-align:center}
.ring{width:88px;height:88px;margin:0 auto 6px;border-radius:50%;overflow:hidden;box-shadow:inset 0 0 0 2px #ffffff30,0 3px 10px #0007}.ring svg{display:block}
figcaption b{display:block}figcaption small{display:block;color:var(--mut);font-size:12px}figcaption code{font-size:10px;color:#6f8696}
.fams{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}.fam{display:flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--line);border-inline-start:5px solid var(--fam);border-radius:12px;padding:10px}.fam code{margin-inline-start:auto;font-size:10px;color:#6f8696}
.tcFamIc{flex:none;display:inline-grid;place-items:center;border-radius:10px;background:var(--fam);box-shadow:0 2px 6px #0005}
.where{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}.where div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px}</style></head><body>
<h1>דיוקנאות אנשי הקשר — טורבו סיטי</h1>
<p>כל דיוקן מצויר בקוד (SVG), בלי שום תמונה. אותו איש — אותו פרצוף בכל מקום: בהודעות, בראש השיחה, בשיחה הנכנסת, ברשימת השיחות, באנשי הקשר, בחלון השיחה ובכרטיסי הסיפור. החולצה — בצבע של הדמות. מקום (מועדון, דואר, בית זיקוק) — סמל במקום פרצוף.</p>
<p>${all.length} אנשי קשר במשחק: ${all.filter(c => !c.look.thing).length} דיוקנאות, ${all.filter(c => c.look.thing).length} סמלים של מקומות.</p>
<h2>איפה זה מופיע</h2><div class="where"><div><b>הודעות</b><br>ברשימה ובראש השיחה (במקום האות הראשונה)</div><div><b>שיחה נכנסת</b><br>דיוקן גדול בכרטיס הצלצול</div><div><b>שיחות</b><br>דיוקן בכל שורה + "אנשי קשר" — כל מי שכתב או התקשר</div><div><b>חלון השיחה</b><br>פנים אל פנים ובטלפון</div><div><b>כרטיסי הסיפור</b><br>מי נתן את המשימה, ובכרטיס הסיפור של המקום</div><div><b>כרטיסי העבודות</b><br>פס וסמל בצבע המשפחה, וסמל בראש כל קבוצה</div></div>
<h2>הסיפור הראשי</h2><div class="grid">${story.map(card).join('')}</div>
<h2>הסיפורים של האזורים</h2><div class="grid">${zones.map(card).join('')}</div>
<h2>משפחות הכרטיסים — צבע וסמל</h2><div class="fams">${fams}</div>
</body></html>`;
fs.writeFileSync(out, html); console.log('page', out, html.length, 'bytes', all.length, 'contacts', 'data:image', html.split('data:image').length - 1, '<img', html.split('<img').length - 1);
