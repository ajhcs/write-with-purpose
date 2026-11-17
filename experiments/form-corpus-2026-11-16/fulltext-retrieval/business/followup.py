#!/usr/bin/env python3
"""Follow up redirects, inspect public HTML, and try alternatives to uncertain PDFs."""
import concurrent.futures as cf, hashlib, html.parser, importlib.util, json, pathlib, re, threading, time, urllib.parse, urllib.robotparser, os
import requests
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base',HERE/'retrieve.py'); b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
prior={x['source_id']:x for x in map(json.loads,(HERE/'first-pass-manifest.jsonl').read_text().splitlines())}
hosts=json.loads((HERE/'host_status.json').read_text())['blocked_or_deferred_hosts']
# Robots redirects are normal protocol, not a rate block. Preserve all other stops.
b.blocked.update({k:v for k,v in hosts.items() if not re.search(r'robots HTTP 30[12378]',v)})
redirect_hosts={k for k,v in hosts.items() if re.search(r'robots HTTP 30[12378]',v)}
# First-pass robots redirects observed before follow-up's host-state checkpoint.
redirect_hosts.update(('doi.org','gateway.webofknowledge.com','www.escholarship.org','hal.science','eprints.lse.ac.uk','eprints.maynoothuniversity.ie','www.hbs.edu','archive.nyu.edu','ageconsearch.umn.edu','disciplinas.stoa.usp.br','strategicdesignthinking.files.wordpress.com','evhippel.files.wordpress.com','asu.pure.elsevier.com','agris.fao.org','harthill.co.uk','opus.bath.ac.uk','lawyernista.files.wordpress.com','thegrcbluebook.com','www.1stream.co.za','ris.utwente.nl','portal.acm.org'))
interval={}; b.CACHE.joinpath('robots').mkdir(exist_ok=True); b.CACHE.joinpath('html').mkdir(exist_ok=True)
def allow(url):
 q=urllib.parse.urlsplit(url); origin=q.scheme+'://'+q.netloc;host=q.netloc.lower()
 if q.scheme not in ('http','https') or not host:return False,'invalid_scheme'
 with b.lock:
  if host in b.robots:return b.robots[host].can_fetch(b.UA,url),'robots_cached'
  if host in b.blocked:return False,'host_deferred'
  try:
   robots_url=origin+'/robots.txt'; robots_hops=[]
   for _ in range(6):
    robot_host=urllib.parse.urlsplit(robots_url).netloc.lower()
    if not gate(robot_host):b.blocked[host]='robots redirect target deferred';return False,'robots_blocked'
    resp=requests.get(robots_url,headers={'User-Agent':b.UA},timeout=(5,12),allow_redirects=False)
    robots_hops.append({'url':robots_url,'status':resp.status_code,'location':resp.headers.get('Location')})
    if not resp.is_redirect:break
    robots_url=urllib.parse.urljoin(robots_url,resp.headers.get('Location',''))
   else:b.blocked[host]='robots redirect limit';return False,'robots_unavailable'
   if resp.status_code in (429,403) or (resp.status_code==503 and resp.headers.get('Retry-After')):
    b.blocked[host]=f'robots HTTP {resp.status_code}; retry-after {resp.headers.get("Retry-After","")}';return False,'robots_blocked'
   if resp.status_code in (404,410): lines=[]
   elif resp.status_code==200:lines=resp.text.splitlines()
   else:b.blocked[host]=f'robots HTTP {resp.status_code}';return False,'robots_unavailable'
   rp=urllib.robotparser.RobotFileParser();rp.parse(lines);b.robots[host]=rp
   delay=rp.crawl_delay(b.UA) or rp.crawl_delay('*') or 0
   rate=rp.request_rate(b.UA) or rp.request_rate('*');rate_interval=(rate.seconds/rate.requests) if rate and rate.requests else 0
   interval[host]=max(.75,delay,rate_interval);b.next_host[host]=time.monotonic()+interval[host]
   name=hashlib.sha256(host.encode()).hexdigest()[:16]+'.json'
   (b.CACHE/'robots'/name).write_text(json.dumps({'host':host,'robots_url':origin+'/robots.txt','final_url':resp.url,'http_status':resp.status_code,'observed_at':b.now(),'redirect_hops':robots_hops,'interval_seconds':interval[host],'content':resp.text if resp.status_code==200 else ''},ensure_ascii=False))
   return rp.can_fetch(b.UA,url),'robots_checked'
  except Exception as e:b.blocked[host]='robots request failed: '+type(e).__name__;return False,'robots_unavailable'
