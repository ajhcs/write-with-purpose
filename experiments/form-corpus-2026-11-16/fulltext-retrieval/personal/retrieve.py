#!/usr/bin/env python3
"""Bounded publisher retrieval; hash bytes, respect robots/rates, checkpoint every record."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from html.parser import HTMLParser
from urllib.parse import urlparse,urljoin
from urllib.robotparser import RobotFileParser
from pathlib import Path
from difflib import SequenceMatcher
import collections, datetime as dt, hashlib, json, re, threading,time,os, requests
try: import pymupdf
except ImportError: pymupdf=None
D=Path(__file__).resolve().parent; ROOT=D.parents[1]; INPUT=ROOT/'domain-expansion/personal/records.jsonl'
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/fulltext/personal');CACHE.mkdir(parents=True,exist_ok=True)
OLD=ROOT/'essays/longform_public_probes.jsonl'; OLD_CACHE=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16/longform')
OUT=D/'checkpoint.jsonl'; USER='WritingCorpusResearch/1.0';HEAD={'User-Agent':USER,'Accept':'text/html,application/pdf;q=0.9,*/*;q=0.1'}
MAX=10*1024*1024;TIMEOUT=(7,14); MAX_DELAY=30
states={}; states_guard=threading.Lock();robots_cache={}; write_lock=threading.Lock()
words=re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*|\d+(?:[.,]\d+)*",re.UNICODE)
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def norm(s):return ' '.join(re.findall(r'[^\W_]+',(s or '').casefold(),re.UNICODE))
def state(host):
 with states_guard:return states.setdefault(host,{'lock':threading.RLock(),'next':0,'delay':1.0,'circuit':None,'failures':0})
def paced(s):
 delay=max(0,s['next']-time.monotonic())
 if delay>MAX_DELAY: return False
 if delay:time.sleep(delay)
 s['next']=time.monotonic()+max(1,s['delay']);return True

def robots(origin,host,s):
 if origin in robots_cache:return robots_cache[origin]
 u=origin+'/robots.txt';rinfo={'robots_url':u,'checked_utc':now()}
 try:
  if not paced(s):rinfo.update(decision='deferred_rate');robots_cache[origin]=rinfo;return rinfo
  redirects=[]; current=u
  for _ in range(5):
   r=requests.get(current,headers=HEAD,timeout=TIMEOUT,allow_redirects=False)
   redirects.append({'url':current,'status':r.status_code,'location':r.headers.get('Location')})
   if r.status_code not in (301,302,303,307,308):break
   target=urljoin(current,r.headers.get('Location',''))
   if not r.headers.get('Location') or urlparse(target).hostname!=host:
    rinfo.update(status=r.status_code,decision='robots_cross_host_redirect_unresolved',redirects=redirects);robots_cache[origin]=rinfo;return rinfo
   if not paced(s):
    rinfo.update(status=r.status_code,decision='deferred_rate',redirects=redirects);robots_cache[origin]=rinfo;return rinfo
   current=target
  rinfo.update(status=r.status_code,final_url=current,sha256=hashlib.sha256(r.content).hexdigest(),redirects=redirects)
  if r.status_code==429:s['circuit']='robots_http_429_retry_after_'+str(r.headers.get('Retry-After'));rinfo['decision']='deferred_429'
  elif r.status_code in (404,410):rinfo['decision']='allowed_no_robots'
  elif r.status_code!=200:rinfo['decision']='robots_unavailable'
  elif 'html' in r.headers.get('Content-Type','').lower() and not re.search(r'(?im)^user-agent\s*:',r.text):rinfo['decision']='robots_unavailable_html'
  elif re.search(r'(?im)^\s*content-signal\s*:.*\bai-input\s*=\s*no\b',r.text):rinfo['decision']='robots_ai_input_disallowed'
  else:
   rp=RobotFileParser();rp.set_url(r.url);rp.parse(r.text.splitlines());rinfo['decision']='check_rules';rinfo['_parser']=rp
   delay=rp.crawl_delay(USER) or rp.crawl_delay('*');rinfo['crawl_delay_seconds']=delay
   if delay:s['delay']=max(s['delay'],float(delay));s['next']=max(s['next'],time.monotonic()+s['delay'])
 except Exception as e:rinfo.update(decision='robots_error',error=str(e)[:250])
 robots_cache[origin]=rinfo;return rinfo

def get_one(url,trace):
 for n in range(7):
  p=urlparse(url)
  if p.scheme not in ('http','https') or not p.hostname:return None,'invalid_url',url
  host=p.hostname.lower();origin=p.scheme+'://'+p.netloc;s=state(host)
  with s['lock']:
   if s['circuit']:trace.append({'url':url,'action':'host_circuit','reason':s['circuit']});return None,'host_circuit',url
   ri=robots(origin,host,s);rd={k:v for k,v in ri.items() if k!='_parser'};trace.append({'url':url,'action':'robots','details':rd})
   if ri['decision'] not in ('allowed_no_robots','check_rules'):return None,ri['decision'],url
   if ri['decision']=='check_rules' and not ri['_parser'].can_fetch(USER,url):return None,'robots_disallowed',url
   if not paced(s):trace.append({'url':url,'action':'deferred','reason':'crawl_delay_exceeds_window','seconds':s['delay']});return None,'crawl_delay_deferred',url
   try:
    r=requests.get(url,headers=HEAD,timeout=TIMEOUT,allow_redirects=False,stream=True)
    trace.append({'url':url,'action':'http','status':r.status_code,'content_type':r.headers.get('Content-Type'),'location':r.headers.get('Location'),'retry_after':r.headers.get('Retry-After'),'at_utc':now()})
    if r.status_code==429:s['circuit']='http_429_retry_after_'+str(r.headers.get('Retry-After'));r.close();return None,'http_429',url
    if 300<=r.status_code<400:
     loc=r.headers.get('Location');r.close()
     if not loc:return None,'redirect_without_location',url
     url=urljoin(url,loc);continue
    if r.status_code!=200:
     if r.status_code>=500:
      s['failures']+=1
      if s['failures']>=3:s['circuit']='repeated_server_errors'
     r.close();return None,'http_'+str(r.status_code),url
    raw=b''
    for chunk in r.iter_content(65536):
     raw+=chunk
     if len(raw)>MAX:r.close();return None,'body_over_10mib',url
    headers=dict(r.headers);r.close();return (raw,headers),None,url
   except Exception as e:
    trace.append({'url':url,'action':'error','error':str(e)[:250]});s['failures']+=1
    if s['failures']>=3:s['circuit']='repeated_network_errors'
    return None,'network_error',url
 return None,'redirect_limit',url

class Article(HTMLParser):
 def __init__(self):super().__init__();self.scope=0;self.skip=0;self.stack=[];self.current=None;self.paras=[];self.meta={};self.title='';self.in_title=False;self.h1=[];self.in_h1=False;self.visible=[]
 def handle_starttag(self,t,a):
  d=dict(a);cl=(d.get('class','')+' '+d.get('id','')).lower()
  if t=='meta':
   k=(d.get('property') or d.get('name') or '').lower()
   if k in ('og:title','twitter:title','author','article:author','citation_author','citation_title','citation_date','description','robots'):self.meta.setdefault(k,[]).append(d.get('content',''))
  if t=='title':self.in_title=True
  if t=='h1':self.in_h1=True
  is_scope=t in ('article','main') or (t=='div' and bool(re.search(r'(^|[ _-])(article-body|article-content|entry-content|post-content|story-body|story-content)([ _-]|$)',cl)))
  self.stack.append((t,is_scope))
  if is_scope:self.scope+=1
  if self.scope:
   if self.skip and t not in ('br','img','meta','link','hr','input','source','wbr'):self.skip+=1
   elif t in ('nav','header','footer','aside','script','style','form','figure','figcaption','table','ul','ol') or re.search('newsletter|related|advert|share-tools|social-share|author-bio|recommend',cl):self.skip=1
   if t=='p' and not self.skip:self.current=[]
 def handle_startendtag(self,t,a):self.handle_starttag(t,a);self.handle_endtag(t)
 def handle_data(self,s):
  if self.in_title:self.title+=s
  if self.in_h1:self.h1.append(s)
  if self.scope and not self.skip:
   if self.current is not None:self.current.append(s)
   if len(self.visible)<10000:self.visible.append(s)
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='h1':self.in_h1=False
  if self.scope and self.skip:self.skip-=1
  elif self.scope and t=='p' and self.current is not None:
   v=' '.join(''.join(self.current).split());self.current=None
   if v:self.paras.append(v)
  # HTML is often malformed, remove matching topmost tracked element.
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:
    removed=self.stack[i:];self.stack=self.stack[:i];self.scope=max(0,self.scope-sum(int(x[1]) for x in removed));break

def identity(expected,observed,author,observed_author,front):
 a=norm(expected);b=norm(observed);ratio=SequenceMatcher(None,a,b).ratio() if a and b else 0
 title='match' if a and (a in b or b in a and len(b)>12 or ratio>=.88) else 'mismatch_or_unavailable'
 surname=norm(author).split()[-1] if norm(author) else ''; authortext=norm(observed_author+' '+front[:2500]);am='match' if surname and surname in authortext.split() else 'unverified'
 return {'observed_title':observed[:250],'title_status':title,'title_similarity':round(ratio,3),'expected_author':author,'observed_author_metadata':observed_author[:250],'author_status':am,'status':'title_author_consistent' if title=='match' and am=='match' else 'unresolved','evidence_scope':'HTML title/h1 and author metadata or early selected article text; no DOI'}

def inspect(raw,headers,row):
 ct=headers.get('Content-Type','').lower();out={}
 if raw.startswith(b'%PDF-') or 'application/pdf' in ct:
  if not raw.startswith(b'%PDF-'):return {'classification':'invalid_pdf_header'}
  if not pymupdf:return {'classification':'pdf_text_unavailable'}
  try:
   doc=pymupdf.open(stream=raw,filetype='pdf');front=doc[0].get_text() if doc.page_count else '';text=' '.join(p.get_text() for p in doc);ident=identity(row['title'],front[:1000],row['author'],'',front)
   return {'classification':'pdf_retrieved_unverified_completeness','page_count':doc.page_count,'text_words':len(words.findall(text)),'source_identity':ident,'frontmatter_hash':hashlib.sha256(front.encode()).hexdigest()}
  except Exception as e:return {'classification':'pdf_parse_error','error':str(e)[:200]}
 if 'html' not in ct and b'<html' not in raw[:1500].lower():return {'classification':'non_html_or_pdf','content_type':ct}
 decoded=raw.decode('utf8','replace');p=Article()
 try:p.feed(decoded)
 except Exception as e:out['parse_error']=str(e)[:180]
 title=(p.meta.get('og:title') or p.meta.get('citation_title') or [' '.join(p.h1) or p.title])[0];author=' '.join((p.meta.get('author') or [])+(p.meta.get('article:author') or [])+(p.meta.get('citation_author') or []));visible=' '.join(p.visible);paras=p.paras;bodywords=sum(len(words.findall(t)) for t in paras)
 is_paywall=bool(re.search(r'"isAccessibleForFree"\s*:\s*(?:false|"false")',decoded,re.I) or re.search(r'\b(subscribe to (?:continue|read)|sign in to (?:continue|read)|subscription (?:is )?required|you need an active subscription|this (?:article|story) is (?:for|available to) subscribers)\b',visible,re.I))
 challenge=bool(re.search(r'just a moment|checking your browser|verify you are human|attention required.{0,30}cloudflare',p.title+' '+visible[:1000],re.I))
 classification='challenge' if challenge else 'declared_paywall' if is_paywall else 'html_body_extracted_unverified_completeness' if bodywords>=100 else 'html_landing_or_short_body'
 out.update(classification=classification,body_prose_words=bodywords,body_paragraphs=len(paras),source_identity=identity(row['title'],title,row['author'],author,visible),body_extraction='p elements in article/main/marked content containers; ads/figures/lists/nav excluded; extraction completeness unverified',metadata={k:v[:3] for k,v in p.meta.items() if k not in ('description',)})
 return out

def process(row):
 url=row.get('target_url');found=found_urls.get(row['title'],{});url=url or found.get('url');rec={'id':row['id'],'title':row['title'],'author':row['author'],'year_display':row.get('year_display'),'edition_status':'source date and original edition not independently confirmed','source_target_url':row.get('target_url'),'attempt_url':url,'discovery_detail':found or None,'attempted_utc':now(),'trace':[],'status':None,'file':None,'sha256':None}
 if not url:rec['status']='missing_article_url';return rec
 # Preserve pre-existing exact-URL cached captures and their original provenance.
 old=old_by_url.get(url)
 if old and old.get('sha256'):
  f=OLD_CACHE/(hashlib.sha256(url.encode()).hexdigest()+'.html')
  if f.exists() and hashlib.sha256(f.read_bytes()).hexdigest()==old['sha256']:
   raw=f.read_bytes();dest=CACHE/(row['id']+'.html');dest.write_bytes(raw);rec.update(status='previous_cache_reused',final_url=url,file=str(dest),sha256=old['sha256'],bytes=len(raw),original_retrieved_utc=old.get('retrieved_utc'),original_capture_source=str(f),capture_note='Previous Guernica request-rate error disclosure applies only to Guernica; this reused capture is an exact URL match.');rec.update(inspect(raw,{'Content-Type':'text/html'},row));return rec
 got,reason,final=get_one(url,rec['trace']);rec['final_url']=final
 if not got:rec['status']=reason;return rec
 raw,headers=got;info=inspect(raw,headers,row);rec.update(info);rec['status']='http_200_'+info['classification'];rec['content_type']=headers.get('Content-Type');rec['bytes']=len(raw)
 if info['classification'] in ('declared_paywall','challenge'):return rec
 ext='.pdf' if raw.startswith(b'%PDF-') else '.html';dest=CACHE/(row['id']+ext);dest.write_bytes(raw);rec['file']=str(dest);rec['sha256']=hashlib.sha256(raw).hexdigest();return rec

found_urls=json.loads((D/'discovered-urls.json').read_text());old_by_url={x['source_url']:x for x in (json.loads(s) for s in OLD.read_text().splitlines()) if x.get('status')=='extracted_unvalidated'}
def main():
 rows=[json.loads(s) for s in INPUT.read_text().splitlines()]; done={}
 if OUT.exists():
  for s in OUT.read_text().splitlines():
   try:r=json.loads(s);done[r['id']]=r
   except (ValueError,KeyError):pass
 todo=[x for x in rows if x['id'] not in done];print('existing',len(done),'remaining',len(todo),flush=True)
 with OUT.open('a') as out,ThreadPoolExecutor(max_workers=24) as pool:
  futures={pool.submit(process,x):x for x in todo}
  for i,f in enumerate(as_completed(futures),1):
   try:r=f.result()
   except Exception as e:r={'id':futures[f]['id'],'title':futures[f]['title'],'author':futures[f]['author'],'status':'internal_error','error':str(e)}
   out.write(json.dumps(r,ensure_ascii=False)+'\n');out.flush()
   if i%20==0:print(i,'/',len(todo),flush=True)
 print('finished',flush=True)
if __name__=='__main__':main()
