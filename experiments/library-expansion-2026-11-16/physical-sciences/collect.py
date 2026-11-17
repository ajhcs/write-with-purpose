import requests,json,time,pathlib,sys
p=pathlib.Path(__file__).parent
items=[
('personal_reflective_essay','10.1103/RevModPhys.74.875','Nobel lecture combining personal historical narrative with a technical account'),
('personal_reflective_essay','10.1103/RevModPhys.74.1131','Nobel lecture expressly describes discovery and study from personal perspective'),
('personal_reflective_essay','10.1103/RevModPhys.76.981','Nobel lecture reflecting on the author’s work and intellectual commitments; technical lecture analogue'),
('argument_perspective','10.1126/science.177.4047.393','Physicist argues for the autonomy and irreducibility of emergent phenomena'),
('argument_perspective','10.1002/cpa.3160130102','Essay argues about the effectiveness of mathematics in natural sciences'),
('conceptual_explainer','10.1103/RevModPhys.81.1727','Colloquium explains EPR concepts and applications'),
('conceptual_explainer','10.1103/RevModPhys.75.715','Explains decoherence and the quantum origins of classical behavior'),
('conceptual_explainer','10.1103/RevModPhys.82.2835','Colloquium introduces consistent quantum theory'),
('tutorial','10.1140/epjst/e2012-01535-1','Tutorial introducing quantum states, measurement and operations'),
('tutorial','10.1080/00107514.2011.603578','Tutorial introducing building blocks of trapped-ion quantum information'),
('tutorial','10.1088/0953-4075/48/8/083001','Tutorial on photonic quantum computing'),
('empirical_report','10.1103/PhysRevLett.116.061102','Reports observation of gravitational waves; 2016 supplemental period'),
('empirical_report','10.1103/PhysRevLett.75.3969','Reports Bose-Einstein condensation in dilute gas'),
('empirical_report','10.1103/PhysRevLett.49.1804','Reports experimental test of Bell inequalities'),
('methods_paper','10.1103/PhysRev.136.B864','Introduces density-functional theory for inhomogeneous electron systems'),
('methods_paper','10.1103/PhysRev.47.777','Theoretical argument, excluded as method unless recategorized'),
('methods_paper','10.1103/PhysRevLett.77.3865','Introduces a generalized gradient approximation for density-functional calculations'),
('methods_paper','10.1103/PhysRevLett.69.2863','Introduces the density-matrix renormalization group numerical method'),
('theory_conceptual_paper','10.1103/PhysRev.47.777','Einstein, Podolsky and Rosen construct a conceptual argument about quantum mechanics'),
('theory_conceptual_paper','10.1103/PhysRev.108.1175','Bardeen, Cooper and Schrieffer develop a microscopic theory of superconductivity'),
('theory_conceptual_paper','10.1103/PhysRev.140.A1133','Kohn and Sham formulate a density-functional approach'),
('narrative_critical_literature_review','10.1103/RevModPhys.86.419','Narrative topical review synthesizes Bell nonlocality'),
('narrative_critical_literature_review','10.1103/RevModPhys.71.463','Narrative review synthesizes Bose-Einstein condensation'),
('narrative_critical_literature_review','10.1103/RevModPhys.82.3045','Narrative colloquium synthesizes topological insulator physics'),
]
s=requests.Session();s.headers.update({'User-Agent':'AcademicBibliographyResearch/1.0 (metadata verification)'})
out=[]
for form,doi,basis in items:
 if form=='methods_paper' and doi=='10.1103/PhysRev.47.777':continue
 try:
  r=s.get('https://api.crossref.org/works/'+doi,timeout=20)
  if r.status_code==403:
   print('CROSSREF_403_STOP',flush=True);sys.exit(3)
  if r.status_code==429:
   print('CROSSREF_429_RETRY',doi,flush=True);time.sleep(3);r=s.get('https://api.crossref.org/works/'+doi,timeout=20)
  if r.status_code!=200:print('CROSSREF_ERROR',doi,r.status_code,flush=True);continue
  x=r.json()['message']; year=(x.get('published-print') or x.get('published-online') or x.get('published'))['date-parts'][0][0]
  q=s.get('https://api.openalex.org/works/https://doi.org/'+doi,timeout=20); o=q.json() if q.status_code==200 else {}
  title=x.get('title',[''])[0]; auth=[' '.join(filter(None,[a.get('given'),a.get('family')])) for a in x.get('author',[])]
  row={'id':'psm_'+str(len(out)+1).zfill(2),'field':'physical_sciences_mathematics','form_id':form,'title':title,'authors':auth,'year':year,'venue':x.get('container-title',[''])[0],'doi':x.get('DOI'),'stable_url':x.get('URL'),'volume':x.get('volume'),'issue':x.get('issue'),'pages':x.get('page',x.get('article-number')),'form_basis':basis,'form_status':'candidate' if form!='personal_reflective_essay' else 'conditional_analogue','selection_signal_type':'citation_count' if 'cited_by_count' in o else 'publisher_or_official_record','selection_evidence':('OpenAlex cited-by count '+str(o['cited_by_count'])+'; retrieval 2026-11-16' if 'cited_by_count' in o else 'Published venue and source metadata; no readership claim'),'selection_source_url':o.get('id',x.get('URL')),'citation_count':o.get('cited_by_count'),'citation_provider':'OpenAlex' if 'cited_by_count' in o else None,'citation_snapshot':'2026-11-16' if 'cited_by_count' in o else None,'verification_status':'crossref_verified','verification_sources':['https://api.crossref.org/works/'+doi,x.get('URL')], 'date_notes':'2015–2019 supplement' if 2015<=year<=2019 else ('Outside preferred period' if year>2019 else 'Original through 2014'), 'copy_status':'metadata only; no full text downloaded','retrieval_locator':x.get('URL'),'why_this_example':basis,'limitations':'Citation count is not a readership measure; content suitability based on metadata and abstract, not full-text assessment.'}
  out.append(row); print(row['id'],year,title,doi,'count',row['citation_count'],flush=True)
 except Exception as e:print('ERROR',doi,repr(e),flush=True)
(p/'candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
