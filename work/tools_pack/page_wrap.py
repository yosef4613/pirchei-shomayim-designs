#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3.11 · R-75 (הבעלים 09:26): כל קובץ שנשלח לבעלים מתפרסם גם בדף הקבוע שלו, עם אותו sha1 ואותו גודל.
שרת הדפים עוטף כל קובץ במעטפת של מסמך; קובץ שכבר עטוף במעטפת הזו מתפרסם כמו שהוא (נבדק 3.11 על התוכנית, המשחק והדוח היומי).
לכן: עוטפים כאן (המעטפת של דף התוכנית v6.47 — אותה מעטפת שהשרת שם), שולחים לבעלים את הקובץ העטוף, ומפרסמים את אותו קובץ.
usage:
  python3 page_wrap.py wrap <file.html> [<out_page.html>]            → out (ברירת מחדל: <file>_page.html), sha1, גודל
  python3 page_wrap.py log <page.html> <url> <the fixed page name>   → שורה ב-deliver/published.json (אחרי הפרסום)
  python3 page_wrap.py check <page.html>                              → exit 0 אם הקובץ נרשם כמפורסם עם אותו sha1"""
import sys, os, re, hashlib, json, datetime
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(W, 'tools_pack', 'page_shell_doc.bin')   # 8.11: the server's document shell, from the live plan page (the v6.47 page is not in the package)
LOG = os.path.join(W, 'deliver', 'published.json')
TAIL = b'\n</body></html>'
COVER = os.path.join(W, 'tools_pack', 'page_shell_cover.bin')   # 3.11: a document whose viewport asks viewport-fit=cover (the game) gets the server's "cover" shell
def shell(b=b''):
    if re.search(rb'<meta[^>]+name=["\']?viewport["\']?[^>]*viewport-fit=cover', b[:20000]): return open(COVER, 'rb').read()
    r = open(REF, 'rb').read(); i = r.index(b'<body>') + len(b'<body>'); return r[:i]
def unwrap(b):
    for sh in (open(COVER, 'rb').read(), shell()):
        if b.startswith(sh) and b.endswith(TAIL): return b[len(sh) + 1:-len(TAIL)]
    return b
def sha(b): return hashlib.sha1(b).hexdigest()
cmd = sys.argv[1]
if cmd == 'wrap':
    f = sys.argv[2]; b = unwrap(open(f, 'rb').read())                     # the server strips a known shell and wraps again — so do we
    page = shell(b) + b'\n' + b + TAIL
    out = sys.argv[3] if len(sys.argv) > 3 else (f[:-5] if f.endswith('.html') else f) + '_page.html'
    open(out, 'wb').write(page); print(out, sha(page)[:12], len(page))
elif cmd == 'log':
    p, url, name = sys.argv[2], sys.argv[3], sys.argv[4]; b = open(p, 'rb').read()
    L = json.load(open(LOG, encoding='utf-8')) if os.path.exists(LOG) else []
    L.append({'page': name, 'file': os.path.relpath(p, W), 'sha1': sha(b), 'size': len(b), 'url': url,
              'at': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%d.%m.%Y %H:%M')})
    json.dump(L, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('logged', name, sha(b)[:12], len(b))
elif cmd == 'check':
    p = sys.argv[2]; b = open(p, 'rb').read(); s = sha(b)
    L = json.load(open(LOG, encoding='utf-8')) if os.path.exists(LOG) else []
    ok = any(x['sha1'] == s for x in L); print(('פורסם' if ok else 'לא פורסם'), s[:12], len(b)); sys.exit(0 if ok else 1)
