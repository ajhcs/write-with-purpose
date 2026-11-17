"""Additional bounded layout/OCR identity evidence; original assessments preserved."""
import concurrent.futures
import csv
import json
import re
import subprocess
from pathlib import Path
import retrieve as rt


def inspect(job):
    row,item=job;path=Path(item['path']);out=path.with_suffix('.inspection-v3.json')
    if out.exists():return json.loads(out.read_text())
    p=subprocess.run(['pdftotext','-layout','-f','1','-l','3',str(path),'-'],capture_output=True,text=True,timeout=30)
    text=p.stdout;method='pdftotext_layout_first_three_pages'
    if len(text.strip())<250:
        prefix=path.with_suffix('.ocr-page1')
        image=Path(str(prefix)+'.png')
        subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','2200','-png',str(path),str(prefix)],capture_output=True,timeout=40,check=True)
        ocr=subprocess.run(['tesseract',str(image),'stdout','--psm','3'],capture_output=True,text=True,timeout=40)
        text=ocr.stdout;method='tesseract_first_page_render'
    tp=path.with_suffix('.inspection.txt');tp.write_text(text)
    titles=[row['title']]
    # Candidate variants are recorded, not silently substituted in the bibliography.
    shortened=re.sub(r'^A piece of my mind\.\s*','',row['title'],flags=re.I)
    if shortened!=row['title']:titles.append(shortened)
    prefix_removed=re.sub(r'^(?:Letters to the editor:|From the Editors:|Colloquium\s*:|Narrative review:)\s*','',row['title'],flags=re.I)
    if prefix_removed!=row['title']:titles.append(prefix_removed)
    without_group=re.sub(r'\.\s+(?:Randomized Aldactone Evaluation Study Investigators|Modification of Diet in Renal Disease Study Group)\.\s*$','',row['title'],flags=re.I)
    if without_group!=row['title']:titles.append(without_group)
    hits=[]
    for page_number,page in enumerate(text.split('\f')[:3],1):
        front=rt.skill.first_page_front_matter(page)
        expected=rt.norm(row['title']);normalized=rt.norm(front)
        for variant in titles:
            match=rt.norm(variant)in normalized
            if match:hits.append({'page':page_number,'title_variant':variant,'exact_normalized_title_present':True})
    authors=json.loads(row['authors'])if row['authors']else[]
    author=authors[0]if authors else''
    author_tokens=rt.norm(author).split()
    raw_tokens=author.replace('.','').split()
    surname=author_tokens[:1] if len(raw_tokens)>1 and raw_tokens[-1].isupper() and len(raw_tokens[-1])<=4 else author_tokens[-1:]
    same_page=[]
    for hit in hits:
        page=text.split('\f')[hit['page']-1]
        front=rt.norm(rt.skill.first_page_front_matter(page))
        if surname and surname[0]in front.split():same_page.append(hit)
    first=rt.norm(text.split('\f')[0][:4500])
    result={'inspection_schema':3,'candidate_key':row['candidate_key'],'path':str(path),'sha256':rt.digest(path.read_bytes()),'method':method,'text_path':str(tp),'page_count':item.get('page_count'),'title_hits':hits,'title_author_same_page_hits':same_page,'first_author':author,'parsed_surname':surname,'first_author_surname_in_first_page':bool(surname and surname[0]in first.split()),'first_author_full_in_first_page':bool(author_tokens and rt.norm(author)in first),'scope':'First three layout-text pages, or first-page OCR; text presence is identity evidence, not completeness or exact-edition certification. Prefix/group removals are explicit title variants, not changed bibliography.'}
    rt.write_json(out,result);return result


def main():
    rows=list(csv.DictReader((rt.REPO/'experiments/library-expansion-2026-11-16/library-pull-list.csv').open()));lookup={r['candidate_key']:r for r in rows}
    jobs=[]
    for p in (rt.CACHE/'records').rglob('result.json'):
        rec=json.loads(p.read_text())
        for item in rec['files']:
            if item['format']=='pdf':jobs.append((lookup[rec['candidate_key']],item))
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
        for f in concurrent.futures.as_completed([pool.submit(inspect,j)for j in jobs]):
            try:results.append(f.result())
            except Exception as e:print(str(e),flush=True)
    rt.write_json(rt.ROOT/'file-inspections.json',results)
    print(json.dumps({'files':len(results),'title_hits':sum(bool(r['title_hits'])for r in results),'ocr_files':sum('tesseract'in r['method']for r in results)}))


if __name__=='__main__':main()
