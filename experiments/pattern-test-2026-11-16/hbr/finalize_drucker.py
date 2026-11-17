#!/usr/bin/env python3
"""Reproduce exploratory Drucker metadata from private reviewed reconstruction."""
import hashlib,json,pathlib,sys
BASE=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/hbr')
OUT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent.parent/'corpus-analysis-2026-11-16/analysis'))
from metrics import measure_document,summarize
items=json.loads((BASE/'drucker-coded-provisional.json').read_text())
sections=[('opening',1,3,None),('strengths',4,14,'What Are My Strengths?'),('performance',15,33,'How Do I Perform?'),('values',34,46,'What Are My Values?'),('belong',47,50,'Where Do I Belong?'),('contribution',51,55,'What Should I Contribute?'),('relationships',56,67,'Responsibility for Relationships'),('second-life',68,79,'The Second Half of Your Life'),('closing',80,81,None)]
blocks=[]; public=[]
for section,lo,hi,heading in sections:
 if heading: blocks.append({'kind':'heading','section_id':section,'heading_level':1,'text':heading})
 for row in items[lo-1:hi]:
  row['section_id']=section
  row['boundary_status']='reviewed_reconstruction_exploratory'
  row['label_status']='single_coder_interpretation'
  blocks.append({'kind':'paragraph','section_id':section,'text':row['text']})
  public.append({k:row[k] for k in ('id','source','sha256','functions','printed_heading','section_id','boundary_status','label_status')})
  public[-1]['span']={'start':0,'end':len(row['text']),'units':'unicode_codepoints_end_exclusive','text_field':'text in private record matching id'}
(BASE/'drucker-coded-reviewed.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
m=measure_document(blocks)
counts={k:m[k] for k in ('prose_words','prose_paragraphs','estimated_sentences','median_paragraph_words','median_sentence_words','headings','section_words','section_shares')}
counts['paragraph_word_distribution']=summarize(m['paragraph_word_counts'])
counts['paragraph_sentence_distribution']=summarize(m['paragraph_sentence_counts'])
counts['sentence_word_distribution']=summarize(m['sentence_word_counts'])
result={'status':'reviewed_reconstruction_exploratory','title':'Managing Oneself','source_sha256':'51a9cfd777119d78296e6691d44658f2c1dc3704bb46ec8c2a10fb7fd32a5f9b','private_text_path':str(BASE/'drucker-coded-reviewed.json'),'scope':'Publisher reprint main prose PDF pp. 3–12. Intro summary, pull quotes, author note, running furniture, reprint notice and further reading excluded. Inline speaker quotation counted as main prose. Headings excluded from prose; printed inline questions are retained as part of paragraphs.','method':'Read all source-ordered body text, viewed page renderings, joined paragraphs across columns/pages, normalized Unicode NFKC, joined wrapped words, collapsed whitespace and corrected observed short-term/long-term hyphenation. The normalized text is an exploratory reconstruction, not a transcription certified at character level. Function tags are a single coder judgment.','sections':[{'section_id':s,'first_id':f'drucker-{lo:03}','last_id':f'drucker-{hi:03}','heading':h,'heading_printed':h is not None,'inferred_role':('opening' if s=='opening' else 'closing' if s=='closing' else None)} for s,lo,hi,h in sections],'metrics':counts,'units':public}
(OUT/'drucker-reviewed.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(counts,indent=2))
