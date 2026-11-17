# Coding clarifications and migration

Candidate guidance for `wwp-debate-0.1.1`; semantic interpretation remains provisional. The twelve function IDs and seven registered relation labels are retained. This appendix clarifies how presence is decided and recorded; it neither overwrites the original catalogue nor recodes historical data. Imported section roles, sentence functions, discourse relations, actors and procedural structures remain in their original namespaces.

## The decision procedure

1. **Identify the task and unit.** In ordinary runtime, inspect the passage or relation needed for an actual choice. For definition, boundary, annotation or reliability research, use its declared units, context, coverage and independent-coding protocol. A paragraph is a container; functions can overlap and cross its boundaries. Record what context was read and the selected narrator or speaker level.
2. **Describe the contribution before tagging it.** Say what the text gives this reader, with the actor, attributed source, addressed reader, and observed/reported/planned/hypothetical status where relevant. An analyst's inferred intent is not a fact about the author.
3. **Decide presence independently of success.** `present` means the passage performs or offers the identified communicative act in context, including an inadequate argument or incomplete instruction. Separately assess whether it is useful, sufficient, source-supported or true when those judgments are requested. Do not remove a support label merely because the offered reason is poor, or assign one merely because an assertion happens to be credible.
4. **Earn additional labels through additional work.** Name the distinct reader-facing job, not an inherited grammatical property. A declarative report is not automatically an argumentative assertion; an instruction is not automatically an explanation. The same words may explain a reason, support a choice and qualify its scope. Do not force a primary label, single-job paragraph or exclusive pair.
5. **Bind relationships.** Identify the exact proposition or contribution supported, explained, illustrated, compared or qualified, and who endorses it. Distinguish quoted/opposed claims from the current writer's position. A target can be local, elsewhere in the source, or a grounded reconstruction of an implicit claim. Missing context is not absence of a target. A plausible but ungrounded target remains unresolved.
6. **Collect the extent needed for the actual objective.** A diagnostic quotation justifies the analyst's reading; it need not cover all words realizing the function. Collect complete realization spans only when the task requires them, with discontinuous and overlapping pieces allowed. An omitted extent is `not_collected`, never zero length. A complete-as-assessed span is an interpretation to review, not a completeness fact proved by matching offsets.
7. **Preserve each instance and the uncertainty.** Keep separate occurrences of one function when they have different sources, targets or decisions. Derive a paragraph's present-label union afterward. In research, retain independently assigned sets and unresolved alternatives before adjudication. In selective runtime, an unmentioned label is unassessed; shared edits or empty sets are not semantic agreement.

## What changes for each retained ID

The original contributions remain the starting definitions. The following presence tests and boundaries are the operative candidate additions; their adequacy questions stay separate.

| ID | Presence test and clarified boundary | Adequacy is a different question |
| --- | --- | --- |
| `orient` | Prepares an identifiable local or later contribution through context, stakes, problem or direction. Record the preparation target when disputed. Opening position alone is insufficient; a transition can orient without a heading. | Is the preparation needed and well placed for this reader? |
| `define` | Establishes a term's meaning, scope, distinction or operation in context. A brief or partial definition can count. An example alone need not define; a usefully defining example may do both. | Does the reader obtain the distinction needed here? |
| `report` | Presents a state, action, result or attributed account. A faithful report of someone else's conclusion remains report at the current writer's level; retain that source's inferential status separately. Planned work and hypothetical descriptions are not completed observations. | Is the account accurate, sufficiently attributed and appropriately complete? |
| `assert` | Foregrounds a position, hypothesis, recommendation or proposition for consideration at the selected speaker level. Do not assign it to every declarative sentence. Reporting an opponent's claim does not make it the current writer's endorsed assertion. | Is its force warranted and its ownership clear? |
| `support` | Offers evidence or reasoning as a reason to accept a recoverable claim. Record that target and the offered connection. Support can be weak, hypothetical or nonempirical. A possible counterexample can logically support rejection of a universal inference without being observed population evidence. Citation presence alone does not count. | Does this reason actually bear on this target, and how strong is it? |
| `explain` | Develops how or why a mechanism, dependency, reason or conceptual relationship holds. It may be brief or attributed. Merely naming a cause, listing capabilities or placing events in order need not make the connection intelligible. | Is the relationship understandable and supported? |
| `illustrate` | Uses an instance, analogy or worked case to make a target idea concrete. Mark its epistemic status. It can also support a claim when a distinct evidential or logical connection is offered. | Does the case clarify without implying unsupported equivalence or frequency? |
| `compare` | Relates alternatives on a recoverable dimension. A contrast need not rank the options; an inventory of alternatives or opposition alone need not compare them. | Is the dimension relevant and the treatment fair? |
| `interpret` | Adds an inference, synthesis, significance or reflection at the selected discourse level. Faithful recap is report. State what was inferred from what. A source's interpretation can be reported without being adopted; explanation and interpretation can coexist when distinct work is done. | Is the inference earned and suitably bounded? |
| `qualify` | Limits a recoverable proposition's scope, force, conditions or application. A small marker can count when its target and effect are clear; it need not fully explain the uncertainty. A rebuttal of someone else's universal rule is not automatically qualification of the author's own claim. | Is the limitation the right one, and is it sufficient? |
| `instruct` | Directs the addressed reader to an action, including a cognitive action such as considering a case when it functions as a directive. An incomplete or unsupported instruction can still be present. Completed Methods reports do not become instructions merely because a reader could imitate them. Track who is addressing whom in dialogue. | Can this reader safely and correctly perform the intended task with the supplied context? |
| `narrate` | Develops an event or experience through time, including hypothetical or nonchronological presentation when marked as such. It can coexist with report, explanation or illustration. A temporal connective or procedural sequence alone does not establish an additional narrative contribution. | Does the sequence convey the intended experience without invented events or a forced lesson? |

