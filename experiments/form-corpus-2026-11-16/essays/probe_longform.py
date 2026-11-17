#!/usr/bin/env python3
"""One page per publisher; honor robots, redirects, refusals and declared paywalls."""
from urllib.parse import urlparse,urljoin
from urllib.robotparser import RobotFileParser
from html.parser import HTMLParser
from pathlib import Path
import datetime as dt,hashlib,json,re,requests,time
from acquire_measure import WORD,SENT
ROOT=Path(__file__).resolve().parent; CACHE=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16/longform');CACHE.mkdir(parents=True,exist_ok=True)
HEAD={'User-Agent':'WritingFormResearch/1.0'}
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.art=0;self.skip=0;self.p=None;self.ps=[];self.heading=0;self.heads=[];self.h='';self.count={'a':0,'ul':0,'ol':0,'figure':0,'blockquote':0,'pre':0};self.title='';self.in_title=False
 def handle_starttag(self,t,a):
  d=dict(a);c=' '.join([d.get('class',''),d.get('id','')]).lower()
  if t=='title':self.in_title=True
  if t=='article':self.art+=1
  if self.art:
   if self.skip:self.skip+=1;return
   if t in ('nav','aside','header','footer','script','style','form') or re.search('related|newsletter|signup|recommend|author.bio|advert|paywall',c):self.skip=1;return
   if t in self.count:self.count[t]+=1
   if t=='p':self.p=[]
   if t in ('h1','h2','h3','h4'):self.heading=1;self.h=''
 def handle_data(self,s):
  if self.in_title:self.title+=s
  if self.art and not self.skip:
   if self.p is not None:self.p.append(s)
   if self.heading:self.h+=s
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if self.art:
   if self.skip:self.skip-=1;return
   if t=='p' and self.p is not None:
    text=' '.join(''.join(self.p).split());self.p=None
    if text:self.ps.append(text)
   if t in ('h1','h2','h3','h4') and self.heading:
    self.heads.append(' '.join(self.h.split()));self.heading=0
   if t=='article':self.art-=1

def main():
 seen=set();candidates=[]
 for x in map(json.loads,(ROOT/'longform_essay_candidates.jsonl').open()):
  p=urlparse(x['source_url']); host=p.hostname
  if not host or host in seen or p.scheme not in ('http','https'):continue
  seen.add(host);candidates.append(x)
  if len(candidates)>=25:break
 with (ROOT/'longform_public_probes.jsonl').open('w') as out:
  for x in candidates:
   url=x['source_url'];p=urlparse(url);base=p.scheme+'://'+p.netloc;res={**x,'status':'failed','extraction_quality':'not_reviewed'}
   try:
    r=requests.get(base+'/robots.txt',headers=HEAD,timeout=12,allow_redirects=False);res['robots_status']=r.status_code
    if r.status_code!=200:res['status']='robots_unavailable_skipped'
    else:
     rp=RobotFileParser();rp.set_url(base+'/robots.txt');rp.parse(r.text.splitlines());res['robots_crawl_delay']=rp.crawl_delay('*')
     if not rp.can_fetch(HEAD['User-Agent'],url):res['status']='robots_disallowed'
     else:
      r=requests.get(url,headers=HEAD,timeout=18,allow_redirects=False);res['http_status']=r.status_code;res['location']=r.headers.get('Location');res['retrieved_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
      if r.status_code!=200:res['status']='http_non_200_skipped'
      elif re.search(r'"isAccessibleForFree"\s*:\s*(?:false|"false")',r.text,re.I):res['status']='declared_paywalled_skipped'
      else:
       raw=r.content;f=CACHE/(hashlib.sha256(url.encode()).hexdigest()+'.html');f.write_bytes(raw);parser=Extract();parser.feed(r.text)
       ws=[len(WORD.findall(t)) for t in parser.ps];sw=[[len(WORD.findall(y)) for y in SENT.split(t) if y.strip()] for t in parser.ps]
       res.update(status='extracted_unvalidated' if sum(ws)>=100 else 'no_article_body',sha256=hashlib.sha256(raw).hexdigest(),body_prose_words=sum(ws),paragraph_count=len(ws),paragraph_words=ws,sentence_words=[v for y in sw for v in y],paragraph_sentences=list(map(len,sw)),headings=parser.heads,presentation_counts=parser.count,characters_in_words=sum(len(w) for t in parser.ps for w in WORD.findall(t)),quotation_marks=sum(t.count('“')+t.count('"') for t in parser.ps),extraction_notes='Article-element paragraphs excluding headers, asides, menus and class-based related/promotional blocks. Full text, form and paywall completeness require manual confirmation.')
   except Exception as e:res['error']=str(e)[:200]
   out.write(json.dumps(res,ensure_ascii=False)+'\n');out.flush();print(url,res['status'],res.get('body_prose_words',''),flush=True);time.sleep(.5)
if __name__=='__main__':main()
