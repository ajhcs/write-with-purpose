#!/usr/bin/env python3
"""Bounded, checkpointed, public-location-only legal full-text retrieval."""
import csv,datetime as dt,hashlib,importlib.util,json,re,threading,time,urllib.parse,urllib.robotparser
from concurrent.futures import ThreadPoolExecutor,as_completed
from html.parser import HTMLParser
from pathlib import Path
import requests
R=Path(__file__).resolve().parent;BASE=R.parents[1]/'domain-expansion'/'law';C=Path('/workspace/repos/builderbob/.writing-corpus-cache/fulltext/law'); (C/'files').mkdir(parents=True,exist_ok=True);(C/'api').mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('oa_skill','/home/builderbob/.agents/skills/fulltext-retrieval/fetch_oa.py');skill=importlib.util.module_from_spec(spec);spec.loader.exec_module(skill)
UA='LegalCorpusResearch/1.0 (public academic document retrieval)'; locks={};last={};robot={};host_delay={};stop={'api.crossref.org':'429_previous_run','dash.harvard.edu':'429_previous_run'};meta_lock=threading.Lock();output_lock=threading.Lock()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def norm(s):return re.sub(r'[^a-z0-9]+',' ',(s or '').lower()).strip()
def domain(url):return urllib.parse.urlsplit(url).netloc.lower()
def get_lock(host):
 with meta_lock:return locks.setdefault(host,threading.Lock())
def pace(host):
 delay=host_delay.get(host,.75)-(time.monotonic()-last.get(host,0))
 if delay>0:time.sleep(delay)
 last[host]=time.monotonic()
def permitted(url):
 p=urllib.parse.urlsplit(url);host=p.netloc.lower();root=f'{p.scheme}://{host}/robots.txt'
 with get_lock(host):
  if host in stop:return False,'host_deferred_'+stop[host]
  if host not in robot:
   try:
    pace(host);r=requests.get(root,headers={'User-Agent':UA},timeout=12,allow_redirects=True)
    if r.status_code==429:stop[host]='429';return False,'robots_429'
    if r.status_code in (401,403):stop[host]='robots_access_denied';return False,'robots_'+str(r.status_code)
    if r.status_code==404:robot[host]=None
    elif r.status_code==200:
     rp=urllib.robotparser.RobotFileParser();rp.parse(r.text.splitlines());robot[host]=rp
     delay=rp.crawl_delay(UA) or rp.crawl_delay('*') or 0;rate=rp.request_rate(UA) or rp.request_rate('*');delay=max(.75,float(delay),rate.seconds/rate.requests if rate and rate.requests else 0)
     if delay>5:stop[host]='robots_long_delay';return False,'robots_long_delay'
     host_delay[host]=delay
    else:stop[host]='robots_unavailable';return False,'robots_'+str(r.status_code)
   except requests.RequestException:stop[host]='robots_error';return False,'robots_error'
  return (True,'allowed') if robot[host] is None or robot[host].can_fetch(UA,url) else (False,'robots_disallow')
def fetch(url,trace,limit=30000000):
 for redirect in range(6):
  ok,why=permitted(url)
  if not ok:trace.append({'url':url,'outcome':why});return None
  host=domain(url)
  try:
   with get_lock(host):
    if host in stop:trace.append({'url':url,'outcome':'host_deferred_'+stop[host]});return None
    pace(host);r=requests.get(url,headers={'User-Agent':UA,'Accept':'application/pdf,text/html;q=0.9,application/json;q=0.8,*/*;q=0.3'},timeout=(10,22),allow_redirects=False,stream=True)
    status=r.status_code;entry={'url':url,'http_status':status,'content_type':r.headers.get('Content-Type',''),'outcome':'http'};trace.append(entry)
    if status==429:stop[host]='429';r.close();return None
    if status in (301,302,303,307,308):
     loc=r.headers.get('Location');r.close()
     if not loc:return None
     url=urllib.parse.urljoin(url,loc);continue
    if status!=200:r.close();return None
    parts=[];size=0
    for chunk in r.iter_content(65536):
     size+=len(chunk)
     if size>limit:entry['outcome']='size_limit';r.close();return None
     parts.append(chunk)
    r.close();data=b''.join(parts);entry['bytes']=len(data);return url,data,entry['content_type']
  except requests.RequestException as e:trace.append({'url':url,'outcome':'network_error','error':type(e).__name__});return None
 return None
