import json,hashlib,collections
from pathlib import Path
base=Path('experiments/pattern-test-2026-11-16'); x=json.loads((base/'results/coding-agreement.json').read_text()); docs=json.loads((base/'results/documents.json').read_text()); pars={p['id']:(d,p) for d in docs for p in d['paragraphs']}
notes={
'NEJMp1616577-p01':('Opening mixes contextual history, evaluation and recommendation. Whether the past administration sentence is independently substantial reporting is a paragraph threshold decision.','granularity; legitimate multi-function','Clarify a minimum independent contribution and use a paired example; existing report/assert boundaries already cover declaratives.'),
'NEJMp1702362-p01':('A narrated personal episode also makes a general communication problem concrete; both narrative and illustration are plausible.','legitimate multi-function; relational vs intrinsic','Keep both; illustrate requires an identifiable idea or relationship made concrete, not merely a story.'),
'NEJMp1707514-p008':('Brief temporal updates lead into reflection. A sequence of life states can be reporting without necessarily constituting a developed narrative; the closing uncertainty may or may not limit an identifiable claim.','granularity; existing boundary application','Use contrasting report/narrate and qualify examples; require the claim limited, not merely a question.'),
'NEJMp1711886-p001':('A patient history narrates events and introduces a treatment that gains significance from the following article; orientation is relational to subsequent text, while report reflects content.','relational vs intrinsic; context','Keep roles distinct; annotate the later contribution that makes orient operative. Local text alone cannot resolve all relationships.'),
'xml-02282-p013':('The final generalization about study quality explicitly goes beyond the individual estimates and includes a counterexample. The established report/interpret boundary applies.','existing boundary application; legitimate multi-function','Keep both; use inference versus faithful recap as a contrastive example.'),
'xml-02298-p003':('A long paragraph combines data quality framing, a case, process description and exceptions. Added report and orient depend on scope and threshold, not missing concepts.','granularity; legitimate multi-function','Offer a multi-function example with paragraph-level threshold and links to subsequent text.'),
'xml-02359-p003':('The author values patient experience, lists cases and reasons that fragmented care makes a whole-system perspective useful. Assertion, illustration, explanation and interpretation can coexist depending on contribution threshold.','granularity; legitimate multi-function','Keep the functions; illustrate coexisting claim and reason, and distinguish inference from mechanism using paired examples.'),
'xml-02382-p038':('A recommendation to address stigma and its hypothesized effects coexist; calling the final forecast interpretation or assertion depends on whether synthesis or proposed position is the relevant job.','semantic boundary; legitimate multi-function','Clarify assert versus interpret operationally with examples rather than merge them.'),
'customers-004':('Industry examples accompany an explicit transformation claim and a market figure. Illustration and support can coexist if the figure is linked as a reason, regardless of whether it proves the broad claim.','relational vs intrinsic; role vs evidence validity','Retain illustrate and support; code intended evidential link separately from whether evidence justifies the claim.'),
'designing-services-018':('A measured tolerance is converted into an acceptable time. Whether that conclusion counts as inference beyond faithful restatement is close; illustrative status depends on its relation to surrounding method.','existing boundary application; context','Use a near-boundary report/interpret example and record the contextual target of illustration.'),
'house-020':('The authors describe where they place evaluations in a diagram as part of a method. Whether this is instruction for the reader or narration of the authors’ practice depends on surrounding procedural framing.','context; semantic boundary','Clarify instruct as an actionable direction in context, including descriptive first-person method wording; no automatic label.'),
'power-030':('The paragraph mixes a tentative gender-related proposition, a directions example and a proposed mechanism. An example can illustrate a claim even when its evidential basis is weak; qualification requires a limit attached to a claim.','legitimate multi-function; role vs evidence validity','Separate illustration, assertion, explanation and qualification from the strength or truth of the generalization.')}
rows=[];selected=[]; counts={}; first=collections.Counter();second=collections.Counter(); diffs=collections.Counter(); unc=collections.Counter()
for cohort,v in x.items():
 cs=[]
 for c in v['comparisons']:
  d,p=pars[c['id']]; a=set(c['primary']);b=set(c['second']);kind='exact' if a==b else 'subset' if a<b or b<a else 'exclusive'; u=c.get('second_uncertain'); uk='null_or_absent' if u is None else 'explicit_false' if u is False else 'explicit_true' if u is True else 'empty_list' if u==[] else 'nonempty_text_or_list';unc[uk]+=1; diffs[str(len(a^b))]+=1;first.update(a-b);second.update(b-a)
  r={'cohort':cohort,'id':c['id'],'primary':sorted(a),'second':sorted(b),'classification':kind,'primary_only':sorted(a-b),'second_only':sorted(b-a),'symmetric_difference_size':len(a^b),'second_uncertainty':u,'second_uncertainty_category':uk,'text_sha256':p['text_sha256'],'source_sha256':d['source_sha256']};rows.append(r);cs.append(r)
 counts[cohort]=dict(collections.Counter(r['classification'] for r in cs))
 used=set()
 for k in ['subset','exclusive']:
  candidates=sorted((r for r in cs if r['classification']==k),key=lambda r:r['id']); chosen=[]
  for r in candidates:
   doc=pars[r['id']][0]['id']
   if doc not in used: chosen.append(r);used.add(doc)
   if len(chosen)==2:break
  for r in candidates:
   if len(chosen)==2: break
   if r not in chosen:chosen.append(r)
  for r in chosen:
   d,p=pars[r['id']];pr=p['provenance']
   if 'body_text_path' in pr:s=Path(pr['body_text_path']).read_text()[pr['start']:pr['end']]
   else:
    z=json.loads(Path(pr['private_units']).read_text());z=z.get('paragraphs',z.get('units')) if isinstance(z,dict) else z;s=next(u['text'] for u in z if u['id']==pr['unit_id'])
   assert hashlib.sha256(s.encode()).hexdigest()==p['text_sha256']; explanation,cause,action=notes[r['id']];selected.append(dict(r,source_id=d['id'],source_title=d['title'],hash_verified=True,reading=explanation,cause=cause,recommendation=action))
assert len(rows)==138 and len(selected)==12
out={'scope':'138 independently compared targets; labels are interpretations, neither coder is truth','classification_rules':{'exact':'sets equal','subset':'one set is a proper subset of the other','exclusive':'each set contains at least one label absent from the other'},'selection_rule':'Within each cohort, sort IDs lexicographically; select two strict-subset and two exclusive disagreements, preferring source documents not already selected within that cohort; if insufficient, fill in sorted order. No exact cases selected.','counts_by_cohort':counts,'total_counts':dict(collections.Counter(r['classification'] for r in rows)),'symmetric_difference_sizes':dict(diffs),'primary_only_label_occurrences':dict(first),'second_only_label_occurrences':dict(second),'uncertainty_categories':dict(unc),'selected_cases':selected,'all_targets':rows,'inputs_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path('docs/writing-harness/paragraph-functions.json'),base/'results/coding-agreement.json',base/'results/documents.json']},'limitations':'Selection is deterministic but not representative; paragraph readings are not adjudicated truth. Text hashes verify recovered text against recorded provenance, not extraction fidelity or source licensing. No full paragraph text is redistributed.'}
(base/'disagreement-review/diagnosis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['total_counts','uncertainty_categories','symmetric_difference_sizes']},indent=2))
