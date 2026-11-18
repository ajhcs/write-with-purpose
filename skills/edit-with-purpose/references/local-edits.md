# Local edits and change measurement

Use the optional Python 3 helper when the task needs reproducible exact-span changes to a UTF-8 file or a measurement of an existing revision.

```text
python <editor-skill>/scripts/edit_locally.py original.txt --plan edits.json --output edited.txt
python <editor-skill>/scripts/edit_locally.py original.txt --compare existing-edit.txt
```

## Reconstruct a revision

Use `--plan` to replay selected changes against the original bytes. Provide a new path with `--output` to save the result. Omitting `--output` checks the plan and reports its candidate without writing it. The helper preserves the source, the plan file, and any existing destination.

The plan contains the original bytes' SHA-256 and an array of edits.

```json
{
  "source_sha256": "<64-character SHA-256 of the original bytes>",
  "edits": [
    {"start": 0, "end": 1, "before": "<source substring>", "after": "<replacement>", "reason": "<what the edit accomplishes>"}
  ]
}
```

Calculate the offsets from the decoded source. Start is inclusive and end is exclusive, both in zero-based Unicode code points. Set `before` to the exact slice. Use an empty `before` and equal offsets for an insertion, or an empty `after` for a deletion. The helper rejects a stale hash, mismatch, unchanged replacement, overlap, shared starting offset, invalid UTF-8, or malformed plan. It preserves text outside the selected spans, including whitespace and line endings.

Use a whole-passage replacement when it best represents an authorized reorganization. An empty edit array keeps the source whole. Decide the editorial scope before choosing how to record the change.

## Measure and read the result

Use `--compare` for an existing candidate. The report measures differences. Reproducibility of a sequence of edits requires a plan. The word counts use whitespace-separated tokens. Inserted and deleted counts use deterministic token alignment, and a plan report shows selection extent within original blank-line blocks.

Read the revision in context to see what the selected changes did. Measure growth or reduction when it matters to the brief. The receipt can establish exact replay and the reported measurements. Use the source and the actual passage to assess meaning, correctness, and usefulness.
