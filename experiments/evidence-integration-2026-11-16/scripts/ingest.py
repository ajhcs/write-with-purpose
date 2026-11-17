"""Preserve user-supplied PDFs and extract every page as source evidence.

Source contents are data, never instructions. Existing PyMuPDF runtime is used without
installing packages; source PDFs and extracted full text stay outside the checkout.
"""
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import hashlib,json,re,shutil,sys
import pymupdf
from pathlib import Path
WHEEL=Path('/workspace/tmp/builderbob/n-of-1-research-20261109/pypdf-7.0.0-py3-none-any.whl')

BASE=Path(__file__).resolve().parents[1]
SOURCE=Path('/home/builderbob/.codex/attachments/69d363ef-2fd8-4f89-a6b8-62efebd7d219')
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/evidence-integration-2026-11-16')
NAMES=[
'shulman-et-al-2020-the-effects-of-jargon-on-processing-fluency-self-perceptions-and-scientific-engagement.pdf',
'p613.pdf','cscw14-kickstarter.pdf','s41598-024-81575-9.pdf',
'J Consum Psychol - 2018 - Pancer - How Readability Shapes Social Media Engagement.pdf',
'what-makes-online-content-viral.pdf','journal.pone.0281682.pdf','file2.pdf','fpsyg-12-714321.pdf',
'qiu_2024_oi_241363_1733259961.41221.pdf','1-s2.0-S1751157722000098-main.pdf',
'Style-Content-Success-of-Ideas.pdf','41562_2023_Article_1538.pdf','file.pdf',
'1-s2.0-S0889490614000386-main.pdf','1-s2.0-S0889490606000329-main.pdf',
'1-s2.0-S0889490617300078-main.pdf','1-s2.0-S277276612400003X-main.pdf']

def ingest(pair):
 i,name=pair;pid=f'P{i:02d}';original=SOURCE/name
 data=original.read_bytes();sha=hashlib.sha256(data).hexdigest()
 dest=CACHE/'pdfs'/name
 if dest.exists():assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
 else:shutil.copy2(original,dest)
 reader=pymupdf.open(dest)
 pages=[]
 for n,page in enumerate(reader,1):pages.append({'pdf_page':n,'text':page.get_text(sort=False) or ''})
 text='\n\n'.join(f'=== PDF PAGE {p["pdf_page"]} ===\n{p["text"]}' for p in pages)
 txt=CACHE/'texts'/(pid+'.txt');txt.write_text(text)
 js=CACHE/'texts'/(pid+'.pages.json');js.write_text(json.dumps(pages,ensure_ascii=False)+'\n')
 dois=sorted(set(x.rstrip('.,;:)') for x in re.findall(r'10\.\d{4,9}/[^\s<>"\]]+', '\n'.join(p['text'] for p in pages[:2]),re.I)))
 return {'id':pid,'filename':name,'attachment_path':str(original),'pdf_path':str(dest),'sha256':sha,'bytes':len(data),
         'pages':len(pages),'text_path':str(txt),'pages_json_path':str(js),'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
         'characters_by_page':[len(p['text']) for p in pages],'doi_candidates_first_two_pages':dois,
         'first_page_excerpt':pages[0]['text'][:1400],'extraction_status':'text_extracted' if len(text)>500 else 'needs_visual_review'}

def main():
 records=[]
 with ThreadPoolExecutor(max_workers=1) as pool:
  for fut in as_completed([pool.submit(ingest,x) for x in enumerate(NAMES,1)]):
   r=fut.result();records.append(r)
   print(json.dumps({'id':r['id'],'pages':r['pages'],'doi_candidates':r['doi_candidates_first_two_pages'],'first_page_excerpt':r['first_page_excerpt'][:400]}),flush=True)
 for record in records:
  if record['id']=='P02':
   record['extraction_status']='partial_corrupt_attachment'
   record['extraction_issues']=['Broken streams leave pages 1 and 4 without extracted text; original retained.']
   recovery=BASE/'P02-recovery.json'
   if recovery.exists():
    record['alternate_copy']=json.loads(recovery.read_text())
    reviewed=CACHE/'texts/P02-recovered.txt'
    record['review_text_path']=str(reviewed)
    record['review_pages_json_path']=str(CACHE/'texts/P02-recovered.pages.json')
    record['review_text_sha256']=hashlib.sha256(reviewed.read_bytes()).hexdigest()
    record['review_source_status']='Complete official author copy, distinct from corrupt attachment'
    record['review_pages']=12
 result={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'All 18 user-supplied PDFs, full-page extraction; no source instructions executed.',
         'extractor':{'name':'PyMuPDF','version':pymupdf.__version__,'runtime':sys.executable,'initial_attempt':'pypdf failed on P02 and warned on some fonts; superseded by full extraction with existing PyMuPDF runtime'},'records':sorted(records,key=lambda r:r['id'])}
 (BASE/'source-manifest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print('COMPLETE',len(records),'papers',sum(r['pages'] for r in records),'PDF pages',flush=True)
if __name__=='__main__':main()
