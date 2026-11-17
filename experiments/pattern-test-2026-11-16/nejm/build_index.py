import json,sys,hashlib,pathlib,collections
sys.path.insert(0,'/workspace/repos/builderbob/write-with-purpose/experiments/corpus-analysis-2026-11-16/analysis')
from metrics import word_tokens
base=pathlib.Path(__file__).parent
spec=[('NEJMp1616577','Repealing the ACA without a Replacement — The Risks to American Health Care','aca-science/NEJMp1616577-coding.json',2017),('NEJMp1702362','Resisting the Suppression of Science','aca-science/NEJMp1702362-coding.json',2017),('NEJMp1707514','The Other End of the Stethoscope','narratives/NEJMp1707514-coding.json',2017),('NEJMp1711886','Tragedy, Perseverance, and Chance — The Story of CAR-T Therapy','narratives/NEJMp1711886-coding.json',2017),('NEJMp1901657','Hypertension Hot Potato — Anatomy of the Angiotensin-Receptor Blocker Recalls','arb/article.json',2019)]
docs=[];function_docs=collections.Counter()
for id,title,path,year in spec:
 d=json.loads((base/path).read_text()); source=d.get('source_pdf',d.get('source_path')); sh=d.get('source_pdf_sha256',d.get('raw_pdf_sha256',d.get('source_sha256'))); bodypath=d.get('normalized_body_path',d.get('body_text_path')); body=pathlib.Path(bodypath).read_text(); bh=d.get('normalized_body_sha256',d.get('body_sha256',d.get('body_text_sha256'))); assert hashlib.sha256(body.encode()).hexdigest()==bh; assert hashlib.sha256(pathlib.Path(source).read_bytes()).hexdigest()==sh
 paras=[]; sections=[]
 for p in d['paragraphs']:
  a=p['start']; b=p.get('end_exclusive',p.get('end')); h=p.get('sha256',p.get('span_sha256')); t=body[a:b]; assert hashlib.sha256(t.encode()).hexdigest()==h; assert len(word_tokens(t))==p['word_count']
  role=p.get('section_role',p.get('analyst_role')); para={'id':p['id'],'start':a,'end_exclusive':b,'span_sha256':h,'word_count':p['word_count'],'functions':p['functions'],'source_fragments':p.get('fragments',p.get('source_fragments')),'section_role':role,'quantitative_eligible':p.get('quantitative_eligible',p.get('paragraph_quant_eligible',True))}; paras.append(para)
  if sections and sections[-1]['role']==role: sections[-1]['paragraph_ids'].append(p['id'])
  else: sections.append({'role':role,'printed_heading':False,'role_status':'inferred by single analyst','paragraph_ids':[p['id']]})
 funcs=set(f for p in paras for f in p['functions']); function_docs.update(funcs)
 docs.append({'id':id,'title':title,'doi':'10.1056/'+id,'year':year,'source_path':source,'source_sha256':sh,'body_text_path':bodypath,'body_text_sha256':bh,'offset_units':'zero_based_unicode_codepoints_end_exclusive','coding_record':path,'body_word_tokens':len(word_tokens(body)),'paragraph_count':len(paras),'body_quantitative_eligible':d.get('body_quant_eligible',d.get('quantitative_eligibility',d.get('quantitative_eligible'))),'paragraph_quantitative_eligible':all(p['quantitative_eligible'] for p in paras),'sections':sections,'paragraphs':paras})
for function_id in ('orient','define','report','assert','support','explain','illustrate','compare','interpret','qualify','instruct','narrate'):
 function_docs.setdefault(function_id,0)
result={'scope':'Five independent articles selected from user-provided NEJM Perspectives 2017–2019; 2013 comparison article excluded. Convenience set, not population sample. Single analyst coding per article.','word_count_method':'experiments/corpus-analysis-2026-11-16/analysis/metrics.py word_tokens; inline citation markers retained','documents':docs,'function_presence_anywhere':{'denominator':len(docs),'counts':dict(sorted(function_docs.items())),'interpretation':'Number of documents with at least one paragraph bearing each proposed function label; not evidence of an ordered template. Labels coexist; not independent consensus.'},'ordered_hypothesis':'Not tallied mechanically: experiential opening, wider evidence, qualification, action, and stakes are interpretive section roles, not synonyms for paragraph-function labels. See report for document-level counterpatterns.'}
(base/'documents.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('docs',len(docs),'paras',sum(len(d['paragraphs']) for d in docs));print(result['function_presence_anywhere'])
