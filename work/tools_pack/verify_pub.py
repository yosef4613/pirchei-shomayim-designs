#!/usr/bin/env python3
"""verify_pub.py <saved_index.html> <local_page.html> — משווה את הגוף (אחרי </head><body> הראשון), כי השרת עשוי להחליף את הכותרת שלו."""
import sys
a=open(sys.argv[1],'rb').read(); b=open(sys.argv[2],'rb').read()
if a==b: print('SAME'); sys.exit(0)
k=b'</head><body>'
try:
    print('BODY-SAME' if a[a.index(k)+len(k):]==b[b.index(k)+len(k):] else 'DIFF')
except ValueError: print('DIFF')
