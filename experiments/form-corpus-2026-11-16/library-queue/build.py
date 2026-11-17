#!/usr/bin/env python3
"""Bounded Europe PMC metadata-only library queue. No full text or credentials."""
import csv,datetime as dt,hashlib,json,re,time
from pathlib import Path
import requests
R=Path(__file__).resolve().parent; P=R.parent
C=Path('/workspace/repos/builderbob/.writing-corpus-cache/library-queue'); C.mkdir(parents=True,exist_ok=True)
API='https://www.ebi.ac.uk/europepmc/webservices/rest/search'
# Scope definitions are discovery predicates, not final full-text document-form labels.
FORMS={
 'systematic_review':('TITLE:"systematic review"','Exact title phrase; may be an overview or a protocol; inspect methods.'),
 'scoping_review':('TITLE:"scoping review"','Exact title phrase; protocol or overview possible.'),
 'narrative_review':('TITLE:"narrative review"','Exact title phrase; article may be a protocol or different review subtype.'),
 'theoretical_framework':('TITLE:"theoretical framework"','Exact title phrase; theory use alone does not establish a conceptual paper.'),
 'methods':('TITLE:"new method"','Exact title phrase; verify the article primarily contributes a method.'),
 'clinical_case_report':('PUB_TYPE:"Case Reports"','Publication type Case Reports; verify substantive case-report body.'),
 'study_protocol':('TITLE:"study protocol"','Exact title phrase; verify prospective protocol rather than retrospective report.'),
 'randomized_empirical':('PUB_TYPE:"Randomized Controlled Trial"','Publication type randomized controlled trial; verify substantive empirical primary report.')}
ERAS={'pre2015':'FIRST_PDATE:[1900-01-01 TO 2014-12-31]', '2015-2019':'FIRST_PDATE:[2015-01-01 TO 2019-12-31]'}
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def norm(v):return re.sub(r'^https?://(?:dx\.)?doi\.org/','',str(v or '').strip().lower())
def iter_records(obj):
 if isinstance(obj,dict):
  if any(k in obj for k in ('doi','DOI','pmcid','pmid')):yield obj
  for v in obj.values():yield from iter_records(v)
 elif isinstance(obj,list):
  for v in obj:yield from iter_records(v)
def existing():
 # Conservative snapshot: exclude identifiers appearing in any preceding corpus record,
 # including candidates as well as extracted XML; record the inspected file list.
 ids=set();files=[]
 for p in P.rglob('*'):
  if not p.is_file() or R in p.parents or p.suffix not in ('.json','.jsonl','.csv'):continue
  try:
   if p.suffix=='.json':objs=list(iter_records(json.loads(p.read_text())))
   elif p.suffix=='.jsonl':objs=[x for line in p.read_text().splitlines() for x in iter_records(json.loads(line))]
   else:objs=list(csv.DictReader(p.open(newline='')))
   for x in objs:
    for k in ('doi','DOI','pmcid','pmid'):
     if x.get(k):ids.add((k.lower(),norm(x[k])))
   files.append(str(p.relative_to(P)))
  except (ValueError,UnicodeDecodeError,OSError):continue
 return ids,files

