"""Recover four source paragraphs and retain proposed, non-gold readings."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
PRIVATE = Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/disagreement-review')
sys.path.insert(0, str(ROOT.parent/'corpus-analysis-2026-11-16/analysis'))
from metrics import word_tokens

def read(path):
    return json.loads(Path(path).read_text())

specs = [
    ('NEJMp1616577-p10', 'NEJM: explanation or interpretation?',
     'Barack H. Obama, NEJM, 2017; supplied PDF p. 2',
     'https://doi.org/10.1056/NEJMp1616577',
     'Prefer interpret for the disputed job: this paragraph summarizes stakes developed in the preceding reasoning. It names consequences without developing their mechanism. Assert remains compatible. This is a proposed reading, not an exhaustive reference label set.'),
    ('drucker-034', 'HBR: orientation or instruction?',
     'Peter F. Drucker, Managing Oneself, 1999; supplied 2005 reprint, PDF p. 6',
     None,
     'Orientation and a directed self-question can coexist. Clarify whether reflective prompts count as instructions; a bare question heading and an actual request to examine oneself need contrasting examples. The distinction from ethics is limited clarification, not a complete definition of values.'),
    ('xml-02359-p018', 'Review: examples, definition and scope',
     'Cathal Doyle, Laura Lennox and Derek Bell, BMJ Open, 2013; Results paragraph',
     'https://doi.org/10.1136/bmjopen-2012-001570',
     'Proposed reading: report plus qualify plus illustrate. The denominator condition limits the table claim; the listed instances illustrate category contents without establishing complete category boundaries. Different clauses perform different jobs.'),
    ('drucker-007', 'HBR: history offered as support',
     'Peter F. Drucker, Managing Oneself, 1999; supplied 2005 reprint, PDF p. 4',
     None,
     'Reporting content, narrative organization, a causal explanation and intended support for the preceding feedback-analysis recommendation can coexist. Mark the claim being supported, then assess the truth and adequacy of the historical reasoning separately. Neither coding set establishes historical validity.'),
]
documents = read(ROOT/'results/documents.json')
comparisons = {p['id']:p for group in read(ROOT/'results/coding-agreement.json').values() for p in group['comparisons']}
PRIVATE.mkdir(exist_ok=True)
cases, public = [], []
def recover(p):
    pr=p['provenance']
    if pr.get('body_text_path'):
        return Path(pr['body_text_path']).read_text()[pr['start']:pr['end']]
    rows=read(pr['private_units'])
    rows=rows if isinstance(rows,list) else rows.get('units') or rows['paragraphs']
    return next(row['text'] for row in rows if row['id']==p['id'])

for pid,label,attribution,url,proposal in specs:
    doc=next(d for d in documents if any(p['id']==pid for p in d['paragraphs']))
    index=next(i for i,p in enumerate(doc['paragraphs']) if p['id']==pid)
    p=doc['paragraphs'][index]; text=recover(p)
    assert hashlib.sha256(text.encode()).hexdigest()==p['text_sha256']
    pair=comparisons[pid]
    original_rationale=None
    original_packet=p['provenance'].get('packet')
    if original_packet:
        packet_path=Path(original_packet)
        if not packet_path.is_absolute(): packet_path=ROOT/'nejm'/packet_path
        if packet_path.exists():
            original=read(packet_path)
            entry=next((row for row in original.get('paragraphs',[]) if row['id']==pid),{})
            original_rationale=entry.get('rationale')
    previous=recover(doc['paragraphs'][index-1]) if index else None
    following=recover(doc['paragraphs'][index+1]) if index+1<len(doc['paragraphs']) else None
    quote_file=PRIVATE/f'{pid}.txt'; quote_file.write_text(text+'\n')
    item=dict(id=pid,label=label,attribution=attribution,url=url,title=doc['title'],
        paragraph=text,previous=previous,following=following,words=p['words'],
        coder_a=pair['primary'],coder_b=pair['second'],
        coder_a_rationale=original_rationale,coder_b_rationale=pair['second_rationale'],
        coder_b_uncertainty=pair['second_uncertain'],
        proposal=proposal,source_path=doc['source_path'],source_sha256=doc['source_sha256'],
        paragraph_sha256=p['text_sha256'],provenance=p['provenance'],
        highlight=None,license_label=None,license_url=None)
    if pid=='xml-02359-p018':
        phrase='for 378 of the 556 cases where sufficient information was available to categorise'
        a=text.index(phrase);b=a+len(phrase)
        item['highlight']=dict(text=phrase,start=a,end=b,words=len(word_tokens(phrase)),label='Scope condition')
        item['license_label']='CC BY-NC 2.0'
        item['license_url']='https://creativecommons.org/licenses/by-nc/2.0/'
        assert item['highlight']['words']==13 and p['words']==113
    cases.append(item)
    public.append({k:v for k,v in item.items() if k not in {'paragraph','previous','following'}} | {'private_paragraph_path':str(quote_file),'status':'proposed_discussion_reading_not_gold_standard'})
(PRIVATE/'worked-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
(ROOT/'disagreement-review/worked-cases.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
template=ROOT/'disagreement-review/reader.fragment.html'
if template.exists():
    target=REPO/'work/visualizations/writing-coder-disagreements.html'
    fragment=template.read_text().replace('__CASE_DATA__',json.dumps(cases,ensure_ascii=False).replace('<','\\u003c'))
    assert '__CASE_DATA__' not in fragment and len(fragment.encode())<1000000
    target.write_text(fragment)
print(json.dumps({'cases':len(cases),'source_span_hashes_verified':True,'scope_words':13,'scope_paragraph_words':113,'original_codings_changed':False}))
