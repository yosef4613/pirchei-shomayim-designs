// release_strip.js — nfkiss 17.11: שלב "שחרור" אחרי join_game — הסרת הערות JS / CSS / HTML מהבנייה שנמסרת (המקור לא משתנה).
// node release_strip.js <in.html> <out.html> [report.json]
// JS: לפי הניתוח של acorn (onComment — המיקום המדויק של כל הערה; מחרוזות, תבניות ו-regex לא נוגעים). הערת בלוק עם שורה חדשה → '\n'
//     (שומר על ASI), בלי שורה → ' '; הערת שורה → נמחקת עד סוף השורה (השורה נשארת). כל השאר — בית בבית כמו במקור.
//     סקריפט שלא נותח (שגיאת ניתוח) — נשאר כמו שהוא, ומדווח.
// CSS (<style>): סורק עם מחרוזות ("…" / '…') — הערות /* */ נמחקות. HTML: <!-- --> מחוץ ל-script / style נמחקות.
// שמות פנימיים (מזהים בלבד — אסימוני name של acorn, לא מחרוזות): RENAME — מזהה שהוא / מכיל מילה רגישה → שם ניטרלי, בכל הבנייה.
// בסוף: node --check לכל סקריפט אחרי ההסרה (כמו join_game).
const fs = require('fs'), path = require('path'), cp = require('child_process');
const acorn = require(path.join(__dirname, 'node', 'node_modules', 'acorn'));
const [inp, out, rep] = process.argv.slice(2);
if (!inp || !out) { console.error('usage: node release_strip.js <in.html> <out.html> [report.json]'); process.exit(2) }
let html = fs.readFileSync(inp, 'utf8');
// (17.11 סבב 2) הנתונים המקודדים: '^' + NV64 (המקור) → '~' + hex (0-9a-f) בבנייה המשוחררת — אותו מפענח (009b:tcNv64). חתיכות hex עברו אצל הבעלים, NV64 — לא תמיד.
const NV64 = 'bcdfghjklmnpqrstvwzBCDFGHJKLMNPQRSTVWZ26789-_.~!*()$@#%&;:,=|?]+', B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
const NVMAP = {}; for (let i = 0; i < 64; i++) NVMAP[NV64[i]] = B64[i];
const HEXN = { strings: 0, b64chars: 0, hexchars: 0 };
html = html.replace(new RegExp('"\\^([' + NV64.replace(/[\]\\^-]/g, '\\$&') + ']{200,})"', 'g'), (m, body) => {
  let b = ''; for (const c of body) b += NVMAP[c]; b += '===='.slice(b.length % 4 || 4);
  const hx = Buffer.from(b, 'base64').toString('hex'); if (Buffer.from(hx, 'hex').toString('base64') !== b) throw new Error('hex round-trip');
  HEXN.strings++; HEXN.b64chars += b.length; HEXN.hexchars += hx.length; return '"~' + hx + '"' });
const SHORTEN = ['G77_OT_CHG'];   // (סבב 2) יומן השינויים: כל ערך → רק המזהים שבו (p441 · p442 …) — F9 ממשיך להציג אותם
const RENAME = { cum: 'cuLen', noseX: 'nozX', visExit: 'visOut', g2SExit: 'g2SOut' };
const R = { renamed: {}, scripts: 0, parsed: 0, failed: [], jsComments: 0, jsCommentChars: 0, cssComments: 0, cssCommentChars: 0, htmlComments: 0, htmlCommentChars: 0 };

