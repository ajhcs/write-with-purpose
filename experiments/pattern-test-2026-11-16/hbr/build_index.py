#!/usr/bin/env python3
"""Index reviewed practitioner reconstructions; external bodies remain private."""
import json,pathlib
out=pathlib.Path(__file__).resolve().parent
cache=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache')
def load(p): return json.loads(p.read_text())
records=[]
for id,title,author,year,reprint,src,pub,pat in [
('managing-oneself','Managing Oneself','Peter F. Drucker',1999,2005,'analysis/attachments/hbr-managing-oneself.pdf','drucker-reviewed.json',{'opening_claim':'present','early_dedicated_research_basis':'absent','repeated_component_definitions':'absent; question-led self-assessment with examples and advice','qualified_closing':'absent; closes with social-change prediction'}),
('balanced-scorecard','Using the Balanced Scorecard as a Strategic Management System','Robert S. Kaplan and David P. Norton',1996,None,'fulltext/business/pdf/W1558046248.pdf','scorecard-reviewed.json',{'opening_claim':'present','early_dedicated_research_basis':'experience with more than 100 organizations reported in opening, no separate research section','repeated_component_definitions':'four named processes with explanation and cases, varied treatment rather than uniform repeated definition-case-application sequence','qualified_closing':'absent; risks and uncertainty addressed in body'}),
]:
 d=load(out/pub);records.append({'id':id,'title':title,'author':author,'original_year':year,'reprint_year':reprint,'source_path':str(cache/src),'source_sha256':d['source_sha256'],'public_units':str(out/pub),'private_units':d['private_text_path'],'metrics':d['metrics'],'sections':d['sections'],'paragraph_functions':str(out/pub),'pattern_observation':pat,'status':d['status']})
f=out/'b/designing-services-body.json'; m=out/'b/designing-services-metrics.json'
if f.exists() and m.exists():
 d=load(f);records.append({'id':'designing-services','title':'Designing Services That Deliver','author':'G. Lynn Shostack','original_year':1984,'reprint_year':None,'source_path':str(cache/'fulltext/business/pdf/W17805075-a94f8556eec6466a.pdf'),'source_sha256':d['source_sha256'],'public_units':str(f),'private_units':str(cache/'pattern-test/hbr/b/designing-services-body.json'),'private_body':str(cache/'pattern-test/hbr/b/designing-services-body.txt'),'metrics':load(m),'sections':d['sections'],'paragraph_functions':str(f),'pattern_observation':{'opening_claim':'present','early_dedicated_research_basis':'not separately developed; example research within procedure','repeated_component_definitions':'absent; blueprint procedure developed through examples and exhibits','qualified_closing':'not a distinct limitation; final claims advocate blueprint use'},'status':d['status']})
for id,title,author,year,src,sha,reason in [
('power-of-talk','The Power of Talk: Who Gets Heard and Why','Deborah Tannen',1995,'fulltext/business/pdf/W1482060575-c97652cef05d7fed.pdf','c97652cef05d7fed50328f5a87b4fcaa8c20af7fe36c1eaece9ff80c6f6c98a9','Full candidate coding prepared; cross-page and normalization review in progress.'),
('customers-as-innovators','Customers as Innovators: A New Way to Create Value','Stefan Thomke and Eric von Hippel',2002,'fulltext/business/pdf/W1552480497-78ce1dfc8869d35f.pdf','78ce1dfc8869d35f68ba71982143c7ed7d334e47628d8a14ab11008ec1dd3bab','Whole-body review and coding in progress.'),
('house-of-quality','The House of Quality','John R. Hauser and Don Clausing',1988,'fulltext/business/pdf/W1578960547.pdf','495611e01d213eb92218ca1b884f9af22f03827ea734c75cd4985e4673f131e7','Source audit complete; masking and coding in progress.'),
('manufacturing-integration','Manufacturing: The New Case for Vertical Integration','Ted Kumpe and Piet T. Bolwijn',1988,'fulltext/business/pdf/W2506228356-60df32d3bf67e51d.pdf','60df32d3bf67e51ddb676f8bebed56a421236d7d0fc4700d8a9961e762956d18','Source audit complete; substantial recognition errors preclude clean-body metrics pending correction.')]:
 records.append({'id':id,'title':title,'author':author,'original_year':year,'reprint_year':None,'source_path':str(cache/src),'source_sha256':sha,'status':'candidate_not_yet_quantified','reason':reason})
