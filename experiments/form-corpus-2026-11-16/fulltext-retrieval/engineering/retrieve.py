#!/usr/bin/env python3
"""Legitimate OA retrieval, no credentials; restartable snapshots and checkpoints."""
import concurrent.futures,datetime,hashlib,html.parser,importlib.util,json,os,re,subprocess,threading,time,urllib.parse,urllib.robotparser
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/fulltext/engineering')
SRC=Path('/workspace/repos/builderbob/write-with-purpose/experiments/form-corpus-2026-11-16/domain-expansion/engineering/records.jsonl')
CACHE.mkdir(parents=True,exist_ok=True);(CACHE/'metadata').mkdir(exist_ok=True);(CACHE/'pdf').mkdir(exist_ok=True)
sp=importlib.util.spec_from_file_location('fetch_oa','/home/builderbob/.agents/skills/fulltext-retrieval/fetch_oa.py'); skill=importlib.util.module_from_spec(sp);sp.loader.exec_module(skill)
AGENT='WritingCorpusResearch/1.0'; lock=threading.Lock(); save_lock=threading.Lock(); next_time={};robots={};blocked={};host_delay={}; attempts_path=ROOT/'checkpoint.jsonl'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pace(host):
 with lock:
  delay=max(0,next_time.get(host,0)-time.monotonic());next_time[host]=time.monotonic()+delay+host_delay.get(host,0.7)
 if delay:time.sleep(delay)
def raw(url):
 host=urllib.parse.urlsplit(url).netloc.lower()
 if host in blocked:return None,'host deferred after HTTP 429'
 pace(host)
 try:
  r=requests.get(url,headers={'User-Agent':AGENT},timeout=(8,18),allow_redirects=False,stream=True)
  if r.status_code==429:
   with lock:blocked[host]={'retry_after':r.headers.get('Retry-After'),'at':now()}
  return r,None
 except requests.RequestException as e:return None,str(e)
def mayfetch(url):
 parts=urllib.parse.urlsplit(url);host=parts.netloc.lower()
 if parts.scheme not in ('http','https') or not host:return False,'unsupported URL'
 # Serialize first robots load to avoid parallel probes of the same host.
 with lock:known=host in robots
 if not known:
  robots_url=parts.scheme+'://'+host+'/robots.txt';r=None;e=None
  for _ in range(5):
   r,e=raw(robots_url)
   if e or not r:break
   if r.status_code in (301,302,303,307,308) and r.headers.get('Location'):
    robots_url=urllib.parse.urljoin(robots_url,r.headers['Location']);r.close();continue
   break
  parser=urllib.robotparser.RobotFileParser();parser.set_url(robots_url)
  if e or r is None:decision=None
  elif r.status_code==200:
   b=r.raw.read(512000,decode_content=True).decode('utf-8','replace');parser.parse(b.splitlines());decision=parser
  elif r.status_code in (404,410):decision='allow'
  else:decision=None
  if r is not None:r.close()
  with lock:robots[host]=decision
 with lock:decision=robots.get(host)
 if decision=='allow':return True,None
 if decision is None:return False,'robots unavailable or disallowed'
 if not decision.can_fetch(AGENT,url):return False,'robots disallow'
 delay=decision.crawl_delay(AGENT) or 0
 rate=decision.request_rate(AGENT)
 if rate and rate.requests:delay=max(delay,rate.seconds/rate.requests)
 if delay>30:return False,'robots rate requires more than 30 seconds between requests; deferred'
 with lock:host_delay[host]=max(0.7,delay)
 return True,None
def fetch(url):
 trace=[];visited=set()
 for _ in range(6):
  if url in visited:return None,trace,'redirect loop'
  visited.add(url);ok,reason=mayfetch(url)
  if not ok:trace.append({'url':url,'status':'not_requested','reason':reason});return None,trace,reason
  r,err=raw(url)
  if err:trace.append({'url':url,'status':'not_requested','reason':err});return None,trace,err
  trace.append({'url':url,'status':r.status_code,'content_type':r.headers.get('Content-Type'),'retry_after':r.headers.get('Retry-After')})
  if r.status_code in (301,302,303,307,308):
   loc=r.headers.get('Location');r.close()
   if not loc:return None,trace,'redirect missing location'
   url=urllib.parse.urljoin(url,loc);continue
  if r.status_code!=200:r.close();return None,trace,'HTTP '+str(r.status_code)
  try:
   data=b''
   for chunk in r.iter_content(65536):
    data+=chunk
    if len(data)>25000000: r.close();return None,trace,'response exceeded 25 MB limit'
   r.close();return data,trace,None
  except requests.RequestException as e:r.close();return None,trace,str(e)
 return None,trace,'too many redirects'
