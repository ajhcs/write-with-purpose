#!/usr/bin/env python3
"""Index retained files and unresolved records without network requests."""

import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
CACHE = Path('/workspace/repos/builderbob/.writing-corpus-cache/fulltext').resolve()


def jsonlines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def rows():
    for domain, records in (
        ('business', jsonlines(ROOT / 'business/retrieval_manifest.jsonl')),
        ('engineering', jsonlines(ROOT / 'engineering/manifest.jsonl')),
        ('law', json.loads((ROOT / 'law/manifest.json').read_text())),
        ('personal', jsonlines(ROOT / 'personal/manifest.jsonl')),
    ):
        for record in records:
            retrieval = record.get('retrieval', record)
            path = retrieval.get('file') or retrieval.get('file_path') or ''
            identity = retrieval.get('source_identity') or {}
            candidate = bool(path)
            if domain == 'personal':
                candidate = bool(record.get('candidate_article_body_not_confirmed'))
            if record.get('held'):
                next_step = 'held source/type conflict; resolve before retrieval'
            elif str(record.get('status', '')).startswith('duplicate'):
                next_step = 'resolve linked duplicate in branch manifest'
            elif not path or not candidate:
                next_step = 'library/source lookup or deferred public route; no candidate body retained'
            else:
                next_step = 'review identity, access, version and completeness before corpus analysis'
            yield {
                'domain': domain,
                'record_id': record.get('source_id') or record.get('id') or '',
                'title': record.get('title', ''),
                'doi': record.get('doi') or '',
                'status': retrieval.get('status') or retrieval.get('result') or '',
                'candidate_article_file': candidate,
                'identity_status': identity.get('status', 'unavailable'),
                'identity_reason': identity.get('reason', ''),
                'title_author_agreement': record.get('title_author_agreement', ''),
                'completeness': record.get('body_completeness') or retrieval.get('completeness') or 'unverified',
                'policy_review_detail': json.dumps(record.get('robots_policy_audit', {}), ensure_ascii=False) if domain == 'personal' else '',
                'file': path,
                'file_sha256': retrieval.get('sha256') or retrieval.get('file_sha256') or '',
                'format': retrieval.get('mimeformat') or retrieval.get('media_type') or retrieval.get('content_type') or '',
                'final_url': retrieval.get('final_url') or '',
                'version': retrieval.get('version') or '',
                'next_step': next_step,
                'source_manifest': f'{domain}/' + ('manifest.json' if domain == 'law' else 'retrieval_manifest.jsonl' if domain == 'business' else 'manifest.jsonl'),
            }


def write_csv(name, records, fields):
    with (ROOT / name).open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract-pdf-text', action='store_true',
                        help='Create local text-layer sidecars with installed pdftotext; no OCR or cleaning.')
    args = parser.parse_args()
    records = list(rows())
    assert collections.Counter(r['domain'] for r in records) == {
        'business': 1200, 'engineering': 350, 'law': 494, 'personal': 316,
    }
    saved = [r for r in records if r['file']]
    candidate = [r for r in saved if r['candidate_article_file']]
    extraction = []
    observed = {}
    for row in saved:
        path = Path(row['file']).resolve()
        assert path.is_relative_to(CACHE), path
        assert path.is_file(), path
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == row['file_sha256'], (str(path), digest, row['file_sha256'])
        observed[str(path)] = digest
        if args.extract_pdf_text and path.suffix.lower() == '.pdf' and str(path) not in {r['source'] for r in extraction}:
            target = CACHE / 'text-layers' / (digest + '.txt')
            target.parent.mkdir(parents=True, exist_ok=True)
            result = {'source': str(path), 'source_sha256': digest,
                      'scope': 'PDF text layer only; no OCR, article cleaning or completeness assessment'}
            try:
                process = subprocess.run(['pdftotext', str(path), str(target)], capture_output=True, timeout=30)
                if process.returncode == 0:
                    text = target.read_bytes()
                    result.update(status='extracted' if text.strip() else 'empty_text_layer',
                                  text_file=str(target), text_bytes=len(text), text_sha256=hashlib.sha256(text).hexdigest())
                else:
                    result.update(status='extractor_failed', returncode=process.returncode)
            except (OSError, subprocess.TimeoutExpired) as error:
                result.update(status='extractor_unavailable_or_timeout', error=type(error).__name__)
            extraction.append(result)
    fields = list(records[0])
    write_csv('retrieval-status.csv', records, fields)
    write_csv('saved-files.csv', saved, fields)
    write_csv('candidate-article-files.csv', candidate, fields)
    write_csv('follow-up.csv', [r for r in records if not r['candidate_article_file'] or r['identity_status'] != 'consistent' or r['completeness'] != 'verified'], fields)
    index = ['# Downloaded candidate files', '',
             'Local source copies, grouped by discovery domain. Identity, version, completeness, form and access-policy review remain open as recorded in the manifests. These links do not constitute a validated corpus. Some copies are preprints or current presentations of older work.', '']
    for domain in ('business', 'engineering', 'law', 'personal'):
        index.extend([f'## {domain.title()}', ''])
        for row in candidate:
            if row['domain'] != domain:
                continue
            title = row['title'].replace('[', '\\[').replace(']', '\\]').replace('\n', ' ')
            index.append(f"- [{title}](<{row['file']}>) — identity: {row['identity_status']}; completeness unverified.")
        index.append('')
    (ROOT / 'downloaded-files.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    # Convenient citation import for library resolution. These are candidates, not an approved collection.
    ris = []
    seen = set()
    for row in records:
        if row['candidate_article_file'] or 'held' in row['next_step'] or 'duplicate' in row['next_step']:
            continue
        key = row['doi'].casefold() or row['title'].casefold()
        if key in seen:
            continue
        seen.add(key)
        clean = lambda value: ' '.join(str(value).split())
        item = ['TY  - GEN', 'TI  - ' + clean(row['title']), 'N1  - Unverified retrieval candidate; ' + clean(row['domain'])]
        if row['doi']:
            item.append('DO  - ' + clean(row['doi']).removeprefix('https://doi.org/'))
        if row['final_url']:
            item.append('UR  - ' + clean(row['final_url']))
        item.append('ER  -')
        ris.append('\n'.join(item))
    (ROOT / 'library-missing.ris').write_text('\n\n'.join(ris) + '\n', encoding='utf-8')
    receipt = {
        'source_records_accounted_for': len(records),
        'per_domain': {},
        'retained_file_records': len(saved),
        'unique_selected_paths': len(observed),
        'unique_selected_byte_hashes': len(set(observed.values())),
        'possible_article_file_records': len(candidate),
        'library_missing_ris_entries': len(ris),
        'scope': 'Saved record/file checks only. Raw captures include wrong/landing pages; candidate files and matching identity evidence do not certify completeness, version, genre, quality or permitted reuse. Counts are not unique works.',
    }
    for domain in ('business', 'engineering', 'law', 'personal'):
        group = [r for r in records if r['domain'] == domain]
        receipt['per_domain'][domain] = {
            'records': len(group),
            'saved_primary_file_records': sum(bool(r['file']) for r in group),
            'possible_article_file_records': sum(r['candidate_article_file'] for r in group),
            'identity_status_for_candidate_files': dict(collections.Counter(r['identity_status'] for r in group if r['candidate_article_file'])),
        }
    (ROOT / 'index-validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if args.extract_pdf_text:
        (ROOT / 'pdf-text-layers.json').write_text(json.dumps(extraction, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
