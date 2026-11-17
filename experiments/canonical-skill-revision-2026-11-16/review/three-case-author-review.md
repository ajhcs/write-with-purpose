# Three original output pairs for author review

16 November 2026. These are the original paired outputs behind the two revised preferences and one baseline preference. They are preserved observations, not new generations or outputs after later fixes. One case compares prose, one compares delivery, and one compares coding analysis.

The variants and earlier model preferences have already been disclosed, so this is an informed author review, not a blinded test. These three cases were selected because the model preferred one variant; they are not a representative sample of all writing tasks.

## E04

Explain this behavior to a novice who knows what a request and a status are but has not encountered idempotence. Keep the standard term idempotent.

Original input:

> Retrying this operation is idempotent. Each retry sets the status to Ready. It does not append a record or send a notification.

| Baseline | Revised |
| --- | --- |
| Retrying this operation is idempotent: any number of retries leaves the status at Ready. Each retry sets the status to Ready. It does not append a record or send a notification. | Retrying this operation is idempotent: each retry sets the status to Ready, so any number of retries leaves it at Ready. No retry appends a record or sends a notification. |

Analysis: The revised paragraph connects the repeated operation to its resulting state with “so,” while the baseline states the Ready outcome and then repeats it. This is a modest explanatory improvement. Both preserve the same supplied facts and standard term; it is not a new argument or a major structural transformation.

Full baseline source: [baseline output](../runs/baseline-A/E04/output.txt)
Full revised source: [revised output](../runs/revised-A/E04/output.txt)

## E06

Improve the Methods passage while accurately reporting what was done. Flag any unsupported rationale or instruction separately; do not invent a source.

Original input:

> We warmed the samples to 40 °C for 10 min, which improves accuracy. That is why readers should warm their samples too.

| Baseline | Revised |
| --- | --- |
| We warmed the samples to 40 °C for 10 min.<br><br>**Separate issue-note.txt:**<br>The claim that warming improves accuracy is unsupported: the study did not compare temperature conditions or accuracy, and no external source was supplied. The instruction that readers should warm their samples is also unsupported in this completed-study Methods section. | We warmed the samples to 40 °C for 10 min.<br><br>The claim that warming improves accuracy is unsupported by the supplied evidence: the study did not compare temperature conditions or accuracy effects. The instruction that readers should warm their samples is also unsupported and does not belong in this Methods report. |

Analysis: The publishable Methods sentence is identical. The preference concerns delivery: the baseline saved its unsupported-claim warning separately; the initial revised output placed it after the manuscript text without a label. This is an artifact/presentation difference, not better scientific reasoning or different manuscript prose. Later fixes and focused outputs are separate records.

Full baseline source: [baseline output](../runs/baseline-B/E06/output.txt)
Full revised source: [revised output](../runs/revised-B/E06/output.txt)

## E07

Analyze the paragraph's functions and relations for coding research, even if no prose edit is necessary. Keep an evidence anchor separate from any complete realization span; allow overlapping readings.

Original input:

> The proposed rule says that every delayed task is low priority. Consider an urgent approval that arrives on Friday when no authorized person is available until Monday. That possible delay would not establish low priority.

