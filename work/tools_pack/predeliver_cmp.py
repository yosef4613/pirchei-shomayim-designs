#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""29.10 14:35 · R-13 — הרשימה הקבועה לפני מסירה: השוואה של הבנייה החדשה מול הקודמת.
usage: predeliver_cmp.py <qa dir of the new build> <qa dir of the previous build> <out.md>
כל qa dir מכיל full/ (מ-run_full.sh) ו-pre/ (מ-predeliver.sh). פלט: שורה לכל בדיקה — עובר / נכשל / השתנה.
יציאה: מספר הכישלונות (0 = אפשר למסור)."""
import sys, os, json, glob
NEW, OLD, OUT = sys.argv[1:4]
rows, fails = [], 0

def J(d, f):
    p = os.path.join(d, f)
    try: return json.load(open(p, encoding='utf-8'))
    except Exception as e: return {'__err': str(e)[:120]}

def row(name, ok, new, old='', note=''):
    global fails
    st = 'עובר' if ok is True else ('נכשל' if ok is False else 'לבדוק')
    if ok is False: fails += 1
    rows.append(f'| {name} | {st} | {new} | {old} | {note} |')

N, O = os.path.join(NEW, 'full'), os.path.join(OLD, 'full')
# 1. t1 / t2
for f in ('t1.json', 't2.json'):
    a, b = J(N, f), J(O, f)
    ok = ('__err' not in a) and not a.get('failed') and not a.get('pageErrors')
    row(f[:-5], ok, f"failed {len(a.get('failed', [1]))} · errors {len(a.get('pageErrors', [1]))}", f"failed {len(b.get('failed', []))}")
# 2. qa.json — every key with ok
a, b = J(N, 'qa.json'), J(O, 'qa.json')
if '__err' in a: row('qa', False, a['__err'])
else:
    bad = [k for k, v in a.items() if isinstance(v, dict) and v.get('ok') is False]
    missing = [k for k in b if k not in a]
    row('qa (' + str(len(a)) + ' בדיקות)', not bad and not missing, 'לא עוברות: ' + (', '.join(bad) or '—'), f'{len(b)} בדיקות', ('חסרות: ' + ', '.join(missing)) if missing else '')
# 3. seeds12 / seeds3
a, b = J(N, 'seeds12.json'), J(O, 'seeds12.json')
row('seeds12', a.get('okN') == 12, f"okN {a.get('okN')} · total {a.get('total')}", f"okN {b.get('okN')} · total {b.get('total')}")
a, b = J(N, 'seeds3.json'), J(O, 'seeds3.json')
bad = [s for s, v in a.items() if isinstance(v, dict) and v.get('ok') is False] if '__err' not in a else ['ERR']
hs = ' '.join(f"{s}:{v.get('hash')}" for s, v in a.items() if isinstance(v, dict))
ho = ' '.join(f"{s}:{v.get('hash')}" for s, v in b.items() if isinstance(v, dict))
row('seeds3', not bad, hs, ho, 'hash השתנה' if hs != ho else 'hash זהה')
# 4. matrix777
a, b = J(N, 'matrix777.json'), J(O, 'matrix777.json')
# 29.10 23:40: the matrix counts the turns of seed 777 — when the simulation changed (seeds3 hash), the number of turns changes with it;
# then every turn must pass (pass == turns, fail 0). With the same simulation, fewer turns than before is a failure.
_simchg = hs != ho
_fn = a.get('fail'); _fn = len(_fn) if isinstance(_fn, list) else (_fn or 0)
_ok = a.get('ok') is True and _fn == 0 and a.get('pass') == a.get('turns', a.get('pass')) and (_simchg or a.get('pass', 0) >= b.get('pass', 0))
row('matrix777', _ok, f"pass {a.get('pass')} / turns {a.get('turns')} · fail {_fn}", f"pass {b.get('pass')}", ('הסימולציה השתנתה — מספר הפניות השתנה איתה; כולן עוברות' if _simchg and a.get('pass') != b.get('pass') else ''))
# 5. single checks with ok
for f in ('taxiwatch_alone.json', 'loadSliced.json', 'zoomLevels.json', 'tileEmpty.json'):
    a = J(N, f); ok = a.get('ok') is True; note = ''
    if f == 'zoomLevels.json' and not ok:   # 17:35: flaky under load — passes when run again alone (both reruns must pass)
        rr = [J(N, 'zoomLevels_rerun%d.json' % i).get('ok') for i in (1, 2)]
        if all(x is True for x in rr): ok = True; note = 'נכשל בריצה המלאה (תחת עומס); בהרצה חוזרת לבד — 2 / 2'
    row(f[:-5], ok, 'ok ' + str(a.get('ok')), '', note)
# 6. capacity
a, b = J(N, 'cap.json'), J(O, 'cap.json')
fa = ' '.join(f"{s}:{v.get('flights')}" for s, v in a.items() if isinstance(v, dict))
fb = ' '.join(f"{s}:{v.get('flights')}" for s, v in b.items() if isinstance(v, dict))
row('cap (טיסות בשעה)', '__err' not in a, fa, fb, 'השתנה' if fa != fb else '')
# 7. dup_decl
try: last = open(os.path.join(N, 'dup_decl.log'), encoding='utf-8').read().strip().split('\n')[-1]
except Exception as e: last = 'ERR ' + str(e)[:60]
row('dup_decl', last.endswith('duplicates []'), last)

# --- pre/ (Chromium checks from predeliver.sh)
P, Q = os.path.join(NEW, 'pre'), os.path.join(OLD, 'pre')
def last_json(path, key=None):
    try: lines = open(path, encoding='utf-8').read().strip().split('\n')
    except Exception: return None
    for l in reversed(lines):
        l = l.strip()
        if key and not l.startswith(key): continue
        try: return json.loads(l[len(key):].strip() if key else l)
        except Exception: continue
    return None
def errs_of(path):
    e = last_json(path, 'ERRS')
    return e if isinstance(e, list) else None
# smoke
for nm in ('c34smoke', 'p34smoke'):
    e = errs_of(os.path.join(P, nm + '.log')); row(nm, e == [], 'errors ' + (str(len(e)) if e is not None else 'לא רץ'))
# census of what is still drawn top-down (D-274: may not grow; the target is zero next to 3/4)
def census_n(d):
    c = J(d, 'census3.json')
    if '__err' in c or 'total' not in c: return None, {}
    return c['total'], c.get('byGroup', {})
cn, cper = census_n(P); co, _ = census_n(Q)
row('census3 — מצויר מלמעלה', None if cn is None else (co is None or cn <= co), f'{cn}', f'{co}', ' · '.join(f'{k} {v}' for k, v in cper.items())[:300])
# buildings (D-275)
bn = last_json(os.path.join(P, 'bldshadow.log')); bo = last_json(os.path.join(Q, 'bldshadow.log'))
fn = bn.get('fails') if isinstance(bn, dict) else None; fo = bo.get('fails') if isinstance(bo, dict) else 11
row('מבנים (0.6×גובה)', None if fn is None else fn <= fo, f'fails {fn}', f'fails {fo}', 'הבסיס 11 (29.10)')
# semi / first seconds / flips / aircraft
for nm in ('c34semiqa2', 'c34firstqa', 'p34flipqa', 'a34qa'):
    p = os.path.join(P, nm + '.log')
    if not os.path.exists(p): row(nm, None, 'לא רץ'); continue
    e = errs_of(p); row(nm, e == [] if e is not None else None, 'errors ' + (str(len(e)) if e is not None else '?'))
# 31.10 (R-35): errtour — all the module error counters after a camera tour (city, port, airport); ok only when every counter is 0
et = J(P, 'errtour.json') if os.path.exists(os.path.join(P, 'errtour.json')) else None
if et is None: row('errtour — מוני השגיאות אחרי סיבוב', None, 'לא רץ')
else: row('errtour — מוני השגיאות אחרי סיבוב', et.get('ok') is True, json.dumps(et.get('counters', et), ensure_ascii=False)[:220], '', 'R-35')
# 1.11 (the owner 31.10 23:46): buses waiting on the road near the E3 terminal — reported ('לבדוק') until the new terminal is built, then blocking
rj = J(P, 'rules.json') if os.path.exists(os.path.join(P, 'rules.json')) else None   # 2.11: כללי הכרטיס (R-62, R-63, R-64) — חוסם
if rj is None: row('rules — כללי הכרטיס: כבישים כמו במפה, מפרץ בכל תחנה, התאים של A4', False, 'לא רץ')
else: row('rules — כללי הכרטיס: כבישים כמו במפה, מפרץ בכל תחנה, התאים של A4', rj.get('ok') is True, ('; '.join(rj.get('fails', [])) or 'בלי הפרות')[:300], '', 'R-62 · R-63 · R-64')
vj = J(P, 'vinv.json') if os.path.exists(os.path.join(P, 'vinv.json')) else None   # 2.11 (R-67): 0 רכבים מזויפים בכל אזור בנוי — חוסם
if vj is None: row('vinv — 0 רכבים מזויפים באזורים הבנויים', False, 'לא רץ', '', 'R-67')
else: row('vinv — 0 רכבים מזויפים באזורים הבנויים', vj.get('ok') is True, ('אזורים %s · הופעות %d · קפיצות %d · חונים %d · ישנים: %d' % (','.join(vj.get('rebuilt', [])), len(vj.get('rebuiltAppear', [])), len(vj.get('rebuiltJumps', [])), len(vj.get('rebuiltParked', [])), sum(vj.get('oldAppearBySource', {}).values()))), '', 'R-67')
# 3.11 (המבקר על S7F210): בדיקות האזור (Z-01…Z-09), הפרטים החיים, מדריך הסגנון, "מה שהבעלים אהב" — חוסמים
for zf in sorted(f for f in os.listdir(P) if f.startswith('zchk_') and f.endswith('.json')):
    zj = J(P, zf); zfails = [k for k, v in zj.items() if isinstance(v, dict) and v.get("ok") is False]
    row('zchk %s — בדיקות האזור Z-01…Z-09' % zf[5:-5], zj.get('ok') is True, ("נכשלו: " + ", ".join(zfails)) if zfails else "כולן עוברות", '', 'הבעלים 18:37 / 19:31')
lj = J(P, 'live.json') if os.path.exists(os.path.join(P, 'live.json')) else None
if lj is None: row('live — הפרטים החיים: 8 מ-4 סוגים בכל אזור בנוי', False, 'לא רץ', '', 'D‑396 / R-74')
else: row('live — הפרטים החיים: 8 מ-4 סוגים בכל אזור בנוי', lj.get('ok') is True, json.dumps(lj.get('summary', lj.get('zones', '')), ensure_ascii=False)[:220], '', 'D‑396 / R-74')
sj = J(P, 'style.json') if os.path.exists(os.path.join(P, 'style.json')) else None
if sj is None: row('style — מדריך הסגנון: 0 חריגות בלי סיבה', False, 'לא רץ', '', 'כלל 18')
else:
    BLK = os.environ.get('STYLE_BLOCK', 'C5,D5').split(',')   # 3.11: the zones of this delivery block; the older zones — reported, fixed in their round (the owner 21:02)
    unz = {z: q.get('dev', 0) - q.get('dev_reason', 0) for z, q in sj.get('summary', {}).items()}
    uns = {p_: q.get('dev', 0) - q.get('dev_reason', 0) for p_, q in sj.get('seam_summary', {}).items()}
    ub = sum(v for z, v in unz.items() if z in BLK) + sum(v for p_, v in uns.items() if any(z in p_ for z in BLK))
    uo = sum(unz.values()) + sum(uns.values()) - ub
    row('style — מדריך הסגנון: 0 חריגות בלי סיבה באזורי המסירה (%s)' % ','.join(BLK), ub == 0, '%d באזורי המסירה · %d באזורים הקודמים (לסבב שלהם): %s' % (ub, uo, ', '.join('%s %d' % kv for kv in list(unz.items()) + list(uns.items()) if kv[1])), '', 'כלל 18')
kj = J(P, 'liked.json') if os.path.exists(os.path.join(P, 'liked.json')) else None
if kj is None: row('liked — מה שהבעלים אהב קיים במשחק (ובמפה)', False, 'לא רץ', '', 'כלל 19 / D‑398')
else: row('liked — מה שהבעלים אהב קיים במשחק (ובמפה)', kj.get('ok') is True, kj.get('summary', ''), '', 'כלל 19 / D‑398')
# 3.11 (R-75): הבנייה פורסמה בדף הקבוע "הבנייה האחרונה" עם אותו sha1 כמו הקובץ שנשלח — עד אז המסירה לא גמורה (נרשם ב-deliver/published.json ע"י page_wrap.py log)
try:
    PL = json.load(open('/home/claude/work/deliver/published.json', encoding='utf-8')); tag = [q for q in os.path.normpath(P).split(os.sep) if q.lower().startswith('s7f')][-1].upper()
    pub = [x for x in PL if tag in x['file'].upper() and x['page'] == 'הבנייה האחרונה']
except Exception: pub = []
row('published — הבנייה בדף הקבוע, אותו sha1 כמו הקובץ שנשלח (R-75)', True if pub else None, ('%s · %s · %d · %s' % (pub[-1]['file'].split('/')[-1], pub[-1]['sha1'][:12], pub[-1]['size'], pub[-1]['at'])) if pub else 'עוד לא פורסם — המסירה לא גמורה', '', 'R-75')
pj = J(P, 'people.json') if os.path.exists(os.path.join(P, 'people.json')) else None   # 3.11 (R-76, D‑404): אנשים בכביש — חוסם
if pj is None: row('people — 0 אנשים בכביש מחוץ למעבר (R-76)', False, 'לא רץ', '', 'R-76 / D‑404')
else: row('people — 0 אנשים בכביש מחוץ למעבר (R-76)', pj.get('ok') is True, json.dumps(pj.get('summary', {k: pj.get(k) for k in ('samples', 'onRoad', 'people') if k in pj}), ensure_ascii=False)[:220], '', 'R-76 / D‑404')
xj = J(P, 'xw.json') if os.path.exists(os.path.join(P, 'xw.json')) else None   # 3.11 23:33 (הביקורת 23:16): מעברי החצייה — שתי בדיקות, חוסמות
if xj is None:
    row('xw1 — מעבר בכל זרוע של צומת עם רמזור (D‑426; חריגים: D‑439, ‏D‑427 / D‑430)', False, 'לא רץ', '', 'הביקורת 23:16')
    row('xw2 — כל מעבר של המפה בצומת שבנוי במשחק — גם במשחק', False, 'לא רץ', '', 'הביקורת 23:16')
else:
    c1, c2 = xj['check1'], xj['check2']
    row('xw1 — מעבר בכל זרוע של צומת עם רמזור (D‑426; חריגים: D‑439, ‏D‑427 / D‑430)', not c1['fails'], f"{c1['junctions']} צמתים, {c1['arms']} זרועות, {c1['xw']} עם מעבר; חסרים {len(c1['fails'])}: " + ', '.join(f"{f['node']}/{f['road']}" for f in c1['fails'])[:240], '', 'הביקורת 23:16')
    row('xw2 — כל מעבר של המפה בצומת שבנוי במשחק — גם במשחק', not c2['fails'], f"קיימים {c2['matched']}, חסרים {len(c2['fails'])}: " + ', '.join(f"{f['mapnode']}/{f['seg']}" for f in c2['fails'])[:240], '', f"הביקורת 23:16 · נוספו {len(xj.get('added', []))}, יצאו {len(xj.get('removed', []))} — xw.md")
aj = J(P, 'a4fleet.json') if os.path.exists(os.path.join(P, 'a4fleet.json')) else None   # 4.11 (D‑459): צי החירום של A4 — חוסם
if aj is None: row('a4fleet — הכבאית והאמבולנס של A4 חוזרים לתא, אף רכב בשדרה לא עומד 90 שנ׳', False, 'לא רץ', '', 'D‑459')
else: row('a4fleet — הכבאית והאמבולנס של A4 חוזרים לתא, אף רכב בשדרה לא עומד 90 שנ׳', aj.get('ok') is True, json.dumps({'trips': aj.get('trips'), 'stuck': (aj.get('stuck') or [])[:2], 'cars': len(aj.get('carsStill') or [])}, ensure_ascii=False)[:220], '', 'D‑459')
tw = J(P, 'termwait.json') if os.path.exists(os.path.join(P, 'termwait.json')) else None
if tw is None: row('termwait — אוטובוסים ממתינים על הכביש ליד המסוף', None, 'לא רץ')
else: row('termwait — אוטובוסים ממתינים על הכביש ליד המסוף', True if tw.get('ok') is True else None, '%d מעל 5 שנ׳: ' % len(tw.get('over5', [])) + ', '.join('%s %s שנ׳ (%s)' % (o.get('bus'), o.get('s'), o.get('limit')) for o in tw.get('over5', []))[:200], '', 'עד המסוף החדש — מדווח')
try: ac = open(os.path.join(P, 'a34count.log'), encoding='utf-8').read().strip().split('\n')[-1][:200]
except Exception: ac = 'לא רץ'
row('a34count', None, ac)

head = ['# בדיקות לפני מסירה — ' + os.path.basename(os.path.normpath(NEW)) + ' מול ' + os.path.basename(os.path.normpath(OLD)), '',
        f'כישלונות: **{fails}**', '', '| בדיקה | מצב | עכשיו | קודם | הערה |', '|---|---|---|---|---|']
open(OUT, 'w', encoding='utf-8').write('\n'.join(head + rows) + '\n')
print('\n'.join(head + rows)); sys.exit(min(fails, 100))
