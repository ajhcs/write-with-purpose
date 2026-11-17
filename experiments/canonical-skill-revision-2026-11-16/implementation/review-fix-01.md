# Review fix 01: requested learning sequence

Remove a learning-sequence ambiguity that could put writing before explicitly requested attempt-first practice. The actual request determines sequence.

Four prose instructions only; versions, scripts, tests and other canonical content unchanged.

## skills/write-with-purpose/SKILL.md

Before SHA-256: `6aafccaf5311cdfc4d2f3808260fb511008e02b8ddf94e0f159bef0bb78d6df1`

After SHA-256: `f2ca3c335f6b71b10e1a247a9bd0048b8d0b0d900f5672f3423f8678c2e4d37f`

```diff
--- skills/write-with-purpose/SKILL.md (before review-fix-01)
+++ skills/write-with-purpose/SKILL.md (after review-fix-01)
@@ -31,2 +31,2 @@
 
-Read the result as a standalone whole for reasoning, flow and the intended experience. Complete the requested work and relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue, not a rewrite quota. Model comparison is provisional, not measured reader success. Deliver only the editorial notes the task needs. When explanation or learning is wanted, connect a real choice to its effect; offer practice only when chosen or part of the learning workflow, after the writing. Give a requested worked solution directly; acceptance of an edit does not establish learning.
+Read the result as a standalone whole for reasoning, flow and the intended experience. Complete the requested work and relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue, not a rewrite quota. Model comparison is provisional, not measured reader success. Deliver only the editorial notes the task needs. When explanation or learning is wanted, connect a real choice to its effect. Follow the requested learning sequence: deliver requested writing before optional practice; when attempt-first practice is requested, let the author attempt first. Give a requested worked solution directly; acceptance of an edit does not establish learning.
```

## skills/edit-with-purpose/SKILL.md

Before SHA-256: `3304c5d253a69f89dc4085334594ba4a5a2a5adda0c85927d44ac9ac15e6bcb5`

After SHA-256: `f681118cc18764919baa4fcee45e307b805c9e8c0747b7d6359888359b15af82`

```diff
--- skills/edit-with-purpose/SKILL.md (before review-fix-01)
+++ skills/edit-with-purpose/SKILL.md (after review-fix-01)
@@ -34,2 +34,2 @@
 
-Preserve a file original unless authorized to replace it. Finish with a whole-result reading and the relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue. Judge conformance, correctness and usefulness separately; model preference is not author acceptance or observed reader benefit. Return the revision and only material notes requested or needed. Explain a real choice when explanation or learning is wanted; practice follows the deliverable only when chosen or part of that workflow. Give a requested worked solution directly.
+Preserve a file original unless authorized to replace it. Finish with a whole-result reading and the relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue. Judge conformance, correctness and usefulness separately; model preference is not author acceptance or observed reader benefit. Return the revision and only material notes requested or needed. Explain a real choice when explanation or learning is wanted. Follow the requested learning sequence: deliver the requested revision before optional practice; when attempt-first practice is requested, let the author attempt first. Give a requested worked solution directly.
```

## skills/write-with-purpose/references/structure-and-purpose.md

Before SHA-256: `a81f60a2019d4b505be5a5d9c433c4608d7e2964d8d3508d6d9ab09d24d74bb8`

After SHA-256: `6ce429e897e7a0d6f44ec35ccda9fee4a949f9a4367f260e0b66b91f2006d6de`

```diff
--- skills/write-with-purpose/references/structure-and-purpose.md (before review-fix-01)
+++ skills/write-with-purpose/references/structure-and-purpose.md (after review-fix-01)
@@ -46,2 +46,2 @@
 
-If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Practice belongs after the writing when chosen or part of that workflow; allow the author to attempt first in practice mode, but deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
+If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Follow the requested learning sequence. When writing or revision is requested, deliver it before optional practice. When attempt-first practice is requested, let the author attempt first; deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
```

## skills/edit-with-purpose/references/structure-and-purpose.md

Before SHA-256: `a81f60a2019d4b505be5a5d9c433c4608d7e2964d8d3508d6d9ab09d24d74bb8`

After SHA-256: `6ce429e897e7a0d6f44ec35ccda9fee4a949f9a4367f260e0b66b91f2006d6de`

```diff
--- skills/edit-with-purpose/references/structure-and-purpose.md (before review-fix-01)
+++ skills/edit-with-purpose/references/structure-and-purpose.md (after review-fix-01)
@@ -46,2 +46,2 @@
 
-If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Practice belongs after the writing when chosen or part of that workflow; allow the author to attempt first in practice mode, but deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
+If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Follow the requested learning sequence. When writing or revision is requested, deliver it before optional practice. When attempt-first practice is requested, let the author attempt first; deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
```

Both shared reference copies remain identical; all other stable-manifest files retain their hashes. The stable manifest now identifies the final source. Parent will capture official qualification on final source and execute narrow learning and standalone-editor fallback cases. Initial revised execution remains tied to its earlier frozen snapshot.
