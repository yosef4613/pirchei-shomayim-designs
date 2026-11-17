# -*- coding: utf-8 -*-
"""The owner 3.11 12:16: at every checkpoint in the report — how much quota went since the previous check, and how many hours it lasts at this pace.
There is no quota counter here. What there is: the usage of every model call, in the session transcripts (the main one and every agent).
The measure: units = input + 1.25 x cache-write + 0.1 x cache-read + 5 x output (the price ratios — an estimate, for the owner's approval).
The calibration: the owner's own readings (READINGS below; add a reading whenever the owner gives one) → units per 1%.
The quota resets on Tuesday 05:00 (Israel). Stop at 99% (rule 15).
usage:
  python3 quota_meter.py calib                       → units per 1% for every pair of readings
  python3 quota_meter.py now [--log]                 → the estimate now, since the last check, the pace of the last hour, hours to 99%; --log adds a row to qa_quota_log.json
"""
import json, glob, os, sys, datetime as dt
TZ = dt.timezone(dt.timedelta(hours=2))
SESS = '/root/.claude/projects/-home-claude/7bb7c82b-9a44-5cd6-ab8f-054dc66a801d'
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'qa_quota_log.json')
READINGS = [  # (Israel time, % shown to the owner) — from the inbox and the status file
    ('2026-11-01 15:15', 67), ('2026-11-02 13:18', 88), ('2026-11-02 15:06', 92), ('2026-11-02 17:17', 92), ('2026-11-03 05:00', 0), ('2026-11-03 12:29', 9), ('2026-11-03 14:31', 13), ('2026-11-03 16:41', 17), ('2026-11-03 21:14', 22)]
RESET = '2026-11-03 05:00'
W = dict(inp=1.0, cw=1.25, cr=0.1, out=5.0)

def t_il(s): return dt.datetime.strptime(s, '%Y-%m-%d %H:%M').replace(tzinfo=TZ)

def calls():
    seen = {}
    files = [SESS + '.jsonl'] + glob.glob(SESS + '/subagents/*.jsonl')
    for f in files:
        try: fh = open(f, encoding='utf-8', errors='replace')
        except OSError: continue
        for line in fh:
            if '"usage"' not in line: continue
            try: o = json.loads(line)
            except ValueError: continue
            m = o.get('message') or {}
            u = m.get('usage'); ts = o.get('timestamp')
            if not u or not ts: continue
            k = m.get('id') or o.get('requestId') or o.get('uuid')
            t = dt.datetime.fromisoformat(ts.replace('Z', '+00:00'))
            units = (W['inp'] * (u.get('input_tokens') or 0) + W['cw'] * (u.get('cache_creation_input_tokens') or 0)
                     + W['cr'] * (u.get('cache_read_input_tokens') or 0) + W['out'] * (u.get('output_tokens') or 0))
            seen[k] = (t, units, os.path.basename(f))
    return sorted(seen.values())

def between(C, a, b): return sum(u for t, u, _ in C if a <= t < b)

def per1(C):
    R = [(t_il(s), p) for s, p in READINGS]
    out = []
    for (a, pa), (b, pb) in zip(R, R[1:]):
        if pb > pa: out.append((a, b, pb - pa, between(C, a, b) / (pb - pa)))
    return out

def main():
    C = calls()
    if not C: print('אין נתונים'); return
    P = per1(C)
    if sys.argv[1:2] == ['calib']:
        for a, b, d, u in P: print('%s → %s: %d%%, %.0f יחידות ל-1%%' % (a.strftime('%d.%m %H:%M'), b.strftime('%d.%m %H:%M'), d, u))
        return
    R_ = [(t_il(s), p) for s, p in READINGS if t_il(s) > t_il(RESET) and p > 0]
    u1 = (between(C, t_il(RESET), R_[-1][0]) / R_[-1][1]) if R_ else sum(u * d for _, _, d, u in P) / sum(d for _, _, d, _ in P)   # the owner's last reading since the reset (cumulative) wins
    now = dt.datetime.now(TZ); r = t_il(RESET)
    used = between(C, r, now) / u1
    hour = between(C, now - dt.timedelta(hours=1), now) / u1
    prev = None
    if os.path.exists(LOG):
        L = json.load(open(LOG, encoding='utf-8'))
        if L: prev = L[-1]
    else: L = []
    since = None
    if prev: since = used - prev['pct']
    left = (99 - used) / hour if hour > 0 else None
    row = {'at': now.strftime('%d.%m %H:%M'), 'pct': round(used, 1), 'since_prev': None if since is None else round(since, 1),
           'prev_at': prev['at'] if prev else None, 'last_hour': round(hour, 2), 'hours_to_99': None if left is None else round(left, 1),
           'units_per_1pct': round(u1)}
    print(json.dumps(row, ensure_ascii=False))
    if '--log' in sys.argv:
        L.append(row); json.dump(L, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__': main()
