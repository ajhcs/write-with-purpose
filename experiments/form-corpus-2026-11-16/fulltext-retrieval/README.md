# Retrieve available full texts

The author authorized retrieval of available copies from the broadened business, engineering, law and personal/public-writing collections. Four GPT-6.1 Terra branches perform the retrieval. This is acquisition and source verification, not a new statistical writing analysis or acceptance of the proposed form labels.

The [completed retrieval summary](summary.md) records what was saved, unresolved identity/completeness and access outcomes, the download index, file validation and disclosed crawler corrections.

## Scope

- Business: the 1,200 discovery records, including practitioner writing in HBR.
- Engineering: the 350 historical bibliographic records.
- Law: the 346 unheld indexed leads and 97 unheld records from the separate HeinOnline ranked snapshot, reconciled where possible. Held source conflicts remain visible rather than being silently treated as genuine articles.
- Personal/public writing: the 316 editorial discovery records, including Notables seeds with incomplete original links.

These are source entries, not necessarily unique works. Earlier medical XML and current software-documentation source caches remain separate; the broadened acquisition is not a further expansion of the medical sample.

The local [full-text retrieval skill](/home/builderbob/.agents/skills/fulltext-retrieval/SKILL.md) guides PDF validation, source identity and manual-access records. The existing `medsci-python` runtime provides `pdftotext` and `pdfinfo`, and `medsci-pdf-python` provides PyMuPDF. Those installed tools are used without a package installation. Unpaywall's email-requiring route is not invoked with an invented contact; other public-source routes are used instead.

## Storage and provenance

Original files and API/source caches are stored outside Git under `/workspace/repos/builderbob/.writing-corpus-cache/fulltext/`, with a directory per source group. The repository retains scripts, per-record results, hashes, attempted/final URLs, identity/completeness assessments and retrieval queues. Existing source records and exclusion decisions are preserved.

No live institutional browser or Zotero session was established in this task. Bounded connected-Drive title searches returned related files rather than established exact article matches; unrelated documents were not downloaded. A public-access failure does not establish that the author's libraries cannot supply the work.

## Interpretation of outcomes

Each branch distinguishes these aspects in its actual schema:

1. **Request outcome:** which source routes were attempted and whether HTTP/API requests succeeded, failed or were deferred after an access/rate response.
2. **File evidence:** format, byte count, local path and SHA-256. A PDF signature and size establish a plausible file, not its bibliographic identity.
3. **Identity evidence:** title, DOI/identifier and author where available. The skill's PDF check examines bounded first-page front matter; titles in a reference list do not verify identity. Coversheets and preprint/publisher identifiers can remain unresolved.
4. **Full-text evidence:** an article body versus a landing page, abstract, preview, supplement, scan or incomplete copy. A successful HTML request is not automatically a retrieved complete article. Downloaded PDFs can also remain unassessed for completeness.
5. **Version and rights:** source location, repository/publisher version and license when supplied. Original publication year and the version served now are distinct.

Keep unresolved files visible for review and do not count them as verified exemplars. A legitimately accessible preprint can be useful while differing from the published historical article. Retrieval does not establish form, source truth, editorial quality, audience fit or permission to redistribute a text.

Rate limiting, robots decisions and access barriers are recorded rather than worked around. Host-level deferrals and missing URLs belong in the remaining retrieval ledger; they are not definitive statements that no accessible copy exists anywhere.

## Reuse

Read the branch report before rerunning its collector. Cached responses and resume behavior differ by branch; live API results, available versions and server behavior can change. Scripts are retrieval tooling, not an installed skill dependency or an automatic publishing workflow. Source material stays local; no corpus publication, external upload or sharing change is part of this task.
