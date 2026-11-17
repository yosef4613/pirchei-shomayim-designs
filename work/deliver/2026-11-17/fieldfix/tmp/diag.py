import sys, json, io, contextlib, collections
sys.argv=['x','sim_rt.json','/dev/null','GA1']
src=open('../tools/ff_flights.py').read(); src=src[:src.index('FL = list(FL0)')]
exec(src)
for sid in ['GA1','P6','P1','C1']:
    busy=[w for a in FL0 for w in S.rwy_wins(a)]; ST=statics(sid); others=FL0+V0+ST
    nn=0; ok=0; C=collections.Counter()
    for tdep in range(0,T,12):
        for dtd in range(T-60,180,-24):
            a=make(sid,(tdep+dtd)%T,tdep,busy)
            if not a: nn+=1; continue
            with contextlib.redirect_stdout(io.StringIO()):
                h=S.ac_conflict(a,[o for o in others if o.id!='FL-'+sid],dt=2.0)
            if h: C[str(h)[:60]]+=1
            else: ok+=1
    print(sid,'none',nn,'ok',ok,C.most_common(6))
print('busy',sorted(busy))
