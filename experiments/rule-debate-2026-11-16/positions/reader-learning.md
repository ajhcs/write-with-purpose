# Round 1: Reader knowledge, language and learning

The biggest change I propose is to **choose the edit that lets the intended reader do the work**, within the author's actual constraints, rather than let minimal change win by default. The current skills already say to recover the reader's question, preserve technical terms, repair connections and protect voice. Those commitments are sound, but their repetition is not a new rule. More specifically, the editing skill's “smallest set of changes” and one-at-a-time language can anchor an authorized improvement to a local repair even when the problem spans several sentences. A correction-only request still calls for a narrow edit; an improvement request can justify a substantial, source-faithful reorganization.

Four mechanisms follow. They are candidate recombinations relative to the inspected baseline, not demonstrated inventions or validated improvements. Details, triggers, model/code/author roles and evaluation plans are in [reader-learning.json](reader-learning.json).

## RL01 — Locate the failed handoff

When a consequential passage asks a reader to understand, decide or act, attempt that specific task at the point where the reader encounters it. Name the missing referent, distinction or link. Search the supplied draft and sources for it; move or explain supported material where needed. If the source does not supply the link, identify exactly what is missing instead of filling it with a plausible premise. Then reattempt the reader task on the actual edited passage. The model's reattempt is a diagnostic, not evidence that the intended audience succeeded; code can bind source pointers and versions but cannot verify meaning.

For example, supplied technical notes establish that parameters are identifiable when observations distinguish their separate effects, and that the current measurement does not distinguish two parameters. Instead of “The parameters are not identifiable. We need another test,” an editor might write: “The current measurements cannot distinguish the effects of the two material parameters, so they do not identify each parameter uniquely. A different test is needed to separate their effects.” This clarifies the reason while making no claim about which test would succeed. A specialist who already knows that relationship may prefer the shorter original; deliberate suspense is not a defect.

## RL02 — Bridge a term to the distinction this reader needs

Keep the technical term when it carries an important distinction. Where a reader must use that distinction and it is not recoverable, place a brief source-supported difference or consequence near the term; compare that actual version with the term alone. For a cross-disciplinary reader, “The parameters are not identifiable: these measurements cannot distinguish their separate effects” retains *identifiable* and supplies the particular distinction needed. The author decides whether the context and term are right. If the concept is unsettled or the explanation is not in the evidence, the model must not invent a definition; if the audience already knows it, the bridge can distract.

Shulman et al.'s P01 experiment found a difference in **perceived fluency**, and optional mouseover definitions were seldom used. It did not establish that inline definitions fail or measure objective comprehension. Pancer et al. P05 cautions that familiarity and precision differ across communities. Ryba et al. P09 tested bundled style variants, not a term bridge in isolation. None proves this proposed mechanism. The existing language reference already recommends natural definitions; the proposed change is a task-specific comparison with the actual term and its consequential meaning.

## RL03 — Compare a local repair with a coordinated rewrite

When substantial improvement is authorized and a local fix leaves a concrete reader failure unresolved, compare the best local repair with a supported, coordinated revision. Evaluate the alternatives on the actual task, meaning, voice and stated limits, and use the stronger permitted result. Signal a consequential change of organization. The model performs the edit; code preserves the source snapshot and checks exact protected items and limits; the author judges intended meaning and voice.

Suppose the author's notes establish that a dashboard marks a repair complete when a request reaches a contractor, while rain still enters a tenant's window. If those facts are scattered across three passages, a supported rewrite can join them:

> The dashboard can show a leaking window repair as complete as soon as the request reaches a contractor. For the tenant, the repair remains unfinished while rain still comes in. The status therefore records a handoff, not a fixed window.

A local synonym change would leave the difference between administrative handoff and physical completion hidden. Conversely, an explicit correction-only request, fixed order, or intentional fragmented voice controls the intervention. This proposal changes the existing “smallest set” default only when the author has authorized improvement and the larger edit has a defensible benefit.

## RL04 — Teach through a choice, optionally

When the author wants to learn or asks for the reason, tie one actual change to the reader's consequence and include a countercase. For the dashboard example: “Putting the two meanings of complete together lets a reader see why the status can mislead. If the preceding sentence already makes that contrast clear, repeating it may be unnecessary.” If learning is a goal, offer a later unaided transfer task on different material. Do not make a lesson, paragraph label or quiz a prerequisite for delivering an ordinary edit.

P17's Methods-section analysis and pedagogical discussion support examining functional alternatives, but do not test this learning interaction. Existing Research Writing Tutor and the project's Astra strategy already combine examples, feedback and transfer, so this is a deliberately scoped proposal for the author's workflow, not a claim of general novelty.

## Evidence and evaluation

P01 measures perceived processing ease under randomized jargon and hover conditions; its serial mediation remains noncausal. P05 combines associations in historical social posts with a randomized test of **intentions**. P09 combines style changes and includes a limited two-item comprehension test; its raw understanding percentages are nonmonotonic, and its confidence reporting is internally inconsistent. These studies support audience-sensitive experiments, not grade thresholds, phrase quotas, removal of necessary hedges, or an equation between fluency and truth.

The existing 36-paragraph calibration produced 21/36 exact-set agreement under original guidance and 18/36 under the richer revision, without semantic gold or complete function spans. It does not establish that these four mechanisms improve labeling, reader performance or writing quality. Compare the same model with existing skills versus the candidate on held-out, author-authorized tasks. Blind independent readers to the arm where practical; measure task performance, source fidelity, preservation of conditions, author recognition of voice, substantive edit acceptance and interaction burden separately. For the teaching mechanism, assess delayed unaided transfer on a different passage. A satisfying model simulation or author click is not proof of learning.
