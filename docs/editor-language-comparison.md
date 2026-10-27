# LanguageTool, Harper and the editor: accepted comparison

27 October 2026. The user accepted this development direction after reviewing the actual writing. Package **0.5.1** publishes the record; writer **0.3.2** and editor **0.2.0** retain the tested instructions and tools.

LanguageTool is the stronger candidate for the next primary diagnostic trial on this corpus. Harper caught a complementary error and offers convenient JavaScript/WebAssembly integration. Both missed errors, and neither engine's suggestions should be applied without checking the complete sentence and its meaning. The grammar engines remain outside the installed skills.

| Observation on 27 fixtures | LanguageTool 6.6 | harper.js 3.0.0 |
| --- | --- | --- |
| Premarked error locations flagged | 12 of 16 | 9 of 16 |
| Valid detections with an unsuitable top replacement | 1 | 0 |
| Unwanted prose flags after two accepted spellings | 0 | 3 |
| Whitespace artifacts from masked code | 2 | 3 |
| Fresh runs returning identical normalized results | 3 of 3 | 3 of 3 |

These are small authored-fixture observations, not general accuracy estimates. The corpus combines 15 prior regression fixtures with 12 new ones; a repeated spelling pair checks Unicode offsets. Sixteen target spans occur in 14 issue fixtures, with 13 controls or context probes. Both engines received identical American-English plain text with fenced code masked by spaces. Each used its own pinned local defaults. LanguageTool cloud AI rules, optional n-gram data, native Markdown comparisons, latency and memory were not tested.

LanguageTool caught two agreement errors Harper missed. Harper caught `there notes` and suggested `their notes`, which LanguageTool missed. LanguageTool located the defect in `Yesterday, the technician calibrate the sensor` but proposed `calibrates`; the ordinary past-tense repair is `calibrated`. Both missed the comma splice, fused sentence and `Three sample` probes.

Harper also flagged legitimate `had had` and technical terms. Its top medical suggestions included `hypoxemia` to `hypoxia` and `bronchiectasis` to `bronchitis's`. Dictionary suggestions are not evidence of equivalent concepts. Accepted spellings `hypoxaemia` and `thermocouple` were declared before execution; a separate filtered view removes exact matching spelling flags only. Two LanguageTool and three Harper whitespace diagnostics came from the code-masking adapter, not prose defects. All raw findings and replacement alternatives remain in the records.

See the [27-fixture ledger](../experiments/editor-language-comparison/all-27-fixtures.csv), [frozen inputs](../experiments/editor-language-comparison/engine-corpus.json), [independent engine review](../experiments/editor-language-comparison/reviews/engine-review.txt), and [grammar investigation](grammar-investigation.md).

## What the editor test measured

Six fresh editors worked on six new passages: four revision cases across engineering, medical, assignment and blog writing, plus two concise controls. All first reader proposals were sealed before any source packet arrived. Each editor then performed its source check. An additional fresh source auditor checked masked prose against sources, two fresh source-blind readers assessed different sets of pairs, and a further fresh reviewer assessed masked engine outputs: ten new task contexts in total. No editor saw either grammar engine's findings.

The three assessments remain separate:

- **Conformance:** compliance with the actual brief and local editing method. Source hashes, exact spans, preservation and reconstruction have mechanical evidence; prose fit remains a judgment.
- **Correctness:** fidelity to the supplied facts, conditions, definitions and attribution. Fidelity to fictional evidence is not independent real-world validation.
- **Usefulness:** recoverable meaning, relevant selection, plain connections, flow and reading effort. Masked model readers supply reasons, not human acceptance.

Every example below is fictional. The blog scenes are not user biography. The final prose is the saved editor output; it was not silently polished after the reviews. Whitespace word counts are descriptive, not reduction quotas.


## 01. Engineering: bypass thresholds

**106 to 36 words.** 3 reader edits and 1 source edits.

**Before**

