#!/usr/bin/env python3
"""Join local extraction receipts; keep versions and sampling frames explicit."""
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from metrics import summarize

ROOT = Path(__file__).resolve().parent.parent


def read_rows(name):
    return [json.loads(s) for s in (ROOT / 'analysis' / f'{name}-records.jsonl').read_text().splitlines()]


def doi_key(value):
    if not value:
        return None
    value = re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', '', value.strip(), flags=re.I)
    return value.casefold().rstrip(' .')


def url_key(value):
    if not value:
        return None
    p = urlsplit(value)
    # Preserve path and query: different essays can live at the same host.
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), p.query, ''))


def era(year):
    return 'pre-2015' if year and year < 2015 else '2015-2019' if year and year < 2020 else '2020-onward' if year else 'unknown'


def build():
    reviews = {}
    for name in ('medical', 'nonmedical'):
        for r in json.loads((ROOT / 'review' / f'{name}-uploads.json').read_text())['documents']:
            reviews[r['source_sha256']] = r
    normalized = []
    originals = {}
    for kind in ('xml', 'docs', 'html', 'pdf'):
        for i, raw in enumerate(read_rows(kind)):
            sha = raw.get('source_sha256_actual') or raw.get('source_sha256') or raw.get('sha256')
            review = reviews.get(sha, {})
            m = raw.get('metrics') or raw.get('approximate_metrics')
            path = raw.get('source_path') or raw.get('source_cache_path') or raw.get('path')
            year = raw.get('first_publication_year')
            reported_years = {year} if year else set()
            if kind == 'xml':
                for meta in raw.get('source_manifest_metadata', []):
                    for key in ('year', 'publication_year', 'first_publication_date', 'pubYear', 'firstPublicationDate'):
                        match = re.match(r'((?:18|19|20)\d{2})(?:\D|$)', str(meta.get(key) or ''))
                        if match:
                            reported_years.add(int(match[1]))
                year = min(reported_years) if reported_years else None
            if review:
                year = review.get('original_publication_year') or review.get('year')
            elif kind == 'html':
                match = re.search(r'\b(?:18|19|20)\d{2}\b', str(raw.get('date') or ''))
                year = int(match[0]) if match else None
            identity = review.get('title') or raw.get('title') or Path(path or '').name
            form = review.get('recommended_form') or review.get('form') or raw.get('form_candidate') or raw.get('form') or 'unresolved'
            if isinstance(form, dict):
                form = '|'.join(form['labels'])
            docdoi = doi_key(review.get('doi') or raw.get('doi'))
            # First-page PDF DOI observations may belong to an adjacent article;
            # they are never work identifiers without the source review.
            excluded_book = review.get('id') == 'measure_life' or ('Book-length' in str(form))
            composite = review.get('id') == 'particle_data' or 'reference compilation' in str(form)
            record = {
                'record_id': f'{kind}-{i+1:05d}', 'source_format': kind,
                'collection': '|'.join(raw.get('source_cohorts', [])) or raw.get('corpus') or raw.get('collection_domain') or raw.get('repo'),
                'source_path': path, 'source_sha256': sha, 'title': identity,
                'doi': docdoi, 'pmcid': raw.get('pmcid'),
                'source_url': raw.get('source_url') or raw.get('url'),
                'year': year, 'era': era(year), 'year_basis': 'reviewed_source' if review else 'earliest_reported_XML_or_discovery_year' if kind == 'xml' else 'retained_metadata',
                'reported_years': '|'.join(str(y) for y in sorted(reported_years)),
                'date_disagreement': len(reported_years) > 1,
                'form_signal_or_review': form,
                'form_status': 'source_review_proposed' if review else 'unverified',
                'status': raw.get('analysis_status') or raw.get('status') or raw.get('screening_status'),
                'has_measurement': bool(m and m.get('prose_words', 0) > 0), 'profile_eligible': False,
                'scope_disposition': 'excluded_book' if excluded_book else 'split_composite_before_profile' if composite else 'candidate_needs_review',
                'metrics_quality': 'structured_XML_exploratory' if kind == 'xml' else 'partial_source' if kind == 'docs' else 'provisional_HTML' if kind == 'html' else 'approximate_PDF',
                'prose_words': m.get('prose_words') if m else None,
                'prose_paragraphs': m.get('prose_paragraphs') if m else None,
                'median_paragraph_words': m.get('median_paragraph_words') if m else None,
                'median_sentence_words': m.get('median_sentence_words') if m else None,
                'headings': m.get('headings') if m else None,
            }
            normalized.append(record)
            originals[record['record_id']] = raw

    # Connected-component identity links preserve all source versions. Only
    # explicit DOI/PMCID, exact bytes or exact URL link records; titles do not.
    parents = list(range(len(normalized)))
    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i
    keys = {}
    for i, r in enumerate(normalized):
        # A shared redirected homepage is not identity evidence. URL links
        # require the same declared title as well.
        url = url_key(r['source_url'])
        url_identity = (url, re.sub(r'\W+', '', r['title'].casefold())) if url else None
        title_key = re.sub(r'\W+', '', r['title'].casefold())
        byte_identity = (r['source_sha256'], title_key) if r['source_sha256'] else None
        for name, key in [('sha256_and_title', byte_identity), ('doi', r['doi']), ('pmcid', r['pmcid']), ('url_and_title', url_identity)]:
            if key:
                k = (name, key)
                if k in keys:
                    parents[find(i)] = find(keys[k])
                else:
                    keys[k] = i
    groups = defaultdict(list)
    for i, r in enumerate(normalized):
        groups[find(i)].append(r)
    duplicates = []
    for members in groups.values():
        wid = 'work-' + hashlib.sha256('|'.join(sorted(x['record_id'] for x in members)).encode()).hexdigest()[:16]
        # Representative is for navigation, not a quality certification.
        representative = min(members, key=lambda x: (not x['has_measurement'], {'xml': 0, 'html': 1, 'docs': 2, 'pdf': 3}[x['source_format']], x['record_id']))
        for r in members:
            r['linked_work_id'] = wid
            r['representative_record'] = representative['record_id']
        if len(members) > 1:
            duplicates.append({'linked_work_id': wid, 'records': [x['record_id'] for x in members], 'titles': sorted({x['title'] for x in members}), 'dois': sorted({x['doi'] for x in members if x['doi']})})

    # These groups reproduce earlier screened sampling frames, not semantic
    # form certification. Never pool PDF block lengths with JATS paragraphs.
    cohorts = defaultdict(dict)
    for r in normalized:
        raw = originals[r['record_id']]
        if r['source_format'] != 'xml' or not r['has_measurement']:
            continue
        for meta in raw.get('source_manifest_metadata', []):
            label = None
            if meta.get('manifest') == 'empirical-methods/manifest.csv' and meta.get('status') == 'measured':
                label = 'screened_RCT' if meta.get('form') == 'empirical' else 'screened_MethodsX'
            elif meta.get('manifest') == 'systematic-review/manifest.jsonl' and meta.get('status') == 'measured':
                label = 'screened_systematic_review'
            if label:
                cohorts[(label, r['era'])].setdefault(r['linked_work_id'], r)
    summaries = []
    for (label, period), works in sorted(cohorts.items()):
        rows = list(works.values())
        summaries.append({'sampling_frame': label, 'era': period, 'n_distinct_linked_works': len(rows), 'record_ids': [r['record_id'] for r in rows],
            'statistics': {key: summarize([r[key] for r in rows if r[key] is not None]) for key in ('prose_words', 'prose_paragraphs', 'median_paragraph_words', 'median_sentence_words', 'headings')},
            'interpretation': 'Exploratory observations in a selected XML cohort, not writing targets; paragraph/sentence medians calculated within each document before across-document summary.'})
    out = ROOT / 'results'
    out.mkdir(exist_ok=True)
    with (out / 'document-inventory.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(normalized[0]))
        writer.writeheader()
        writer.writerows(normalized)
    (out / 'linked-versions.json').write_text(json.dumps(duplicates, indent=2, ensure_ascii=False) + '\n')
    response_groups = defaultdict(list)
    for r in normalized:
        if r['source_sha256']:
            response_groups[r['source_sha256']].append(r)
    response_collisions = [{'sha256': sha, 'records': [r['record_id'] for r in rows], 'titles': sorted({r['title'] for r in rows}), 'interpretation': 'Identical response bytes with different requested titles; not evidence of a shared work.'} for sha, rows in response_groups.items() if len({r['title'] for r in rows}) > 1]
    (out / 'response-collisions.json').write_text(json.dumps(response_collisions, indent=2, ensure_ascii=False) + '\n')
    (out / 'exploratory-cohort-statistics.json').write_text(json.dumps(summaries, indent=2) + '\n')
    (out / 'attachment-review-index.json').write_text(json.dumps([r for r in normalized if r['source_sha256'] in reviews], indent=2, ensure_ascii=False) + '\n')
    # Prior calculations whose source bytes were not retained cannot be
    # recomputed using the common parser. Register rather than silently pool.
    legacy = []
    prior = ROOT.parent / 'form-corpus-2026-11-16'
    for p in sorted((prior / 'procedure-reference').glob('*-records.jsonl')):
        for row in map(json.loads, p.read_text().splitlines()):
            historical = p.name == 'procedure-historical-records.jsonl'
            if row.get('metrics') and (row.get('included_in_analysis') or historical):
                legacy.append({'source_record_file': str(p), 'id': row.get('requested_url') or row.get('canonical_url'), 'form_signal': row.get('genre'), 'doi': None, 'url': row.get('requested_url') or row.get('canonical_url'), 'prose_words_legacy': row['metrics']['prose_words'], 'separate_historical_pilot': historical, 'prior_screen_included': True})
    for name in ('records.jsonl', 'frontiers-records.jsonl'):
        p = prior / 'critical-theory' / name
        for row in map(json.loads, p.read_text().splitlines()):
            if row.get('measurement'):
                legacy.append({'source_record_file': str(p), 'id': row.get('id'), 'form_signal': row.get('form'), 'doi': doi_key(row.get('doi')), 'url': row.get('url'), 'prose_words_legacy': row['measurement']['main_prose_words'], 'separate_historical_pilot': False, 'prior_screen_included': name != 'frontiers-records.jsonl' or bool(row.get('discovery_source'))})
    for row in legacy:
        row['status'] = 'derived_only_not_harmonized_source_unavailable'
        row['possibly_linked_current_record_ids'] = [r['record_id'] for r in normalized if (row['doi'] and row['doi'] == r['doi']) or (row['id'] and row['id'] == r['pmcid']) or (row['url'] and url_key(row['url']) == url_key(r['source_url']))]
    (out / 'legacy-derived-register.json').write_text(json.dumps(legacy, indent=2, ensure_ascii=False) + '\n')
    counts = {
        'inventory_records_including_unavailable_and_held': len(normalized),
        'measured_source_records_before_work_dedup': sum(r['has_measurement'] for r in normalized),
        'measured_linked_work_groups': len({r['linked_work_id'] for r in normalized if r['has_measurement']}),
        'retained_unique_source_paths': len({r['source_path'] for r in normalized if r['source_path'] and Path(r['source_path']).is_file()}),
        'linked_version_groups': len(duplicates),
        'different_title_response_collision_groups': len(response_collisions),
        'profile_eligible': sum(r['profile_eligible'] for r in normalized),
        'by_parser': {name: {'records': sum(r['source_format'] == name for r in normalized), 'measured': sum(r['source_format'] == name and r['has_measurement'] for r in normalized), 'statuses': dict(Counter(r['status'] for r in normalized if r['source_format'] == name))} for name in ('xml', 'docs', 'html', 'pdf')},
        'manual_review': {'files': len(reviews), 'passage_annotations': sum(len(x.get('spans') or x.get('annotations') or []) for x in reviews.values())},
        'legacy_derived_only_records': len(legacy),
        'legacy_derived_records_in_prior_screened_samples': sum(r['prior_screen_included'] for r in legacy),
        'legacy_derived_only_by_form': dict(Counter(r['form_signal'] for r in legacy)),
        'legacy_derived_records_linking_to_current_inventory': sum(bool(r['possibly_linked_current_record_ids']) for r in legacy),
        'dedup_limit': 'Identity links are candidate work groups; unreviewed titles, versions, supplements and unresolved PDF identities can leave duplicates undetected. They do not assert unique complete articles.',
    }
    (out / 'coverage.json').write_text(json.dumps(counts, indent=2) + '\n')
    return counts


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
