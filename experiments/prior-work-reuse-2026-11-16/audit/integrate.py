"""Rebuild generated bibliography/count receipts, preserving authored reports.

Run with Python 3. No network requests or third-party corpus code are executed.
The source archive remains in a persistent workspace cache outside the checkout.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import zipfile

BASE = Path(__file__).resolve().parent.parent
FIELDS = 'id title authors year kind doi primary_urls repository_url artifact_urls verified_scope baseline_status unit genres_or_forms annotation_or_metrics_available size_and_count_basis human_or_automatic reliability code_license annotation_license source_text_rights access_status reuse_recommendation project_feature_mapping limitations paywall_retrieval_record'.split()
SUBSTANTIVE = {'assumption', 'anecdote', 'testimony', 'statistics', 'common-ground', 'other'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def normalized_doi(value):
    match = re.search(r'10\.\d{4,9}/[^\s)]+', str(value or '').lower())
    return match.group(0).rstrip('.,;') if match else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=Path('/workspace/repos/builderbob/.writing-corpus-cache/prior-work-reuse-2026-11-16/webis-editorials-16.zip'))
    args = parser.parse_args()
    records, missing, inputs = [], [], []
    for path in sorted(BASE.glob('agents/*/findings.json')):
        data = json.loads(path.read_text())
        inputs.append({'path': str(path.relative_to(BASE)), 'sha256': digest(path)})
        for record in data['records']:
            absent = [field for field in FIELDS if field not in record]
            if absent:
                missing.append({'file': str(path.relative_to(BASE)), 'id': record.get('id'), 'fields': absent})
            records.append({'scout': data['scout'], 'source_file': str(path.relative_to(BASE)), 'record': record})
    groups = defaultdict(list)
    for item in records:
        key = normalized_doi(item['record'].get('doi'))
        if key:
            groups[key].append(item)
    unique, seen = [], set()
    for item in records:
        doi = normalized_doi(item['record'].get('doi'))
        key = ('doi', doi) if doi else ('scout-id', item['scout'], item['record']['id'])
        if key in seen:
            continue
        seen.add(key)
        occurrences = groups[doi] if doi else [item]
        unique.append({'canonical_record': item['record'], 'source_occurrences': [
            {'scout': other['scout'], 'source_file': other['source_file'], 'id': other['record']['id']}
            for other in occurrences]})
    write_json('merged-records.json', {
        'description': 'DOI-normalized scout bibliography; original records retained. Same-corpus releases and no-DOI aliases require manual family grouping, not independent sample counts. Parent-verified systems are separate in supplemental-systems.json.',
        'input_records': len(records), 'deduplicated_records': len(unique), 'records': unique})

    labels, fields, portals = Counter(), Counter(), Counter()
    empty, nonnumeric, duplicate = 0, 0, 0
    with zipfile.ZipFile(args.archive) as archive:
        names = [name for name in archive.namelist()
                 if '/annotated-txt/split-by-portal-final/' in name and name.endswith('.txt')]
        for name in names:
            portals[name.split('/')[-2]] += 1
            ids = set()
            for line in archive.read(name).decode('utf-8').splitlines():
                parts = line.split('\t')
                fields[str(len(parts))] += 1
                if len(parts) < 2:
                    continue
                label = parts[1]
                labels[label] += 1
                if label in SUBSTANTIVE:
                    empty += int(len(parts) < 3 or not '\t'.join(parts[2:]).strip())
                    nonnumeric += int(not parts[0].isdigit())
                    duplicate += int(parts[0] in ids)
                    ids.add(parts[0])
    proof = {
        'source': 'https://zenodo.org/records/3254405',
        'archive_local_path': str(args.archive.resolve()), 'archive_sha256': digest(args.archive),
        'scope': 'All TXT files under annotated-txt/split-by-portal-final; duplicate time-split omitted; UTF-8 physical lines; label is second tab-delimited field; extra tabs preserved in text. No source text included.',
        'files': len(names), 'files_by_portal': dict(portals),
        'rows_by_tab_field_count': dict(fields), 'row_labels': dict(labels),
        'six_substantive_label_rows': sum(labels[label] for label in SUBSTANTIVE),
        'upstream_reported_units': 14313,
        'difference_unresolved': '14,334 label rows versus 14,313 source-reported units; row != independently validated unit; version, segmentation and counting semantics need investigation. par-sep count is separator rows, not validated paragraph count.',
        'readme_path_note': 'README says split-by-portal; actual ZIP uses split-by-portal-final.',
        'limitations': 'No complete-text or underlying source-rights verification; other split organizations duplicate source documents.',
        'substantive_row_checks': {'empty_text_rows': empty, 'non_numeric_ids': nonnumeric,
                                   'duplicate_id_rows_within_same_document': duplicate,
                                   'scope': 'Substantive rows; IDs checked within each file, not across documents'}}
    write_json('audit/reusable-data-proof.json', proof)
    write_json('audit/checks.json', {
        'input_records': len(records), 'doi_deduplicated_records': len(unique),
        'input_files': inputs, 'missing_required_fields': missing,
        'duplicate_dois': {doi: [{'scout': item['scout'], 'id': item['record']['id']} for item in group]
                           for doi, group in groups.items() if len(group) > 1},
        'manual_families': ['GUM/GDTB/GENTLE/DISRPT share source documents or converted annotations',
                            'Webis 2016/2018 are related releases', 'WLP 2018/2020 overlap',
                            'BAWE classification and corpus share assignments', 'PERSUADE releases are related',
                            'RST-DT/PDTB/DiscAlign overlap WSJ material'],
        'proof': proof, 'source_status': 'See audit/report.md for independent source and scope checks; no claim of independent samples.'})
    print(json.dumps({'input': len(records), 'doi_unique': len(unique), 'missing_fields': missing,
                      'webis_files': len(names), 'substantive_rows': proof['six_substantive_label_rows']}))
    if missing:
        raise SystemExit('Required fields missing')


if __name__ == '__main__':
    main()
