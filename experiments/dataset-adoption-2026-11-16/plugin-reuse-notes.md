# How this becomes part of our own plugin

The plugin owns the author's workflow, form profiles, voice decisions, learning prompts and writing files. Imported datasets provide evidence and examples. Imported codebooks provide documented distinctions to test. Existing applications provide implementation patterns; none has been installed as the writing runtime.

A minimal source adapter should retain:

```text
source release and hash
original document ID plus a stable file/row or node locator
source unit and original label namespace
original spans, including discontinuous pieces
source attribution, role, epistemic status and relation targets when supplied
paragraph alignment: known / crosses boundaries / unresolved
candidate harness functions with conditions and provenance
author or reviewer decision, reason and uncertainty
rights for code, annotations and source text separately
```

Family → Form → Section selects the outline choices and section questions. Passage functions describe contributions within that structure. Relations connect contributions. Sentence/word counts, glossary checks and explicit budgets are a separate measurement layer. A form chooses which checks are relevant; it does not declare that every possible function must appear.

The downloaded AcaWriter archive includes 13 `database/seeds/rules/feature_*.json` files with configurable tag checks, conditions and messages, plus code that applies those schemas. That separation is useful to study. Porting a pattern or component still requires attribution and dependency review. Its cue-based interpretations, institution-specific rules and stock sentence stems are not validated defaults for our forms or the author's voice.

For writing with Codex, a useful interaction is: choose a section question → recover the author's relevant thought → offer a small number of structural options → draft or revise with the author → show mechanical checks and unresolved semantic questions. Examples should show a function's contribution and alternatives, while blank templates ask for ideas rather than supply borrowed wording.

The current outputs are acquisition receipts, original-unit profiles and review-only mappings. They are a concrete input to building adapters and a pilot; they are not a trained function classifier, installed plugin, adopted revised codebook or calibrated set of writing limits.
