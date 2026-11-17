from extract import *
for f in ['cole-cs50','cole-engineering','doctorow','python']:
 p=P((base/(f+'.html')).read_text());
 if f.startswith('cole'): root=next(n for n in walk(p.root) if 'essay-prose' in n.a.get('class',''))
 elif f=='doctorow':root=next(n for n in walk(p.root) if n.a.get('class')=='entry-content')
 else:root=next(n for n in walk(p.root) if n.a.get('class')=='body')
 print('\n',f)
 for c in root.c:
  if isinstance(c,N):print(c.t,c.a.get('class',''),c.a.get('id',''),repr(' '.join(plain(c).split())[:100]))
