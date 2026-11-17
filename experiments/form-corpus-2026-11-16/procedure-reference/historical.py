#!/usr/bin/env python3
"""Small explicit archived-version pilot; do not infer page publication date."""
import concurrent.futures,json
from pathlib import Path
from supplement import run_one
p=Path(__file__).resolve().parent
names=['pyporting','cporting','urllib2','clinic','sorting','logging','webservers']
items=[('procedure',f'https://docs.python.org/3.4/howto/{n}.html','Python 3.4 archived how-to',None) for n in names]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e: rows=list(e.map(run_one,items))
with (p/'procedure-historical-records.jsonl').open('w') as f:
 for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
for r in rows:print(r.get('title'),r.get('accepted'),r.get('error',''))
