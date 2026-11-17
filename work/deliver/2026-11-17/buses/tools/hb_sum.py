#!/usr/bin/env python3
# hb_sum.py <try> — buses (17.11): סיכום הבדיקות של הניסיון (מהקבצים ב-qa) — שורות בעברית להחזרה.
import json, sys, os, re
Q = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/buses/qa'; T = sys.argv[1]
def jl(p):
    """the last JSON object in a file (the tools print [bslot] lines before it)"""
    try: s = open(os.path.join(Q, p), encoding='utf-8').read()
    except OSError: return None
    try: return json.loads(s)
    except ValueError: pass
    for line in reversed(s.splitlines()):
        line = line.strip()
        if line.startswith('{'):
            try: return json.loads(line)
            except ValueError: continue
    return None
def txt(p):
    try: return open(os.path.join(Q, p), encoding='utf-8').read()
    except OSError: return ''
out = []
g = jl(f'{T}_ingame.json')
if g:
    ra = g.get('roadAudit') or {}; bad = [k for k, v in g.items() if isinstance(v, dict) and v.get('ok') is False]
    fl = ra.get('failed') or []; known = all('build-id-without-a-build-number' in str(x) for x in fl) and set(bad) <= {'roadAudit', 'texts'}
    out.append(f"q_ingame: ‏{ra.get('passed')}/{ra.get('total')}, שגיאות {len(g.get('errors') or [])}, נכשלו: {', '.join(bad) or '—'}" + (" — הנכשלת היחידה build_texts_from_one_version_constant (\"build-id-without-a-build-number\": המזהה של ניסיון, ‎-tryNNNN‎, בלי s7f — כך בכל ניסיון, לא קשור)" if fl and known else ''))
else: out.append('q_ingame: אין תוצאה')
r = jl(f'{T}_rules.json'); out.append(f"rules_gate: {'עובר' if r and r.get('ok') else ('לא עובר' if r else 'אין תוצאה')} · כישלונות {len((r or {}).get('fails') or [])}" + (f" ({'; '.join(map(str, r['fails']))[:400]})" if r and r.get('fails') else '') + (" — רק build_texts (המזהה של ניסיון, כמו ב-q_ingame; כך בכל ניסיון)" if r and r.get('fails') and all('build_texts_from_one_version_constant' in str(x) and str(x).count(',') == 0 for x in r['fails']) else ''))
s = jl(f'{T}_stuck150.json'); out.append(f"stuckmax 150: מעל 5 שנ׳ — {s.get('over5')} (אוטובוסים {s.get('busOver5')}) · שגיאות דף {len(s.get('pe') or [])}" + (f" · {json.dumps(s.get('long'), ensure_ascii=False)[:300]}" if s and s.get('long') else '') if s else 'stuckmax 150: אין תוצאה')
pl = txt(f'{T}_people.log').strip().splitlines(); pl = [l for l in pl if 'people_on_road' in l]; out.append(pl[0][:260] if pl else 'people_on_road: אין תוצאה')
k = jl(f'{T}_stuck1500.json')
if k:
    ln = k.get('ln') or {}
    out.append(f"stuckmax 1500 (העותק שלי, stuckmax_bus.js — אותה ספירה + אוטובוסי הקווים לפי המקום): מעל 5 שנ׳ — {k.get('over5')} (אוטובוסים {k.get('busOver5')}) · שגיאות דף {len(k.get('pe') or [])}"
               + (f" · {json.dumps(k.get('long'), ensure_ascii=False)[:400]}" if k.get('long') else '')
               + f" · אוטובוסי הקווים בשלב נסיעה שלא זזו: מעל 30 שנ׳ — {ln.get('over30')}, מעל 60 — {ln.get('over60')}, ‏180 ומעלה — {ln.get('over180')} · הארוכים: {json.dumps((ln.get('top') or [])[:5], ensure_ascii=False)[:400]} · LN: {json.dumps(ln.get('audit'), ensure_ascii=False)[:200]}")
else: out.append('stuckmax 1500: אין תוצאה')
def night(p, label):
    n = jl(p)
    if not n: return f'{label}: אין תוצאה'
    rows = n.get('rows') or []; fin = (n.get('fin') or {}).get('audit') or {}
    oks = ''.join('1' if (x.get('a') or {}).get('ok') else '0' for x in rows); y = (fin.get('stats') or {}).get('yields', 0); fz = fin.get('frz') or {}
    lb = fin.get('lb') or {}; sw = lb.get('sidewalk') or {}; bf = (n.get('bsv') or {}).get('first') if isinstance(n.get('bsv'), dict) else None
    why = f"lb.ok={lb.get('ok')} (על המדרכה במסוף walkTerm={sw.get('term')}, על המדרכה בכלל {sw.get('n')}; wait.ok={(lb.get('wait') or {}).get('ok')})"
    return (f"{label}: ok לפי השלבים (יום, ‏8 לילה, ‏3 בוקר) {oks} · בסוף ok={fin.get('ok')} — {why} · קיפאון (frz) n={fz.get('n')} max={fz.get('max')} · \"האוטובוס ראשון\" (מעבר דרך גוף) {y}"
            + (f" · 074zu: המתנה במקום מעבר {bf.get('hold')}, בקשות נסיגה {bf.get('backReq')}, מוצא אחרון {bf.get('passN')}" if bf else '')
            + (lambda bd: f" · bend: שוחרר {bd.get('free')}, נשאר (סכנה אמיתית) {bd.get('keep')}" + (f", העצירה הרצופה הארוכה {bd.get('maxS')} שנ׳, בקשות נסיגה אחרי 30 שנ׳ {bd.get('ask')}" if 'maxS' in bd else '') if bd else '')((n.get('bsv') or {}).get('bend') if isinstance(n.get('bsv'), dict) else None) + f" · trips {(fin.get('stats') or {}).get('trips')} · שגיאות {len(n.get('errs') or [])}")
out.append(night(f'{T}_night.json', 'הלילה של הקווים (lines_night_tr2.js)')); out.append(night('base299_night.json', 'הלילה של הקווים — הבסיס S7F299'))
for lab, p in (('המדידה — הבסיס S7F299', 'beh_base299.json'), ('המדידה — הניסיון', f'beh_{T}.json')):
    b = jl(p)
    if not b: out.append(f'{lab}: אין תוצאה'); continue
    sh = b.get('share') or {}; lnS = {k2: v for k2, v in sh.items() if k2.startswith('ln') or k2 == 'coach5'}
    st = sum(v['stopS'] for v in lnS.values()); mv = sum(v['moveS'] for v in lnS.values()); car = sh.get('car') or {}
    bf = b.get('busFirst') or {}; au = b.get('aud') or {}; f = au.get('first') if isinstance(au, dict) else None
    lns = b.get('lns') or {}; fz = (lns.get('frz') or {}) if isinstance(lns, dict) else {}
    out.append(f"{lab} ({b.get('secs')} שנ׳, {b.get('clk0')}–{b.get('clk1')}): אוטובוסי הקווים עומדים {round(100*st/max(1,st+mv))}% מהזמן, מכוניות {round(100*car.get('stopShare',0))}% · bend (טיקים) {sum(v['bend'] for v in lnS.values())} · \"האוטובוס ראשון\" {bf.get('n')}"
               + (f" · במקומו המתנה כמו מכונית {f.get('hold')} (נגמרו כשהמכונית נסעה {f.get('free')}, לתקרה {f.get('capN')})" if f else '') + f" · קיפאון n={fz.get('n')} max={fz.get('max')} · שגיאות {len(b.get('errs') or [])}")
print('\n'.join('- ' + l for l in out))
