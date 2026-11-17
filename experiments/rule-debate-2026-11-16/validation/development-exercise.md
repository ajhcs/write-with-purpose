# Eight-case candidate rule development exercise

The candidate was applied to the supplied synthetic development cases. These are debugging examples, not held-out validation, measured reader benefit, or author approval. Guide SHA-256: `operative-rules.md` `3f6703101041e24e33c85a6abacc52a442dee3d4cc3523f7c19ef41370dcf2aa`; `coding-clarifications.md` `d1dfd92374476f03d5b5cd783684f061baa981a898cb75a2f7dbf127cdfc3d06`. The structured duplicate `rules.json` (SHA-256 `d16a838e98f3c8a0b43faa04cdd9c99e26c38fa0595dd5b36a5b89ae621d6e89`) arrived after the first execution and was inspected; both original guide hashes remained unchanged. Structured details and mechanical observations are in [development-exercise.json](development-exercise.json).

## E01

Rules: B01, R01, B03.

The sensor does not transmit while the valve is closed. In the current prototype it records pressure every 5 s. We have not tested it outdoors.

**Change and gain:** Corrected subject-verb agreement; retained sequence, negation, interval and uncertainty.

**Loss or uncertainty:** No material loss identified.

**Comparison:** not needed for a typo

**Semantic review:** Grammar and meaning checked against supplied source, not against device behavior.

**Mechanical observations:** whitespace count 26 (before 26); literal counts does not transmit: 1, 5 s: 1, not tested it outdoors: 1. Preliminary counts await the declared-contract checker.

## E02

Rules: B01, R01, R02, R03, B03.

The backlog rose from 12 to 30 tickets last month because 36 tickets arrived and 18 were closed. The gap shows that incoming work exceeded closures for that month, but it does not establish how many additional analysts are needed. To reduce the backlog, assess the ticket mix, seasonal demand, and the capacity another analyst could add before deciding on staffing.

**Change and gain:** Connected arrivals and closures to the 18-ticket backlog increase; replaced unsupported two-hire conclusion with an evaluation of demand and capacity to guide staffing.

**Loss or uncertainty:** A process recommendation is made, but exact staffing remains unresolved because capacity, mix and seasonality are unknown.

**Comparison:** Hiring two analysts cannot be inferred from the current evidence.

**Semantic review:** Arithmetic 12+36−18=30; whether evaluation will reduce backlog or estimates will be available remains open.

**Mechanical observations:** whitespace count 61 (before 26); literal counts none declared. Preliminary counts await the declared-contract checker.

## E03

Rules: B01, R01, R03, B03.

I kept the ticket. It proved nothing, and I knew that. Still, I kept it. By morning the address had smudged; the date stayed. I do not know why that mattered.

**Change and gain:** Kept the original after comparing the short alternative. Repetition, smudging and the unresolved ending retain their rhythm.

**Loss or uncertainty:** No substantive change; comparison is editorial judgment, not proof of author acceptance.

**Comparison:** “By morning the address had smudged, but the date remained.” Clarifies contrast but adds a more formal rhythm and weakens the original pause.

**Semantic review:** All story details and uncertainty remain; no explanation of the narrator’s motives added.

**Mechanical observations:** whitespace count 31 (before 31); literal counts I kept it: 1, I do not know why that mattered.: 1. Preliminary counts await the declared-contract checker.

## E04

Rules: B01, R01, R03, B03.

This operation is idempotent: retrying it any number of times leaves the status in the same state, Ready. A retry does not append a record or send a notification.

**Change and gain:** Defined idempotence for this operation through the same resulting state and retained both absent side effects.

**Loss or uncertainty:** Only the specified behavior is described; no guarantee about failures or other operations is inferred.

**Comparison:** Omitting the standard term would lose vocabulary the learner needs.

**Semantic review:** Definition is scoped to this operation and repeated requests as provided; semantic fidelity requires human review.

**Mechanical observations:** whitespace count 29 (before 22); literal counts idempotent: 1, Ready: 1. Preliminary counts await the declared-contract checker.

## E05

Rules: B01, R01, R02, R03, B03.

Teams can spend too long choosing note apps. An app can store every note and still leave a project stuck: a complete record does not by itself tell the team what to ask next. Deciding what to ask is the hard part.

