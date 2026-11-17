#!/usr/bin/env python3
# chunk_words.py — nfkiss 17.11: לחלק את הבנייה בדיוק כמו tools_pack/split_any.py ולהדפיס לכל חלק מה יש בו
# (אילו קבצי parts, מילים / מחרוזות חריגות בעברית ובאנגלית, דפוסי JS "חשודים", כתובות, base64) — כדי להשוות חלקים שעברו לחלקים שנחסמו.
# usage:
#   python3 chunk_words.py <build.html> [--mb 1.3] [--src <src_game dir>] [--blocked 6,8,10,18,20] [--json out.json] [--top 12]
#   --src: ממפה כל חלק לקבצי parts/ (לפי manifest.json; בלי --src — מחפש את src_game לפי מזהה הבנייה, אחרת בלי מיפוי)
#   --pieces K: כל חלק נחתך ל-K חתיכות שוות (g6.1 … g6.K) — להשוואה מול בדיקת החתיכות (nftest); ‏--only 6,8 — רק החלקים האלה
#   --blocked: (גם 6.3 לחתיכה) מדפיס בסוף השוואה — מה נמצא בחלקים החסומים ואין / כמעט אין בחלקים שעברו (מילים, דפוסים, קבצים)
import sys, os, re, json, collections, argparse, hashlib
ap = argparse.ArgumentParser()
ap.add_argument('build'); ap.add_argument('--mb', type=float, default=1.3); ap.add_argument('--src')
ap.add_argument('--blocked', default=''); ap.add_argument('--pieces', type=int, default=1); ap.add_argument('--only', default=''); ap.add_argument('--json'); ap.add_argument('--top', type=int, default=12)
a = ap.parse_args()
s = open(a.build, encoding='utf-8').read()

# 1. החלוקה — אותו אלגוריתם בדיוק של split_any.py (בלוקים של 50,000 תווים, עד MB מ"ב לחלק)
maxb = int(a.mb * 1_000_000); chunks, cur, size, start, starts = [], [], 0, 0, []
pos = 0
for i in range(0, len(s), 50_000):
    blk = s[i:i+50_000]; bl = len(blk.encode('utf-8'))
    if size and size + bl > maxb: chunks.append(''.join(cur)); starts.append(start); cur, size, start = [], 0, i
    cur.append(blk); size += bl
if cur: chunks.append(''.join(cur)); starts.append(start)

# 2. מיפוי לקבצי parts (אופציונלי)
spans = []
src = a.src
if src and os.path.exists(os.path.join(src, 'manifest.json')):
    man = json.load(open(os.path.join(src, 'manifest.json'), encoding='utf-8')); at = 0
    for p in man['parts']:
        t = open(os.path.join(src, 'parts', p['name']), encoding='utf-8').read()
        k = s.find(t[:2000], at) if t else -1
        if k >= 0: spans.append((k, k + len(t), p['name'])); at = k + len(t)
def parts_in(c0, c1):
    out = []
    for k0, k1, nm in spans:
        o = min(k1, c1) - max(k0, c0)
        if o > 0: out.append((nm, o))
    return out

# 3. מה מחפשים
B64 = re.compile(r'[A-Za-z0-9+/]{100,}={0,2}')
WATCH_EN = ('kiss sex sexy girl girls boy love lover bikini swimsuit lingerie nude naked porn xxx adult escort strip stripper babe hot '
 'wine beer bar pub club nightclub vodka whisky whiskey alcohol liquor cocktail drunk casino poker gamble gambling bet betting lottery '
 'dating date hookup drug drugs weed cannabis tattoo dance disco party cross church christmas jesus god torrent proxy vpn hack crack '
 'kill dead death blood gun guns shoot shooting weapon bomb police prison jail terror fight war dog pig body model fashion dress '
 'beach swim pool spa massage hotel bed bath shower woman women lady ladies female male man men kid kids baby').split()
WATCH_HE = ('נשיקה נשיקות נשק סקס סקסי ביקיני בגד ים אהבה יין יינות בירה פאב מועדון דיסקו קזינו הימור הימורים לוטו היכרויות דייט אלכוהול וודקה '
 'ויסקי חשפנ עירום סמים קעקוע מסיבה כנסייה כנסיה צלב נצרות חג המולד בחורה בחורות נערה נערות אשה אישה נשים גבר גברים ילד ילדה ילדים תינוק '
 'רחצה חוף בריכה ספא עיסוי מלון מיטה מקלחת שחייה ים דגמנית אופנה שמלה רצח מוות דם אקדח נשק פצצה כלא משטרה מלחמה חזיר כלב גוף').split()
