#!/usr/bin/env python3
import json
from pathlib import Path
from retrieve import D,ROOT,process
rows=[json.loads(s) for s in (ROOT/'domain-expansion/personal/records.jsonl').read_text().splitlines()]
r=next(x.copy() for x in rows if x['title']=='My Mother and Mercy')
old=r['author'];r['author']='Jaquira Díaz';r['target_url']='https://www.thesunmagazine.org/articles/24264-my-mother-and-mercy'
x=process(r);x['source_author_misprint']=old;x['corrected_author']='Jaquira Díaz';x['correction_source']='https://www.hmhco.com/~/media/sites/home/at-home/featured-shops/by-brand/best-american/2016-docs/2016-notables/ba_essays-notables.pdf?la=en';x['correction_evidence']='Publisher correction states 2014 notable list misspelled this author for this essay.'
(D/'followup-diaz.jsonl').write_text(json.dumps(x,ensure_ascii=False)+'\n')
print(x['status'],x.get('final_url'),flush=True)
