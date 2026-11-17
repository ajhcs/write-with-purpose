#!/usr/bin/env python3
"""Collect methods candidates ranked 501 through 1000 into a separate checkpoint."""
import csv, json, concurrent.futures as cf
import collect
C=collect.C; P=C/'methods-tail.csv'
rows=[]
search=json.loads((C/'methods-search.json').read_text());items=search['resultList']['result'][500:1000]
count=sum(r['status']=='measured' for r in rows)
with cf.ThreadPoolExecutor(max_workers=3) as pool:
 for start in range(0,len(items),25):
  if count>=200:break
  for r in pool.map(collect.work, [('methods',x) for x in items[start:start+25]]):
   if r['status']=='measured':
    if count>=200:r.update(status='excluded',reason='sample quota reached')
    else:count+=1
   rows.append(r)
  fields=sorted(set().union(*(r.keys() for r in rows)))
  with P.open('w',newline='') as f:
   w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
  print('methods',525+start,count,flush=True)