**Change and gain:** Made the gap between a complete record and selecting the next inquiry explicit and retained the author’s distinction.

**Loss or uncertainty:** The bridge is an editorial formulation of the given contrast, not an observed empirical result; author acceptance is unknown.

**Comparison:** A broader claim that teams avoid questions because they fear uncertainty would invent a motive.

**Semantic review:** “Can” keeps the opening impression from being presented as a measured population rate; no new evidence or experience supplied.

**Mechanical observations:** whitespace count 42 (before 28); literal counts none declared. Preliminary counts await the declared-contract checker.

## E06

Rules: B01, R01, R04, B03.

We warmed the samples to 40 °C for 10 min.

**Change and gain:** Retained completed warming procedure and removed the unsupported accuracy assertion and reader directive from Methods.

**Loss or uncertainty:** The removed rationale and recommendation are not supported by the supplied study record; a legitimate rationale might exist elsewhere but was not supplied.

**Comparison:** “Warm samples to improve accuracy” would turn an unsupported claim into instruction.

**Semantic review:** A report of what happened is preserved; the record does not support improved accuracy or a general procedure.

**Mechanical observations:** whitespace count 10 (before 22); literal counts 40 °C: 1, 10 min: 1. Preliminary counts await the declared-contract checker.

## E07

Rules: B01, R04, B03.

No prose rewrite requested. Analysis is recorded as competing hypotheses below.

**Change and gain:** Recorded opposed proposition, hypothetical status, logical support target, and overlapping illustrative and directive roles.

**Loss or uncertainty:** No independent coder or gold labels; qualify is an unresolved alternative; anchor spans do not establish full realization.

**Comparison:** Treating the hypothetical scenario as an observed case or as evidence of population frequency.

**Semantic review:** The hypothetical case offers a logical counterexample to a universal proposition, provided the proposed rule does cover this approval scenario. It does not establish that delays have a particular prevalence. Keep candidate readings and attribution separate.

**Coding hypotheses:**

- `report` (hypothesis: present): “The proposed rule says that every delayed task is low priority.” → Proposed universal delay-to-priority rule. Current writer reports a proposed rule; the rule is an opposed position, not the writer’s endorsed assertion. Extent: not_collected.

- `illustrate` (hypothesis: present): “Consider an urgent approval that arrives on Friday when no authorized person is available until Monday.” → Distinction between delay and low priority. Current writer offers a hypothetical approval case. Extent: not_collected.

- `instruct` (hypothesis: present): “Consider an urgent approval” → Reader’s consideration of the hypothetical. Current writer directs reader to consider a case; this is a cognitive action. Extent: not_collected.

- `support` (hypothesis: present): “Consider an urgent approval that arrives on Friday when no authorized person is available until Monday. That possible delay would not establish low priority.” → Writer’s rejection of the proposed universal inference. Current writer offers a possible counterexample as logical reasoning, not an observed incident. Extent: not_collected.

- `assert` (hypothesis: present): “That possible delay would not establish low priority.” → A possible delay does not establish low priority. Current writer advances a bounded objection to the opposed rule. Extent: not_collected.

- `qualify` (unresolved alternative): “That possible delay would not establish low priority.” → Opposed universal rule, if coded as limited rather than rejected. Could be read as limiting a delay-to-priority inference; a rebuttal of the opponent’s rule need not be a qualification of the writer’s claim. Extent: not_collected.

**Mechanical observations:** all six anchors are exact substrings of the source. No complete realization span was collected; exact matching does not establish function presence.

## E08

Rules: B01, R01, R03, B03.

The operation is retry-safe only while the request identifier stays unchanged: a repeated request returns the existing result. A new identifier starts another operation. This behavior was tested in the prototype, not in production.

**Change and gain:** Joined the retry condition to its existing-result behavior and retained the consequence of a new identifier and the prototype-only test.

**Loss or uncertainty:** No cause or production behavior inferred.

**Comparison:** Removing the production qualification would overstate what was tested.

**Semantic review:** Confirm unchanged identifier, result, new-identifier operation and scope manually; a literal match cannot prove them.

**Mechanical observations:** whitespace count 34 (before 38); literal counts retry-safe: 1. Preliminary counts await the declared-contract checker.
