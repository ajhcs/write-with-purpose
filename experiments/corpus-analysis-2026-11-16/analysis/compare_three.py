#!/usr/bin/env python3
"""Source-bound comparison of three supplied articles; no genre-wide norms."""
import hashlib
import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis')
OUT = ROOT / 'comparisons'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def movement(name, pages, printed, functions, purpose):
    return dict(name=name, pdf_pages=pages, printed_heading=printed,
                proposed_functions=functions, purpose=purpose)


def build():
    reviews = {}
    for kind in ('medical', 'nonmedical'):
        for r in json.loads((ROOT / 'review' / f'{kind}-uploads.json').read_text())['documents']:
            reviews[r['title']] = r
    specs = [
        {
            'id': 'nejm', 'filename': 'NEJMp1312793.pdf', 'title': 'Dead Man Walking',
            'original_year': 2013, 'family': 'Essays and commentary',
            'form': 'Argument / perspective', 'variant': 'Experience-led professional argument',
            'reader_question': 'What does this experience reveal, and what responsibility follows?',
            'source_boundary': 'PDF pp. 1–2. Start at target title on shared p. 1; end before disclosures on p. 2. Prior article and target references excluded.',
            'sections': [
                movement('Opening reaction and patient account', [1], False, ['assert', 'narrate', 'illustrate'], 'Give the authors’ response, then develop the encounter that motivates it.'),
                movement('Additional cases and wider evidence', [1, 2], False, ['report', 'illustrate', 'support', 'qualify'], 'Move beyond the individual case while limiting the counterfactual claim.'),
                movement('Policy setting and professional obligations', [2], False, ['orient', 'interpret', 'assert', 'support'], 'Connect the problem to physician responsibilities and three proposed responses.'),
                movement('Closing stakes', [2], False, ['report', 'interpret', 'assert'], 'Return to patients and the consequences that motivate the argument.'),
            ],
            'samples': [
                (2, 'However unconscionable', 'Elected officials', ['report', 'support', 'qualify'], 'Connects cited population evidence to the patient case while acknowledging that an individual counterfactual outcome is uncertain.'),
                (2, 'First, we can', 'Second, we can', ['assert', 'support'], 'Recommends professional responsibility and supplies ethical reasoning; not a reproducible action procedure.'),
            ],
            'blank_template': [
                'TITLE: [The tension or claim I want the reader to notice]',
                'OPENING: [My response or the problem that brought me to this piece]',
                'ENCOUNTER: [What happened, to whom, and what made it matter]',
                'BEYOND THIS CASE: [Other observations and relevant evidence]',
                'BOUNDARY: [What this case and evidence do not establish]',
                'POSITION: [What I think follows, and why]',
                'RESPONSES: [Who could do what, with reasons]',
                'CLOSING: [The stakes I want the reader to carry away]',
            ],
        },
        {
            'id': 'hbr', 'filename': 'What-Makes-a-Leader.pdf', 'title': 'What Makes a Leader?',
            'original_year': 1998, 'reprint_year': 2004, 'family': 'Essays and commentary',
            'form': 'Argument / perspective', 'variant': 'Practitioner argument organized by a proposed framework',
            'reader_question': 'What should I recognize, and how would it change my professional judgment?',
            'source_boundary': 'Main article PDF pp. 3–11; exclude reprint introduction, author bio, table/sidebar, pull quotes and order information from main-prose measurement. Summary on p. 2 and further reading on p. 12 are separate.',
            'sections': [
                movement('Unheaded opening', [3, 4], False, ['orient', 'compare', 'assert', 'qualify'], 'Contrast familiar outcomes and state the proposed distinction.'),
                movement('Evaluating Emotional Intelligence', [4, 5], True, ['report', 'support', 'explain'], 'Describe the author’s research basis and reported findings.'),
                movement('Self-Awareness; Self-Regulation; Motivation; Empathy; Social Skill', [5, 6, 7, 8, 9, 10, 11], True, ['define', 'explain', 'illustrate', 'compare', 'interpret'], 'Develop five named components through varying combinations of meaning, cases, signs and significance.'),
                movement('Unheaded closing', [11], False, ['assert', 'qualify'], 'Reassert the position and conditions on developing the capabilities.'),
            ],
            'samples': [
                (5, 'Self-awareness is the first', 'People who have a high degree', ['define', 'compare'], 'Defines a capability and distinguishes it from overly critical or unrealistically hopeful self-assessment.'),
                (7, 'Biological impulses drive', 'Imagine an executive', ['define', 'explain'], 'Defines self-regulation through a proposed relationship between impulses and behavior; the causal account is attributed to the author.'),
                (11, 'It is fortunate, then', 'Reprint R0401H', ['assert', 'qualify'], 'Ends with a claim of learnability conditioned on effort, time and commitment.'),
            ],
            'blank_template': [
                'TITLE: [The professional question I want to answer]',
                'OPENING: [A recognizable puzzle, contrast or problem]',
                'CENTRAL IDEA: [The distinction or framework I propose]',
                'BASIS: [Observations, research or reasoning that support it]',
                'REPEAT FOR EACH USEFUL COMPONENT — not necessarily five:',
                '  HEADING: [The component in my terms]',
                '  MEANING: [What it means and what it is often confused with]',
                '  CASE: [A sourced experience or explicitly hypothetical illustration]',
                '  CONNECTION: [Why this case makes the component useful]',
                '  RECOGNITION OR APPLICATION: [What the reader could notice or do]',
                '  CONDITION, IF NEEDED: [When the advice needs adjustment]',
                'CLOSING: [The judgment I want the reader to make; conditions on applying it]',
            ],
        },
        {
            'id': 'systematic', 'filename': 'PIIS0161642014004333.pdf',
            'title': 'Global Prevalence of Glaucoma and Projections of Glaucoma Burden through 2040: A Systematic Review and Meta-Analysis',
            'original_year': 2014, 'family': 'Evidence syntheses', 'form': 'Systematic review',
            'variant': 'Prevalence review using meta-analysis and projections',
            'reader_question': 'What does the selected evidence show, how was it obtained, and how certain is the interpretation?',
            'source_boundary': 'Main body PDF pp. 1–7. Structured abstract separate; acknowledgments, references and author information excluded. External appendices unavailable in supplied PDF.',
            'sections': [
                movement('Structured abstract', [1], True, ['orient', 'report', 'interpret'], 'Separate summary with Purpose, Design, Participants, Methods, Main Outcome Measures, Results and Conclusions.'),
                movement('Unheaded introduction', [1, 2], False, ['orient', 'compare', 'qualify', 'assert', 'explain'], 'Establish need, shortcomings of prior estimates, scope and rationale.'),
                movement('Methods', [2, 3], True, ['report', 'define', 'explain', 'qualify'], 'Describe search, eligibility, extraction and analytical decisions, including assumptions.'),
                movement('Results', [3, 4, 5], True, ['report', 'compare', 'qualify'], 'Report selection, included studies, estimates and subgroup patterns with scope and uncertainty.'),
                movement('Discussion, including Study Strengths and Limitations', [5, 6, 7], True, ['interpret', 'compare', 'explain', 'qualify'], 'Relate findings to prior estimates, possible explanations and constraints.'),
                movement('Unheaded concluding paragraph within Discussion', [7], False, ['report', 'interpret'], 'Restate the synthesis and its proposed use.'),
            ],
            'samples': [
                (2, 'The review followed', 'In our literature search', ['report'], 'Reports databases, publication-language scope and the actual final search date; it does not instruct the reader to run a search.'),
                (3, 'Table 2 shows', 'Variations in Glaucoma Prevalence', ['report'], 'Reports pooled estimates, named populations, uncertainty and a figure pointer rather than offering a personal reaction.'),
                (7, 'This review has a few limitations', 'In conclusion, our study', ['qualify', 'explain'], 'Connects geographical coverage, language selection, data availability and projection assumptions to interpretation.'),
            ],
            'blank_template': [
                'TITLE: [Question, scope and review design]',
                'ABSTRACT (placed first; finalize after the body): [A faithful summary matching the completed report and destination format]',
                'INTRODUCTION: [Why an answer is needed; gap; exact question]',
                'METHODS: [What was actually searched, selected, extracted, appraised and synthesized; dates and decisions]',
                'RESULTS: [Study flow; included evidence; findings; uncertainty and relevant differences]',
                'DISCUSSION: [What findings mean; comparison with prior work; limits; implications]',
                'CONCLUSION: [The answer justified by those findings]',
            ],
        },
    ]
    private = CACHE / 'comparison-nejm-hbr-systematic'
    private.mkdir(exist_ok=True)
    count = 0
    for spec in specs:
        source = CACHE / 'attachments' / spec['filename']
        source_sha = sha(source.read_bytes())
        assert source_sha == reviews[spec['title']]['source_sha256']
        spec['source_path'] = str(source)
        spec['source_sha256'] = source_sha
        spec['form_status'] = 'proposed_for_comparison_not_taxonomy_adoption'
        spec['function_assessment'] = 'single_model_interpretation_not_independent_agreement'
        spec['observed_range'] = None
        spec['working_target'] = None
        spec['declared_minimum'] = None
        spec['declared_maximum'] = None
        samples = []
        with pymupdf.open(source) as pdf:
            for i, (page, opening, next_opening, functions, explanation) in enumerate(spec.pop('samples'), 1):
                page_text = pdf[page-1].get_text()
                start = page_text.find(opening)
                end = page_text.find(next_opening, start + 1)
                assert start >= 0 and end > start, (spec['id'], page)
                span = page_text[start:end].rstrip()
                end = start + len(span)
                path = private / f'{spec["id"]}-p{page}.txt'
                path.write_text(page_text)
                samples.append(dict(id=f'{spec["id"]}-{i}', pdf_page=page,
                    page_text_path=str(path), page_text_sha256=sha(page_text.encode()),
                    start=start, end=end, offset_units='zero_based_end_exclusive_Unicode_codepoints',
                    span_sha256=sha(span.encode()), observed_functions=functions,
                    analysis=explanation, boundary_status='source-delimited paragraph sample; PDF line order remains representation-dependent'))
                count += 1
        spec['paragraph_samples'] = samples
    data = dict(schema_version='0.1', status='worked_comparison_not_genre_profile',
        source_selection='Three user-supplied examples with original publication years before 2015; no population sampling claim.',
        scope='Compare section structure and interpreted paragraph functions; no word-budget or reading-level inference.',
        template_policy='Blocks describe contributions, not mandatory paragraphs or source wording. Repeat, combine, reorder or omit when appropriate to the task. Research methods/results must come from actual records; mark gaps unresolved.',
        documents=specs)
    catalogue = json.loads((ROOT.parent.parent / 'docs/writing-harness/paragraph-functions.json').read_text())
    valid = {f['id'] for f in catalogue['functions']}
    for doc in specs:
        for section in doc['sections']:
            assert set(section['proposed_functions']) <= valid
        for sample in doc['paragraph_samples']:
            text = Path(sample['page_text_path']).read_text()
            assert sha(text.encode()) == sample['page_text_sha256']
            assert sha(text[sample['start']:sample['end']].encode()) == sample['span_sha256']
            assert set(sample['observed_functions']) <= valid
    OUT.mkdir(exist_ok=True)
    (OUT / 'nejm-hbr-systematic.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    worksheet = [
        'THREE WRITING STRUCTURES — WORKING BLANKS',
        '',
        'These are optional contribution blocks, not fixed paragraph counts.',
        'Combine or expand blocks; keep your own wording and reasoning.',
        'For the practitioner essay, choose components your subject needs.',
        'For a systematic review, fill methods and results from actual records.',
        'No observed word ranges, working budgets or hard limits are assigned.',
    ]
    for doc in specs:
        worksheet.extend(['', doc['variant'].upper(),
            f'Observed example: {doc["title"]} ({doc["original_year"]})',
            f'Family: {doc["family"]}; candidate form: {doc["form"]}',
            f'Reader question: {doc["reader_question"]}', '', *doc['blank_template']])
    (OUT / 'three-writing-templates.txt').write_text('\n'.join(worksheet) + '\n')
    print(json.dumps({'documents': len(specs), 'anchored_paragraph_samples': count,
        'source_hashes_verified': True, 'page_and_span_hashes_verified': True,
        'all_function_ids_registered': True, 'semantic_agreement_assessed': False}, indent=2))


if __name__ == '__main__':
    build()