# Include usable coding packets even when body metrics remain withheld.
for row in records:
 if row['id']=='power-of-talk' and (out/'a/power-coding.json').exists():
  row.update(public_units=str(out/'a/power-coding.json'), private_units=str(cache/'pattern-test/hbr/a/power-reconstruction.json'), private_body=str(cache/'pattern-test/hbr/a/power-body.txt'), paragraph_functions=str(out/'a/power-coding.json'), sections=load(out/'a/power-coding.json')['sections'], metrics_subset=load(out/'a/power-metrics-provisional.json') if (out/'a/power-metrics-provisional.json').exists() else None, status='reviewed_reconstruction_exploratory', metrics=load(out/'a/power-metrics-exploratory.json'), metrics_heading_caveat='Engine heading count is zero because heading blocks were not passed; see sections for printed headings.', pattern_observation={'opening_claim':'present','early_research_basis':'author sociolinguistic work stated in opening','repeated_component_definitions':'varied communication topics with case and explanation; not uniform definition sequence','qualified_closing':'present; no single solution fits every context'})
 if row['id']=='customers-as-innovators' and (out/'a/customers-coding.json').exists():
  row.update(public_units=str(out/'a/customers-coding.json'),private_units=str(cache/'pattern-test/hbr/a/customers-reconstruction.json'),private_body=str(cache/'pattern-test/hbr/a/customers-body.txt'),paragraph_functions=str(out/'a/customers-coding.json'), sections=load(out/'a/customers-coding.json')['sections'],status='reviewed_reconstruction_exploratory', metrics=load(out/'a/customers-metrics-exploratory.json'), normalized_units=str(cache/'pattern-test/hbr/a/customers-normalized.json'), normalized_body=str(cache/'pattern-test/hbr/a/customers-body-normalized.txt'), normalization_trace=str(out/'a/customers-normalization.json'), metrics_heading_caveat='Engine heading count is zero because heading blocks were not passed; see sections for printed headings.',pattern_observation={'opening_claim':'present','early_research_basis':'authors cross-industry study stated in opening','repeated_component_definitions':'toolkit capabilities introduced; later industry, benefit, implementation and value sections vary','qualified_closing':'present; value capture remains uncertain'})
 if row['id']=='house-of-quality' and (out/'b/house-body-candidate.json').exists():
  row.update(public_units=str(out/'b/house-body-candidate.json'),private_units=str(cache/'pattern-test/hbr/b/house-body-candidate.json'),private_body=str(cache/'pattern-test/hbr/b/house-body-candidate.txt'),paragraph_functions=str(out/'b/house-body-candidate.json'),status='reviewed_reconstruction_exploratory',metrics=load(out/'b/house-metrics.json'),sections=load(out/'b/house-body-candidate.json')['sections'],pattern_observation={'opening_claim':'present','early_research_basis':'not a separate opening research section','repeated_component_definitions':'quality-house elements and procedures developed through worked design case; repeated construction moves rather than fixed definition-case sequence','qualified_closing':'present near end: acknowledges implementation is not simple before final advocacy'})
for row in records:
 if row['id']=='manufacturing-integration' and (out/'b/manufacturing-body-candidate.json').exists():
  row.update(public_units=str(out/'b/manufacturing-body-candidate.json'),private_units=str(cache/'pattern-test/hbr/b/manufacturing-body-candidate.json'),private_body=str(cache/'pattern-test/hbr/b/manufacturing-body-candidate.txt'),paragraph_functions=str(out/'b/manufacturing-body-candidate.json'),sections=load(out/'b/manufacturing-body-candidate.json')['sections'],metrics_partial=load(out/'b/manufacturing-partial-metrics.json'),status='tentative_full_range_ocr_candidate_only_two_corrected_units')
eligibility={
 'managing-oneself':(True,'Advances a practitioner position that knowledge workers should manage themselves; questions and advice develop that position.'),
 'balanced-scorecard':(True,'Argues for extending the scorecard from measurement into an integrated strategic management system; processes substantiate this position.'),
 'power-of-talk':(True,'Argues that linguistic style shapes workplace judgments and that managers should adapt to those differences.'),
 'customers-as-innovators':(True,'Advocates shifting innovation activities to customers using toolkits and examines strategic consequences.'),
 'designing-services':(False,'Boundary case: central contribution is a procedural explanation of service blueprinting with worked examples; it advances a position but the dominant purpose is to explain a method.'),
 'house-of-quality':(False,'Boundary case: central contribution is explanation of a technical design tool and its use in a worked engineering example; its advocacy supports that explanatory purpose.'),
 'manufacturing-integration':(True,'Provisional form screen: sustained position favoring vertical integration using production-tier and cost examples. Corrupt OCR limits the full-body review, so this is not a verified quantitative holdout.')
}
for row in records:
 row['primary_argument_eligible'],row['primary_argument_rationale']=eligibility[row['id']]
for row in records:
 if row['id'] in ('power-of-talk','customers-as-innovators') and 'metrics' in row:
  row['metrics']['headings']=None
  row['metrics']['max_heading_depth']=None
  row['printed_headings']={'displayed':sum(x.get('type')=='explicit' for x in row['sections']), 'run_in':sum(x.get('type')=='explicit_run_in' for x in row['sections'])}
for row in records:
 row['included_in_primary_pattern_test']=row['id'] in ('managing-oneself','balanced-scorecard','power-of-talk','customers-as-innovators')
 row['included_in_quantitative_source_descriptions']=row['id']!='manufacturing-integration'
(out/'documents.json').write_text(json.dumps({'status':'live_index_exploratory','notes':'Distinct HBR holdouts. Do not interpret roles as additive paragraph budgets. Examples and author claims are not independently verified empirical evidence. Sources selected for availability, not population inference.','documents':records},indent=2,ensure_ascii=False)+'\n')
