"""Additional public artifact attempts; initial failures remain in acquisition.json."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from acquire import acquire, BASE

items = [
 {'id':'echr-main','type':'github_archive','repo':'trusthlt/mining-legal-arguments','branch':'main'},
 {'id':'bawe-data','type':'archive','url':'https://llds.phon.ox.ac.uk/llds/xmlui/bitstream/handle/20.500.14106/2539/2539.zip?sequence=4&isAllowed=y','filename':'2539.zip'},
 {'id':'persuade-train','type':'dataset','url':'https://drive.usercontent.google.com/download?id=13phHyDzIsb0MHyJr6q-B-qIa9P2tM135&export=download&confirm=t','filename':'persuade-training.csv'},
 {'id':'persuade-test','type':'dataset','url':'https://drive.usercontent.google.com/download?id=1K1SIJiG-2zWgMlTzxQeYOcLwOsFaVel1&export=download&confirm=t','filename':'persuade-test.zip'},
 {'id':'erst-paper','type':'codebook-paper','url':'https://aclanthology.org/2025.cl-1.3.pdf','filename':'erst-paper.pdf'},
 {'id':'az-paper','type':'codebook-paper','url':'https://aclanthology.org/E99-1015.pdf','filename':'az-paper.pdf'},
 {'id':'scidtb-paper','type':'codebook-paper','url':'https://aclanthology.org/D18-1388.pdf','filename':'scidtb-paper.pdf'},
 {'id':'wlp-paper','type':'codebook-paper','url':'https://aclanthology.org/N18-2016.pdf','filename':'wlp-paper.pdf'},
 {'id':'microtext-guide','type':'codebook','url':'https://angcl.ling.uni-potsdam.de/pdfs/ArgGuidelinesEnglish.pdf','filename':'ArgGuidelinesEnglish.pdf'},
 {'id':'persuade-paper','type':'codebook-paper','url':'https://zenodo.org/api/records/8221504/files/A%20large-scale%20corpus%20for%20assessing%20written%20argumentation%20preprint.pdf/content','filename':'persuade-preprint.pdf'},
 {'id':'dita-task-guide','type':'codebook','url':'https://docs.oasis-open.org/dita/v1.2/cd03/spec/common/task2.html','filename':'task2.html'},
]
(BASE/'followup-plan.json').write_text(json.dumps({'artifacts':items},indent=2)+'\n')
records=[]
with ThreadPoolExecutor(max_workers=4) as pool:
 for future in as_completed([pool.submit(acquire,item) for item in items]):
  record=future.result()
  path=record.get('local_path')
  if record['id'].startswith('persuade-') and record['type']=='dataset' and path:
   from pathlib import Path
   with Path(path).open('rb') as stream:head=stream.read(1024).lstrip().lower()
   if head.startswith((b'<!doctype',b'<html')):
    record['status']='unavailable';record['error']='Public download returned HTML confirmation/error page, not dataset bytes'
  records.append(record)
  (BASE/'followup-acquisition.json').write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'records':sorted(records,key=lambda r:r['id'])},indent=2)+'\n')
  print(json.dumps({'id':record['id'],'status':record['status'],'bytes':record.get('download',{}).get('bytes'),'error':record.get('error')}),flush=True)
