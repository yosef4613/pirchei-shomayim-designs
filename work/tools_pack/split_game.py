#!/usr/bin/env python3
"""split_game.py — פעם אחת (8.11.2026): מפרק בנייה של המשחק לקבצי מקור.
usage: split_game.py <game.html> <src_dir> <build_id>
- shell.html: כל הדף, וכל גוף של <script>/<style> מוחלף בשורת סימון ‎/*@@TC-PART <name>@@*/
- parts/NNN_<label>.js|.css: הגופים, לפי הסדר; הסקריפטים הגדולים מתחלקים בגבולות שורה (בלי לשנות סדר)
- manifest.json: הסדר, ולכל חלק — לאיזה גוף הוא שייך, sha1, אזורים עיקריים
- הקבוע BUILD (מזהה הבנייה) מוחלף ב-@@BUILD_ID@@ ו-join_game.py מחזיר אותו
"""
import sys, os, re, json, hashlib, collections
src, out, build_id = sys.argv[1], sys.argv[2], sys.argv[3]
h = open(src, encoding='utf-8').read()
assert h.count(build_id) == 1, 'build id must appear exactly once'
h = h.replace(build_id, '@@BUILD_ID@@')
Z = re.compile(r'\b([A-H][0-9])\b')
MARK = re.compile(r'^(/\*|//)|^(var|let|const|function|async function|class) ')
ZONEHEAD = re.compile(r'^(//|/\*)\s*=+\s*(v1\.\d+\s*·\s*)?(p\d{3}\w*\s*·\s*)?([A-H][0-9])\b')
TARGET, MAXSZ = 90_000, 160_000
os.makedirs(os.path.join(out, 'parts'), exist_ok=True)
parts, shell, pos, n = [], [], 0, 0
def label_of(lines):
    c = collections.Counter()
    for l in lines: c.update(Z.findall(l))
    top = [z for z, k in c.most_common(3) if k >= 8]
    tag = ''
    for l in lines[:60]:
        m = re.search(r'\b(p\d{3}[a-z0-9]*)\b', l)
        if m: tag = m.group(1); break
    return ('_'.join(top) or 'core') + ('_' + tag if tag else ''), [z for z, _ in c.most_common(6)]
def add(kind, body, block):
    global n
    n += 1
    lines = body.split('\n')
    lab, zones = label_of(lines) if kind == 'js' else ('style', [])
    name = '%03d_%s.%s' % (n, lab, kind)
    open(os.path.join(out, 'parts', name), 'w', encoding='utf-8', newline='').write(body)
    parts.append({'name': name, 'block': block, 'bytes': len(body.encode('utf-8')),
                  'sha1': hashlib.sha1(body.encode('utf-8')).hexdigest(), 'zones': zones})
    return name
blk = 0
for m in re.finditer(r'(<(script|style)[^>]*>)(.*?)(</\2>)', h, flags=re.S):
    shell.append(h[pos:m.start(3)])
    body, kind = m.group(3), ('js' if m.group(2) == 'script' else 'css')
    blk += 1
    names = []
    if kind == 'js' and len(body) > MAXSZ:
        lines = body.split('\n'); cur, cursz = [], 0
        for i, l in enumerate(lines):
            boundary = MARK.match(l) is not None
            if cur and ((ZONEHEAD.match(l) and cursz > 20_000) or (boundary and cursz >= TARGET) or cursz >= MAXSZ * 1.6):
                names.append(add(kind, '\n'.join(cur) + '\n', blk)); cur, cursz = [], 0
            cur.append(l); cursz += len(l) + 1
        last = '\n'.join(cur)          # the last piece: no added newline
        names.append(add(kind, last, blk))
    else:
        names.append(add(kind, body, blk))
    shell.append('/*@@TC-BLOCK %d@@*/' % blk)
    pos = m.end(3)
shell.append(h[pos:])
open(os.path.join(out, 'shell.html'), 'w', encoding='utf-8', newline='').write(''.join(shell))
json.dump({'from': os.path.basename(src), 'from_sha1': hashlib.sha1(open(src, 'rb').read()).hexdigest(),
           'build_id_at_split': build_id, 'parts': parts}, open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('parts', len(parts), 'blocks', blk)
