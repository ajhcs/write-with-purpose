import requests,json,re,time,os
from datetime import date
P='experiments/library-expansion-2026-11-16/law/'
rows=[
('argument_perspective','W46302826','Uses legal history and doctrinal analysis to argue that whiteness operates as property.'),
('argument_perspective','W143173597','Argument interpreting Brown through interest convergence; a legal perspective, not a clinical case report.'),
('argument_perspective','W2989863638','Jurisprudential lecture advances a position on law and morality.'),
('theory_conceptual_paper','W3023063752','Develops a framework of property rules, liability rules, and inalienability.'),
('theory_conceptual_paper','W2166987116','Develops the anticommons concept using property institutions.'),
('theory_conceptual_paper','W2337002970','Develops intersectionality through legal and social analysis.'),
('critical_review_of_work','W1578338854','Review critiques Epstein, Landes, and Posner’s book; the article is the retrieval target.'),
('critical_review_of_work','W2657814049','Book review critiques Piketty’s Capital in the Twenty-First Century; the article is the target.'),
('critical_review_of_work','W2319044928','Review of Ely’s Democracy and Distrust, not the book itself; database author field needs checking.'),
('methods_paper','W1501821359','Examines feminist legal methods and how to use them in legal analysis.'),
('empirical_report','W3123985438','Empirical study of judicial treatment of race in criminal sentencing.'),
('empirical_report','W2177794968','Empirical evaluation of local police surges on crime and arrests in New York City; criminal justice policy adjacency.'),
('empirical_report','W4237793781','Empirical reply tests abortion and crime evidence; criminal justice policy research with contested conclusions.'),
('systematic_review','W2186243923','Campbell systematic review and meta-analysis of problem-oriented policing; criminal justice and public policy adjacency.'),
('systematic_review','W2112915715','Campbell systematic review of legitimacy in policing; criminal justice and public policy adjacency.'),
('systematic_review','W2180537218','Campbell systematic review of hot spots policing; criminal justice and public policy adjacency.'),
('study_review_protocol','W2956864763','Protocol for a systematic review of hot-spots policing; criminal justice and public policy adjacency.'),
('study_review_protocol','W2590707784','Protocol for a systematic review of third-party policing; criminal justice and public policy adjacency.'),
('study_review_protocol','W2959253837','Protocol for a systematic review of community-oriented policing; criminal justice and public policy adjacency.'),
]
contract=json.load(open(P+'../selection-contract.json'))
s=requests.Session(); output=[]; crossref=True; errors=[]
for form,wid,basis in rows:
 r=s.get('https://api.openalex.org/works/'+wid,timeout=25);r.raise_for_status();w=r.json(); doi=(w.get('doi') or '').replace('https://doi.org/','') or None
 cv=None; ctitle=None; cs=None
 if doi and crossref:
  try:
   c=s.get('https://api.crossref.org/works/'+doi,timeout=25);cs=c.status_code
   if cs==403: crossref=False;errors.append('Crossref HTTP 403: stopped all subsequent requests')
   elif cs==200:
    cv=c.json()['message'];ctitle=(cv.get('title') or [''])[0]
  except Exception as e: errors.append(str(e))
 norm=lambda a:re.sub(r'[^a-z0-9]','',re.sub(r'<[^>]*>','',a).lower())
 matched=bool(ctitle and norm(ctitle)==norm(w['title']))
 if cv and not matched: errors.append(wid+' DOI title mismatch: '+repr(ctitle)+' vs '+repr(w['title']))
 b=w.get('biblio') or {}; loc=w.get('primary_location') or {}; src=loc.get('source') or {}; authors=[a['author']['display_name'] for a in w.get('authorships',[])]; year=w['publication_year']; title=w['title']
 # Review Cox/Ely: OpenAlex misattributes the reviewed book author; use reviewer only.
 if wid=='W2319044928': authors=['Archibald Cox']
 if wid=='W1578338854': src={'display_name':'Harvard Law Review'}; b={'volume':'127','first_page':'2464','last_page':'2497'}; loc['landing_page_url']='https://scholarship.law.tamu.edu/facscholar/2481/'
 if wid=='W2657814049': src={'display_name':'Harvard Law Review'}; b={'volume':'128','issue':'2','first_page':'626','last_page':'667'}; loc['landing_page_url']='https://harvardlawreview.org/print/vol-128/the-laws-of-capitalism/'
 if b.get('first_page') == b.get('last_page'): b['last_page']=None
 doiout=doi if matched else None
 d={'id':'law_'+wid.lower(),'field':'law_public_policy','form_id':form,'title':title,'authors':authors,'year':year,'venue':src.get('display_name'),'doi':doiout,'stable_url':loc.get('landing_page_url') or w['id'],'volume':b.get('volume'),'issue':b.get('issue'),'pages':'–'.join(x for x in [b.get('first_page'),b.get('last_page')] if x) or None,'form_basis':basis,'form_status':'provisional metadata and abstract screening; inspect article on retrieval','selection_signal_type':'scholarly citations (OpenAlex indexed works)','selection_evidence':f"OpenAlex reports {w.get('cited_by_count')} citations, snapshot 2026-11-16; provider coverage and document matching vary.",'selection_source_url':'https://api.openalex.org/works/'+wid,'citation_count':w.get('cited_by_count'),'citation_provider':'OpenAlex','citation_snapshot':'2026-11-16','verification_status':'live OpenAlex work record'+(' and Crossref DOI-title match' if matched else '; DOI not independently matched'),'verification_sources':['https://api.openalex.org/works/'+wid]+(['https://api.crossref.org/works/'+doi] if matched else []),'date_notes':'2015–2019 supplement' if 2015<=year<=2019 else 'original publication through 2014','copy_status':'metadata only; article body not downloaded','retrieval_locator':f"{', '.join(authors)}; {title}; {src.get('display_name')}; {year}; volume {b.get('volume')}, issue {b.get('issue')}, pages {b.get('first_page')}–{b.get('last_page')}; {loc.get('landing_page_url') or w['id']}",'why_this_example':basis,'limitations':'Citation count is a selection signal, not a readership measure or proof of quality; full-text form and original pagination require confirmation.'}
 if doi and not matched:d['limitations']+=f' OpenAlex DOI lead {doi} is withheld pending exact bibliographic verification.'
 output.append(d)
