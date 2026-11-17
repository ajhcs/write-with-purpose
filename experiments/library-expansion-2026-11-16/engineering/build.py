import json, requests, time, datetime, re, pathlib
p=pathlib.Path(__file__).parent
leads=[json.loads(l) for l in open(p.parent.parent/'form-corpus-2026-11-16/domain-expansion/engineering/records.jsonl')]
# form, lead index, abstract / primary evidence, form rationale
items=[
('narrative_critical_literature_review',0,'https://yetl.yabesh.ir/yetl1/handle/yetl/136487','Reviews metamodel-based design optimization techniques by role and discusses challenges; no systematic search claimed.'),
('narrative_critical_literature_review',209,'https://orbi.umons.ac.be/handle/20.500.12907/20050','Compares existing refactoring research using explicit topical criteria; not claimed to be systematic.'),
('narrative_critical_literature_review',202,'https://ieeexplore.ieee.org/document/5487526','Analysis and survey of mutation-testing research and trends; no systematic review asserted.'),
('empirical_report',214,'https://doi.org/10.1109/TSE.2003.1205177','Uses change management and survey data, with replication in a second organization.'),
('empirical_report',217,'https://doi.org/10.1109/32.988497','Reports a family of empirical studies comparing test case prioritization.'),
('empirical_report',218,'https://ieeexplore.ieee.org/abstract/document/895989/figures','Focus groups and interviews in 26 organizations inform models, followed by case validation.'),
('methods_paper',1,'https://scholarsmine.mst.edu/mec_aereng_facwork/2815/','Presents sequential optimization and reliability assessment method and two engineering applications.'),
('methods_paper',211,'https://ieeexplore.ieee.org/abstract/document/6035728','Describes an automated software repair algorithm and experiments.'),
('theory_conceptual_paper',210,'https://research.utwente.nl/en/publications/the-physics-of-notations-toward-a-scientific-basis-for-constructi','Proposes a theory and principles for cognitive effectiveness of visual notations.')]
extra=[('tutorial','10.1007/s10664-008-9102-8','https://link.springer.com/article/10.1007/s10664-008-9102-8','Introduces case-study methodology with guidelines, checklists and examples; tutorial-like methods article.'),('systematic_review','10.1016/j.infsof.2008.09.009','https://www.sciencedirect.com/science/article/pii/S0950584908001390','Reports a systematic review of systematic reviews using manual searches of 10 journals and four conferences.'),('systematic_review','10.1016/j.infsof.2010.03.006','https://www.sciencedirect.com/science/article/pii/S0950584910000467','Systematic tertiary review extending the earlier manual search of journals and conferences.')]
now=datetime.datetime.now(datetime.timezone.utc).isoformat(); rows=[]; receipts=[]; s=requests.Session(); s.headers.update({'User-Agent':'BuilderBob-library-selection/1.0 (bibliographic verification)'})
for form,i,url,basis in items:
 x=leads[i]; extra.append((form,x['doi_url'].replace('https://doi.org/',''),url,basis))
for form,doi,url,basis in extra:
 try:
  u='https://api.crossref.org/works/'+requests.utils.quote(doi,safe=''); res=s.get(u,timeout=20); receipts.append({'url':u,'retrieved_utc':now,'status':res.status_code,'body':res.json() if res.ok else res.text[:200]})
  if res.status_code in (403,429): print('CROSSREF STOP',res.status_code); break
  res.raise_for_status(); m=res.json()['message']; title=m['title'][0]; authors=[' '.join(filter(None,[a.get('given'),a.get('family')])) for a in m.get('author',[])]; date=m.get('published-print',m.get('issued',{})).get('date-parts',[[None]])[0]; year=date[0]
  oaurl='https://api.openalex.org/works/https://doi.org/'+doi; oa=s.get(oaurl,timeout=20); receipts.append({'url':oaurl,'retrieved_utc':now,'status':oa.status_code,'body':oa.json() if oa.ok else oa.text[:200]}); o=oa.json() if oa.ok else {}; cnt=o.get('cited_by_count')
  source=next((x for x in leads if x.get('doi_url','').lower().endswith(doi.lower())),None)
  if source and re.sub(r'\W','',source['title']).lower()!=re.sub(r'\W','',title).lower(): print('TITLE MISMATCH',doi,source['title'],title);continue
  rows.append(dict(id='eng_'+str(len(rows)+1).zfill(2),field='engineering_computing',form_id=form,title=title,authors=authors,year=year,venue=m.get('container-title',[''])[0],doi=doi,stable_url='https://doi.org/'+doi,volume=m.get('volume'),issue=m.get('issue'),pages=m.get('page'),form_basis=basis,form_status='abstract or source description verified; full-text writing-model assessment pending',selection_signal_type='citation_count' if cnt is not None else 'publisher or field relevance',selection_evidence=('OpenAlex '+str(cnt)+' cited-by works, retrieved '+now+'; citations reflect scholarly attention, not readership.') if cnt is not None else 'Research-methodology relevance; quantitative prominence unavailable.',selection_source_url=oaurl if cnt is not None else url,citation_count=cnt,citation_provider='OpenAlex' if cnt is not None else None,citation_snapshot=now if cnt is not None else None,verification_status='Crossref DOI metadata matched '+('prior lead title' if source else 'primary source title; confirm during parent merge'),verification_sources=[u,url,oaurl],date_notes='Print publication year where provided; online-first may differ.',copy_status='unknown; parent library deduplication required',retrieval_locator='https://doi.org/'+doi,why_this_example=basis,limitations='Abstract or source description assessed; complete text not downloaded or evaluated.'))
  time.sleep(.35)
 except Exception as e: print('ERROR',doi,str(e))
json.dump(rows,open(p/'candidates.json','w'),indent=2,ensure_ascii=False);json.dump(receipts,open(p/'verification-receipts.json','w'),indent=2,ensure_ascii=False)
contract=json.load(open(p.parent/'selection-contract.json')); cov=[]
for f in contract['forms']:
 ids=[x['id'] for x in rows if x['form_id']==f['id']]; n=len(ids); status='three_targets' if n>=3 else ('partial_gap' if n else 'no_verified_targets')
 reason=('Three source-supported examples.' if n>=3 else 'Further targeted search required; this is a search shortfall, not evidence that the form is absent.')
 if f['id']=='case_report': status='not_applicable';reason='Clinical case-report taxonomy does not map automatically to engineering case studies; empirical cases are covered separately.'
 if f['id']=='scoping_review':reason='Systematic mapping studies are related but not silently treated as scoping reviews; exact scoping examples remain unverified.'
 cov.append(dict(form_id=f['id'],status=status,requested=3,provided=n,candidate_ids=ids,reason=reason))
json.dump(cov,open(p/'coverage.json','w'),indent=2,ensure_ascii=False)
print(len(rows),[(x['form_id'],x['provided']) for x in cov])
