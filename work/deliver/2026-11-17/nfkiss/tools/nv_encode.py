#!/usr/bin/env python3
# nv_encode.py — nfkiss 17.11: קידוד "בלי תנועות" לנתונים המקודדים בבנייה (כדי שלא ייווצרו מילים אקראיות בתוך הנתונים).
#  base64 (הקול 029k / 074zf / 074zv, הלוגו 009a): כל מחרוזת base64 (100+ תווים) → '^' + אותו תוכן באלפבית NV64 (64 סימנים, בלי a e i o u x y
#    ובלי 0 1 3 4 5), בלי '=' בסוף. המפענח: tcNv64 (009b) — מחזיר את ה-base64 הרגיל (מחרוזת בלי '^' — כמו שהיא).
#  המותגים (074m / ‏074m6, הנתיבים של TCB): החלפת תו-בתו של האלפבית של TCB (91 תווים, ASCII 35–126 בלי '\') באלפבית TCB_ALPH2 (בלי תנועות;
#    14 התווים הנדירים — סימנים לטיניים של 2 בתים). המפענח: TCB.dec (074m) עם ALPH2.
# usage: python3 nv_encode.py <parts dir> [--check]   (בודק הלוך-חזור לכל מחרוזת, ואורך / sha1 של התוכן המפוענח)
import sys, os, re, hashlib, collections, json
NV64 = 'bcdfghjklmnpqrstvwzBCDFGHJKLMNPQRSTVWZ26789-_.~!*()$@#%&;:,=|?]+'
B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
assert len(NV64) == 64 == len(set(NV64)) and not set(NV64) & set('aeiouxyAEIOUXY01345"\\\'<>^')
TO = str.maketrans(B64, NV64); FROM = str.maketrans(NV64, B64)
OLD_ALPH = ''.join(chr(c) for c in range(35, 127) if c != 92)
ASCII2 = [chr(c) for c in range(33, 127) if chr(c) not in '"\\<@' + 'aeiouxyAEIOUXY']   # בלי '@' (במקור '@@' נכתב ‎@\\u0040‎)
LAT = list('¡¢£¤¥¦§©«®°±¶·¬')
JSU = re.compile(r'\\u([0-9a-fA-F]{4})')
def jsdec(d):
    t = JSU.sub(lambda m: chr(int(m.group(1), 16)), d).replace('\\/', '/'); assert '\\' not in t, d[:80]; return t
assert len(ASCII2) + len(LAT) == 91
def nv(s):
    return '^' + s.rstrip('=').translate(TO)
def un(s):
    t = s[1:].translate(FROM); return t + '=' * (-len(t) % 4)
P = sys.argv[1]; check = '--check' in sys.argv
rep = {}
B64RE = re.compile(r'"([A-Za-z0-9+/]{100,}={0,2})"')
for f in ('009a_opening_logo_data.js', '029k_voice_rec_data.js', '074zf_story_vrec_data.js', '074zv_side_vrec_data.js'):
    p = os.path.join(P, f); s = open(p, encoding='utf-8', newline='').read()
    n = 0; h0 = hashlib.sha1(); h1 = hashlib.sha1()
    def rp(m):
        global n
        b = m.group(1); e = nv(b); assert un(e) == b; assert not re.search('[aeiouxyAEIOUXY]', e)
        h0.update(b.encode()); h1.update(un(e).encode()); n += 1
        return '"' + e + '"'
    t = B64RE.sub(rp, s)
    assert h0.hexdigest() == h1.hexdigest()
    rep[f] = {'strings': n, 'before': len(s.encode()), 'after': len(t.encode()), 'sha1_b64': h0.hexdigest()[:12]}
    if not check: open(p, 'w', encoding='utf-8', newline='').write(t)
# brands: the frequency of each TCB symbol → the most frequent get the ASCII ones
LRE = re.compile(r'(\["#[0-9a-fA-F]{3,8}",")([^"]*)("\])')
fq = collections.Counter()
for f in ('074m_brands_data.js', '074m6_brands6_data.js'):
    s = open(os.path.join(P, f), encoding='utf-8').read()
    for m in LRE.finditer(s): fq.update(jsdec(m.group(2)))
assert set(fq) <= set(OLD_ALPH), set(fq) - set(OLD_ALPH)
order = sorted(range(91), key=lambda i: -fq.get(OLD_ALPH[i], 0))
new = [None] * 91
for rank, i in enumerate(order): new[i] = ASCII2[rank] if rank < len(ASCII2) else LAT[rank - len(ASCII2)]
ALPH2 = ''.join(new); assert len(set(ALPH2)) == 91
TB = str.maketrans(OLD_ALPH, ALPH2); TBR = str.maketrans(ALPH2, OLD_ALPH)
for f in ('074m_brands_data.js', '074m6_brands6_data.js'):
    p = os.path.join(P, f); s = open(p, encoding='utf-8', newline='').read(); n = [0]
    def rb(m):
        d = jsdec(m.group(2)); e = d.translate(TB); assert '@' not in e and '"' not in e and '\\' not in e; assert e.translate(TBR) == d; n[0] += 1
        return m.group(1) + e + m.group(3)
    t = LRE.sub(rb, s)
    rep[f] = {'paths': n[0], 'before': len(s.encode()), 'after': len(t.encode())}
    if not check: open(p, 'w', encoding='utf-8', newline='').write(t)
rep['TCB_ALPH2'] = ALPH2
print(json.dumps(rep, ensure_ascii=False, indent=1))
