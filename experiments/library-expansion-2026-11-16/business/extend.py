import json,urllib.parse,urllib.request,time,difflib,datetime
from pathlib import Path
p=Path(__file__).parent
items=[
('How I Did It: A Maverick CEO Explains How He Persuaded His Team to Leap into the Future','personal_reflective_essay','https://hbr.org/2010/06/how-i-did-it-a-maverick-ceo-explains-how-he-persuaded-his-team-to-leap-into-the-future','CEO narrates a company turning point in first person.'),
('How I Did It: The CEO of Aramex on Turning a Failed Sale into a Huge Opportunity','personal_reflective_essay','https://hbr.org/2011/03/how-i-did-it-the-ceo-of-aramex-on-turning-a-failed-sale-into-a-huge-opportunity','Founder narrates lessons from an attempted sale in first person.'),
('How I Did It: Giving Up the CEO Seat','personal_reflective_essay','https://hbr.org/2010/03/how-i-did-it-giving-up-the-ceo-seat','Founder reflects on recognizing the need to step down.'),
('What Is Strategy?','argument_perspective','https://hbr.org/1996/11/what-is-strategy','Porter argues that operational effectiveness alone does not constitute strategy.'),
('The Rise and Fall of Strategic Planning','argument_perspective','https://hbr.org/1994/01/the-fall-and-rise-of-strategic-planning','Argues for distinguishing planning from strategic thinking.'),
('How Will You Measure Your Life?','personal_reflective_essay','https://hbr.org/2010/07/how-will-you-measure-your-life','Personal reflection applies management ideas to life choices; HBR labels this article a bestseller.'),
('The Five Competitive Forces That Shape Strategy','conceptual_explainer','https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy','Explains a five-forces framework for analyzing industries; HBR labels it a bestseller.'),
('What Is Disruptive Innovation?','conceptual_explainer','https://hbr.org/2015/12/what-is-disruptive-innovation','Authors explain the theory, common misapplications, and its evolution.'),
('How to Write a Great Business Plan','procedure_how_to','https://store.hbr.org/product/how-to-write-a-great-business-plan/97409','Sets out questions and four factors to address when composing a business plan.'),
('Managing Your Boss','procedure_how_to','https://hbr.org/2005/01/managing-your-boss','Provides practical advice to assess and manage a working relationship; first published in 1980.'),
('Leading Change: Why Transformation Efforts Fail','procedure_how_to','https://hbr.org/1995/03/leading-change-why-transformation-efforts-fail-2','Describes eight sequential actions in a transformation; HBR labels it a bestseller.'),
('Discovering Your Authentic Leadership','procedure_how_to','https://hbr.org/2007/02/discovering-your-authentic-leadership','Offers practices for personal leadership development; HBR labels it a bestseller.'),
]
raw=[]
for title,form,url,basis in items:
 q='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':title,'per-page':10})
 try:
  req=urllib.request.Request(q,headers={'User-Agent':'CorpusResearch/1.0 metadata'})
  with urllib.request.urlopen(req,timeout=20) as f: result=json.load(f)
  def score(x):return difflib.SequenceMatcher(None,title.lower(),(x.get('title') or '').lower()).ratio()
  x=max(result['results'],key=score); sc=score(x)
  print(title,'=>',x['title'],x['publication_year'],round(sc,2),x.get('doi'))
  raw.append({'title_query':title,'query_url':q,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'score':sc,'form':form,'publisher_url':url,'basis':basis,'response':x})
 except Exception as e: print('ERROR',title,str(e))
 time.sleep(.3)
(p/'openalex-hbr-raw.json').write_text(json.dumps(raw,indent=2))