> The bypass opens when reservoir pressure stays below 160 kPa for two consecutive readings taken 2 seconds apart. It closes after three consecutive readings above 180 kPa. This means that one low reading by itself does not open the bypass, and it is also important to recognize that the closing threshold differs from the opening threshold. In other words, the bypass does not open and close at the same pressure. The display shows the most recent reading, so operators can see the latest pressure value on the display. These details explain the sequence the controller follows when deciding whether the bypass should be open or closed.

**After**

> The bypass opens when reservoir pressure stays below 160 kPa for two consecutive readings taken 2 seconds apart. It closes after three consecutive readings at or above 180 kPa. The display shows the most recent reading.

**Actual changes.** Deleted repeated explanations of the two-reading rule, the different thresholds and the purpose of the note; shortened the display sentence. The separate source pass changed above 180 kPa to at or above 180 kPa.

**Conformance.** Local-edit method verified: three reader edits and one source correction reconstruct the saved final exactly; original preserved. The required conditions remain, without added advice.

**Correctness.** The source pass fixed a material boundary error: exactly 180 kPa must count toward closure. A minor ambiguity remains: the 2-second interval is attached to opening, although the specification applies it to all readings. Stays below can also suggest continuous pressure rather than two sampled values.

**Usefulness.** The masked reader preferred the revision because the operating conditions and display behavior are direct. The remaining timing ambiguity keeps this from being a fully resolved operator instruction.

The display sentence was retained. All required facts remain; the source ledger does not require every specification label to be repeated.

[Original, source, plans and receipts](../experiments/editor-language-comparison/cases/01/)

## 02. Medical: assessment and order status

**102 to 66 words.** 3 reader edits and 1 source edits.

**Before**

> Mira reported feeling light-headed when she stood up. Her blood pressure was 126/78 mmHg while seated and 102/66 mmHg two minutes after standing. The readings were obtained in different positions, so they describe blood pressure in two different positions. A dose reduction was suggested during the review, but no medication order has been entered. It is important to distinguish a suggestion from an order because the suggestion is not itself an order. Mira reported nearly fainting the previous evening, but she did not report losing consciousness. The cause of the symptoms remains unconfirmed; no cause has yet been established in the record.

**After**

> Mira reported feeling light-headed when she stood up. Her blood pressure was 126/78 mmHg while seated and 102/66 mmHg two minutes after standing. A dose reduction was suggested during the review, but no medication order has been entered in the supplied record. Mira reported nearly fainting the previous evening, but she did not report losing consciousness. The cause of the symptoms remains unconfirmed in the record.

**Actual changes.** Deleted the statements that different positions are different positions, that a suggestion is not an order, and the second statement of uncertain cause. The source pass added the record boundary to the order statement.

**Conformance.** Three targeted reader edits and one source insertion verified; original preserved. Readings, posture, timing, suggestion versus order and reported symptoms remain; no diagnosis or treatment advice was added.

**Correctness.** Clinical facts match the fictional ledger. The record boundary is explicit. An inherited source gap remains: the original uses she/her, but the ledger does not specify pronouns. This was not introduced by the edit and was not caught in its source pass.

**Usefulness.** The masked reader preferred the revision: required facts are adjacent and the elementary explanations are gone. Parent judgment: no medication order is recorded could express the same documentary limit more economically; that alternative was not substituted or tested.

Fictional source-fidelity editing only; the test did not validate a diagnosis or clinical decision.

[Original, source, plans and receipts](../experiments/editor-language-comparison/cases/02/)

## 03. Assignment: sampling versus assignment

**103 to 63 words.** 5 reader edits and 4 source edits.

**Before**

> The researchers recruited 80 volunteers from one campus class and randomly assigned them to use one of two study apps. This random assignment means that the study used random sampling, so its findings can be generalized to all university students. Random assignment and random sampling both involve randomness, which is why the distinction between them is important to understand. In this case, the participants were divided randomly between the two apps, with each participant assigned to one app. The study therefore provides information about app performance, and the results should be considered in light of how the participants entered the study. [A, B]

**After**

> The researchers recruited 80 volunteers from one campus class and randomly assigned them to use one of two study apps. [B] This random assignment does not mean that the study used random sampling, which would require selecting participants randomly from the population of interest. [A] Recruiting volunteers from one campus class does not support generalizing any findings to all university students. [A, B]

