#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""4.11 01:45 · schedule_calc — אבני הדרך מחושבות מחדש (הבעלים 01:24–01:27, סעיף 6): התאריך שבו כל שלב מתחיל ונגמר, לפי הקצב האמיתי של היום ולפי המכסה של השבוע.
המודל:
 · עובדים ברצף (D‑452: כל הלילה, בונה אחד ואני), עד שהמכסה מגיעה ל-98% — שם לא מתחילים בנייה (D‑393); ממשיכים אחרי האיפוס, ביום שלישי 05:00.
 · השבת: שישי 16:30 עד מוצאי שבת 17:30 — לא עובדים.
 · הקצב של המכסה: אחוזים לשעת עבודה (מדוד היום: 1.7–2.1; quota_meter). שתי הערכות: מוקדמת (1.6, השעות ×0.9) ומאוחרת (2.1, השעות ×1.2).
 · השעות של כל שלב — הערכה מהקצב של היום: אזור בעיר כ-3.5 שע׳ עם התיקונים (C5/D5, ‏E3, ‏A5, ‏B5 — 4 אזורים ב-12 שע׳), אזור ים פתוח כ-1.5.
usage: python3 schedule_calc.py [--now 'YYYY-MM-DD HH:MM'] [--pct 28.7] [--json out.json]"""
import sys, json, argparse, datetime as dt
ap = argparse.ArgumentParser(); ap.add_argument('--now', default=None); ap.add_argument('--pct', type=float, default=None); ap.add_argument('--json')
A = ap.parse_args()
TZ = dt.timezone(dt.timedelta(hours=2))
now = dt.datetime.strptime(A.now, '%Y-%m-%d %H:%M').replace(tzinfo=TZ) if A.now else dt.datetime.now(TZ).replace(second=0, microsecond=0)
pct0 = A.pct if A.pct is not None else 28.7
STOP, RESET_WD, RESET_H = 98.0, 1, 5   # Tuesday (Monday=0) 05:00
# the stages, in the owner's order (01:24–01:27): S7 … S13; the home and the garage in the city; S14; S15; S16; then the vehicles (D‑392)
STAGES = [
 ('S7', 'S7 — הסוף: הרכבים והאנשים האמיתיים (p574 — כלל 25, השטיפה והאורחים ב-C3, הכלב)', 5.0),   # 4.11 07:30: B5, A5 and the hotel are done
 ('S8', 'S8 — A2, ‏B2, ‏C2, ‏D2 (בית החולים, הפארק, הקניון, העסקים)', 14.0),   # the owner 07:24: S8 before the island road and the lines
 ('S9a', 'S9 — דרך האי, רחוב המסוף והפעלת הקווים 1, 3 ו-4', 5.0),
 ('S9', 'S9 — השאר: E4, ‏E5, ‏F3, ‏F4, ‏F5, ‏F6', 18.0),
 ('S10', 'S10 — הנמל: C6, ‏D6, ‏E6, ונתיבי השיט בתוך הנמל', 14.0),
 ('S11', 'S11 — A6, ‏B6 (החווה, החוף)', 7.0),
 ('S12', 'S12 — הצפון: A0–D1 (יער, רכס, כפר, שדות)', 16.0),
 ('S13', 'S13 — האי, הגשר המתרומם, E7 ו-E8 (13 אזורים)', 20.0),
 ('HOME', 'הבית והמוסך בעיר', 8.0),
 ('S14', 'S14 — הים: A7–E9 (13 אזורים) ושלב 18 — האוניות, הסירות והדיג (23)', 43.0),
 ('S15', 'S15 — השדה, הצד האווירי (שלב 8)', 46.0),
 ('S16', 'S16 — השדה, צד היבשה (שלב 9) והשחקן בשדה (שלב 10)', 32.0),
]
def shabbat(t):
    wd = t.weekday()   # Friday 4, Saturday 5
    if wd == 4 and (t.hour, t.minute) >= (16, 30): return True
    if wd == 5 and (t.hour, t.minute) < (17, 30): return True
    return False
def next_reset(t):
    d = (RESET_WD - t.weekday()) % 7
    r = (t + dt.timedelta(days=d)).replace(hour=RESET_H, minute=0)
    return r if r > t else r + dt.timedelta(days=7)
def run(rate, mult):
    t, pct, out, STEP = now, pct0, [], dt.timedelta(minutes=10)
    for sid, name, h in STAGES:
        need = h * mult; start = None
        while need > 1e-9:
            if pct >= STOP: t = next_reset(t); pct = 0.0; continue
            if shabbat(t): t += STEP; continue
            if start is None: start = t
            step_h = min(need, 1 / 6); t += dt.timedelta(hours=step_h); need -= step_h; pct += rate * step_h
        out.append({'id': sid, 'name': name, 'hours': round(h * mult, 1), 'start': start.strftime('%d.%m %H:%M'), 'end': t.strftime('%d.%m %H:%M'), 'pctEnd': round(pct, 1)})
    return out
E, L = run(1.6, 0.9), run(2.1, 1.2)
rows = [{'id': e['id'], 'name': e['name'], 'hours': [e['hours'], l['hours']], 'start': [e['start'], l['start']], 'end': [e['end'], l['end']]} for e, l in zip(E, L)]
res = {'at': now.strftime('%d.%m.%Y %H:%M'), 'pct': pct0, 'model': 'עבודה רצופה עד 98% במכסה, איפוס ביום שלישי 05:00, בלי שבת (שישי 16:30 – מוצאי שבת 17:30); מוקדם — 1.6% לשעה והשעות ×0.9; מאוחר — 2.1% לשעה והשעות ×1.2',
       'total': [round(sum(h for _, _, h in STAGES) * 0.9, 1), round(sum(h for _, _, h in STAGES) * 1.2, 1)], 'rows': rows}
if A.json: json.dump(res, open(A.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in rows: print(r['id'], r['hours'], 'start', r['start'], 'end', r['end'])