def hold_reason(form, doi, title):
 title=title.lower()
 if form=='systematic_review' and re.search(r'preferred reporting items|\bprisma(?:-|\b)|\b(?:guidance|guideline|checklist|protocol|statement)\b|elaboration and explanation|explanation and elaboration', title):
  return 'Title contains a reporting/guidance or protocol cue; hold pending form review.'
 explicit={
  '10.1111/epi.12550':'Clinical definition report; indexed Case Reports but not a case report.',
  '10.1164/rccm.167.2.211':'Professional society statement; not a case report.',
  '10.1182/blood-2014-05-552729':'Current-concepts overview; not a case report.',
  '10.1146/annurev.psych.53.100901.135114':'Review on episodic memory; not a clinical case report.',
  '10.1177/0272989x9301300409':'Decision-modelling guide; not a clinical case report.',
  '10.7861/futurehosp.6-2-94':'Healthcare AI overview; not a clinical case report.',
  '10.1038/nrclinonc.2017.148':'Therapy toxicity assessment and management overview; not a clinical case report.',
  '10.1016/j.cmi.2018.07.011':'Systematic review and meta-analysis of case reports, not one clinical case report.',
  '10.1053/j.ajkd.2017.10.026':'Core curriculum update; not a clinical case report.',
  '10.1016/s1474-4422(19)30244-3':'Neurology update; not a clinical case report.',
  '10.1016/s0140-6736(86)90837-8':'Methods paper indexed as randomized trial; not a trial report.',
  '10.1161/01.str.24.1.35':'Stroke classification and definitions for a trial; not a trial outcomes report.',
  '10.1093/aje/152.2.99':'Study Protocol Team is author group; title describes trial findings.',
  '10.1016/j.jaapos.2007.08.014':'Study applies a prior protocol; title describes visual acuity findings.',
  '10.1200/jco.1996.14.8.2274':'Title explicitly reports randomized multicenter trial results.',
  '10.1097/00126334-200008150-00010':'Study Protocol Team is author group; title describes changes in a population.',
  '10.1097/00007435-199807000-00005':'Study Protocol Team is author group; title is about trial feasibility.',
  '10.1002/cyto.a.22855':'Title describes reference values generated with an existing protocol.',
  '10.1016/j.ophtha.2015.09.039':'Title explicitly reports first-year outcomes using an existing protocol.',
  '10.1111/bjh.14523':'Title describes prognostic results for patients treated under an existing protocol.',
  '10.1007/s002040100214':'Pre-validation study using a modified rat study protocol, not a prospective study protocol.',
  '10.1007/s00204-002-0337-7':'Experimental detection using a modified rat study protocol, not a prospective study protocol.'}
 return explicit.get(doi,'')

