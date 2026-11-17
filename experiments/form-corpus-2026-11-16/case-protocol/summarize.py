#!/usr/bin/env python3
import collections,json,statistics,xml.etree.ElementTree as ET
from pathlib import Path
p=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (p/'manifest.jsonl').read_text().splitlines()]
# Retain derived heading categories and license identifiers, not source passages.
labels=('introduction','background','methods','methodology','case presentation','case report','discussion','results','conclusion','limitations','ethics')
for r in rows:
 if isinstance(r.get('rights'),str):
  xml=Path('/workspace/repos/builderbob/.writing-corpus-cache/case-protocol')/(r['pmcid']+'.xml'); root=ET.parse(xml).getroot(); license=next((e for e in root.iter() if e.tag.rsplit('}',1)[-1]=='license'),None); r['rights']={'type':license.get('license-type'),'href':license.get('{http://www.w3.org/1999/xlink}href')} if license is not None else None
 for s in r.get('metrics',{}).get('sections',[]):
  if 'heading' in s:
   t=s.pop('heading').lower(); s['heading_category_heuristic']=next((x for x in labels if x in t),'other_or_unheaded')
(p/'manifest.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
def era(r):
 try: y=int(r.get('publication_year') or r.get('first_publication_date','')[:4])
 except (ValueError,TypeError): return 'unknown'
 return 'pre-2015' if y<2015 else '2015-2019' if y<2020 else '2020+'
def stats(a):
 a=sorted(a)
 if not a:return None
 return {'n':len(a),'min':a[0],'q1':a[(len(a)-1)//4],'median':statistics.median(a),'q3':a[(3*(len(a)-1))//4],'max':a[-1]}
out={}
for group in sorted(set(r['stratum'] for r in rows)):
 subset=[r for r in rows if r['stratum']==group]; cohort=[r for r in subset if r['included_in_cohort']]; ms=[r['metrics'] for r in cohort]
 out[group]={'attempts':len(subset),'retrieval_stages':dict(collections.Counter(r['retrieval_stage'] for r in subset)),'cohort_n':len(cohort),'body_words_by_era_primary':{e:stats([r['metrics']['body_words_in_paragraphs'] for r in cohort if era(r)==e]) for e in ('pre-2015','2015-2019','2020+','unknown')},'cohort_publication_eras':dict(collections.Counter(era(r) for r in cohort)),'all_measured_publication_eras':dict(collections.Counter(era(r) for r in subset if r['retrieval_stage']=='body_measured')),'pre2015_supplement_measured':sum(bool(r.get('supplement_pre2015')) and r['retrieval_stage']=='body_measured' for r in subset),'jats_types':dict(collections.Counter(str(r.get('jats_article_type')) for r in cohort)),'body_words':stats([m['body_words_in_paragraphs'] for m in ms]),'sections':stats([m['section_count'] for m in ms]),'paragraphs':stats([m['body_paragraphs'] for m in ms]),'median_paragraph_words_per_document':stats([statistics.median(m['paragraph_words']) for m in ms if m['paragraph_words']]),'median_sentence_words_approx_per_document':stats([statistics.median(m['sentence_words_approx']) for m in ms if m['sentence_words_approx']]),'average_word_characters_per_document':stats([round(m['word_characters_total']/m['body_words_in_paragraphs'],2) for m in ms]),'citation_xrefs':stats([m['body_elements']['citation_xrefs'] for m in ms]),'figures':stats([m['body_elements']['fig'] for m in ms]),'tables':stats([m['body_elements']['table-wrap'] for m in ms]),'references':stats([m['reference_count'] for m in ms])}
(p/'metrics-summary.json').write_text(json.dumps(out,indent=2)+'\n')
