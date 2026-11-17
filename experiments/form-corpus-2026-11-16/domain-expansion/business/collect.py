#!/usr/bin/env python3
"""Historical business metadata: source-specific OpenAlex citation-ranked leads."""
import csv, datetime, json, pathlib, subprocess, urllib.parse, concurrent.futures
P=pathlib.Path(__file__).resolve().parent
OBS=datetime.datetime.now(datetime.timezone.utc).isoformat()
SOURCES=[
 ('Academy of Management Review','S46763546','theoretical/conceptual scholarly journal; individual form unverified','https://journals.aom.org/journal/amr'),
 ('Academy of Management Journal','S117778295','empirical management research journal; individual form unverified','https://www.aom.org/publications/journals/journal/'),
 ('Strategic Management Journal','S102949365','scholarly management research; theory, evidence, reviews, methods and other types','https://sms.onlinelibrary.wiley.com/hub/journal/10970266/homepage/productinformation.html'),
 ('Organization Science','S206124708','scholarly research and conceptual perspectives; individual form unverified','https://pubsonline.informs.org/page/orsc/editorial-statement'),
 ('Management Science','S33323087','scholarly theoretical and empirical management research; individual form unverified','https://pubsonline.informs.org/page/mnsc/editorial-statement'),
 ('Harvard Business Review','S41416626','practitioner-oriented magazine; specific genre and review process unverified','https://hbr.org/')]
SELECT='id,doi,title,publication_date,authorships,cited_by_count,type,open_access,primary_location,biblio'
def fetch(src):
 name,ident,scope,publisher=src
 param={'filter':f'primary_location.source.id:{ident},to_publication_date:2014-12-31','sort':'cited_by_count:desc','per-page':'200','select':SELECT}
 url='https://api.openalex.org/works?'+urllib.parse.urlencode(param)
 cmd=['curl','-fsS','--connect-timeout','5','--max-time','25',url]
 try:
  p=subprocess.run(cmd,capture_output=True,check=True); data=json.loads(p.stdout); result=[]
  for z in data.get('results',[]):
   authors=[a.get('author',{}).get('display_name') for a in z.get('authorships',[]) if a.get('author',{}).get('display_name')]; b=z.get('biblio') or {}; loc=z.get('primary_location') or {}; oa=z.get('open_access') or {}; doi=z.get('doi'); date=z.get('publication_date'); title=z.get('title') or ''; 
   citation=f"{', '.join(authors)}. {title}. {name}. {date or 'n.d.'}"
   if b.get('volume'):citation+=f"; {b['volume']}"
   if b.get('issue'):citation+=f"({b['issue']})"
   if b.get('first_page'):citation+=f": {b['first_page']}"+(f"–{b['last_page']}" if b.get('last_page') else '')
   if doi:citation+=f". {doi}"
   result.append({'stage':'historical_candidate_unverified','openalex_id':z.get('id'),'title':title,'authors':authors,'date':date,'year':date[:4] if date else None,'venue':name,'venue_openalex_id':'https://openalex.org/'+ident,'publisher_scope':scope,'publisher_scope_url':publisher,'source_original_type':z.get('type'),'provisional_form':'unassigned; screen individual work','doi':doi,'publisher_or_index_landing_url':loc.get('landing_page_url'),'volume':b.get('volume'),'issue':b.get('issue'),'first_page':b.get('first_page'),'last_page':b.get('last_page'),'full_citation':citation,'citation_count':z.get('cited_by_count'),'citation_provider':'OpenAlex','citation_observed_at':OBS,'selection':'top 200 indexed to this venue through 2014 by OpenAlex cited_by_count; discovery signal only','is_oa':oa.get('is_oa'),'oa_status':oa.get('oa_status'),'oa_url':oa.get('oa_url'),'fulltext_status':'not requested or inspected','query_url':url})
  return {'venue':name,'source_id':'https://openalex.org/'+ident,'publisher_scope':scope,'publisher_scope_url':publisher,'query_url':url,'match_count':data.get('meta',{}).get('count'),'returned':len(result),'observed_at':OBS},result
 except Exception as e:return {'venue':name,'source_id':'https://openalex.org/'+ident,'query_url':url,'error':str(e),'observed_at':OBS},[]
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e: got=list(e.map(fetch,SOURCES))
 previous=P.parents[1]/'critical-theory'/'historical-candidates.jsonl'
 # Explicit lineage for the independently captured AMR queue, if it exists.
 prior=set()
 if previous.exists():
  for line in previous.read_text().splitlines():
   z=json.loads(line)
   if z.get('source_name')=='Academy of Management Review' and z.get('openalex_id'):prior.add(z['openalex_id'])
 records=[]; seen=set(); duplicates=[]
 for info,rows in got:
  for r in rows:
   r['also_in_prior_amr_queue']=r['openalex_id'] in prior
   key=(r.get('doi') or r.get('openalex_id') or '').lower()
   if key and key in seen: duplicates.append({'duplicate_key':key,'venue':r['venue']}); continue
   seen.add(key); records.append(r)
 (P/'records.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
 fields=['title','authors','date','venue','source_original_type','provisional_form','doi','publisher_or_index_landing_url','volume','issue','first_page','last_page','full_citation','openalex_id','venue_openalex_id','citation_count','citation_provider','citation_observed_at','is_oa','oa_status','oa_url','fulltext_status','selection','also_in_prior_amr_queue','query_url']
 with (P/'records.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader()
  for r in records:
   row=dict(r);row['authors']='; '.join(r['authors']);w.writerow(row)
 report={'generated_at':OBS,'sources':[a for a,b in got],'duplicates_removed':duplicates,'prior_amr_path':str(previous),'prior_amr_distinct_ids':len(prior),'records':len(records),'matched_prior_amr_records':sum(x['also_in_prior_amr_queue'] for x in records)}
 (P/'sources.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