JS = {'eval(': r'\beval\s*\(', 'new Function': r'new\s+Function\s*\(', 'atob(': r'\batob\s*\(', 'btoa(': r'\bbtoa\s*\(',
      'fromCharCode': r'fromCharCode', 'unescape(': r'\bunescape\s*\(', 'document.write': r'document\.write', 'innerHTML': r'innerHTML',
      'WebAssembly': r'WebAssembly', 'Worker(': r'new\s+Worker\s*\(', 'Blob(': r'new\s+Blob\s*\(', 'createObjectURL': r'createObjectURL',
      'XMLHttpRequest': r'XMLHttpRequest', 'fetch(': r'\bfetch\s*\(', 'WebSocket': r'WebSocket', 'localStorage': r'localStorage',
      'indexedDB': r'indexedDB', 'navigator.': r'navigator\.', 'crypto': r'\bcrypto\b', '\\x escapes': r'\\x[0-9a-fA-F]{2}',
      '\\u escapes': r'\\u[0-9a-fA-F]{4}', 'data:': r'data:[a-z]+/', 'base64,': r'base64,', 'http://': r'http://', 'https://': r'https://',
      'iframe': r'<iframe', '<script': r'<script', 'onerror=': r'onerror\s*=', 'AudioContext': r'AudioContext', 'mp3/wav/ogg/opus': r'\.(?:mp3|wav|ogg|opus)\b'}
URL = re.compile(r'\b(?:https?://)?((?:[a-z0-9-]+\.)+(?:com|net|org|io|co|il|gov|edu|info|app|dev|ru|cn|xyz|me|tv|ly|gl))\b', re.I)
EN_TOK = re.compile(r'[A-Za-z]{3,}'); HE_TOK = re.compile(r'[א-ת]{2,}')
HEP = r'(?<![א-ת])[ובלהמש]{0,2}%s(?![א-ת])'

def analyse(c):
    b64 = [m.group() for m in B64.finditer(c)]; t = B64.sub(' ', c)
    en = collections.Counter(w.lower() for w in EN_TOK.findall(t)); he = collections.Counter(HE_TOK.findall(t))
    watch = {}
    for w in WATCH_EN:
        n = len(re.findall(r'(?<![A-Za-z])' + re.escape(w) + r'(?![A-Za-z])', t, re.I))
        if n: watch[w] = n
    for w in WATCH_HE:
        n = len(re.findall(HEP % re.escape(w), t))
        if n: watch[w] = n
    # צירופים מקריים בתוך base64 (בלי גבולות מילה)
    inb64 = collections.Counter()
    for w in ('kiss', 'sex', 'porn', 'xxx', 'nude', 'gay', 'fuck', 'shit', 'cum', 'tit', 'ass', 'dick', 'cock', 'pussy', 'slut', 'whore', 'nazi', 'jihad'):
        n = sum(len(re.findall(w, x, re.I)) for x in b64)
        if n: inb64[w] = n
    js = {k: len(re.findall(p, c)) for k, p in JS.items()}; js = {k: v for k, v in js.items() if v}
    urls = collections.Counter(m.group(1).lower() for m in URL.finditer(t))
    return {'bytes': len(c.encode('utf-8')), 'b64_runs': len(b64), 'b64_bytes': sum(map(len, b64)), 'b64_max': max(map(len, b64), default=0),
            'he_chars': len(re.findall(r'[א-ת]', c)), 'lines': c.count('\n'), 'watch': watch, 'in_b64': dict(inb64), 'js': js,
            'urls': dict(urls.most_common(20)), 'en_top': en.most_common(a.top), 'he_top': he.most_common(a.top), '_en': en, '_he': he, '_watch': watch}

