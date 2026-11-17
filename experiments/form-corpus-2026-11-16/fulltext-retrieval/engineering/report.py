#!/usr/bin/env python3
"""Build inspectable inventory from checkpoint files; does not access the network."""
import collections,csv,datetime,hashlib,json,subprocess
from pathlib import Path
import retrieve as m
P=m.ROOT
rows=[json.loads(x) for x in m.SRC.read_text().splitlines()]
def read(n):
 p=P/n
 return {r['id']:r for r in map(json.loads,p.read_text().splitlines())} if p.exists() else {}
a=read('checkpoint.jsonl');old=read('fallback-checkpoint.jsonl');b=read('fallback-redirect-checkpoint.jsonl');alt=collections.defaultdict(list)
alt_file=P/'alternative-checkpoint.jsonl'
if alt_file.exists():
 for line in alt_file.read_text().splitlines():
  item=json.loads(line);alt[item['id']].append(item)
out=[]
for row in rows:
 rid=row['openalex_id'].rsplit('/',1)[-1];x=a.get(rid,{'id':rid,'result':'not_attempted','attempts':[],'source_identity':{'status':'unavailable'}}).copy();retry=b.get(rid);x['prior_publisher_attempt']=old.get(rid);x['publisher_fallback']=retry or {'result':'not_yet_attempted','attempts':[]};x['source_article_indexed_year']=row['year'];x['source_indexed_year_caveat']='indexed date; actual first publication and PDF version need verification'
 if retry and retry.get('result')=='pdf_retrieved':
  for key in ['result','source_identity','file','file_sha256','bytes','version','license','final_url']:x[key]=retry.get(key)
 x['alternative_reviews']=alt.get(rid,[])
 for candidate in x['alternative_reviews']:
  if candidate.get('result')=='pdf_retrieved' and candidate.get('source_identity',{}).get('status')=='consistent':
   x['original_candidate']={k:x.get(k) for k in ['file','file_sha256','source_identity','version','license']}
   for key in ['result','source_identity','file','file_sha256','bytes','version','license','final_url']:x[key]=candidate.get(key)
  if candidate.get('result')=='html_retrieved' and x.get('result')!='pdf_retrieved':
   for key in ['result','source_identity','file','file_sha256','bytes','version','license']:x[key]=candidate.get(key)
 if x.get('result')=='pdf_retrieved':
  path=Path(x['file']);data=path.read_bytes();x['hash_verified']=hashlib.sha256(data).hexdigest()==x['file_sha256']
  try:
   r=subprocess.run(['medsci-run','pdfinfo',str(path)],capture_output=True,text=True,timeout=20);pages=next((z.split(':',1)[1].strip() for z in r.stdout.splitlines() if z.startswith('Pages:')),None);x['pdfinfo_status']=r.returncode;x['pdf_pages']=int(pages) if pages and pages.isdigit() else None
  except Exception:x['pdfinfo_status']='failed';x['pdf_pages']=None
  x['fulltext_completeness']='unverified; PDF signature, page count and first-page identity do not establish completeness'
 out.append(x)
(P/'manifest.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out))
manual=[x for x in out if x.get('result') not in ('pdf_retrieved','html_retrieved') or x.get('source_identity',{}).get('status') not in ('consistent','html_title_and_doi_consistent')]
with (P/'manual_needed.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','title','doi','result','first_pass','publisher_fallback']);w.writeheader()
 for x in manual:w.writerow({'id':x['id'],'title':x.get('title'),'doi':x.get('doi'),'result':x['result'],'first_pass':x['result'],'publisher_fallback':x['publisher_fallback']['result']})
counts=collections.Counter(x['result'] for x in out);ids=collections.Counter(x.get('source_identity',{}).get('status','unavailable') for x in out if x['result']=='pdf_retrieved'); fallback=collections.Counter(x['publisher_fallback']['result'] for x in out);snapshot={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':len(out),'results':dict(counts),'pdf_identity':dict(ids),'manual_needed_or_identity_review':len(manual),'no_public_fulltext_retrieved':sum(x.get('result') not in ('pdf_retrieved','html_retrieved') for x in out),'publisher_fallback':dict(fallback),'blocked_hosts':json.loads((P/'run-state.json').read_text()).get('blocked_hosts',{}),'metadata_cache':str(m.CACHE/'metadata'),'pdf_cache':str(m.CACHE/'pdf')};(P/'counts.json').write_text(json.dumps(snapshot,indent=2)+'\n');print(json.dumps(snapshot,indent=2))
