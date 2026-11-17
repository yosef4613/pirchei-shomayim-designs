# -*- coding: utf-8 -*-
"""1.11 (R-51 (3)): one list of the names — the 80 zones and the streets of the road map — that the game, the map and the plan read.
Written by the map's build into names.json (the zone codes and names of plan7b_svg.ZN; every street of the map with its segments and its
half width, so the game can say which street is nearest to a point)."""
import json, os
def write(P, ZN, path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names.json')):
    rn = {r['id']: r['name'] for r in P['roads']}; hw = {k: v.get('halfW') for k, v in P['classes'].items()}
    streets = []
    for s in P['segments']:
        if s.get('kind') == 'bridge' and not rn.get(s['road']): continue
        streets.append(dict(road=s['road'], name=rn.get(s['road'], ''), hw=hw.get(s['cls'], 40), pts=[[round(p[0]), round(p[1])] for p in s['pts']]))
    out = dict(source='city_plan.json · ' + P.get('title', ''), zones={z: v[0] for z, v in ZN.items()}, streets=streets)
    json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return out
if __name__ == '__main__':
    import plan7b_svg as SV
    P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'city_plan.json'), encoding='utf-8'))
    o = write(P, SV.ZN); print(len(o['zones']), 'zones ·', len(o['streets']), 'street segments')
