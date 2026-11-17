# Review fix 03: separate prose from editorial notes

Parent reported an E06 execution artifact containing the correct Methods sentence followed by an unlabelled explanatory paragraph, despite a request for Methods text plus a separate unsupported-claim flag. Restore an explicit delivery boundary for publishable prose and editorial/source notes.

Parent-reported packaging failure only; no unrelated paired outputs inspected. The observation does not establish that the rule caused the failure.

Two entrypoint delivery instructions only. No universal headings, logs or separate-file requirement. Prior fix 02 records, failure outputs and snapshots preserved; core rules, shared references, scripts, tests and metadata versions unchanged.

## skills/write-with-purpose/SKILL.md

Before SHA-256: `1e1623e4cac013a4eaeaf033f757c0bb3e406780f0b105d55c594019114ce8b2`

After SHA-256: `9c2824bae19c6aeef0e13845124b98c1805f4b2b0901bb61b4b537fbe287748b`

```diff
--- skills/write-with-purpose/SKILL.md (after review-fix-02)
+++ skills/write-with-purpose/SKILL.md (after review-fix-03)
@@ -31,2 +31,2 @@
 
-Read the result as a standalone whole for reasoning, flow and the intended experience. Complete the requested work and relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue, not a rewrite quota. Model comparison is provisional, not measured reader success. Deliver only the editorial notes the task needs. When explanation or learning is wanted, connect a real choice to its effect. Follow the requested learning sequence: deliver requested writing before optional practice; when attempt-first practice is requested, let the author attempt first. In chosen practice, supply necessary facts and constraints without completing the writing move being practised, even in a facts preface. Give a requested worked solution directly; acceptance of an edit does not establish learning.
+Read the result as a standalone whole for reasoning, flow and the intended experience. Complete the requested work and relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue, not a rewrite quota. Model comparison is provisional, not measured reader success. Deliver only the editorial notes the task needs. Keep publishable prose distinct from editorial or source notes so the intended text and any counted scope are unambiguous. Use only the separation the task needs; headings or separate files are not required for ordinary chat. When explanation or learning is wanted, connect a real choice to its effect. Follow the requested learning sequence: deliver requested writing before optional practice; when attempt-first practice is requested, let the author attempt first. In chosen practice, supply necessary facts and constraints without completing the writing move being practised, even in a facts preface. Give a requested worked solution directly; acceptance of an edit does not establish learning.
```

## skills/edit-with-purpose/SKILL.md

Before SHA-256: `6eae53f0231eef0dfff83c72d677ce67ab2faabe248cd5f5722a04712712e694`

After SHA-256: `7b612c6b8253ffc2b1926ac826cfd2fd32c65b72a57e564a808522a8739bbea5`

```diff
--- skills/edit-with-purpose/SKILL.md (after review-fix-02)
+++ skills/edit-with-purpose/SKILL.md (after review-fix-03)
@@ -34,2 +34,2 @@
 
-Preserve a file original unless authorized to replace it. Finish with a whole-result reading and the relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue. Judge conformance, correctness and usefulness separately; model preference is not author acceptance or observed reader benefit. Return the revision and only material notes requested or needed. Explain a real choice when explanation or learning is wanted. Follow the requested learning sequence: deliver the requested revision before optional practice; when attempt-first practice is requested, let the author attempt first. In chosen practice, supply necessary facts and constraints without completing the writing move being practised, even in a facts preface. Give a requested worked solution directly.
+Preserve a file original unless authorized to replace it. Finish with a whole-result reading and the relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue. Judge conformance, correctness and usefulness separately; model preference is not author acceptance or observed reader benefit. Return the revision and only material notes requested or needed. Keep publishable prose distinct from editorial or source notes so the intended text and any counted scope are unambiguous. Use only the separation the task needs; headings or separate files are not required for ordinary chat. Explain a real choice when explanation or learning is wanted. Follow the requested learning sequence: deliver the requested revision before optional practice; when attempt-first practice is requested, let the author attempt first. In chosen practice, supply necessary facts and constraints without completing the writing move being practised, even in a facts preface. Give a requested worked solution directly.
```

Every other stable-manifest file retains its hash. Parent will freeze final source and narrowly retest E06 plus learning cases, then capture final Python, skill-validator and annotation regression results. A delivery clarification prompted by a development observation, not causal or general efficacy evidence.
