import {LocalLinter,Dialect} from '../language-check-probe/node_modules/harper.js/dist/index.js';
import {binaryInlined as binary} from '../language-check-probe/node_modules/harper.js/dist/binaryInlined.js';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const corpus=JSON.parse(await readFile(new URL('../../outputs/editor-language-comparison/engine-corpus.json',import.meta.url),'utf8'));
const engine=JSON.parse(await readFile(new URL('../language-check-probe/node_modules/harper.js/package.json',import.meta.url),'utf8'));
if(engine.version!=='3.0.0')throw new Error('Unexpected engine version');
const cmp=(a,b)=>a<b?-1:a>b?1:0;
const stable=v=>JSON.stringify(v,(_,x)=>x&&!Array.isArray(x)&&typeof x==='object'?Object.fromEntries(Object.entries(x).sort(([a],[b])=>cmp(a,b))):x);
const hash=v=>createHash('sha256').update(v).digest('hex');
const linter=new LocalLinter({binary,dialect:Dialect.American});
try {
  await linter.setup();
  const config=await linter.getLintConfig();
  const results=[];
  for(const c of corpus.cases){
    const groups=await linter.organizedLints(c.input,{language:'plaintext',dedup:true,isolateEnglish:false});
    const findings=[];
    for(const [rule,lints] of Object.entries(groups))for(const l of lints){
      const span=l.span(),text=l.get_problem_text();
      if(c.input.slice(span.start,span.end)!==text)throw new Error(`Unverified UTF-16 span ${c.id}`);
      const start=[...c.input.slice(0,span.start)].length,end=[...c.input.slice(0,span.end)].length;
      if([...c.input].slice(start,end).join('')!==text)throw new Error(`Invalid scalar span ${c.id}`);
      const raw=l.suggestions().map(s=>({kind:s.kind(),replacement:s.get_replacement_text()}));
      findings.push({rule,kind:l.lint_kind(),spelling:l.lint_kind()==='Spelling',message:l.message(),start,end,text,engine_span_utf16:{start:span.start,end:span.end},suggestions:raw.slice().sort((a,b)=>cmp(stable(a),stable(b))),engine_top_suggestion:raw[0]??null});
    }
    findings.sort((a,b)=>a.start-b.start||a.end-b.end||cmp(stable(a),stable(b)));
    results.push({id:c.id,input_sha256:c.sha256,findings});
  }
  const output={engine:'Harper',version:engine.version,profile:{dialect:'American',format:'plaintext',dedup:true,isolateEnglish:false,custom_words:[],default_config_sha256:hash(stable(config))},results};
  output.normalized_sha256=hash(stable(output));
  const filename=process.argv[2];if(!filename)throw new Error('Need output filename');
  await writeFile(new URL(filename,import.meta.url),JSON.stringify(output,null,2)+'\n',{flag:'wx'});
  console.log(JSON.stringify({engine:output.engine,cases:results.length,findings:results.reduce((n,c)=>n+c.findings.length,0),sha256:output.normalized_sha256}));
}finally{await linter.dispose();}
