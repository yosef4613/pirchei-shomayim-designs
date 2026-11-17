#!/usr/bin/env python3
"""join_game.py — הבנייה של המשחק מקבצי המקור (מ-8.11.2026, במקום שרשרת הטלאים).
usage: BUILD_SUFFIX=-s7f266 python3 tools_pack/join_game.py [src_dir] out.html
- מחבר את shell.html עם החלקים שב-manifest.json, לפי הסדר, ומחזיר את מזהה הבנייה (BUILD_BASE + BUILD_SUFFIX, או BUILD_ID).
- בודק תחביר של כל סקריפט ב-node --check (כמו build_s6r.py), ומדפיס sha1 וגודל.
- חלק חדש: קובץ ב-parts/ ושורה ב-manifest.json במקום שלו בסדר ("block" — לאיזה גוף הוא שייך).
"""
import sys, os, re, json, hashlib, subprocess
args = sys.argv[1:]
src = args[0] if len(args) == 2 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src_game')
out = args[-1]
man = json.load(open(os.path.join(src, 'manifest.json'), encoding='utf-8'))
shell = open(os.path.join(src, 'shell.html'), encoding='utf-8', newline='').read()
blocks = {}
for p in man['parts']:
    blocks.setdefault(p['block'], []).append(open(os.path.join(src, 'parts', p['name']), encoding='utf-8', newline='').read())
def fill(m):
    return ''.join(blocks.pop(int(m.group(1))))
html = re.sub(r'/\*@@TC-BLOCK (\d+)@@\*/', fill, shell)
assert not blocks, 'parts without a block marker: %s' % sorted(blocks)
bid = os.environ.get('BUILD_ID') or (man['build_base'] + os.environ.get('BUILD_SUFFIX', ''))
assert html.count('@@BUILD_ID@@') == 1
html = html.replace('@@BUILD_ID@@', bid)
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
open(out, 'w', encoding='utf-8', newline='').write(html)
chk = os.path.join(os.path.dirname(os.path.abspath(out)), '_join_check')
os.makedirs(chk, exist_ok=True)
if not os.path.exists(os.path.join(chk, 'package.json')):
    open(os.path.join(chk, 'package.json'), 'w').write('{"type": "commonjs"}\n')
ok = True
for i, s in enumerate(re.findall(r'<script[^>]*>(.*?)</script>', html, flags=re.S)):
    p = os.path.join(chk, 'c%d.js' % i)
    open(p, 'w', encoding='utf-8').write(s)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode:
        ok = False; print('SYNTAX ERROR in script', i, r.stderr[:1500])
b = html.encode('utf-8')
print('join_game · %d parts · id %s · %s bytes · sha1 %s · syntax %s -> %s' % (
    len(man['parts']), bid, format(len(b), ','), hashlib.sha1(b).hexdigest()[:12], 'OK' if ok else 'FAILED', out))
sys.exit(0 if ok else 1)