**Actual changes.** Corrected the false equivalence between random assignment and sampling; deleted repeated allocation language and generic framing. The source pass removed an unsupported performance claim, made findings conditional, and placed [A] and [B] beside their supported claims.

**Conformance.** Five reader edits and four source edits verified. Both required technical terms remain, and the response answers the population-generalization question with the supplied evidence markers.

**Correctness.** The final distinction and generalization limit agree with the definitions and fictional recruitment record. The first reader proposal still asserted app-performance information that the source had not supplied; the separate source pass removed it.

**Usefulness.** The masked reader preferred the revision: study procedure leads to the distinction and then the generalization assessment. That preference partly reflects a corrected conceptual error, so it cannot be attributed to style alone.

The markers [A] and [B] refer to the supplied test packet, not external publications.

[Original, source, plans and receipts](../experiments/editor-language-comparison/cases/03/)

## 04. Blog: the temporary bus stop

**101 to 56 words.** 1 reader edits and 0 source edits.

**Before**

> I missed the replacement bus stop because I followed the large blue sign. It sent me to the usual shelter, which was fenced off for roadworks. A smaller notice at the corner gave the temporary stop’s address, but its arrow pointed back toward the shelter. I walked the block twice before a driver waved me over. This experience illustrates the importance of clear communication in everyday life. Good signs should help people find the places they need to go, and confusing signs can make that harder. In the end, the purpose of a sign is to tell people where to go.

**After**

> I missed the replacement bus stop because I followed the large blue sign. It sent me to the usual shelter, which was fenced off for roadworks. A smaller notice at the corner gave the temporary stop’s address, but its arrow pointed back toward the shelter. I walked the block twice before a driver waved me over.

**Actual changes.** One exact-span deletion removed the three closing lessons. The four scene sentences were retained verbatim. The source check made no further change.

**Conformance.** A deletion only; first-person voice, concrete details and original wording remain. No event, personal history or statistic was added.

**Correctness.** The retained scene agrees with the fictional ledger. Missed the stop is reasonably read as failure to locate it, not evidence that a bus departed.

**Usefulness.** The masked reader preferred the revision. The driver waving the narrator over supplies a concrete ending; the deleted sentences explain a lesson the scene already makes available.

This is invented narrative for the test and is not a story about the user.

[Original, source, plans and receipts](../experiments/editor-language-comparison/cases/04/)

## 05. Concise control: guard, Reset and Start

**34 to 27 words.** 2 reader edits and 0 source edits.

**Before**

> Keep the pump stopped while the guard is open. After closing the guard, press Reset; the pump remains stopped until Start is pressed. Reset clears the interlock, but it does not restart the pump.

**After**

> Keep the pump stopped while the guard is open. After closing the guard, press Reset to clear the interlock; the pump remains stopped until Start is pressed.

**Actual changes.** Inserted to clear the interlock beside Reset and deleted the separate sentence that gave Reset the same explanation. No source correction followed.

**Conformance.** Two local edits verified. Exact button labels, guard condition and close-Reset-Start sequence remain; no step was added.

**Correctness.** Both versions agree with the fictional specification. The revision still states that the pump remains stopped until Start is pressed.

**Usefulness.** The masked reader slightly preferred the revision because the explanation sits beside the action. The original is also sound: its separate warning gives extra emphasis to Reset not starting the pump. No substantial defect needed repair.

Control was a parent design label, not prior user approval or a rule requiring no edits.

[Original, source, plans and receipts](../experiments/editor-language-comparison/cases/05/)

## 06. Concise control: the station scene

**42 to 42 words.** 0 reader edits and 0 source edits.

**Before**

> The rain stopped just before I reached the station. The bench was wet, so I stood under the timetable and watched a porter dry each seat with yesterday’s newspaper. He left the sports pages on the one seat beneath the leaking roof.

**After**

