"""Save scoped integration proposals; never modify canonical writing rules."""
import json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
rows=[]

def add(id,title,disposition,current,proposal,trigger,papers,checks,judgment,counterexample,reuse,local):
 rows.append({'id':id,'title':title,'status':'candidate_for_review; not installed or adopted',
              'disposition':disposition,'current_rule_files':current,'proposal':proposal,
              'trigger_and_scope':trigger,'paper_evidence':papers,'computable_part':checks,
              'semantic_or_author_part':judgment,'counterexample':counterexample,
              'borrowed_components':reuse,'local_evidence':local})

writer='skills/write-with-purpose/SKILL.md';editor='skills/edit-with-purpose/SKILL.md'
foundation='docs/writing-harness/accepted-foundations.md';functions='docs/writing-harness/paragraph-functions.json'
calibration='experiments/rule-calibration-2026-11-16/report.md'
reuse='experiments/dataset-adoption-2026-11-16/comparison.md'
add('C01','Bind language choices to reader knowledge','reaffirm principle; add durable runtime context',[writer,'skills/write-with-purpose/references/structure-and-purpose.md'],
    'Store the reader task, assumed concepts and necessary technical vocabulary. Explain an unfamiliar distinction where this reader needs it, preserving useful exact terms.',
    'An explanation, term or connection may be unfamiliar to the intended reader; reuse settled context instead of asking a questionnaire.',
    [{'id':'P01','pdf_pages':[6,7,9,10,14,15]},{'id':'P05','pdf_pages':[3,5,6,7,8]},{'id':'P09','pdf_pages':[3,4,5,6]}],
    'Check declared vocabulary consistency and locate first uses/linked explanations; counts are observations.',
    'Assess familiarity, explanation sufficiency and technical meaning with this reader in mind.',
    'An expert reference entry can correctly use a specialized identifier without teaching it.',
    ['Scoped glossary and source-term records; README/DITA section roles'],[foundation,reuse])
add('C02','Check how an explanation is encountered','refine reader edit',[writer,'skills/write-with-purpose/references/structure-and-purpose.md'],
    'Treat an available glossary or tooltip as a resource, not proof that a reader encounters or understands a necessary explanation. Consider inline context, an example or a term-first route as alternatives.',
    'A novice-facing passage depends on a concept explained elsewhere.',
    [{'id':'P01','pdf_pages':[7,10,14,15]}],
    'Resolve glossary links and detect presence of declared definitions.',
    'Judge whether the explanation is available at the point of need; evaluate actual reader understanding separately.',
    'P01 tested optional mouseovers; its null effect does not prove inline definitions or glossaries are useless.',
    ['DITA context/prerequisite distinctions; Research Writing Tutor learning/example progression'],[reuse])
add('C03','Keep the intended outcome with every evidence-based suggestion','reaffirm measurement boundary; add rule metadata',[foundation,writer],
    'Attach source scope, measured outcome, baseline and uncertainty to a rule. Use clicks, sharing, citations, awards or perceived ease as explicit task-specific outcomes only when relevant to the author purpose.',
    'Importing a corpus signal or considering a style/attention recommendation.',
    [{'id':'P04','pdf_pages':[5,6,9]},{'id':'P07','pdf_pages':[9,10,13]},{'id':'P13','pdf_pages':[3,4]},{'id':'P08','pdf_pages':[5,8,9]},{'id':'P10','pdf_pages':[5,7,8]}],
    'Filter known scope metadata, retain source/version and declared objective; group overlapping source populations.',
    'Judge applicability and whether a suggested tradeoff serves the author and reader.',
    'A truthful headline experiment may legitimately use click-through as its outcome; it still does not measure comprehension.',
    ['AcaWriter schema/condition/message separation; existing provenance receipts'],[foundation,reuse])
add('C04','Show section jobs and alternative structures','reaffirm accepted hierarchy; implement visible choice',[foundation,'skills/write-with-purpose/references/structure-and-purpose.md'],
    'Use Family → Form → Section to offer purpose-based blanks and alternative arrangements, with blended, recursive and unheaded sections permitted. Do not copy source sentence stems.',
    'Planning or revising a substantial piece; selected source conventions must match its form and discipline.',
    [{'id':'P15','pdf_pages':[5,6,7,8,9,10,11,12]},{'id':'P16','pdf_pages':[10,14]},{'id':'P17','pdf_pages':[6,8,10,15,16]}],
    'Store selected outline and section IDs; validate explicitly required sections and declared budgets.',
    'Judge each section contribution, choose/merge routes and retain useful exceptions.',
    'A Methods-section model is not a template for a methods paper, personal essay or complete business report.',
    ['BAWE purpose/stage metadata','README original eight roles','DITA task components','Cotos three moves/sixteen steps as scoped questions'],[foundation,reuse])
