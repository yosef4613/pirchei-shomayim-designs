#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""30.10 · the morning update of the daily report, after the plan v6.33: the packages of 4–6 h and the daily line (R-30, R-27) copied from
the plan's data (plan600/data/new.json — 'packages'), what was delivered since the previous report, what moved and why, what is next.
usage: UPDATED='30.10.2026 · HH:MM' PLAN='v6.33 · sha' BUILD='S7F1NN · sha' DELIVERED='["…", …]' MOVED='["…"]' NEXT='["…"]' python3 daily_0700.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(H, 'daily.json'); d = json.load(open(p, encoding='utf-8'))
N = json.load(open('/home/claude/work/plan600/data/new.json', encoding='utf-8'))
J = lambda k: json.loads(os.environ.get(k, '[]') or '[]')
d['updated'] = os.environ.get('UPDATED', '30.10.2026 · 07:00'); d['next'] = '30.10 · 15:30 — המסירה המסודרת לפני השבת'
if os.environ.get('PLAN'): d['plan'] = os.environ['PLAN']
if os.environ.get('BUILD'): d['build'] = os.environ['BUILD']
P = N['packages']
d['packages'] = {'rows': P['rows'], 'daily': P['daily'], 'note': P['note'],
                 'moves': [('נמסרו מאז הדוח הקודם:', x) for x in J('DELIVERED')] + [('זזו:', x) for x in J('MOVED')] + [('הבאות:', x) for x in J('NEXT')]}
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('ok', len(P['rows']), 'rows')
