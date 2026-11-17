#!/usr/bin/env python3
"""Discover historical library-lookup leads; no full text or eligibility claims."""
import json, urllib.parse, datetime, pathlib, concurrent.futures as cf
import collect
P=pathlib.Path(__file__).resolve().parent
SOURCES=[('critical_review','S122513169','New York Review of Books'),('conceptual_paper','S110667073','Theory & Psychology'),('conceptual_paper','S46763546','Academy of Management Review')]
DATE=datetime.datetime.now(datetime.timezone.utc).isoformat()
def getsource(spec):
 form,ident,name=spec
 params={'filter':f'primary_location.source.id:{ident},to_publication_date:2014-12-31','sort':'cited_by_count:desc','per-page':'200','select':'id,doi,title,publication_date,authorships,cited_by_count,type,open_access,primary_location'}
 u='https://api.openalex.org/works?'+urllib.parse.urlencode(params)
 try:
  x=json.loads(collect.get(u,30)); out=[]
  for z in x.get('results',[]):
   loc=z.get('primary_location') or {}; oa=z.get('open_access') or {}
   out.append({'form':('critical_review' if z.get('type') == 'book-review' else form),'stage':'historical_candidate_unverified','title':z.get('title'),'authors':[a.get('author',{}).get('display_name') for a in z.get('authorships',[])], 'date':z.get('publication_date'),'doi':z.get('doi'),'openalex_id':z.get('id'),'publisher_url':loc.get('landing_page_url'), 'source_original_type':z.get('type'),'source_name':name,'source_id':'https://openalex.org/'+ident,'selection':'highest OpenAlex citation counts among works indexed to this venue through 2014; source-level editorial inclusion, not verified form eligibility','citation_count':z.get('cited_by_count'),'citation_provider':'OpenAlex','citation_observed_at':DATE,'open_access_flag':oa.get('is_oa'),'oa_status':oa.get('oa_status'),'open_access_url':oa.get('oa_url'),'fulltext_status':'not retrieved; access flag is metadata only','classification_basis':'venue and citation signal only; title and full text require screening'})
  return {'source':name,'source_id':ident,'match_count':x.get('meta',{}).get('count'),'records_returned':len(out),'request':u},out
 except Exception as e: return {'source':name,'source_id':ident,'error':str(e)},[]
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=3) as p: result=list(p.map(getsource,SOURCES))
 (P/'historical-discovery.json').write_text(json.dumps({'timestamp':DATE,'sources':[a for a,b in result]},indent=2))
 (P/'historical-candidates.jsonl').write_text(''.join(json.dumps(z,ensure_ascii=False)+'\n' for a,b in result for z in b))
 print(json.dumps([a for a,b in result],indent=2))
