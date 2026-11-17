"""Normalize review metadata without relabeling corpus text or proving equivalence."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
FUNCTIONS=json.loads((REPO/'docs/writing-harness/paragraph-functions.json').read_text())
allowed={x['id'] for x in FUNCTIONS['functions']}
SOURCES=[('argument-crosswalk.json','records'),('discourse-crosswalk.json','records'),
         ('scientific-crosswalk.json','rows'),('legal-crosswalk.json','crosswalk'),
         ('technical-crosswalk.json','records'),('persuade-crosswalk.json','records')]
AZ={'BACKGROUND':'BKG','OTHER':'OTH','OWN':'OWN','AIM':'AIM','TEXTUAL':'TXT','CONTRAST':'CTR','BASIS':'BAS'}
MULMS={'MOTIVATION':'Motivation','BACKGROUND':'Background','BACKGROUND/PRIOR WORK':'Background_PriorWork',
       'EXPERIMENTS':'Experiment','EXPERIMENTS/PREPARATION':'Exp_Preparation',
       'EXPERIMENTS/CHARACTERIZATION':'Exp_Characterization','EXPLANATION':'Explanation',
       'EXPLANATION/ASSUMPTION':'Explanation_Assumption','EXPLANATION/HYPOTHESIS':'Explanation_Hypothesis',
       'RESULTS':'Results','CONCLUSION':'Conclusion','ABSTRACT':'Abstract','HEADING':'Heading',
       'METADATA':'Metadata','CAPTION':'Caption','FIGURE/TABLE':'Figure/Table'}
SCIDTB={'Attribution':'attribution','Background: Goal':'bg-goal','Cause-effect: Cause':'cause',
        'Comparison: Comparison':'comparison','Contrast: Contrast':'contrast','Elaboration: Definition':'elab-definition',
        'Elaboration: Example':'elab-example','Explain: Evidence':'exp-evidence','Explain: Reason':'exp-reason',
        'Summary: Summary':'summary','Same-unit: Same-unit':'same-unit'}
README={n:str(i+1) for i,n in enumerate(['What','Why','How','When','Who','References','Contribution','Other'])}
rows=[];checks=[]
for filename,key in SOURCES:
    path=BASE/'reviews'/filename
    review=json.loads(path.read_text())
    checks.append({'path':str(path.relative_to(BASE)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    for index,r in enumerate(review[key]):
        dataset=r.get('dataset','GUM/eRST')
        label=r['original_label']
        candidates=r.get('proposed_functions',r.get('candidate_functions',[]))
        condition=r.get('condition',r.get('necessary_context',r.get('context',r.get('necessary_context_or_counterexample',''))))
        target=r.get('nuclearity_or_role','Original unit; paragraph alignment not assumed')
        normalized=[]
        for c in candidates:
            if isinstance(c,str):normalized.append({'function_id':c,'condition':condition,'candidate_target':target})
            else:normalized.append(c)
        kind=r['mapping_kind']
        # A row explicitly marked no inference is not evidence of every possible function.
        if kind in {'none','relation_only'}:normalized=[]
        assert all(c['function_id'] in allowed for c in normalized),(filename,label)
        definition=r.get('source_definition_paraphrase',r.get('original_definition_paraphrase',r.get('definition','')))
        evidence=r.get('definition_evidence',r.get('definition_source',r.get('definition_url',r.get('definition_source_url',''))))
        evidence=json.dumps(evidence,ensure_ascii=False) if isinstance(evidence,dict) else evidence
        serialized=r.get('serialized_label')
        if dataset=='AZ':serialized=AZ.get(label)
        elif dataset=='MuLMS-AZ':serialized=MULMS.get(label)
        elif dataset=='SciDTB':serialized=SCIDTB.get(label)
        elif dataset=='Indian-50 2019':serialized=r['original_name']
        elif dataset=='READMEClassifier original human codebook':serialized=README.get(label)
        elif dataset=='GUM/eRST' or dataset=='Webis-Editorials-16':serialized=label
        record={'id':f'{filename.removesuffix("-crosswalk.json")}:{index+1:03d}',
                'source_review':str(path.relative_to(BASE)),'source_record_index':index,
                'dataset':dataset,'original_label':label,'serialized_label':serialized,
                'source_unit':r.get('source_unit',r.get('annotation_unit',r.get('unit',''))),
                'original_definition_paraphrase':definition,'definition_evidence':evidence,
                'mapping_kind':kind,'function_candidates':normalized,'condition':condition,
                'counterexample':r.get('counterexample',r.get('necessary_context_or_counterexample','')),
                'computable_checks':r.get('deterministic_checks',r.get('deterministic_check',r.get('computable_validation',''))),
                'status':'proposed_for_contextual_review; not a validated corpus relabeling'}
        rows.append(record)
result={'version':'0.1','purpose':'Review-only label comparison for the author\'s own writing plugin/harness',
        'catalogue_version':FUNCTIONS['version'],'source_reviews':checks,
        'mapping_kinds':{'conditional':'Needs the stated contextual realization and alignment',
                         'partial':'Source class is broader or different; only some instances may overlap',
                         'relation_only':'Preserve structure or relation; no function conversion inferred',
                         'none':'No function inference from this source label'},
        'source_rows':len(rows),'counts_by_dataset':dict(Counter(r['dataset'] for r in rows)),
        'counts_by_mapping_kind':dict(Counter(r['mapping_kind'] for r in rows)),
        'warning':'Candidate union and source-label frequencies are not function coverage, gold paragraph labels, agreement, or validated length ranges. Paper names and serialization are separate. Some schemes are intentionally only partly compared.',
        'records':rows}
(BASE/'crosswalk.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
fields=['id','dataset','original_label','serialized_label','source_unit','mapping_kind','candidate_functions','condition','counterexample','definition_evidence','source_review']
with (BASE/'crosswalk.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    for row in rows:
        out={k:row.get(k) for k in fields};out['candidate_functions']='; '.join(c['function_id'] for c in row['function_candidates']);writer.writerow(out)
# Show unmapped original labels rather than silently calling them missing functions.
profiles=json.loads((BASE/'source-profiles.json').read_text())['profiles']
sci=next(p for p in profiles if p['dataset']=='SciDTB')
covered=set(SCIDTB.values())
gaps={'scope':'Original source labels without a reviewed crosswalk; not evidence that text lacks our functions.',
      'SciDTB_observed_not_compared':sorted(set(sci['relation_counts'])-covered-{'ROOT','null'}),
      'SciDTB_structural_only':['ROOT','null'],
      'GUM_structural_only':['span'],
      'MuLMS_observed_without_AZ_guide_definition':['MEASUREMENT','QUAL_MEASUREMENT'],
      'MuLMS_codebook_name_without_observed_serialization':['SYNTHESIS PROCEDURE'],
      'not_fully_crosswalked':['ECHR sixteen argument types (four illustrative types reviewed separately in legal review)',
                               'WLP entity/event arguments (selected structures only)',
                               'CORE register taxonomy (form layer, not paragraph function)',
                               'BAWE families/stages (form/section layer, not paragraph function)',
                               'Workplace intent and email zones (intent/structure layers)']}
(BASE/'source-label-gaps.json').write_text(json.dumps(gaps,indent=2)+'\n')
print(json.dumps({'comparison_rows':len(rows),'by_dataset':result['counts_by_dataset'],'by_kind':result['counts_by_mapping_kind']}))
