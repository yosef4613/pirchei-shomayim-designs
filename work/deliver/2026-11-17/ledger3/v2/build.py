# -*- coding: utf-8 -*-
# בונה את ledger.json ואת ledger.html מתוך items.py. הרצה: python3 -I build.py (מתוך התיקייה tools)
import json, re, os, sys, html, datetime, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE)
sys.path.insert(0,HERE)
import items
W='/home/user/tc_root/tc/pkg/work'
TODAY=['ledger','docs','f9fix','stadium','seatrees','mapfix','newgame','locks','pier','missions','actions','portraits','opening','cutscenes','loading','events','fieldcalc','fieldfix','island','garage','carrier','signs','posters','buses','police','w17','voiceint','sealife','farm','perf','gfxlib','threed','fieldthru']
LATER=['planrev','merge','merge2','ledger2']
now=subprocess.run(['date','+%d.%m.%Y %H:%M'],capture_output=True,text=True,env={'TZ':'Asia/Jerusalem'}).stdout.strip()
U=getattr(items,'U',{})
rows=[]
for i,x in enumerate(items.I,1):
    x=dict(x);rid='L-%03d'%i;up=U.get(rid,{})
    x['state298']=x['state']
    if 's' in up: x['state']=up['s']
    if 'f' in up: x['found298']=x['found']; x['found']=up['f']
    if 'ag' in up: x['agent']=up['ag']
    ag=x['agent']
    if 't' in up: today=up['t']
    elif ag in TODAY: today='בעבודה היום'
    elif ag in LATER: today='בעבודה היום (גל מאוחר)'
    elif ag=='ממתין לבעלים': today='ממתין לבעלים'
    elif ag=='—': today='נעשה'
    else: today='לא מכוסה — גל 2'
    if x['state']=='נעשה' and today in ('בעבודה היום','לא מכוסה — גל 2'): today='נעשה'
    x['rev2']=('נבדק ע״י בקר שני — '+up['n']) if up.get('n') else ('נבדק ע״י בקר שני — עודכן לפי S7F299' if up else 'נבדק ע״י בקר שני — בלי שינוי (הקוד של השורה לא השתנה ב-S7F299)')
    rows.append(dict(id=rid,**x,today=today))
# בדיקות הבקר השני: לכל פתוח — סוכן / גל 2 / ממתין; "נעשה" לא "בעבודה"; כיסוי הביקורת וההחלטות
ALLOWED=set(TODAY)|set(LATER)|{'לא מכוסה — גל 2','ממתין לבעלים','—'}
bad_agent=[r['id'] for r in rows if r['agent'] not in ALLOWED]
open_no_owner=[r['id'] for r in rows if r['state']!='נעשה' and r['agent']=='—']
done_but_open=[r['id'] for r in rows if r['state']=='נעשה' and r['today'] in ('בעבודה היום','לא מכוסה — גל 2','מוכן למיזוג — הגל הבא')]
not_checked=[r['id'] for r in rows if r['state']=='לא נבדק']
rf=set()
for r in rows:
    for s_ in r['src']:
        if s_.startswith('Review_full'):
            for a_,b_ in re.findall(r'#(\d+)(?:[–-]#?(\d+))?',s_): rf.update(range(int(a_),int(b_ or a_)+1))
rf_missing=[n for n in range(1,57) if n not in rf]
alltx=' '.join(' '.join(r['src'])+' '+r['req']+' '+r['found']+' '+r['note'] for r in rows)
fp_missing=['F-%02d'%n for n in range(1,11) if ('F-%02d'%n) not in alltx]
PROC={683:'המכסה (הוחלף ב-D‑688)',688:'המכסה — 98%',689:'קודם למצוא, אחר כך לתקן (כלל 19 / 19א)',690:'כל מה שנעשה נכנס לגרסה של היום'}
d_missing=[n for n in range(683,699) if ('D‑%d'%n) not in alltx and n not in PROC]
agents_wo_row=[a for a in TODAY if a!='ledger' and not any(r['agent']==a for r in rows)]
# כיסוי משימות tasks.json
tj=json.load(open(W+'/deliver/2026-11-12/review/plan_s7f298_site/Turbo_City_after_S16_tasks.json',encoding='utf-8'))
alltxt=' '.join(' '.join(r['src']) for r in rows)
missing=[t['id'] for t in tj['tasks'] if not re.search(r'(?<![A-Z0-9-])'+re.escape(t['id'])+r'(?![0-9])',alltxt)]
# כיסוי סעיפי Owner_requests (1–16)
orsec=set()
for r in rows:
    for s in r['src']:
        if s.startswith('Owner_requests'):
            for m in re.findall(r'§(\d+)',s): orsec.add(int(m))
