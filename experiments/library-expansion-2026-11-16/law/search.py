import requests,time
q=['The Positive Foundations of Formalism False Necessity and American Legal Realism','The Laws of Capitalism','The Life of the Law Goldberg','Feminist Legal Methods','The Effects of Problem-Oriented Policing on Crime and Disorder','Legitimacy in Policing A Systematic Review','The Effects of Hot Spots Policing on Crime','The Effect of Police on Crime New Evidence from US Cities','Do Judges Vary in Their Treatment of Race','A Regression-Discontinuity Analysis of the Criminal Deterrence Effect of Incarceration','The Use and Abuse of Empirical Evidence in the Death Penalty Debate','A Theory of Justice Rawls','Mapping the Margins Intersectionality Identity Politics and Violence against Women of Color','The Costs of Accidents A Legal and Economic Analysis','Racial Disparities in Sentencing A Meta Analysis','Scoping review criminal justice policing','protocol systematic review policing crime']
for s in q:
 try:
  j=requests.get('https://api.openalex.org/works',params={'search':s,'per-page':2},timeout=20).json()
  print('\n',s)
  for x in j.get('results',[]): print(x['title'],x['id'],x['publication_year'],x['cited_by_count'],x.get('doi'))
 except Exception as e:print(type(e).__name__)
