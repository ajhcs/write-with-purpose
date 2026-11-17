import requests,json,time,pathlib
p=pathlib.Path(__file__).parent
queries={
'personal_reflective_essay':'(JOURNAL:"JAMA" OR JOURNAL:"New England Journal of Medicine") AND (TITLE:"patient" OR TITLE:"physician") AND ("personal narrative" OR "a piece of my mind" OR "my story")',
'argument_perspective':'(JOURNAL:"New England Journal of Medicine" OR JOURNAL:"Lancet") AND (PUB_TYPE:"Comment" OR PUB_TYPE:"Editorial") AND (TITLE:"medicine" OR TITLE:"health care")',
'critical_review_of_work':'(PUB_TYPE:"Book Review" OR TITLE:"book review") AND (medicine OR patient)',
'conceptual_explainer':'TITLE:"explained" AND (clinical OR medicine OR medical)',
'tutorial':'TITLE:"tutorial" AND (clinical OR medicine OR medical)',
'procedure_how_to':'TITLE:"how to" AND (clinical OR medicine OR medical)',
'reference_entry':'TITLE:"clinical review" AND (diagnosis OR treatment)',
'empirical_report':'TITLE:"randomized" AND PUB_TYPE:"Randomized Controlled Trial"',
'methods_paper':'TITLE:"method" AND (clinical OR patient) AND PUB_TYPE:"Journal Article"',
'theory_conceptual_paper':'TITLE:"theoretical framework" AND (health OR patient)',
'case_report':'(JOURNAL:"Journal of Medical Case Reports" OR JOURNAL:"BMJ Case Reports") AND TITLE:"case report"',
'study_protocol':'TITLE:"study protocol" AND (trial OR randomized)',
'narrative_critical_literature_review':'TITLE:"narrative review" AND (clinical OR patient)',
'scoping_review':'TITLE:"scoping review" AND (health OR patient)',
'systematic_review':'TITLE:"systematic review" AND (health OR disease)',
'proposal':'TITLE:"proposal" AND (clinical OR health OR patient)',
'decision_memo':'TITLE:"recommendation" AND (clinical OR screening)'
}
base='https://www.ebi.ac.uk/europepmc/webservices/rest/search'
all={}
for form,q in queries.items():
 params={'query':q+' AND FIRST_PDATE:[1900-01-01 TO 2014-12-31] AND LANG:eng NOT PUB_TYPE:"Retracted Publication" SORT_CITED:y','format':'json','pageSize':15,'resultType':'core'}
 try:
  r=requests.get(base,params=params,timeout=45);r.raise_for_status();j=r.json(); all[form]={'url':r.url,'hitCount':j['hitCount'],'results':j['resultList'].get('result',[])}
  print('\n'+form+' '+str(j['hitCount']),flush=True)
  for x in all[form]['results'][:10]: print(x.get('pmid'),x.get('citedByCount'),x.get('pubYear'),x.get('title','')[:140],flush=True)
 except Exception as e: print('ERR',form,str(e),flush=True)
 time.sleep(.3)
(p/'search-receipts.json').write_text(json.dumps(all,indent=2))
