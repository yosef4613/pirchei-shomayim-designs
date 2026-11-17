#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3.11 · כלל 19 (D‑398): "מה שהבעלים אהב — נשמר" — בדיקת הסנכרון בכל מסירה.
לכל פריט ב-study/style/owner_liked.json: (1) במשחק — המזהה שלו (game) קיים בקובץ המשחק (חוסם: מה שהבעלים אהב לא נמחק);
(2) במפה — המזהה או השורה שלו קיימים ב-study/roads/city_plan.json, או שהפריט מסומן "לא צריך מגרש" (מדווח; חוסם מסבב 8 של המפה — LIKED_MAP_BLOCK=1).
usage: python3 liked_check.py <game.html> <out.json>   → exit 0 = עובר"""
import json, os, sys
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
game, out = sys.argv[1], sys.argv[2]
G = open(game, encoding='utf-8').read()
L = json.load(open(os.path.join(W, 'study/style/owner_liked.json'), encoding='utf-8'))
M = open(os.path.join(W, 'study/roads/city_plan.json'), encoding='utf-8').read()
MB = os.environ.get('LIKED_MAP_BLOCK') == '1'
rows, ok = [], True
for it in L['items']:
    gid = (it.get('game') or '').split(' ')[0]
    in_game = bool(gid) and gid in G
    need_map = not str(it.get('map', '')).startswith('לא צריך')
    in_map = (not need_map) or (bool(gid) and gid in M) or (it['id'] in M)
    r = {'id': it['id'], 'zone': it['zone'], 'what': it['what'], 'game': gid, 'inGame': in_game if gid else None, 'inMap': in_map}
    if gid and not in_game: ok = False
    if MB and not in_map: ok = False
    rows.append(r)
res = {'ok': ok, 'mapBlocks': MB, 'items': rows,
       'summary': '%d פריטים · במשחק %d מתוך %d עם מזהה · במפה %d מתוך %d' % (len(rows), sum(1 for r in rows if r['inGame']), sum(1 for r in rows if r['game']),
                                                                      sum(1 for r in rows if r['inMap']), len(rows))}
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(('עובר' if ok else 'נכשל') + ' · ' + res['summary'])
sys.exit(0 if ok else 1)
