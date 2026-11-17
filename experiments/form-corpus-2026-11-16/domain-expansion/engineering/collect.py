#!/usr/bin/env python3
"""Collect bibliographic leads, not article text, using the public OpenAlex API."""
import csv,datetime,json,time
from pathlib import Path
import requests
OUT=Path(__file__).resolve().parent
BASE='https://api.openalex.org/works'
VENUES=[
 ('mechanical engineering','Journal of Mechanical Design','1050-0472'),
 ('mechanical engineering: thermal','Journal of Heat Transfer','0022-1481'),
 ('civil engineering: structures','Journal of Structural Engineering','0733-9445'),
 ('electrical engineering: power systems','IEEE Transactions on Power Systems','0885-8950'),
 ('software engineering','IEEE Transactions on Software Engineering','0098-5589'),
 ('systems engineering','Systems Engineering','1098-1241'),
 ('civil engineering: construction','Journal of Construction Engineering and Management','0733-9364'),
]
SELECT='id,doi,title,publication_date,authorships,primary_location,open_access,cited_by_count,type,biblio'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 records=[];queries=[];seen=set()
 for field,journal,issn in VENUES:
  params={'filter':f'primary_location.source.issn:{issn},from_publication_date:2000-01-01,to_publication_date:2014-12-31,type:article','sort':'cited_by_count:desc','per-page':50,'select':SELECT}
  r=requests.get(BASE,params=params,timeout=50,headers={'User-Agent':'engineering-bibliography-research/1.0'});date=now()
  entry={'field':field,'intended_journal':journal,'issn':issn,'provider':'OpenAlex','request_url':r.url,'retrieved_utc':date,'status':r.status_code}
  if r.status_code!=200:
   entry['error']=r.text[:500];queries.append(entry);continue
  payload=r.json();entry['provider_total_matches']=payload.get('meta',{}).get('count');entry['returned']=len(payload.get('results',[]));queries.append(entry)
  for rank,x in enumerate(payload.get('results',[]),1):
   oid=x.get('id');doi=x.get('doi');title=x.get('title');loc=x.get('primary_location') or {};source=loc.get('source') or {};bib=x.get('biblio') or {};oa=x.get('open_access') or {};authors=[a.get('author',{}).get('display_name') for a in (x.get('authorships') or []) if a.get('author',{}).get('display_name')]; pub=x.get('publication_date') or ''
   if not oid or oid in seen or not title or not doi or not pub[:4].isdigit() or int(pub[:4])>2014:continue
   seen.add(oid)
   citation=f"{', '.join(authors)} ({pub[:4]}). {title}. {source.get('display_name') or journal}"
   if bib.get('volume'):citation+=f", {bib['volume']}"
   if bib.get('issue'):citation+=f"({bib['issue']})"
   if bib.get('first_page'):citation+=f", {bib['first_page']}"+(f"–{bib['last_page']}" if bib.get('last_page') else '')
   citation+=f'. {doi}'
   records.append({'field':field,'candidate_form':'research article; methods / conceptual / empirical unresolved until full-text screening','candidate_form_status':'unreviewed; article type from OpenAlex','title':title,'authors':authors,'publication_date':pub,'year':int(pub[:4]),'venue':source.get('display_name') or journal,'volume':bib.get('volume'),'issue':bib.get('issue'),'first_page':bib.get('first_page'),'last_page':bib.get('last_page'),'doi_url':doi,'openalex_id':oid,'citation':citation,'query_intended_venue':journal,'query_issn':issn,'query_url':r.url,'query_rank':rank,'retrieved_utc':date,'citation_count_provider':'OpenAlex','citation_count_as_of_retrieval':x.get('cited_by_count'),'open_access_status_provider':'OpenAlex','open_access_status':oa.get('oa_status'),'open_access_indicated':oa.get('is_oa'),'open_access_url':oa.get('oa_url'),'publisher_landing_url':loc.get('landing_page_url'),'license':loc.get('license'),'access_verification':'metadata indicator only; full text, access, license, and genre not independently verified','date_verification':'OpenAlex metadata only; historical versions and original publication date not independently verified','duplicate_scope':'deduplicated by OpenAlex ID within this collection only; cross-collection duplication unchecked'})
  print(journal,entry['provider_total_matches'],'returned',entry['returned'],'cumulative unique DOI leads',len(records),flush=True)
 (OUT/'records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
 with (OUT/'records.csv').open('w',newline='') as f:
  fields=list(records[0]) if records else [];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for row in records:w.writerow({k:'; '.join(v) if isinstance(v,list) else v for k,v in row.items()})
 (OUT/'sources.json').write_text(json.dumps({'retrieved_utc':now(),'provider':'OpenAlex public API, no key','queries':queries,'selection':'top 50 article records per named journal, publication years 2000–2014, sorted by OpenAlex cited_by_count descending; exclude records without DOI or date; deduplicate by OpenAlex ID','ieee_sort_reference':'https://ieeexplore.ieee.org/Xplorehelp/searching-ieee-xplore/search-results-page','ieee_reference_note':'Context for IEEE Xplore sorting only; rankings here are OpenAlex, not IEEE Xplore.'},indent=2)+'\n')
 print('done',len(records),flush=True)
if __name__=='__main__':main()
