"""CLI tests for immutable source snapshots, exact patches and change metrics."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'skills/edit-with-purpose/scripts/edit_locally.py'


class LocalEditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='local-edit-')
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def write(self, name, value):
        p = self.root / name
        p.write_bytes(value if isinstance(value, bytes) else value.encode('utf-8'))
        return p

    def plan(self, source, edits, **changes):
        data = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'edits': edits}
        data.update(changes)
        return self.write('plan.json', json.dumps(data))

    def edit(self, text, old, new, reason='Remove a duplicated expression.'):
        start = text.index(old)
        return dict(start=start, end=start+len(old), before=old, after=new, reason=reason)

    def invoke(self, source, *args):
        original = source.read_bytes() if source.is_file() else None
        result = subprocess.run([sys.executable, str(TOOL), str(source), *map(str,args)], capture_output=True, encoding='utf-8')
        self.assertEqual(result.stderr, '')
        value = json.loads(result.stdout)
        self.assertEqual(value['assessment']['correctness']['status'], 'NOT_ASSESSED')
        self.assertEqual(value['assessment']['usefulness']['status'], 'NOT_ASSESSED')
        if original is not None:
            self.assertEqual(source.read_bytes(), original)
        return result.returncode, value

    def test_exact_word_change_preserves_crlf_unicode_and_surroundings(self):
        text = '🧪 First line.\r\n\r\nA measurment follows.\r\n'
        source = self.write('before.txt', text)
        p = self.plan(source, [self.edit(text,'measurment','measurement','Correct the spelling.')])
        output = self.root/'after.txt'
        code, report = self.invoke(source,'--plan',p,'--output',output)
        self.assertEqual(code,0)
        self.assertEqual(output.read_bytes(),text.replace('measurment','measurement').encode('utf-8'))
        self.assertEqual(report['changes'][0]['location'], {'line':3,'column':3})
        self.assertEqual(report['output']['sha256'], hashlib.sha256(output.read_bytes()).hexdigest())

    def test_adjacent_changes_and_original_offsets(self):
        source = self.write('before.txt','abcd')
        p = self.plan(source,[dict(start=1,end=2,before='b',after='BB',reason='Clarify a term.'),dict(start=2,end=3,before='c',after='',reason='Remove duplicate material.')])
        out = self.root/'after.txt'
        code,_ = self.invoke(source,'--plan',p,'--output',out)
        self.assertEqual(code,0)
        self.assertEqual(out.read_text(),'aBBd')

    def test_input_edit_order_does_not_shift_offsets(self):
        text='Use this here and that there.'
        source=self.write('before.txt',text)
        p=self.plan(source,[self.edit(text,'that','one'),self.edit(text,'this','it')])
        out=self.root/'after.txt'
        code,report=self.invoke(source,'--plan',p,'--output',out)
        self.assertEqual(code,0)
        self.assertEqual(out.read_text(),'Use it here and one there.')
        self.assertLess(report['changes'][0]['start'], report['changes'][1]['start'])

    def test_empty_plan_preserves_a_good_passage(self):
        source=self.write('before.txt','A complete thought can stand.\n')
        out=self.root/'after.txt'
        code,report=self.invoke(source,'--plan',self.plan(source,[]),'--output',out)
        self.assertEqual(code,0)
        self.assertEqual(source.read_bytes(),out.read_bytes())
        self.assertEqual(report['measurements']['net_words_removed'],0)

    def test_stale_hash_blocks_output(self):
        source=self.write('before.txt','Keep this.')
        p=self.plan(source,[],source_sha256='0'*64)
        out=self.root/'after.txt'
        code,_=self.invoke(source,'--plan',p,'--output',out)
        self.assertEqual(code,2)
        self.assertFalse(out.exists())

    def test_wrong_source_substring_blocks_output(self):
        source=self.write('before.txt','Keep this.')
        p=self.plan(source,[dict(start=0,end=4,before='Lose',after='Read',reason='Make the action clear.')])
        code,_=self.invoke(source,'--plan',p)
        self.assertEqual(code,2)

    def test_overlapping_and_same_start_edits_are_rejected(self):
        source=self.write('before.txt','abcd')
        for second in [dict(start=1,end=3,before='bc',after='X',reason='Clarify.'),dict(start=0,end=0,before='',after='X',reason='Add context.')]:
            with self.subTest(second=second):
                p=self.plan(source,[dict(start=0,end=2,before='ab',after='A',reason='Clarify.'),second])
                code,_=self.invoke(source,'--plan',p)
                self.assertEqual(code,2)

    def test_boolean_and_out_of_range_offsets_are_rejected(self):
        source=self.write('before.txt','abcd')
        for start,end in [(True,2),(-1,2),(0,5),(3,2)]:
            with self.subTest(bounds=(start,end)):
                p=self.plan(source,[dict(start=start,end=end,before='ab',after='A',reason='Clarify.')])
                code,_=self.invoke(source,'--plan',p)
                self.assertEqual(code,2)

    def test_empty_reason_and_noop_are_rejected(self):
        source=self.write('before.txt','abcd')
        for after,reason in [('X','  '),('ab','No change.')]:
            with self.subTest(after=after):
                p=self.plan(source,[dict(start=0,end=2,before='ab',after=after,reason=reason)])
                code,_=self.invoke(source,'--plan',p)
                self.assertEqual(code,2)

    def test_duplicate_json_keys_and_extra_fields_are_rejected(self):
        source=self.write('before.txt','abcd')
        p=self.write('plan.json','{"edits":[],"edits":[],"source_sha256":"'+hashlib.sha256(source.read_bytes()).hexdigest()+'"}')
        code,_=self.invoke(source,'--plan',p)
        self.assertEqual(code,2)
        p=self.plan(source,[],unrecognized=True)
        code,_=self.invoke(source,'--plan',p)
        self.assertEqual(code,2)

    def test_existing_output_and_source_alias_are_not_overwritten(self):
        source=self.write('before.txt','Keep this.')
        p=self.plan(source,[])
        out=self.write('after.txt','Existing content.')
        code,_=self.invoke(source,'--plan',p,'--output',out)
        self.assertEqual(code,2)
        self.assertEqual(out.read_text(),'Existing content.')
        code,_=self.invoke(source,'--plan',p,'--output',source)
        self.assertEqual(code,2)
        plan_bytes=p.read_bytes()
        code,_=self.invoke(source,'--plan',p,'--output',p)
        self.assertEqual(code,2)
        self.assertEqual(p.read_bytes(),plan_bytes)

    def test_invalid_utf8_and_malformed_plan_return_json_failure(self):
        source=self.write('before.txt',b'\xff')
        p=self.write('plan.json','{}')
        code,_=self.invoke(source,'--plan',p)
        self.assertEqual(code,2)
        source=self.write('before.txt','Keep this.')
        p=self.write('plan.json','{broken')
        code,_=self.invoke(source,'--plan',p)
        self.assertEqual(code,2)

    def test_compare_reports_growth_and_does_not_claim_local_preservation(self):
        source=self.write('before.txt','The pump stops.')
        after=self.write('after.txt','The pump stops when the timer expires.')
        code,r=self.invoke(source,'--compare',after)
        self.assertEqual(code,0)
        self.assertEqual(r['measurements']['before_words'],3)
        self.assertEqual(r['measurements']['after_words'],7)
        self.assertEqual(r['measurements']['net_words_removed'],-4)
        self.assertEqual(r['outside_named_spans'],'NOT_ASSESSED in comparison mode.')

    def test_compare_cannot_write_an_output(self):
        source=self.write('before.txt','Keep this.')
        after=self.write('after.txt','Keep this.')
        out=self.root/'new.txt'
        code,_=self.invoke(source,'--compare',after,'--output',out)
        self.assertEqual(code,2)
        self.assertFalse(out.exists())

    def test_whole_block_deletion_is_visible_and_permitted(self):
        text='Repeated point.\n\nA useful next point.\n'
        source=self.write('before.txt',text)
        p=self.plan(source,[self.edit(text,'Repeated point.','')])
        code,r=self.invoke(source,'--plan',p)
        self.assertEqual(code,0)
        self.assertEqual(r['original_blocks'][0]['selected_percent'],100)
        self.assertTrue(r['original_blocks'][0]['whole_block_selected'])
        self.assertEqual(r['original_blocks'][1]['selected_percent'],0)
        self.assertEqual(r['measurements']['net_words_removed'],2)

    def test_insertion_and_empty_source_have_defined_measurements(self):
        source=self.write('before.txt','')
        p=self.plan(source,[dict(start=0,end=0,before='',after='New context.',reason='Supply the required context.')])
        out=self.root/'after.txt'
        code,r=self.invoke(source,'--plan',p,'--output',out)
        self.assertEqual(code,0)
        self.assertEqual(out.read_text(),'New context.')
        self.assertIsNone(r['measurements']['net_reduction_percent'])
        self.assertEqual(r['measurements']['words_inserted'],2)

    def test_measurement_matches_net_change_and_is_repeatable(self):
        source=self.write('before.txt','Record the result for future monitoring and tracking.')
        after=self.write('after.txt','Record the result for monitoring.')
        code,a=self.invoke(source,'--compare',after)
        other,b=self.invoke(source,'--compare',after)
        self.assertEqual(code,0)
        self.assertEqual(other,0)
        self.assertEqual(a,b)
        m=a['measurements']
        self.assertEqual(m['words_removed_or_replaced']-m['words_inserted'],m['net_words_removed'])


if __name__ == '__main__':
    unittest.main()
