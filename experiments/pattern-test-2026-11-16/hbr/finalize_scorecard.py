#!/usr/bin/env python3
import json,pathlib,sys
BASE=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/hbr'); OUT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent.parent/'corpus-analysis-2026-11-16/analysis'))
from metrics import measure_document,summarize
items=json.loads((BASE/'scorecard-coded-reviewed.json').read_text())
sections=[('opening',1,11,None,0),('vision',12,15,'Translating the Vision',1),('communication',16,19,'Communicating and Linking',1),('educating',20,24,'Communicating and Educating.',2),('goals',25,26,'Setting Goals.',2),('rewards',27,32,'Linking Rewards to Performance Measures.',2),('planning',33,45,'Business Planning',1),('feedback',46,56,'Feedback and Learning',1),('closing',57,59,'Toward a New Strategic Management System',1)]
blocks=[]; public=[]
for sec,lo,hi,h,depth in sections:
 if h: blocks.append({'kind':'heading','section_id':sec,'heading_level':depth,'text':h})
 for row in items[lo-1:hi]:
  row['section_id']=sec; blocks.append({'kind':'paragraph','section_id':sec,'text':row['text']})
  if row['id']=='scorecard-057':
   for t in ['clarify and update strategy','communicate strategy throughout the company','align unit and individual goals with the strategy','link strategic objectives to long-term targets and annual budgets','identify and align strategic initiatives','conduct periodic performance reviews to learn about and improve strategy']:
    blocks.append({'kind':'list_item','text':t,'section_id':sec})
  u={k:row[k] for k in ('id','source','sha256','functions','printed_heading','section_id','boundary_status','label_status')}
  u['span']={'start':0,'end':len(row['text']),'units':'unicode_codepoints_end_exclusive','text_field':'text in private record matching id'}; public.append(u)
(BASE/'scorecard-coded-reviewed.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
m=measure_document(blocks)
counts={k:m[k] for k in ('prose_words','prose_paragraphs','estimated_sentences','median_paragraph_words','median_sentence_words','headings','list_words','section_words','section_shares')}
for output,key in [('paragraph_word_distribution','paragraph_word_counts'),('paragraph_sentence_distribution','paragraph_sentence_counts'),('sentence_word_distribution','sentence_word_counts')]: counts[output]=summarize(m[key])
result={'status':'reviewed_reconstruction_exploratory','title':'Using the Balanced Scorecard as a Strategic Management System','source_sha256':'7d86992e261841fc4c9695260a35f266a563bd3d26ffb1cc79210c2e989cd7d1','private_text_path':str(BASE/'scorecard-coded-reviewed.json'),'scope':'Publisher reprint main prose PDF pp. 3–13. Summary, author note, diagrams/exhibits, running furniture, and reprint notice excluded; ordinary inline quotation retained as prose. Six-item p. 13 list is separate from prose. Heading text excluded, including three run-in subheadings.','method':'Read all reconstructed prose and reviewed all page renderings; manually selected blocks based on column and diagram positions, joined cross-column/page continuations, normalized Unicode NFKC, joined wrapped words and repaired known meaningful compounds. Character-level normalization may contain remaining uncertainty. Function labels are a single coder interpretation.','sections':[{'section_id':s,'first_id':f'scorecard-{lo:03}','last_id':f'scorecard-{hi:03}','heading':h,'heading_printed':h is not None,'heading_level':depth if h else None} for s,lo,hi,h,depth in sections],'metrics':counts,'units':public,'list_evidence':{'page':13,'blocks':[6,7,8,9],'item_count':6,'treatment':'excluded from prose, included in list_words'},'figures_and_sidebar':{'treatment':'excluded from prose; present in source','examples':'PDF pp. 5–6, 8–12 contain diagrams and exhibits; summary p. 2, margin author note p. 4.'}}
(OUT/'scorecard-reviewed.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(counts,indent=2))
