# Legal full-text retrieval receipt

Updated 2026-11-16T01:52:16.375229+00:00.

Source records accounted: 494; held skipped: 47; duplicate linked to another candidate: 41; no file acquired: 395; file acquired: 11.
For acquired files, first-page source identity consistent: 0; unresolved: 11; conflict: 0; unavailable: 0. A consistent identity is bounded first-page evidence, not proof of completeness or suitability. The unresolved and conflicting files require manual review and are not counted as confirmed full texts.

Source materials are stored outside Git under `/workspace/repos/builderbob/.writing-corpus-cache/fulltext/law/files/`. Per-item manifests preserve title, provider, full-text URL attempts, HTTP outcomes, final source URL, version/license if reported, size, hash, page count and identity assessment. Full text is not redistributed here. First-page title match alone is not identifier agreement. For legal articles, alternate versions, book/review merges, footnote-only appearances, published/corrected status and document boundaries also require review.

The initial pass identified ordinary robots-file redirects as unavailable; a corrected subsequent pass followed them and retained prior attempts. The retrieval code respects robots exclusion, crawl-delay and request-rate (deferring delays over five seconds), limits four workers, paces each host, stops on HTTP 429, does not bypass denials, and does not use Unpaywall because no contact email was supplied. It tries source metadata public locations, publisher landing pages and advertised citation PDF links; HTML is not treated as a retrieved full article except one explicit official brief saved as unverified for review. First-pass Crossref metadata lookup stopped at 429; unresolved Hein-only items may need catalog lookup. No credentials or publisher access bypass were used.

429-related hosts recorded: {'dash.harvard.edu': 4, 'api.crossref.org': 55}. Other logged deferred/denied attempt counts: {'host_deferred_robots_unavailable': 384, 'robots_301': 3, 'robots_403': 4, 'host_deferred_robots_access_denied': 8, 'robots_error': 3, 'host_deferred_robots_long_delay': 25, 'host_deferred_robots_error': 77, 'robots_long_delay': 5, 'robots_disallow': 47, 'host_deferred_429_previous_run': 4, 'host_deferred_429': 53, 'network_error': 1}.

The `manual_needed.txt` list includes no-file and identity-unresolved records; held source records remain in the manifest rather than being silently discarded. Duplicate rows refer to the linked source record and are not additional acquired documents. DOI and version access, rights, actual body completeness and whether a full document is the requested legal form remain to be checked.
