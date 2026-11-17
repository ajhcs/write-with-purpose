import copy
import hashlib
import unittest

from contract import normalize, validate


def fixture(arm='original'):
    text = 'Élan is here. Élan is here.'
    manifest = {'units': [{'unit_id': 'u', 'text': text, 'source_id': 's', 'kind': 'paragraph', 'sha256': hashlib.sha256(text.encode()).hexdigest()}], 'targets': [{'paragraph_id': 'p', 'unit_id': 'u', 'source_id': 's', 'stage': 'pilot'}]}
    context = {'reviewed_units': ['u'], 'context_sufficiency': 'sufficient'}
    if arm == 'revised':
        context.update(family=None, form=None, section=None, audience=None, reader_task=None, neutral_contribution='A claim.', context_reason='Read paragraph.', extraction_issues=[])
    role = {'function_id': 'support', 'decision': 'present', 'status': 'clear', 'reason': 'Reason for a claim.', 'anchors': [{'unit_id': 'u', 'quote': 'Élan', 'occurrence': 1}]}
    if arm == 'revised':
        role.update(role_fields={'supported_claim': 'claim', 'intended_link': 'reason', 'basis_kind': 'reasoning'}, targets=[{'target_id': 't', 'kind': 'explicit_span', 'anchors': [{'unit_id': 'u', 'quote': 'here', 'occurrence': 0}], 'paraphrase': 'claim', 'status': 'clear', 'reason': 'Located claim.'}], alternatives=[], evidence_assessment={'basis_kind': 'reasoning', 'role_adequacy': 'not_assessed', 'empirical_evidence_status': 'not_claimed', 'truth_status': 'not_assessed'})
    packet = {'coder_id': 'c', 'arm': arm, 'stage': 'pilot', 'model': 'm', 'started_at_utc': '2026-11-16T00:00:00Z', 'finished_at_utc': '2026-11-16T00:01:00Z', 'annotations': [{'paragraph_id': 'p', 'context': context, 'roles': [role], 'notes': ''}]}
    return packet, manifest


class ContractTests(unittest.TestCase):
    def test_original_preserved_and_unicode_offsets(self):
        p, m = fixture()
        original = copy.deepcopy(p)
        n = normalize(p, m)
        self.assertEqual(p, original)
        a = n['annotations'][0]['roles'][0]['anchors'][0]
        self.assertEqual((a['start'], a['end']), (14, 18))
        self.assertEqual(a['text_sha256'], hashlib.sha256('Élan'.encode()).hexdigest())
        self.assertEqual(n['annotations'][0]['clear_labels'], ['support'])
        self.assertNotIn('role_fields', n['annotations'][0]['roles'][0])

    def test_quote_occurrence_and_hash(self):
        p, m = fixture()
        p['annotations'][0]['roles'][0]['anchors'][0].pop('occurrence')
        self.assertTrue(any('occurrence' in e for e in validate(p, m)))
        p['annotations'][0]['roles'][0]['anchors'][0]['occurrence'] = 2
        self.assertTrue(any('occurrence' in e for e in validate(p, m)))
        p['annotations'][0]['roles'][0]['anchors'][0]['quote'] = 'élan'
        self.assertTrue(any('not found' in e for e in validate(p, m)))
        m['units'][0]['sha256'] = 'bad'
        self.assertTrue(any('sha256' in e for e in validate(p, m)))

    def test_revised_target_exceptions(self):
        p, m = fixture('revised')
        self.assertEqual(validate(p, m), [])
        r = p['annotations'][0]['roles'][0]
        r['targets'] = []
        self.assertTrue(any('requires target' in e for e in validate(p, m)))
        r.update(decision='rejected', target_absence_reason='No claim in reviewed context.')
        self.assertEqual(validate(p, m), [])
        p['annotations'][0]['context']['context_sufficiency'] = 'uncertain'
        self.assertTrue(any('sufficient context' in e for e in validate(p, m)))
        r.update(decision='unresolved', status='insufficient_context', missing_target_reason='Neighbor unavailable.')
        self.assertEqual(validate(p, m), [])
        self.assertEqual(normalize(p, m)['annotations'][0]['unresolved_labels'], ['support'])
        r['status'] = 'ambiguous'
        r['alternatives'] = ['possible claim']
        self.assertTrue(any('without target' in e for e in validate(p, m)))

    def test_complete_stage_coverage(self):
        p, m = fixture()
        m['targets'].append({'paragraph_id': 'p2', 'unit_id': 'u', 'source_id': 's', 'stage': 'pilot'})
        self.assertTrue(any('cover exactly' in e for e in validate(p, m)))
        m['targets'][1]['stage'] = 'other'
        self.assertEqual(validate(p, m), [])

    def test_target_unit_anchor_and_conflicting_decisions(self):
        p, m = fixture()
        m['units'].append({'unit_id': 'neighbor', 'text': 'Nearby', 'source_id': 's', 'kind': 'paragraph', 'sha256': hashlib.sha256(b'Nearby').hexdigest()})
        a = p['annotations'][0]
        a['context']['reviewed_units'].append('neighbor')
        role = a['roles'][0]
        role['anchors'] = [{'unit_id': 'neighbor', 'quote': 'Nearby'}]
        self.assertTrue(any('paragraph unit' in e for e in validate(p, m)))
        role['anchors'].append({'unit_id': 'u', 'quote': 'Élan', 'occurrence': 0})
        a['roles'].append(copy.deepcopy(role))
        self.assertEqual(validate(p, m), [])
        a['roles'][1]['decision'] = 'rejected'
        self.assertTrue(any('conflicting decisions' in e for e in validate(p, m)))

    def test_supplied_summary_must_match(self):
        p, m = fixture()
        ann = p['annotations'][0]
        ann['clear_labels'] = []
        with self.assertRaisesRegex(ValueError, 'supplied summary differs'):
            normalize(p, m)
        ann['clear_labels'] = ['support']
        ann['candidate_union'] = ['support']
        self.assertEqual(validate(p, m), [])
        self.assertEqual(normalize(p, m)['annotations'][0]['clear_labels'], ['support'])

    def test_contradiction_and_binding(self):
        p, m = fixture('revised')
        a = p['annotations'][0]['roles'][0]['evidence_assessment']
        a.update(basis_kind='hypothetical', empirical_evidence_status='independently_checked', assessment_reason='Checked.')
        self.assertTrue(any('contradicts' in e for e in validate(p, m)))
        m['targets'][0]['source_id'] = 'wrong'
        self.assertTrue(any('binding' in e for e in validate(p, m)))


if __name__ == '__main__':
    unittest.main()
