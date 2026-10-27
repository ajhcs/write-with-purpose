// Research fixtures only. This is not an automatic correction or acceptance gate.
import { LocalLinter, Dialect } from 'harper.js';
import { binaryInlined as binary } from 'harper.js/binaryInlined';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';

const cases = [
  ['spelling', 'The measurment is repeatble.'],
  ['article', 'This is a example.'],
  ['repeated_word', 'The sensor records the the temperature.'],
  ['punctuation_spacing', 'The pump stopped , but the alarm remained active.'],
  ['agreement', 'The results is consistent.'],
  ['comma_splice', 'The pump stopped, the alarm remained active.'],
  ['run_on', 'The sensor failed the alarm stayed silent.'],
  ['attachment_ambiguity', 'I saw the operator with the camera.'],
  ['medical_vocabulary', 'The patient had hypoxaemia; auscultation revealed bilateral crackles.'],
  ['engineering_vocabulary', 'The microcontroller reads the thermocouple and logs the hysteresis.'],
  ['purposeful_repetition', 'The first valve is closed. The second valve is closed.'],
  ['good_punctuation', 'The report, which I sent yesterday, contains three figures; the appendix contains two.'],
  ['passive_without_actor', 'The sample was collected at 09:00.'],
  ['unicode_offsets', '🧪 The measurment is repeatble.'],
  ['markdown', '# Test results\n\n```text\nThe measurment is repeatble.\n```\n\nThe measurement is repeatable.'],
];

const order = (a,b) => a < b ? -1 : a > b ? 1 : 0;
const canonical = value => JSON.stringify(value, (_,v) => v && !Array.isArray(v) && typeof v === 'object' ? Object.fromEntries(Object.entries(v).sort(([a],[b])=>order(a,b))) : v);
const hash = value => createHash('sha256').update(value).digest('hex');
const packageURL = new URL('../package.json', import.meta.resolve('harper.js'));
const engine = JSON.parse(await readFile(packageURL,'utf8'));
if (engine.version !== '3.0.0') throw new Error('The experiment requires the pinned Harper 3.0.0 package.');
const customWords = process.argv.includes('--custom') ? ['hypoxaemia','thermocouple'] : [];
const linter = new LocalLinter({binary,dialect:Dialect.American});
try {
  await linter.setup();
  if (customWords.length) await linter.importWords(customWords);
  const config=await linter.getLintConfig();
  const results=[];
  for (const [id,text] of cases) {
    const lints=await linter.lint(text);
    const findings=lints.map(lint=>{
      const span=lint.span();
      const problem=lint.get_problem_text();
      // This published JS API returns UTF-16 indices. Verify actual source text
      // before converting to the Python editing tool's Unicode code-point spans.
      if (text.slice(span.start,span.end)!==problem) throw new Error(`Unverified source span in ${id}`);
      const start=[...text.slice(0,span.start)].length;
      const end=[...text.slice(0,span.end)].length;
      if ([...text].slice(start,end).join('')!==problem) throw new Error(`Code-point conversion failed in ${id}`);
      return {
        span:{start,end},engine_span_utf16:{start:span.start,end:span.end},
        text:problem,kind:lint.lint_kind(),message:lint.message(),
        suggestions:lint.suggestions().map(s=>({kind:s.kind(),replacement:s.get_replacement_text()}))
          .sort((a,b)=>order(canonical(a),canonical(b))),
      };
    }).sort((a,b)=>a.span.start-b.span.start || a.span.end-b.span.end || order(canonical(a),canonical(b)));
    results.push({id,text,findings});
  }
  const payload={engine:'harper.js',version:engine.version,dialect:'American',
    profile:'Pinned upstream defaults; includes optional style suggestions. Not an enforcement profile.',
    config_sha256:hash(canonical(config)),custom_words:customWords,
    offset_convention:'Normalized spans use Unicode code points; original engine spans use UTF-16. Both checked against the source substring.',
    suggestion_order:'Sorted for stable reporting, not a ranking of preferred corrections.',
    results};
  const output={...payload,normalized_payload_sha256:hash(canonical(payload)),
    limitations:'Small authored probe set, not a coverage benchmark. No automatic replacements. A clean result does not establish correct or useful prose.'};
  const outIndex=process.argv.indexOf('--out');
  if (outIndex>=0) {
    if (!process.argv[outIndex+1]) throw new Error('--out needs a filename.');
    await writeFile(process.argv[outIndex+1],JSON.stringify(output,null,2)+'\n',{flag:'wx'});
    console.log(JSON.stringify({cases:results.length,payload_sha256:output.normalized_payload_sha256}));
  } else console.log(JSON.stringify(output,null,2));
} finally { await linter.dispose(); }
