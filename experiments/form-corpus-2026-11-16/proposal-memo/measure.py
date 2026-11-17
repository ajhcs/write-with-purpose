#!/usr/bin/env python3
"""Reproduce bounded FRUS transcription measurements; not a classifier or quality assessment."""
import csv,hashlib,json,re,statistics,requests
from html.parser import HTMLParser
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parent
CACHE=Path('/workspace/tmp/builderbob/writing-corpus/proposal-memo'); CACHE.mkdir(parents=True,exist_ok=True)
class Node:
 def __init__(self,tag='',attrs=()): self.tag=tag; self.a=dict(attrs); self.children=[]
class Tree(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a); self.stack[-1].children.append(n)
  if t not in {'br','hr','meta','link','img','input','source','wbr','area','base','embed','param','track'}:self.stack.append(n)
 def handle_startendtag(self,t,a): self.handle_starttag(t,a); self.handle_endtag(t)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].children.append(s)
def walk(n):
 if isinstance(n,str):return
 yield n
 for c in n.children:yield from walk(c)
def skip(n):
 c=n.a.get('class','');return 'footnotes' in c or 'tei-opener' in c or 'tei-pb1' in c or n.a.get('rel')=='footnote' or n.tag in ('style','script')
def content(n,omit_blocks=False):
 if isinstance(n,str):return n
 if skip(n):return ''
 if omit_blocks and n.tag in ('ul','ol','li','p'):return ''
 return ''.join(content(c,True) for c in n.children)
def clean(s):return re.sub(r'\s+',' ',s).strip()
def words(s):return re.findall(r"[\w]+(?:[’'-][\w]+)*",s,flags=re.UNICODE)
def sentences(s):return [x for x in re.split(r'(?<=[.!?])\s+(?=[A-Z“"(])',s) if words(x)]
def extract(root,docid):
 div=next((n for n in walk(root) if n.a.get('id')==docid and 'tei-div3' in n.a.get('class','')),None)
 if not div:raise ValueError('document div missing')
 title=next((clean(content(n)) for n in walk(div) if n.tag in ('h2','h3')), '')
 dates=[clean(content(n)) for n in walk(div) if 'tei-date' in n.a.get('class','')]
 units=[]
 def visit(n, in_foot=False):
  if isinstance(n,str) or skip(n):return
  if n.tag in ('p','li','h4','h5'):
   s=clean(content(n));
   if s:
    kind='heading' if 'section-title' in n.a.get('class','') else ('choice' if n.tag=='p' and re.match(r'^(approve|disapprove|speak to me)\b',s,re.I) else ('li' if n.tag=='p' and s.startswith(('—','–')) else n.tag))
    units.append((kind,s))
  for c in n.children:visit(c)
 visit(div)
 # SUBJECT is routing metadata, not prose; consume its immediately following item.
 if units and units[0][0] in ('h4','h5') and units[0][1].upper()=='SUBJECT':
  units=units[2:] if len(units)>1 and units[1][0]=='li' else units[1:]
 return title,dates[:1],units

def run():
 records=json.loads((ROOT/'candidates.json').read_text()); out=[]
 for rec in records:
  if rec['form']!='decision memo':continue
  url=rec['url']; fn=CACHE/(rec['id']+'.html')
  if not fn.exists():
   res=requests.get(url,timeout=30);res.raise_for_status();fn.write_bytes(res.content)
  data=fn.read_bytes(); tree=Tree();tree.feed(data.decode('utf-8'))
  title,dates,units=extract(tree.root,url.rsplit('/',1)[-1]); prose=[s for t,s in units if t=='p'];lists=[s for t,s in units if t=='li']; headings=[s for t,s in units if t in ('h4','h5','heading')];choices=[s for t,s in units if t=='choice']
  ps=[len(words(s)) for s in prose]; ss=[len(words(z)) for p in prose for z in sentences(p)]; full=' '.join(prose+lists+choices)
  out.append(dict(id=rec['id'],title=title,date=dates[0] if dates else '',sha256=hashlib.sha256(data).hexdigest(),unit='published primary memorandum transcription; excludes editorial footnotes, routing opener and subject; includes decision alternatives as list items',paragraphs=len(prose),prose_words=sum(ps),prose_sentences=len(ss),median_paragraph_words=round(statistics.median(ps),1) if ps else None,median_sentence_words=round(statistics.median(ss),1) if ss else None,list_items=len(lists),list_words=sum(len(words(s)) for s in lists),decision_choice_lines=len(choices),decision_choice_words=sum(len(words(s)) for s in choices),explicit_headings=len(headings),all_body_words=len(words(full)),word_char_mean=round(sum(len(w) for w in words(full))/len(words(full)),2) if full else None,heading_text=headings))
  print(rec['id'], title[:105], dates, 'p/list/head',len(prose),len(lists),len(headings),'words',len(words(full)))
 (ROOT/'metrics.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':run()