add('C05','Preserve supported force while allowing truthful emphasis','reaffirm fidelity; implement focused change review',[writer,editor,'skills/write-with-purpose/references/language-and-meaning.md'],
    'Review edits that alter certainty, novelty, negation, attribution, comparisons or commitments. Retain supported positive emphasis and meaningful modifiers; a word-list signal alone does not justify deletion or addition.',
    'A proposed edit strengthens or weakens a claim, especially in a proposal, scientific result or recommendation.',
    [{'id':'P10','pdf_pages':[3,5,6,7,8]},{'id':'P11','pdf_pages':[7,8,9,10,11]},{'id':'P14','pdf_pages':[1,2,3,4]}],
    'Diff relevant terms, modals, negations, values and declared protected literals; flag changes as candidates.',
    'Compare full claims and sources; determine supported force, tone and author intention.',
    'A justified correction can remove unnecessary tentativeness; a valid scientific uncertainty cannot disappear to improve a style score.',
    ['Existing local edit/diff measurements and source-bound checks; legal actor attribution'],[calibration,reuse])
add('C06','Evaluate titles against the promised contribution','refine purpose-based title review',[writer,'skills/write-with-purpose/references/structure-and-purpose.md'],
    'Offer title alternatives that make different, truthful tradeoffs in specificity, intrigue and voice. Judge the title alongside the piece and intended reader rather than optimizing a universal lexical formula.',
    'Title or heading creation/revision for a stated audience, form and destination.',
    [{'id':'P04','pdf_pages':[6,9]},{'id':'P07','pdf_pages':[9,10,11,12,13]},{'id':'P13','pdf_pages':[3,4,5]}],
    'Enforce actual character/word ceilings and check required identifiers or headings.',
    'Assess accurate framing, reader expectation and author tone.',
    'A reflective title may leave a question open; an API heading may require exact syntax.',
    ['Optional headline comparison fixture; sentence-concreteness tool as descriptive research candidate only'],[foundation])
add('C07','Use examples and narrative as purposeful options','reaffirm author voice and provenance',[writer,'skills/write-with-purpose/references/cole-lyons-style.md',functions],
    'Develop an author-supplied experience or sourced example when it clarifies the contribution. Offer narrative and non-narrative routes; preserve unresolved endings and distinguish observed, reported and invented cases.',
    'An actual experience or concrete case helps the selected section job.',
    [{'id':'P06','pdf_pages':[8,9,10,11,12]},{'id':'P08','pdf_pages':[5,8,9]},{'id':'P12','pdf_pages':[4,5,8,9,10,11]}],
    'Retain provenance and links from an example to its target; preserve author decisions.',
    'Judge what the case illuminates and whether its voice and generalization fit.',
    'A reference lookup can be complete without a story; an emotional anecdote does not prove a population rate.',
    ['Webis anecdote metadata','GUM example/sequence relations','P08 narrative-rating questions as a distinct instrument'],[functions,reuse])
add('C08','Keep surface metrics descriptive unless a real constraint applies','reaffirm existing rule',[foundation,'skills/write-with-purpose/references/checks.md',editor],
    'Display relevant counts or observed distributions with their units and scope. Enforce only actual author/task/destination limits; do not turn associations or averages into prose-quality quotas.',
    'A readability, length, hedge, modifier, pronoun or vocabulary score is offered as a reason to edit.',
    [{'id':'P05','pdf_pages':[3,5,6,7,8]},{'id':'P09','pdf_pages':[3,4,5]},{'id':'P11','pdf_pages':[7,8,10,11]},{'id':'P14','pdf_pages':[1,2,3,4]}],
    'Run the existing declared-limit checker with pinned count convention and delivered-file hash.',
    'Assess whether the original or proposed prose better serves this purpose and retains meaning.',
    'An actual publisher word ceiling is binding even if longer abstracts correlate with citations.',
    ['Existing check_text.py; imported count implementations after compatibility checks'],[foundation,calibration])
add('C09','Retain who says what and how contributions connect','refine source representation',[functions,writer],
    'Keep passage function, evidence type, speaker/actor, argument role and relation target distinct. A source label supplies a lens for review; validate the actual link and preserve missing or ambiguous targets.',
    'Support, qualification, reported opposition, comparison or a disputed inference is material to the draft.',
    [{'id':'P02','pdf_pages':[2,5,6,7,8]},{'id':'P16','pdf_pages':[10,14]},{'id':'P18','pdf_pages':[7,11,12,13]}],
    'Validate original node/span IDs, endpoint types, offsets and supplied target references.',
    'Judge evidential relevance, attribution, meaningful comparison and target scope.',
    'Reporting an opponent statement is not author endorsement; a statistic without a claim link is not automatically support.',
    ['GUM directed/secondary relations','microtext edge-to-edge undercuts','legal actors','ConvoKit reply/context metadata'],[calibration,reuse])
