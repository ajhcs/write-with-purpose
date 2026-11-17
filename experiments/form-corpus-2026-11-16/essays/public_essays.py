#!/usr/bin/env python3
"""Author-selected original essay archive; local HTML parser, no prose exported."""
from html.parser import HTMLParser
from urllib.parse import urljoin
from pathlib import Path
import concurrent.futures as cf, datetime as dt, hashlib, json, re, threading,time,requests
from acquire_measure import WORD,SENT
ROOT=Path(__file__).resolve().parent
CACHE=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16/paulgraham');CACHE.mkdir(parents=True,exist_ok=True)
INDEX='https://paulgraham.com/articles.html'; HEAD={'User-Agent':'WritingFormResearch/1.0'}; lock=threading.Lock(); next_req=0

def get(url):
 global next_req
 with lock:
  time.sleep(max(0,next_req-time.monotonic()));next_req=time.monotonic()+0.7
 r=requests.get(url,headers=HEAD,timeout=25);r.raise_for_status();return r
class Index(HTMLParser):
 def __init__(self):super().__init__();self.href=None;self.words=[];self.links=[]
 def handle_starttag(self,t,a):
  if t=='a':self.href=dict(a).get('href');self.words=[]
 def handle_data(self,s):
  if self.href:self.words.append(s)
 def handle_endtag(self,t):
  if t=='a' and self.href:
   title=' '.join(''.join(self.words).split()); h=self.href
   if title and re.fullmatch(r'[a-zA-Z0-9_-]+\.html',h):self.links.append((title,urljoin(INDEX,h)))
   self.href=None
class Page(HTMLParser):
 def __init__(self):super().__init__();self.depth=0;self.buff=[];self.blocks=[];self.skip=0
 def handle_starttag(self,t,a):
  attrs=dict(a)
  if t=='font':
   if self.depth:self.depth+=1
   elif attrs.get('face','').lower()=='verdana':self.depth=1;self.buff=[]
  if self.depth and t=='br':self.buff.append('\n')
  if self.depth and t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style') and self.skip:self.skip-=1
  if t=='font' and self.depth:
   self.depth-=1
   if not self.depth:self.blocks.append(''.join(self.buff))
 def handle_data(self,s):
  if self.depth and not self.skip:self.buff.append(s)

def run(x):
 rank,title,url=x;p=CACHE/(url.rsplit('/',1)[-1]);res={'archive_rank':rank,'title':title,'author':'Paul Graham','source_url':url,'selection':'author essay index; archive order, not a popularity or citation ranking','form_candidate':'argument_perspective_or_reflection','eligibility':'not_manually_screened'}
 try:
  if p.exists():raw=p.read_bytes()
  else:raw=get(url).content;p.write_bytes(raw)
  parser=Page()
  try: decoded=raw.decode('utf-8')
  except UnicodeDecodeError: decoded=raw.decode('windows-1252',errors='replace')
  parser.feed(decoded);body=max(parser.blocks,key=len,default='')
  # Date is not prose. References/acknowledgments after a standalone Notes heading are excluded.
  pars=[' '.join(v.split()) for v in re.split(r'\n\s*\n+',body) if v.strip()]
  date=None
  for i,t in enumerate(pars[:5]):
   if re.match(r'^(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',t,re.I):
    date=t; pars=pars[i+1:]; break
  for i,t in enumerate(pars):
   if re.match(r'^(?:Notes?|Acknowledg(?:e)?ments?)(?:\s|:|$)|^Thanks to\b|^Related:',t,re.I):pars=pars[:i];break
  ws=[len(WORD.findall(t)) for t in pars]; ss=[[len(WORD.findall(s)) for s in SENT.split(t) if s.strip()] for t in pars]
  res.update(retrieved_utc=dt.datetime.fromtimestamp(p.stat().st_mtime,dt.timezone.utc).isoformat(),sha256=hashlib.sha256(raw).hexdigest(),date_label=date,publication_year=int(re.search(r'\d{4}',date).group()) if date else None,extraction_status='measured' if sum(ws)>=100 else 'too_little_extracted_text',body_prose_words=sum(ws),paragraph_count=len(ws),paragraph_words=ws,paragraph_sentences=list(map(len,ss)),sentence_words=[v for a in ss for v in a],characters_in_words=sum(len(w) for t in pars for w in WORD.findall(t)),first_person_tokens=sum(w.casefold() in {'i','me','my','mine','myself','we','our','us','ours','ourselves'} for t in pars for w in WORD.findall(t)),quotation_marks=sum(t.count('“')+t.count('"') for t in pars),extraction_notes='Longest Verdana font block; double breaks define paragraphs, leading promotional text and date when identifiable, and Notes onward, excluded; approximate HTML extraction, body completeness and form unscreened.')
 except Exception as e:res.update(extraction_status='failed',error=str(e)[:250])
 return res

def main():
 r=get(INDEX); idx=Index();idx.feed(r.text); seen=set(); links=[]
 for title,url in idx.links:
  if url not in seen and url not in {INDEX,'https://paulgraham.com/index.html'}:seen.add(url);links.append((len(links)+1,title,url))
 (ROOT/'public_archive_discovery.json').write_text(json.dumps({'source':INDEX,'retrieved_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'sha256':hashlib.sha256(r.content).hexdigest(),'distinct_title_links':len(links),'selection':'first 225 distinct links in archive order; the archive is author-selected, not a popularity ranking','selected':min(225,len(links))},indent=2)+'\n')
 with (ROOT/'public_archive_candidates.jsonl').open('w') as out:
  for rank,title,url in links:out.write(json.dumps({'rank':rank,'title':title,'url':url},ensure_ascii=False)+'\n')
 with (ROOT/'public_archive_measurements.jsonl').open('w') as out,cf.ThreadPoolExecutor(max_workers=4) as pool:
  for i,f in enumerate(cf.as_completed([pool.submit(run,x) for x in links[:225]]),1):
   out.write(json.dumps(f.result(),ensure_ascii=False)+'\n');out.flush()
   if i%25==0:print(f'{i} complete',flush=True)
if __name__=='__main__':main()
