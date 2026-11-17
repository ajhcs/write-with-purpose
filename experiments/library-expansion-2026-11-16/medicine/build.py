import requests,json,csv,datetime,re,xml.etree.ElementTree as ET,pathlib,html
p=pathlib.Path(__file__).parent
s=json.load(open(p/'search-receipts.json'))
q='TITLE:"systematic review protocol" AND FIRST_PDATE:[1900-01-01 TO 2014-12-31] SORT_CITED:y'
r=requests.get('https://www.ebi.ac.uk/europepmc/webservices/rest/search',params={'query':q,'format':'json','pageSize':50,'resultType':'core'},timeout=30);r.raise_for_status();j=r.json();s['review_protocol']={'url':r.url,'hitCount':j['hitCount'],'results':j['resultList']['result']};(p/'review-protocol-receipt.json').write_text(json.dumps(s['review_protocol'],indent=2))
allrecords={str(x['pmid']):x for d in s.values() for x in d['results'] if x.get('pmid')}
selection={
'personal_reflective_essay':['18812523','24002273','23571585'],
'argument_perspective':['22579042','19362359','18790295'],
'critical_review_of_work':['29405744'],
'conceptual_explainer':['19061483','20840865','18566595'],
 'tutorial':['20688472','20053272','17031868'],
'procedure_how_to':['19362699','18323559','12111920'],
'reference_entry':['24193082','24737367','21171977'],
'empirical_report':['12117397','10471456','9196156'],
'methods_paper':['10075613','7249508','17099194'],
'theory_conceptual_paper':['22594719','16134045','19850390'],
'case_report':['21418591','18447934','24513181'],
'study_review_protocol':['15178990','3124598','23763567'],
'narrative_critical_literature_review':['17200220','22709336','20083828'],
'scoping_review':['21672914','19261347','23350759'],
'systematic_review':['15479938','21069833','21768583'],
'proposal':['15273542','21793988','10484010'],
'decision_memo':['24378917','22801674','18838716']}
ids=[i for v in selection.values() for i in v];url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi';r=requests.get(url,params={'db':'pubmed','id':','.join(ids),'retmode':'xml'},timeout=60);r.raise_for_status();(p/'pubmed-efetch.xml').write_text(r.text);(p/'pubmed-receipt.json').write_text(json.dumps({'url':r.url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':r.status_code,'requested_pmids':ids},indent=2)); root=ET.fromstring(r.content)
pm={a.findtext('.//MedlineCitation/PMID'):a for a in root.findall('PubmedArticle')}
inv={x['doi'].lower().strip() for x in csv.DictReader(open('experiments/corpus-analysis-2026-11-16/results/document-inventory.csv')) if x['doi']}
assert len(pm)==len(ids),(len(pm),len(ids))
clean=lambda e: ''.join(e.itertext()).strip() if e is not None else ''
forms={x['id']:x for x in json.load(open('experiments/library-expansion-2026-11-16/selection-contract.json'))['forms']}
explain={
'personal_reflective_essay':'JAMA Narrative Medicine collection identifies A Piece of My Mind as real-life physician essays; this is a section-based classification, with full text still to inspect.',
'argument_perspective':'Lancet comment in which the author argues for an approach to a healthcare question; commentary type and article purpose support perspective placement.',
'critical_review_of_work':'Publisher labels it Book Review and identifies the specific book under evaluation; review itself is the unit requested.',
'conceptual_explainer':'Abstract describes an explanatory synthesis of mechanisms, designed to convey how a biological process works; a review-article form used as a conceptual explanation.',
'tutorial':'Abstract explicitly presents a didactic overview, examples, or guidance to learn a research or statistical technique.',
'procedure_how_to':'Abstract describes steps and practical choices for carrying out or interpreting a research procedure; research methods rather than bedside instructions.',
'reference_entry':'Conditional analogue: standalone clinical topic review organized to support consultation, not an encyclopedia entry. Abstract establishes scope; full text needs inspection for reference-like organization.',
'empirical_report':'Abstract reports an actual randomized clinical trial and its participant outcomes; an empirical report, not a design-only protocol.',
'methods_paper':'Abstract develops, evaluates or applies an explicit method for clinical measurement, assessment, or prediction.',
 'theory_conceptual_paper':'Abstract proposes or develops an explicit explanatory framework addressing health, care, or health behavior.',
'case_report':'Journal of Medical Case Reports article reports an individual clinical case; abstract describes the patient presentation and case. Publisher explicitly labels the article Case report, and the abstract presents the case.',
'study_review_protocol':'Protocol describes proposed study or review design; exact stratum identified in why_this_example. Abstract should be checked for prospective versus retrospective timing.',
'narrative_critical_literature_review':'Review synthesizes a subject without presenting a completed systematic-review design as its defining method; abstract and review context support narrative placement.',
'scoping_review':'Abstract states mapping or scoping purpose and describes review of a broad literature; source also indexes it as a scoping review.',
'systematic_review':'Abstract describes a structured literature search and evidence selection; the actual completed review is distinct from a protocol.',
'proposal':'Proposal for a classification or common definition, with rationale and supporting evidence; conditional analogue to a funding or project proposal.',
'decision_memo':'Conditional analogue: published recommendation statement, with evidence assessment and explicit recommendation; not an internal decision memo.'}
rows=[];coverage=[]
for f,chosen in selection.items():
 for n,i in enumerate(chosen,1):
  x=allrecords[i]; a=pm[i]; art=a.find('.//MedlineCitation/Article'); title=clean(art.find('ArticleTitle')); title2=html.unescape(re.sub('<[^>]+>','',x['title'])).rstrip('.').lower(); assert title.rstrip('.').lower()==title2,(i,title,x['title'])
  authors=[]
  for au in art.findall('./AuthorList/Author'):
   name=au.findtext('CollectiveName') or ' '.join(filter(None,[au.findtext('LastName'),au.findtext('Initials')]))
   if name:authors.append(name)
  doi=next((e.text for e in a.findall('.//PubmedData/ArticleIdList/ArticleId') if e.get('IdType')=='doi'),None);assert (doi or '').lower()==(x.get('doi') or '').lower(),(i,doi,x.get('doi'))
  year=int(x['pubYear']);journal=art.find('./Journal'); venue=journal.findtext('Title'); issue=journal.find('./JournalIssue'); vol=issue.findtext('Volume'); number=issue.findtext('Issue'); pages=art.findtext('./Pagination/StartPage') or art.findtext('./Pagination/MedlinePgn') or x.get('pageInfo')
  sourceurl='https://europepmc.org/article/MED/'+i
  sourcegenre={'18812523':'https://jamanetwork.com/journals/jama/article-abstract/182618','24002273':'https://jamanetwork.com/journals/jama/article-abstract/1734708','23571585':'https://jamanetwork.com/journals/jama/article-abstract/1677377','29405744':'https://faseb.onlinelibrary.wiley.com/doi/10.1096/fj.14-0901ufm','21418591':'https://link.springer.com/article/10.1186/1752-1947-5-111','18447934':'https://link.springer.com/article/10.1186/1752-1947-2-139','24513181':'https://link.springer.com/article/10.1186/1752-1947-8-41'}.get(i,sourceurl)
  why=('Review protocol' if i=='23763567' else 'Study protocol') if f=='study_review_protocol' else forms[f]['name']
  row={'id':'medicine-'+f+'-'+str(n),'field':'medicine_health','form_id':f,'title':title,'authors':authors,'year':year,'venue':venue,'doi':doi,'stable_url':'https://pubmed.ncbi.nlm.nih.gov/'+i+'/','volume':vol,'issue':number,'pages':pages,'form_basis':explain[f], 'form_status':'conditional_analogue' if f in ('reference_entry','proposal','decision_memo') else 'source_metadata_abstract_supported; full_text_review_pending', 'selection_signal_type':'Europe PMC cited-by count' if x.get('citedByCount',0)>20 else 'Named journal section; citation count recorded for context', 'selection_evidence':f"Europe PMC indexed cited-by count {x.get('citedByCount',0)}; not field normalized",'selection_source_url':sourceurl,'citation_count':x.get('citedByCount',0),'citation_provider':'Europe PMC','citation_snapshot':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verification_status':'PubMed metadata checked; DOI matched Europe PMC; DOI resolution not checked','verification_sources':['https://pubmed.ncbi.nlm.nih.gov/'+i+'/',sourceurl,sourcegenre], 'date_notes':'Publication year from Europe PMC; PubMed record attached; print/online date can differ' ,'copy_status':'metadata only; library holdings unknown', 'retrieval_locator':'PMID '+i+ ('; DOI '+doi if doi else ''),'why_this_example':why+'; varied source for prose analysis and manual acquisition.', 'limitations':'Historical writing exemplar; clinical content may be outdated. Citation frequency is not writing quality or clinical endorsement; full text and source identity require library inspection.'}
  if doi and doi.lower() in inv: row['copy_status']='DOI found in existing document inventory; possible existing copy, inspect source before requesting'
  rows.append(row)
 status='conditional_analogue' if f in ('reference_entry','proposal','decision_memo') else ('three_targets' if len(chosen)==3 else 'partial_gap')
 reason=('Clinical topic reviews support consultation but are not reference entries.' if f=='reference_entry' else 'Classification proposals are conditional analogues to project or grant proposals.' if f=='proposal' else 'Recommendation statements are public decision-support analogues, not internal memos.' if f=='decision_memo' else 'Only one specific work review has sufficient source-genre support; further search needed.' if f=='critical_review_of_work' else 'Three metadata and abstract supported targets; full texts still need inspection.')
 coverage.append({'form_id':f,'status':status,'requested':3,'provided':len(chosen),'candidate_ids':['medicine-'+f+'-'+str(n) for n in range(1,len(chosen)+1)],'reason':reason})
(p/'candidates.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False));(p/'coverage.json').write_text(json.dumps(coverage,indent=2,ensure_ascii=False))
print('rows',len(rows),'inventory overlaps',[(r['id'],r['doi']) for r in rows if r['doi'] and r['doi'].lower() in inv])
