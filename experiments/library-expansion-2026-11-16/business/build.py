import json,datetime
from pathlib import Path
p=Path(__file__).parent
rows=[json.loads(x) for x in (p/'crossref-raw.jsonl').read_text().splitlines()]
forms={
'Building Theories from Case Study Research':('methods_paper','Publisher abstract explains an iterative case-based theory-building research process.'),
'Strategies for Theorizing from Process Data':('methods_paper','Publisher abstract compares strategies for analyzing process data.'),
'Methodological fit in management field research':('methods_paper','Publisher abstract presents a framework aligning research questions, prior work and design.'),
'An Integrative Model of Organizational Trust':('theory_conceptual_paper','Publisher abstract defines trust and proposes a model and research propositions.'),
'Upper Echelons: The Organization as a Reflection of Its Top Managers':('theory_conceptual_paper','Publisher abstract synthesizes a perspective and proposes a theory of managerial characteristics and outcomes.'),
'The Relational View: Cooperative Strategy and Sources of Interorganizational Competitive Advantage':('theory_conceptual_paper','Publisher abstract proposes interfirm relations as a unit of analysis and four sources of advantage.'),
'Agency Theory: An Assessment and Review':('narrative_critical_literature_review','Publisher abstract reviews agency theory, its contributions and extant empirical work.'),
'Sources of Conflict between Work and Family Roles':('narrative_critical_literature_review','Publisher abstract examines the literature and develops a model and propositions.'),
'A Review and an Integration of Research on Job Burnout':('narrative_critical_literature_review','Publisher abstract describes an integrative review and conceptual framework.'),
'How Does Human Resource Management Influence Organizational Outcomes? A Meta-analytic Investigation of Mediating Mechanisms':('systematic_review','Publisher abstract identifies a quantitative meta-analysis of HR systems and organizational outcomes.'),
'A Meta-Analytic Test of the Challenge Stressor–Hindrance Stressor Framework: An Explanation for Inconsistent Relationships Among Stressors and Performance':('systematic_review','Publisher abstract describes a meta-analytic test of workplace stressors; selection details require full-text checking.'),
'Women on Boards and Firm Financial Performance: A Meta-Analysis':('systematic_review','Publisher abstract describes a meta-analysis combining 140 studies; selection details require full-text checking.'),
'Is the Resource-Based “View” a Useful Perspective for Strategic Management Research?':('argument_perspective','Publisher abstract argues that the resource-based view needs conceptual development.'),
'The Reification of Absorptive Capacity: A Critical Review and Rejuvenation of the Construct':('critical_review_of_work','Publisher abstract critically examines the treatment of one named construct across 289 papers; a body-of-work critique, not a review of a single work.'),
'Bad for Practice: A Critique of the Transaction Cost Theory':('argument_perspective','A named theoretical critique; exact form should be checked against publisher abstract before coding.'),
'What Constitutes a Theoretical Contribution?':('tutorial','Publisher abstract discusses steps and tradeoffs in developing theory for researchers.'),
'Measuring organizational performance in the absence of objective measures: The case of the privately‐held firm and conglomerate business unit':('methods_paper','Publisher abstract addresses measuring organizational performance where objective measures are unavailable.'),
'High-Performance Human Resource Practices, Citizenship Behavior, and Organizational Performance: A Relational Perspective':('empirical_report','Publisher abstract reports a multilevel analysis of hotels linking HR practices, citizenship behavior and performance.'),
'THE IMPACT OF HUMAN RESOURCE MANAGEMENT PRACTICES ON TURNOVER, PRODUCTIVITY, AND CORPORATE FINANCIAL PERFORMANCE.':('empirical_report','Publisher abstract reports analysis of a national sample of nearly 1,000 firms.'),
}
# Limit to evidence demonstrated in publisher abstracts. Inferred titles remain flagged provisional, not counted.
provisional={'Bad for Practice: A Critique of the Transaction Cost Theory'}
candidates=[]
for r in rows:
 m=r['crossref'];title=m['title'][0]
 if title not in forms:continue
 form,basis=forms[title]; doi=r['doi'].removeprefix('https://doi.org/'); year=m['published']['date-parts'][0][0]
 author=[' '.join(filter(None,[a.get('given'),a.get('family')])) for a in m.get('author',[])]
 cand={'id':'business_'+str(len(candidates)+1).zfill(3),'field':'business_management','form_id':form,'title':title,'authors':author,'year':year,'venue':m.get('container-title',[''])[0],'doi':doi,'stable_url':'https://doi.org/'+doi,'volume':m.get('volume'),'issue':m.get('issue'),'pages':m.get('page'),'form_basis':basis,'form_status':'provisional: obtain publisher abstract or inspect full text' if title in provisional else 'publisher abstract supports placement','selection_signal_type':'OpenAlex citation count, venue queue','selection_evidence':r['selection'],'selection_source_url':r['query_url'],'citation_count':r['citation_count'],'citation_provider':r['citation_provider'],'citation_snapshot':r['citation_observed_at'],'verification_status':'Crossref live metadata; some publisher DOI requests redirect to a second DOI record for the same title','verification_sources':[{'provider':'Crossref','query_url':r['verification_url'],'retrieved_at':'2026-11-16 UTC'},{'provider':'publisher','query_url':'https://journals.aom.org/doi/'+doi if doi.startswith('10.5465/') else 'https://doi.org/'+doi,'retrieved_at':'2026-11-16 UTC'}],'date_notes':('Published online November 2014; print 2015, classified as 2015 supplement' if title.startswith('Women on Boards') else '2015–2019 supplement' if year>=2015 else 'original publication through 2014'),'copy_status':'complete copy not requested or verified','retrieval_locator':f"{title}; {', '.join(author)}; {m.get('container-title',[''])[0]}, {year}; DOI {doi}",'why_this_example':basis,'limitations':'Citation counts measure citations, not readership or writing quality. Full text not inspected.'}
 candidates.append(cand)
