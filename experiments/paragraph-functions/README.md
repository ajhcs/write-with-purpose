# Paragraph annotation experiment

This standard-library Python prototype checks supplied annotations against an exact source version and the [initial function catalogue](../../docs/writing-harness/paragraph-functions.json). It does not label prose, decide whether a function succeeds, or integrate with the installed writing skills. The [design guide](../../docs/writing-harness/paragraph-functions.md) explains the intended Codex workflow.

```sh
python3 experiments/paragraph-functions/check_annotations.py \
  experiments/paragraph-functions/examples/queue-explainer.txt \
  experiments/paragraph-functions/examples/queue-explainer.annotations.json
python3 -m unittest discover -s experiments/paragraph-functions -p 'test_*.py' -v
```

Use Python 3. No network, grammar engine, model call, or additional package is required. The checker reads input files and prints JSON without modifying them. `--catalog PATH` selects another catalogue with a matching declared version.

## Annotation contract

The [complete example](examples/queue-explainer.annotations.json) records:

- `schema_version`, `catalog_version`, and the source file's raw-byte `source_sha256`.
- `document.family`, `document.form`, and `document.audience`: supplied context, checked for presence. Their correctness and compatibility are not checked.
- `sections`: unique IDs and a purpose for each section, whether or not it has a printed heading.
- `paragraphs`: unique IDs, section references, exact source spans and quotes, planned and observed functions, supplied annotation status, and evidence references. Function names must occur in the catalogue. Status is `proposed`, `reviewed`, or `unresolved`; the last permits an empty observed-functions array. A supplied `reviewed` label is not proof of an actual review.
- `relations`: registered relation names connecting different known paragraph IDs. Relation meaning is not checked.
- `evidence`: registered IDs, kinds, and locators. The checker validates pointers; it does not open sources, find citations in prose, or verify claims.
- `constraints`: explicitly declared paragraph bounds, each with a source description and `unit: "whitespace_tokens"`. Either `min` or `max` can be absent/null; at least one must be a nonnegative integer. These are hard limits, not observed ranges or working targets. Duplicate constraints for a paragraph and unknown constraint fields are rejected.

Offsets are zero-based Python Unicode character indices, with `end` exclusive, into the raw bytes decoded as UTF-8. No newline or Unicode normalization occurs. Offsets are neither byte positions nor JavaScript UTF-16 positions. Paragraph spans must be nonempty, ordered, nonoverlapping, and exactly equal their supplied quote. Paragraph boundaries are supplied by the annotator; the checker does not infer or validate paragraph segmentation. Unannotated source text is allowed and excluded from span counts. The report states that scope and returns annotated/source character totals.

The token rule is `re.findall(r"\S+", span)`: runs separated by whitespace. It counts raw Markdown and code tokens if the selected span contains them, so it is not a general visible-word counter. Sentence counts, headings, corpus ranges, nested subspans, role-specific field contracts, and terminology rules are future work. Existing word-limit conventions need an explicit counting-policy mapping before integration.

## Output and exits

| Exit | Meaning |
| --- | --- |
| 0 | Input checks passed and no supplied limit was violated, including when no limits were declared |
| 1 | Valid inputs, with at least one declared minimum or maximum violated |
| 2 | Input/invocation error, including stale source hash, invalid JSON, unknown IDs, or invalid spans |

Every assessment reports `semantic_assessment: "not_performed"`. A planned/observed label difference is an observation, not a failure. Reports keep supplied annotations, mechanical counts, declared limits, and observations separate. Input validity does not certify factual correctness, voice, reader comprehension, or writing quality.

The queue example and its annotations are synthetic model-authored fixtures. Its single 40-token ceiling is an arbitrary demonstration contract; it is not a measured norm or an author preference. All role assignments remain proposed.