add('C10','Measure labels, spans and reader benefit separately','refine research protocol, not routine prose',[calibration,functions],
    'For the next frozen coding pilot retain exact sets, set overlap, positive agreement, prevalence, unresolved states and target judgments. Keep evidence anchors separate from full realization spans and test boundaries independently.',
    'Research calibration or function-length measurement; do not impose complete annotation on ordinary writing.',
    [{'id':'P18','pdf_pages':[6,7,10,11,12,13,14]}],
    'Compute declared set distances and appropriate chance-corrected statistics only from comparable units and explicit missingness rules.',
    'Review semantic correctness, boundary completeness and source-target meaning; agreement is not accuracy.',
    'The paper’s 750-unit behavior is specific to its sample, not our acceptance criterion; identical empty labels are not positive reliability.',
    ['Original annotation-unit schemas and independent-coder workflows'],[calibration,reuse])
add('C11','Give only assistance that resolves the current writing problem','new runtime hypothesis; no claimed empirical win',[writer,editor,calibration],
    'Retrieve the relevant section guidance and surface a small number of consequential choices or minimal edits. Use detailed function records for actual ambiguities and offline research; retain an adequate passage when no benefit is identified.',
    'Routine drafting or editing after purpose and material are known; teaching detail follows the author need.',
    [{'id':'P17','pdf_pages':[15,16]},{'id':'P18','pdf_pages':[12,13,14]}],
    'Persist selected context, exact diffs, source versions and unresolved findings; invalidate receipts after changes.',
    'Choose which issue matters, explain its consequence, and evaluate whether an edit has a defensible benefit.',
    'A safety-critical meaning error must not be hidden by a cosmetic feedback-count cap; a narrow copy edit needs no outline quiz.',
    ['AcaWriter configurable feedback pattern','RWT learning/examples/feedback progression','existing local edit tools'],[calibration,reuse])
add('C12','Preserve the author thought and scope of accepted decisions','new durable workflow hypothesis; existing voice principle',[writer,editor,'skills/write-with-purpose/references/cole-lyons-style.md'],
    'Save original notes before paraphrasing; distinguish supplied ideas, source evidence and model inference. Retain accepted/rejected structural and wording choices with reasons and scope, using them for the current piece and future relevant tasks.',
    'Writing from notes, eliciting an unstated connection, or incorporating author feedback across drafts.',
    [{'id':'P17','pdf_pages':[15,16]},{'id':'P02','pdf_pages':[5,6,7,8]}],
    'Version original/candidate/decision records, maintain source links and enforce actual preservation constraints.',
    'Author supplies lived experience, priorities and voice choices; a local acceptance is not a global preference or proof of factual truth.',
    'Silence is not approval; an accepted phrase for a personal essay need not fit a Methods section.',
    ['Our existing approved/rejected example practice; source adapters supply evidence rather than author identity'],[foundation,calibration,reuse])

for r in rows:
 for name in r['current_rule_files']+r['local_evidence']:assert (REPO/name).exists(),name
result={'status':'Integration proposals, not canonical rule edits or installed runtime',
        'purpose':'Reaffirm sound prose principles and identify executable workflow additions with explicit scopes',
        'candidates':rows}
(BASE/'rule-decision-ledger.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
text='# Rule decisions from the supplied evidence\n\nThese twelve integration proposals preserve the existing skills and accepted foundations. They are not twelve new universal prose rules. Several reaffirm existing guidance; the main additions concern durable context, source scope, visible structural choices and measured review behavior. [Full records](rule-decision-ledger.json) include source pages, current files, triggers, counterexamples and the model/code/author boundary.\n\n| ID | Decision | Disposition |\n| --- | --- | --- |\n'
for r in rows:text+='| '+r['id']+' | '+r['title']+' | '+r['disposition']+' |\n'
text+='\nHard enforcement belongs to explicit task constraints and mechanically verifiable structure. Source-derived associations provide conditional review guidance. Author preferences retain their own authority and scope; they need not be justified by a population study. The model evaluates uncertain meaning and applicability; the author controls intended substance and voice. No proposed rule is supported merely because its proxy predicts popularity.\n'
(BASE/'rule-decisions.md').write_text(text)
# A contemporaneous read-only snapshot; not described as a pre-experiment freeze.
paths=sorted({p for r in rows for p in r['current_rule_files']+r['local_evidence']})
(BASE/'comparison-baseline-hashes.json').write_text(json.dumps({'scope':'Read-only comparison snapshot at integration time; not a new randomized-experiment freeze.','files':[{'path':p,'sha256':hashlib.sha256((REPO/p).read_bytes()).hexdigest()} for p in paths]},indent=2)+'\n')
print('Saved',len(rows),'scoped integration proposals')
