#!/usr/bin/env python3
# vis_text.py <page.html> — הטקסט שרואים בדף (בלי style, ‏script ותגיות), לבדיקת העברית: python3 vis_text.py p.html | python3 tools_pack/heb_check.py
import sys, re, html
s = open(sys.argv[1], encoding='utf-8').read()
s = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', s, flags=re.S | re.I)
s = re.sub(r'<[^>]+>', ' ', s)
print(html.unescape(s))
