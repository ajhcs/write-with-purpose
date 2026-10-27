# Deterministic language checks and targeted editing

Investigation date: 27 October 2026.

Deterministic checking is practical for explicit language patterns and exact editing operations. It does not provide a complete decision procedure for good English, faithful claims or enjoyable writing.

## What the precedents establish

[Boeing's Simplified English Checker](https://www.boeing.com/company/simplified-english-checker) describes structural parsing and checks for selected vocabulary, syntax, spelling and punctuation constraints. It supports technical vocabulary extensions and says it does not automatically correct sentences or guarantee full STE compliance. Its parser-based approach is useful precedent; its controlled-language restrictions need not become general writing requirements.

[NASA SP-7084](https://ntrs.nasa.gov/citations/19900017394) takes a functional approach to grammar, syntax and punctuation. It distinguishes required, incorrect and optional punctuation and acknowledges editorial preferences. Turning every recommendation into a mandatory lint would lose those distinctions.

These sources support assistance around the writer's decisions, with different treatment for a mechanical error, a local convention and an editorial choice. The investigation did not establish the current capabilities of a separate Lockheed-specific checker.

## Candidate tools

| Tool | Relevant role | What was checked here |
| --- | --- | --- |
| [Harper](https://writewithharper.com/docs/harperjs/introduction) | Local English spelling and grammar suggestions through a WebAssembly engine. | Executed harper.js 3.0.0 on 15 initial fixtures and a later paired 27-fixture corpus. |
| [LanguageTool](https://dev.languagetool.org/http-server) | Local spelling and grammar diagnostics; the documented local server excludes cloud AI rules. | Executed the 6.6 command-line build on the paired 27-fixture corpus, using Java 17 and default en-US local rules. No server was started. |
| [Vale](https://docs.vale.sh/) | Markup-aware, configurable style and terminology rules. Its own documentation distinguishes this from general grammatical correctness. | Documentation reviewed; not executed. |

No paid or proprietary checker was installed. NASA and STE source documents are not copied into the package.

## First probe: 15 Harper fixtures

The harness in `experiments/grammar` pins `harper.js` to 3.0.0 and its dependency lock. It uses American English and the engine's default rules. A second run imports two accepted domain spellings. The probe runs locally without a model API or a background service.

```text
cd experiments/grammar
npm ci --ignore-scripts --no-audit --no-fund
node probe.mjs
node probe.mjs --custom
```

The installation needs network access; the probes use the installed engine locally. `--out NEW_FILE.json` saves a report without overwriting an existing file. Suggestions are sorted for stable reporting, not ranked as preferred edits.

| Fixture | Default observation |
| --- | --- |
| Misspellings in `The measurment is repeatble.` | Both flagged. |
| Wrong article in `This is a example.` | Flagged. |
| Immediate accidental `the the` | Flagged. |
| Space before a comma | Flagged. |
| `The results is consistent.` | Not flagged. |
| Comma-splice and run-on fixtures | Not flagged. |
| Potential attachment ambiguity | Not flagged; intended meaning also needs context. |
| `hypoxaemia` and `thermocouple` | Spelling flags. Importing the accepted terms removed those flags. |
| Purposeful repetition and a passive with no named actor | No findings in these fixtures. |
| Correct punctuation fixture | No findings. |
| Markdown heading and code fence | Code-fence content excluded; a title-case suggestion appeared for the heading. That is a style proposal. |
| Misspellings after an emoji | Found; source spans required verified conversion from JS UTF-16 positions to Unicode code points. |

The default binary loader hit a Windows file-URL path problem in this environment. Using the package's exported inlined binary resolved it. The harness verifies that each reported span selects the reported source text before converting coordinates.

Three fresh processes returned the same normalized payload hash on these fixtures. That establishes repeatability for this pinned configuration and fixture set. It does not establish recall, precision across disciplines or invariance across engine upgrades.

The false positives and missed syntax problems make automatic correction inappropriate. A usable integration needs accepted domain vocabulary, an explicit dialect, separation of style proposals from errors and review of each proposed replacement. All of those settings must be recorded to make results reproducible.

## Paired comparison: 27 fixtures

The later comparison used the 15 regression fixtures and 12 new fixtures. Both engines received identical plain-text strings in American English, with fenced code masked by spaces. This differs from the native Markdown mode in the first probe. Each engine ran in three fresh processes; all three normalized result arrays matched within each engine.

An independent reviewer assessed all 32 raw diagnostics with engine identity and intended-error labels withheld. The review distinguishes locating an error from proposing a faithful correction.

| Observation on this corpus | LanguageTool 6.6 | harper.js 3.0.0 |
| --- | --- | --- |
| Premarked error locations flagged | 12 of 16 | 9 of 16 |
| Valid detections with an unsuitable top replacement | 1 | 0 |
| Unwanted prose flags after the two declared accepted spellings | 0 | 3 |
| Whitespace diagnostics caused by code masking | 2 | 3 |

LanguageTool caught two agreement probes Harper missed. Harper caught `there notes` and suggested `their notes`, which LanguageTool missed. Both missed the comma splice, fused sentence and `Three sample` probes. LanguageTool flagged `calibrate` after `Yesterday` but proposed `calibrates`, leaving the tense wrong. Harper flagged valid medical terms and offered replacements that changed their meaning.

The accepted spellings were `hypoxaemia` and `thermocouple`, declared before execution. A separate post-filtered view removes spelling findings only when the exact flagged source string matches one of those terms. Raw findings remain available. Whitespace diagnostics inside masked code are adapter artifacts, not ordinary prose errors.

These observations favor LanguageTool as the next primary diagnostic trial. They do not establish product-wide accuracy or a performance winner. The test did not cover LanguageTool cloud AI rules, optional n-gram data, native Markdown comparisons, or latency and memory benchmarks. Domain terms and proposed replacements still need review. No engine hook or new global dependency was installed.

See the [complete comparison, six new editing cases and assessment limits](editor-language-comparison.md), [frozen corpus](../experiments/editor-language-comparison/engine-corpus.json) and [raw independent engine review](../experiments/editor-language-comparison/reviews/engine-review.txt).

## Changes to the editor

Editor 0.2.0 works from existing wording. It identifies a particular defect, tests a deletion where material repeats existing work, then changes a word, phrase, clause or sentence as needed. A connection can require adjacent changes; unaffected language stays in place. Larger restructuring needs an explicit request or an identified organizational problem.

The local-edit tool binds named changes to the original file's SHA-256 and exact source spans. It reconstructs a separate candidate while preserving everything outside the changes. It reports word counts, net reduction, inserted and removed tokens, and the original text selected by each plan. The checks expose scope and expansion; they cannot determine whether a change was worthwhile. No fixed reduction percentage, sentence-length limit or vocabulary blacklist is imposed.

A model can still propose too many individually small changes. The visible edit footprint therefore supports editorial review rather than certifying minimality. A hook could require a receipt at a chosen file-finalization boundary; no such hook has been installed, and direct chat replies are not mechanically gated.
