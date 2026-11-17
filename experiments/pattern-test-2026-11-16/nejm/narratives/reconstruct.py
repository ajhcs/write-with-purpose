import pymupdf as fitz, pathlib, re, json, hashlib, statistics, collections, importlib.util
spec=importlib.util.spec_from_file_location("corpus_metrics", "/workspace/repos/builderbob/write-with-purpose/experiments/corpus-analysis-2026-11-16/analysis/metrics.py")
metrics=importlib.util.module_from_spec(spec); spec.loader.exec_module(metrics)
out=pathlib.Path('/workspace/repos/builderbob/write-with-purpose/experiments/pattern-test-2026-11-16/nejm/narratives'); cache=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/nejm/narratives'); src=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis/attachments')
# Each tuple identifies a PDF page and the unique beginning of an extraction block, in reading order.
S={
'NEJMp1707514':[
([(1,'I\u200a'),(1,'receive a call'),(1,'tific openness'),(1,'His name is Master'),(2,'my own sorrow')],['narrate','interpret'],'opening diagnosis and call'),
([(2,'My mother calls')],['narrate','interpret'],'family and travel'),
([(2,'The air in Atlanta'),(2,'he sees me first')],['narrate','report'],'hospital encounter'),
([(2,'At 3 a.m.'),(2,'phlebotomy cart')],['narrate','report'],'hospital encounter'),
([(2,'In the morning'),(2,'pressed, and clean'),(2,'better equipped')],['narrate','interpret'],'hospital encounter'),
([(2,'Later I return')],['narrate','interpret'],'care relationship'),
([(2,'At first I walk')],['narrate'],'care relationship'),
([(2,'My father is back'),(3,'strength of its methods'),(3,'tain methodology'),(3,'your life and your death')],['narrate','interpret','qualify'],'recovery and reflection')],
'NEJMp1711886':[
([(1,'I\u200a'),(1,'n 2010')],['narrate','report'],'patient and treatment history'),
([(1,'Unfortunately, a clinical trial'),(1,'study that wouldn’t')],['narrate','report'],'patient and treatment history'),
([(1,'But her parents opted')],['narrate','report','qualify'],'treatment and approval'),
([(1,'The approval is probably'),(1,'lymphocytic leukemia')],['report','qualify'],'treatment and approval'),
([(1,'The emergence of CAR-T')],['report','interpret'],'development history'),
([(1,'As Carl June'),(2,'munotherapy.')],['narrate','report'],'development history'),
([(2,'The translational hurdles'),(2,'fund a clinical trial'),(2,'ous nature of anecdote')],['narrate','report','qualify'],'development history'),
([(2,'Indeed, anecdote'),(2,'pal investigator')],['report','interpret','qualify'],'trial risk and uncertainty'),
([(2,'Emily Whitehead was'),(2,'derstood to be')],['narrate','report','qualify'],'trial experience'),
([(2,'That she survived')],['narrate','explain','interpret'],'trial experience'),
([(2,'Once again, they got lucky'),(3,'Emily received a dose')],['narrate','report'],'treatment and response'),
([(3,'Though the remissions'),(3,'duction of a CAR')],['qualify','explain','report'],'technical limits'),
([(3,'Meanwhile, the CAR-T'),(3,'it’s the hope')],['report','compare','qualify','interpret'],'cost and closing reflection')]
}
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):
 s=re.sub(r'\u00ad\s*\n\s*', '', s); s=s.replace('\u00ad','').replace('\u200a','').replace('\u200b','').replace('\xa0',' ')
 # Undo discretionary line-wrap hyphens; preserve explicit compounds when known.
 s=re.sub(r'-\s*\n\s*', '¬',s)
 s=re.sub(r'\s+',' ',s).strip().replace('¬','')
 return s
for id,ps in S.items():
 pdf=src/(id+'.pdf'); doc=fitz.open(pdf); full=''; records=[]
 for i,(frags,labels,role) in enumerate(ps,1):
  chunks=[]; prov=[]
  for page,prefix in frags:
   matches=[b for b in doc[page-1].get_text('blocks') if b[4].startswith(prefix)]
   assert len(matches)==1,(id,page,prefix,len(matches))
   b=matches[0]; chunks.append(b[4]); prov.append({'page':page,'bbox':[round(x,2) for x in b[:4]],'raw_block_sha256':sha(b[4].encode())})
  # Join first, so line wrapping at a block/column boundary is resolved as within a block.
  raw=''.join(chunks); text=norm(raw)
  if id=='NEJMp1707514' and i==1: text='I '+text[1:].lstrip()
  if id=='NEJMp1711886' and i==1: text='In '+text[3:].lstrip() # drop cap is a separate block
  # Preserve source compound hyphens broken at line endings.
  for a,b in [('Penndeveloped','Penn-developed'),('taxpayersupported','taxpayer-supported'),('CAR T','CAR-T'),('CAR-Tcell','CAR-T cell'),('Bcell','B-cell'),('Tcell','T-cell'),('1000fold','1000-fold'),('lowestpaid','lowest-paid'),('postop','post-op'),('nonHodgkin','non-Hodgkin'),('interleukin6','interleukin-6'),('5yearold','5-year-old'),('41yearold','41-year-old'),('12yearold','12-year-old')]: text=text.replace(a,b)
  start=len(full); full+=text; end=len(full); full+='\n\n'
  records.append({'id':f'{id}-p{i:03}','start':start,'end':end,'sha256':sha(text.encode()),'fragments':prov,'functions':labels,'analyst_role':role,'status':'coded_single_analyst','word_count':len(metrics.word_tokens(text)), 'paragraph_quant_eligible': True})
 (cache/f'{id}.txt').write_text(full,encoding='utf8')
 d={'document_id':id,'source_pdf':str(pdf),'source_pdf_sha256':sha(pdf.read_bytes()),'normalized_body_path':str(cache/f'{id}.txt'),'normalized_body_sha256':sha(full.encode()),'offset_units':'zero-based Unicode code points, end-exclusive','scope':'Main-body paragraphs; excludes adjacent article, title, byline, running matter, graphics, pull quotes, references and disclosures.','normalization':'Join fragments in reading order; remove extraction soft hyphens and discretionary line-end hyphens; normalize whitespace; restore selected compound hyphens. Superscript reference numbers retained inline.','verification':'Single analyst visually inspected all six rendered pages and paragraph boundaries and reviewed every extracted line-end hyphen. The PDF extraction retains superscript reference numerals inline; token counts include them.', 'body_quant_eligible': True, 'paragraph_quant_eligible': True, 'ambiguities': [],'paragraphs':records}
 (out/f'{id}-coding.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
 w=[p['word_count'] for p in records]; counts=collections.Counter(f for p in records for f in p['functions'])
 m={'document_id':id,'paragraph_count':len(w),'body_words':sum(w),'paragraph_word_range':[min(w),max(w)],'paragraph_word_median':statistics.median(w),'word_rule':'experiments/corpus-analysis-2026-11-16/analysis/metrics.py word_tokens; reference numbers included','function_counts_multilabel':dict(counts),'body_quant_eligible':True,'paragraph_quant_eligible':True,'status':'Single-analyst visual reconstruction; inline reference numerals are included in token counts.'}
 (out/f'{id}-metrics.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
 print(id,len(w),sum(w),sha(pdf.read_bytes()))
