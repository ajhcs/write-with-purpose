"""Validate source provenance and integration consistency, not paper correctness."""
import ast
from collections import Counter
from datetime import datetime,timezone
import hashlib,json,re
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as stream:
  while block:=stream.read(1024*1024):h.update(block)
 return h.hexdigest()

def main():
 manifest=json.loads((BASE/'source-manifest.json').read_text())
 assert len(manifest['records'])==18
 pdfs=0;texts=0
 for source in manifest['records']:
  assert sha(source['attachment_path'])==sha(source['pdf_path'])==source['sha256'],source['id']
  assert sha(source['text_path'])==source['text_sha256'],source['id']
  pdfs+=1;texts+=1
  if source['id']=='P02':
   assert source['extraction_status']=='partial_corrupt_attachment'
   alt=source['alternate_copy'];assert sha(alt['pdf_path'])==alt['sha256']
   assert sha(source['review_text_path'])==source['review_text_sha256']
 evidence=json.loads((BASE/'evidence-map.json').read_text());papers=evidence['papers']
 assert len(papers)==18 and {p['id'] for p in papers}=={f'P{i:02d}' for i in range(1,19)}
 assert len({p['doi'].lower().removeprefix('https://doi.org/') for p in papers})==18
 assert evidence['missing_finding_page_locators']==[]
 assert evidence['reporting_caution_record']
 for receipt in evidence['source_review_receipts']:assert sha(BASE/receipt['path'])==receipt['sha256']
 pages={p['id']:p.get('review_pages',p['pages']) for p in manifest['records']}
 findings=0
 for paper in papers:
  assert Path(paper['source_text_path']).exists()
  for finding in paper['findings']:
   findings+=1;assert finding['pdf_pages']
   for page in finding['pdf_pages']:
    if isinstance(page,int):assert 1<=page<=pages[paper['id']]
    else:assert paper['id']=='P14' and str(page).startswith('S1:') and 1<=int(str(page).split(':')[1])<=5
 candidates=json.loads((BASE/'reviewer-candidate-register.json').read_text())['candidates']
 assert len(candidates)==len({p['id'] for p in candidates})==32
 ledger=json.loads((BASE/'rule-decision-ledger.json').read_text())['candidates']
 assert len(ledger)==len({p['id'] for p in ledger})==12
 for row in ledger:
  assert row['status'].startswith('candidate') and row['trigger_and_scope'] and row['counterexample']
  for claim in row['paper_evidence']:
   assert claim['id'] in pages and all(1<=page<=pages[claim['id']] for page in claim['pdf_pages'])
 for item in json.loads((BASE/'comparison-baseline-hashes.json').read_text())['files']:
  assert sha(REPO/item['path'])==item['sha256'],item['path']
 supplements=json.loads((BASE/'supplement-attempts.json').read_text())['records']
 for item in supplements:
  if item.get('path'):assert sha(item['path'])==item['sha256'],item['id']
 broken=[];json_count=0
 for path in BASE.rglob('*.json'):json.loads(path.read_text());json_count+=1
 for path in (BASE/'scripts').glob('*.py'):ast.parse(path.read_text(),filename=str(path))
 for path in BASE.rglob('*.md'):
  for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
   if target.startswith(('http:','https:','mailto:','#')):continue
   target=target.split('#')[0].strip('<>')
   if target and not (path.parent/target).exists() and (path.parent/target).resolve()!=(BASE/'validation.json').resolve():broken.append({'file':str(path),'target':target})
 assert not broken,broken
 assert not any(BASE.rglob('*.pdf')) and not any(BASE.rglob('*.csv')) and not any(BASE.rglob('*.docx'))
 result={'verified_utc':datetime.now(timezone.utc).isoformat(),'supplied_pdf_hashes_verified':pdfs,
         'supplied_extraction_hashes_verified':texts,'recovered_author_copy_verified':True,
         'unique_primary_works':18,'physical_pages_in_supplied_batch':sum(p['pages'] for p in manifest['records']),
         'primary_review_hashes_verified':len(evidence['source_review_receipts']),
         'finding_page_locators_checked':findings,'reviewer_candidates':len(candidates),'integrated_candidates':len(ledger),
         'supplement_hashes_verified':len(supplements),'canonical_comparison_files_unchanged_since_snapshot':True,
         'json_files_parsed':json_count,'local_link_errors':broken,
         'scope':'Byte provenance, source-page references, unique coverage, unchanged comparison inputs and artifact structure. No semantic correctness, statistical replication, writing improvement or market advantage is certified.'}
 (BASE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
if __name__=='__main__':main()