class Meta(HTMLParser):
 def __init__(self):super().__init__();self.pdf=[];self.title=''
 def handle_starttag(self,t,a):
  a=dict(a);key=(a.get('name') or a.get('property') or '').lower();v=a.get('content','')
  if t=='meta' and v and (key=='citation_pdf_url' or (key in ('dc.identifier','dc.identifier.uri') and v.lower().endswith('.pdf'))):self.pdf.append(v)

def source_candidates(x):
 loc=x.get('locations') or [];best=x.get('best_oa_location');loc=([best] if best else [])+loc;out=[];seen=set()
 for l in loc:
  if not l or not l.get('is_oa'):continue
  for key in ('pdf_url','landing_page_url'):
   u=l.get(key)
   if u and u.startswith(('https://','http://')) and u not in seen:out.append((u,l.get('version'),l.get('license'),(l.get('source') or {}).get('display_name','')));seen.add(u)
 return out[:5]
def identify_file(path,title,doi):
 try:
  import fitz
  doc=fitz.open(str(path));pages=len(doc);text=doc[0].get_text() if pages else '';doc.close()
  result=skill.assess_source_identity({'title':title,'doi':doi or '', 'first_author':''},text)
  return pages,result
 except Exception as e:return None,{'status':'unavailable','reason':type(e).__name__}
def handle(rec):
 rec['attempts']=[];rec['started_utc']=now();rec['status']='not_retrieved';rec['source_identity']={'status':'unavailable','reason':'no_file'}
 if rec.get('held'):rec['status']='held_skipped';return rec
 if rec.get('duplicate_of'):rec['status']='duplicate_link';return rec
 candidates=rec.pop('_locations',[]);files=rec.pop('_prior_files',[])
 # DOI URL supplies public landing evidence only; protected pages/challenges are not bypassed.
 if rec.get('doi'):candidates.append(('https://doi.org/'+rec['doi'],None,None,'DOI landing'))
 seen=set()
 for url,version,license_,source in candidates:
  if url in seen:continue
  seen.add(url);result=fetch(url,rec['attempts'])
  if not result:continue
  final,data,ctype=result
  if data.startswith(b'%PDF-'):
   if len(data)<10000:rec['attempts'][-1]['outcome']='pdf_too_small';continue
   digest=hashlib.sha256(data).hexdigest();path=C/'files'/(rec['id']+'-'+digest[:12]+'.pdf');path.write_bytes(data);pages,ident=identify_file(path,rec['title'],rec.get('doi',''))
   file={'file_path':str(path),'size_bytes':len(data),'sha256':digest,'media_type':'application/pdf','final_url':final,'source':source,'version':version or 'unknown','license':license_ or 'unknown','page_count':pages,'source_identity':ident,'retrieved_utc':now()};files.append(file)
   if ident.get('status')=='consistent':break
   continue
  if b'<html' in data[:2048].lower() or 'text/html' in ctype:
   if rec['id']=='official-heller-brief' and len(data)>25000 and b'CONCLUSION' in data.upper() and b'ARGUMENT' in data.upper():
    digest=hashlib.sha256(data).hexdigest();path=C/'files'/(rec['id']+'-'+digest[:12]+'.html');path.write_bytes(data)
    ident={'status':'unresolved','reason':'html_title_identifier_and_complete_body_not_verified','text_scope':'HTML page'}
    files.append({'file_path':str(path),'size_bytes':len(data),'sha256':digest,'media_type':'text/html','final_url':final,'source':source,'version':version or 'unknown','license':license_ or 'unknown','page_count':None,'source_identity':ident,'retrieved_utc':now()})
   p=Meta()
   try:p.feed(data[:3000000].decode('utf-8','replace'))
   except Exception:continue
   for link in p.pdf[:1]:
    u=urllib.parse.urljoin(final,link)
    if u not in seen:candidates.append((u,version,license_,source+' citation_pdf_url'))
 if files:
  files.sort(key=lambda f:{'consistent':0,'unresolved':1,'unavailable':2,'conflict':3}.get(f['source_identity'].get('status'),4));rec.update(files[0]);rec['candidate_files']=files;rec['status']='file_obtained'
 rec['finished_utc']=now();return rec

