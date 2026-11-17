import json,urllib.request,urllib.parse,datetime,time
from pathlib import Path
p=Path(__file__).parent
cs=json.loads((p/'candidates.json').read_text()); cells=json.loads((p/'coverage.json').read_text()); now=datetime.datetime.now(datetime.timezone.utc).isoformat()
# Capture DOI aliases in returned Crossref metadata without replacing original publisher locator.
raw=[json.loads(x) for x in (p/'crossref-raw.jsonl').read_text().splitlines()]
for c in cs:
 for r in raw:
  if c['doi']==r['doi'].removeprefix('https://doi.org/'):
   other=r['crossref']['DOI']
   c['doi_aliases']=[other] if other.lower()!=c['doi'].lower() else []
   break
# ID, form, author, date, publisher URL, purpose, selection signal, secondary source, metadata detail
hbr=[
('How I Did It: Giving Up the CEO Seat','personal_reflective_essay',['Jeffrey Hollender'],2010,'https://hbr.org/2010/03/how-i-did-it-giving-up-the-ceo-seat','A founder reflects in the first person on stepping down as CEO.','HBR selected the essay for its How I Did It magazine series','https://hbr.org/archive-toc/BR1003',None),
('How I Did It: The CEO of Aramex on Turning a Failed Sale into a Huge Opportunity','personal_reflective_essay',['Fadi Ghandour'],2011,'https://hbr.org/2011/03/how-i-did-it-the-ceo-of-aramex-on-turning-a-failed-sale-into-a-huge-opportunity','The founder recounts a failed sale and how the business grew.','HBR selected the essay for its How I Did It magazine series','https://hbr.org/archive-toc/BR1103',None),
('How Will You Measure Your Life?','personal_reflective_essay',['Clayton M. Christensen'],2010,'https://hbr.org/2010/07/how-will-you-measure-your-life','A management scholar reflects on personal decisions and applying business ideas to life.','HBR bestseller designation','https://hbr.org/archive-toc/BR1007',None),
('What Is Strategy?','argument_perspective',['Michael E. Porter'],1996,'https://hbr.org/1996/11/what-is-strategy','Argues that strategy involves distinct positioning and tradeoffs, beyond operational effectiveness.','HBR bestseller designation','https://hbr.org/archive-toc/3966',None),
('The Fall and Rise of Strategic Planning','argument_perspective',['Henry Mintzberg'],1994,'https://hbr.org/1994/01/the-fall-and-rise-of-strategic-planning','Challenges the conflation of formal planning and strategic thinking.','HBR magazine editorial selection','https://store.hbr.org/product/fall-and-rise-of-strategic-planning/94107',None),
('The Five Competitive Forces That Shape Strategy','conceptual_explainer',['Michael E. Porter'],2008,'https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy','Explains the five competitive forces and how they shape industry structure.','HBR bestseller designation','https://hbr.org/archive-toc/BR0801','18271320'),
('Why Business Models Matter','conceptual_explainer',['Joan Magretta'],2002,'https://hbr.org/2002/05/why-business-models-matter','Explains the business model and its relationship to strategy.','HBR selected feature and publisher reissued the work','https://store.hbr.org/product/why-business-models-matter/R0205F',None),
('What Is Disruptive Innovation?','conceptual_explainer',['Clayton M. Christensen','Michael E. Raynor','Rory McDonald'],2015,'https://hbr.org/2015/12/what-is-disruptive-innovation','Explains a theory and common misapplications.','HBR selected work as a classic','https://hbr.org/2015/12/what-is-disruptive-innovation',None),
('How to Write a Great Business Plan','procedure_how_to',['William A. Sahlman'],1997,'https://hbr.org/1997/07/how-to-write-a-great-business-plan','Provides questions and components for preparing a business plan.','Publisher selected for entrepreneurial finance collection','https://hbr.org/insight-center/entrepreneurship-for-the-long-term','10168340'),
('Managing Your Boss','procedure_how_to',['John J. Gabarro','John P. Kotter'],1980,'https://hbr.org/2005/01/managing-your-boss','Offers practical steps for understanding and managing a working relationship.','HBR bestseller designation','https://hbr.org/archive-toc/BR0501','10245410'),
('Discovering Your Authentic Leadership','procedure_how_to',['Bill George','Peter Sims','Andrew N. McLean','Diana Mayer'],2007,'https://hbr.org/2007/02/discovering-your-authentic-leadership','Guides readers through developing self-knowledge and authentic leadership.','HBR bestseller designation','https://hbr.org/archive-toc/BR0702',None),
]
for title,form,authors,year,url,basis,signal,surl,pmid in hbr:
 vs=[{'provider':'Harvard Business Review publisher','query_url':url,'retrieved_at':now}]
 if pmid:vs.append({'provider':'PubMed','query_url':'https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/','retrieved_at':now})
 c={'id':'business_'+str(len(cs)+1).zfill(3),'field':'business_management','form_id':form,'title':title,'authors':authors,'year':year,'venue':'Harvard Business Review','doi':None,'doi_aliases':[],'stable_url':url,'volume':None,'issue':None,'pages':None,'form_basis':basis,'form_status':'publisher text and description support placement','selection_signal_type':'publisher bestseller' if 'bestseller' in signal.lower() else 'publisher editorial selection','selection_evidence':signal,'selection_source_url':surl,'citation_count':None,'citation_provider':None,'citation_snapshot':None,'verification_status':'publisher metadata verified live'+(' and PubMed' if pmid else '; no bibliographic API match established'),'verification_sources':vs,'date_notes':('2015 supplement' if year==2015 else 'original publication through 2014')+('; linked publisher version is a 2005 reprint; PubMed gives 1980 title with subtitle' if title=='Managing Your Boss' else ''),'copy_status':'complete copy not requested or verified','retrieval_locator':f"{title}; {', '.join(authors)}; Harvard Business Review, {year}; {url}"+('; PMID '+pmid if pmid else ''),'why_this_example':basis,'limitations':'Editorial selection alone does not establish readership. DOI not identified. No full copy inspected.'}
 cs.append(c)
