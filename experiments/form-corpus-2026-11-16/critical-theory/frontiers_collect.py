#!/usr/bin/env python3
"""Discover Frontiers editorially classified conceptual analyses, inspect PMC XML."""
import concurrent.futures as cf, re, json, html, urllib.parse, pathlib, datetime
import collect
P=pathlib.Path(__file__).resolve().parent
INDEX='https://www.frontiersin.org/journals/psychology/sections/theoretical-and-philosophical-psychology/articles?publication-date=01%2F01%2F2007-24%2F09%2F2026&page='
def page(n):
 try:
  s=collect.get(INDEX+str(n),20).decode('utf8','replace')
  # Each card wrapper begins with a stable DOI link and image alt title.
  pattern=r'<a href="(https://www\.frontiersin\.org/journals/psychology/articles/(10\.3389/[^"/]+(?:/[^"/]+)?)/full)"[^>]*class="CardArticle__wrapper"[^>]*>(.*?)<p class="CardArticle__type">([^<]+)</p>'
  results=[]
  for m in re.finditer(pattern,s,re.S):
   typ=m.group(4).strip()
   if typ!='Conceptual Analysis': continue
   title=re.search(r'<img alt="([^"]*)"',m.group(3))
   results.append({'doi':html.unescape(m.group(2)),'title':html.unescape(title.group(1)) if title else '', 'publisher_url':m.group(1),'publisher_type':typ,'index_url':INDEX+str(n),'selection':'Publisher editorial classification in theoretical and philosophical psychology section; not a global ranking'})
  return n,results,None
 except Exception as e:return n,[],str(e)
def lookup(group):
 q=' OR '.join('DOI:"'+r['doi']+'"' for r in group)
 u=collect.BASE+'search?'+urllib.parse.urlencode(dict(query=q,format='json',pageSize=100,resultType='core'))
 try:
  data=json.loads(collect.get(u,35)); return data['resultList']['result'],None
 except Exception as e:return [],str(e)
if __name__=='__main__':
 found=[]; errors={}
 with cf.ThreadPoolExecutor(max_workers=8) as pool:
  for n,rows,error in pool.map(page,range(1,41)):
   found.extend(rows)
   if error:errors[str(n)]=error
   if n%10==0:print('index pages',n,'candidates',len(found),flush=True)
 unique={x['doi']:x for x in found}; found=list(unique.values())
 (P/'frontiers-index.json').write_text(json.dumps({'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages_attempted':40,'page_errors':errors,'candidates':found},ensure_ascii=False,indent=2))
 print('unique candidates',len(found),flush=True)
 groups=[found[i:i+25] for i in range(0,len(found),25)]; metadata=[]; lookerrs=[]
 with cf.ThreadPoolExecutor(max_workers=4) as pool:
  for rows,err in pool.map(lookup,groups):
   metadata.extend(rows)
   if err:lookerrs.append(err)
 index={x['doi'].lower():x for x in found}
 output=[]
 with cf.ThreadPoolExecutor(max_workers=16) as pool:
  futures=[pool.submit(collect.parse,('conceptual_paper',z)) for z in metadata]
  for i,f in enumerate(cf.as_completed(futures),1):
   r=f.result(); r['discovery_source']=index.get(r['doi'].lower(),{}); r['selection']='Frontiers publisher section editorial classification as Conceptual Analysis; citation count is descriptive, not global rank'; output.append(r)
   if i%25==0:
    (P/'frontiers-records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in output))
    print('inspected',i,'measured',sum(x['stage']=='measured_source_label' for x in output),flush=True)
 (P/'frontiers-records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in output))
 (P/'frontiers-lookup.json').write_text(json.dumps({'candidate_count':len(found),'metadata_found':len(metadata),'lookup_errors':lookerrs},indent=2))
