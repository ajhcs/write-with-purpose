# Legal role crosswalk for the writing harness

The 13 BUILD labels and seven Indian-50 labels are **sentence-level judicial annotations**, not gold paragraph functions. The [machine-readable crosswalk](legal-crosswalk.json) preserves every original label, a source-linked definition, proposed function IDs, conditional context, a counterexample and structural checks. No mapping has been validated or adopted. All candidate functions refer to the project’s proposed `paragraph-functions.json`; a label is never enough on its own.

The greatest reusable design element is **separating attribution from function**: ECHR distinguishes five actors from sixteen types of legal argument on the same token spans. A report of an opposing position is not an endorsement; a court order is an institutional act, not automatically `assert`. A quoted statute does not automatically `instruct` the reader. A citation may report a prior case, support a specified claim, or compare cases depending on context. ECHR does not annotate support/attack edges between spans; do not invent relation targets.

| Source | Original label | Candidate functions | Mapping |
| --- | --- | --- | --- |
| BUILD | Preamble (`PREAMBLE`) | `orient`, `report` | partial |
| BUILD | Facts (`FAC`) | `report`, `narrate` | conditional |
| BUILD | Ruling by Lower Court (`RLC`) | `report`, `explain`, `support` | conditional |
| BUILD | Issues (`ISSUE`) | `orient` | partial |
| BUILD | Argument by Petitioner (`ARG_PETITIONER`) | `report`, `assert`, `support` | conditional |
| BUILD | Argument by Respondent (`ARG_RESPONDENT`) | `report`, `assert`, `support` | conditional |
| BUILD | Analysis (`ANALYSIS`) | `report`, `interpret`, `explain`, `support`, `compare`, `qualify` | conditional |
| BUILD | Statute (`STA`) | `report`, `define`, `interpret`, `support` | conditional |
| BUILD | Precedent Relied (`PRE_RELIED`) | `report`, `support`, `compare`, `interpret` | conditional |
| BUILD | Precedent Not Relied (`PRE_NOT_RELIED`) | `report`, `compare`, `qualify`, `interpret` | conditional |
| BUILD | Ratio of the decision (`Ratio`) | `support`, `explain`, `interpret` | conditional |
| BUILD | Ruling by Present Court (`RPC`) | `report`, `interpret` | partial |
| BUILD | NONE (`NONE`) | none inferred | none |
| Indian-50 | Facts (`FAC`) | `report`, `narrate` | conditional |
| Indian-50 | Ruling by Lower Court (`RLC`) | `report`, `explain`, `support` | conditional |
| Indian-50 | Argument (`ARG`) | `report`, `interpret`, `compare`, `support` | conditional |
| Indian-50 | Statute (`STA`) | `report`, `define`, `interpret`, `support` | conditional |
| Indian-50 | Precedent (`PRE`) | `report`, `support`, `compare`, `interpret` | conditional |
| Indian-50 | Ratio of the decision (`Ratio`) | `support`, `explain`, `interpret` | conditional |
| Indian-50 | Ruling by Present Court (`RPC`) | `report`, `interpret` | partial |

## Decisions and verification

- Keep source attribution, legal role, source text, sentence and character offsets as separate fields. Associate reviewed paragraph or span functions only when the relevant textual contribution is present; allow multiple and unresolved functions. The BUILD README describes one role per sentence but also specifies `ANALYSIS` co-tags for statute and precedent. Retain actual source label arrays and investigate the discrepancy rather than forcing single-label output.
- Preserve the ECHR actor dimension as metadata: ECHR, Applicant, State, Third parties and Commission/Chamber. Legal argument types are not equivalent to generic argument functions. When text supports a target claim, a reviewer can separately identify that target; an actor or citation alone cannot. The authors explicitly note that context beyond a paragraph may be needed.
- Meaningful deterministic checks validate label vocabularies, span offsets and ordering, retained source metadata, paragraph alignment and existing explicit target IDs. They do not decide whether evidence supports a claim, a comparison is meaningful, a quotation is endorsed, or a legal action is an assertion.
- The [2019 paper, section 4.1](https://arxiv.org/html/1911.05405#S4.SS1), defines its seven labels, including `Argument` as the court weighing opposing parties. It reports disagreement between precedent and reasoning and between reasoning and court rulings; this provides strong adversarial calibration cases. Its reported 50 cases and other published counts are not recalculated here.
- The [BUILD role definitions](https://github.com/Legal-NLP-EkStep/rhetorical-role-baseline#appendix) distinguish petitioner and respondent arguments and explicitly define `Ratio` differently from the academic term ratio decidendi. Data availability and complete actual split counts await the acquisition manifest; the direct dev download previously returned HTTP 401.
- The [ECHR actor definitions](https://link.springer.com/article/10.1007/s10506-023-09361-y#Sec5) and [argument-type definitions](https://link.springer.com/article/10.1007/s10506-023-09361-y#Sec6) are available in the open paper. The JSON covers all five actors and four illustrative argument types, not the complete set of 16. Paper reports 373 gold cases; processed BIO training uses only “The Law” onward. No data-derived counts are asserted here.

These sources provide boundary cases and provenance patterns for the user’s own plugin, not function frequencies, validated paragraph labels, or structural targets for essays, proposals or decision memos. Check actual corpus terms and underlying judgment rights before redistribution or downstream product use.
