#!/usr/bin/env python3
"""Conservative OpenAlex-location/full-text retrieval, with robot checks and checkpoints."""
import concurrent.futures as cf, csv, datetime, hashlib, html.parser, importlib.util, json, os, pathlib, re, threading, time, urllib.parse, urllib.robotparser
import requests
ROOT=pathlib.Path('/workspace/repos/builderbob/write-with-purpose')
OUT=ROOT/'experiments/form-corpus-2026-11-16/fulltext-retrieval/business'
IN=ROOT/'experiments/form-corpus-2026-11-16/domain-expansion/business/records.jsonl'
CACHE=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/fulltext/business')
for p in [OUT,CACHE/'api',CACHE/'pdf']:p.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('fetch_oa','/home/builderbob/.agents/skills/fulltext-retrieval/fetch_oa.py'); helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
UA='WritingCorpusResearchBot/1.0 (research discovery; respects robots.txt)'
lock=threading.RLock(); next_host={}; blocked={}; robots={}; local=threading.local()
def session():
 if not hasattr(local,'s'):
  local.s=requests.Session(); local.s.headers.update({'User-Agent':UA,'Accept':'application/pdf,text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.5'})
 return local.s
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def gate(host):
 with lock:
  if host in blocked:return False
  t=time.monotonic(); wait=max(0,next_host.get(host,0)-t);next_host[host]=max(t,next_host.get(host,0))+0.75
 if wait:time.sleep(wait)
 with lock:return host not in blocked
def allow(url):
 q=urllib.parse.urlsplit(url); origin=q.scheme+'://'+q.netloc; host=q.netloc.lower()
 if q.scheme not in ('http','https') or not host:return False,'invalid_scheme'
 # Serialized first fetch avoids a stampede of robots requests.
 with lock:
  if host in robots:return robots[host].can_fetch(UA,url), 'robots_cached'
  if host in blocked:return False,'host_deferred'
  try:
   r=requests.get(origin+'/robots.txt',headers={'User-Agent':UA},timeout=(5,10),allow_redirects=False)
   if r.status_code in (429,403) or (r.status_code==503 and r.headers.get('Retry-After')):
    blocked[host]=f'robots HTTP {r.status_code}; retry-after {r.headers.get("Retry-After","")}';return False,'robots_blocked'
   if r.status_code==404 or r.status_code==410: lines=[]
   elif r.status_code==200: lines=r.text.splitlines()
   else:blocked[host]=f'robots HTTP {r.status_code}';return False,'robots_unavailable'
   rp=urllib.robotparser.RobotFileParser();rp.parse(lines);robots[host]=rp
   next_host[host]=time.monotonic()+0.75
   return rp.can_fetch(UA,url),'robots_checked'
  except Exception as e:
   blocked[host]='robots request failed: '+type(e).__name__;return False,'robots_unavailable'
def request(url, trace, kind, maxbytes=25000000):
 visited=set()
 for _ in range(6):
  if url in visited:return None,None,'redirect_loop'
  visited.add(url); host=urllib.parse.urlsplit(url).netloc.lower(); ok,why=allow(url)
  if not ok:
   trace.append({'url':url,'kind':kind,'status':why});return None,None,why
  if not gate(host):trace.append({'url':url,'kind':kind,'status':'host_deferred'});return None,None,'host_deferred'
  try:
   r=session().get(url,timeout=(6,18),allow_redirects=False,stream=True)
   entry={'url':url,'kind':kind,'http_status':r.status_code,'content_type':r.headers.get('Content-Type',''),'retry_after':r.headers.get('Retry-After'),'location':r.headers.get('Location')};trace.append(entry)
   if r.status_code in (429,403) or (r.status_code==503 and r.headers.get('Retry-After')):
    with lock:blocked[host]=f'HTTP {r.status_code}; retry-after {r.headers.get("Retry-After","")}'
    r.close();return None,url,'host_deferred'
   if r.is_redirect:
    nxt=urllib.parse.urljoin(url,r.headers.get('Location',''));r.close();url=nxt;continue
   if r.status_code!=200:r.close();return None,url,f'http_{r.status_code}'
   length=r.headers.get('Content-Length');
   if length and length.isdigit() and int(length)>maxbytes:r.close();return None,url,'size_limit'
   chunks=[];size=0
   for c in r.iter_content(65536):
    size+=len(c)
    if size>maxbytes:r.close();return None,url,'size_limit'
    chunks.append(c)
   r.close();return b''.join(chunks),url,'ok'
  except Exception as e:
   trace.append({'url':url,'kind':kind,'status':'network_error','error':type(e).__name__});return None,url,'network_error'
 return None,url,'redirect_limit'