contract=json.loads((p.parent/'selection-contract.json').read_text()); cells=[]
reasons={
'personal_reflective_essay':'Applicable: practitioner first-person reflection. Publisher HBR leads found, but live bibliographic API verification and eligible prominence signals are unfinished.',
'argument_perspective':'Applicable: management perspectives argue and defend a position. Only one publisher-abstract-verified selection so far.',
'critical_review_of_work':'Applicable: critiques of single books, papers or named bodies of work occur, but body-of-work analogue must be distinguished from single-work review.',
'conceptual_explainer':'Applicable to management concepts; no form-screened examples verified in this pass.',
' tutorial':'Applicable research teaching; screen for instructional sequence.',
'procedure_how_to':'Applicable to management practice; HBR publisher leads located but not yet bibliographically API verified.',
'reference_entry':'Applicable in business reference works; individual entries require source and eligibility checks.',
'empirical_report':'Applicable to management field research; two verified reports, with a third target still needed.',
'methods_paper':'Applicable: process research and empirical design methods.',
' theory_conceptual_paper':'Applicable: original conceptual models and theory.',
'case_report':'Clinical case report is not equivalent to a business teaching case; no clinical-type business analogue is counted.',
'study_review_protocol':'Applicable to management review protocols; no verified targets identified.',
'narrative_critical_literature_review':'Applicable: integrative syntheses of management research.',
'scoping_review':'Applicable: exploratory evidence mapping. A 2024 publisher example exists outside requested window; no eligible historical examples verified.',
'systematic_review':'Applicable: systematic and meta-analytic syntheses. Reported search and screening require full-text verification.',
'proposal':'Applicable to business projects and investment decisions; no verified public examples identified.',
'decision_memo':'Applicable to executive decisions; no verified public examples identified.'}
reasons['tutorial']=reasons.pop(' tutorial');reasons['theory_conceptual_paper']=reasons.pop(' theory_conceptual_paper')
for f in contract['forms']:
 fid=f['id']; good=[x['id'] for x in candidates if x['form_id']==fid and not x['form_status'].startswith('provisional')][:3]
 # Body-of-work critique is conditional, not counted as single-work review.
 if fid=='critical_review_of_work': good=[]
 status=('three_targets' if len(good)>=3 else 'partial_gap' if good else 'conditional_analogue' if fid in ['case_report','critical_review_of_work'] else 'no_verified_targets')
 cells.append({'form_id':fid,'status':status,'requested':3,'provided':len(good),'candidate_ids':good,'reason':reasons[fid]})
(p/'candidates.json').write_text(json.dumps(candidates,indent=2,ensure_ascii=False)+'\n')
(p/'coverage.json').write_text(json.dumps(cells,indent=2,ensure_ascii=False)+'\n')
print(len(candidates),sum(c['provided'] for c in cells),[(c['form_id'],c['provided']) for c in cells])
