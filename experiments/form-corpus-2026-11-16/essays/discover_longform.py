#!/usr/bin/env python3
"""Record Longform essay-tag discovery metadata; never treat discovery as measurements."""
from html.parser import HTMLParser
from pathlib import Path
import datetime as dt,hashlib,json,time,requests
ROOT=Path(__file__).resolve().parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.post=None;self.depth=0;self.title=False;self.items=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='article' and 'post' in a.get('class','').split():self.post={'source_url':None,'title':''};self.depth=1;return
  if self.post:
   if t=='article':self.depth+=1
   if t=='a' and 'post__link' in a.get('class','').split() and not self.post['source_url']:self.post['source_url']=a.get('href')
   if t=='h2' and 'post__title' in a.get('class','').split():self.title=True
 def handle_data(self,s):
  if self.post and self.title:self.post['title']+=s
 def handle_endtag(self,t):
  if self.post and t=='h2':self.title=False
  if self.post and t=='article':
   self.depth-=1
   if self.depth==0:
    self.post['title']=' '.join(self.post['title'].split());self.items.append(self.post);self.post=None
seen=set();count=0
with (ROOT/'longform_essay_candidates.jsonl').open('w') as out,(ROOT/'longform_discovery_pages.jsonl').open('w') as pages:
 for n in range(1,16):
  u=f'https://longform.org/archive/tags/essay?p={n}'
  try:
   r=requests.get(u,headers={'User-Agent':'WritingFormResearch/1.0'},timeout=20);r.raise_for_status();p=Parser();p.feed(r.text)
   pages.write(json.dumps({'url':u,'status':r.status_code,'sha256':hashlib.sha256(r.content).hexdigest(),'retrieved_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'items':len(p.items)})+'\n');pages.flush()
   for x in p.items:
    if not x['source_url'] or x['source_url'] in seen:continue
    seen.add(x['source_url']);count+=1;x.update(discovery_url=u,selection='Longform editor-curated essay tag, not a popularity rank',form_eligibility='not_screened',fulltext_status='not_retrieved');out.write(json.dumps(x,ensure_ascii=False)+'\n')
   out.flush()
  except Exception as e:pages.write(json.dumps({'url':u,'error':str(e)[:200]})+'\n');pages.flush()
  time.sleep(.6)
print(count,'distinct candidates')