class Meta(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.pdf=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs); name=(d.get('name') or d.get('property') or '').lower()
  if tag.lower()=='meta' and name in ('citation_pdf_url','dc.identifier.pdf') and d.get('content'):self.pdf.append(d['content'])

def batch_metadata(rows):
 out={}; batch=50
 for offset in range(0,len(rows),batch):
  group=rows[offset:offset+batch];ids=[r['openalex_id'].rsplit('/',1)[-1] for r in group];path=CACHE/'api'/f'batch_{offset//batch:03}.json'; trace=[]
  url='https://api.openalex.org/works?'+urllib.parse.urlencode({'filter':'openalex_id:'+('|'.join(ids)),'per-page':'50','select':'id,doi,title,locations,best_oa_location,open_access,updated_date,type'})
  if path.exists():
   try:data=json.loads(path.read_text()); print('API cached',offset,flush=True)
   except Exception:data=None
  else:
   raw,final,status=request(url,trace,'openalex_api',12000000);data=None
   if raw:
    try:data=json.loads(raw);path.write_text(json.dumps(data,ensure_ascii=False))
    except Exception:pass
   (CACHE/'api'/f'batch_{offset//batch:03}.trace.json').write_text(json.dumps({'url':url,'trace':trace,'status':status,'observed_at':now()},indent=2))
  for x in (data or {}).get('results',[]):out[x.get('id')]=x
  if offset%200==0:print('API done',offset+len(group),'of',len(rows),'matches',len(out),flush=True)
 return out

