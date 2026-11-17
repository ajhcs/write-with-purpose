# Proposed joint candidate — awaiting Astra B review

Astra A accepts the following candidate. Astra B has not yet accepted its exact wording. The JSON companion supplies exact unique `old_text`/`new_text` replacements for all six target files; no patch has been applied.

## J01 — Cole-specific example selection

Targets: `skills/write-with-purpose/references/cole-lyons-style.md`, `skills/edit-with-purpose/references/cole-lyons-style.md`

Proposed wording:

> **Let examples develop the argument.** For Cole's prose, avoid illustrative series of more than three items and repeated lists within a paragraph; a shorter list can still be filler. Select the example that advances the point or explain the relationship the inventory stood in for. Do not merely spread the same inventory across sentences. Preserve required coverage and materially distinct reasons, developing or reorganizing them rather than silently dropping them. This is Cole's preference, not a rule for every author's voice.

Evidence: R02 explicitly objects to long and repeated lists. R03 criticizes a pattern containing three items; the precise disliked feature is not isolated.

Limits: No universal author rule or count-based success measure. Required coverage and distinct reasons remain; do not hide inventories across sentences.

IP01: agree on purpose and scope; narrow to profile replacement, no linter or propagated general rule.

## J02 — Compare progression while pursuing stronger arrangement

Targets: `skills/write-with-purpose/references/structure-and-purpose.md`, `skills/edit-with-purpose/references/structure-and-purpose.md`

Proposed wording:

> Compare what the actual versions make recoverable, what they delay and what they might lose. Read a passage with its surroundings: what makes the next claim matter, or prepares the next event or turn? Moving or dividing material can change endorsement, timing or rhetorical force without changing the underlying facts. An unresolved reflection can become an apparent thesis; coordination can become an asserted sequence. Preserve supported relationships while pursuing a stronger arrangement. Choose independently when the brief settles the tradeoff; expose consequential unresolved intent rather than silently deciding a new belief.

Evidence: R03 explicitly praises the speed-to-judgment connection. R11 explicitly prefers original overall story; cadence mechanism remains hypothetical. R09/R10 permit successful splitting/compression; R13 is a technical countercase.

Limits: No ending-specific rule: R11 is not the document ending. No sentence-boundary preservation or correction-first requirement. Current ambition and expression paragraph retained; no added example stacked onto this replacement.

IP02: agree objective; use compact comparison replacement instead of additional contrasting examples or broader obligations.

## J03 — Grounded personal history and author-corrected disclaimers

Targets: `skills/write-with-purpose/references/language-and-meaning.md`, `skills/edit-with-purpose/references/technical-meaning.md`

Proposed wording:

> An argument that “stayed with me from” a report was not necessarily “first encountered” there. Make the useful connection without adding unsupported personal history. A disclaimer is also a claim: follow an author's correction at its supported scope without inferring a credential or experience they have not specified, and retain independent qualifications that still apply. Repair the unsupported relationship while retaining useful changes around it.

Evidence: R05 preferred wording adds unsupported first encounter; source-comparison judgment, not author reason. R01 explicitly disputes an inherited disclaimer; actual generation brief required preservation. R06 demonstrates grounded development from the full source.

Limits: No credential facts added to global profile and no automatic clarification gate. Do not remove independent material qualifications or infer the opposite of a disputed claim. Former/both remains an unresolved scope risk in evidence/tests, not a canonical answer key.

IP03: agree source/context distinction; compact example replaces general caveat instructions, with no blanket deletion of defensive framing.

## Proportional next test — proposal only

{
  "status": "proposal_only_not_run",
  "purpose": "Small diagnostic of isolated candidate changes; not causal performance estimate or adoption proof.",
  "route": "Explicit WRITER; prompt and supplied whole context identical within each pair.",
  "generation_design": "One fresh current-versus-candidate paired generation for each of four fresh tasks. Load only the relevant changed reference in the candidate condition; do not change prompt and reference together.",
  "tasks": [
    {
      "task": "Cole argument with redundant illustrative inventory and required distinct coverage",
      "change": "J01"
    },
    {
      "task": "Argumentative passage with supported reason, developing sequence and a viable alternative arrangement",
      "change": "J02"
    },
    {
      "task": "First-person passage with source-based connection, author-disputed disclaimer, independent material qualification and a harmless paraphrase opportunity",
      "change": "J03"
    },
    {
      "task": "Technical explanation whose representation/sequence distinctions must survive, with no narrative requirement",
      "change": "J02"
    }
  ],
  "review": "Randomize anonymous versions with Original/tie/Unsure options; collect preference separately from substantive improvement and exact helpful/harmful spans. Include a defect-only repair comparator for progression. Independently review source support, retained coverage and new temporal/causal implications before revealing conditions.",
  "failure_signals": [
    "Hidden inventories or omitted distinct reasons.",
    "Conservative rewriting, lost reasoning or invented chronology.",
    "Unsupported biography, invented opposite credential or dropped independent qualification.",
    "Narrative imposed on technical explanation."
  ],
  "follow_up": "Repeat promising or unstable cases before adoption claims; inspect failures rather than automatically expanding guidance. Whole-work and direct EDITOR checks remain separate gaps. Any later former/both ambiguity probe must permit supported resolution or preserved uncertainty, not enforce the audit interpretation."
}

## Agreement provenance

J01 resolves the crossing by retaining the explicit numerical author preference as an avoidance instruction, immediately paired with qualitative selection and anti-gaming. J02 adopts BC02 exactly and withdraws both A02’s longer replacement and AC03’s extra example. J03 adopts BC03, removing the former/both example from canonical text. No more than these three changes are proposed.

B must independently accept, reject or condition J01–J03 and the test plan. Mirroring editor references is a consistency proposal, not observed editor benefit. Original trial limitations and all unrated whole-work cases remain unchanged.
