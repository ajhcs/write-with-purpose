# Development challenges

Eight original synthetic cases exercise correction, substantive improvement, expressive choice, audience adaptation, idea development, source-faithful editing, coding research and explicit limits. These are design probes, not independent evidence of writing improvement or annotation accuracy. The cases contain no real user experiences. [Machine-readable cases](development-cases.json) retain sources, tasks and declared constraints.

## E01 — correction-only

Correct grammar only; preserve the ordering, technical terms, facts and uncertainty. Do not grow the text.

> The sensor does not transmit while the valve is closed. In the current prototype it record pressure every 5 s. We have not tested it outdoors.

## E02 — substantive improvement

Improve the reasoning and recommendation, including structure if useful. Reconsider the requested staffing level if the supplied evidence does not support it; retain the aim of reducing backlog.

> Our backlog increased from 12 to 30 tickets last month. The team closed 18 tickets. We should hire two analysts because the backlog is now 30.

## E03 — expression improvement

Improve flow while preserving the repeated I kept it and the unresolved ending. Do not invent the narrator's experience or explain away their ambivalence.

> I kept the ticket. It proved nothing, and I knew that. Still, I kept it. By morning the address had smudged; the date stayed. I do not know why that mattered.

## E04 — audience improvement

Explain this behavior to a novice who knows what a request and a status are but has not encountered idempotence. Keep the standard term idempotent.

> Retrying this operation is idempotent. Each retry sets the status to Ready. It does not append a record or send a notification.

## E05 — idea development

Develop the author's distinction and improve the paragraph. You may propose an interpretation as a hypothesis or question, but do not turn it into the author's settled belief or add empirical evidence.

> Teams spend too long choosing note apps. An app can store every note and still leave a project stuck. The hard part is deciding what to ask next.

## E06 — source-faithful edit

Improve the Methods passage while accurately reporting what was done. Flag any unsupported rationale or instruction separately; do not invent a source.

> We warmed the samples to 40 °C for 10 min, which improves accuracy. That is why readers should warm their samples too.

## E07 — annotation-research

Analyze the paragraph's functions and relations for coding research, even if no prose edit is necessary. Keep an evidence anchor separate from any complete realization span; allow overlapping readings.

> The proposed rule says that every delayed task is low priority. Consider an urgent approval that arrives on Friday when no authorized person is available until Monday. That possible delay would not establish low priority.

## E08 — bounded improvement

Improve the explanation under a maximum of 45 words. Retain the exact term retry-safe and all material conditions. Do not add facts about causes or tests.

> The operation is retry-safe only while the request identifier remains unchanged. A repeated request returns the existing result. A request with a new identifier starts another operation. We have tested this behavior in the prototype, not in production.

