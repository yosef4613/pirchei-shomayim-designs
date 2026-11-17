# מחלץ את B4 מתוכנית הדרכים (study/roads/city_plan.json) לקובץ נתונים קטן, במטרים — הנתונים של העולם, בלי שום ציור.
# python3 extract_b4.py <city_plan.json> <out.json>
import json, sys
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding='utf-8'))
X0, Y0, X1, Y1 = 1080, 2430, 2640, 3520          # חלון: B4 ועוד ~12 מ' מסביב (פיקסלים, 10 = 1 מ')
OX, OY = 1200, 2550                               # הראשית = כיכר הספורט J12_25
m = lambda v: round(v / 10.0, 2)
P = lambda p: [m(p[0] - OX), m(p[1] - OY)]
def inwin(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return max(xs) >= X0 and min(xs) <= X1 and max(ys) >= Y0 and min(ys) <= Y1
cls = d['classes']
roads = []
for s in d['segments']:
    if not inwin(s['pts']): continue
    c = cls[s['cls']]
    roads.append({'id': s['id'], 'name': next((r['name'] for r in d['roads'] if r['id'] == s['road']), ''), 'cls': s['cls'],
                  'lanes': s['lanes'], 'width': c['width_m'], 'walk': c['walk_m'], 'median': c.get('median_m', 0),
                  'speed': c['speed'], 'pts': [P(p) for p in s['pts']]})
nodes = [{'id': n['id'], 'kind': n['kind'], 'label': n['label'], 'p': P([n['x'], n['y']])}
         for n in d['nodes'] if X0 <= n['x'] <= X1 and Y0 <= n['y'] <= Y1]
R = lambda r: [m(r[0] - OX), m(r[1] - OY), m(r[2] - OX), m(r[3] - OY)]
sites = [{'id': s['id'], 'kind': s['kind'], 'rect': R(s['rect']), 'label': s['label'], 'floors': s.get('floors')}
         for s in d['sites'] if s['zone'] == 'B4']
lots = [{'id': s['id'], 'use': s['use'], 'rect': R(s['rect']), 'label': s['label']} for s in d['lots'] if s['zone'] == 'B4']
dws = [{'id': s['id'], 'lanes': s['lanes'], 'w': round(s['hw'] / 10 * 2 / 2, 2) if s['lanes'] == '1' else 6.0,
        'pts': [P(p) for p in s['pts']]} for s in d['site_roads'] if s['zone'] == 'B4']
blocks = [{'id': b['id'], 'rect': R(b['rect'])} for b in d['blocks'] if 'B4' in b['zones']]
ra = [r for r in d['roundabouts'] if r['node'] == 'J12_25']
CX0, CY0, CX1, CY1 = 500, 1850, 3300, 4150   # הסביבה: מבנים של האזורים השכנים — ברמת פירוט נמוכה
ctx = []
for s in d['sites'] + d.get('r9s_lots', []) + d.get('r9ayin_lots', []):
    z = s.get('zone'); r = s.get('rect')
    if z == 'B4' or not r or s.get('kind') not in ('building',): continue
    if r[2] < CX0 or r[0] > CX1 or r[3] < CY0 or r[1] > CY1: continue
    ctx.append({'id': s['id'], 'zone': z, 'rect': R(r), 'floors': s.get('floors') or 2})
out_d = {'zone': 'B4', 'purpose': d['zones']['B4']['purpose'], 'src': 'study/roads/city_plan.json (' + d.get('updated_until', '') + ')',
         'origin_px': [OX, OY], 'unit': 'מטר (10 פיקסלים במשחק = 1 מ׳)', 'window': R([X0, Y0, X1, Y1]), 'zone_rect': R([1200, 2550, 2510, 3400]),
         'roads': roads, 'nodes': nodes, 'roundabouts': [{'node': r['node'], 'label': r['label'], 'arms': r['arms']} for r in ra],
         'sites': sites, 'lots': lots, 'driveways': dws, 'blocks': blocks, 'context': ctx}
json.dump(out_d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(ctx), 'context', len(roads), 'roads', len(nodes), 'nodes', len(sites), 'sites', len(lots), 'lots', len(dws), 'dw')
