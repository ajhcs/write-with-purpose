"""Apply declared type check to cached source and refresh flat view, without re-fetching."""
import csv, hashlib, json, re
from pathlib import Path
H=Path(__file__).resolve().parent; C=Path('/workspace/tmp/builderbob/writing-corpus/explanation-tutorial')
records=[json.loads(x) for x in (H/'records.jsonl').read_text().splitlines()]
for r in records:
 if 'raw_url' not in r: continue
 sections=r['metrics']['sections']; total=sum(x['prose_words'] for x in sections)
 for x in sections: x['prose_share']=round(x['prose_words']/total,4) if total else None
 if r['repo']=='kubernetes/website':
  body=(C/hashlib.sha256(r['raw_url'].encode()).hexdigest()).read_text()
  m=re.search(r'^content_type:\s*(\S+)',body,re.M); declared=m.group(1) if m else None
  expected='concept' if r['proposed_form']=='explanation' else 'tutorial'
  r['original_type']=declared or ('directory: concepts' if r['proposed_form']=='explanation' else 'directory: tutorial')
  if declared and declared!=expected: r['screening_status']='excluded_conflicting_declared_type'
 else: r['original_type']='directory: '+r['proposed_form']
with (H/'records.jsonl').open('w') as f:
 for r in records:f.write(json.dumps(r,ensure_ascii=False)+'\n')
with (H/'measurements.csv').open() as f: cols=next(csv.reader(f))
with (H/'measurements.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader()
 for r in records:w.writerow({**r,**r.get('metrics',{})})
