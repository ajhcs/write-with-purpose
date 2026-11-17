#!/usr/bin/env python3
"""Build dated, auditable literary discovery queue without retrieving article text."""
import collections,csv,datetime,hashlib,json,re,unicodedata
from pathlib import Path
D=Path(__file__).resolve().parent; ROOT=D.parents[1]; E=ROOT/'essays'
def read(p):return [json.loads(s) for s in p.read_text().splitlines() if s]
def norm(s):return re.sub(r'[^\w]+','',unicodedata.normalize('NFKC',s or '').casefold())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=E/'longform_dated_candidates.jsonl';pg=E/'longform_dated_pages.jsonl';sp=D/'atwan-notable-seeds.jsonl'; pages={x['url']:x for x in read(pg) if 'sha256' in x}
rows=[]
for x in read(base):
 if x['historical_stratum']!='pre_2015':continue
 page=pages.get(x['discovery_url'],{})
 rows.append({'id':'LF-'+hashlib.sha256((x['title']+'\0'+x['author']).encode()).hexdigest()[:12],'title':x['title'],'author':x['author'],'outlet':x['publication'],'date_display':x['date_display'],'year_display':x['year_display'],'date_basis':'Longform display; original publication date and edition unverified','target_url':x['source_url'],'target_url_basis':'Longform destination; may be a publisher page, reprint, dead link or another source; original URL not verified','selector':'Longform essay-tag editorial selection; neither popularity nor citation rank','source_record_url':x['longform_record'],'source_page_url':x['discovery_url'],'source_page_sha256':page.get('sha256'),'source_retrieved_utc':page.get('retrieved_utc'),'subject_domain':'unassigned','collection_domain':'personal/literary discovery','form':'unresolved: personal, argument, criticism and reported narrative possible','form_evidence':'Longform essay tag alone is not a personal-essay determination','fulltext_status':'not_retrieved_in_this_expansion','access_status':'unknown; check publisher and library','fulltext_screened':False})
for x in read(sp):
 rows.append({'id':'BAE-'+hashlib.sha256((x['title']+'\0'+x['author']).encode()).hexdigest()[:12],'title':x['title'],'author':x['author'],'outlet':x['outlet'],'date_display':x['date_display'],'year_display':2014,'date_basis':'2014 notables list issue label; publication date not independently established except where noted','target_url':x['original_url'],'target_url_basis':'publisher link individually located where supplied; otherwise missing','selector':'Robert Atwan editorial selection, Notable Essays and Literary Nonfiction of 2014; not an award or popularity ranking','source_record_url':None,'source_page_url':'https://www.hmhco.com/~/media/sites/home/at-home/featured-shops/by-brand/best-american/2015-docs/2015-notables/ba%20essays%202015%20notables.pdf?la=en','source_pdf_page':x['source_page'],'source_pdf_lines':x['source_lines'],'source_page_sha256':None,'source_hash_note':'Publisher PDF inspected via web reader; binary could not be retrieved for hashing','subject_domain':'unassigned unless a subject is explicit in candidate_scope','collection_domain':'personal/literary discovery and form boundary','form':x['candidate_scope'],'form_evidence':'editorial list is not a form determination; no full-text screening','fulltext_status':'not_retrieved_in_this_expansion','access_status':x['access'],'fulltext_screened':False,'date_discrepancy':x.get('date_discrepancy')})
seen={}
for r in rows:
 key=(norm(r['title']),norm(r['author']))
 if key in seen:raise ValueError('duplicate normalized title + author '+str(key))
 seen[key]=1
(D/'records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
cols=['id','title','author','outlet','date_display','year_display','target_url','target_url_basis','selector','source_record_url','source_page_url','source_page_sha256','source_retrieved_utc','subject_domain','collection_domain','form','form_evidence','fulltext_status','access_status','date_discrepancy']
with (D/'records.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)
lf=[x for x in rows if x['id'].startswith('LF-')];authors=collections.Counter(norm(x['author']) for x in lf if x['author']); outlets=collections.Counter(x['outlet'] for x in lf if x['outlet']);countries=collections.Counter(x['year_display'] for x in lf)
manifest={'built_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_files':{str(base):sha(base),str(pg):sha(pg),str(sp):sha(sp)},'longform_records':len(lf),'atwan_seed_records':len(rows)-len(lf),'total_records':len(rows),'distinct_normalized_title_author_pairs':len(seen),'longform_distinct_normalized_author_strings':len(authors),'longform_distinct_outlet_labels':len(outlets),'longform_missing_authors':sum(not x['author'] for x in lf),'longform_top_author_count':max(authors.values()),'longform_outlet_counts':outlets.most_common(),'longform_publication_year_counts':dict(sorted(countries.items())),'records_with_longform_page_hash':sum(bool(x['source_page_sha256']) for x in lf),'fulltext_eligibility_screened':0,'notable_pdf_binary_sha256':None,'notable_pdf_hash_reason':'web reader inspected source PDF; direct binary fetch timed out'}
(D/'audit.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
