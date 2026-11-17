import json
from pathlib import Path
p=Path(__file__).parent
contract=json.loads((p.parent/'selection-contract.json').read_text())
long='https://longreads.com/2014/12/19/longreads-best-of-2014-essay-writing/'
sci='https://longreads.com/2014/12/18/longreads-best-of-2014-science-stories/'
asme='https://www.asme.media/national-magazine-awards-2014-finalists-announced'
rows=[
('p01','personal_reflective_essay','Poor Teeth','Sarah Smarsh',2014,'Aeon','https://aeon.co/essays/there-is-no-shame-worse-than-poor-teeth-in-a-rich-world','October 23','Personal experience and family history frame social reflection.','Longreads 2014 favorite essays; also 2015 Best American Essays notable for 2014',long),
('p02','personal_reflective_essay','Sliver of Sky: Confronting the Trauma of Sexual Abuse','Barry Lopez',2013,'Harper’s Magazine','https://harpers.org/archive/2013/01/sliver-of-sky/','January issue, pp. 41–48','Personal account and reflection on childhood sexual abuse and its aftermath.','2014 National Magazine Awards finalist, Essays and Criticism',asme),
('p03','personal_reflective_essay','The Old Man at Burning Man','Wells Tower',2013,'GQ','https://www.gq.com/story/burning-man-experiences-wells-tower-gq-february-2013','February issue','First-person father and son travel narrative.','2014 National Magazine Awards finalist, Essays and Criticism',asme),
('p04','argument_perspective','The Case for Reparations','Ta-Nehisi Coates',2014,'The Atlantic','https://www.theatlantic.com/magazine/archive/2014/06/the-case-for-reparations/361631/','June issue; online May 21','Evidence-led public argument calling for reparations.','Longreads 2014 essay editor’s pick',long),
('p05','argument_perspective','My Vassar College Faculty ID Makes Everything OK','Kiese Laymon',2014,'Gawker','https://gawker.com/my-vassar-college-faculty-id-makes-everything-ok-1664133077','November 29','Experience-grounded critique of racism and institutional power.','Longreads 2014 favorite essay',long),
('p06','argument_perspective','Men Explain Things to Me','Rebecca Solnit',2008,'TomDispatch','https://tomdispatch.com/best-of-tomdispatch-rebecca-solnit-the-archipelago-of-arrogance/','April 2008; original-title and exact-date verification pending','Personal anecdote develops an argument about gender and credibility.','2014 Best of TomDispatch selection of 2008 piece','https://znetwork.org/znetarticle/men-explain-things-to-me/'),
('p07','critical_review_of_work','Difficult Women','Emily Nussbaum',2013,'The New Yorker','https://www.newyorker.com/magazine/2013/07/29/sex-and-the-city-difficult-women','July 29 issue; July 22 online','Retrospective evaluation of Sex and the City.','One of three columns in 2014 National Magazine Award-winning portfolio','https://www.newyorker.com/galleries/gallery-the-new-yorker-wins-four-national-magazine-awards'),
('p08','critical_review_of_work','Hannah Arendt, Guilty Pleasure','J. Hoberman',2013,'Tablet Magazine','https://www.tabletmag.com/sections/arts-letters/articles/hannah-arendt-guilty-pleasure','May 24','Critical review of Margarethe von Trotta’s film Hannah Arendt.','One of three columns in 2014 National Magazine Awards finalist portfolio',asme),
('p09','critical_review_of_work','Overexposed','Witold Rybczynski',2013,'Architect','https://www.architectmagazine.com/architects/overexposed.aspx','April issue; pages 76, 78, 81–82, 84, 87','Comparison and architectural criticism of Seattle Central Library and another building.','One of three columns in 2014 National Magazine Awards finalist portfolio',asme),
('p10','conceptual_explainer','The End of Night','Rebecca Boyle',2014,'Aeon','https://aeon.co/essays/we-can-t-thrive-in-a-world-without-darkness','April 1','Reported public explanation of artificial light, ecology and circadian biology.','Longreads 2014 favorite science stories',sci),
('p11','conceptual_explainer','DIY Diagnosis','Ed Yong',2014,'Mosaic','https://gizmodo.com/diy-diagnosis-how-one-woman-uncovered-her-own-genetic-1623734397','August 19; Mosaic syndication on Gizmodo','Explains genetics through a patient’s learning and diagnosis; strongly narrative.','Longreads 2014 favorite science stories',sci),
('p12','conceptual_explainer','Arrested Development','Virginia Hughes',2014,'Mosaic','https://medium.com/mosaic-science/arrested-development-c3e153332db4','May 20','Reported examination of developmental arrest and uncertain science, intertwined with cases.','Longreads 2014 favorite science stories',sci)]
res=[]
for id,form,title,author,year,venue,url,date,basis,signal,source in rows:
 x={k:None for k in contract['row_fields']};x.update(id=id,field='personal_public_writing',form_id=form,title=title,authors=[author],year=year,venue=venue,stable_url=url,form_basis=basis,form_status='provisional; full text and version review required',selection_signal_type='editorial selection' if 'Longreads' in signal or 'TomDispatch' in signal else 'award or finalist portfolio',selection_evidence=signal,selection_source_url=source,verification_status='live source metadata and selection verified; eligibility provisional',verification_sources=[url,source],date_notes=date,copy_status='not retrieved in this phase; existing inventory dedup required',retrieval_locator=f'{venue}; {date}; {title}; {author}; {url}',why_this_example=basis,limitations='DOI not identified in inspected publisher/selection records; no exhaustive DOI search. Volume, issue number and pages unavailable unless stated in date notes. Award or editorial selection is not readership or citations.');res.append(x)
# source is a later hosted reprint, with issuer named by publisher; do not claim original URL
res[10]['limitations']+=' Original Mosaic URL unresolved; Gizmodo explicitly credits Mosaic; confirm original publication date and version before retrieval.'
res[11]['limitations']+=' Mosaic hosted archive; this is narrative reporting and only a conditional explainer pending full-text screening.'
res[9]['limitations']+=' Reported essay with conceptual explanation; classification remains provisional.'
res[5]['limitations']+=' TomDispatch best-of page is a later version; original title/date and archival version require library verification.'
res[4]['copy_status']='existing inventory: original Gawker URL returned 404; no body retained'
res[3]['copy_status']='existing inventory: original URL returned 403; no body retained'
(p/'candidates.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n')
coverage=[]
for form in contract['forms']:
 id=form['id']; ids=[x['id'] for x in res if x['form_id']==id]
 if ids: status='three_targets'; reason='Three metadata-verified editorial or award selections; full-text form and version screening remains pending.'
 elif id in ('tutorial','procedure_how_to','reference_entry'): status='conditional_analogue';reason='Public-facing service writing exists, but sources and reader tasks differ from the personal/literary context; none established as comparable within this scope.'
 elif id in ('empirical_report','methods_paper','theory_conceptual_paper','case_report','study_review_protocol','narrative_critical_literature_review','scoping_review','systematic_review'): status='not_applicable';reason='Formal research form outside this personal and public literary writing stratum; related disciplinary work belongs in its own context.'
 else: status='conditional_analogue';reason='Actual institutional proposals or decision memos may be public, but no comparable personal/public literary example was verified.'
 coverage.append(dict(form_id=id,status=status,requested=3,provided=len(ids),candidate_ids=ids,reason=reason))
(p/'coverage.json').write_text(json.dumps(coverage,indent=2,ensure_ascii=False)+'\n')