or_missing=[n for n in range(1,17) if n not in orsec]
cnt=lambda k,v: sum(1 for r in rows if r[k]==v)
summary=dict(total=len(rows),
  state={s:cnt('state',s) for s in ['נעשה','חלקי','לא','לא נבדק']},
  today={s:cnt('today',s) for s in ['נכנס ל-S7F299','מוכן למיזוג — הגל הבא','בעבודה היום','בעבודה היום (גל מאוחר)','לא מכוסה — גל 2','ממתין לבעלים','נעשה']},
  state298={s:cnt('state298',s) for s in ['נעשה','חלקי','לא','לא נבדק']},
  changed_by_s7f299=[r['id'] for r in rows if r['state']!=r['state298']],
  rev2=dict(bad_agent=bad_agent,open_without_owner=open_no_owner,done_but_open=done_but_open,not_checked=not_checked,
    review_full_missing=rf_missing,review_part2_F_missing=fp_missing,decisions_missing=d_missing,
    decisions_process_only={('D‑%d'%k):v for k,v in PROC.items()},agents_without_row=agents_wo_row),
  open_total=sum(1 for r in rows if r['state']!='נעשה'),
  open_uncovered=sum(1 for r in rows if r['state']!='נעשה' and r['today']=='לא מכוסה — גל 2'),
  tasks_json_missing=missing, owner_requests_sections_missing=or_missing)
agents={}
for r in rows:
    if r['state']!='נעשה': agents.setdefault(r['agent'],[]).append(r['id'])
doc=dict(title='הרשימה המרוכזת — טורבו סיטי',round='17.11.2026',base='S7F299 (int299 930919a, נמסר 07:05) — המצב בקוד; המצב ב-S7F298 (הבנייה של הביקורת 12.11) — בשדה state298',
  built=now, version='טיוטה 2 — נבדק ע״י בקר שני (ledger2)', sources=['deliver/2026-11-12/review/Owner_requests_all_1112.txt','deliver/2026-11-12/review/Review_full_owner_1112.txt','deliver/2026-11-12/review/Review_part2_F_logos_vehicles_island_airfield_1112.md','deliver/2026-11-12/review/plan_s7f298_site/Turbo_City_after_S16_tasks.json (66)','HANDOFF_NEXT.md','DECISIONS_1110.md D‑683–D‑698','HANDOFF_1111.md','התמליל — הודעות הבעלים 10.11–16.11 (255 הודעות)','HANDOFF_1111 — 07:05 (17.11) נמסר S7F299 + הודעות הבעלים 07:58 / 08:10','deliver/2026-11-17/*/handback.txt — שורות "מוכן למיזוג" (09:15)'],
  states_legend={'נעשה':'קיים בקוד של S7F299','חלקי':'חלק קיים — חסר מה שבשורה','לא':'לא קיים בקוד של S7F299','לא נבדק':'לא אומת בקוד'},
  today_legend={'נכנס ל-S7F299':'נבנה היום ונכנס במסירה של 07:05','מוכן למיזוג — הגל הבא':'יש שורת "מוכן למיזוג" שעוד לא ב-master (גל 09:15 / ~12:30)','בעבודה היום':'סוכן של היום עובד על זה','לא מכוסה — גל 2':'פתוח ואין לו סוכן היום'},
  reviewed='נבדק ע״י בקר שני (ledger2) — 17.11, מול המקורות ומול הקוד של S7F299',
  summary=summary, open_by_agent=agents, items=rows)
json.dump(doc,open(OUT+'/ledger.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(summary,ensure_ascii=False,indent=1))
print('agents:',{k:len(v) for k,v in agents.items()})

# ===== HTML =====
data=json.dumps(doc,ensure_ascii=False).replace('</','<\\/')
tpl=open(HERE+'/page.html',encoding='utf-8').read()
open(OUT+'/ledger.html','w',encoding='utf-8').write(tpl.replace('/*@@DATA@@*/null',data))
print('ok', os.path.getsize(OUT+'/ledger.html'))
