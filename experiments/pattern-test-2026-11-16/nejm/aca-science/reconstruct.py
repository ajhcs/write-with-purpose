import json, pathlib, re, hashlib, collections, statistics, sys
sys.path.insert(0,"/workspace/repos/builderbob/write-with-purpose/experiments/corpus-analysis-2026-11-16/analysis")
from metrics import word_tokens
root=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/nejm/aca-science'); out=pathlib.Path(__file__).parent
src=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis/attachments')
# Each tuple lists ordered (page, PyMuPDF block index); roles and functions are analyst judgments.
spec={
'NEJMp1616577':[
([(1,5),(1,6),(1,7)],'position and context',['orient','report','interpret','assert']),
([(1,8)],'reform record',['report','support']),([(1,9),(1,10)],'reform record',['report','support']),([(1,11),(2,4)],'reform limits',['qualify','report','assert']),
([(2,5)],'repeal proposal',['report','compare']),([(2,6),(2,7)],'consequences',['assert','explain','qualify']),([(2,8)],'repeal uncertainty',['assert','explain','illustrate']),([(2,9),(2,10)],'tradeoff example',['illustrate','explain','report']),([(2,11)],'repeal uncertainty',['qualify','report','support']),([(2,12)],'stakes',['assert','explain']),([(2,13),(3,4)],'recommended approach',['assert','illustrate']),([(3,5),(3,6)],'human stakes and closing',['illustrate','assert'])],
'NEJMp1702362':[
([(1,22),(1,23),(1,24),(2,4)],'clinical experience and problem',['narrate','orient','interpret']),([(2,5)],'political context',['assert','report','qualify']),([(2,6),(2,7)],'resistance question',['orient','assert','explain']),([(2,8),(2,9)],'belief and evidence',['assert','explain','report','support']),([(2,10)],'politicization and evidence',['assert','report','support']),([(2,11),(3,4)],'politicization risk',['interpret','illustrate','report']),([(3,5)],'identity mechanism',['explain','interpret']),([(3,6),(3,7)],'measured response',['explain','assert','illustrate']),([(3,8)],'response uncertainty',['qualify','compare','illustrate']),([(3,9),(3,10)],'closing call',['interpret','assert'])]}
def sha(s):return hashlib.sha256(s).hexdigest()
for id,items in spec.items():
 paragraphs=[]; chunks=[]; offset=0
 for n,(frags,role,labels) in enumerate(items,1):
  parts=[]; refs=[]
  for page,index in frags:
   b=json.loads((root/f'{id}-{page}.json').read_text())[index]; parts.append(b[4]); refs.append({'page':page,'block':index,'bbox_pdf_points':[round(v,2) for v in b[:4]],'block_text_sha256':sha(b[4].encode())})
  raw=''.join(parts)
  if n==1:
   dropindex=4 if id=='NEJMp1616577' else 21
   z=json.loads((root/f'{id}-1.json').read_text())[dropindex]
   refs.insert(0,{'page':1,'block':dropindex,'bbox_pdf_points':[round(v,2) for v in z[:4]],'block_text_sha256':sha(z[4].encode()),'role':'drop cap'})
   raw=z[4].strip()+raw
  # A line-final hyphen is often a layout break, but cannot always be distinguished from a lexical hyphen.
  ambiguous=re.findall(r'([\w]+)-\s*\n\s*([\w]+)',raw)
  text=re.sub(r'\u00ad\s*\n\s*','',raw); text=re.sub(r'(?<=high)-\s*\n\s*(?=quality)|(?<=identity)-\s*\n\s*(?=laden)|(?<=trade)-\s*\n\s*(?=offs)', '-', text); text=re.sub(r'-\s*\n\s*','',text); text=re.sub(r'\s+',' ',text).strip().replace('\u200b','').replace('\xad','')
  if chunks:offset+=2
  start=offset; offset+=len(text); chunks.append(text)
  paragraphs.append({'id':f'{id}-p{n:02}','start':start,'end_exclusive':offset,'sha256':sha(text.encode()),'fragments':refs,'section_role':role,'functions':labels,'coding_status':'single analyst; proposed labels','normalization_ambiguity':'trade-offs line-wrap spelling may also be tradeoffs; token count unchanged.' if ('trade','offs') in ambiguous else None,'quantitative_eligible':True,'word_count':len(word_tokens(text)),'line_end_hyphen_candidates':['-'.join(a) for a in ambiguous]})
 body='\n\n'.join(chunks); (root/f'{id}.body.txt').write_text(body,encoding='utf-8')
 data={'doi':'10.1056/'+id,'source_pdf':str(src/(id+'.pdf')),'raw_pdf_sha256':sha((src/(id+'.pdf')).read_bytes()),'body_text_path':str(root/f'{id}.body.txt'),'body_sha256':sha(body.encode()),'offset_units':'Unicode code points, end exclusive','normalization':'Ordered visual blocks; restore initial drop cap; remove line-wrap hyphens except identified compound hyphens; collapse whitespace; paragraphs separated by two newlines. Citation markers retained. Line-end hyphen status remains uncertain.','paragraph_boundary_status':'visually inspected by one analyst','quantitative_eligibility':True,'normalization_review':'Line-end candidates inspected individually. high-quality and identity-laden retain lexical hyphens; trade-offs retained with spelling ambiguity. Soft-hyphen wraps removed before hard-wrap processing.','paragraphs':paragraphs}
 (out/f'{id}-coding.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 counts=collections.Counter(f for p in paragraphs for f in p['functions'])
 metrics={'scope':'One visually reconstructed Perspective; not a genre norm.','paragraph_count':len(paragraphs),'function_counts_multilabel':dict(counts),'role_counts':dict(collections.Counter(p['section_role'] for p in paragraphs)),'body_words':sum(p['word_count'] for p in paragraphs),'paragraph_word_range':[min(p['word_count'] for p in paragraphs),max(p['word_count'] for p in paragraphs)],'paragraph_word_median':statistics.median(p['word_count'] for p in paragraphs),'role_words':{r:sum(p['word_count'] for p in paragraphs if p['section_role']==r) for r in set(p['section_role'] for p in paragraphs)},'word_count_note':'Citation markers retained and may affect counts.' + (' trade-offs spelling ambiguity does not affect token count.' if id=='NEJMp1616577' else ''),'word_count_method':'experiments/corpus-analysis-2026-11-16/analysis/metrics.py word_tokens','coding_status':'single analyst; interpretive and provisional'}
 (out/f'{id}-metrics.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n')
 print(id, len(paragraphs),sha(body.encode()))