These tests refine application; they do not add function quotas or prove that the categories are optimal. Several were already proposed in the earlier Astra candidate. Their inclusion here is inheritance and clarification, not a claim of fresh theoretical invention.

## Report, explain and interpret: a concrete distinction

Synthetic contrast:

- “The team reports that heating improved accuracy” reports a source's causal conclusion. It does not itself develop how heating changes accuracy, and does not establish that the current writer endorses the source's conclusion.
- “In this setup, heating reduces viscosity, allowing the sample to fill the channel more evenly” offers an explanation through a stated mechanism. Whether that mechanism is true is a separate check. If expressly attributed, it may also report another source's explanation.
- “The improvement therefore appears to depend on preparation rather than the detector” offers an interpretation of earlier material. It is not justified merely because “therefore” occurs; inspect the inference and its basis.

These sentences are invented coding examples, not scientific assertions to reuse. A passage may genuinely do more than one of these jobs; boundaries are established by contribution and attribution, not cue words.

## Presence and effectiveness: Methods example

Development case E06 says: “We warmed the samples to 40 °C for 10 min, which improves accuracy. That is why readers should warm their samples too.” The supplied record confirms warming but supplies no accuracy comparison or outside rationale.

The passage reports a completed action, advances an accuracy claim, offers that claim as a reason for a recommendation, and directs the reader. Those functions do not disappear because the rationale is unsupported. Whether the bare causal assertion independently earns `explain` is a contextual question: naming an effect does not necessarily develop a mechanism or reason beyond the offered support. Mark that reading unresolved if the protocol cannot settle it; do not label every “why” phrase automatically. For the requested source-faithful Methods edit, an appropriate candidate is: “We warmed the samples to 40 °C for 10 min.” Separately flag removal of the unsupported accuracy rationale and directive. The edit repairs the reporting task; it is not a recoding that pretends the original never instructed.

## Relation and span representation

Keep the existing relation vocabulary (`supports`, `explains`, `illustrates`, `contrasts`, `qualifies`, `elaborates`, `follows`) and preserve imported relation labels alongside it. Paragraph IDs remain valid coarse targets. Candidate records can additionally point to a span, a discontinuous span group, or an explicitly marked implicit-proposition reconstruction with grounding anchors. Record an opposed proposition separately when needed; do not silently replace the local vocabulary with an upstream attack/undercut scheme.

For E07's hypothetical Friday approval, the scenario may illustrate the distinction between delay and priority and support the author's rejection of the universal inference. The target of that support is the rejection; the universal rule is the opposed proposition. The case is not empirical evidence of how often delays have another cause. “Consider” can direct a cognitive action as an additional local function. These are candidate readings, not a fixed gold set. Research must retain a disagreeing coder's account even if both coders would keep the prose unchanged.

Use exact evidence anchors bound to the source text when recording labels. A separate realization extent states whether it is not collected, partial, unresolved or complete as assessed. For comparative lengths, verify eligible units, extraction, extent completeness and counting conventions before analysis. Overlapping function extents do not form an additive paragraph budget. All locally collected historical evidence anchors remain anchors; none is upgraded to a complete realization by this appendix.

The accompanying [structured guidance](coding-guidance.json) specifies candidate fields and per-ID rules. It is **not** an implemented replacement validator. Existing tools can check their supported IDs, offsets, exact text and hashes; semantic presence, target meaning, full coverage, effectiveness and author acceptance remain unverified by such checks. Old experimental records cannot represent every new per-instance decision and must not be silently coerced into this schema.

## Migration and research implications

Each old function ID maps to itself. Apply these clarified tests only in a newly versioned coding pass. Preserve old labels, context, anchors, rule version and unknown metadata; a new annotation supplements the historical record. The former paragraph-level summary may remain a derived view, but it cannot substitute for per-instance attribution or target decisions. Unknown legacy fields stay unknown, not clear, absent or approved.

Measure boundary agreement, multilabel agreement, target interpretation and task benefit as different questions. Report positive-label counts and shared empty sets; do not turn a better aggregate into correctness. The 21/36 versus 18/36 local result did not demonstrate improvement, and P18's sentence-based human study does not validate these paragraph or span decisions. Its sample recommendations are not universal acceptance thresholds. No numeric function-length targets follow from this candidate.