function stripJs(code, idx) {
  const cm = [];
  let ok = false, srcType = 'script', ast = null;
  for (const sourceType of ['script', 'module']) {
    srcType = sourceType;
    cm.length = 0;
    try { ast = acorn.parse(code, { ecmaVersion: 'latest', sourceType, allowHashBang: true, allowReturnOutsideFunction: true, onComment: (block, text, start, end) => cm.push([block, start, end]) }); ok = true; break }
    catch (e) { if (sourceType === 'module') R.failed.push({ script: idx, err: String(e.message).slice(0, 200) }) }
  }
  if (!ok) return code;
  R.parsed++;
  const ed = [];
  for (const [block, s, e] of cm) { const t = code.slice(s, e); R.jsComments++; R.jsCommentChars += t.length; ed.push([s, e, block ? (/[\n\r\u2028\u2029]/.test(t) ? '\n' : ' ') : '']) }
  for (const tk of acorn.tokenizer(code, { ecmaVersion: 'latest', sourceType: srcType, allowHashBang: true, allowReturnOutsideFunction: true })) {
    if (tk.type.label === 'name' && Object.prototype.hasOwnProperty.call(RENAME, tk.value)) { ed.push([tk.start, tk.end, RENAME[tk.value]]); R.renamed[tk.value] = (R.renamed[tk.value] || 0) + 1 }
  }
  const decls = []; (function walk(n) { if (!n || typeof n.type !== 'string') return; if (n.type === 'VariableDeclarator' && n.id && SHORTEN.includes(n.id.name)) decls.push(n);
    for (const k in n) { const v = n[k]; if (Array.isArray(v)) v.forEach(walk); else if (v && typeof v.type === 'string') walk(v) } })(ast);
  { for (const d of decls) { if (!d.init || d.init.type !== 'ObjectExpression') continue;
      for (const pr of d.init.properties) { const v = pr.value; if (!v || v.type !== 'Literal' || typeof v.value !== 'string') continue;
        const ids = [...new Set(v.value.match(/\bp\d{2,4}[a-z0-9_]*/g) || [])]; const nv = ids.length ? ids.join(' · ') : '—';
        ed.push([v.start, v.end, JSON.stringify(nv)]); R.shortened = (R.shortened || 0) + 1; R.shortChars = (R.shortChars || 0) + v.value.length - nv.length } } }
  // the comments inside a shortened value are already gone with it — drop edits inside a replaced range
  ed.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
  for (let i = 1; i < ed.length; i++) if (ed[i][0] < ed[i - 1][1]) { ed.splice(i, 1); i-- }
  let o = '', at = 0;
  for (const [s, e, rep] of ed) { if (s < at) throw new Error('overlap at ' + s); o += code.slice(at, s) + rep; at = e }
  return o + code.slice(at);
}
function stripCss(css) {
  let o = '', i = 0, n = css.length;
  while (i < n) {
    const c = css[i];
    if (c === '"' || c === "'") { let j = i + 1; while (j < n && css[j] !== c) { if (css[j] === '\\') j++; j++ } o += css.slice(i, j + 1); i = j + 1; continue }
    if (c === '/' && css[i + 1] === '*') { const j = css.indexOf('*/', i + 2); const e = j < 0 ? n : j + 2; R.cssComments++; R.cssCommentChars += e - i; i = e; continue }
    o += c; i++;
  }
  return o;
}
// HTML: walk the document, script / style raw text by their closing tag
let o = '', i = 0, si = 0;
const re = /<(script|style)\b[^>]*>|<!--/gi;
while (true) {
  re.lastIndex = i; const m = re.exec(html);
  if (!m) { o += html.slice(i); break }
  o += html.slice(i, m.index);
  if (m[0] === '<!--') { const j = html.indexOf('-->', m.index + 4); const e = j < 0 ? html.length : j + 3; R.htmlComments++; R.htmlCommentChars += e - m.index; i = e; continue }
  const tag = m[1].toLowerCase(), open = m[0], bodyStart = m.index + open.length;
  const close = html.toLowerCase().indexOf('</' + tag, bodyStart);
  const body = html.slice(bodyStart, close);
  let nb = body;
  if (tag === 'style') nb = stripCss(body);
  else { const ty = (open.match(/\btype\s*=\s*["']?([^"'\s>]+)/i) || [])[1]; R.scripts++;
    if (!ty || /javascript|module|ecmascript/i.test(ty)) nb = stripJs(body, si); si++ }
  o += open + nb; i = close;
}
fs.writeFileSync(out, o);
// syntax check of every script after the stripping
const chk = path.join(path.dirname(path.resolve(out)), '_strip_check'); fs.mkdirSync(chk, { recursive: true });
fs.writeFileSync(path.join(chk, 'package.json'), '{"type": "commonjs"}\n');
let k = 0, bad = 0; const sre = /<script[^>]*>([\s\S]*?)<\/script>/g; let mm;
while ((mm = sre.exec(o))) { const p = path.join(chk, 'c' + k + '.js'); fs.writeFileSync(p, mm[1]); const r = cp.spawnSync('node', ['--check', p], { encoding: 'utf8' }); if (r.status) { bad++; console.log('SYNTAX ERROR in script', k, (r.stderr || '').slice(0, 600)) } k++ }
fs.rmSync(chk, { recursive: true, force: true });
R.hex = HEXN; R.inBytes = Buffer.byteLength(html); R.outBytes = Buffer.byteLength(o); R.syntax = bad ? 'FAILED' : 'OK';
R.sha1 = require('crypto').createHash('sha1').update(o).digest('hex');
console.log(JSON.stringify(R));
if (rep) fs.writeFileSync(rep, JSON.stringify(R, null, 1));
process.exit(bad || R.failed.length ? 1 : 0);