class Meta(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.pdf=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='meta' and (a.get('name') or '').lower() in ('citation_pdf_url','dc.identifier') and a.get('content','').lower().endswith('.pdf'):self.pdf.append(a['content'])
  if t=='link' and 'pdf' in (a.get('type') or '').lower() and a.get('href'):self.pdf.append(a['href'])
  if t=='a' and re.search(r'\.pdf(?:[?#]|$)',a.get('href',''),re.I):self.pdf.append(a['href'])
def firstpage(p):
 try:
  r=subprocess.run(['medsci-run','pdftotext','-f','1','-l','1',str(p),'-'],capture_output=True,timeout=20);return r.stdout.decode('utf-8','replace') if r.returncode==0 else None
 except Exception:return None
def assess(row,meta):
 rid=row['openalex_id'].rsplit('/',1)[-1];out={'id':rid,'title':row['title'],'doi':row['doi_url'],'metadata_status':'available' if meta else 'unavailable','attempts':[],'result':'library_needed','source_identity':{'status':'unavailable','reason':'no full text'},'file':None,'file_sha256':None,'bytes':None,'version':None,'license':None}
 if not meta:out['attempts'].append({'route':'OpenAlex batch','status':'metadata unavailable'});return out
 locs=meta.get('locations') or [];out['openalex_oa']=meta.get('open_access');out['locations_total']=len(locs);queue=[];seen=set()
 for loc in locs:
  if not loc.get('is_oa'):continue
  for k in ('pdf_url','landing_page_url'):
   u=loc.get(k)
   if u and u not in seen:seen.add(u);queue.append((u,loc.get('version'),loc.get('license'),k))
 if not queue:out['attempts'].append({'route':'OpenAlex locations','status':'no OA location advertised'});return out
 # Bounded fallback per record; retain remaining URLs in metadata cache.
 queue=queue[:5];i=0;pdf_candidates=[]
 while i<len(queue) and i<7:
  url,version,lic,kind=queue[i];i+=1;data,trace,error=fetch(url);out['attempts'].append({'route':kind,'url':url,'trace':trace,'error':error,'version':version,'license':lic})
  if data is None:continue
  if data.startswith(b'%PDF-') and len(data)>=10000:
   digest=hashlib.sha256(data).hexdigest();p=CACHE/'pdf'/f'{rid}-{digest[:12]}.pdf';p.write_bytes(data);ident=skill.assess_source_identity({'title':row['title'],'doi':row['doi_url']},firstpage(p));candidate={'result':'pdf_retrieved','source_identity':ident,'file':str(p),'file_sha256':digest,'bytes':len(data),'version':version,'license':lic,'final_url':trace[-1]['url']};pdf_candidates.append(candidate)
   if ident['status']=='consistent':out.update(candidate);out['pdf_candidates']=pdf_candidates;return out
   continue
  if b'<html' in data[:2000].lower() or b'<!doctype html' in data[:2000].lower():
   out['attempts'][-1]['outcome']='HTML landing page; not counted as full text';p=Meta()
   try:p.feed(data.decode('utf-8','replace'))
   except Exception:continue
   for v in p.pdf[:3]:
    candidate=urllib.parse.urljoin(trace[-1]['url'],v)
    if candidate not in seen:seen.add(candidate);queue.append((candidate,version,lic,'landing_pdf_link'))
  else:out['attempts'][-1]['outcome']='non-PDF response; not counted as full text'
 if pdf_candidates:
  pdf_candidates.sort(key=lambda c: 0 if c['source_identity']['status']=='unresolved' else 1);out.update(pdf_candidates[0]);out['pdf_candidates']=pdf_candidates;return out
 if any('429' in json.dumps(x) for x in out['attempts']):out['result']='deferred_rate_limit'
 return out
def main():
 rows=[json.loads(x) for x in SRC.read_text().splitlines()];existing={}
 if attempts_path.exists():
  for x in attempts_path.read_text().splitlines():
   try:y=json.loads(x);existing[y['id']]=y
   except Exception:pass
 metadata={};metadata_errors=[]
 for batch in range(0,len(rows),50):
  ids=[x['openalex_id'].rsplit('/',1)[-1] for x in rows[batch:batch+50]];cache=CACHE/'metadata'/f'batch-{batch//50:02}.json'
  if cache.exists():payload=json.loads(cache.read_text())
  else:
   params={'filter':'openalex:'+'|'.join(ids),'select':'id,doi,title,locations,open_access,best_oa_location','per-page':50};u=requests.Request('GET','https://api.openalex.org/works',params=params).prepare().url;data,trace,error=fetch(u)
   if data is None:metadata_errors.append({'batch':batch//50,'trace':trace,'error':error});continue
   try:payload=json.loads(data);cache.write_text(json.dumps({'retrieved_utc':now(),'request_url':u,'trace':trace,'payload':payload}))
   except Exception as e:metadata_errors.append({'batch':batch//50,'error':str(e)});continue
  payload=payload.get('payload',payload)
  for item in payload.get('results',[]):metadata[item['id']]=item
  print('metadata',batch//50,'retrieved records',len(metadata),flush=True)
 todo=[r for r in rows if r['openalex_id'].rsplit('/',1)[-1] not in existing]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futures={pool.submit(assess,r,metadata.get(r['openalex_id'])):r for r in todo}
  for n,f in enumerate(concurrent.futures.as_completed(futures),1):
   r=futures[f]
   try:o=f.result()
   except Exception as e:o={'id':r['openalex_id'].rsplit('/',1)[-1],'title':r['title'],'doi':r['doi_url'],'result':'error','error':str(e),'attempts':[],'source_identity':{'status':'unavailable'}}
   with save_lock:
    with attempts_path.open('a') as dest:dest.write(json.dumps(o,ensure_ascii=False)+'\n')
   if n%20==0:print('completed',n,'of',len(todo),'blocked hosts',len(blocked),flush=True)
 (ROOT/'run-state.json').write_text(json.dumps({'ended_utc':now(),'metadata_errors':metadata_errors,'blocked_hosts':blocked,'records':len(rows)},indent=2)+'\n')
 print('done',len(rows),flush=True)
if __name__=='__main__':main()