> The rain stopped just before I reached the station. The bench was wet, so I stood under the timetable and watched a porter dry each seat with yesterday’s newspaper. He left the sports pages on the one seat beneath the leaking roof.

**Actual changes.** No change in either stage. Before, reader proposal and final are byte-identical.

**Conformance.** The editor preserved the whole passage rather than manufacturing a revision. No moral, personal history or new event was added.

**Correctness.** The scene and chronology were preserved. The narrower ledger does not independently state the narrator watched, that the wet bench caused the standing choice, or that each seat was dried. These plausible details already occur in the original; the editor did not add them.

**Usefulness.** The masked reader tied the identical versions and found the ending effective without adding a lesson. This is evidence of restraint on one case, not proof that the skill will always leave effective writing alone.

For creative prose the author-supplied scene is evidence too. The ledger gaps should not be turned into a requirement to flatten valid narrative connections. This is invented narrative, not user biography.

[Original, source, plans and receipts](../experiments/editor-language-comparison/cases/06/)

## Interpretation and limits

Masked readers preferred the five changed finals; the byte-identical control tied. The two readers handled different cases, so each pair has one reader judgment. Controls were hidden parent design hypotheses, not passages previously approved by the user.

All saved finals were reconstructed from exact-span plans, with originals and first proposals preserved. The masked source auditor was deliberately not given original identity or change records. Its inability to inspect those records is a masking limitation; the parent verified them separately. The raw audit remains unchanged.

The source pass mattered: the first reader proposals still contained a pressure-boundary error and an unsupported app-performance assertion. Grammar alone would not have established their source fidelity. The final audit also records the engineering interval ambiguity, inherited unspecified pronouns and the narrower narrative ledger. In creative prose the author-supplied scene is evidence too; ledger gaps should not become a rule to flatten valid narrative connections.

This is one editing trajectory per case on parent-authored material, with model reviewers and no matched previous-editor or no-skill writing condition. Fresh contexts reduce shared-history contamination, not shared model-family bias. Corrected factual errors partly explain two pairwise preferences. No clinical or operational decision was validated. Because editors received no engine findings, the prose improvements cannot be credited to LanguageTool or Harper.

## Final direction for this version

Preserve the tested targeted-edit workflow and separate source check. Trial local LanguageTool as an optional primary diagnostic engine in future integration work, with accepted domain vocabulary and reviewed replacements. Keep exact-span changes auditable and reread the complete passage for flow. Mechanical validity, factual support and reader benefit remain separate questions. There is no compulsory engine chain, reduction quota, new vocabulary blacklist or automatic grammar hook in this release.

## Evidence and downloads

- [Full public text/JSON snapshot](../experiments/editor-language-comparison/)
- [Independent source audit](../experiments/editor-language-comparison/reviews/source-review.txt)
- [Masked reader A](../experiments/editor-language-comparison/reviews/reader-a.txt) and [reader B](../experiments/editor-language-comparison/reviews/reader-b.txt)
- [PDF report](https://github.com/ajhcs/write-with-purpose/releases/download/v0.5.1/Comparison-and-Edits.pdf)
- [Editable text and all exact edits](https://github.com/ajhcs/write-with-purpose/releases/download/v0.5.1/Comparison-and-Edits.txt)
- [Original complete evidence bundle](https://github.com/ajhcs/write-with-purpose/releases/download/v0.5.1/Review-Evidence.zip)

The archived text records preserve original local workspace paths for provenance. They are not installation requirements. Workspace reproduction scripts remain in the original evidence ZIP; binaries and npm dependencies are excluded from both the snapshot and the bundle. No personal drafts, source PDFs, credentials or real patient data are part of this comparison.

Official tool documentation: [LanguageTool Java and accepted terms](https://dev.languagetool.org/java-api.html), [local server and cloud-rule distinction](https://dev.languagetool.org/http-server), [harper.js](https://writewithharper.com/docs/harperjs/introduction), and [Harper](https://github.com/Automattic/harper). Terminology references: [NCI hypoxemia](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/hypoxemia) and [NHLBI bronchiectasis](https://www.nhlbi.nih.gov/health/bronchiectasis).
