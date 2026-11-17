# -*- coding: utf-8 -*-
"""quota_now.py — הערכת המכסה בצ'אט הזה, לפי מודל (10.11.2026).
הבעלים 10.11 ~08:58: "היה 37 בטעות איפסתי היתי אמור לחכות ל99 / עכשיו 0 / אבל היה על פאבל והעברתי ל אופוס"; ~09:05: "אין לי עוד איפוס".
כלומר מונה אחד לכל השבוע, שאופס ל-0 בערך ב-08:58, ואין איפוס נוסף. כל הצריכה מאז — של פאבל ושל אופוס יחד — נספרת בו.
הכיול: לפני האיפוס הכלי ספר 13.53 יחידות (‏1 יחידה = 7,976,435 טוקנים משוקללים) כשהבעלים ראה 37% → ‏K = 37 / 13.53 לפאבל.
לאופוס — אותו K עד הקריאה הראשונה שלו (כנראה מחמיר: אופוס זול יותר). הבסיס: 0% בנקודה שבה הכלי ספר 13.53 (פאבל) ו-0.37 (אופוס).
עוצרים: 98.5% לסוכנים, 99% למתאם, 99.5% למסירה (D‑599). בכל קריאה חדשה של הבעלים — מכיילים.
usage: python3 tools_pack/quota_now.py [--log]"""
import json, glob, os, sys, datetime as dt
SESS = '/root/.claude/projects/-home-user/59afe673-6e42-5712-9b20-6bf3463c6a6d'
PER1 = 7976435
W = dict(inp=1.0, cw=1.25, cr=0.1, out=5.0)
# model → (K, units at the owner's reading, the owner's reading %)
CAL = {'claude-fable-5-2': (0.8229, 15.401, 0.0),   # 17.11 05:00: האיפוס השבועי — 0%   # 11.11 08:00: הבעלים אִפֵּס — 0% (היחידות באיפוס: 15.401)
       'claude-opus-5-5':  (0.8999, 230.652, 0.0)}   # 17.11 05:00: האיפוס השבועי — 0%   # 12.11 ~00:45: הבעלים 96%, הכלי 95.4% (K 0.8943 → 0.8999)   # 11.11 ~23:45: הבעלים 92%, הכלי 94.2% (K 0.9157 → 0.8943)   # 11.11 08:00: הבעלים 0% אחרי האיפוס (היחידות באיפוס: 119.226; K מהכיול של 10.11 23:50)   # 10.11 ~23:50: הבעלים 92%, הכלי 93.7% (K 0.8229 → 0.8077)
NAME = {'claude-fable-5-2': 'פאבל', 'claude-opus-5-5': 'אופוס'}
TZ = dt.timezone(dt.timedelta(hours=2))
seen = {}
for f in [SESS + '.jsonl'] + glob.glob(SESS + '/**/*.jsonl', recursive=True):
    try: fh = open(f, encoding='utf-8', errors='replace')
    except OSError: continue
    for line in fh:
        if '"usage"' not in line: continue
        try: o = json.loads(line)
        except ValueError: continue
        m = o.get('message') or {}; u = m.get('usage'); ts = o.get('timestamp')
        if not u or not ts: continue
        k = m.get('id') or o.get('requestId') or o.get('uuid')
        t = dt.datetime.fromisoformat(ts.replace('Z', '+00:00'))
        seen[k] = (t, m.get('model'), (W['inp'] * (u.get('input_tokens') or 0) + W['cw'] * (u.get('cache_creation_input_tokens') or 0)
                   + W['cr'] * (u.get('cache_read_input_tokens') or 0) + W['out'] * (u.get('output_tokens') or 0)) / PER1)
now = dt.datetime.now(dt.timezone.utc)
pct, rate, parts = 0.0, 0.0, []
for mo, (K, u0, p0) in CAL.items():
    units = sum(v for t, m, v in seen.values() if m == mo)
    hour = sum(v for t, m, v in seen.values() if m == mo and (now - t).total_seconds() < 3600)
    a, r = p0 + K * max(0.0, units - u0), K * hour
    pct += a; rate += r; parts.append('%s %.1f%% (%.1f%% לשעה)' % (NAME[mo], a, r))
left = (99.5 - pct) / rate if rate > 0 else float('inf')
print('המכסה (הערכה): %.1f%% · בשעה האחרונה %.2f%% · עד 99.5%% בקצב הזה: %s שע׳ · מתוכם: %s' % (pct, rate, ('%.1f' % left) if left != float('inf') else '—', ' · '.join(parts)))
if '--log' in sys.argv:
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'qa_quota_log_1110.json')
    L = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
    L.append({'at': now.astimezone(TZ).strftime('%d.%m %H:%M'), 'pct': round(pct, 2), 'last_hour': round(rate, 2), 'hours_to_99_5': None if left == float('inf') else round(left, 1)})
    json.dump(L, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
