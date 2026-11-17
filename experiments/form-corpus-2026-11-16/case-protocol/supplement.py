#!/usr/bin/env python3
"""Add separately identified pre-2015 candidates without replacing the original sample."""
import concurrent.futures,json
import collect as c
p=c.ROOT
rows=[json.loads(x) for x in (p/'manifest.jsonl').read_text().splitlines()]
seen={(r['stratum'],r.get('pmcid')) for r in rows if r.get('pmcid')}
info={}
for group,original in list(c.QUERIES.items()):
 q=original.replace(' SORT_CITED:y',' AND FIRST_PDATE:[1900-01-01 TO 2014-12-31] SORT_CITED:y');c.QUERIES[group]=q
 res=c.get(c.BASE+'/search',params={'query':q,'format':'json','pageSize':500,'resultType':'core','cursorMark':'*'})
 if res is None:info[group]={'error':'search failed'};continue
 d=res.json();results=d.get('resultList',{}).get('result',[])
 candidates=[r for r in results if c.candidate(r,group) and (group,r.get('pmcid')) not in seen][:60]
 with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool: add=list(pool.map(c.work,[(group,r) for r in candidates]))
 for r in add:r['included_in_cohort']=False;r['supplement_pre2015']=True
 rows.extend(add); info[group]={'query':q,'hit_count':d.get('hitCount'),'response_sort':d.get('request',{}).get('sort'),'attempts':len(add),'measured':sum(r['retrieval_stage']=='body_measured' for r in add)}
 # Save after each stratum so a stopped run retains evidence.
 (p/'manifest.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows));(p/'supplement-search.json').write_text(json.dumps(info,indent=2)+'\n')
 print(group,info[group],flush=True)
