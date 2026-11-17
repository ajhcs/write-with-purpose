# Blind long-form author review

16 November 2026. The author requests longer real works and passages from different sections, using GPT-6.1 Terra for all rewrites. Each comparison identifies the Original and presents two rewrites as A and B. Positions change across cases; the condition key stays outside the human review materials until the author requests a reveal.

## Design

Four sources provide sixteen comparisons: the full prose work and exact opening, middle and closing passage windows for each source. Two sources are published Cole Lyons essays; the others provide a contrasting argumentative voice and technical instructional writing. Source URLs, attribution, extraction scope and exact source offsets are retained. Interactive figure text, navigation and unrelated back matter are excluded consistently and documented. Sources are frozen before generation.

Both conditions use frozen skill packages, identical source context and the same substantive-rewrite brief. All generation uses fresh GPT-6.1 Terra contexts with high reasoning effort. Each context receives one source and its four tasks; tasks within a context and source are clustered, not independent observations. Skill selection within the assigned package is part of the condition. No new prompt wording, source facts or expected answer is supplied to only one condition.

The brief authorizes improvements in reasoning, organization and expression, including material restructuring, while preserving the author's contribution, voice, facts, conditions, attribution and temporal context. It asks for roughly comparable reading commitment as a working target, not a hard length limit. Passage rewrites receive the full original context and must fit their unchanged surroundings. They are generated as scoped rewrites, not extracted from a separately reorganized full-work rewrite.

Python code examples are fixed source material; exact content and order are declared mechanical requirements. Third-party prose quotations may be paraphrased with attribution retained. These constraints apply equally to both conditions. No new evidence, memories, sources or retrospective updates may be invented.

## Blinding and preservation

The A/B key is generated once with random assignments before output inspection and kept in a separate control directory. A public hash commitment binds the key without revealing it. Human data contains only source identity, common task, Original, A and B; no skill version, worker path, generation notes, model verdict or key. Client state stores only blind choices and exact human comments. A/B assignment remains stable when the review is reopened.

Workers cannot read another package, another worker's output, previous evaluations or the key. These are instructed boundaries on a shared filesystem, not an operating-system sandbox. Raw generated outputs, supplied source versions and receipts are preserved. Mechanical checks and source-fidelity review are recorded separately; no model ranks the writing for the author. No favorable subset is selected.

Human choices start empty. The author can select Original, A, B, Tie or Neither, identify which rewrite makes a substantive improvement, and comment freely. Preserve exact human wording. The author's earlier general preference is not converted into case-level adjudications or a predicted result for this trial.

## Checks and interpretation

Check source hashes/spans, declared code preservation, output completeness, frozen skill bindings and the absence of condition identifiers from the human packet. Inspect rewrites against their supplied sources for material omissions or unsupported additions, separately from style preference. Keep failed outputs and any bounded repairs distinguishable; never silently edit a rewrite or replace it with a selected favorite.

The review combines quality preference and meaningful gain over the original. It does not reward difference, brevity, extra explanation or added labels by default. Recognition of familiar prose may partially reveal a condition through style; the interface does not disclose it. Multiple tasks share source and worker context. A single paired generation per task cannot isolate a rule's causal effect or establish general superiority. The original is visible and may be preferred.

This is a private author-evaluation exercise. It does not edit or publish the source websites, update globally installed skills, change the frozen canonical packages or retrain a model.
