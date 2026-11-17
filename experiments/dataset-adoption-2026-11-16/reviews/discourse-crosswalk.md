# GUM eRST relation crosswalk

16 November 2026. This compares the 32 relations in the [pinned GUM release](https://github.com/amir-zeldes/gum/tree/1d999e5a0327ecb83015007774f6a9be23ecbc41) to the project’s 12 **provisional** functions. The full machine-readable crosswalk, including each source definition, condition, counterexample, target and deterministic check, is [discourse-crosswalk.json](discourse-crosswalk.json). Definitions are paraphrases of [eRST Table A.12](https://aclanthology.org/2025.cl-1.3.pdf#page=42), printed page 64; detailed guidance is in the [GUM annotation guide](https://wiki.gucorpling.org/gum/rst).

These are **semantic hypotheses, not observed mapping coverage or verified paragraph annotations**. eRST links elementary discourse units or grouped spans, with nucleus/satellite roles or multiple nuclei. A paragraph can contain many units, a relation may cross paragraphs, and a nucleus can include many paragraphs. No relation label alone assigns a job to any paragraph. S means satellite and N nucleus below.

| Original relation | Kind | Candidate function(s) and proposed target |
| --- | --- | --- |
| `adversative-antithesis` | conditional | compare (S and N together); qualify (S relative to N) |
| `adversative-concession` | conditional | qualify (S in relation to N) |
| `adversative-contrast` | partial | compare (the nuclei jointly) |
| `attribution-negative` | conditional | report (S and N together) |
| `attribution-positive` | conditional | report (S and N together) |
| `causal-cause` | conditional | explain (S with N) |
| `causal-result` | conditional | explain (N with S); interpret (S relative to N) |
| `context-background` | conditional | orient (S relative to N) |
| `context-circumstance` | conditional | qualify (S relative to N); orient (S relative to N) |
| `contingency-condition` | conditional | qualify (S relative to N); explain (S and N jointly) |
| `elaboration-additional` | conditional | illustrate (S relative to N); report (S relative to N) |
| `elaboration-attribute` | conditional | define (S and the participant in N) |
| `evaluation-comment` | conditional | interpret (S relative to N); assert (S) |
| `explanation-evidence` | partial | support (S as support for N); illustrate (S relative to N) |
| `explanation-justify` | relation_only | None |
| `explanation-motivation` | conditional | instruct (N, with S as motivation); support (S relative to N) |
| `joint-disjunction` | conditional | compare (the nuclei jointly) |
| `joint-list` | relation_only | None |
| `joint-other` | none | None |
| `joint-sequence` | conditional | narrate (nuclei jointly); instruct (nuclei jointly) |
| `mode-manner` | conditional | explain (S and N jointly); instruct (S and N jointly) |
| `mode-means` | conditional | explain (S and N jointly); instruct (S and N jointly) |
| `organization-heading` | relation_only | None |
| `organization-phatic` | none | None |
| `organization-preparation` | conditional | orient (S relative to N) |
| `purpose-attribute` | conditional | explain (S and the participant in N) |
| `purpose-goal` | conditional | explain (S and N jointly) |
| `restatement-partial` | conditional | report (S relative to N); define (S relative to N) |
| `restatement-repetition` | relation_only | None |
| `same-unit` | none | None |
| `topic-question` | conditional | orient (S relative to N) |
| `topic-solutionhood` | conditional | instruct (N relative to S); orient (S relative to N) |

## Adoption and observed evidence

The strongest overlap is `explanation-evidence`: an S span is annotated as evidence intended to increase belief in N. That link is a useful candidate for **support**, with the claim as target; it does not prove relevance, factual accuracy, sufficiency, or that a full paragraph performs that function. `explanation-justify` instead concerns accepting the writer’s right to say N; `explanation-motivation` concerns willingness to act. Keep the three separate. `causal-cause` and `causal-result` identify opposing directions around the more prominent N, so neither can be reduced to an undirected “explains” label.

We inspected the pinned [academic rs4 example](https://github.com/amir-zeldes/gum/blob/1d999e5a0327ecb83015007774f6a9be23ecbc41/rst/rstweb/GUM_academic_art.rs4). Its declared header has exactly the 32 labels listed above; programmatic comparison found no missing or additional labels. The file includes `joint-list` links over author information and research questions, `elaboration-attribute` embedded inside clauses, and four `same-unit` fragments. This is an inspection of one actual annotation, not an empirical estimate of any mapping. The paired source XML includes author names in `<p>` tags, underscoring the need to distinguish document content and front matter before paragraph measurements.

The corpus is an imported annotated relation layer, not a substitute for independently evaluating reader jobs. Store original label, document and node IDs, nucleus/satellite or multinuclear grouping, exact spans, primary and secondary edges, signal links, source version and source rights. `same-unit` marks fragments of one discontinuous EDU and must not be counted as a relation between separate functions. Preserve noncontiguous pieces rather than silently filling the intervening text. Independently align to source XML tokens and record missing, split, or cross-paragraph spans; do not inflate a clause-level link into a whole-paragraph annotation.

Deterministic code can validate declared IDs and labels, graph references, node roles, parse structure, group membership, spans, ordering, signal references and measured overlap with already-aligned paragraph boundaries. It can flag conditional mapping candidates for review. It cannot decide whether a comparison uses a meaningful dimension, a reason supports the claim, a case illustrates an idea, an instruction is executable, or a passage earns an interpretation. Citation presence, a temporal sequence, an attribution, or a header is not sufficient to settle those judgments.

The crosswalk was checked against [paragraph-functions.json](../../../docs/writing-harness/paragraph-functions.json) and [accepted foundations](../../../docs/writing-harness/accepted-foundations.md). Several functions—especially define, illustrate, assert and interpret—have only conditional overlaps with eRST; absence of a dedicated relation does not mean their absence in text. Any adoption test should double-code function spans independently, retain disagreements and unresolved cases, and compare boundaries separately from meanings. No success rate or coverage is claimed.

The corpus annotations are CC BY 4.0; source texts have different licenses, including noncommercial conditions for some genres. Code and text rights require separate checks against the [release license](https://github.com/amir-zeldes/gum/blob/1d999e5a0327ecb83015007774f6a9be23ecbc41/LICENSE.md). GDTB’s shallow relations are partially derived from GUM’s RST graph, so they cannot supply independent validation of this crosswalk.
