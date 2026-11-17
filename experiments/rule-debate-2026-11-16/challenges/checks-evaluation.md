# Round 2 challenges: checks and evaluation

## CE-C01 → EI-05: comparison is evidence of an attempted edit, not of benefit

**Objection.** “Stop after a useful comparison” and “strongest authorized candidate” let the same model propose a version, declare it best and stop without identifying what improved. The supplied colon example changes punctuation but does not demonstrate that a reader better recovers the decision or that the author's voice improves. A self-comparison can be sufficient to make a provisional editorial choice in an ordinary task, but it is not an observed reader gain or author acceptance.

**Failure case.** The model chooses a recommendation-first rewrite because it seems clearer, while omitting an exception the reader needed. It calls the revision useful and stops. A checker's passing word limit will not reveal the lost condition.

**Exact repair.** “For a material authorized change, identify the actual reader problem and compare the original with the changed passage on the relevant recoverable information and any condition, voice or evidence lost. Apply supported improvements, check task constraints, and stop when no specific unresolved issue warrants another pass. Treat this as a provisional editorial judgment; claim measured reader benefit or author acceptance only from the corresponding evidence.” Do not require a second independently generated full draft: a changed passage and its original can be enough; for a typo, direct correction and rereading suffice. When no plausible improvement emerges, leave the original.

**Novelty assessment.** Existing `structure-and-purpose.md` already directs trying concrete alternatives, performing the reader task and keeping model judgment separate from reader performance; writer `SKILL.md` already stops when no further edit has a defensible benefit. EI-05's name is not itself a new mechanism. Its distinctive proposed change is making an improvement request trigger active consideration of a substantial candidate; test that behavioral change against baseline rather than claiming the comparison is new.

## CE-C02 → EI-02: a plausible bridge can create a claim

**Objection.** “Supported premises” and “challenge plausible alternative readings” do not say whether the model has a source-supported inference or is constructing a new proposition. The bridge may be sensible yet exceed the author’s intended claim. Requiring explicit premise mapping for every minor connective would also burden ordinary editing.

**Failure case.** “Pilot missed deadline; vendor had no test environment; defer launch” becomes “The vendor delayed the pilot, so the launch must wait.” Both causal attribution and the necessity of the decision have been added. A numeric or exact-text check may pass.

**Exact repair.** “For an authorized development, make a substantive inferred link explicit only if supplied premises support its force and attribution; preserve possibility where the inference is conditional. If the missing premise would change the conclusion, retain the gap as a question or offer a clearly labeled proposal. Compare the source and changed passage for that link; do not require a separately generated full alternative when a local edit suffices.” For the leaking-window example, keep the stated distinction between administrative status and completed repair; do not infer who caused the delay.

**Novelty assessment.** The existing writing skill already requires explaining a needed inference and preserving attribution and uncertainty; `structure-and-purpose.md` already tells the editor to identify missing premises. EI-02’s useful potential lies in applying those commitments to **authorized thought development** with a bounded comparative test, rather than presenting inference bridges as a wholly new action. Its emphasis on the author’s own thought improves on my CE-01, which could focus too narrowly on task recovery and neglect conceptual development.

## CE-C03 → RL04: countercase and transfer should be contingent on the learning goal

**Objection.** A single countercase can illuminate a decision, but may give a false impression that the author has learned a general principle. A later transfer task requires suitable fresh material, an independently specified criterion and a meaningful opportunity to decline; it is not necessary for ordinary writing. Success on one nearby passage is weak evidence of generalization, and author satisfaction or accepting the edit is not learning evidence.

**Failure case.** The author asks only “Why did you join those sentences?” The model provides an unsolicited lesson and a second task; later the author repeats the wording in a superficially similar passage where the underlying contrast does not hold. The test has rewarded imitation rather than transferable judgment.

**Exact repair.** “If the author requests an explanation or learning support, explain a concrete choice through its reader consequence; include a contrast when it clarifies a transferable distinction. Offer optional practice on different material only if it serves the author’s learning goal. When evaluating learning as a research claim, prespecify the transfer task and criterion, include counterexamples where the move should not be used, and assess delayed unaided performance separately from edit acceptance.” Explain the requested edit directly and do not require a quiz, timed follow-up, second draft or reader experiment to deliver it.

**Novelty assessment.** RL04 itself correctly identifies existing Research Writing Tutor and Astra approaches and does not claim general novelty. Existing editing guidance already uses author feedback and contrastive style examples. Its distinctive candidate is opt-in, task-linked teaching plus a countercase for this workflow, with transfer a separately tested hypothesis. Its explicit focus on learning is stronger than my CE-04, which treats reader task performance and author preference but does not assess whether the author can make a future distinction unaided.

## CE-C04 → RL03: two full candidates are not always needed

**Objection.** “Compare the best local repair with a supported, coordinated revision” can mandate creating two full drafts every time an authorized larger change seems worthwhile; “best” cannot be known without an unbounded search. That overhead risks promoting shallow or speculative alternatives and delaying the actual edit. My own CE-03 has the same potential burden if read as requiring multiple full drafts.

**Failure case.** A three-sentence explanatory passage has a missing antecedent fixed by one clause. The model fabricates a reorganized version merely to satisfy a comparison rule, creating additional scope and voice risks. Conversely, a scattered multi-section argument may genuinely need a coordinated rewrite.

**Exact repair.** “When a local repair leaves a specific consequential reader failure or underdeveloped thought unresolved and the task authorizes broader work, make the smallest meaningful comparison needed: inspect a representative revised passage or a coordinated outline, and materialize the coordinated version when it is plausibly better. Compare its reader consequence and losses to the original or local repair; choose without requiring exhaustive candidates.” This names an intervention reason rather than calling any version definitively best.

**Novelty assessment.** The existing writer skill already compares changes and allows extra explanation; the editor allows coordinated paragraph changes, and explicit substantial rewrites. RL03 adds the operational trigger to examine a broader option when a local fix leaves a named failure unresolved. That is a scoped change to a possibly restrictive default, not a claim that reorganization was previously forbidden.

## Concessions

EI-02 is stronger than CE-01 on substantive conceptual development and separating unsupported causal additions; RL04 is stronger than CE-04 on optional learning and delayed unaided transfer. RL01's locating a specific failed handoff and searching the actual source before repairing it is more concrete than my general instruction to select a reader failure. These are useful merges provided the evaluation and burden limits above remain explicit. None of the proposed mechanisms has yet demonstrated reader gains, learning transfer or an advantage over the existing skills.
