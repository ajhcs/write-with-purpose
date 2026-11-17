#!/usr/bin/env python3
"""Normalize existing domain manifests for library browsing; no network or text analysis."""

import collections
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def choose(record, *names):
    for name in names:
        value = record.get(name)
        if value is not None and value != "" and value != []:
            return value
    return ""


def normalize(domain, record, index):
    authors = choose(record, "authors", "authors_openalex", "author")
    if isinstance(authors, list):
        authors = "; ".join(authors)
    doi = str(choose(record, "doi", "doi_url"))
    doi = doi.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    return {
        "source_group": domain,
        "source_record_number": index,
        "title": record["title"],
        "authors_as_indexed": authors,
        "indexed_or_displayed_year": choose(record, "year", "publication_year", "year_display"),
        "source_date": choose(record, "date", "publication_date", "date_display"),
        "outlet_as_indexed": choose(record, "venue", "outlet"),
        "doi": doi,
        "discovery_url": choose(record, "publisher_or_index_landing_url", "publisher_landing_url", "landing_page_url", "target_url", "doi_url", "source_record_url"),
        "provider_work_id": choose(record, "openalex_id", "openalex_work_id", "id"),
        "form_hypothesis": choose(record, "provisional_form", "candidate_form", "form"),
        "selection_signal": choose(record, "selection", "selector", "priority") or "Source-specific OpenAlex citation ordering; see exact query in original record.",
        "citation_count": choose(record, "citation_count", "citation_count_as_of_retrieval", "openalex_cited_by_count"),
        "citation_provider": choose(record, "citation_provider", "citation_count_provider"),
        "citation_or_discovery_snapshot": choose(record, "citation_observed_at", "retrieved_utc", "citation_snapshot_utc", "source_retrieved_utc"),
        "held_by_source_screen": bool(record.get("known_or_suspected_conflict", False)),
        "hold_reason": record.get("hold_reason", ""),
        "form_and_suitability_status": "unverified discovery lead; no full-text examination in this expansion",
        "historical_date_status": "provider/index/display date; original publication and version verification required",
        "source_manifest": f"{domain}/records.jsonl",
    }


def main():
    rows, sources = [], []
    for domain in ("business", "engineering", "law", "personal"):
        path = ROOT / domain / "records.jsonl"
        data = path.read_bytes()
        records = [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]
        rows.extend(normalize(domain, record, index) for index, record in enumerate(records, 1))
        sources.append({"path": str(path.relative_to(ROOT)), "records": len(records),
                        "sha256": hashlib.sha256(data).hexdigest()})
    with (ROOT / "nonmedical-discovery.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    doi_occurrences = collections.Counter(row["doi"].lower() for row in rows if row["doi"])
    report = {
        "source_records": len(rows),
        "by_source_group": dict(collections.Counter(row["source_group"] for row in rows)),
        "held_records": sum(row["held_by_source_screen"] for row in rows),
        "distinct_nonempty_dois": len(doi_occurrences),
        "doi_values_appearing_multiple_times": sum(count > 1 for count in doi_occurrences.values()),
        "missing_dois": sum(not row["doi"] for row in rows),
        "sources": sources,
        "scope": "Source records, not verified works or measured texts. This normalization preserves source-group overlaps and does not establish bibliographic identity, original dates, access, form or quality. HeinOnline's separate ranked snapshot is not merged.",
    }
    (ROOT / "merge-receipt.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "sources"}, indent=2))


if __name__ == "__main__":
    main()
