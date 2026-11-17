#!/usr/bin/env python3
"""gen_signs12.py — מייצר את טבלת הזהות של סט 12 (catalog.js של המעצב) לחלק 074v_signs12.js.
   רשומה לכל מקום במשחק (placeId): [מזהה, שם, מפתח מותג או '', צבע, קוד סוג]. בלי תמונות."""
import json, sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
arr = json.loads(s[s.index('=') + 1:s.rindex(']') + 1])
CLS = {'existing_brand_place': 'b', 'existing_shared_brand_family': 'f', 'residence_not_independent_business': 'r',
       'place_or_infrastructure_review_surface_before_branding': 'p', 'operational_shared_symbol_or_infrastructure': 'o',
       'mission_coordinate_not_sign_entity': 'm', 'activity_or_vehicle_not_business_identity': 'a',
       'historical_update_note_not_a_new_place': 'h', 'previously_deferred_requires_current_game_check': 'd',
       'current_source_entity': 'c', 'airport_fence_viewpoint_no_panel': 'v', 'no_independent_brand_in_prior_brief': 'n',
       'no_sign_face_defined_in_brief': 'n'}
ROLE = {'city': '', 'park': 'P', 'farm': 'F', 'workshop': 'W', 'wc': 'T'}
rows = []
for a in arr:
    pid = a.get('placeId')
    if not pid: continue
    faces = [f.get('text') for k, f in a['formats'].items() if k.startswith('face_') and f.get('text')]
    rows.append([pid, a['name'], a.get('brandKey') or '', a.get('color') or '', CLS.get(a.get('classification'), 'x') + ROLE.get(a.get('role') or 'city', ''), len(faces)])
rows.sort(key=lambda r: r[0])
js = json.dumps(rows, ensure_ascii=False, separators=(',', ':'))
open(out, 'w', encoding='utf-8').write(js)
print(len(rows), 'רשומות', len(js), 'בתים')
