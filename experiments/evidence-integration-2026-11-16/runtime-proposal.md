# A concrete first implementation for our own plugin

This is a proposed build, not an installed capability. Keep the existing skills as editorial guidance and add a small local runner, durable writing records and an author-facing section view. One shared engine should handle all selected forms; source confidence and missing evidence remain visible. Implement idea development and targeted revision first, then exercise those paths on contrasting explanatory, reflective and decision-oriented work.

## What we own

1. **Original material and intent.** Preserve notes, the source draft, intended contribution, reader task, necessary concepts and source roles. Keep author-supplied ideas separate from model inferences. Recover settled context from the project and conversation; ask only when missing substance actually blocks the next useful step.
2. **Visible structural choices.** Display Family → Form → Section as meaningful questions and available alternatives. The author can choose, combine or override them. A section can contain several functions without receiving a full coding form, and it need not have a printed heading.
3. **Scoped assistance.** At each step give the model the selected section question, relevant notes, a small set of applicable source-backed distinctions and the author decisions that matter. Keep entire corpora out of routine prompts. Known metadata can filter guidance mechanically; interpreting uncertain purpose or applicability is a model task.
4. **Local revision and concrete checks.** Retain original and candidate text, show the actual diff, run applicable existing checks, and attach each suggestion to the problem it solves. Protect supported meaning and required terms while permitting legitimate paraphrase. A matching number/term set cannot certify fidelity.
5. **Decision history and learning.** Record accepted/rejected choices with their reasons and scope. Explain an edit's functional consequence when teaching is useful. A rejected suggestion should stop recurring without a new reason; one acceptance should not silently redefine the author's global voice.

These are workflow records, not a tenth writing-quality feature. The nine accepted feature groups remain unchanged. Observed ranges, working targets and explicit minimum/maximum limits keep separate fields and meanings.

## A session through the harness

| Step | Model job | Code job | Author contribution |
| --- | --- | --- | --- |
| Recover the thought | Identify a tentative main contribution and a consequential gap | Preserve original notes, sources and current decisions | Correct or develop the idea; supply experience and priorities |
| Choose the route | Offer a few meaningfully different structures and explain their tradeoffs | Retain the chosen map and section IDs | Choose, combine or replace the route |
| Develop one section | Ask a useful missing question or draft the authorized passage | Retrieve only relevant guidance and source material | Add the missing reasoning, observation or example |
| Review the passage | Name a concrete reader problem and show a minimal remedy | Check actual limits, links, spans, terms and diff integrity | Judge intended meaning and voice |
| Finish or learn | Explain a chosen consequence, or retain adequate text | Version the result and invalidate stale receipts | Decide whether it serves the purpose and which choice should persist |

A single conversational model can perform these jobs sequentially. Separate source verification and reader editing in its task instructions. Add an independent review for a consequential ambiguity when authorized, rather than require a reviewer panel for every paragraph. Model reader simulation remains provisional editorial judgment; it is not an actual audience test.

## Example: exposing a structural choice

Synthetic pilot scenario: an author wants to explain why copying an admired paper's wording can obscure their own contribution. The harness first preserves the author's account and identifies the intended reader question. It can offer:

- **Claim-led:** the problem → a supplied example → why it happens → a more useful alternative → a limitation.
- **Experience-led:** an experience supplied by the author → what changed in their understanding → the underlying problem → an unresolved question or alternative.

If no experience has been supplied, the model cannot fill that slot with an invented event. A functional blank asks `[what happened] / [what it showed you] / [what you still think is uncertain]`. For a technical section the blanks instead ask for a concept, relationship, evidence or action. Templates describe contributions rather than provide phrases to copy.

After a draft exists, feedback might identify that a recommendation lacks the criterion connecting it to the evidence, or that a technical term is introduced before its distinction is available. The author sees the exact passage, the proposed local change and the reason. Useful wording can remain unchanged. No global readability score or exhaustive function checklist is required to finish the session.

## Rule and check representation

Each imported rule should retain its source, version, evidence type, form/audience/destination scope, trigger, suggestion, counterexample and check type. Store observations separately from author preferences and declared constraints. A source's original label namespace remains intact in any adapter.

Use code for things it can establish: file versions, IDs, supplied links and targets, offset bounds, declared terms/literals, word budgets and exact diffs. Use a model to assess the meaning of a contribution, a possible missing link or a change in certainty. Use author judgment for intended experience, priorities, acceptable tradeoffs and voice. Preserve uncertainty rather than transform a model's confidence into a quality score.

Reuse existing `check_text.py`, `edit_locally.py` and the bounded source-span checker where they fit. Borrow AcaWriter's configurable feedback pattern, the Research Writing Tutor learning progression and source codebooks through small adapters. Dependency and source-content terms need their own review before a distribution includes them. This proposal does not register services, install hooks or deploy another application.

## Evaluation and stopping

Test the same base model and current skills against the added workflow on fresh, matched author tasks. Preselect practical outcomes: repair work, repeated corrections, independent meaning fidelity, reader task success, voice acceptance and later unaided transfer. Keep those outcomes separate. Record actual usage/timing rather than equate output size with effort. Fix the success criteria before looking at results; no sample-specific threshold from a paper becomes our requirement.

Stop when a passage serves its purpose and no defensible change remains. Retain a supported exception to a style pattern. If context or source evidence is missing, expose the specific gap instead of manufacturing a claim. If several readings work, preserve the choice. A sparse feedback policy must still surface consequential meaning problems; any interface cap is a usability hypothesis, not a writing law.