blocked = {x.strip() for x in a.blocked.split(',') if x.strip()}
only = {int(x) for x in a.only.split(',') if x.strip()}
units = []
for i, c in enumerate(chunks, 1):
    if only and i not in only: continue
    if a.pieces <= 1: units.append((str(i), c, starts[i-1])); continue
    L = len(c); step = -(-L // a.pieces)
    for j in range(a.pieces): units.append(('%d.%d' % (i, j + 1), c[j*step:(j+1)*step], starts[i-1] + j*step))
res = []
for lab, c, st in units:
    i = lab
    r = analyse(c); r['n'] = lab; r['start'] = st; r['sha1'] = hashlib.sha1(c.encode('utf-8')).hexdigest()[:12]
    r['parts'] = [(nm, o) for nm, o in sorted(parts_in(st, st + len(c)), key=lambda x: -x[1])]
    res.append(r)
    isb = lab in blocked or lab.split('.')[0] in blocked
    flag = ' [חסום]' if isb else (' [עבר]' if blocked else '')
    print('=== g%s.txt%s · %s בתים · sha1 %s · base64: %d רצפים / %s תווים (הארוך %s) · עברית %s אותיות' % (
        i, flag, format(r['bytes'], ','), r['sha1'], r['b64_runs'], format(r['b64_bytes'], ','), format(r['b64_max'], ','), format(r['he_chars'], ',')))
    if r['parts']: print('  קבצים: ' + ', '.join('%s (%s)' % (nm, format(o, ',')) for nm, o in r['parts'][:8]) + (' …+%d' % (len(r['parts']) - 8) if len(r['parts']) > 8 else ''))
    if r['watch']: print('  מילים לבדיקה: ' + ', '.join('%s %d' % kv for kv in sorted(r['watch'].items(), key=lambda x: -x[1])))
    if r['in_b64']: print('  בתוך base64 (מקרי): ' + ', '.join('%s %d' % kv for kv in r['in_b64'].items()))
    if r['js']: print('  JS: ' + ', '.join('%s %d' % kv for kv in sorted(r['js'].items(), key=lambda x: -x[1])))
    if r['urls']: print('  כתובות: ' + ', '.join('%s %d' % kv for kv in r['urls'].items()))
    print('  אנגלית (הנפוצות): ' + ', '.join('%s %d' % kv for kv in r['en_top']))
    print('  עברית (הנפוצות): ' + ', '.join('%s %d' % kv for kv in r['he_top']))

if blocked:
    isb = lambda r: r['n'] in blocked or r['n'].split('.')[0] in blocked
    B = [r for r in res if isb(r)]; P = [r for r in res if not isb(r)]
    print('\n##### השוואה: חסומים %s מול עברו %d' % (sorted(blocked), len(P)))
    def cmp(key, label, minb=1):
        inb = collections.Counter(); inp = collections.Counter(); totb = collections.Counter(); totp = collections.Counter()
        for r in B:
            for w, n in r[key].items(): inb[w] += 1; totb[w] += n
        for r in P:
            for w, n in r[key].items(): inp[w] += 1; totp[w] += n
        rows = []
        for w in inb:
            fb = inb[w] / len(B); fp = inp[w] / max(1, len(P))
            if inb[w] >= minb and fb > fp: rows.append((fb - fp, w, inb[w], inp[w], totb[w], totp[w]))
        rows.sort(reverse=True)
        print('-- %s: בכמה חסומים / בכמה שעברו (מופעים בחסומים / בשעברו) — ממוין לפי ההפרש' % label)
        for d, w, nb, np_, tb, tp in rows[:40]: print('   %-28s %d/%d  מול  %d/%d   (%d / %d)' % (w, nb, len(B), np_, len(P), tb, tp))
    cmp('_watch', 'מילים לבדיקה')
    cmp('js', 'דפוסי JS')
    cmp('in_b64', 'צירופים בתוך base64')
    cmp('urls', 'כתובות')
    cmp('_en', 'כל המילים באנגלית (רק מה שבכל החסומים או ברובם)', minb=max(2, (len(B) + 1) // 2))
    cmp('_he', 'כל המילים בעברית (רק מה שבכל החסומים או ברובם)', minb=max(2, (len(B) + 1) // 2))
    for key, label in (('bytes', 'גודל'), ('b64_bytes', 'base64 (תווים)'), ('he_chars', 'אותיות עבריות')):
        avg = lambda L: sum(r[key] for r in L) / max(1, len(L))
        print('-- ממוצע %s: חסומים %s · עברו %s' % (label, format(int(avg(B)), ','), format(int(avg(P)), ',')))
    print('-- קבצים בחסומים: ' + '; '.join('g%s: %s' % (r['n'], ', '.join(nm for nm, o in r['parts'][:6])) for r in B))
if a.json:
    json.dump([{k: v for k, v in r.items() if not k.startswith('_')} for r in res], open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('json →', a.json)
