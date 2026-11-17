"""Download independently discovered public copies; preserve first-pass receipts."""
import concurrent.futures
import csv
import fcntl
import json
from pathlib import Path
import time
import retrieve as rt


def one(row,leads):
    directory=rt.CACHE/'records'/rt.key(row)/'web'
    directory.mkdir(parents=True,exist_ok=True)
    out=directory/'result.json'
    old=json.loads(out.read_text())if out.exists()else None
    attempted={a['url']for a in old['attempts']}if old else set()
    urls=list(dict.fromkeys(leads))
    urls=[u for u in urls if not any(h in u for h in ('wikipedia.org','metascienceobservatory','minicod.com','synapsesocial','ycr-index','ouci.dntb'))]
    if old and (old['status']=='downloaded_pdf' or set(urls)<=attempted):return old
    rec=old or {'candidate_key':row['candidate_key'],'doi':row['doi'],'title':row['title'],'field':row['field'],'form':row['form_name'],'started_at_utc':rt.now(),'files':[],'attempts':[],'status':'not_retrieved'}
    deadline=time.monotonic()+140;seen=set(attempted)
    pending=[u for u in urls if u not in attempted]
    pending.sort(key=lambda u: not any(part in u.lower() for part in ('.pdf','/bitstream','/download/','/bitstreams/')))
    for url in pending[:12]:
        if rt.landing(url,row,rec,directory,'web_search_discovery',deadline,seen):
            rec['status']='downloaded_pdf';break
        if time.monotonic()>deadline:break
    if rec['status']!='downloaded_pdf'and rec['files']:rec['status']='candidate_needs_identity_review'
    rec['finished_at_utc']=rt.now();rt.write_json(out,rec)
    return rec


def main():
    guard=(rt.CACHE/'rescue.lock').open('w')
    fcntl.flock(guard,fcntl.LOCK_EX|fcntl.LOCK_NB)
    rows=list(csv.DictReader((rt.REPO/'experiments/library-expansion-2026-11-16/library-pull-list.csv').open()));lookup={r['candidate_key']:r for r in rows}
    leads={}
    for p in sorted((rt.ROOT/'searches').glob('*.json')):
        data=json.loads(p.read_text())
        for entry in data.get('candidates',[]):leads.setdefault(entry['candidate_key'],[]).extend(u['url']if isinstance(u,dict)else u for u in entry['urls'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
        futures={pool.submit(one,lookup[k],urls):k for k,urls in leads.items()if urls}
        for i,f in enumerate(concurrent.futures.as_completed(futures),1):
            try:
                r=f.result();print(json.dumps({'done':i,'total':len(futures),'key':r['candidate_key'],'status':r['status'],'files':len(r['files'])}),flush=True)
            except Exception as e:print(json.dumps({'key':futures[f],'error':str(e)}),flush=True)


if __name__=='__main__':main()
