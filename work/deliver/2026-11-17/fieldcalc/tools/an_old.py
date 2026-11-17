# ניתוח ההרצה של המתכנן הישן (S7F272) — 3 זרעים, חלון 0–1800 שנ׳
import json,statistics as st,collections as C,sys
d=json.load(open(sys.argv[1]))
W=1800
res={'seeds':[]}
for S in d['seeds']:
    fl=[f for f in S['fl'] if not f['heli']]
    he=[f for f in S['fl'] if f['heli']]
    L=[f for f in fl if f['land'] is not None and 0<=f['land']<W]
    T=[f for f in fl if f['to'] is not None and 0<=f['to']<W]
    hL=[f for f in he if f['onb'] is not None and 0<f['onb']<W]
    hT=[f for f in he if f['dep'] is not None and 0<=f['dep']<W]
    mixL=C.Counter(f['ac'] for f in L); mixT=C.Counter(f['ac'] for f in T)
    st_used=C.Counter(f['sd'] for f in L+T)
    turn=[f['push']-f['onb'] for f in fl if f['onb'] is not None and f['push'] is not None and f['onb']>0]
    turnBy=C.defaultdict(list)
    for f in fl:
        if f['onb'] is not None and f['push'] is not None and f['onb']>0: turnBy[f['ac']].append(round(f['push']-f['onb']))
    rotA=[f['vac']-f['land'] for f in L if f['vac'] is not None]
    rotD=[f['dep']-f['lu'] for f in T if f['lu'] is not None]
    rollD=[f['dep']-f['to'] for f in T]
    taxiIn=[f['onb']-f['vac'] for f in L if f['onb'] and f['vac']]
    taxiOut=[f['lu']-f['push'] for f in T if f['lu'] and f['push']]
    holdW=[f['lu']-f['hold'] for f in T if f['lu'] and f['hold']]
    # מרווחים בין תנועות מסלול
    ev=sorted([f['land'] for f in L]+[f['to'] for f in T])
    gaps=[b-a for a,b in zip(ev,ev[1:])]
    svc=C.Counter()
    for f in fl:
        for s in (f['svc'] or '').split():
            svc[(f['ac'],s.split(':')[0])]+=1
    r=dict(seed=S['seed'],land=len(L),to=len(T),mov=len(L)+len(T),heliLand=len(hL),heliDep=len(hT),
        mixL=dict(mixL),mixT=dict(mixT),stands=dict(st_used),nStands=len(st_used),
        turn_med=round(st.median(turn)) if turn else None,turnBy={k:(min(v),round(st.median(v)),max(v),len(v)) for k,v in turnBy.items()},
        rotA=(round(min(rotA),1),round(st.median(rotA),1),round(max(rotA),1)),rotD=(round(min(rotD),1),round(st.median(rotD),1),round(max(rotD),1)),
        rollD=round(st.median(rollD),1),taxiIn=round(st.median(taxiIn)),taxiOut=round(st.median(taxiOut)),holdW=round(st.median(holdW),1),
        gapMin=round(min(gaps),1),gapMed=round(st.median(gaps),1),gapMax=round(max(gaps),1),
        stats={k:S['stats'][k] for k in ('planned','failed','recovered','queued','maxQueue')},why=S['stats'].get('why'),fleet=S['fleet'],reached=S['reached'])
    res['seeds'].append(r)
    res.setdefault('svcPairs',C.Counter()).update({'|'.join(k):v for k,v in svc.items()})
res['svcPairs']=dict(res['svcPairs'])
json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
for r in res['seeds']:
    print({k:v for k,v in r.items() if k not in('fleet','why','svcPairs')})
    print(' why',r['why'])
    print(' fleet',{k:(v['n'],v['used'],v['tasks'],v['busy']) for k,v in r['fleet'].items()})
print(res['svcPairs'])
