# Mechanical checks

For a requested exact check, reuse the existing `write-with-purpose/scripts/check_text.py` helper when it is available in a known configured skill root. Read its usage or run `--help` if needed. If it is unavailable, identify the unavailable mechanical check and continue the editorial work. The editor has no required service or helper installation.

```text
python <writer-skill>/scripts/check_text.py <edited.txt> [--source <before-or-source.txt>] [--contract <contract.json>]
```

The helper reports exact duplicate prose paragraphs, explicit unresolved markers, limited internal Markdown-anchor discrepancies and source-number differences. A declared contract can check required literal presence. It does not judge semantic correctness, paragraph flow, useful repetition or reader benefit. Its input hashes identify the bytes checked.

Use contracts for actual obligations. A selected explanation need not retain every source number, and a justified omission is not a reason to restore a fact mechanically. Interpret findings in context; retain good writing where an observation has no editorial consequence. Check the delivered bytes again if changes make an earlier receipt stale. The helper is read-only, with no automatic repair loop.
