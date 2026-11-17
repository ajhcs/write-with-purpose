# Review fix 02: preserve the chosen practice operation

An observed L02 development failure supplied an already-composed target sentence as source facts before inviting the author to practise that sentence. Sequence alone did not preserve the chosen writing operation.

Four conditional learning instructions only. Ordinary writing gains no practice burden; requested worked solutions remain direct. Scripts, tests, metadata versions and all other canonical content unchanged.

Only the raw L02 task and the parent-quoted failure informed this change. The shared reference illustrates raw counts and labels versus a sentence that already performs the requested move; it explicitly avoids requiring a particular presentation format.

## skills/write-with-purpose/SKILL.md

Before SHA-256: `f2ca3c335f6b71b10e1a247a9bd0048b8d0b0d900f5672f3423f8678c2e4d37f`

After SHA-256: `1e1623e4cac013a4eaeaf033f757c0bb3e406780f0b105d55c594019114ce8b2`

```diff
--- skills/write-with-purpose/SKILL.md (after review-fix-01)
+++ skills/write-with-purpose/SKILL.md (after review-fix-02)
@@ -31,2 +31,2 @@
 
-Read the result as a standalone whole for reasoning, flow and the intended experience. Complete the requested work and relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue, not a rewrite quota. Model comparison is provisional, not measured reader success. Deliver only the editorial notes the task needs. When explanation or learning is wanted, connect a real choice to its effect. Follow the requested learning sequence: deliver requested writing before optional practice; when attempt-first practice is requested, let the author attempt first. Give a requested worked solution directly; acceptance of an edit does not establish learning.
+Read the result as a standalone whole for reasoning, flow and the intended experience. Complete the requested work and relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue, not a rewrite quota. Model comparison is provisional, not measured reader success. Deliver only the editorial notes the task needs. When explanation or learning is wanted, connect a real choice to its effect. Follow the requested learning sequence: deliver requested writing before optional practice; when attempt-first practice is requested, let the author attempt first. In chosen practice, supply necessary facts and constraints without completing the writing move being practised, even in a facts preface. Give a requested worked solution directly; acceptance of an edit does not establish learning.
```

## skills/write-with-purpose/references/structure-and-purpose.md

Before SHA-256: `6ce429e897e7a0d6f44ec35ccda9fee4a949f9a4367f260e0b66b91f2006d6de`

After SHA-256: `ca7bed5792f329df5d357e0ad0e36c007d0eaf1bbb3927ebe44ab07c81ce0434`

```diff
--- skills/write-with-purpose/references/structure-and-purpose.md (after review-fix-01)
+++ skills/write-with-purpose/references/structure-and-purpose.md (after review-fix-02)
@@ -46,2 +46,2 @@
 
-If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Follow the requested learning sequence. When writing or revision is requested, deliver it before optional practice. When attempt-first practice is requested, let the author attempt first; deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
+If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Follow the requested learning sequence. When writing or revision is requested, deliver it before optional practice. When attempt-first practice is requested, supply necessary raw facts and constraints in a form that leaves the chosen writing move to the author. Check that the setup itself has not completed that move, even if labelled as facts. For example, when practising replacement of vague praise with a specific result, “correct classifications: 80; evaluated cases: 100; comparator: none supplied” leaves the sentence to compose; “The model correctly classified 80 of 100 cases” already supplies it. Choose a useful presentation for the task; labels or bullets are not required. Let the author attempt before showing a solution. Deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
```

## skills/edit-with-purpose/SKILL.md

Before SHA-256: `f681118cc18764919baa4fcee45e307b805c9e8c0747b7d6359888359b15af82`

After SHA-256: `6eae53f0231eef0dfff83c72d677ce67ab2faabe248cd5f5722a04712712e694`

```diff
--- skills/edit-with-purpose/SKILL.md (after review-fix-01)
+++ skills/edit-with-purpose/SKILL.md (after review-fix-02)
@@ -34,2 +34,2 @@
 
-Preserve a file original unless authorized to replace it. Finish with a whole-result reading and the relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue. Judge conformance, correctness and usefulness separately; model preference is not author acceptance or observed reader benefit. Return the revision and only material notes requested or needed. Explain a real choice when explanation or learning is wanted. Follow the requested learning sequence: deliver the requested revision before optional practice; when attempt-first practice is requested, let the author attempt first. Give a requested worked solution directly.
+Preserve a file original unless authorized to replace it. Finish with a whole-result reading and the relevant checks; another pass needs a specific worthwhile opportunity or unresolved issue. Judge conformance, correctness and usefulness separately; model preference is not author acceptance or observed reader benefit. Return the revision and only material notes requested or needed. Explain a real choice when explanation or learning is wanted. Follow the requested learning sequence: deliver the requested revision before optional practice; when attempt-first practice is requested, let the author attempt first. In chosen practice, supply necessary facts and constraints without completing the writing move being practised, even in a facts preface. Give a requested worked solution directly.
```

## skills/edit-with-purpose/references/structure-and-purpose.md

Before SHA-256: `6ce429e897e7a0d6f44ec35ccda9fee4a949f9a4367f260e0b66b91f2006d6de`

After SHA-256: `ca7bed5792f329df5d357e0ad0e36c007d0eaf1bbb3927ebe44ab07c81ce0434`

```diff
--- skills/edit-with-purpose/references/structure-and-purpose.md (after review-fix-01)
+++ skills/edit-with-purpose/references/structure-and-purpose.md (after review-fix-02)
@@ -46,2 +46,2 @@
 
-If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Follow the requested learning sequence. When writing or revision is requested, deliver it before optional practice. When attempt-first practice is requested, let the author attempt first; deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
+If explanation or a learning workflow is requested, connect a real choice to the actual wording and its consequence. A countercase can clarify when the same move would be unhelpful. Follow the requested learning sequence. When writing or revision is requested, deliver it before optional practice. When attempt-first practice is requested, supply necessary raw facts and constraints in a form that leaves the chosen writing move to the author. Check that the setup itself has not completed that move, even if labelled as facts. For example, when practising replacement of vague praise with a specific result, “correct classifications: 80; evaluated cases: 100; comparator: none supplied” leaves the sentence to compose; “The model correctly classified 80 of 100 cases” already supplies it. Choose a useful presentation for the task; labels or bullets are not required. Let the author attempt before showing a solution. Deliver a requested worked solution directly. Neither accepting an edit nor repeating a phrase proves learning or transfer.
```

Both shared reference copies remain identical; every other stable-manifest file retains its hash. Parent will freeze snapshot 02, commission a fresh two-case retest, and capture final Python, skill-validator and annotation regression results. Prior failures and snapshots remain preserved. This addresses an observed development defect; it does not demonstrate general method efficacy.
