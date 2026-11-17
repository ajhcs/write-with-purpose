import json,hashlib,collections,statistics
from pathlib import Path
out=Path('experiments/pattern-test-2026-11-16/systematic');cache=Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/systematic');docs=[]; funcs=['orient','define','report','assert','support','explain','illustrate','compare','interpret','qualify','instruct','narrate']; pool=collections.defaultdict(list);roles=collections.defaultdict(list);allp=[]
for f in sorted(out.glob('*-coding.json')):
 d=json.loads(f.read_text());id=d['document_id']; t=(cache/f'{id}.txt').read_text();raw=(cache/f'{id}.xml').read_bytes();assert hashlib.sha256(raw).hexdigest()==d['source_xml_sha256'];assert hashlib.sha256(t.encode()).hexdigest()==d['cache_sha256']; ss=collections.defaultdict(list)
 for p in d['paragraphs']:
  assert hashlib.sha256(t[p['start']:p['end']].encode()).hexdigest()==p['span_sha256'];ss[p['section_id']].append(p['word_count']);allp.append(p['word_count'])
  for fn in p['functions']:assert fn in funcs;pool[fn].append(p['word_count'])
 sections={s['id']:s for s in d['sections']}; sections[None]={'heading':None,'analyst_role':'introduction'}
 section_stats=[{'source_section_id':sid,'source_heading':sections[sid]['heading'],'analyst_role':sections[sid]['analyst_role'],'paragraphs':len(ws),'prose_words':sum(ws)} for sid,ws in ss.items()]
 totals=collections.defaultdict(int)
 for p in d['paragraphs']:totals[p['analyst_role']]+=p['word_count']
 for r in ['introduction','methods','results','discussion','conclusion']:roles[r].append(totals[r])
 docs.append({'id':id,'body_words':sum(p['word_count'] for p in d['paragraphs']),'paragraph_count':len(d['paragraphs']),'paragraph_median_words':statistics.median(p['word_count'] for p in d['paragraphs']),'role_words':dict(totals),'nonempty_source_sections':len(ss),'sections':section_stats})
def stats(v):return {'n':len(v),'min':min(v),'median':statistics.median(v),'max':max(v)} if v else {'n':0,'min':None,'median':None,'max':None}
a={'scope':'Eight selected pre-2015 biomedical-origin XML articles; prose only, including unheaded; one analyst, not generalizable or targets. Eight distinct eligible reviews; no false positive among selected.','word_count_rule':'Shared corpus-analysis metrics.py word_tokens; citation artifacts included.','body_words_across_documents':stats([d['body_words'] for d in docs]),'paragraphs_across_documents':stats([d['paragraph_count'] for d in docs]),'nonempty_source_sections_across_documents':stats([d['nonempty_source_sections'] for d in docs]),'role_words_across_documents_including_zero_for_absent':{r:stats(v) for r,v in roles.items()},'all_paragraph_word_lengths_pooled':stats(allp),'paragraph_word_lengths_by_overlapping_function':{f:stats(pool[f]) for f in funcs},'overlap_note':'Functions are multilabel; paragraphs appear in multiple subsets; these lengths are not additive budgets. Section counts are source section IDs with direct prose including unheaded group; not hierarchical totals.','documents':docs}
(out/'aggregate.json').write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in a.items() if k!='documents'},indent=2))
