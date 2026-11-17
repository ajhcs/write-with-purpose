# Blind long-form author review

The first batch contains **16 comparisons**: four complete prose works and opening, middle and closing passage windows from each. Eight fresh GPT-6.1 Terra contexts produced all 32 rewrites using identical briefs and supplied source context. Each context handled one source and its four tasks. No model quality ranking is included.

**Unblinded at the author's explicit request:** revised writer preferred in six rated cases, baseline in three, Original in one. All generators selected the writer skill, and all ten submitted judgments concern section passages. See [the results and proposed improvements](review/unblinded-results.md) and [the complete released mapping](review/unblinded-key.json). The original blind reader remains unchanged as a record of what was judged.

The original human view always identifies Original. A and B were anonymous, their positions varied across comparisons, and assignments stayed fixed. The key was kept separate during collection and has now been released by request. Further ratings on this set must be identified as informed by that reveal and kept separate from the frozen pre-reveal counts. A new blinded round needs a distinct trial ID and preserved assignments.

## Sources

- Cole Lyons, [Learning CS50 at 256 Kilobits per Second](https://colelyons.com/writing/cs50-software-ai-formation/).
- Cole Lyons, [Making engineering part of healthcare’s work](https://colelyons.com/writing/making-engineering-part-of-healthcares-work/).
- Cory Doctorow, [Tiktok’s enshittification](https://pluralistic.net/2023/01/21/potemkin-ai/), Creative Commons Attribution 4.0 for the main essay, with the stated exclusions preserved.
- Python documentation, [Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/3.8/tutorial/floatingpoint.html), with the source license retained.

These are prose-only extracts with source links, attribution, hashes and scope recorded. Navigation, interactive figure text and unrelated daily-link sections are excluded. Original code examples are retained. Source-visible counts range from roughly 800 to 4,200 words; the passage windows preserve real paragraph boundaries rather than padding to a target.

## Human review

**Author review closed:** ten case-level judgments were submitted before the author ended the round. Six cases have no submitted rating. All ten rated cases are section passages; the four whole-work comparisons remain unrated. [The author summary](review/author-summary.md) preserves the choices and distinctions without revealing conditions. Missing ratings were not imputed, and closure does not itself request unmasking.

Use the interactive reader or the [blind text packet](review/blind-review.md). For each comparison, select which version you would use—Original, A, B, Tie or Neither—and which rewrite makes a substantive improvement. Comments remain the author's exact words. There are no prefilled judgments. Partial reviews are useful and must not trigger automatic unmasking.

[The public data](review/data.json) contains no skill identities, worker paths, source-audit findings or model preferences. [The adjudication register](review/adjudications.json) remains empty until actual author feedback arrives. Browser interaction tests use isolated mock state and are not human judgments.

## Evidence and limits

- [Protocol](protocol.md)
- [Source extraction checks](validation/source-extraction.md)
- [Pre-generation key commitment](validation/blinding-commitment.json)
- [Reader browser checks](validation/reader-ui.md)
- [Final blinding and artifact checks](validation/final-review.json)

All first outputs are preserved. Source-fidelity notes are stored separately so they do not prime the author's initial preference. That review is a model assessment of supplied-source fidelity, not independent verification of every published claim. Multiple comparisons share source and generation context. Familiar published prose and recognizable style may weaken blinding; this is not an unseen benchmark or a claim of general superiority.

Browser tests cover the real data at desktop and narrow widths, including state restoration and sending through mocked host APIs. A reproduced stale-state overwrite was repaired so older events cannot replace newer comments. Those checks did not verify actual cross-client persistence, and the assistant did not submit real human reviews. The reader provides an explicit copy fallback.

Subsequent real author submissions were received through the reader's Send reviews action and validated against the trial and case IDs. [Live-host observations](validation/live-host-observations.json) record that evidence separately from the pre-launch mocked tests. Cross-client persistence remains unverified. The launch validation receipts describe the initially blank review set; they are preserved as historical checks, not rewritten after real feedback.

No source website, canonical skill, globally installed skill, service or publication was changed by this trial. Working sources and controls are preserved on `/workspace`; the conversation fragment is a matching native response copy.

Local recovery receipt: `/workspace/build/builderbob/write-with-purpose/checkpoints/blind-longform-20261116T224421Z/manifest.json`. Public review materials and private controls are archived separately; the human packet does not contain the key. This is a local recovery snapshot, not publication or an offsite backup.