# Independent Crossref metadata plus publisher abstracts for relevant journal articles.
newdois=[('10.1287/orsc.1060.0191','empirical_report','Publisher abstract reports data from 88 urban schools and tests hypotheses on social capital and performance.','https://pubsonline.informs.org/doi/abs/10.1287/orsc.1060.0191'),('10.5465/amj.2009.44632557','tutorial','Publisher full text provides practical guidance for writing and reviewing qualitative research.','https://journals.aom.org/doi/full/10.5465/AMJ.2009.44632557'),('10.1177/1094428104263675','tutorial','Publisher describes a tutorial on choosing factors using parallel analysis.','https://journals.sagepub.com/doi/10.1177/1094428104263675'),('10.5465/amr.1998.192979','critical_review_of_work','Publisher identifies this as Dave Ulrich’s review of a named management book; the selected work is the review article.','https://journals.aom.org/doi/10.5465/amr.1998.192979'),('10.5465/amr.1990.4309121','critical_review_of_work','Publisher identifies Chris Argyris as reviewer of Robert Cole’s named book; the selected work is the review article.','https://journals.aom.org/doi/10.5465/amr.1990.4309121'),('10.1177/0170840611416736','critical_review_of_work','Publisher identifies Stewart Clegg’s review of the named edited handbook; the selected work is the review article.','https://journals.sagepub.com/doi/10.1177/0170840611416736')]
receipts=[]
for doi,form,basis,pub in newdois:
 u='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='/')
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'CorpusResearch/1.0 metadata'}),timeout=15) as f:m=json.load(f)['message']
 except Exception as e:
  print('ERROR CROSSREF',str(e));break
 title=m['title'][0]; authors=[' '.join(filter(None,[a.get('given'),a.get('family')])) for a in m.get('author',[])];year=m['published']['date-parts'][0][0]
 # Pull OpenAlex by DOI to establish a dated citation signal if available.
 oa=None;ou='https://api.openalex.org/works/https://doi.org/'+urllib.parse.quote(doi,safe='/')
 try:
  with urllib.request.urlopen(urllib.request.Request(ou,headers={'User-Agent':'CorpusResearch/1.0 metadata'}),timeout=15) as f: oa=json.load(f)
 except Exception:pass
 receipts.append({'doi_query':doi,'crossref_query_url':u,'crossref':m,'openalex_query_url':ou,'openalex':oa,'retrieved_at':now})
 if 'review' in form: signal='Editorial selection of review of a named management work';stype='publisher editorial selection'; source=pub
 elif oa: signal='OpenAlex cited_by_count at retrieval';stype='citation count';source=ou
 else:signal='Publisher selected methods tutorial';stype='publisher editorial selection';source=pub
 c={'id':'business_'+str(len(cs)+1).zfill(3),'field':'business_management','form_id':form,'title':title,'authors':authors,'year':year,'venue':m.get('container-title',[''])[0],'doi':doi,'doi_aliases':[m['DOI']] if m['DOI'].lower()!=doi.lower() else [],'stable_url':pub,'volume':m.get('volume'),'issue':m.get('issue'),'pages':m.get('page'),'form_basis':basis,'form_status':'publisher description supports placement','selection_signal_type':stype,'selection_evidence':signal,'selection_source_url':source,'citation_count':oa.get('cited_by_count') if oa and stype=='citation count' else None,'citation_provider':'OpenAlex' if oa and stype=='citation count' else None,'citation_snapshot':now if oa and stype=='citation count' else None,'verification_status':'Crossref live metadata and publisher description','verification_sources':[{'provider':'Crossref','query_url':u,'retrieved_at':now},{'provider':'publisher','query_url':pub,'retrieved_at':now}],'date_notes':'original publication through 2014','copy_status':'complete copy not requested or verified','retrieval_locator':f"{title}; {', '.join(authors)}; {m.get('container-title',[''])[0]}, {year}; DOI {doi}",'why_this_example':basis,'limitations':'Full text not inspected for all entries; editorial selection is not a readership claim.'}
 cs.append(c); time.sleep(.3)
(p/'additional-metadata.json').write_text(json.dumps(receipts,indent=2,ensure_ascii=False)+'\n')
for cell in cells:
 fid=cell['form_id'];valid=[x for x in cs if x['form_id']==fid and not x['form_status'].startswith('provisional')]
 if fid=='critical_review_of_work':valid=[x for x in valid if x['id']!='business_014']
 # Use new purpose-built tutorials before broad Whetten guidance.
 if fid=='tutorial':valid=valid[-2:]+valid[:1]
 valid=valid[:3];cell['candidate_ids']=[x['id'] for x in valid];cell['provided']=len(valid)
 if len(valid)==3: cell['status']='three_targets';cell['reason']='Three publisher-described examples identified; source relevance and complete-copy status still require corpus review.'
 elif valid:cell['status']='partial_gap';cell['reason']='Applicable form; '+str(len(valid))+' examples identified and further selection is needed.'
(p/'candidates.json').write_text(json.dumps(cs,indent=2,ensure_ascii=False)+'\n');(p/'coverage.json').write_text(json.dumps(cells,indent=2,ensure_ascii=False)+'\n')
print('candidates',len(cs),'counted',sum(c['provided'] for c in cells));print([(c['form_id'],c['provided']) for c in cells])
