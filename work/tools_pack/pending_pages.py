#!/usr/bin/env python3
"""pending_pages.py — אילו דפים מההחזרות עוד לא פורסמו (או השתנו מאז הפרסום האחרון).
סורק W/deliver/2026-11-1*/*/handback.txt, שורות "הציור מוכן" / "ניסיון לבעלים" / "ההצעה מוכנה",
ולכל קובץ .html שמוזכר בהן משווה את זמן השינוי שלו לפרסום האחרון של <קובץ>_page.html ב-published.json."""
import os, re, json, glob, datetime
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(W, 'deliver', 'published.json'), encoding='utf-8'))
last = {}
for e in L:
    t = datetime.datetime.strptime(e['at'], '%d.%m.%Y %H:%M')
    last[e['file']] = max(last.get(e['file'], t), t)
seen = set()
for hb in sorted(glob.glob(os.path.join(W, 'deliver', '2026-11-1*', '*', 'handback.txt'))):
    for ln in open(hb, encoding='utf-8', errors='replace'):
        if not re.search(r'הציור מוכן|ניסיון לבעלים|ההצעה מוכנה', ln): continue
        for m in re.findall(r'(?:W/)?(deliver/[\w\-./]+?\.html)', ln):
            if m in seen or m.endswith('_page.html'): continue
            seen.add(m); src = os.path.join(W, m)
            if not os.path.exists(src): print('חסר  ', m); continue
            pg = m[:-5] + '_page.html'
            mt = datetime.datetime.fromtimestamp(os.path.getmtime(src)) + datetime.timedelta(hours=2)  # שעון ישראל
            pub = last.get(pg)
            if pub is None: print('חדש  ', m, mt.strftime('%H:%M'))
            elif mt > pub + datetime.timedelta(minutes=1): print('השתנה', m, mt.strftime('%H:%M'), '> פורסם', pub.strftime('%H:%M'))
