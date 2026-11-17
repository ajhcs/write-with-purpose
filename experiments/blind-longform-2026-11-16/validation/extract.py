from html.parser import HTMLParser
from pathlib import Path
class N:
 def __init__(self,t='',a=(),p=None): self.t=t;self.a=dict(a);self.p=p;self.c=[]
class P(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.root=N();self.n=self.root;self.feed(s)
 def handle_starttag(self,t,a):
  n=N(t,a,self.n);self.n.c.append(n)
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.n=n
 def handle_startendtag(self,t,a): self.handle_starttag(t,a);self.handle_endtag(t)
 def handle_endtag(self,t):
  x=self.n
  while x.p and x.t!=t:x=x.p
  if x.t==t:self.n=x.p
 def handle_data(self,d):self.n.c.append(d)
def walk(n):
 yield n
 for c in n.c:
  if isinstance(c,N):yield from walk(c)
def plain(n):return ''.join(plain(c) if isinstance(c,N) else c for c in n.c)
base=Path('/workspace/repos/builderbob/.writing-corpus-cache/blind-longform-2026-11-16')
if __name__=='__main__':
 for f in ['cole-cs50','cole-engineering','doctorow','python']:
  p=P((base/(f+'.html')).read_text());print('\n',f)
  for n in walk(p.root):
   if n.t in ['main','article'] or (n.t=='div' and (any(x in n.a.get('class','') for x in ['prose','content','body']) or n.a.get('role')=='main')):
    print(n.t,n.a.get('class'),n.a.get('id'),len(plain(n)), repr(plain(n)[:140]))

def inline(n):
 if isinstance(n,str):return n
 if n.t in ('script','style','img','svg') or 'headerlink' in n.a.get('class','') or (n.t=='a' and n.a.get('href','').startswith('#note-ref-')):return ''
 if n.a.get('class')=='claim-note':
  marker=next((x for x in walk(n) if x.a.get('class')=='claim-note-fallback'),None)
  return ' ['+plain(marker)+']' if marker else ''
 s=''.join(inline(c) for c in n.c)
 if n.t=='br':return '\n'
 if n.t=='a' and n.a.get('href') and not n.a['href'].startswith('#') and s.strip() and s.strip()!=n.a['href']:
  from urllib.parse import urljoin
  return '['+s+']('+urljoin(current_url,n.a['href'])+')'
 if n.t in ('em','i'):return '*'+s+'*'
 if n.t in ('strong','b'):return '**'+s+'**'
 if n.t=='code':return '`'+s+'`'
 return s

def compact(s):
 import re
 return re.sub(r'\s+',' ',s).strip()
def blocks(n, skiptitle=False):
 out=[]
 def go(n):
  if not isinstance(n,N):return
  cl=n.a.get('class','')
  if n.t in ('figure','aside','table','script','style','nav') or cl in ('transfer-table',):return
  if n.t=='div' and 'highlight-' in cl:
   pre=next((x for x in walk(n) if x.t=='pre'),None)
   if pre:out.append('```\n'+plain(pre).rstrip('\n')+'\n```')
   return
  if n.t in ('h1','h2','h3','h4'):
   if skiptitle and n.t=='h1':return
   out.append('#'*int(n.t[1])+' '+compact(inline(n)));return
  if n.t in ('p','li','blockquote'):
   s=compact(inline(n))
   if s:out.append(('> ' if n.t=='blockquote' else '- ' if n.t=='li' else '')+s)
   return
  for c in n.c:go(c)
 go(n);return out

def produce():
 import json,hashlib,re,shutil
 target=Path(__file__).resolve().parent.parent;dest=target/'sources'
 names=['cole-cs50','cole-engineering','doctorow','python']; manifest=json.loads((base/'fetch-manifest.json').read_text())
 titles=['Learning CS50 at 256 Kilobits per Second','Making engineering part of healthcare’s work',"Tiktok’s enshittification",'Floating Point Arithmetic: Issues and Limitations']
 docs=[]
 for i,f in enumerate(names):
  global current_url
  current_url=manifest[i]['url']
  tree=P((base/(f+'.html')).read_text())
  if i<2:
   root=next(n for n in walk(tree.root) if 'essay-prose' in n.a.get('class','')); b=blocks(root)
  elif i==2:
   root=next(n for n in walk(tree.root) if n.a.get('class')=='entry-content');children=root.c;on=False;b=[]
   for n in children:
    if not isinstance(n,N):continue
    if n.t=='h1' and "Tiktok's enshittification" in plain(n):on=True;continue
    if on and n.t=='h1':break
    if on:b.extend(blocks(n))
  else:
   root=next(n for n in walk(tree.root) if n.a.get('class')=='body');b=blocks(root,True)
  text='\n\n'.join(b)+'\n'; ident=f'S{i+1:02d}'; path=dest/(ident+'.md');path.write_text(text)
  # Select consecutive full prose paragraphs, avoiding code, headings, notes and URL-only paragraphs.
  paras=[];pos=0;section=('Floating Point Arithmetic: Issues and Limitations' if i==3 else 'Unheaded essay')
  for block in b:
   start=text.index(block,pos);pos=start+len(block)
   if block.startswith('#'):section=block.lstrip('# ').strip();continue
   if block.startswith(('```','- ','> ')) or block.startswith('http') or section=='Notes':continue
   count=len(re.findall(r'\b[\w]+(?:[’\'-][\w]+)*\b',block))
   if count>=35:paras.append((start,pos,count,section))
  # Form windows from adjacent prose blocks with total 120-250 words whenever possible.
  candidates=[]
  for j,(a,e,w,sec) in enumerate(paras):
   for k in range(j,min(j+4,len(paras))):
    aa,ee,ww,ss=paras[k]
    if ss!=sec or (k>j and text[paras[k-1][1]:aa]!='\n\n'):break
    total=sum(x[2] for x in paras[j:k+1])
    if 100<=total<=260:candidates.append((a,ee,total,sec));
    if total>260:break
  selected=[]
  for frac in [0.08,0.48,0.88]:
   valid=[c for c in candidates if all(c[1]<=x[0] or c[0]>=x[1] for x in selected)]
   if not valid:raise Exception((f,'insufficient windows',len(candidates)))
   c=min(valid,key=lambda x:(abs((x[0]+x[1])/2-frac*len(text))/len(text)+abs(x[2]-160)/2000));selected.append(c)
  selected.sort();passages=[]
  for label,(a,e,w,sec) in zip(['opening','middle','closing'],selected):
   passages.append(dict(id=label,label=label.capitalize(),section=sec,start=a,end=e,text=text[a:e],context_before=text[max(0,a-250):a],context_after=text[e:min(len(text),e+250)]))
  docs.append(dict(id=ident,title=titles[i],author=['Cole Lyons','Cole Lyons','Cory Doctorow','Python Software Foundation'][i],url=manifest[i]['url'],form=['Personal essay','Personal essay','Commentary essay','Technical documentation'][i],audience=['General readers interested in learning','Healthcare and engineering readers','General technology readers','Python learners'][i],permission=['User-authorized','User-authorized','CC BY 4.0; source excludes third-party quotations and images from its license','Python documentation license; cached license retained'][i],source_file=ident+'.md',source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),word_count=len(re.findall(r'\b[\w]+(?:[’\'-][\w]+)*\b',re.sub(r'\]\([^)]*\)',']',text))),extraction_scope=['Article narrative and notes; visual inserts omitted','Article narrative and notes; visual inserts omitted','Main essay between matching heading and next heading; hyperlinks and quotation retained','Tutorial body prose and exact preformatted examples; navigation, title and figures/tables omitted'][i],exact_code_blocks=[x[4:-4] for x in b if x.startswith('```\n')],passages=passages))
 shutil.copyfile(base/'python-license.html',dest/'python-license.html')
 (dest/'documents.json').write_text(json.dumps({'documents':docs},ensure_ascii=False,indent=2)+'\n')
 print([(d['id'],d['word_count'],[(p['id'],len(p['text'].split())) for p in d['passages']],len(d['exact_code_blocks'])) for d in docs])
if __name__=='__main__':produce()
