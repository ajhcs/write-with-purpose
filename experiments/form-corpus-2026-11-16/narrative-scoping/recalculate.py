#!/usr/bin/env python3
"""Recompute both samples from cached XML after documented parser/screen corrections."""
import datetime,hashlib,json,statistics
import acquire as a
p=a.ROOT
for cohort in ('','historical-'):
 receipt_path=p/(cohort+'receipt.json');receipt=json.loads(receipt_path.read_text())
 for form in ('narrative','scoping'):
  f=p/(cohort+form+'-candidates.json'); rows=json.loads(f.read_text()); measurements=[]
  for row in rows:
   row['measured']=False;row['year_basis']='Europe PMC pubYear';row['citation_snapshot_utc']=receipt['queries'][form]['search_utc']
   path=a.CACHE/(row.get('pmcid','')+'.xml')
   if not row.get('pmcid') or not path.exists(): continue
   m,status=a.analyze(row)
   if not m: row['xml_status']=status; continue
   row['publisher_article_type']=m['publisher_article_type'];row['publisher_subject_labels']=m['publisher_subject_labels']
   row['xml_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();row['xml_cached_mtime_utc']=datetime.datetime.fromtimestamp(path.stat().st_mtime,datetime.timezone.utc).isoformat()
   row['citation_snapshot_utc']=receipt['queries'][form]['search_utc'];row['year_basis']='Europe PMC pubYear'
   incompatible=(form=='narrative' and m['publisher_article_type']=='systematic-review') or (m['publisher_article_type'] in ('editorial','letter','commentary','book-review') and not any('review' in s.lower() for s in m['publisher_subject_labels']))
   row['classification_basis']='explicit form phrase in title; automated exclusion of named other forms and methods papers; semantic fit provisional'
   if incompatible: row['classification_basis']+='; publisher type excluded';row['xml_status']='excluded_incompatible_publisher_type'
   elif len(measurements)<200: row['measured']=True;row['xml_status']='cached';measurements.append({'pmcid':row['pmcid'],**m})
   else: row['xml_status']='available_beyond_selected_limit'
  f.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
  (p/(cohort+form+'-metrics.json')).write_text(json.dumps(measurements,ensure_ascii=False)+'\n')
  stats={k:a.quant([m[k] for m in measurements]) for k in ('body_words','paragraphs','top_level_sections','max_section_depth','abstract_words','reference_entries','figures','tables','lists','code','bibliographic_xrefs')}
  stats.update({k+'_document_medians':a.quant([statistics.median(m[k]) for m in measurements if m[k]]) for k in ('paragraph_words','sentence_words','word_characters')})
  (p/(cohort+form+'-aggregate.json')).write_text(json.dumps(stats,indent=2)+'\n')
  receipt['queries'][form]['measured']=len(measurements)
 receipt['recomputed_utc']=a.now();receipt['recompute_note']='Corrected reference lists outside back matter; excluded systematic narrative publisher types; removed exact administrative section titles; added XML hashes and citation snapshot date. Cached XML only.'
 receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
