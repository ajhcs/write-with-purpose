#!/usr/bin/env python3
"""Append pinned tutorial-source candidates from independent project archives."""
import ast, csv, datetime, hashlib, io, json, re, tarfile, tokenize
from pathlib import Path
from markdown_it import MarkdownIt
H=Path(__file__).resolve().parent; C=Path('/workspace/tmp/builderbob/writing-corpus/explanation-tutorial'); A=C/'archives'; stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
# Reuse only definitions, not collection side effects.
tree=ast.parse((H/'collect.py').read_text()); names={'words','textinline','measure'}; nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names]; module=ast.Module(body=nodes,type_ignores=[]); env={'re':re,'md':MarkdownIt('commonmark').enable('table'),'wordre':re.compile(r"[A-Za-z]+(?:['’\-][A-Za-z]+)*|\d+(?:\.\d+)?")};exec(compile(module,str(H/'collect.py'),'exec'),env); measure=env['measure']
configs=[('tensorflow-docs.tar.gz','tensorflow/docs','82158b810d30edc737411744e27a0801fdad4554','Apache-2.0'),('pytorch-tutorials.tar.gz','pytorch/tutorials','5277794075fd393cf24f139ac978f96bc06b5aa3','BSD-3-Clause'),('ros2-jazzy.tar.gz','ros2/ros2_documentation','929e37c4c6d0746e75d10f1fd76f024743ff75ea','CC-BY-4.0'),('diffusers.tar.gz','huggingface/diffusers','43e30028af5120d8b0868cb6975b9fad39cc4fab','Apache-2.0')]
def rst_to_markdown(s):
 lines=s.splitlines(); out=[]; code=0; figures=0; omitted=0; i=0
 while i<len(lines):
  line=lines[i]; stripped=line.strip()
  if re.match(r'^\.\.\s+(?:code-block|sourcecode|parsed-literal)::',stripped):code+=1
  if re.match(r'^\.\.\s+(?:image|figure)::',stripped):figures+=1
  if re.match(r'^\.\.\s',stripped):
   omitted+=1; i+=1
   while i<len(lines) and (not lines[i].strip() or lines[i][:1].isspace()):i+=1
   continue
  if i+1<len(lines) and stripped and re.fullmatch(r'[=\-~^"`:+*#]{3,}\s*',lines[i+1].strip()):
   mark=lines[i+1].strip()[0]; level={'=':1,'-':2,'~':3,'^':3}.get(mark,3);out.extend(['#'*level+' '+stripped,'']);i+=2;continue
  # RST inline roles and references retain displayed text; literal code is excluded by Markdown parser.
  line=re.sub(r':\w+:`([^`<>]+)\s*<[^>]+>`',r'\1',line);line=re.sub(r':\w+:`([^`]+)`',r'\1',line)
  out.append(line);i+=1
 return '\n'.join(out),code,figures,omitted
def py_to_markdown(s):
 try:
  parsed=ast.parse(s); doc=ast.get_docstring(parsed) or ''
  comments=[]
  for tok in tokenize.generate_tokens(io.StringIO(s).readline):
   if tok.type==tokenize.COMMENT and tok.start[1]==0:
    value=tok.string[1:].lstrip(); comments.append('' if re.fullmatch(r'[%#=\-]{3,}',value) else value)
  return doc+'\n\n'+'\n'.join(comments), len([x for x in parsed.body if not isinstance(x,(ast.Expr,ast.Import,ast.ImportFrom))])
 except (SyntaxError,tokenize.TokenError,IndentationError):return '',0