def build():
 data={}
 for file in Path('/workspace/tmp/builderbob/writing-corpus/legal-openalex').glob('S*.json'):
  for x in json.loads(file.read_text()).get('results',[]):data[x.get('id')]=x
 orig=list(csv.DictReader((BASE/'records.csv').open()));hein=list(csv.DictReader((BASE/'heinonline-top100.csv').open()));items=[];titlemap={}
 for i,row in enumerate(orig):
  wid=row['openalex_work_id'];x=data.get(wid,{});ident=wid.rsplit('/',1)[-1];doi=row['doi'].replace('https://doi.org/','');held=row['known_or_suspected_conflict']=='True'
  r={'id':ident,'collection':'openalex','title':row['title'],'doi':doi,'authors':row['authors_openalex'],'provider_record':wid,'held':held,'hold_reason':row['hold_reason'],'_locations':source_candidates(x)};items.append(r)
  if not held:titlemap.setdefault(norm(row['title']),[]).append(r)
 for row in hein:
  key=norm(row['title']);matches=titlemap.get(key,[]);held=row['known_or_suspected_conflict']=='True';ident='hein-'+str(row['rank']).zfill(3)
  # Strict exact normalized title only establishes a linkage candidate, not article identity.
  venues={'Harvard Law Review':'harv l rev','The Yale Law Journal':'yale l j','Michigan Law Review':'mich l rev','Stanford Law Review':'stan l rev','Columbia Law Review':'colum l rev','The University of Chicago Law Review':'u chi l rev'}
  surname=norm(row['author_as_printed'].split(';')[0].split(',')[0]); candidates=[m for m in matches if surname and surname in norm(m['authors']) and venues.get(next((z['venue'] for z in orig if z['openalex_work_id'].endswith(m['id'])),''),'!') in norm(row['source_citation'])]
  duplicate=candidates[0]['id'] if len(candidates)==1 and not held else ''
  items.append({'id':ident,'collection':'heinonline','title':row['title'],'doi':'','authors':row['author_as_printed'],'provider_record':row['source_url'],'provider_rank':row['rank'],'source_citation':row['source_citation'],'held':held,'hold_reason':row['hold_reason'],'duplicate_of':duplicate,'_locations':[]})
 for ident,title,url in [
 ('official-brown','Brown v. Board of Education','https://tile.loc.gov/storage-services/service/ll/usrep/usrep347/usrep347483/usrep347483.pdf'),
 ('official-heller-memo','District of Columbia v. Heller','https://www.justice.gov/sites/default/files/dag/legacy/2008/11/10/dag-memo-07032008.pdf'),
 ('official-olc-guidance','Best Practices for OLC Legal Advice and Written Opinions','https://www.justice.gov/sites/default/files/olc/legacy/2010/08/26/olc-legal-advice-opinions.pdf'),
 ('official-heller-brief','District of Columbia v. Heller','https://www.justice.gov/osg/brief/district-columbia-v-heller-amicus-merits')]:
  items.append({'id':ident,'collection':'official_legal_example','title':title,'doi':'','authors':'','provider_record':url,'held':False,'hold_reason':'','_locations':[(url,'official','unknown','official government source')]})
 return items

