import json,datetime
from pathlib import Path
base=Path('/workspace/repos/builderbob/.writing-corpus-cache/rule-calibration/packets/A')
m=json.loads((base/'manifest.json').read_text()); U={x['unit_id']:x for x in m['units']}; T=m['targets']; sources={x['id']:x for x in m['sources']}
# Each tuple contains a function, source anchor, role-specific fields, and optionally a grounded relation target.
D={
'LF-d23d38c43ea7-p005':[
('assert','a great deal of harm',('belief in work causes harm; reducing work brings prosperity','author','central position')),
('orient','All this is only preliminary',('main thesis about work','marks preceding savings argument as preliminary'),('LF-d23d38c43ea7-p005','I want to say','the essay’s work thesis'))],
'LF-d23d38c43ea7-p015':[
('assert','If the ordinary wage-earner worked four hours',('four-hour workday could provide enough and end unemployment','author','proposes an alternative arrangement')),
('qualify','assuming a certain very moderate amount of sensible organization',('four-hour workday would provide enough and eliminate unemployment','depends on sensible organization','condition'),('LF-d23d38c43ea7-p015','If the ordinary wage-earner worked four hours','predicted effects of a four-hour day')),
('explain','because they are convinced that the poor',('well-to-do reaction and beliefs about poor people’s leisure','belief accounts for their shock')),
('compare','while they wish their sons to work so hard',('sons versus wives and daughters','expected work','sons work hard while wives and daughters need not')),
('interpret','The snobbish admiration of uselessness',('different expectations for sexes','plutocracy confines admiration of uselessness to women','generalizes and evaluates the described contrast'))],
'LF-d23d38c43ea7-p025':[
('assert','four hours’ work a day should entitle',('four hours of work should secure basic comforts and free remaining time','author','clarifies proposal')),
('assert','It is an essential part of any such social system',('education should develop tastes for intelligent leisure','author','adds a social policy proposal')),
('explain','This results from the fact that their active energies',('work and passive urban pleasures','work consumes the energy for active pleasures')),
('qualify','I am not meaning to imply',('suggestion to reduce work to four hours','remaining time need not all be frivolous','clarification of scope'),('LF-d23d38c43ea7-p025','working hours should be reduced to four','four-hour proposal'))],
'LF-80bd6f30b443-p006':[
('interpret','My education taught me to believe',('author’s education and learned responses','education conveyed that non-elite people were beneath him','reflects on social conditioning')),
('report','I learned to give that little nod',('author’s reaction to less prestigious colleges','author’s personal account','past habitual conduct')),
('illustrate','I learned to give that little nod',('learned disregard for those outside elite education','describes a concrete learned reaction','personal recollection'),('LF-80bd6f30b443-p006','people who didn’t go to an Ivy League or equivalent school weren’t worth talking to','learned judgment about non-elite people'))],
'LF-80bd6f30b443-p018':[
('assert','An elite education gives you the chance to be rich',('elite education closes off the opportunity not to be rich','author','advances critique of security')),
('compare','you have to drive a Honda instead of a BMW',('ordinary and wealthy lifestyles','material consumption versus meaningful work','ordinary goods are traded for work one loves')),
('illustrate','You can live comfortably in the United States as a schoolteacher',('non-rich people can live comfortably','lists concrete occupations','general illustrative cases'),('LF-80bd6f30b443-p018','provide a decent living to whole classes of people','decent living outside wealth'))],
'LF-80bd6f30b443-p029':[
('define','Being an intellectual begins with thinking your way outside',('being an intellectual','thinking beyond one’s assumptions and enforcing system','starting characteristic')),
('explain','But students who get into elite schools',('elite admission and inability to see beyond the system','successful adaptation to the system makes seeing outside difficult')),
('compare','the situation may be better at second-tier schools',('second-tier schools and prestigious universities','potential for intellectual independence','second-tier situation may be better')),
('qualify','Some students end up at second-tier schools because',('possible advantage of second-tier schools','distinguishes similarly conformist students from independent ones','exception'),('LF-80bd6f30b443-p029','the situation may be better at second-tier schools','potential second-tier advantage'))],
'LF-fca9142fd337-p006':[
('narrate','An interview followed',('narrator and Utton','interview, discussion of interests and pay','encounter develops into job discussion')),
('report','he paid a per-body bonus of four shillings',('bonus and possibility of earnings','Utton as recalled by narrator','reported offer'))],
'LF-fca9142fd337-p018':[
('narrate','I removed the old gent’s pinstriped trousers',('narrator and deceased man','stripping and dissection','progresses to exposing femur')),
('report','the longest bone in the human body. The femur.',('exposed femur and its appearance','narrator’s account','described observation'))],
'LF-fca9142fd337-p029':[
('narrate','He waited for a second',('Utton and narrator','pause and revelation of cremation','tension changes as information is disclosed'))],
'LF-2cb0e10879f3-p003':[
('orient','This, however, is not a story of my cooking',('story of mother and her cooking','turns from the narrator’s own cooking to its inspiration'),('LF-2cb0e10879f3-p003','It is the story of my mother','forthcoming story about the mother'))],
'LF-2cb0e10879f3-p007':[
('narrate','he kept their marriage intact by absolving her',('narrator and parents','father takes mother out while narrator cooks','recounts family arrangement and experience')),
('interpret','the more necessary connection was between food and honesty',('author cooking for himself and family food stories','food was bound to honesty as well as love','personal reflection on family experience')),
('illustrate','the Mott\'s applesauce she\'d doctored',('mother’s lies concerned food','specific prepared food described as homemade','personal recollection'),('LF-2cb0e10879f3-p007','most of her lies were about food','mother’s food-related fibs'))],
'LF-2cb0e10879f3-p011':[
('narrate','On Sunday nights after they moved near us',('narrator and mother','family suppers and mother’s questions','repeated encounters lead to realization')),
('interpret','Now I understood that she hated cooking',('mother’s cooking, questions and prior assumptions','her dislike arose from lack of knowledge and uncertainty','revises earlier explanation')),
('interpret','They were in over their heads',('mother’s food experience and father’s infidelities','parents were unhappy and deserved forgiveness','reflects on family experience')),
('explain','because she didn\'t know how to do it',('mother’s cooking knowledge and aversion','lack of know-how made meal outcomes uncertain'))],
'PMC2867979-p011':[
('report','An association has been shown between industry sponsorship',('association between sponsorship or affiliation and positive results','cited studies and reviews','published research summary')),
('illustrate','in a systematic review of the scope and impact',('association between sponsorship and positive conclusions','eight analyses give a concrete review example','attributed review'),('PMC2867979-p011','An association has been shown between industry sponsorship','industry sponsorship and positive research conclusions')),
('compare','the latter were less transparent',('Cochrane reviews and industry-supported meta-analyses','transparency, critical attention and favorable conclusions','industry-supported reviews rated less transparent and more favorable')),
('qualify','Other aspects of industry involvement',('paper’s treatment of industry involvement','design bias excluded from scope','scope restriction'),('PMC2867979-p011','industry involvement','paper’s discussion of industry involvement'))],
'PMC2867979-p033':[
('report','In 2000, a trial comparing upper gastrointestinal toxicity',('VIGOR trial findings and subsequent cardiovascular concerns','cited trial and analysis','attributed published findings')),
('narrate','Concerns about the risk of selective COX-2-inhibitor-related cardiovascular events',('researchers and rofecoxib evidence','2000 trial, 2001 concerns, 2002 analysis','evidence and concern develop across time'))],
'PMC2867979-p055':[
('qualify','Another potential limitation of the review',('review’s cases of reporting bias','source validity may limit review','limitation'),('PMC2867979-p055','the validity of the sources describing cases of reporting bias','validity of review’s source cases')),
('explain','as they provide a broader overview',('non-journal sources and review value','broader coverage and leads for systematic research justify their use')),
('report','several cases were based on information from other sources',('some cases relied on newspapers and websites','review authors','description of source base'))],
'PMC4053896-p007':[
('report','we conducted a four step approach',('review search dates, sampling and selection','study authors','completed methods')),
('explain','Based on these articles, we defined the research focus',('key reviews and subsequent search criteria','key papers informed focus and inclusion/exclusion criteria'))],
'PMC4053896-p021':[
('report','Although most of the studies had student participants',('participant groups and environments in reviewed studies','review authors','summary of reviewed studies')),
('compare','The majority of the studies compared urban with Nature environments',('urban versus nature comparison designs and other designs','frequency among studies','urban versus nature comparisons more common'))],
'PMC4053896-p035':[
('report','The most evident finding was the short-term stress-reducing potential',('review’s principal finding','review authors','reported synthesis finding')),
('interpret','the major achievement of our present review could be seen',('review findings and decision support','review could increase societal impact of knowledge','infers significance of the review')),
('assert','the data of the current scientific literature suggests to use',('use nature for primary, secondary and tertiary stress prevention','review authors','recommendation based on literature')),
('qualify','could be seen in enhancing',('review’s societal impact','achievement presented as a possibility','uncertainty'),('PMC4053896-p035','the major achievement of our present review','proposed societal impact'))],
'git-p02':[
('report','With `--contains`, shows only the branches',('branch filters and default commit','documentation','described command behavior')),
('define','the branches whose tip commits are descendants of the named commit',('branches containing the named commit','branches whose tips descend from that commit','meaning of contains filter')),
('define','the branches whose tip commits are reachable from the named commit',('branches merged into the named commit','branches whose tips are reachable from that commit','meaning of merged filter'))],
'git-p05':[
('report','Git sets up the branch',('tracking configuration and override options','documentation','default and configurable behavior')),
('explain','so that \'git pull\' will appropriately merge',('tracking configuration and git pull','configuration enables merging from the remote-tracking branch'))],
'git-p07':[
('report','With a `-d` or `-D` option',('branch deletion, multiple branches and reflog deletion','documentation','command behavior')),
('instruct','You may specify more than one branch for deletion',('command user','specify multiple branches for deletion','manual describes available invocation'))],
'python-p02':[
('define','Such a file is called a *module*',('module','file containing definitions that may be reused','introductory Python terminology')),
('explain','definitions from a module can be *imported*',('module definitions and other modules or main module','import allows definitions to be used elsewhere'))],
'python-p04':[
('instruct','Now enter the Python interpreter and import this module',('tutorial reader','enter interpreter and import the module','walkthrough directs action using following command'))],
'python-p06':[
('instruct','you can assign it to a local name',('tutorial reader','assign frequently used function to a local name','conditional tutorial suggestion with following example'))]
}
keys={'orient':['prepared_contribution','preparation_link'],'define':['term','meaning_or_distinction','definition_scope'],'report':['reported_content','attribution','event_or_claim_status'],'assert':['position','position_holder','commitment_job'],'support':['supported_claim','intended_link','basis_kind'],'explain':['relata','connection_made_intelligible'],'illustrate':['illustrated_idea','concretizing_link','case_status'],'compare':['alternatives','shared_dimension','stated_relationship'],'interpret':['input_material','inference_or_significance','transformation'],'qualify':['affected_claim','scope_change','qualification_kind'],'instruct':['addressed_actor','action','directive_context'],'narrate':['participant_or_subject','events','change_through_time']}
rel={'orient','support','illustrate','qualify'}
# Exact anchor snippets extended to the end of the sentence when possible.
def anchor(uid,needle):
 text=U[uid]['text']; i=text.find(needle)
 if i<0: raise ValueError((uid,needle))
 end=text.find('.',i+len(needle)); end=min(end+1,len(text)) if end>=0 and end-i<350 else i+len(needle)
 return {'unit_id':uid,'quote':text[i:end], 'occurrence':0}