def make(repo,sha,path,license,data,kind):
 source=data.decode('utf-8'); code=figures=omitted=0
 if kind=='notebook':
  try: nb=json.loads(source)
  except ValueError:return None
  cells=nb.get('cells',[]); text='\n\n'.join(''.join(c.get('source',[])) for c in cells if c.get('cell_type')=='markdown');code=sum(c.get('cell_type')=='code' for c in cells)
 elif kind=='rst':text,code,figures,omitted=rst_to_markdown(source)
 elif kind=='sphinx-gallery':text,code=py_to_markdown(source)
 else:text=source
 m=measure(text)
 if kind=='sphinx-gallery': m['python_top_level_non_import_statements']=code; m['code_blocks']=None
 else: m['code_blocks']+=code
 m['images']+=figures;m['unexpanded_directives']=omitted
 title=re.search(r'^#\s+(.+)$',text,re.M); title=title.group(1).strip() if title else Path(path).stem.replace('_',' ').replace('-',' ')
 url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'; (C/hashlib.sha256(url.encode()).hexdigest()).write_bytes(data)
 status='candidate_source_typed_needs_human_review' if m['prose_words']>=120 else 'excluded_under_120_prose_words_or_fragment'
 return dict(id=hashlib.sha256(url.encode()).hexdigest()[:16],repo=repo,path=path,source_url=f'https://github.com/{repo}/blob/{sha}/{path}',raw_url=url,commit=sha,title=title,original_type='official tutorial source',proposed_form='tutorial',classification_basis='official tutorial collection; page purpose and suitability require human review',attribution=repo+' project contributors',license_spdx=license,sha256=hashlib.sha256(data).hexdigest(),retrieved_at_utc=stamp,selection_signal='source-owner-maintained documentation; no readership/citation ranking',unit='individual documentation page or tutorial notebook',acquisition_stage='pinned git archive full source; rendered output and transclusions not expanded',source_format=kind,screening_status=status,metrics=m)
rs=[]
for filename,repo,sha,license in configs:
 with tarfile.open(A/filename) as tar:
  for member in tar:
   if not member.isfile():continue
   path=member.name.split('/',1)[-1]; kind=None
   if repo=='tensorflow/docs' and re.fullmatch(r'site/en/tutorials/.+\.ipynb',path):kind='notebook'
   elif repo=='pytorch/tutorials' and re.fullmatch(r'(beginner|intermediate|advanced)_source/[^/]+\.py',path):kind='sphinx-gallery'
   elif repo=='ros2/ros2_documentation' and re.fullmatch(r'source/Tutorials/.+\.rst',path):
    # A published learning-goal or tutorial-level marker distinguishes lesson candidates from directory pages.
    data=tar.extractfile(member).read(); src=data.decode('utf-8')
    if re.search(r'\*\*(?:Tutorial level|Goal):\*\*',src,re.I):kind='rst'
   elif repo=='huggingface/diffusers' and re.fullmatch(r'docs/source/en/tutorials/[^/]+\.md',path):kind='markdown'
   if kind:
    if not (repo=='ros2/ros2_documentation'):data=tar.extractfile(member).read()
    r=make(repo,sha,path,license,data,kind)
    if r:rs.append(r)
old=[json.loads(x) for x in (H/'records.jsonl').read_text().splitlines()]; old=[r for r in old if r['repo'] not in {c[1] for c in configs}]; rows=old+rs
with (H/'records.jsonl').open('w') as f:
 for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
with (H/'measurements.csv').open() as f:cols=next(csv.reader(f))
with (H/'measurements.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader()
 for r in rows:w.writerow({**r,**r.get('metrics',{})})
meta=json.loads((H/'sources.json').read_text()); meta['archive_sources']=[dict(repo=repo,commit=sha,license_spdx=license,archive=f'https://codeload.github.com/{repo}/tar.gz/{sha}',archive_sha256=hashlib.sha256((A/filename).read_bytes()).hexdigest(),retrieved_at_utc=stamp,selection_signal='official project tutorial source directory; individual pages require review') for filename,repo,sha,license in configs];(H/'sources.json').write_text(json.dumps(meta,indent=2)+'\n')
from collections import Counter
print('Added',len(rs),Counter((r['repo'],r['screening_status']) for r in rs));print('All candidates',Counter(r['proposed_form'] for r in rows if r['screening_status'].startswith('candidate')))
