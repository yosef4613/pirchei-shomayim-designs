# summ.py <try> — תקציר התוצאות של ניסיון אחד (leftovers 17.11)
import json,sys,os,re
T=sys.argv[1];O='/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/leftovers/qa/'+T
def J(n):
    try: return json.load(open(os.path.join(O,n)))
    except Exception as e: return None
print(open(O+'/build.txt').read().strip())
print(open(O+'/runs.tsv').read().strip().replace('\t',' '))
d=J('ingame.json')
if d:
    ra=d['roadAudit'];ch=ra.get('checks') or []
    fl=[c.get('name') or c.get('id') for c in ch if isinstance(c,dict) and not c.get('ok')]
    print('ingame: ok',ra.get('ok'),'total',ra.get('total'),'pass',sum(1 for c in ch if isinstance(c,dict) and c.get('ok')),'fails',fl,'errors',d.get('errors'))
r=J('rules.json')
if r: print('rules:',r.get('ok'),r.get('fails'))
p=J('people.json')
if p: print('people:',{k:p[k] for k in p if k in('ok','onLane','errs','samples','maxPeople')})
s=os.path.join(O,'stuck.log')
if os.path.exists(s):
    L=[l for l in open(s) if l.startswith('{')];print('stuck:',L[-1].strip()[:400] if L else open(s).read()[-300:])
