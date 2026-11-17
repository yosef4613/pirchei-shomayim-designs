#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""full_set_summary.py <outdir> [base_outdir] — הסיכום בעברית של full_set.sh (בונה S7F266, 8.11).
לכל בדיקה: עובר / נכשל, והמספרים שלה. עם base_outdir — טבלת השוואה מול הבסיס: "אין החמרה" או "החמרה" לכל בדיקה.
החמרה = בדיקה שעברה בבסיס ונכשלת עכשיו, או מספר כישלונות שגדל. היציאה: מספר הבדיקות שנכשלו בריצה הזו."""
import sys, os, json, re
O = sys.argv[1]; B = sys.argv[2] if len(sys.argv) > 2 else None

def J(d, n):
    try: return json.load(open(os.path.join(d, n), encoding='utf-8'))
    except Exception: return None
def runs(d):
    r = {}
    try:
        for ln in open(os.path.join(d, 'runs.tsv'), encoding='utf-8'):
            p = ln.rstrip('\n').split('\t')
            if len(p) >= 2: r[p[0]] = int(p[1])
    except Exception: pass
    return r
def log(d, n):
    try: return open(os.path.join(d, n + '.log'), encoding='utf-8', errors='replace').read()
    except Exception: return ''

def collect(d):
    """בדיקה -> (עובר?, מספר הכישלונות, שורת פירוט)"""
    R = runs(d); out = {}
    g = J(d, 'ingame.json') or {}
    ra = g.get('roadAudit') or {}
    sub = [k for k, v in g.items() if isinstance(v, dict) and k not in ('roadAudit',) and v.get('ok') is False]
    out['ingame'] = (bool(ra.get('ok')) and not sub, len(ra.get('failed') or []) + len(sub),
                     'בדיקת הכבישים %s/%s עברו%s · בדיקות האזורים שנכשלו: %s' % (ra.get('passed'), ra.get('total'),
                     (' · נכשלו: ' + ' | '.join(ra.get('failed')[:6])) if ra.get('failed') else '', ', '.join(sub) if sub else 'אין') +
                     ' · חדשות של S7F266: ' + ', '.join('%s %s' % (k, 'עוברת' if (g.get(k) or {}).get('ok') else ('לא קיימת' if (g.get(k) or {}).get('missing') else 'נכשלת')) for k in ('pipe', 'texts')))
    r = J(d, 'rules.json') or {}
    out['rules'] = (bool(r.get('ok')), len(r.get('fails') or []), 'כישלונות: ' + (' | '.join(r.get('fails') or []) or 'אין'))
    lv = J(d, 'live.json') or {}
    Z = (lv.get('audit') or {}).get('zones') or {}
    badz = [z for z, v in Z.items() if not v.get('ok') and not v.get('exception')]
    still = [k + ':' + x for k, v in (lv.get('pixels') or {}).items() if isinstance(v, dict) for x in (v.get('still') or [])]
    out['live'] = (bool(lv.get('ok')), len(badz) + len(still), '%d אזורים · אזורים שנכשלו בספירה: %s · פרטים שלא זזו בבדיקת הפיקסלים: %d%s' % (len(Z), ', '.join(badz) or 'אין', len(still), (' (' + ', '.join(still[:8]) + (' …' if len(still) > 8 else '') + ')') if still else ''))
    i = 1
    while os.path.exists(os.path.join(d, 'people%d.json' % i)) or ('people%d' % i) in R:
        p = J(d, 'people%d.json' % i) or {}
        out['people%d' % i] = (bool(p.get('ok')), len(p.get('hits') or []), '%s דגימות · אנשים על נתיב: %d' % (p.get('samples'), len(p.get('hits') or [])))
        i += 1
    x = J(d, 'xw.json') or {}
    c1 = (x.get('check1') or {}); c2 = (x.get('check2') or {})
    out['xw'] = (bool(x.get('ok')), len(c1.get('fails') or []) + len(c2.get('fails') or []),
                 'זרועות %s, עם מעבר %s · מעברי המפה: קיימים %s, חסרים %d · נוספו %d, יצאו %d' % (c1.get('arms'), c1.get('xw'), c2.get('matched'), len(c2.get('fails') or []), len(x.get('added') or []), len(x.get('removed') or [])))
    s = J(d, 'signal.json') or {}
    out['signal'] = (bool(s.get('ok')), len(s.get('bad') or []), '%s צמתים · %s עם רמזור · %s עם סיבה · %d בלי' % (s.get('junctions'), s.get('signals'), s.get('reasons'), len(s.get('bad') or [])))
    q = J(d, 'rule30.json') or {}
    out['rule30'] = (('rule30' in R and R['rule30'] == 0), int(q.get('fail') or 0), '%s נקודות · %s חלונות · %s נכשלו' % (q.get('points'), q.get('opened'), q.get('fail')))
    for k in ('a4fleet', 'a4fleet2'):
        a = J(d, k + '.json') or {}
        out[k] = (bool(a.get('ok')), len(a.get('stuck') or []), 'יציאות %s · חזרו %s · נתקעו %d' % (json.dumps(a.get('trips'), ensure_ascii=False), json.dumps(a.get('parkedBack'), ensure_ascii=False), len(a.get('stuck') or [])))
    st = None
    for ln in log(d, 'stuck').splitlines():
        if ln.startswith('{'):
            try: st = json.loads(ln)
            except Exception: pass
    if st is not None:
        out['stuck'] = (True, int(st.get('over5') or 0), 'רכבים שעמדו יותר מ-5 שנ׳: %s (אוטובוסים %s) · שגיאות דף %d' % (st.get('over5'), st.get('busOver5'), len(st.get('pe') or [])))
    else: out['stuck'] = (False, 1, 'לא רץ')
    sy = J(d, 'story.json')
    if isinstance(sy, dict):
        bad = [k for k, v in sy.items() if isinstance(v, dict) and v.get('ok') is False]
        out['story'] = (not bad, len(bad), 'בדיקות הסיפורים: %d · נכשלו: %s' % (len(sy), ', '.join(bad) or 'אין'))
    else: out['story'] = (False, 1, 'לא רץ')
    za = J(os.path.join(d, 'zoneaudit'), 'audit.json') or {}
    zz = za.get('zones') or {}
    fl = {z: (len(v.get('gaps') or []), len(v.get('flags') or [])) for z, v in zz.items()}
    out['zoneaudit'] = ('zoneaudit' in R and R['zoneaudit'] == 0, sum(b for a, b in fl.values()),
                        ' · '.join('%s: פערי פנסים %d, דגלים %d' % (z, a, b) for z, (a, b) in fl.items()) or 'לא רץ')
    v = J(d, 'vinv.json') or {}
    nv = len(v.get('rebuiltAppear') or []) + len(v.get('rebuiltJumps') or []) + len(v.get('rebuiltParked') or [])
    out['vinv'] = (bool(v.get('ok')), nv, 'באזורים הבנויים: מופיעים/נעלמים %d, קופצים %d, חונים בלי דרך %d · באזורים הישנים (לא נכשל): %d · רכבים עומדים %s' % (
        len(v.get('rebuiltAppear') or []), len(v.get('rebuiltJumps') or []), len(v.get('rebuiltParked') or []), sum((v.get('oldAppearBySource') or {}).values()), v.get('vehiclesChecked')))
    return out

NAMES = dict(ingame='הבדיקות שבתוך המשחק (roadAudit, ‏E3, ‏E4, ‏C5 ועוד)', rules='סקריפט הכללים (rules_gate)', live='הפרטים החיים (live_audit)',
             xw='מעברי החצייה (xw_gate)', signal='הרמזורים (signal_gate)', rule30='כלל 30 — מסכי המקומות (rule30_gate)', a4fleet='צי החירום של A4',
             a4fleet2='צי החירום של A4 — המחמירה', stuck='עצירות ארוכות (stuckmax)', story='הסיפורים (qa_story5)', zoneaudit='בדיקת האזורים (zoneaudit)',
             vinv='הרכבים המזויפים (vinv)')
def nm(k): return NAMES.get(k) or ('אנשים בכביש — ריצה ' + k[6:] if k.startswith('people') else k)

cur = collect(O); bld = open(os.path.join(O, 'build.txt')).read().split() if os.path.exists(os.path.join(O, 'build.txt')) else ['?', '?', '?']
L = ['הסט המלא של הבדיקות — ' + bld[0], 'sha1 %s · %s בתים' % (bld[1], bld[2] if len(bld) > 2 else '?'), '']
nf = 0
for k, (ok, n, det) in cur.items():
    if not ok: nf += 1
    L.append('%s %s — %s' % ('✓' if ok else '✗', nm(k), det))
L += ['', 'נכשלו בריצה הזו: %d מתוך %d' % (nf, len(cur))]
if B:
    base = collect(B); bb = open(os.path.join(B, 'build.txt')).read().split() if os.path.exists(os.path.join(B, 'build.txt')) else ['?', '?']
    L += ['', 'ההשוואה מול הבסיס — ' + bb[0] + ' (' + bb[1] + ')', '']
    worse = []
    for k, (ok, n, det) in cur.items():
        b = base.get(k)
        if not b: L.append('· %s — אין בבסיס' % nm(k)); continue
        w = (b[0] and not ok) or (n > b[1])
        if w: worse.append(k)
        L.append('%s %s — בבסיס %s (%d), עכשיו %s (%d)' % ('החמרה ✗' if w else 'אין החמרה ✓', nm(k), 'עובר' if b[0] else 'נכשל', b[1], 'עובר' if ok else 'נכשל', n))
    L += ['', 'סך הכול: ' + ('אין החמרה' if not worse else 'החמרה ב-' + ', '.join(nm(k) for k in worse))]
open(os.path.join(O, 'summary.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L)); sys.exit(nf)
