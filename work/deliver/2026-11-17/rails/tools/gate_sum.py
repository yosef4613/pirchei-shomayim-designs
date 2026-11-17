# rails 17.11 — סיכום הבדיקות החוסמות של ניסיון: python3 gate_sum.py tryNNNN
import json,sys,os,re
T=sys.argv[1];D='/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/rails/qa/'
def J(n):
    p=D+T+'_'+n+'.json'
    try: return json.load(open(p))
    except Exception as e: return {'_err':str(e)[:120]}
def L(n):
    try: return open(D+T+'_'+n+'.log').read()[-600:]
    except Exception: return ''
r=J('rails');print('rails_check:',r.get('ok'),r.get('fail'),'pageErrors',r.get('pageErrors'),'| pax',r.get('pax',{}).get('ok'),r.get('pax',{}).get('issues'),'| rl',r.get('rl',{}).get('ok'),r.get('rl',{}).get('issues'),'| rli',r.get('rli'),'| net',r.get('net'))
print('  sweep:',r.get('sweep',{}).get('ok'),(r.get('sweep',{}).get('issues') or [])[:4]);print('  trains:',[(t['id'],t['cycle'],t['stall']) for t in r.get('trains',[])]);print('  crossings:',r.get('crossings'));print('  rjx:',r.get('rjx'),'drawn',r.get('drawn'))
print('  not drawn:',[t for t in r.get('turnouts',[]) if not t.get('by')])
q=J('qingame');ra=q.get('roadAudit') if isinstance(q,dict) else None
print('q_ingame: errors',q.get('errors'),'roadAudit',(ra if not isinstance(ra,dict) else {k:ra.get(k) for k in ('ok','pass','total','n','fail')}),'railNet',str(q.get('railNet'))[:200],'rl',str(q.get('rl'))[:300]); print('  log:',L('qingame')[-300:])
g=J('rules');print('rules_gate:',{k:g.get(k) for k in ('ok','fails')} if isinstance(g,dict) else g,'|',L('rules')[-200:])
p=J('people');print('people_on_road:',{k:p.get(k) for k in ('ok','samples','people','drawn','onLane','errs')} if isinstance(p,dict) else p,'|',L('people')[-200:])
print('stuckmax:',L('stuck')[-400:])