print('errors',errors)
json.dump(output,open(P+'candidates.json','w'),indent=2,ensure_ascii=False)
coverage=[]
reasons={'personal_reflective_essay':'Applicable to law through personal legal essays; no separately verified examples in this bounded search.', 'argument_perspective':'Three original legal arguments, screened provisionally from article records.', 'critical_review_of_work':'Three reviews of specific books, not the books; reviewer and pagination should be confirmed in original journal.', 'conceptual_explainer':'Applicable; no three verified standalone legal explainers identified.', 'tutorial':'Applicable in legal education; no verified historical standalone tutorials identified in this pass.', 'procedure_how_to':'Applicable legal practice guidance, but historical edition and specific procedural document require verification.', 'reference_entry':'Applicable legal reference entries; historical version and individual authorship not established.', 'empirical_report':'Three published empirical studies including crime-policy work; one is a 2015–2019 supplement.', 'methods_paper':'One legal methods paper; two further standalone methods papers not verified.', 'theory_conceptual_paper':'Three conceptual contributions grounded in legal theory.', 'case_report':'Clinical case-report form does not map directly to judicial opinions or doctrinal case commentary; case studies may be considered only with a separately defined analogue.', 'study_review_protocol':'Three research protocols adjacent to law via policing policy; two are 2015–2019 supplements.', 'narrative_critical_literature_review':'Applicable to sociolegal research; doctrinal synthesis and book reviews are not sufficient evidence of a literature review.', 'scoping_review':'Applicable to public-policy research; no pre-2020 eligible study verified.', 'systematic_review':'Three Campbell reviews are criminology/policing policy, not doctrinal legal reviews.', 'proposal':'Applicable to public policy; no three actual proposals with date, authorship and subject verified.', 'decision_memo':'Applicable to government decision-making; published OLC legal advice and policy directives cannot automatically be treated as decision memos.'}
for f in contract['forms']:
 fid=f['id']; ids=[x['id'] for x in output if x['form_id']==fid]; n=len(ids)
 status='three_targets' if n==3 else ('partial_gap' if n else ('conditional_analogue' if fid=='case_report' else 'no_verified_targets'))
 coverage.append({'form_id':fid,'status':status,'requested':3,'provided':n,'candidate_ids':ids,'reason':reasons[fid]})
json.dump(coverage,open(P+'coverage.json','w'),indent=2,ensure_ascii=False)
