"""Inspect saved public HTML bodies; do not label landing pages as full text."""
import csv
import importlib.util
import json
from pathlib import Path
import re
import sys
import retrieve as rt

sys.path.insert(0,str(rt.REPO/'experiments/corpus-analysis-2026-11-16/analysis'))
spec=importlib.util.spec_from_file_location('retained_html_parser',rt.REPO/'experiments/corpus-analysis-2026-11-16/analysis/analyze_html.py')
hm=importlib.util.module_from_spec(spec);spec.loader.exec_module(hm)
OriginalTree=hm.memo.Tree
class CleanTree(OriginalTree):
    def handle_starttag(self,tag,attrs):
        return super().handle_starttag(tag,[(k,v or '')for k,v in attrs])
hm.memo.Tree=CleanTree


def main():
    rows=list(csv.DictReader((rt.REPO/'experiments/library-expansion-2026-11-16/library-pull-list.csv').open()));lookup={r['candidate_key']:r for r in rows}
    result=[]
    for p in (rt.CACHE/'records').rglob('result.json'):
        rec=json.loads(p.read_text());row=lookup[rec['candidate_key']]
        for source in rec.get('landing_files',[]):
            path=Path(source['path']);raw=path.read_bytes();text=raw.decode('utf8','replace')
            try:
                blocks,objects,audit=hm.extract_generic(raw,row['title'])
            except Exception as error:
                blocks=[];audit={'error':str(error)}
            prose=[b['text']for b in blocks if b['kind']=='paragraph']
            words=sum(len(hm.word_tokens(t))for t in prose)
            headings=[b['text']for b in blocks if b['kind']=='heading']
            paywall=bool(re.search(r'"isAccessibleForFree"\s*:\s*false|purchase.{0,30}access|sign in to read|subscribe to continue|subscriber.only',text,re.I))
            tree=hm.memo.Tree();tree.feed(text)
            meta={n.a.get('name',n.a.get('property','')).lower():n.a.get('content','')for n in hm.memo.walk(tree.root)if n.tag=='meta'}
            observed_doi=meta.get('citation_doi',meta.get('dc.identifier',''))
            observed_titles=[meta.get('citation_title',''),meta.get('og:title','')]
            author=json.loads(row['authors'])[0]if row['authors']else''
            parts=author.replace('.','').split()
            surname=parts[0]if len(parts)>1 and parts[-1].isupper()and len(parts[-1])<=4 else parts[-1]if parts else''
            author_in_page=surname.casefold()in hm.norm(hm.plain(tree.root)).casefold() if surname else False
            doi_match=bool(row['doi'] and row['doi'].casefold()in observed_doi.casefold())
            # These are review candidates, not automatic completeness certification.
            possible=(words>=700 and not paywall)or('history.state.gov/historicaldocuments/'in source['url']and words>=70 and not paywall)
            result.append({'candidate_key':rec['candidate_key'],'title':row['title'],'path':str(path),'source_url':source['url'],'sha256':rt.digest(raw),'prose_words':words,'paragraphs':len(prose),'headings':headings,'body_preview':prose[:2],'body_end':prose[-2:],'paywall_marker':paywall,'possible_fulltext_for_review':possible,'observed_doi':observed_doi,'doi_match':doi_match,'observed_titles':observed_titles,'author_in_page':author_in_page,'parser_audit':audit})
    # Source snippets remain private; publish only the reviewed manifest later.
    rt.write_json(rt.CACHE/'html-inspections.json',result)
    public=[{k:v for k,v in r.items()if k not in ('body_preview','body_end','headings')}for r in result]
    rt.write_json(rt.ROOT/'html-inspections.json',public)
    print(json.dumps({'inspected':len(result),'possible_fulltext':sum(r['possible_fulltext_for_review']for r in result)}))


if __name__=='__main__':main()
