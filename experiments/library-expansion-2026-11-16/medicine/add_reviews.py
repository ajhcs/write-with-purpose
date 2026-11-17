import requests,json,csv,datetime,xml.etree.ElementTree as ET
from pathlib import Path
p=Path(__file__).parent
path=p/'candidates.json';rows=json.loads(path.read_text());rows=[x for x in rows if x['id'] not in ('medicine-critical_review_of_work-2','medicine-critical_review_of_work-3')]
inv={r['doi'].lower() for r in csv.DictReader(open('experiments/corpus-analysis-2026-11-16/results/document-inventory.csv')) if r['doi']}
items=[('PMC3000396','10.1186/1756-3305-3-112','Webster J','28k (publisher rounds to nearest thousand)','https://link.springer.com/article/10.1186/1756-3305-3-112','Toxoplasmosis of Animals and Humans, second edition'),('PMC2628334','10.1186/1756-3305-2-1','Walker A','9246','https://link.springer.com/article/10.1186/1756-3305-2-1','Ticks: Biology, Disease and Control')]
receipts=[]
for n,(pmc,doi,author,views,publisher,work) in enumerate(items,2):
 r=requests.get('https://www.ebi.ac.uk/europepmc/webservices/rest/search',params={'query':'EXT_ID:'+pmc,'format':'json','resultType':'core'},timeout=45);r.raise_for_status();j=r.json();x=j['resultList']['result'][0];assert x['doi'].lower()==doi and x['authorString']==author+'.' and doi not in inv
 now=datetime.datetime.now(datetime.timezone.utc).isoformat(); receipts.append({'request_url':r.url,'retrieved_utc':now,'response':j});journal=x['journalInfo'];yr=int(x['pubYear']);title=x['title']; url='https://europepmc.org/articles/'+pmc
 rows.append({'id':f'medicine-critical_review_of_work-{n}','field':'medicine_health','form_id':'critical_review_of_work','title':title,'authors':[author],'year':yr,'venue':journal['journal']['title'],'doi':doi,'stable_url':publisher,'volume':journal.get('journalVolume'),'issue':journal.get('issue'),'pages':x.get('pageInfo'),'form_basis':f'Publisher explicitly labels this a Book review; its text evaluates {work}. DOI belongs to this review, not to the reviewed book.','form_status':'publisher_genre_and_text_verified','selection_signal_type':'publisher article accesses','selection_evidence':f'Publisher article page displayed {views} accesses when inspected; access counts are not unique readers or a quality measure.','selection_source_url':publisher,'citation_count':x.get('citedByCount'),'citation_provider':'Europe PMC','citation_snapshot':now,'verification_status':'Europe PMC metadata and publisher article page corroborated; no PubMed PMID located; publisher identifies DOI as review DOI','verification_sources':[url,publisher],'date_notes':f'Publisher gives {"23 November 2010" if n==2 else "5 January 2009"}; Europe PMC supplies year.','copy_status':'No matching DOI in provided document inventory; prior branch derived record exists; library and other holdings unknown','retrieval_locator':f'PMCID {pmc}; DOI {doi}','why_this_example':f'A review of {work}, with evaluative discussion and publisher access evidence.','limitations':'Publisher access metrics are an unnormalized view signal and may include repeated visits. They do not establish writing quality or endorse historical clinical content; full-text coding is pending.','prominence_tier':'publisher_access_evidence'})
for x in rows:
 if x['form_id']=='personal_reflective_essay':
  x['prominence_tier']='verified_relevant_no_prominence_evidence'; x['selection_signal_type']='source genre; no individual prominence evidence';x['selection_evidence'] += '; section membership and citation count do not establish notable or widely read status';x['limitations']+=' Individual prominence is not established.'
# PubMed gives both start and complete Medline pagination; preserve the latter.
root=ET.parse(p/'pubmed-efetch.xml').getroot(); med={a.findtext('.//MedlineCitation/PMID'):a.findtext('.//Article/Pagination/MedlinePgn') for a in root.findall('PubmedArticle')}
for x in rows:
 if x['stable_url'].startswith('https://pubmed.ncbi.nlm.nih.gov/'):
  pmid=x['stable_url'].strip('/').split('/')[-1]
  if med.get(pmid): x['pages']=med[pmid]
path.write_text(json.dumps(rows,indent=2,ensure_ascii=False)); (p/'additional-review-receipts.json').write_text(json.dumps(receipts,indent=2)); cov=json.loads((p/'coverage.json').read_text())
for c in cov:
 if c['form_id']=='critical_review_of_work': c.update(status='three_targets',provided=3,candidate_ids=[f'medicine-critical_review_of_work-{i}' for i in range(1,4)],reason='Three specific work reviews with publisher genre verification; two have publisher access-count evidence; formal prose coding remains pending.')
 if c['form_id']=='personal_reflective_essay': c['reason']='Three source-verified examples; individual prominence has not been demonstrated.'
(p/'coverage.json').write_text(json.dumps(cov,indent=2))
print('total',len(rows),'DOI unique',len({x['doi'] for x in rows}))
