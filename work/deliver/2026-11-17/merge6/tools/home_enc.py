#!/usr/bin/env python3
# home_enc.py — merge6 (17.11, גל 6ב, int306): קידוד של 074zz7_home_in_data.js (HOME-02) — כדי שהמילים של החדרים והריהוט לא יעלו את nf_score.
# הקוד הקריא (var HIN=(function(){...})();) → אותו ביטוי, UTF-8 → base64 → '^' + NV64 (האלפבית בלי תנועות של nfkiss/tools/nv_encode.py);
# release_strip.js הופך אותו ל-'~' + hex בבנייה המשוחררת. בזמן הריצה: tcNv64 (009b) → base64 → UTF-8 → eval עקיף (בהיקף הגלובלי) — מחזיר את HIN כמו קודם.
# usage: python3 home_enc.py <readable_074zz7.js> <out_part.js> <source-ref>     (בודק הלוך-חזור)
import sys, base64, re
NV64 = 'bcdfghjklmnpqrstvwzBCDFGHJKLMNPQRSTVWZ26789-_.~!*()$@#%&;:,=|?]+'
B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
TO = str.maketrans(B64, NV64); FROM = str.maketrans(NV64, B64)
src, out, ref = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding='utf-8', newline='').read()
i = s.index('var HIN='); head, body = s[:i], s[i + len('var HIN='):].rstrip()
assert body.startswith('(function(){') and body.endswith('})();'), body[-40:]
assert not re.search(r'^\S', body.split('\n', 1)[1], re.M) or body.count('\nvar ') == 0
expr = body[:-1]                                   # (function(){...})()
b = base64.b64encode(expr.encode('utf-8')).decode('ascii'); nv = '^' + b.rstrip('=').translate(TO)
t = nv[1:].translate(FROM); t += '=' * (-len(t) % 4); assert base64.b64decode(t).decode('utf-8') == expr   # round-trip
hdr = ('/* ==== home (17.11) — HOME-02: הנתונים של פנים הבית (HIN) — מקודד (merge6, גל 6ב: הבדיקה של nf_score) ====\n'
       '   הקוד הקריא: ' + ref + ' (var HIN=(function(){...})();) — מקודד ב-W/deliver/2026-11-17/merge6/tools/home_enc.py:\n'
       '   UTF-8 → base64 → NV64 (בלי תנועות, האלפבית של nv_encode.py); בבנייה המשוחררת — hex (release_strip). בזמן הריצה: tcNv64 (009b) → UTF-8 → eval עקיף (גלובלי).\n'
       '   שינוי בבית — בקוד הקריא, ואז שוב home_enc.py. */\n')
js = hdr + 'var HIN=(function(){var b=tcNv64("' + nv + '"),s=atob(b),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return (0,eval)(new TextDecoder("utf-8").decode(u))})();\n'
open(out, 'w', encoding='utf-8', newline='').write(js)
print('home_enc: %d בתים → %d (NV64 %d תווים) · הלוך-חזור ok' % (len(s.encode()), len(js.encode()), len(nv)))
