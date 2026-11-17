#!/usr/bin/env python3
"""Try public publisher landing-page metadata without authentication or paywall bypass."""
import concurrent.futures,hashlib,json,urllib.parse
from pathlib import Path
import retrieve as m
ROOT=m.ROOT; CACHE=m.CACHE
state=json.loads((ROOT/'run-state.json').read_text());m.blocked.update(state['blocked_hosts'])
rows=[json.loads(x) for x in m.SRC.read_text().splitlines()];prev={r['id']:r for r in map(json.loads,(ROOT/'checkpoint.jsonl').read_text().splitlines())};meta={}
for f in (CACHE/'metadata').glob('*.json'):
 for x in json.loads(f.read_text())['payload']['results']:meta[x['id']]=x
path=ROOT/'fallback-redirect-checkpoint.jsonl';done={}
if path.exists():
 for line in path.read_text().splitlines():
  x=json.loads(line);done[x['id']]=x
def process(row):
 rid=row['openalex_id'].rsplit('/',1)[-1];old=prev[rid];out={'id':rid,'attempts':[],'result':'publisher_fallback_unavailable'}
 if old['result']=='pdf_retrieved':out['result']='already_retrieved';return out
 x=meta.get(row['openalex_id']) or {};locs=x.get('locations') or [];primary=next((l for l in locs if (l.get('source') or {}).get('type')=='journal'),None) or (locs[0] if locs else {});u=primary.get('landing_page_url') or row.get('publisher_landing_url')
 if not u:out['attempts'].append({'status':'no publisher landing URL'});return out
 data,trace,error=m.fetch(u);out['attempts'].append({'url':u,'route':'publisher_landing_public','trace':trace,'error':error})
 if data is None:return out
 queue=[]
 if data.startswith(b'%PDF-'):queue.append((u,data,trace))
 elif b'<html' in data[:2000].lower() or b'<!doctype html' in data[:2000].lower():
  p=m.Meta()
  try:p.feed(data.decode('utf-8','replace'))
  except Exception:pass
  for link in p.pdf[:2]:
   pdf=urllib.parse.urljoin(trace[-1]['url'],link);buf,tr,err=m.fetch(pdf);out['attempts'].append({'url':pdf,'route':'publisher_pdf_link','trace':tr,'error':err})
   if buf and buf.startswith(b'%PDF-'):queue.append((pdf,buf,tr));break
 for u,data,trace in queue:
  if len(data)<10000:continue
  p=CACHE/'pdf'/f'{rid}.pdf';p.write_bytes(data);identity=m.skill.assess_source_identity({'title':row['title'],'doi':row['doi_url']},m.firstpage(p));out.update({'result':'pdf_retrieved','source_identity':identity,'file':str(p),'file_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'version':primary.get('version'),'license':primary.get('license'),'final_url':trace[-1]['url']});return out
 return out
remaining=[r for r in rows if r['openalex_id'].rsplit('/',1)[-1] not in done]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for i,o in enumerate(ex.map(process,remaining),1):
  with path.open('a') as f:f.write(json.dumps(o,ensure_ascii=False)+'\n')
  if i%25==0:print('publisher fallback',i,'of',len(remaining),'blocked',len(m.blocked),flush=True)
state['blocked_hosts']=m.blocked;state['publisher_fallback_finished']=m.now();(ROOT/'run-state.json').write_text(json.dumps(state,indent=2)+'\n')
