# Existing annotations compared with our paragraph functions

16 November 2026. This work supports the author's own writing plugin and harness. It downloads source materials and compares their definitions; it does not replace the author interface or the accepted Family → Form → Section model with another product.

The [crosswalk CSV](crosswalk.csv) and [JSON](crosswalk.json) contain **159 original labels, roles and structural categories** across six reviews. There are 87 conditional comparisons, 23 partial overlaps, 12 relation-only categories and 37 categories from which no function inference is supported. These are counts of review entries, not paragraphs or validation results. Some source schemes are only partly compared; [unreviewed labels remain explicit](source-label-gaps.json).

## What the comparison tells us

| Our function | Useful existing distinctions | What we still need to establish |
| --- | --- | --- |
| Orient | GUM background/preparation; AZ background; PERSUADE Lead; README What | Whether the material prepares this reader for the next contribution; opening position alone is insufficient |
| Define | SciDTB definition relations; selected scientific/background descriptions | Whether meaning, scope or distinguishing properties are established for the intended audience |
| Report / describe | AZ OTHER/OWN; MuLMS Results; legal Facts; attributed testimony | Source fidelity, attribution, and planned versus observed status |
| Assert | PERSUADE Position/Claim; scientific aims and hypotheses | Who endorses the proposition; an aim, finding, hypothesis and opponent's position remain distinct |
| Support | GUM evidence links; microtext support edges; PERSUADE Evidence; Webis statistics/testimony | An identifiable claim and connection; many evidence-type labels lack targets, and even labeled evidence can be ineffective |
| Explain | GUM cause/means/purpose; MuLMS EXPLANATION; SciDTB cause/reason | A recoverable mechanism or relationship; MuLMS also includes assumptions and hypotheses |
| Illustrate | SciDTB examples; microtext example-support; Webis anecdotes; DITA examples | What idea is illustrated, whether the case is observed or invented, and whether it also supports a claim |
| Compare / contrast | GUM contrast; AZ contrast; SciDTB comparison; README Why | A meaningful shared dimension; opposition and mentioning alternatives are not sufficient |
| Interpret | Scientific conclusions; legal reasoning; SciPara concluding sentences | New inference or meaning versus faithful recap; conclusion placement does not settle the distinction |
| Qualify | GUM conditions/concessions; scientific limits and assumptions | The affected claim and its scope; rebuttal or an opponent's assertion need not qualify the author's claim |
| Instruct | DITA commands and prerequisites; WLP actions; OpenPI state changes | Reader-directed executable action with appropriate context; completed Methods descriptions ordinarily report |
| Narrate | Webis anecdotes; GUM sequences; legal event histories | Development of events or experience through time; sequence alone is insufficient and authentic personal-writing coverage remains weak |

These are proposed relationships, not equivalences demonstrated by annotation agreement. Each crosswalk record links to definitions, unit, conditions, counterexamples and bounded code checks. Original labels and serialized spellings remain separate, including AZ's `BACKGROUND`/`BKG`, Indian-50 paper acronyms/released names, and PERSUADE's rubric “Concluding summary”/CSV `Concluding Statement`.

## Borrow several layers rather than flatten everything into functions

1. **Family, form and section purpose.** BAWE's purposes/stages, README's eight section roles and DITA's task components can help the author see the shape of a piece. A section can contain multiple functions. A broad register or a header is not a paragraph function.
2. **Passage function.** Scientific and paragraph-discourse guides provide definitions, boundary cases, attribution distinctions and multilabel conventions. Keep full realization spans separate from short evidence quotations and allow functions to span paragraphs.
3. **Relations and provenance.** GUM and microtexts supply directed links, grouping and argument roles. Keep both ends, polarity, opposing voice, missing targets and discontinuous spans. GUM's `span` marker is structural, and microtext undercuts can target an edge rather than a text node.
4. **Procedure structure.** DITA, WLP and OpenPI identify commands, participants, prerequisites and expected state changes. Reuse these as optional task fields and checks; a valid structure is separate from an effective or executable procedure.

This suggests keeping the twelve proposed functions while adding source-specific metadata and explicit relations. The evidence does not yet justify merging functions or adding global categories. In particular, `counterclaim`, `testimony`, `method`, `lead` and `heading` name different kinds of things; they need not become five additional paragraph functions.

## What code can usefully check now

The acquisition and profiling scripts preserve URLs, source revisions, hashes, original labels and distinct counting units. They count actual files and labels, separate excluded README rows and primary/secondary GUM edges, validate some serialized structures, and check PERSUADE offset bounds. The comparison checker can validate known function IDs, source-review hashes and JSON/CSV consistency. None of these checks infers what a passage means.

An eventual adapter can validate IDs and relation targets, offset bounds and text agreement, paragraph overlap, missing prerequisites or expected-result *fields*, explicitly declared author limits, and reproducible word/section counts. It can display a proposed function with its source evidence and ask the author to accept or change it. Semantic success, trustworthy evidence, appropriate vocabulary and executability require contextual judgment.

Local checks found 97 PERSUADE rows whose end offset exceeds the stored text length. Those flags are preserved in [diagnostics](persuade-offset-diagnostics.json); no offsets or labels were silently repaired. Raw MuLMS annotation counts differ from projected sentence counts, and Webis continuation rows require reconstruction. These issues must be resolved or excluded explicitly before function-length measurements.

## Remaining gaps

- **Audience and technical vocabulary:** genre labels do not establish what a particular reader understands. We still need explicit assumed knowledge, a scoped glossary, and checks for first-use explanations and ambiguous terms.
- **Voice and originality:** an annotated corpus is not the author's voice model. Use the author's notes, choices and accepted edits. AcaWriter's configurable rule pattern is useful; its cue-heavy stock sentence stems should not become our drafting defaults.
- **Professional form coverage:** decision memos, proposals, professional business reports and authentic personal/reflective writing need better scoped evidence. Student essays, court decisions and medical abstracts cannot silently fill those gaps.
- **Realization boundaries and reliability:** no imported scheme provides independently validated gold labels for our exact twelve functions. Boundary and label agreement still need a small compatibility pilot before scaling.
- **Observed ranges:** complete eligible documents, source boundaries, audience, discipline, era and selection reasons must be known before estimating lengths or proportions. Observations remain separate from working targets and author-declared limits.
- **Access, format and rights:** a paper or codebook is distinct from its annotated corpus; a source archive can contain only code or rubrics. SciPara's pickle is downloaded but unopened. Code, annotations and original texts retain separate terms.

The next implementation should be a source adapter and review interface inside our own harness: import original annotations, display section purpose and candidate passage functions, retain author decisions, and expose deterministic checks. First test a small mixed sample against our collected professional articles and the author's writing. Use new annotation to test mappings and fill gaps, rather than recreate the existing corpora.