| Baseline | Revised |
| --- | --- |
| The catalogue permits overlapping functions; the readings below are analytical choices, not mutually exclusive labels. The quoted anchors identify evidence for a reading. Realization spans give the complete text used for that reading.<br><br>- **report** — Anchor: “The proposed rule says”. Realization: “The proposed rule says that every delayed task is low priority.” The sentence reports a proposed universal rule; reporting it does not endorse it. It also **orients** the reader to the proposition under challenge.<br>- **illustrate** — Anchor: “an urgent approval”. Realization: “Consider an urgent approval that arrives on Friday when no authorized person is available until Monday.” This is a hypothetical case, not an observed event or evidence of a population rate.<br>- **interpret** and **assert** — Anchor: “would not establish low priority”. Realization: “That possible delay would not establish low priority.” The sentence draws and asserts a limited inference about the imagined delay.<br>- **support** — Anchor: “every delayed task” and “That possible delay would not establish low priority.” Realization: the entire paragraph. The imagined urgent approval supplies a possible counterexample to the universal rule. This is reasoning from a hypothetical, not empirical case evidence. The scenario and the conclusion may also be read together as **explain**, because they make the challenge to the rule intelligible.<br><br>Relations: The hypothetical scenario **illustrates** a possible delayed urgent task. The final inference **follows** from the scenario and **supports** the challenge to the reported rule; the hypothetical's urgency **contrasts** with the rule's assignment of low priority. These are local analytical readings, not a claim of a complete formal discourse parse. | Context: One paragraph; the proposed rule belongs to its proponent, while the writer challenges it. The approval is hypothetical. Catalogue: paragraph-functions version 0.1, proposed initial catalogue; functions may overlap. The extents below quote the full assessed realization, while anchors are diagnostic excerpts.<br><br>1. report and orient — Anchor: “The proposed rule says”. Realization: “The proposed rule says that every delayed task is low priority.” The writer reports the rule and sets up the challenge; this is not endorsement of the rule.<br>2. illustrate — Anchor: “an urgent approval that arrives on Friday”. Realization: “Consider an urgent approval that arrives on Friday when no authorized person is available until Monday.” This hypothetical instance makes a possible delay involving an urgent task concrete.<br>3. support — Anchor: “That possible delay would not establish low priority.” Realization: “Consider an urgent approval that arrives on Friday when no authorized person is available until Monday. That possible delay would not establish low priority.” The scenario and its stated implication provide a logical counterexample to the universal rule, not an observed case or evidence of frequency.<br>4. assert and interpret — Anchor: “would not establish low priority”. Realization: “That possible delay would not establish low priority.” The writer draws and advances a limited conclusion from the hypothetical scenario.<br>5. instruct — Anchor: “Consider”. Realization: “Consider an urgent approval that arrives on Friday when no authorized person is available until Monday.” The writer directs the reader to consider the case; this overlaps the illustration.<br><br>Relations within the paragraph: the hypothetical illustrates the delay/priority distinction and supports the rejection of the proposed universal rule; the last sentence interprets the hypothetical and contrasts with the rule. The catalogue’s registered relations are defined for paragraph IDs, so these are intra-paragraph analytical relationships rather than registered paragraph-to-paragraph links. A qualification reading is possible if the last sentence is treated as limiting the rule’s application, but it is more directly a rejection of its universal inference, not a qualification of an author-endorsed proposition. No other functions are assessed here. |

Analysis: This task requested analysis, not a rewrite. The revised analysis makes the paragraph-ID limitation explicit, preserves a possible qualification reading and explains a cognitive-instruction reading. Those details help inspection; they do not prove more accurate coding. The disputed instruct label and different support extents remain provisional. This case should not be counted as improved article prose.

Full baseline source: [baseline output](../runs/baseline-A/E07/output.txt)
Full revised source: [revised output](../runs/revised-A/E07/output.txt)

## How the author review will be used

A natural-language response is enough: which version you would use (including tie or neither), what makes the difference, and what you would change. Preserve the author’s exact remarks alongside the source hashes. Keep acceptability separate from meaningful improvement. Do not convert one local preference into a universal rule. No human judgments have been supplied yet.

For later testing, distinguish ordinary correction, substantive idea/structure development and analytical/diagnostic tasks. Compare quality and material difference separately. Prompt wording and examples are candidate interventions to test; these output pairs cannot identify a particular internal memory or weight-space mechanism.

Relevant primary sources: [prompt-format sensitivity study](https://arxiv.org/abs/2310.11324), [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices), and [OpenAI prompting guidance](https://developers.openai.com/api/docs/guides/prompt-engineering).
