# Advisory checks

Use the bundled checker when a requested mechanical review or declared preservation obligation benefits from exact observations. It is optional and does not edit the document. It needs Python3 and only the standard library.

```text
python <skill>/scripts/check_text.py <draft.md> [--source <source.md>] [--contract <contract.json>] [--enforce-contract]
```

The JSON report identifies duplicate prose paragraphs, explicit unresolved markers, simple internal Markdown-anchor discrepancies and numeric-token differences when a source is supplied. These are observations to interpret. Repeated words, stylistic vocabulary, sentence length and punctuation choices are not quality violations. An exact duplicate can be justified at separate points of use.

A task contract can declare exact literals and word limits:

```json
{"protected_literals": [{"text": "<exact source text>", "min_count": 1}], "max_words": 250, "max_growth_words": 0}
```

Each key is optional; include only constraints the task actually sets. `max_words` and `max_growth_words` accept nonnegative integers. `max_growth_words` requires `--source`; zero means the candidate cannot exceed that source's word count. Use the original draft as that source for a no-growth check, not a larger factual source packet. The sample value 250 is illustrative, never a default. Counts include all whitespace-separated tokens in the raw artifact, including Markdown and code, excluding an initial UTF-8 BOM. Isolate the requested body in its own file when a brief excludes notes or headings. This convention may differ from a publisher's word counter.

Use a contract only for actual task constraints. Meaning-preserving paraphrase should not be prohibited by inventing an exact-text requirement. Literal presence does not establish correct context or entity binding.

In a selective summary, source details may legitimately be absent. Numeric differences are review candidates for the claims the task needs to retain, not a completeness requirement for the entire source packet. Use an explicit contract for actual preservation obligations; an omission alone is not a reason to add a fact back.

The report names evaluated, not-requested and unavailable checks and fingerprints the input bytes. Source-number differences warrant review, including for justified conversion or omission; matching number sets does not prove semantic preservation. Fenced code is excluded from prose scanning while retaining line positions. Internal anchor analysis is a limited Markdown approximation, not a full renderer. Review the actual artifact and the method's stated limits.

By default, a successful invocation exits 0 even when it reports findings. `--enforce-contract` requires a contract and exits 1 for violated literal or word-limit requirements. It exits 0 when those declared checks pass; unrelated findings remain advisory. Invalid inputs exit 2 and leave enforcement unavailable. Inspect `contract_enforcement` as well as the exit code. Enforcement covers these mechanical constraints only. It is not an installed hook and cannot intercept a chat response or force the model to use the checker. Inspect both the assessment status and findings. Correctness and usefulness remain unassessed by this program. A repaired artifact requires a new check if the receipt is to describe its delivered bytes.

Address relevant findings, retain justified choices, and surface material unresolved questions. Another automatic rewrite is appropriate only when it has a defensible benefit within the task. No installed hooks run this checker or impose repair loops in this version.
