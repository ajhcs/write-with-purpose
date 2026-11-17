#!/usr/bin/env python3
"""Recheck robots for retained captures after correcting redirect pacing."""
import concurrent.futures as cf,datetime,json,time,urllib.parse
from pathlib import Path
from retrieve import robots,state
D=Path(__file__).resolve().parent; a=[json.loads(s) for s in (D/'checkpoint.jsonl').read_text().splitlines()];hosts_blocked=set();host_delay={};origins={}
for x in a:
 for t in x.get('trace',[]):
  if t.get('action')=='http' and t.get('status')==429:hosts_blocked.add(urllib.parse.urlparse(t['url']).hostname)
  if t.get('action')=='host_circuit':hosts_blocked.add(urllib.parse.urlparse(t['url']).hostname)
  if t.get('action')=='robots':
   z=t['details'];host=urllib.parse.urlparse(z['robots_url']).hostname;host_delay[host]=max(host_delay.get(host,1),z.get('crawl_delay_seconds') or 1)
   if x.get('file'):origins[z['robots_url']]=1
 if x.get('file') and not x.get('trace'):
  u=urllib.parse.urlparse(x['final_url']);origins[u.scheme+'://'+u.netloc+'/robots.txt']=1

def audit(u):
 p=urllib.parse.urlparse(u);host=p.hostname;origin=p.scheme+'://'+p.netloc
 if host in hosts_blocked:return {'robots_url':u,'decision':'prior_host_circuit_deferred'}
 if host_delay.get(host,1)>30:return {'robots_url':u,'decision':'prior_long_crawl_delay_deferred','delay':host_delay[host]}
 s=state(host)
 with s['lock']:
  d=robots(origin,host,s);return {k:v for k,v in d.items() if k!='_parser'}
with (D/'robots-audit.jsonl').open('w') as out,cf.ThreadPoolExecutor(max_workers=16) as pool:
 for i,f in enumerate(cf.as_completed([pool.submit(audit,u) for u in origins]),1):
  try:x=f.result()
  except Exception as e:x={'decision':'audit_error','error':str(e)[:200]}
  out.write(json.dumps(x,ensure_ascii=False)+'\n');out.flush()
  if i%20==0:print(i,'/',len(origins),flush=True)
print('complete',len(origins),flush=True)