def gate(host):
 with b.lock:
  if host in b.blocked:return False
  t=time.monotonic();wait=max(0,b.next_host.get(host,0)-t);b.next_host[host]=max(t,b.next_host.get(host,0))+interval.get(host,.75)
 if wait:time.sleep(wait)
 with b.lock:return host not in b.blocked
b.allow=allow;b.gate=gate
class Article(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.depth=0;self.in_article=0;self.skip=0;self.p_depth=0;self.cur=[];self.paras=[];self.h1=0;self.h1text=[];self.meta={}
 def handle_starttag(self,t,a):
  t=t.lower();d={str(k).lower():v for k,v in a};self.depth+=1
  if t=='meta':
   k=(d.get('name') or d.get('property') or '').lower()
   if k in ('citation_title','dc.title','citation_doi','dc.identifier','dc.identifier.doi') and d.get('content'):self.meta.setdefault(k,[]).append(d['content'])
  if t=='article' and not self.in_article:self.in_article=self.depth
  if self.in_article and t in ('script','style','nav','aside','footer','form','header'):self.skip+=1
  if t=='p' and self.in_article and not self.skip:self.p_depth=self.depth;self.cur=[]
  if t=='h1' and not self.skip:self.h1=self.depth
  if t in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.depth-=1
 def handle_endtag(self,t):
  t=t.lower()
  if t=='p' and self.p_depth:self.paras.append(' '.join(''.join(self.cur).split()));self.p_depth=0
  if t=='h1' and self.h1:self.h1=0
  if self.in_article and t in ('script','style','nav','aside','footer','form','header') and self.skip:self.skip-=1
  if t=='article' and self.in_article==self.depth:self.in_article=0
  self.depth=max(0,self.depth-1)
 def handle_startendtag(self,t,a):
  self.handle_starttag(t,a)
  if t not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.handle_endtag(t)
 def handle_data(self,d):
  if self.p_depth and not self.skip:self.cur.append(d)
  if self.h1 and not self.skip:self.h1text.append(d)
def html_info(body,row):
 text=body.decode('utf8','replace'); parser=Article()
 try:parser.feed(text)
 except Exception:return None
 paras=[x for x in parser.paras if len(x.split())>=15];wc=sum(len(x.split()) for x in paras)
 if len(paras)<3 or wc<500:return None
 observed_title=' '.join(parser.h1text); titlematch=b.helper.normalize_title(row['title'])==b.helper.normalize_title(observed_title)
 if not titlematch and not observed_title.strip():
  titlematch=any(b.helper.normalize_title(t)==b.helper.normalize_title(row['title']) for t in parser.meta.get('citation_title',[])+parser.meta.get('dc.title',[]))
 doi=b.helper.normalize_identifier(row.get('doi') or '');doi_values=parser.meta.get('citation_doi',[])+parser.meta.get('dc.identifier.doi',[])+parser.meta.get('dc.identifier',[])
 doi_match=bool(doi and any(b.helper.normalize_identifier(d)==doi for d in doi_values))
 # Paywall notices cannot be judged by short preview text alone. Restrict to explicit gating language.
 plaintext=' '.join(paras).lower()
 gated=any(s in plaintext for s in ('subscribe to read the full article','purchase access to this article','sign in to read the full article','purchase this article to continue reading','this article is available to subscribers only','unlock this article'))
 if gated:return None
 if not titlematch:return None
 state='consistent' if doi_match else 'unresolved'
 return {'status':state,'reason':'html_title_and_doi_metadata_agree' if doi_match else 'html_title_agrees_doi_unavailable','text_scope':'HTML heading or title metadata and DOI metadata; article element paragraphs','title_match':'match','doi_match':'match' if doi_match else 'unavailable','article_paragraphs':len(paras),'article_words_approx':wc,'paywall_marker':'none among checked phrases'}
def getmeta():
 out={}
 for path in sorted((b.CACHE/'api').glob('batch_*.json')):
  if path.name.endswith('.trace.json'):continue
  try:
   for x in json.loads(path.read_text()).get('results',[]):out[x['id']]=x
  except Exception:pass
 return out
METADATA=getmeta()
def candidate_list(row,old):
 x=METADATA.get(row['openalex_id'],{});locs=x.get('locations') or [];best=x.get('best_oa_location');locs=([best] if best else [])+locs
 previously={t.get('url') for t in old['attempted_urls'] if t.get('url') and t.get('content_class')!='landing_html_only' and urllib.parse.urlsplit(t.get('url')).netloc.lower() not in redirect_hosts}
 seen=set(previously);result=[]
 def add(u,kind,loc):
  if u and u.startswith(('http://','https://')) and u not in seen:seen.add(u);result.append((u,kind,loc or {}))
 for loc in locs:
  if loc.get('is_oa'):add(loc.get('pdf_url'),'openalex_oa_pdf',loc)
 for loc in locs:
  if loc.get('is_oa'):add(loc.get('landing_page_url'),'openalex_oa_landing',loc)
 doi=(row.get('doi') or '').removeprefix('https://doi.org/')
 if doi.startswith('10.5465/'):add('https://journals.aom.org/doi/'+doi,'publisher_doi_landing',{})
 elif doi.startswith('10.1287/'):add('https://pubsonline.informs.org/doi/'+doi,'publisher_doi_landing',{})
 elif doi.startswith('10.1002/'):add('https://onlinelibrary.wiley.com/doi/'+doi,'publisher_doi_landing',{})
 add(row.get('publisher_or_index_landing_url'),'indexed_landing',{})
 return result,seen
def rank(x):return {'consistent':3,'unresolved':2,'unavailable':1,'conflict':0}.get(x.get('source_identity',{}).get('status'),0)
def inspect(row):
 old=prior[row['openalex_id']]; out=dict(old);out['attempted_urls']=list(old['attempted_urls']); trace=out['attempted_urls']; candidates,seen=candidate_list(row,old)
 old_result={k:old.get(k) for k in ('status','file','bytes','sha256','mimeformat','source_identity','completeness','final_url','version','license','location_source','retrieved_at','page_count')}
 alternatives=[old_result] if old.get('file') else [];best=old_result if old.get('file') else None
 if best and rank(best)==3:out['alternates']=alternatives;out['followup_status']='first-pass PDF identity consistent; no additional version required';return out
 i=0
 while i<len(candidates):
  url,kind,loc=candidates[i];i+=1
  doi=(row.get('doi') or '').removeprefix('https://doi.org/')
  canonical=('journals.aom.org' if doi.startswith('10.5465/') else 'pubsonline.informs.org' if doi.startswith('10.1287/') else 'onlinelibrary.wiley.com' if doi.startswith('10.1002/') else 'www.jstor.org' if doi.startswith('10.2307/') else '')
  has_oa=any(l.get('is_oa') for l in METADATA.get(row['openalex_id'],{}).get('locations',[]))
  if kind=='indexed_landing' and urllib.parse.urlsplit(url).netloc.lower()=='doi.org' and (canonical in b.blocked or (canonical=='www.jstor.org' and 'jstor.org' in b.blocked)) and not has_oa:
   trace.append({'url':url,'kind':kind,'status':'deferred_closed_record_canonical_host_blocked'});continue
  data,final,status=b.request(url,trace,kind)
  if not data:continue
  if data.startswith(b'%PDF-') and len(data)>=10240:
   sha=hashlib.sha256(data).hexdigest();p=b.CACHE/'pdf'/(row['openalex_id'].rsplit('/',1)[-1]+'-'+sha[:16]+'.pdf')
   if not p.exists():p.write_bytes(data)
   first=b.helper.extract_pdf_text(p);author=(row.get('authors') or [''])[0].split()[-1] if row.get('authors') else ''
   identity=b.helper.assess_source_identity({'doi':row.get('doi') or '', 'title':row.get('title') or '', 'first_author':author},first)
   candidate={'status':'pdf_retrieved','file':str(p),'bytes':len(data),'sha256':sha,'mimeformat':'application/pdf','source_identity':identity,'completeness':'unverified; page count recorded; manual inspection required','final_url':final,'version':loc.get('version'),'license':loc.get('license'),'location_source':(loc.get('source') or {}).get('display_name'),'retrieved_at':b.now(),'page_count':b.helper.pdf_page_count(p)}
   alternatives.append(candidate)
   if not best or rank(candidate)>rank(best):best=candidate
   if rank(candidate)==3:break
  elif data.lstrip().lower().startswith((b'<!doctype',b'<html')) or b'<html' in data[:500].lower():
   low=data[:200000].lower()
   if any(s in low for s in (b'captcha',b'challenge-platform',b'cf-chl-',b'please verify you are human')):
    with b.lock:b.blocked[urllib.parse.urlsplit(final).netloc.lower()]='automated access challenge'
    trace[-1]['content_class']='access_challenge';continue
   identity=html_info(data,row)
   if identity:
    sha=hashlib.sha256(data).hexdigest();p=b.CACHE/'html'/(row['openalex_id'].rsplit('/',1)[-1]+'-'+sha[:16]+'.html');p.write_bytes(data)
    cand={'status':'html_body_retrieved','file':str(p),'bytes':len(data),'sha256':sha,'mimeformat':'text/html','source_identity':identity,'completeness':'unverified; substantial public article element; manual inspection required','final_url':final,'version':loc.get('version'),'license':loc.get('license'),'location_source':(loc.get('source') or {}).get('display_name'),'retrieved_at':b.now()};alternatives.append(cand)
    if not best or rank(cand)>rank(best):best=cand
    if rank(cand)==3:break
   parser=b.Meta()
   try:parser.feed(data[:1500000].decode('utf8','replace'))
   except Exception:pass
   trace[-1]['content_class']='landing_html_only' if not identity else 'article_html_candidate'
   for u in parser.pdf[:2]:
    u=urllib.parse.urljoin(final,u)
    if u not in seen:seen.add(u);candidates.append((u,'citation_pdf_url',loc))
  else:trace[-1]['content_class']='not_valid_pdf_or_html'
 if best:out.update(best)
 elif any(t.get('status') in ('host_deferred','robots_blocked','robots_unavailable') for t in trace):out['status']='deferred_host_access_or_rate'
 out['alternates']=alternatives;out['followup_status']='candidate routes checked; see attempted_urls and cached OpenAlex metadata';return out
if __name__=='__main__':
 rows=[json.loads(x) for x in b.IN.read_text().splitlines() if x];done={};checkpoint=HERE/'followup_checkpoint.jsonl'
 if checkpoint.exists():
  for line in checkpoint.read_text().splitlines():
   try:x=json.loads(line);done[x['source_id']]=x
   except Exception:pass
  for result in done.values():
   for entry in result.get('attempted_urls',[]):
    if entry.get('http_status') in (403,429) or entry.get('content_class')=='access_challenge':
     host=urllib.parse.urlsplit(entry.get('url','')).netloc.lower()
     if host:b.blocked[host]='previous run access block or rate limit'
 with checkpoint.open('a') as f,cf.ThreadPoolExecutor(max_workers=4) as pool:
  remaining=[row for row in rows if row['openalex_id'] not in done]
  remaining.sort(key=lambda row:not any(l.get('is_oa') for l in METADATA.get(row['openalex_id'],{}).get('locations',[])))
  futures=[pool.submit(inspect,row) for row in remaining]
  for i,future in enumerate(cf.as_completed(futures),1):
   r=future.result();done[r['source_id']]=r;f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush()
   if i%25==0:
    print('followup',len(done),'pdf',sum(x['status']=='pdf_retrieved' for x in done.values()),'html',sum(x['status']=='html_body_retrieved' for x in done.values()),'consistent',sum(x['source_identity']['status']=='consistent' for x in done.values()),'blocked',len(b.blocked),flush=True);b.write_final(list(done.values()))
 b.write_final([done[r['openalex_id']] for r in rows]);print('followup finished',len(done),flush=True)
