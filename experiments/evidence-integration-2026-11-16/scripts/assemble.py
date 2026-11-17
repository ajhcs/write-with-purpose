"""Assemble the seven primary reviews; keep strategy/audit separate from papers."""
from collections import Counter
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
FILES=['audience-readability','interactive-persuasion','funding-persuasion','headlines-attention','narrative-style-impact','genre-moves','agreement-writing-rules']
USE={
'P01':'Make term choice and the reader encounter with explanations explicit; optional mouseovers do not establish comprehension.',
'P02':'Preserve audience viewpoint and interaction context; predictive phrase associations are not prescriptive persuasion edits.',
'P03':'Use proposal purposes and evidence, while separating retrospective prediction from an effect of changing wording.',
'P04':'Offer context-sensitive title alternatives; concreteness has no universal optimum from these historical tests.',
'P05':'Treat processing ease as a reader-related consideration; platform engagement and intentions differ from comprehension.',
'P06':'Allow useful emotional or narrative routes when true and purposeful; sharing is a distinct outcome.',
'P07':'Keep headline metrics scoped; modest held-out winner prediction does not support deterministic lexical rules.',
'P08':'Reuse narrative-rating questions and data as a distinct instrument; journal-confounded citations do not validate our narrate spans.',
'P09':'Compare bundled accessibility approaches while preserving necessary terms and uncertainty; individual ingredients were not isolated.',
'P10':'Allow truthful positive emphasis and check claims; promotional-word associations do not demonstrate a benefit from adding hype.',
'P11':'Respect section, stage and nonlinear variation; no transferable word/sentence target or universal penalty on tentative words.',
'P12':'Consider voice and connecting language in context; small predictive improvements and sentence judgments do not establish whole-piece impact.',
'P13':'Keep negativity/attention optional and purpose-bound; whole headline packages were randomized, individual word effects are model-dependent.',
'P14':'Question familiar style maxims; one-feature citation models are not causal writing advice or a universal inverse recipe.',
'P15':'Preserve empirical-law section variation, blending and recursive moves; heading does not uniquely identify purpose.',
'P16':'Expose findings, interpretation, warrant and recommendation when the decision requires them; retain diverse report structures.',
'P17':'Seed Methods questions from three moves and sixteen steps; do not impose sequence, step quotas or cross-form templates.',
'P18':'Define shared units and multilabel agreement explicitly; separately evaluate boundaries, targets, positive agreement and semantic usefulness.'}
rows=[];candidates=[];review_receipts=[]
for name in FILES:
 p=BASE/'reviews'/(name+'.json');data=json.loads(p.read_text())
 review_receipts.append({'path':str(p.relative_to(BASE)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 for r in data['papers']:
  row=dict(r);row['review_file']=str(p.relative_to(BASE));row['review_report']='reviews/'+name+'.md';row['practical_takeaway']=USE[r['id']];rows.append(row)
 for i,r in enumerate(data.get('proposed_rule_changes',[]),1):
  candidates.append({'review':str(p.relative_to(BASE)),'source_rule_id':r.get('id',str(i)),
                     'id':name+':'+r.get('id',str(i)),'proposal':r})
assert len(rows)==18 and len({r['id'] for r in rows})==18
assert {r['id'] for r in rows}=={f'P{i:02d}' for i in range(1,19)}
assert len({r['doi'].lower().removeprefix('https://doi.org/') for r in rows})==18
rows.sort(key=lambda r:r['id'])
manifest=json.loads((BASE/'source-manifest.json').read_text());sources={r['id']:r for r in manifest['records']}
issues=[]
for r in rows:
 assert Path(r['source_text_path']).exists(),r['id']
 for finding in r['findings']:
  for page in finding.get('pdf_pages',[]):
   if isinstance(page,int):
    assert 1<=page<=sources[r['id']].get('review_pages',sources[r['id']]['pages']),(r['id'],page)
   else:
    assert r['id']=='P14' and str(page).startswith('S1:') and 1<=int(str(page).split(':')[1])<=5,(r['id'],page)
  if not finding.get('pdf_pages'):issues.append({'id':r['id'],'issue':'finding lacks physical PDF page','claim':finding.get('claim')})
result={'status':'Full-text evidence integration; no statistical pooling or canonical rule changes',
        'papers':rows,'source_review_receipts':review_receipts,
        'unique_supplied_works':18,'supplied_pdf_pages':sum(r['pages'] for r in sources.values()),
        'strategy_and_audit':'Separate records, excluded from primary-paper and replication counts',
        'overlap_groups':[{'id':'upworthy','papers':['P04','P07','P13'],'reason':'Shared historical headline-test archive; subsets and pair/bundle construction differ. Not independent corpus replications.'}],
        'missing_finding_page_locators':issues,'reporting_caution_record':'reviews/independent-audit.md; selected source reporting tensions, distinct from missing page locators'}
(BASE/'evidence-map.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
(BASE/'reviewer-candidate-register.json').write_text(json.dumps({'status':'Original proposed implications preserved and namespaced; not all are adopted or independent evidence','candidates':candidates},indent=2,ensure_ascii=False)+'\n')
text='# All eighteen papers: identity, design and useful contribution\n\nSeven thematic reviewers read the full supplied papers. The independent audit checked selected decisive passages; Astra supplied strategy, not a second independent study. Physical PDF page locators, denominators and limitations are in the linked structured reviews and [combined evidence map](evidence-map.json). P02 uses an explicitly identified complete author copy because the supplied attachment has two broken text pages.\n\n| ID | Work | Design | Useful contribution to our harness |\n| --- | --- | --- | --- |\n'
for r in rows:
 title=r['title'].replace('|','/')
 reviewed_pdf=sources[r['id']].get('alternate_copy',{}).get('pdf_path',sources[r['id']]['pdf_path'])
 text+='| '+r['id']+' | ['+title+']('+r['review_report']+') ('+str(r['year'])+'); [DOI](https://doi.org/'+r['doi'].removeprefix('https://doi.org/')+'); [PDF](<'+reviewed_pdf+'>) | '+r['study_kind'].replace('|','/')+' | '+r['practical_takeaway']+' |\n'
text+='\nThe batch includes a headline meta-analysis, a systematic methodological review, randomized comparisons, observational/predictive analyses, descriptive genre studies and an editorial. These are different evidence types. The three Upworthy papers share an archive, and several papers contain multiple designs or nonindependent annotations. No pooled universal style effect is estimated.\n'
(BASE/'paper-index.md').write_text(text)
# Additive source-access updates leave historical limitations intact.
updates=[]
for pid in ['P15','P16','P17','P18']:
 r=next(x for x in rows if x['id']==pid);source=sources[pid]
 updates.append({'paper_id':pid,'title':r['title'],'doi':r['doi'],'previous_scope':'Earlier prior-work map had abstract/preview/method-snippet access only; see historical source records.',
                 'current_scope':'User-supplied full paper read, with source-page review; not a new replication.',
                 'source_pdf':source['pdf_path'],'source_sha256':source['sha256'],'review':r['review_file']})
(BASE/'fulltext-access-upgrades.json').write_text(json.dumps({'scope':'Additive full-text access updates, preserving earlier records and limitations','records':updates},indent=2)+'\n')
print(json.dumps({'unique_works':18,'pages':result['supplied_pdf_pages'],'review_files':len(review_receipts),'reviewer_candidate_records':len(candidates),'missing_finding_page_lists':issues}))
