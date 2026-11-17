# בונה מחדש את גלריית הציורים של 17.11 מכל השורות "הציור מוכן:" בהחזרות; מדפיס את מפת הקבצים לפרסום (JSON) ומה חדש.
import re,os,glob,json,html,sys
W='/home/user/tc_root/tc/pkg/work'; G='/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/gallery1117'
os.makedirs(G+'/d',exist_ok=True)
HE=json.load(open(W+'/deliver/2026-11-17/tools/gallery_names.json',encoding='utf-8'))
order=['פתיחה','סיפור ומשימות','השדה','העולם','תנועה','כלים','ניסויים','אחר']
items=[];bad=[]
for hb in sorted(glob.glob(W+'/deliver/2026-11-17/*/handback.txt')):
    ag=hb.split('/')[-2]; n=0
    for line in open(hb,encoding='utf-8'):
        if not line.startswith('הציור מוכן'): continue
        for m in re.finditer(r'((?:/home/user/tc_root/tc/pkg/work/|W/)?deliver/2026-11-17/[^\s()]+?\.html)',line):
            p=m.group(1); p=W+p[1:] if p.startswith('W/') else (p if p.startswith('/') else W+'/'+p)
            if not os.path.exists(p): continue
            s=open(p,encoding='utf-8',errors='replace').read()
            s=s.replace(' (גברים ונערים)',''); s=re.sub(r'<li><b>כלל 7:</b>[^<]*</li>','',s)
            if re.search(r'גברים|נערים בלבד|<img\b',s) or re.search(r'data:image/',s): bad.append(p); continue
            back='<a href="../" style="position:fixed;top:10px;right:10px;z-index:2147483647;background:#1d5f8c;color:#fff;padding:7px 14px;border-radius:8px;font:600 15px Arial,sans-serif;text-decoration:none;box-shadow:0 2px 8px #0004" dir="rtl">→ חזרה לרשימת הציורים</a>'
            m2=re.search(r'<body[^>]*>',s,re.I)
            s=(s[:m2.end()]+back+s[m2.end():]) if m2 else back+s
            key=ag if n==0 else '%s_%d'%(ag,n); n+=1
            fn='d/%s.html'%key; open(os.path.join(G,fn),'w',encoding='utf-8').write(s)
            g,t=HE.get(ag,['אחר',ag]); items.append((g,t+('' if n==1 else ' (%d)'%n),fn,os.path.getsize(p)))
for ln in open(W+'/deliver/2026-11-17/tools/gallery_extra.txt',encoding='utf-8'):
    ln=ln.strip()
    if not ln: continue
    ag,p=ln.split('|',1)
    if not os.path.exists(p): continue
    s=open(p,encoding='utf-8',errors='replace').read()
    back='<a href="../" style="position:fixed;top:10px;right:10px;z-index:2147483647;background:#1d5f8c;color:#fff;padding:7px 14px;border-radius:8px;font:600 15px Arial,sans-serif;text-decoration:none;box-shadow:0 2px 8px #0004" dir="rtl">→ חזרה לרשימת הציורים</a>'
    m2=re.search(r'<body[^>]*>',s,re.I); s=(s[:m2.end()]+back+s[m2.end():]) if m2 else back+s
    fn='d/%s_x_%s'%(ag,os.path.basename(p)); open(os.path.join(G,fn),'w',encoding='utf-8').write(s)
    g,t=HE.get(ag,['אחר',ag]); items.append((g,os.path.basename(p).replace('.html','').replace('_',' ')+' — '+t,fn,os.path.getsize(p)))
import hashlib,subprocess
SP=W+'/deliver/2026-11-17/tools/gallery_state.json'; ST=json.load(open(SP,encoding='utf-8'))
now=subprocess.run(['bash','-c','TZ=Asia/Jerusalem date +%H:%M'],capture_output=True,text=True).stdout.strip()
changed=[]
for _,_,fn,_ in items:
    h=hashlib.sha1(open(os.path.join(G,fn),'rb').read()).hexdigest()[:12]; e=ST['items'].get(fn)
    if e is None: changed.append((fn,'new',h))
    elif e['sha']!=h: changed.append((fn,'upd',h))
if changed:
    ST['rev']+=1; r=ST['rev']
    for fn,k,h in changed:
        e=ST['items'].setdefault(fn,{'first':r,'t_first':now}); e.update(sha=h,upd=r,t_upd=now)
    json.dump(ST,open(SP,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
R=ST['rev']
def badge(fn):
    e=ST['items'].get(fn,{})
    if e.get('first')==R: return '<span class="new">חדש · עדכון %d · %s</span>'%(R,e['t_first'])
    if e.get('upd')==R: return '<span class="upd">עודכן · עדכון %d · %s</span>'%(R,e['t_upd'])
    if e.get('upd',1)>1: return '<span class="old">עודכן בעדכון %d · %s</span>'%(e['upd'],e['t_upd'])
    return ''
rows=''
for r in range(R,max(0,R-3),-1):  # שלושת העדכונים האחרונים, מהחדש לישן (בלי כפילויות)
    fresh=[i for i in items if ST['items'].get(i[2],{}).get('upd')==r]
    if not fresh: continue
    tt=max(ST['items'][i[2]].get('t_upd','') for i in fresh)
    hd=('בעדכון האחרון — עדכון %d · %s'%(r,tt)) if r==R else ('עדכון %d · %s'%(r,tt))
    rows+='<section class="fresh"><h2>%s <span class="n">%d</span></h2><ul>'%(hd,len(fresh))
    for _,t,fn,sz in fresh:
        e=ST['items'][fn]; b=('<span class="new">חדש · עדכון %d · %s</span>'%(r,e['t_first'])) if e.get('first')==r else ('<span class="upd">עודכן · עדכון %d · %s</span>'%(r,e['t_upd']))
        rows+='<li><a href="%s">%s</a>%s</li>'%(fn,html.escape(t),b)
    rows+='</ul></section>'
for g in order:
    its=[i for i in items if i[0]==g]
    if not its: continue
    rows+='<section><h2>%s <span class="n">%d</span></h2><ul>'%(g,len(its))
    for _,t,fn,sz in its: rows+='<li><a href="%s">%s</a>%s<span class="kb">%s ק״ב</span></li>'%(fn,html.escape(t),badge(fn),format(round(sz/1024),','))
    rows+='</ul></section>'
idx=open(G+'/index.html',encoding='utf-8').read()
a=idx.index('<section') if '<section' in idx else idx.index('</main>'); b=idx.index('</main>')
open(G+'/index.html','w',encoding='utf-8').write(idx[:a]+rows+idx[b:])
json.dump({fn:os.path.join(G,fn) for _,_,fn,_ in items},open(G+'/files.json','w'),ensure_ascii=False)
# גיטהב: דף מלא + אותם ציורים
GH='/home/user/pirchei-shomayim-designs/turbo-city/drawings/2026-11-17'; import shutil
os.makedirs(GH+'/d',exist_ok=True)
for _,_,fn,_ in items: shutil.copy(os.path.join(G,fn),os.path.join(GH,fn))
body=open(G+'/index.html',encoding='utf-8').read()
open(GH+'/index.html','w',encoding='utf-8').write('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+body.replace('<main>','</head><body><main>',1).replace('</main>','<p style="color:var(--muted);font-size:.85rem">גם בגלריה: https://claude.ai/artifact/JiEuCJLoWcGeujf4gRe6zM</p></main></body>')+'</html>\n')
print(len(items),'ציורים; נפסלו:',bad,'| עדכון',R,'| חדשים/עודכנו עכשיו:',[c[0] for c in changed])
