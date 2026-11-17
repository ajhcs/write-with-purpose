import csv, json, os, hashlib, shutil, xml.etree.ElementTree as ET
from pathlib import Path
root=Path('/workspace/repos/builderbob/write-with-purpose')
out=root/'experiments/pattern-test-2026-11-16/nejm'
cache=Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/nejm')
cache.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(open(root/'experiments/corpus-analysis-2026-11-16/results/document-inventory.csv')))
results=[]; missing=[]; errors=[]
for r in rows:
 if r['source_format']!='xml': continue
 p=Path(r['source_path'])
 if not p.exists(): missing.append(str(p)); continue
 try:
  x=ET.parse(p).getroot()
  journal=' '.join(''.join(e.itertext()) for e in x.findall('.//journal-title'))
  ids=' '.join(''.join(e.itertext()) for e in x.findall('.//journal-id'))
  if 'new england journal of medicine' not in journal.lower() and 'n engl j med' not in (journal+' '+ids).lower(): continue
  results.append(dict(doi=r['doi'],category_assessment='unconfirmed without publisher verification; no NEJMp DOI or explicit Perspective subject',record_id=r['record_id'],source_path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),title=r['title'],year=r['year'],journal=journal,article_type=x.get('article-type'),subjects=[''.join(e.itertext()).strip() for e in x.findall('.//article-categories//subject')]))
 except Exception as e: errors.append([str(p),str(e)])
review=json.load(open(root/'experiments/corpus-analysis-2026-11-16/review/medical-uploads.json'))
docs=[]
labels={'NEJMp1616577':[['interpret','assert'],['assert','explain','qualify']],'NEJMp1702362':[['orient','assert','explain'],['assert','support','report']],'NEJMp1707514':[['narrate','report'],['narrate','interpret']],'NEJMp1711886':[['report','interpret'],['qualify','explain']],'NEJMp1901657':[['qualify','report'],['report']],'NEJMp1312793':[['orient','report'],['assert','support']]}
for d in review['documents']:
 if 'NEJMp' not in d['source_path']: continue
 p=Path(d['source_path']); original=d['title']=='Dead Man Walking'; spans=[]
 for i,s in enumerate(d['spans'],1):
  source=Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis/review-medical')/(p.name+f".page{s['pdf_page']:02}.txt")
  dest=cache/source.name; shutil.copyfile(source,dest)
  t=dest.read_text(); sample=t[s['start_char']:s['end_char_exclusive']]
  assert hashlib.sha256(sample.encode()).hexdigest()==s['sha256']
  spans.append(dict(id=f"{p.stem}-sample-{i}",page=s['pdf_page'],page_text_path=str(dest),page_text_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),start=s['start_char'],end_exclusive=s['end_char_exclusive'],offset_units='unicode_codepoints',span_sha256=s['sha256'],prior_interpretation=s['reason'],status='selected passage; paragraph boundaries not verified',quantitative_eligible=False,functions=labels[p.stem][i-1]))
 docs.append(dict(coding_status='excluded_original' if original else 'selectively_coded',full_body_paragraphs_retained=False,quantitative_eligibility={'full_body':False,'paragraphs':False,'reason':'Text layer contains columns, neighboring articles, or duplicated display material; complete paragraph boundaries not visually validated.'},title=d['title'],year=d['original_publication_year'],doi=d['doi'],pdf=str(p),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),publisher_category=d['article_type_source'],body_pages=d['main_body_pdf_pages'],prior_section_outline=d['section_outline_order'],holdout_status='excluded_original' if original else '2015-2019_candidate',selected_passages=spans))
coding_paths={'NEJMp1616577':'aca-science/NEJMp1616577-coding.json','NEJMp1702362':'aca-science/NEJMp1702362-coding.json','NEJMp1707514':'narratives/NEJMp1707514-coding.json','NEJMp1711886':'narratives/NEJMp1711886-coding.json','NEJMp1901657':'arb/article.json'}
for doc in docs:
 key=Path(doc['pdf']).stem
 if key in coding_paths:
  doc['coding_status']='fully_coded_single_analyst'
  doc['full_body_paragraphs_retained']=True
  doc['quantitative_eligibility']={'full_body':True,'paragraphs':True,'reason':'Reconstructed from visually inspected PDF pages; see article coding record for normalization and scope.'}
  doc['full_coding_record']=coding_paths[key]
output={'xml_records_checked':sum(r['source_format']=='xml' for r in rows),'missing_paths':missing,'parse_errors':errors,'nejm_metadata_matches':results,'publisher_perspective_matches':[r for r in results if any('perspective' in s.lower() for s in r['subjects'])], 'uploads':docs,'method':'Retained inventory only; journal-title or journal-id text match; Perspective publisher category requires explicit article-categories subject. Existing attachment review and excerpts are provisional. No network.'}
(out/'inventory.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