def main():
 prior,files=existing();rows=[];queries=[];seen=set();ts=now()
 for form,(pred,basis) in FORMS.items():
  for era,dates in ERAS.items():
   q=f'{pred} AND OPEN_ACCESS:N AND {dates} AND LANG:eng NOT PUB_TYPE:"Retracted Publication" NOT TITLE:retracted SORT_CITED:y'
   params={'query':q,'format':'json','resultType':'core','pageSize':100}
   key=f'{form}-{era}'; cache=C/(key+'.json')
   if not cache.exists():
    res=requests.get(API,params=params,timeout=45);res.raise_for_status();cache.write_bytes(res.content)
   raw=cache.read_bytes();data=json.loads(raw); query_ts=dt.datetime.fromtimestamp(cache.stat().st_mtime,dt.timezone.utc).isoformat(); request_url=requests.Request('GET',API,params=params).prepare().url
   hits=data.get('resultList',{}).get('result',[]);chosen=0;filtered={'missing_doi':0,'prior_cohort':0,'duplicate_queue':0,'retraction_metadata':0,'literal_title_mismatch':0}
   for rank,x in enumerate(hits,1):
    phrase=re.search(r'TITLE:"([^"]+)"',pred)
    if phrase and phrase.group(1).lower() not in x.get('title','').lower():filtered['literal_title_mismatch']+=1;continue
    doi=norm(x.get('doi'));pmcid=x.get('pmcid','');pmid=x.get('pmid','');types=x.get('pubTypeList',{}).get('pubType',[])
    if not doi:filtered['missing_doi']+=1;continue
    if any('retract' in t.lower() for t in types) or 'retracted' in x.get('title','').lower():filtered['retraction_metadata']+=1;continue
    if any((k,norm(v)) in prior for k,v in [('doi',doi),('pmcid',pmcid),('pmid',pmid)] if v):filtered['prior_cohort']+=1;continue
    if doi in seen:filtered['duplicate_queue']+=1;continue
    seen.add(doi);chosen+=1
    rows.append({'era':era,'candidate_form':form,'priority':'P1' if era=='pre2015' else 'P2','rank_in_provider_query':rank,'doi':doi,'doi_url':'https://doi.org/'+doi,'title':x.get('title',''),'authors':x.get('authorString',''),'first_publication_date':x.get('firstPublicationDate',''),'publication_year':x.get('pubYear',''),'journal':x.get('journalTitle',''),'source_publication_types':'; '.join(types),'pmid':pmid,'pmcid':pmcid,'provider_oa_flag':x.get('isOpenAccess',''),'provider_in_pmc':x.get('inPMC',''),'provider_in_europe_pmc':x.get('inEPMC',''),'provider_fulltext_link_availability':'; '.join(f"{v.get('site','')}: {v.get('availability','')}" for v in x.get('fullTextUrlList',{}).get('fullTextUrl',[])),'citation_count':x.get('citedByCount'),'citation_provider':'Europe PMC','citation_snapshot_utc':query_ts,'search_query':q,'classification_basis':basis,'selection_signal':'descending Europe PMC cited-by count within exact query and date stratum; no field normalization','retraction_screen':'Search excludes Retracted Publication and title retracted; returned publication types and title checked; subsequent retractions not independently checked','retrieval_status':'metadata only; full text not requested; library availability unknown','license':'not checked; verify at source','measurement_status':'not measured','known_type_conflict':bool(hold_reason(form,doi,x.get('title',''))),'hold_reason':hold_reason(form,doi,x.get('title','')),'library_request_status':'hold: known type conflict' if hold_reason(form,doi,x.get('title','')) else 'candidate: full-text screening pending'})
    if chosen==25:break
   queries.append({'form':form,'era':era,'query':q,'request_url':request_url,'retrieved_at_utc':query_ts,'provider_hit_count':data.get('hitCount'),'returned':len(hits),'selected':chosen,'filtered_before_selection':filtered,'raw_response_sha256':hashlib.sha256(raw).hexdigest()})
   print(key,'hits',data.get('hitCount'),'selected',chosen,'filtered',filtered,flush=True)
 (R/'queue.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 with (R/'queue.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 with (R/'eligible-candidates.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(r for r in rows if not r['known_type_conflict'])
 with (R/'library-first.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(r for r in rows if r['provider_in_pmc']=='N' and not r['known_type_conflict'])
 (R/'receipt.json').write_text(json.dumps({'built_at_utc':ts,'provider':'Europe PMC REST','prior_identifier_files':files,'prior_identifier_count':len(prior),'selection_cap_per_query':25,'query_log':queries,'record_count':len(rows)},indent=2)+'\n')
 # Ten highest cited, date-stratified and per form, directly actionable DOI links.
 lines=['# Library retrieval shortlist','', 'Priority P1 is first-publication date through 2014; P2 is the 2015–2019 supplement. These exclude identified type conflicts and are provider-ranked candidates within each exact query, not validated writing-form exemplars; selection requires full-text review and a current retraction check. The full metadata and exact query are in `queue.csv` and `queue.json`.','']
 for form in FORMS:
  lines += ['## '+form.replace('_',' ').title(),'']
  for era in ERAS:
   subset=[r for r in rows if r['candidate_form']==form and r['era']==era and not r['known_type_conflict']][:10]
   lines += ['### '+era,'']
   if not subset:lines+=['No candidates retained.',''];continue
   for x in subset:lines.append(f"- [{x['title']}]({x['doi_url']}) — {x['authors']}; first publication {x['first_publication_date']}; indexed publication year {x['publication_year']}; Europe PMC cited-by {x['citation_count']} (provider query rank {x['rank_in_provider_query']}).")
   lines.append('')
 (R/'shortlist.md').write_text('\n'.join(lines)+'\n')
 print('TOTAL',len(rows))
if __name__=='__main__':main()