annotations=[]
for t in T:
 pid=t['paragraph_id']; src=sources[t['source_id']]; roles=[]; reviewed=[pid]
 for j,row in enumerate(D[pid]):
  fid,quote,vals,*tr=row
  aa=anchor(pid,quote); reason={'assert':'Presents a distinct position.','report':'Presents an attributed account or description.','define':'Makes a term or category distinguishable.','explain':'Connects the stated elements.','compare':'Relates alternatives along a dimension.','interpret':'Draws meaning from the stated material.','instruct':'Directs an action for the reader.','narrate':'Develops an experience or events through time.','orient':'Prepares the subsequent contribution.','illustrate':'Makes a specific idea concrete.','qualify':'Changes the scope or certainty of an identifiable claim.'}[fid]
  targets=[]
  if tr:
   tu,tq,par=tr[0]
   if tu not in reviewed: reviewed.append(tu)
   targets=[{'target_id':f'{pid}-r{j}-t1','kind':'explicit_span','anchors':[anchor(tu,tq)],'paraphrase':par,'status':'clear','reason':'The quoted source identifies the affected contribution.'}]
  assessment={'basis_kind':('attributed_report' if fid=='report' else 'reasoning'),'role_adequacy':'not_assessed','empirical_evidence_status':'not_claimed','truth_status':'not_assessed','assessment_reason':'Function coding only; source claims were not independently verified.'}
  roles.append({'annotation_id':f'{pid}-r{j}','function_id':fid,'layer':'relation' if fid in rel else ('temporal_presentation' if fid=='narrate' else 'local_move'),'decision':'present','status':'clear','anchors':[aa],'reason':reason+' '+str(vals[0])+'.','role_fields':dict(zip(keys[fid],vals)),'targets':targets,'alternatives':[],'evidence_assessment':assessment})
 form=src.get('provisional_form') or src.get('stratum') or 'unknown'
 context={'family':{'value':None,'hypothesis_status':'unknown','reason':'Family not supplied.'},'form':{'value':form,'hypothesis_status':'provisional','reason':'Packet metadata.'},'section':{'value':None,'reason':'No section identity assigned for this excerpt.'},'audience':None,'reader_task':'Follow the local contribution in the supplied document context.','neutral_contribution':str(D[pid][0][2][0]),'reviewed_units':reviewed,'context_sufficiency':'sufficient','context_reason':'Selected text and relevant supplied local context establish these judgments.','extraction_issues':[]}
 annotations.append({'paragraph_id':pid,'context':context,'roles':roles})
out={'coder_id':'A-revised-2','arm':'revised','stage':'A','model':'gpt-6.1-terra','started_at_utc':'2026-11-16T16:24:34Z','finished_at_utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'annotations':annotations}
Path(__file__).with_name('raw.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
