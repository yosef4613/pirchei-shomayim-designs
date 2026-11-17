import re,glob,os,sys,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from nf_words import EN,HE
D=sys.argv[1]; BL=set(sys.argv[2].split(','))
rows=[]
for f in sorted(glob.glob(D+'/*.txt')):
  s=open(f,encoding='utf-8').read(); low=s.lower(); n=len(s.encode())/100000
  c={}
  for w in EN: k=low.count(w); c[w]=k
  for w in HE: c[w]=len(re.findall(r'(?<![א-ת])[ובלהמשכ]{0,2}'+re.escape(w)+r'(?![א-ת])',s)) if len(w)<4 else s.count(w)
  sc=sum(EN.get(w,HE.get(w,0))*k for w,k in c.items())/n
  rows.append((os.path.basename(f)[:-4] in BL,os.path.basename(f),round(sc,1),round(n,2),c))
for b,f,sc,n,c in sorted(rows,key=lambda r:-r[2]):
  top=sorted(((EN.get(w,HE.get(w,0))*k,w,k) for w,k in c.items() if k),reverse=True)[:9]
  print('%s %-10s score/100KB %6.1f  %s'%('X' if b else '.',f,sc,' '.join('%s:%d'%(w,k) for _,w,k in top)))
