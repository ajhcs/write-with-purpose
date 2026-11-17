#!/usr/bin/env python3
"""Source-specific OpenAlex metadata discovery; caches responses, no full-text acquisition."""
import csv,datetime,hashlib,json,re
from pathlib import Path
import requests
R=Path(__file__).resolve().parent;C=Path('/workspace/tmp/builderbob/writing-corpus/legal-openalex');C.mkdir(parents=True,exist_ok=True)
VENUES={'Harvard Law Review':'S117766065','The Yale Law Journal':'S161895660','Michigan Law Review':'S69429964','Stanford Law Review':'S161743634','Columbia Law Review':'S183770981','The University of Chicago Law Review':'S21339052'}
URL='https://api.openalex.org/works'
# Known book titles or conspicuous book/review author merges, not a full screen.
BOOK_CONFLICT_IDS=set('W2795737110 W2795846212 W2052201324 W4229639624 W3143088062 W2966755844 W2800400548 W4298209999 W1574390379 W2977708908 W2058869603 W2113893891 W2052471430 W1542305406 W2124525589 W2795628851 W1538097327 W2797897542 W3022730379 W2102696110 W2090052903 W2078449652 W2797227964 W1973962934 W2029355702 W2010458688 W2049893405 W1573382455 W2078299499 W2025083892 W1487279857 W1543971459 W4234789913 W1964676977 W2795637364 W1978042795 W4300116504 W2800301215 W2799856606 W4300912073 W4240732435 W2801912221 W4297215370 W1605421440'.split())
def main():
 rows=[];receipt=[];seenid=set();seentitle=set()
 for journal,sid in VENUES.items():
  params={'filter':f'primary_location.source.id:{sid},to_publication_date:2014-12-31,type:article','sort':'cited_by_count:desc','per_page':100}
  cache=C/(sid+'.json')
  if not cache.exists():
   res=requests.get(URL,params=params,timeout=45);res.raise_for_status();cache.write_bytes(res.content)
  data=cache.read_bytes();obj=json.loads(data);snapshot=datetime.datetime.fromtimestamp(cache.stat().st_mtime,datetime.timezone.utc).isoformat();req=requests.Request('GET',URL,params=params).prepare().url
  count=0;exclusions={'retracted_metadata':0,'missing_title':0,'duplicate_id':0,'duplicate_title_year':0,'date_outside':0}
  for rank,x in enumerate(obj.get('results',[]),1):
   title=x.get('display_name') or '';year=x.get('publication_year'); wid=x.get('id','')
   if x.get('is_retracted'):exclusions['retracted_metadata']+=1;continue
   if not title:exclusions['missing_title']+=1;continue
   if not year or year>2014:exclusions['date_outside']+=1;continue
   if wid in seenid:exclusions['duplicate_id']+=1;continue
   k=(re.sub(r'\W+',' ',title.lower()).strip(),year)
   if k in seentitle:exclusions['duplicate_title_year']+=1;continue
   seenid.add(wid);seentitle.add(k);count+=1
   loc=x.get('primary_location') or {};source=loc.get('source') or {};authors='; '.join((a.get('author') or {}).get('display_name','') for a in x.get('authorships',[]));doi=x.get('doi') or ''
   rows.append({'venue':journal,'venue_openalex_id':sid,'source_reported':source.get('display_name',''),'rank_in_source_query':rank,'title':title,'authors_openalex':authors,'publication_year':year,'publication_date':x.get('publication_date',''),'doi':doi,'landing_page_url':loc.get('landing_page_url',''),'openalex_work_id':wid,'openalex_cited_by_count':x.get('cited_by_count'),'citation_provider':'OpenAlex','citation_snapshot_utc':snapshot,'provider_type':x.get('type',''),'candidate_form':'law-review item; article/note/comment/book review uncertain','classification_basis':'OpenAlex type article and primary journal location; law-review editorial form not verified','retraction_screen':'OpenAlex is_retracted flag false at query; current status not independently verified','priority':'citation-ranked bibliographic lead; source and form verification required','fulltext_status':'not retrieved or measured','known_or_suspected_conflict':wid.rsplit('/',1)[-1] in BOOK_CONFLICT_IDS,'hold_reason':'Known book title or probable book/review metadata merger; verify journal item and attribution.' if wid.rsplit('/',1)[-1] in BOOK_CONFLICT_IDS else '', 'request_status':'held' if wid.rsplit('/',1)[-1] in BOOK_CONFLICT_IDS else 'unscreened candidate', 'query_url':req})
   if count>=65:break
  receipt.append({'venue':journal,'openalex_source_id':sid,'query_url':req,'filter':params['filter'],'sort':params['sort'],'provider_hit_count':obj.get('meta',{}).get('count'),'returned_page':len(obj.get('results',[])),'selected':count,'exclusions_before_limit':exclusions,'snapshot_utc':snapshot,'response_sha256':hashlib.sha256(data).hexdigest()})
  print(journal,count,'hits',obj.get('meta',{}).get('count'),flush=True)
 with (R/'records.jsonl').open('w') as f:
  for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
 with (R/'records.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 with (R/'library-candidates.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(r for r in rows if not r['known_or_suspected_conflict'])
 (R/'query-receipts.json').write_text(json.dumps({'provider':'OpenAlex','retrieved_records':len(rows),'queries':receipt},indent=2)+'\n')
 print('TOTAL',len(rows))
if __name__=='__main__':main()
