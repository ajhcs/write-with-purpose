# Migration from the existing rules

Candidate `wwp-debate-0.1.1`. This is a comparison and proposed use path; no canonical skill, installed plugin or historical annotation has been modified. Exact debate lineage is in [decisions.json](../adjudication/decisions.json).

## Skill behavior

| Existing rule or behavior | Candidate behavior | Retained boundary |
| --- | --- | --- |
| `edit-with-purpose/SKILL.md` line12 identifies a particular problem; line16 chooses the smallest set of changes resolving it. The same file already permits substantial rewrites and coordinated changes. | **R01:** separate correction/polish from requested improvement. In improvement, inspect the whole requested work and actively consider a consequential opportunity even when adequate; choose depth before minimizing collateral edits. | Narrow briefs remain narrow. Existing broad-rewrite capability is acknowledged; no claim that the old skill prohibited it. |
| Writing skill/reference recover contribution, missing premises and inference; earlier Astra strategy preserves author ideas and decisions. | **R02:** distinguish stated conclusion, supported connective and proposed new interpretation. When stronger reasoning is requested, test a consequential alternative/boundary, specify what changes and develop the grounded result. | Do not invent premises or treat a model proposal as author belief. A fact or exact preservation obligation is different from a recommendation the author has authorized reconsidering. |
| `structure-and-purpose.md` lines19–21 already attempt the reader task and compare removal, movement and combination. | **R03:** a materially different structure changes a dependency, condition placement or experience. Render decisive prose; check changed rhetorical force as well as facts. Compare at a useful scale, allowing uncertain aesthetic effect. | No two-full-draft requirement, fixed sequence or analytic justification for every creative choice. Author context controls rhetorical purpose. |
| Earlier Astra candidate collects detailed role/target records; subsequent strategy proposes sparse runtime feedback. | **R04:** decide analysis depth using the requested objective and what competing readings would change. | Definition, boundary and reliability research keeps disagreements whether or not an edit differs. Shared prose choices do not establish coding agreement. |
| Existing limits/checks/diff tools and source-fidelity review. | **B03:** retained; only checks on actual final scoped artifacts support claims of mechanical compliance. | No literal lock inferred from an idea; no semantic certification or chat delivery binding implied by a hash. Automatic delivery linkage remains deferred. |
| Existing author feedback, approved style examples, RWT and prior Astra learning sequence. | **B04:** retain choice-linked explanation; practice only when chosen/requested or part of the learning workflow; deliver requested worked solutions directly. | No acceptance-as-learning claim or exercise blocking the writing deliverable. |

The candidate supplements/reorganizes these behaviors for review. Adoption would require a separately scoped skill/plugin revision, with current examples and constraints preserved and its actual implementation verified. This packet is already usable as candidate guidance for the requested development exercise; it is not globally active.

## Twelve function IDs

No category is renamed, removed, merged or added. Each ID maps to itself. Core contribution definitions remain; [coding clarifications](coding-clarifications.md) add explicit presence tests and decision procedures:

| Old ID → candidate ID | Clarification to apply in a new coding pass |
| --- | --- |
| `orient` → `orient` | Preparation target can be local or later; location alone does not count. |
| `define` → `define` | Brief/partial operational meaning can count; success for the reader is separate. |
| `report` → `report` | Retain source, speaker and planned/observed/hypothetical status; reported interpretation is not automatically the current author's interpretation. |
| `assert` → `assert` | Foregrounded proposition at selected speaker level, not every grammatical assertion; retain whether the author endorses it. |
| `support` → `support` | Reason/target connection and adequacy separate; hypothetical logical support can coexist with illustration without becoming empirical evidence. |
| `explain` → `explain` | Develop a relationship, including brief or attributed explanation; neither sequence nor a cause word automatically establishes the job. |
| `illustrate` → `illustrate` | Bind case to idea and preserve epistemic status; overlap with support requires an additional offered connection. |
| `compare` → `compare` | Recover the comparison dimension; mentioning or opposing alternatives alone is insufficient. |
| `interpret` → `interpret` | Identify new inference/significance at the selected discourse level and its basis; faithful recap remains report. |
| `qualify` → `qualify` | Short scope markers may count; identify affected proposition; rebuttal of another's claim is not automatically qualification of one's own. |
| `instruct` → `instruct` | Reader-directed actions may include cognitive actions; incomplete instructions can be present; completed Methods or instructions to a character are not automatically directives to the reader. |
| `narrate` → `narrate` | Temporal development can overlap with other jobs; retain hypothetical status; sequence alone does not automatically add narration. |

These application clarifications do not establish that the taxonomy is exhaustive or optimal. They also inherit much from earlier candidate discussions and the calibration report. Their changed rule version must be retained when new decisions are compared with historical codes.

## Records, relations and measurements

The seven registered relations retain their names. Existing paragraph IDs remain coarse anchors; the candidate representation also allows exact spans, discontinuous span groups and grounded implicit propositions. External roles and relation labels stay in their own namespaces; no 159-entry crosswalk is treated as an automatic relabeling rule or validated paragraph gold.

Preserve historical source bytes, context, codebook version, labels, anchors and unresolved/unknown fields. Add any new candidate assessment separately. Do not convert missing metadata to clarity or convert a diagnostic quote into a complete realization span. Per-instance decisions can differ within a function; paragraph unions are derived summaries, not the primary evidence. New record fields are guidance, not supported behavior of the old validator until an explicit adapter and checks exist.

Observed ranges, working targets and declared limits remain separate. No historical anchor length becomes a function-length profile. Before computing such a profile, establish complete eligible realizations, segmentation, overlap/counting rules, audience/form scope and extraction quality. Better codebook agreement would still not prove reader benefit or author originality.

## Version 0.1 to 0.1.1

The parent froze `0.1` inputs before the eight synthetic development cases. After that execution, a reviewer noted B04 could force an author attempt even when a worked solution was requested. Version `0.1.1` limits attempt-first to chosen practice and explicitly permits the requested worked solution. R01–R04 and coding semantics are unchanged; candidate labels and source hashes were synchronized. The [revision record](../adjudication/revision-0.1.1.json) preserves the old/new guide hashes and the narrow counterexamples.
