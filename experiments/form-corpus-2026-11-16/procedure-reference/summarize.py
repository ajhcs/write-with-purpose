#!/usr/bin/env python3
import collections,json,statistics
from pathlib import Path
p=Path(__file__).resolve().parent

def dist(a):
 a=sorted(a)
 if not a:return None
 return {'n':len(a),'min':a[0],'p25':a[round((len(a)-1)*.25)],'median':statistics.median(a),'p75':a[round((len(a)-1)*.75)],'max':a[-1]}
output={}
for genre in ['procedure','reference']:
 rows=[json.loads(x) for filename in [genre+'-records.jsonl',genre+'-supplement-records.jsonl'] for x in (p/filename).read_text().splitlines()]
 selected=[r for r in rows if r['included_in_analysis']]
 get=lambda f:[f(r['metrics']) for r in selected]
 output[genre]={'candidate_count':sum(len(json.loads((p/(genre+suffix)).read_text())) for suffix in ['-candidates.json','-supplement-candidates.json']),'attempted':len(rows),'mechanically_accepted':sum(bool(r.get('accepted')) for r in rows),'manually_title_excluded':sorted(r['title'] for r in rows if r['title_screen_status']=='excluded_by_title_screen'),'selected_still_provisional':len(selected),'type_counts':dict(collections.Counter(r['original_type'] for r in selected)), 'prose_words_per_page':dist(get(lambda m:m['prose_words'])),'paragraph_words_page_median':dist(get(lambda m:m['paragraph_word_distribution'].get('median',0))),'sentence_words_page_median':dist(get(lambda m:m['sentence_word_distribution'].get('median',0))),'headings_per_page':dist(get(lambda m:m['heading_count'])),'list_items_per_page':dist(get(lambda m:m['list_item_count'])),'code_blocks_per_page':dist(get(lambda m:m['code_block_count'])),'tables_per_page':dist(get(lambda m:m['table_count'])),'example_headings_per_page':dist(get(lambda m:m['example_heading_count'])),'list_word_share_of_prose_list_code':dist(get(lambda m:round(m['list_words']/(m['prose_words']+m['list_words']+m['code_words']),3))),'code_word_share_of_prose_list_code':dist(get(lambda m:round(m['code_words']/(m['prose_words']+m['list_words']+m['code_words']),3)))}
(p/'aggregate.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
