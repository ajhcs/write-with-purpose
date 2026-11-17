#!/usr/bin/env python3
"""Reconcile source packets and describe the held-out writing pilot."""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / 'corpus-analysis-2026-11-16/analysis'))
from metrics import word_tokens, summarize


def read(path):
    return json.loads(Path(path).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def clean_paragraph(p, text, section_id, role, provenance):
    labels = p['functions']
    assert len(labels) == len(set(labels)), p['id']
    return dict(id=p['id'], section_id=section_id, section_role=role,
                functions=labels, words=len(word_tokens(text)),
                text_sha256=sha(text.encode()), provenance=provenance,
                coding_status='single_primary_model_interpretation')


def load_documents():
    docs = []
    second_nejm = {r['document_id']: r for r in read(ROOT / 'review/nejm-second-coding.json')['articles']}
    for d in read(ROOT / 'nejm/documents.json')['documents']:
        text = Path(d['body_text_path']).read_text()
        assert sha(text.encode()) == d['body_text_sha256']
        sections = []
        assignment = {}
        for i, s in enumerate(d['sections']):
            sid = f's{i+1}'
            sections.append(dict(id=sid, source_heading=None, role=s['role'], printed=False))
            for pid in s['paragraph_ids']:
                assert pid not in assignment, pid
                assignment[pid] = (sid, s['role'])
        paragraphs = []
        for p in d['paragraphs']:
            span = text[p['start']:p['end_exclusive']]
            assert sha(span.encode()) == p['span_sha256']
            sid, role = assignment[p['id']]
            paragraphs.append(clean_paragraph(p, span, sid, role, dict(packet=d['coding_record'], start=p['start'], end=p['end_exclusive'], body_text_path=d['body_text_path'])))
        review = second_nejm[d['id']]
        docs.append(dict(id=d['id'], cohort='NEJM_publisher_Perspective', title=d['title'],
            year=d['year'], doi=d['doi'], source_path=d['source_path'], source_sha256=d['source_sha256'],
            source_packet=str(ROOT / 'nejm/documents.json'),
            primary_argument_eligible=review['primary_argument_eligible'],
            dominant_form=review['dominant_form'], form_rationale=review['form_rationale'],
            section_interpretation='All unheaded movements inferred by primary coder; not printed sections.',
            expected_words=d['body_word_tokens'], paragraphs=paragraphs, sections=sections))
    for d in read(ROOT / 'systematic/manifest.json'):
        coding_path = ROOT / 'systematic' / f'{d["id"]}-coding.json'
        coding = read(coding_path)
        text = Path(d['normalized_cache_path']).read_text()
        assert sha(text.encode()) == coding['cache_sha256']
        sections = [dict(id=s['id'], source_heading=s['heading'], role=s['analyst_role'],
                         printed=bool(s['heading'])) for s in coding['sections']]
        unheaded_roles = {p['analyst_role'] for p in coding['paragraphs'] if p['section_id'] is None}
        sections.extend(dict(id=f'__unheaded_{role}__', source_heading=None, role=role, printed=False) for role in sorted(unheaded_roles))
        paragraphs = []
        for p in coding['paragraphs']:
            span = text[p['start']:p['end']]
            assert sha(span.encode()) == p['span_sha256']
            assert len(word_tokens(span)) == p['word_count']
            sid = p['section_id'] if p['section_id'] is not None else f'__unheaded_{p["analyst_role"]}__'
            paragraphs.append(clean_paragraph(p, span, sid, p['analyst_role'], dict(packet=str(coding_path), body_text_path=d['normalized_cache_path'], start=p['start'], end=p['end'], xml_path=p['source_xml_path'])))
        docs.append(dict(id=d['id'], cohort='systematic_review', title=d['title'],
            year=int(d['earliest_reported_year']), doi=d['doi'], date_disagreement=d['date_disagreement'],
            source_path=d['source_path'], source_sha256=d['source_sha256'],
            source_packet=str(coding_path), primary_argument_eligible=False,
            dominant_form='systematic review', paragraphs=paragraphs, sections=sections,
            section_interpretation='Heading and analyst role distinct. Role budgets are disjoint prose: separate conclusion paragraphs are not also counted under discussion.'))
    for d in read(ROOT / 'hbr/documents.json')['documents']:
        if not d.get('metrics'):
            continue
        packet = read(d.get('normalized_units') or d['private_units'])
        units = packet if isinstance(packet, list) else packet.get('units') or packet['paragraphs']
        section_source = d['sections']
        ss = {s.get('section_id') or s.get('id'): s for s in section_source}
        sections = []
        for sid, s in ss.items():
            if sid is not None:
                heading = s.get('heading') or s.get('label')
                printed = s.get('heading_printed', s.get('type') == 'explicit')
                sections.append(dict(id=sid, source_heading=heading if printed else None,
                    role=s.get('inferred_role') or heading or sid, printed=printed))
        paragraphs = []
        for p in units:
            if p.get('kind', 'prose') not in ('prose', 'paragraph') or not p.get('metric_eligible', True):
                continue
            span = p['text']
            expected_sha = p.get('normalized_sha256') or p.get('sha256')
            assert sha(span.encode()) == expected_sha, p['id']
            sid = p.get('section_id') or p.get('section')
            section = ss.get(sid, {})
            role = section.get('inferred_role') or section.get('heading') or section.get('label') or sid
            # The two boundary-case packets record source headings and local
            # unit hints without a complete heading-to-unit registry. Keep
            # that as an explicit coverage gap; do not invent section budgets.
            source_section_hint = sid
            if sid not in ss or sid is None:
                sid, role = None, None
            paragraphs.append(clean_paragraph(p, span, sid, role,
                dict(private_units=d.get('normalized_units') or d['private_units'], unit_id=p['id'], source=d.get('public_units'), source_section_hint=source_section_hint)))
        assert len(paragraphs) == d['metrics']['prose_paragraphs'], d['id']
        docs.append(dict(id=d['id'], cohort='HBR_practitioner_argument' if d['primary_argument_eligible'] else 'HBR_procedure_tool_boundary',
            title=d['title'], year=d.get('original_year'), reprint_year=d.get('reprint_year'),
            source_path=d['source_path'], source_sha256=d['source_sha256'],
            source_packet=d['public_units'], primary_argument_eligible=d['primary_argument_eligible'],
            form_rationale=d['primary_argument_rationale'], expected_words=d['metrics']['prose_words'],
            section_interpretation='Actual assigned source headings; boundary-case paragraphs without source-specific assignment have no section-role budget.',
            source_heading_inventory=section_source,
            paragraphs=paragraphs, sections=sections))
    ids = set()
    for d in docs:
        assert sha(Path(d['source_path']).read_bytes()) == d['source_sha256']
        for p in d['paragraphs']:
            assert p['id'] not in ids
            ids.add(p['id'])
        d['prose_words'] = sum(p['words'] for p in d['paragraphs'])
        if 'expected_words' in d:
            assert d['expected_words'] == d['prose_words'], (d['id'], d['expected_words'], d['prose_words'])
    return docs


def summarize_cohort(docs, functions):
    paragraphs = [p for d in docs for p in d['paragraphs']]
    by_fn = {}
    for fn in functions:
        values = [p['words'] for p in paragraphs if fn in p['functions']]
        medians = []
        for d in docs:
            lengths = [p['words'] for p in d['paragraphs'] if fn in p['functions']]
            if lengths:
                medians.append(summarize(lengths)['median'])
        by_fn[fn] = dict(documents_present=len(medians), document_denominator=len(docs),
            tagged_paragraph_lengths=summarize(values), per_document_medians=summarize(medians))
    roles = defaultdict(list)
    headings = []
    for d in docs:
        role_words = defaultdict(int)
        section_words = defaultdict(int)
        for p in d['paragraphs']:
            if p['section_role']:
                role_words[p['section_role']] += p['words']
            section_words[p['section_id']] += p['words']
        for role, words in role_words.items():
            roles[role].append((d['id'], words, words / d['prose_words']))
        for s in d['sections']:
            if s['printed'] and section_words[s['id']]:
                headings.append(dict(document_id=d['id'], heading=s['source_heading'], words=section_words[s['id']]))
    return dict(range_kind='observed_pilot_only', working_targets=None, declared_limits=None,
        function_coding='Primary model interpretations; second-coder disagreements have not been adjudicated.',
        documents=len(docs), paragraph_count=len(paragraphs),
        document_words=summarize([d['prose_words'] for d in docs]),
        paragraphs_per_document=summarize([len(d['paragraphs']) for d in docs]),
        paragraph_words_pooled=summarize([p['words'] for p in paragraphs]),
        per_document_median_paragraph_words=summarize([summarize([p['words'] for p in d['paragraphs']])['median'] for d in docs]),
        function_lengths=by_fn,
        analyst_role_budgets={role:dict(documents_present=len(v), document_ids=[x[0] for x in v], words=summarize([x[1] for x in v]), proportion=summarize([x[2] for x in v])) for role, v in roles.items()},
        printed_sections=headings,
        caveats='Observed descriptive counts; roles interpreted. Multi-function paragraph lengths overlap and are not additive budgets. Role ranges conditional on presence; no zero is silently assigned to missing roles.')


def agreement(docs, functions):
    primary = {p['id']:p for d in docs for p in d['paragraphs']}
    results = {}
    for name in ('nejm', 'systematic', 'hbr'):
        second = read(ROOT / 'review' / f'{name}-second-coding.json')['paragraphs']
        assert len({p['id'] for p in second}) == len(second)
        rows = []
        for p in second:
            first = primary[p['id']]
            a, b = set(first['functions']), set(p['functions'])
            assert b <= set(functions)
            rows.append(dict(id=p['id'], primary=sorted(a), second=sorted(b),
                exact=a==b, jaccard=len(a & b)/len(a | b) if a | b else 1,
                second_uncertain=p.get('uncertain'), second_rationale=p.get('rationale')))
        results[name] = dict(compared_paragraphs=len(rows), exact_sets=sum(r['exact'] for r in rows),
            exact_set_fraction=sum(r['exact'] for r in rows)/len(rows),
            mean_jaccard=sum(r['jaccard'] for r in rows)/len(rows),
            primary_labels_not_adjudicated=True, comparisons=rows,
            interpretation='Agreement between two model coding passes on supplied paragraph boundaries, not human agreement or semantic validity. NEJM all paragraphs; other sources six deterministic targets per document.')
    return results


if __name__ == '__main__':
    functions = [f['id'] for f in read(ROOT.parent.parent / 'docs/writing-harness/paragraph-functions.json')['functions']]
    docs = load_documents()
    expected_groups = {'NEJM_publisher_Perspective': 5, 'HBR_practitioner_argument': 4,
                       'HBR_procedure_tool_boundary': 2, 'systematic_review': 8}
    assert dict(Counter(d['cohort'] for d in docs)) == expected_groups
    assert len({d['source_sha256'] for d in docs}) == 19
    development = read(ROOT.parent / 'corpus-analysis-2026-11-16/comparisons/nejm-hbr-systematic.json')['documents']
    assert not ({d['source_sha256'] for d in docs} & {d['source_sha256'] for d in development})
    title_key = lambda title: ''.join(c for c in title.casefold() if c.isalnum())
    assert not ({title_key(d['title']) for d in docs} & {title_key(d['title']) for d in development})
    development_dois = {'10.1056/nejmp1312793', '10.1016/j.ophtha.2014.05.013'}
    assert not ({d.get('doi', '').casefold() for d in docs} & development_dois)
    assert sum(len(d['paragraphs']) for d in docs) == 680
    for d in docs:
        section_ids = {s['id'] for s in d['sections']}
        d['paragraph_section_mapping_complete'] = all(p['section_id'] in section_ids for p in d['paragraphs'])
        assert d['paragraph_section_mapping_complete'] or d['cohort'] == 'HBR_procedure_tool_boundary'
        for p in d['paragraphs']:
            assert set(p['functions']) <= set(functions)
    groups = defaultdict(list)
    for d in docs:
        groups[d['cohort']].append(d)
    statistics = {name:summarize_cohort(ds, functions) for name, ds in groups.items()}
    (ROOT / 'results/documents.json').write_text(json.dumps(docs, indent=2, ensure_ascii=False)+'\n')
    (ROOT / 'results/statistics.json').write_text(json.dumps(statistics, indent=2, ensure_ascii=False)+'\n')
    compared = agreement(docs, functions)
    assert {k:v['compared_paragraphs'] for k,v in compared.items()} == {'nejm':54, 'systematic':48, 'hbr':36}
    (ROOT / 'results/coding-agreement.json').write_text(json.dumps(compared, indent=2, ensure_ascii=False)+'\n')
    validation = dict(status='passed', documents=len(docs), paragraphs=sum(len(d['paragraphs']) for d in docs),
        source_hashes_verified=len(docs), normalized_span_hashes_and_shared_token_counts=True,
        original_development_examples_excluded=True, independent_second_coded=sum(r['compared_paragraphs'] for r in compared.values()),
        complete_paragraph_section_mappings=sum(d['paragraph_section_mapping_complete'] for d in docs),
        boundary_documents_with_unmapped_section_assignments=[d['id'] for d in docs if not d['paragraph_section_mapping_complete']],
        semantic_validity_certified=False)
    validation['artifact_sha256'] = {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.suffix in ('.py','.md','.txt','.json') and p != ROOT/'results/validation.json'}
    (ROOT / 'results/validation.json').write_text(json.dumps(validation, indent=2)+'\n')
    print(json.dumps({k:v for k,v in validation.items() if k != 'artifact_sha256'}, indent=2))
