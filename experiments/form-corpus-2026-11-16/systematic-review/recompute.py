#!/usr/bin/env python3
"""Recompute measured cached articles without changing the original screened cohort."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import build
p=Path(__file__).resolve().parent
metadata=build.search()['resultList']['result']
rows=[json.loads(s) for s in (p/'manifest.jsonl').read_text().splitlines()]
old=json.loads((p/'aggregate.json').read_text())
metrics=[]
for i,row in enumerate(rows):
    if row['status']!='measured': continue
    fresh,status,met=build.fetch(row['rank_in_search']-1,metadata[row['rank_in_search']-1])
    if status!='measured' or fresh['xml_sha256']!=row['xml_sha256']:
        raise RuntimeError(f"Recompute changed inclusion or XML for {row['pmcid']}: {status}")
    fresh['status']='measured'; rows[i]=fresh
    metrics.append({'pmcid':fresh['pmcid'],'rank_in_search':fresh['rank_in_search'],'year':fresh.get('year'),'meta_analysis_setting':fresh['meta_analysis_setting'],**met})
keys=['main_words','paragraphs','sentences_estimate','word_characters','citation_xrefs','figures','tables','lists','list_words','caption_words','references','abstract_words','title_words']
groups={'all':metrics}
for setting in ['with_meta_analysis','without_meta_analysis','uncertain']: groups[setting]=[x for x in metrics if x['meta_analysis_setting']==setting]
for era,lo,hi in [('pre_2015',0,2014),('2015_2019',2015,2019),('2020_onward',2020,9999)]: groups[era]=[x for x in metrics if str(x.get('year','')).isdigit() and lo<=int(x['year'])<=hi]
groups['year_unknown']=[x for x in metrics if not str(x.get('year','')).isdigit()]
old['statistics']={g:{'n':len(v),'metrics':{k:build.dist([x[k] for x in v]) for k in keys},'sentence_words':build.dist([p for x in v for p in x['sentence_word_counts']]),'paragraph_words':build.dist([p for x in v for p in x['paragraph_word_counts']]),'paragraph_sentences':build.dist([p for x in v for p in x['paragraph_sentence_estimates']]),'section_count':build.dist([len(x['sections']) for x in v])} for g,v in groups.items()}
old['search_retrieved_at_utc']=datetime.fromtimestamp((build.CACHE/'search.json').stat().st_mtime,timezone.utc).isoformat()
old['measurement_run_at_utc']=datetime.now(timezone.utc).isoformat()
(p/'manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(p/'metrics.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in metrics))
(p/'aggregate.json').write_text(json.dumps(old,indent=2,ensure_ascii=False)+'\n')
print('Recomputed cached cohort:',len(metrics), 'articles')
