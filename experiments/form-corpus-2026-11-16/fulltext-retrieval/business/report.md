# Business full-text retrieval

Records in this report: **1200** of 1,200. OpenAlex metadata matched **1200**; **519** records received at least one HTTP response from a checked document or landing URL. The remainder still have metadata and attempted/deferred URL traces. This is a retrieval attempt, not a count of works available to a licensed library.

Primary retained results: **36 PDFs** and **0 substantial public HTML bodies**. Across retained results, **7** have matching source-identity evidence, **28** are unresolved, **0** conflict, and **1** lack usable identity evidence. Completeness was verified for **0**: page count and an extracted title are not evidence of a complete publication.

All retained files are outside Git under `/workspace/repos/builderbob/.writing-corpus-cache/fulltext/business`. The full per-record trace and alternate paths are in `retrieval_manifest.jsonl`; `manual_needed.csv` distinguishes library access, identity/completeness review, and completeness/version review. Hash audit: 0 missing files, 0 hash mismatches; 0 other cache files not referenced by the current manifest are preserved and listed in `counts.json`.

The first pass matched all location metadata and applied a 0.75-second per-host minimum. It did **not** enforce robots-declared longer crawl delays or request rates, and treated robots redirects conservatively as unavailable. The initial follow-up followed robots redirects automatically without separately pacing redirect hops, although it enforced crawl-delay and request-rate for document requests. The last follow-up corrected this by manually pacing robots redirect hops and paces document requests by the greater of 0.75 seconds, declared crawl-delay, and request-rate interval. These earlier limitations are retained rather than retroactively claiming compliance. Follow-up preserves 403, 429, and access-challenge host deferrals. For 632 closed records, it recorded a deferral instead of following a DOI to an already-blocked canonical publisher. Rate blocks and challenge detection may be over-conservative; a generic CAPTCHA marker can also appear in a normal page. HBR disallows automated `/search` in its robots file, so indexed public locations were used.

OpenAlex OA flags are leads, not proof of access; metadata batches are cached outside Git. Public landing pages count only when a substantial article element has at least three prose paragraphs and approximately 500 words, matching title evidence, and no detected explicit paywall markers. HTML DOI metadata is required for an identity-consistent HTML result. These checks can miss paywalls, truncated bodies, and article layouts; HTML is never claimed complete automatically. Only PDFs at least 10 KiB with a `%PDF-` header are retained. PDF identity uses the fulltext-retrieval skill's bounded first-page text, not a title appearing in the body or references. Unresolved or conflicting alternatives remain in the manifest and cache. No restricted content or site challenge was bypassed.

The set is a citation-ranked business discovery queue, not a verified classification of writing forms; no rhetorical or genre claims have been made from downloads. Source titles, author strings, identifiers, versions, licenses, dates, URL traces, byte sizes and SHA-256 digests are recorded where known, not inferred when missing.

| Venue | Primary result status counts |
| --- | --- |
| Academy of Management Review | deferred_host_access_or_rate: 195, pdf_retrieved: 5 |
| Academy of Management Journal | deferred_host_access_or_rate: 194, pdf_retrieved: 6 |
| Strategic Management Journal | deferred_host_access_or_rate: 195, pdf_retrieved: 5 |
| Organization Science | deferred_host_access_or_rate: 192, pdf_retrieved: 8 |
| Management Science | deferred_host_access_or_rate: 194, pdf_retrieved: 5, not_retrieved: 1 |
| Harvard Business Review | not_retrieved: 138, pdf_retrieved: 7, robots_disallowed: 11, deferred_host_access_or_rate: 44 |
