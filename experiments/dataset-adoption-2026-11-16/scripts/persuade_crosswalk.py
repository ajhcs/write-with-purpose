"""Record original rubric names and exact released CSV labels separately."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
source='https://raw.githubusercontent.com/scrosseye/persuade_corpus_2.0/main/argumentation_effectiveness_rubric.pdf'
values=[
 ('Lead','Lead','Opening that attracts attention and points toward the position.',['orient'],'conditional','It must prepare this reader for the argument; introduction position alone does not establish orientation.','A generic attention-grabber can fail to orient.',1),
 ('Position','Position','Stance addressing the assigned topic.',['assert'],'partial','Identify the stance and its author; a source label includes weak or irrelevant attempts.','A prompt repetition rated as a position may not advance a clear proposition.',1),
 ('Claim','Claim','Point or perspective offered in relation to the position.',['assert','support'],'conditional','Assert if it offers a proposition; support requires its relation to an identifiable position or claim.','A disconnected claim is not support merely because it has this label.',1),
 ('Counterclaim','Counterclaim','Opposing position or objection to the writer\'s position.',['report','assert'],'conditional','Retain opposing voice and target; distinguish reporting an objection from endorsing it.','An objection is not automatically a qualification accepted by the author.',2),
 ('Rebuttal','Rebuttal','Response intended to answer or refute a counterclaim.',['assert','support','interpret','qualify'],'conditional','Record opposition and target; determine whether it reasons, infers or limits a claim.','A dismissal without reasons is not support; a flat rejection is not necessarily qualification.',2),
 ('Evidence','Evidence','Material intended to support a claim, including facts, reasons or examples.',['support','illustrate','report'],'partial','Support requires the identifiable claim and connection; distinguish a reported fact, invented illustration and empirical evidence.','The rubric includes ineffective evidence, which can be irrelevant or unsubstantiated.',2),
 ('Concluding summary','Concluding Statement','Restatement of claims, possibly reconsidered in light of evidence.',['report','interpret'],'conditional','A faithful recap reports; a new implication or inference interprets.','Restating a position does not automatically synthesize new meaning.',3),
 ('Unannotated','Unannotated','Released CSV value outside the seven rubric roles.',[],'none','Keep the span and its unannotated status for open review.','Unannotated does not establish that a span has no communicative function.',None)]
rows=[]
for label,serialized,definition,functions,kind,condition,counter,page in values:
 rows.append({'dataset':'PERSUADE 2.0','original_label':label,'serialized_label':serialized,
              'source_definition_paraphrase':definition,'source_unit':'character span within a school essay; not a paragraph',
              'proposed_functions':functions,'mapping_kind':kind,'condition':condition,'counterexample':counter,
              'definition_evidence':source+('#page='+str(page) if page else ' (CSV inventory, not rubric)'),
              'deterministic_checks':'Check exact released label, essay/discourse IDs, offsets, text alignment and any explicit hierarchy IDs. Do not infer quality or claim targets from role membership.'})
(BASE/'reviews/persuade-crosswalk.json').write_text(json.dumps({'status':'Proposed mappings; source rubric effectiveness scores are not professional writing norms. Concluding summary is the rubric wording; Concluding Statement is the released CSV value.','records':rows},indent=2)+'\n')
print('PERSUADE roles and unannotated value',len(rows))