def item(row, meta):
 trace=[]; ident=row['openalex_id']; out={'source_id':ident,'domain':'business','title':row['title'],'doi':row['doi'],'authors':row['authors'],'venue':row['venue'],'date':row['date'],'source_original_type':row['source_original_type'],'metadata_source':'OpenAlex location batch','metadata_found':bool(meta),'attempted_urls':trace,'final_url':None,'status':'not_retrieved','file':None,'bytes':None,'sha256':None,'mimeformat':None,'source_identity':{'status':'unavailable','reason':'no_pdf'},'completeness':'not established','version':None,'license':None,'location_source':None,'retrieved_at':None}
 locations=(meta or {}).get('locations') or [];best=(meta or {}).get('best_oa_location')
 if best:locations=[best]+locations
 candidates=[]; seen=set()
 def add(url,kind,loc):
  if url and url not in seen and url.startswith(('https://','http://')):seen.add(url);candidates.append((url,kind,loc or {}))
 # Only OA-identified location PDFs; separately inspect public landing pages for public citation_pdf_url.
 for loc in locations:
  if loc.get('is_oa'):add(loc.get('pdf_url'),'openalex_oa_pdf',loc)
 for loc in locations:
  if loc.get('is_oa'):add(loc.get('landing_page_url'),'openalex_oa_landing',loc)
 add(row.get('publisher_or_index_landing_url'),'indexed_landing',{})
 # Limit per-record work; all discovered candidate URL metadata remains in cached OpenAlex responses.
 candidates=candidates[:8];i=0
 while i<len(candidates):
  url,kind,loc=candidates[i];i+=1
  body,final,status=request(url,trace,kind)
  if not body:continue
  if body.startswith(b'%PDF-') and len(body)>=10240:
   path=CACHE/'pdf'/(ident.rsplit('/',1)[-1]+'.pdf');tmp=path.with_suffix('.part');tmp.write_bytes(body);os.replace(tmp,path)
   extracted=helper.extract_pdf_text(path); author=(row.get('authors') or [''])[0].split()[-1] if row.get('authors') else ''
   assessment=helper.assess_source_identity({'doi':row.get('doi') or '', 'title':row.get('title') or '', 'first_author':author},extracted)
   pages=helper.pdf_page_count(path);out.update({'final_url':final,'status':'pdf_retrieved','file':str(path),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'mimeformat':'application/pdf','source_identity':assessment,'page_count':pages,'completeness':'unverified; page count recorded, manual inspection required','version':loc.get('version'),'license':loc.get('license'),'location_source':(loc.get('source') or {}).get('display_name'),'retrieved_at':now()});return out
  if body.lstrip().startswith((b'<!DOCTYPE',b'<!doctype',b'<html',b'<HTML')) or b'<html' in body[:500].lower():
   low=body[:200000].lower()
   if any(marker in low for marker in (b'captcha',b'challenge-platform',b'cf-chl-',b'please verify you are human')):
    host=urllib.parse.urlsplit(final).netloc.lower()
    with lock:blocked[host]='automated access challenge'
    trace[-1]['content_class']='access_challenge';continue
   parser=Meta()
   try:parser.feed(body[:1500000].decode('utf-8','replace'))
   except Exception:pass
   for u in parser.pdf[:2]:
    u=urllib.parse.urljoin(final,u)
    if u not in seen and len(candidates)<10:seen.add(u);candidates.append((u,'citation_pdf_url',loc))
   trace[-1]['content_class']='landing_html_only'
  else:trace[-1]['content_class']='not_valid_pdf_or_html'
 if not meta:out['status']='metadata_unavailable'
 elif not candidates:out['status']='no_public_candidate'
 elif any(x.get('status') in ('host_deferred','robots_blocked','robots_unavailable') for x in trace):out['status']='deferred_host_access_or_rate'
 elif trace and all(x.get('status') in ('robots_checked','robots_cached') for x in trace):out['status']='robots_disallowed'
 return out

def write_final(rows):
 manifest=OUT/'retrieval_manifest.jsonl'; manifest.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 fields=['source_id','venue','title','doi','status','source_identity','landing_url']
 with (OUT/'manual_needed.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fields);w.writeheader()
  for r in rows:
   if r['status']!='pdf_retrieved' or r['source_identity']['status']!='consistent' or r['completeness']!='verified':
    w.writerow({'source_id':r['source_id'],'venue':r['venue'],'title':r['title'],'doi':r['doi'],'status':r['status'],'source_identity':r['source_identity']['status'],'landing_url':r['attempted_urls'][0]['url'] if r['attempted_urls'] else ''})
 (OUT/'host_status.json').write_text(json.dumps({'observed_at':now(),'blocked_or_deferred_hosts':blocked},indent=2))
if __name__=='__main__':
 rows=[json.loads(x) for x in IN.read_text().splitlines() if x]; print('input',len(rows),flush=True)
 meta=batch_metadata(rows);print('metadata total',len(meta),flush=True)
 completed={}
 checkpoint=OUT/'checkpoint.jsonl'
 if checkpoint.exists():
  for x in checkpoint.read_text().splitlines():
   try:r=json.loads(x);completed[r['source_id']]=r
   except Exception:pass
 print('already completed',len(completed),flush=True)
 with checkpoint.open('a') as f, cf.ThreadPoolExecutor(max_workers=4) as e:
  futures=[e.submit(item,r,meta.get(r['openalex_id'])) for r in rows if r['openalex_id'] not in completed]
  for i,future in enumerate(cf.as_completed(futures),1):
   r=future.result();completed[r['source_id']]=r;f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush()
   if i%25==0:
    values=list(completed.values());print('completed',len(values),'pdfs',sum(x['status']=='pdf_retrieved' for x in values),'identity',sum(x['source_identity']['status']=='consistent' for x in values),'blocked_hosts',len(blocked),flush=True);write_final(values)
 write_final([completed[r['openalex_id']] for r in rows]); print('done',len(completed),flush=True)
