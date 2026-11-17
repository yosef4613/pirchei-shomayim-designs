#!/usr/bin/env python3
"""manifest_tool.py — הרשימה של חלקי המשחק (src_game/manifest.json), 8.11.2026.
  refresh <src_dir>                    → מחשב מחדש לכל חלק: bytes, ‏sha1, ‏zones, ‏defines (מהקובץ עצמו). מריצים לפני כל commit שמשנה חלקים.
  merge <src_dir> <ours.json> <theirs.json> <base.json>
                                       → מיזוג של שלוש גרסאות של הרשימה: הסדר והחלקים מהשניים (חלק חדש נכנס אחרי החלק שלפניו בגרסה שהוסיפה אותו),
                                         שאר השדות (build_base וכו׳) — מ-ours, אלא אם רק theirs שינה אותם; ואז refresh. כותב ל-<src_dir>/manifest.json.
ההתנגשויות במיזוג באות מהשדות המחושבים (sha1, ‏defines) — לכן תמיד ממזגים בכלי הזה, לא ביד."""
import sys, os, re, json, hashlib, collections
Z = re.compile(r'\b([A-H][0-9])\b')
D = re.compile(r'^(?:var|let|const|function|async function|class)\s+([A-Za-z_$][\w$]*)', re.M)
def refresh(src, man):
    for p in man['parts']:
        t = open(os.path.join(src, 'parts', p['name']), encoding='utf-8', newline='').read()
        b = t.encode('utf-8'); p['bytes'] = len(b); p['sha1'] = hashlib.sha1(b).hexdigest()
        if p['name'].endswith('.js'):
            c = collections.Counter(Z.findall(t)); p['zones'] = [z for z, _ in c.most_common(6)]; p['defines'] = D.findall(t)[:400]
    return man
def merge(ours, theirs, base):
    bn = [p['name'] for p in base['parts']]; on = [p['name'] for p in ours['parts']]; tn = [p['name'] for p in theirs['parts']]
    gone = (set(bn) - set(on)) | (set(bn) - set(tn))
    order = [n for n in on if n not in gone]
    for i, n in enumerate(tn):                     # the parts that only theirs added: after their predecessor in theirs
        if n in order or n in gone: continue
        prev = next((tn[j] for j in range(i - 1, -1, -1) if tn[j] in order), None)
        order.insert(order.index(prev) + 1 if prev else 0, n)
    byname = {p['name']: p for p in base['parts']}; byname.update({p['name']: p for p in theirs['parts']}); byname.update({p['name']: p for p in ours['parts']})
    out = {k: v for k, v in ours.items() if k != 'parts'}
    for k, v in theirs.items():
        if k != 'parts' and base.get(k) == ours.get(k) and v != base.get(k): out[k] = v
    out['parts'] = [dict(byname[n]) for n in order]
    return out
if __name__ == '__main__':
    cmd, src = sys.argv[1], sys.argv[2]
    if cmd == 'refresh':
        m = refresh(src, json.load(open(os.path.join(src, 'manifest.json'), encoding='utf-8')))
    else:
        L = lambda f: json.load(open(f, encoding='utf-8'))
        m = refresh(src, merge(L(sys.argv[3]), L(sys.argv[4]), L(sys.argv[5])))
    json.dump(m, open(os.path.join(src, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('manifest:', len(m['parts']), 'חלקים')
