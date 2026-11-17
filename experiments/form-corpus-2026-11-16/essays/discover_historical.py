#!/usr/bin/env python3
"""Longform tagged essays, archive dates and original-publication links; discovery only."""
from html.parser import HTMLParser
from pathlib import Path
import datetime as dt,hashlib,json,re,time,requests
ROOT=Path(__file__).resolve().parent
class Archive(HTMLParser):
 def __init__(self):super().__init__();self.item=None;self.grab=None;self.items=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs);c=a.get('class','').split()
  if t=='article' and 'post' in c:self.item={'source_url':None,'title':'','date_display':'','publication':'','author':'','longform_record':None}
  elif self.item:
   if t=='a' and 'post__link' in c and not self.item['source_url']:self.item['source_url']=a.get('href')
   if t=='a' and 'post__permalink' in c:self.item['longform_record']=__import__('urllib.parse',fromlist=['urljoin']).urljoin('https://longform.org',a.get('href',''))
   if (t=='h2' and 'post__title' in c):self.grab='title'
   if t=='span' and 'post__date' in c:self.grab='date_display'
   if t=='a' and 'post__publication' in c:self.grab='publication'
   if t=='a' and 'post__author__link' in c:self.grab='author'
 def handle_data(self,s):
  if self.item and self.grab:self.item[self.grab]+=s
 def handle_endtag(self,t):
  if self.grab and ((self.grab=='title' and t=='h2') or (self.grab=='date_display' and t=='span') or (self.grab in ('author','publication') and t=='a')):self.grab=None
  if t=='article' and self.item:
   for k in ('title','date_display','publication','author'):self.item[k]=' '.join(self.item[k].split())
   m=re.search(r'\b(1[89]\d{2}|20\d{2})\b',self.item['date_display']);year=int(m.group()) if m else None
   self.item['year_display']=year;self.item['historical_stratum']=('pre_2015' if year<2015 else '2015_2019' if year<2020 else '2020_or_later') if year else 'unknown'
   self.items.append(self.item);self.item=None
seen=set();num=0
with (ROOT/'longform_dated_candidates.jsonl').open('w') as out,(ROOT/'longform_dated_pages.jsonl').open('w') as pages:
 for n in range(1,31):
  u=f'https://longform.org/archive/tags/essay?p={n}'
  try:
   r=requests.get(u,headers={'User-Agent':'WritingFormResearch/1.0'},timeout=20);r.raise_for_status();p=Archive();p.feed(r.text)
   pages.write(json.dumps({'url':u,'sha256':hashlib.sha256(r.content).hexdigest(),'retrieved_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'count':len(p.items)})+'\n')
   for x in p.items:
    if not x['source_url'] or x['source_url'] in seen:continue
    seen.add(x['source_url']);x.update(discovery_url=u,selection='Longform essay tag, editorial selection; no popularity ranking',screening='unreviewed',access='not_assessed');out.write(json.dumps(x,ensure_ascii=False)+'\n');num+=1
   out.flush();pages.flush()
  except Exception as e:pages.write(json.dumps({'url':u,'error':str(e)[:200]})+'\n');pages.flush()
  time.sleep(.6)
print(num)
