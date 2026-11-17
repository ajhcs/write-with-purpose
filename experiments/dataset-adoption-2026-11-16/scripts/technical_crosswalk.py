"""Author-reviewed hypotheses for documentation labels; no text classification."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
rows=[]

def add(dataset,label,definition,unit,functions,kind,condition,counterexample,evidence):
 rows.append(dict(dataset=dataset,original_label=label,source_definition_paraphrase=definition,
                  source_unit=unit,proposed_functions=functions,mapping_kind=kind,
                  condition=condition,counterexample=counterexample,definition_evidence=evidence,
                  deterministic_checks='Validate original vocabulary, IDs and structural boundaries; count only declared units. Conditional function meaning needs contextual review.'))

src='https://ctreude.ca/pdf/categorizing-the-content-of-github-2019.pdf#page=9'
readme=[
 ('What','Project purpose and functionality.',['orient','report','define'],'conditional','Determine whether the section introduces context, describes capabilities or establishes meaning.','An About heading alone does not orient.'),
 ('Why','Advantages and explicit comparisons with other projects.',['assert','support','compare'],'conditional','A benefit claim asserts; support needs a claim connection; comparison needs a relevant dimension.','Marketing a benefit does not establish evidence.'),
 ('How','Installation, configuration, usage and other programming-related information.',['instruct','report','define'],'partial','Distinguish reader actions, behavior descriptions and parameter definitions.','A configuration-key inventory is not necessarily a procedure.'),
 ('When','Project status, versions, progress and planned functionality.',['report','qualify'],'conditional','Retain time and planned/completed status; a limitation must attach to a claim.','A version number or date is metadata, not a qualification.'),
 ('Who','Credits, license, contact and conduct information.',['report'],'partial','Prose can report attribution or obligations, while lists and identifiers remain metadata.','A list of author names has no automatic paragraph function.'),
 ('References','Links to documentation, help, translations or related projects.',[],'none','Retain as section/navigation metadata; inspect any surrounding prose independently.','A link is not evidence that supports a proposition.'),
 ('Contribution','How to contribute, fork or clone, and get involved.',['instruct','report'],'conditional','Reader actions can instruct; contributor policies can describe the process.','A link to CONTRIBUTING.md is navigation rather than an executable instruction.'),
 ('Other','Content outside the seven original section types.',[],'none','Keep unresolved content for open review; no function inference follows.','Other does not mean meaningless or bad writing.')]
for label,definition,funcs,kind,cond,counter in readme:
 add('READMEClassifier original human codebook',label,definition,'README section; multiple codes permitted',funcs,kind,cond,counter,src)

src='https://docs.oasis-open.org/dita/v1.2/cd03/spec/common/task2.html'
dita=[
 ('prereq','Conditions or actions required before starting the task.',['qualify','instruct'],'conditional','Separate constraints on a task from actions the reader must perform.','A list of equipment is a prerequisite inventory, not an instruction by itself.'),
 ('context','Context needed to understand the task.',['orient','report'],'conditional','It orients if it prepares this reader for the selected task.','XML element membership does not prove the text provides useful context.'),
 ('steps','Container of ordered steps.',[],'none','Retain hierarchy and order; inspect commands individually.','A container has no independent prose function.'),
 ('step','One step containing its command and optional explanatory material.',[],'none','Keep a composite object; its children may have several functions.','A step object is not one homogeneous paragraph function.'),
 ('cmd','Action performed in a step.',['instruct'],'conditional','The text must communicate an executable action for its intended reader.','An incomplete verb phrase can satisfy a structural field without enabling action.'),
 ('info','Additional information about a step.',['explain','report','qualify'],'partial','Determine what the information contributes to the command or result.','Additional text is not automatically explanatory.'),
 ('substeps','Nested sequence of smaller actions.',[],'none','Keep parent/child and sequencing relationships.','Sequence alone establishes neither causation nor task success.'),
 ('tutorialinfo','Information associated with learning while doing a step.',['explain','illustrate'],'conditional','A tutorial may explain a reason or develop a worked instance.','Learner-directed text can still be a factual aside.'),
 ('stepxmp','Example illustrating a step.',['illustrate'],'conditional','A concrete instance must illuminate the action or concept.','An irrelevant sample is still an example element but fails the reader job.'),
 ('choices','Alternative ways of completing an action.',['instruct','compare'],'conditional','Actions can instruct; comparison additionally needs an explicit meaningful dimension.','Listing choices is not necessarily comparing them.'),
 ('stepresult','Expected outcome of one step.',['report'],'conditional','Describe a predicted outcome and retain its status rather than claim it was observed.','Expected output is not verification that the real action succeeded.'),
 ('result','Expected outcome of the task.',['report'],'conditional','Preserve scope and expected versus observed status.','A results element does not certify an executable procedure.'),
 ('example','Example associated with the task.',['illustrate'],'conditional','It must make a task-related idea or case recoverable.','An unrelated anecdote does not illustrate the task.'),
 ('postreq','Actions to perform after completing the task.',['instruct'],'conditional','State a reader action with enough context.','A vague reminder may not tell the intended reader what to do.'),
 ('stepsection','Expository material among steps, distinguished from an action.',['orient','report'],'partial','Inspect its contribution without converting it into another numbered command.','Its placement between commands does not make it an instruction.')]
for label,definition,funcs,kind,cond,counter in dita:
 add('DITA 1.2 task model',label,definition,'XML task element; not an observed paragraph label',funcs,kind,cond,counter,src)

src='https://aclanthology.org/N18-2016.pdf'
add('WLP 2018','Action','Action predicate marked as a text span.','entity/action character span',[],'none','Use to locate a candidate action within context; reader-directed instruction is a separate question.','A single verb cannot establish that a complete paragraph instructs.',src)
for label in ['Acts-on','Using','Creates']:
 add('WLP 2018',label,'Typed semantic argument linked to an action.','event-to-span argument link',[],'relation_only','Preserve role, source action and argument IDs; use to check that supplied participants exist.','The argument role says nothing about whether the surrounding text teaches or reports a completed method.',src)
add('OpenPI','entity / attribute / before / after','State-change fields tied to a procedural step.','structured state-change tuple',[],'none','Keep task, step and state-transition layers; inspect any proposed explanatory prose separately.','A state tuple is not a paragraph and is not proof that a causal explanation has been written.','https://github.com/allenai/openpi-dataset')

(BASE/'reviews/technical-crosswalk.json').write_text(json.dumps({'status':'Proposed conditional mappings, not validated conversions. Full README codebook and selected DITA/WLP/OpenPI structures only; no claim of exhaustive WLP label coverage.','serialized_readme_codes':{str(i+1):x[0] for i,x in enumerate(readme)},'records':rows},indent=2)+'\n')
text='''# Documentation labels and the paragraph functions

The original README human codebook has eight section roles, while our twelve functions describe work performed by passages. These are different layers. The downloaded CSV has **4,922 rows, including 696 excluded `-` rows**, leaving **4,226 coded section rows**. Original numeric codes 1–8 retain What, Why, How, When, Who, References, Contribution and Other. A classifier's merged What/Why label is a separate artifact.

The [machine-readable comparison](technical-crosswalk.json) covers all eight original README roles plus selected DITA task elements, WLP action/argument structures and OpenPI state fields. Its candidate mappings are contextual hypotheses. Neither headings nor type membership demonstrate successful writing.

- **Reuse section questions:** What does this do? Why use it? How does the reader act? What is its status? Who is responsible? Where are further resources? How can someone contribute?
- **Reuse optional task fields:** prerequisites, context, command, explanation, worked example and expected outcome. Keep complete steps as composite structures rather than force one function onto each.
- **Reuse action and state links:** validate referenced participants, offsets, ordering and supplied outcomes. Reader competence, actual executability and successful explanation still require review.

For a README, manual or tutorial, the harness can show the author section purpose first, then offer function cards for a particular passage. It should preserve the author's answers and wording. Common section labels should provide navigable choices, not mandatory sections or quotas.

DITA is a standard schema, not a measured corpus of successful procedures. WLP marks action/entity spans, and OpenPI supplies step-related state changes. Their source units must not become paragraph functions merely because we can parse them. Business reports, personal reflections and audience-specific vocabulary remain separate research needs.
'''
(BASE/'reviews/technical-crosswalk.md').write_text(text)
print('technical comparison rows',len(rows))