def resolve_hein(item):
 # Crossref bibliographic search is metadata only; accept title + author + venue/year matching.
 q=urllib.parse.urlencode({'query.bibliographic':item['title']+' '+item['source_citation'],'rows':3});url='https://api.crossref.org/works?'+q;trace=[];result=fetch(url,trace,limit=5000000);item['attempts_pre']=trace
 if result:
  try:
   obj=json.loads(result[1]);cs=obj['message']['items'];target=norm(item['title']);author=norm(item['authors']).split(' ')[0];matches=[]
   for c in cs:
    titles=c.get('title') or [];a=' '.join((z.get('family','') for z in c.get('author',[])));journal=' '.join(c.get('container-title',[]));
    if titles and norm(titles[0])==target and author and author in norm(a):matches.append(c)
   if len(matches)==1:
    z=matches[0];item['doi']=z.get('DOI','');item['crossref_match']='exact normalized title and author; venue not independently confirmed';item['crossref_source']=result[0]
   else:item['crossref_match']='no unique title/author match';item['crossref_source']=result[0]
  except (ValueError,KeyError,TypeError):item['crossref_match']='metadata_parse_failed'
 else:item['crossref_match']='metadata_unavailable'
 return item

def run():
 items=build(); done={}
 checkpoint=R/'checkpoint.jsonl'
 if checkpoint.exists():
  for line in checkpoint.read_text().splitlines():
   try:x=json.loads(line);done[x['id']]=x
   except (ValueError,KeyError):pass
 previous={k:v for k,v in done.items() if (v.get('status')=='not_retrieved' and any(a.get('outcome') in ('host_deferred_robots_unavailable','robots_301') for a in v.get('attempts',[]))) or (v.get('status')=='duplicate_link' and k.startswith('hein-')) or (v.get('status')=='file_obtained' and v.get('source_identity',{}).get('status')!='consistent')}
 for k in previous:del done[k]
 todo=[x for x in items if x['id'] not in done];print('total',len(items),'cached',len(done),'todo',len(todo),flush=True)
 def one(x):
  old=previous.get(x['id'],{})
  if old.get('status')=='file_obtained':
   keys=('file_path','size_bytes','sha256','media_type','final_url','source','version','license','page_count','source_identity','retrieved_utc');x['_prior_files']=old.get('candidate_files') or [{k:old[k] for k in keys if k in old}]
  if x['collection']=='heinonline' and not x['held'] and not x['duplicate_of']:
   old=previous.get(x['id'],{});x['doi']=old.get('doi','');x['crossref_match']=old.get('crossref_match','')
   if not x['doi']:x=resolve_hein(x)
  pre=x.pop('attempts_pre',[]);z=handle(x);z['attempts']=previous.get(x['id'],{}).get('attempts',[])+pre+z['attempts'];return z
 with ThreadPoolExecutor(max_workers=4) as pool:
  futures=[pool.submit(one,x) for x in todo]
  for f in as_completed(futures):
   try:r=f.result()
   except Exception as e:print('WORKER ERROR',type(e).__name__,str(e),flush=True);continue
   with output_lock:
    with checkpoint.open('a') as out:out.write(json.dumps(r,ensure_ascii=False)+'\n')
    done[r['id']]=r
    if len(done)%25==0:print('completed',len(done),'file_obtained',sum(z['status']=='file_obtained' for z in done.values()),flush=True)
 result=[done[x['id']] for x in items if x['id'] in done];(R/'manifest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 (R/'manual_needed.txt').write_text('\n'.join(f"{x['id']} | {x['status']} | {x['title']} | {x.get('doi','')}" for x in result if x['status']=='not_retrieved' or x['status']=='file_obtained' and x['source_identity']['status']!='consistent')+'\n')
 print('done',len(result),'stopped_hosts',stop,flush=True)
if __name__=='__main__':run()
