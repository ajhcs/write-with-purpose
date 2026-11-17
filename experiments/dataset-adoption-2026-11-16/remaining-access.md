# Remaining access and format gaps

These are unresolved endpoints after the current attempts, not proof of a paywall. Original failures and later resolutions remain in the [acquisition index](acquisition-index.json).

| Resource | Outcome | Next route |
| --- | --- | --- |
| build-dev | HTTPError: HTTP Error 401: Unauthorized | Authoritative data release or maintainer-provided copy |
| build-train | HTTPError: HTTP Error 401: Unauthorized | Authoritative data release or maintainer-provided copy |
| moreno-swales | URLError: <urlopen error [Errno 111] Connection refused> | Institutional author version or library article access |
| nathan-options | HTTPError: HTTP Error 403: Forbidden | Institutional author version or library article access |

BUILD definitions and source code were downloaded, but its train/dev files returned 401. The existing [research access list](../prior-work-reuse-2026-11-16/paywalled-research.md) supplies exact article citations and DOIs. Moreno & Swales: **10.1016/j.esp.2017.11.006**. The complete Nathan thesis is downloaded even though its separate options article endpoint failed.

SciPara's source archive and pickle are downloaded, but the pickle is unopened and no usable annotation rows are claimed. An interoperable text/JSON/CSV export and clear rights would resolve that format gap. The semantic essay extension is downloaded, but its underlying AAE text release and custom terms are not acquired through that extension.

CoreSC/ART and DrInventor methods papers are downloaded; complete annotated corpus releases and their operative terms were not established in this acquisition. Licensed RST-DT/PDTB source text is not reconstructed from placeholders. The public PDTB annotation manual is downloaded. No claim of exhaustive access to every resource in the earlier bibliography is made.
