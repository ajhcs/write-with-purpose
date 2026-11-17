import pymupdf, re, hashlib, json, pathlib, sys
src=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis/attachments/NEJMp1901657.pdf')
cache=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/nejm/arb'); out=pathlib.Path('/workspace/repos/builderbob/write-with-purpose/experiments/pattern-test-2026-11-16/nejm/arb'); sys.path.insert(0,'/workspace/repos/builderbob/write-with-purpose/experiments/corpus-analysis-2026-11-16/analysis'); from metrics import word_tokens
pdf=pymupdf.open(src)
# Indices of PyMuPDF blocks in source reading order, selected against rendered pages.
blocks=[]
for pg in pdf:
 blocks.append([b for b in pg.get_text('blocks') if b[6]==0])
def b(page,x,y):
 a=[z for z in blocks[page-1] if abs(z[0]-x)<1 and abs(z[1]-y)<1]
 assert len(a)==1,(page,x,y,len(a)); return a[0]
coords=[[(1,101.7,325.8),(1,101.7,401),(1,250.4,401)],[(1,250.4,641),(1,399.1,329)],[(1,411.1,665),(2,71,364.8)],[(2,71,628.8),(2,219.7,364.8)],[(2,368.3,364.8)],[(2,368.3,544.8),(3,101.9,52.8)],[(3,101.9,220.8)],[(3,101.9,544.8),(3,101.9,580.8),(3,250.6,52.8)],[(3,250.6,148.8)],[(3,250.6,448.8)],[(3,262.6,664.8),(3,399.2,52.8)]]
functions=[['orient','report'],['qualify','report'],['define','report','explain'],['report','explain','qualify'],['report','explain'],['report','explain','interpret'],['report','explain'],['report','qualify','interpret'],['report','interpret'],['interpret','assert','explain'],['assert','interpret']]
roles=['recall and scope','recall and scope','impurity and manufacturing','impurity and manufacturing','consequences and response','consequences and response','consequences and response','oversight and preparedness','oversight and preparedness','oversight and preparedness','oversight and preparedness']
# Preserve real compound hyphens that happen to end a printed line.
keep={'ARB','nitro','N','drug'}
def norm(raw):
 raw=re.sub(r'\u00ad\s*\n\s*', '', raw).replace('\u00ad','').replace('\u200b','').replace('\ufeff','')
 raw=re.sub(r'([\w]+)-\s*\n\s*',lambda m:m.group(1)+('-' if m.group(1) in keep else ''),raw)
 return re.sub(r'\s+',' ',raw).strip()
paragraphs=[]; body=''
for i,parts in enumerate(coords):
 fr=[]; pieces=[]
 for page,x,y in parts:
  z=b(page,x,y); t=z[4]; pieces.append(t); fr.append({'page':page,'bbox':[round(v,2) for v in z[:4]],'source_text_sha256':hashlib.sha256(t.encode()).hexdigest()})
 raw='\n'.join(pieces)
 if i==0:
  z=b(1,101.7,312.1); fr.insert(0,{'page':1,'bbox':[round(v,2) for v in z[:4]],'source_text_sha256':hashlib.sha256(z[4].encode()).hexdigest(),'role':'drop cap'}); raw='A'+raw
 text=norm(raw); start=len(body); body+=text; end=len(body); body+='\n\n'
 paragraphs.append({'id':f'arb-p{i+1:02}','start':start,'end_exclusive':end,'offset_units':'unicode_codepoints','span_sha256':hashlib.sha256(text.encode()).hexdigest(),'source_fragments':fr,'functions':functions[i],'section_role':roles[i],'word_count':len(word_tokens(text)),'boundary_status':'visually checked source paragraph; joined source fragments','quantitative_eligible':True})
body=body.rstrip()+'\n'; (cache/'body.txt').write_text(body)
sections=[]
for role in dict.fromkeys(roles):
 ps=[p for p in paragraphs if p['section_role']==role]; sections.append({'role':role,'printed_heading':False,'paragraph_ids':[p['id'] for p in ps],'words':sum(p['word_count'] for p in ps)})
result={'title':'Hypertension Hot Potato — Anatomy of the Angiotensin-Receptor Blocker Recalls','year':2019,'doi':'10.1056/NEJMp1901657','source_path':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'body_text_path':str(cache/'body.txt'),'body_text_sha256':hashlib.sha256(body.encode()).hexdigest(),'body_scope':'Main prose from opening drop cap A to final period before disclosure; excludes title, byline, timeline and caption, disclosure, references, running matter and audio prompt.','source_validation':'All three PDF pages rendered and inspected; page 2 figure and page 3 audio prompt excluded; ordered blocks checked against three-column reading order.','normalization':'Whitespace collapsed, line-wrap hyphenation removed except explicit preserved compounds; zero-width and soft hyphens removed; paragraphs separated by blank lines.','word_count_method':'experiments/corpus-analysis-2026-11-16/analysis/metrics.py word_tokens','word_count':len(word_tokens(body)),'paragraph_count':len(paragraphs),'quantitative_eligible':True,'coding_status':'fully_coded_single_reviewer','sections':sections,'paragraphs':paragraphs}
(out/'article.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('\n'.join(f"{p['id']} {p['word_count']} {body[p['start']:p['start']+90]} ... {body[p['end_exclusive']-90:p['end_exclusive']]}" for p in paragraphs))
