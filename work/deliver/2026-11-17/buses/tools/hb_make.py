#!/usr/bin/env python3
# hb_make.py <try> [ready-line] — buses (17.11): מחבר את ההחזרה מהחלקים (hb_head / hb_built / hb_rev / hb_inv) ומהסיכום של הבדיקות (hb_sum.py).
import sys, subprocess, os, datetime
D = '/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/buses'; T = sys.argv[1]; ready = sys.argv[2] if len(sys.argv) > 2 else ''
R = lambda n: open(os.path.join(D, n), encoding='utf-8').read().rstrip('\n') if os.path.exists(os.path.join(D, n)) else ''
now = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)).strftime('%H:%M')
tests = subprocess.run(['python3', os.path.join(D, 'tools/hb_sum.py'), T], capture_output=True, text=True).stdout.rstrip('\n')
parts = []
if ready: parts.append(ready)
parts.append(R('hb_head.txt'))
parts.append(f'== המצב ({now}) ==\n' + R('hb_status.txt'))
parts.append(R('hb_rb.txt')); parts.append(R('hb_plan.txt')); parts.append(R('hb_built.txt')); parts.append(R('hb_rev.txt'))
parts.append(f'== הבדיקות — {T} ==\n' + tests)
parts.append(R('hb_inv.txt')); parts.append(R('hb_tail.txt'))
open(os.path.join(D, 'handback.txt'), 'w', encoding='utf-8').write('\n\n'.join(p for p in parts if p) + '\n'); print('ok', len('\n'.join(parts)))
