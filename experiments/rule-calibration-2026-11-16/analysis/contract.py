"""Bounded structural checks for the calibration, not semantic adjudication.

Offsets are zero-based Python Unicode code points, end exclusive. Hashes are
SHA-256 of exact UTF-8 text. No source text or labels are inferred or repaired.
"""
from copy import deepcopy
from hashlib import sha256

FUNCTION_FIELDS = {
    'orient': ('prepared_contribution', 'preparation_link'),
    'define': ('term', 'meaning_or_distinction', 'definition_scope'),
    'report': ('reported_content', 'attribution', 'event_or_claim_status'),
    'assert': ('position', 'position_holder', 'commitment_job'),
    'support': ('supported_claim', 'intended_link', 'basis_kind'),
    'explain': ('relata', 'connection_made_intelligible'),
    'illustrate': ('illustrated_idea', 'concretizing_link', 'case_status'),
    'compare': ('alternatives', 'shared_dimension', 'stated_relationship'),
    'interpret': ('input_material', 'inference_or_significance', 'transformation'),
    'qualify': ('affected_claim', 'scope_change', 'qualification_kind'),
    'instruct': ('addressed_actor', 'action', 'directive_context'),
    'narrate': ('participant_or_subject', 'events', 'change_through_time'),
}
RELATIONS = {'orient', 'support', 'illustrate', 'qualify'}
STATUSES = {'clear', 'ambiguous', 'insufficient_context', 'extraction_uncertain'}
ASSESSMENT_ENUMS = {
    'basis_kind': {'observed_in_current_source', 'attributed_report', 'reasoning', 'hypothetical', 'analogy', 'mixed', 'not_applicable', 'unknown'},
    'role_adequacy': {'not_assessed', 'adequate_for_stated_task', 'inadequate', 'disputed'},
    'empirical_evidence_status': {'not_claimed', 'claimed_unverified', 'independently_checked', 'not_applicable', 'unknown'},
    'truth_status': {'not_assessed', 'corroborated_with_sources', 'challenged_with_sources', 'disputed'},
}


def _digest(text):
    return sha256(text.encode('utf-8')).hexdigest()


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(packet, manifest):
    """Return human-readable structural errors; never modify either input."""
    errors = []
    def err(path, message):
        errors.append(f'{path}: {message}')
    if not isinstance(packet, dict) or not isinstance(manifest, dict):
        return ['packet and manifest must be objects']
    for key in ('coder_id', 'arm', 'stage', 'model', 'started_at_utc', 'finished_at_utc'):
        if not _nonempty(packet.get(key)):
            err('packet.' + key, 'required nonempty string')
    arm = packet.get('arm')
    if arm not in ('original', 'revised'):
        err('packet.arm', 'must be original or revised')
    units, targets = {}, {}
    unit_list = manifest.get('units')
    target_list = manifest.get('targets')
    if not isinstance(unit_list, list) or not isinstance(target_list, list):
        return errors + ['manifest: units and targets must be lists']
    for i, unit in enumerate(unit_list):
        p = f'manifest.units[{i}]'
        if not isinstance(unit, dict):
            err(p, 'must be an object'); continue
        uid = unit.get('unit_id')
        if not _nonempty(uid) or uid in units:
            err(p, 'unit_id must be nonempty and unique'); continue
        units[uid] = unit
        if not isinstance(unit.get('text'), str) or not _nonempty(unit.get('source_id')) or not _nonempty(unit.get('kind')):
            err(p, 'requires text, source_id and kind')
        elif unit.get('sha256') != _digest(unit['text']):
            err(p, 'text sha256 mismatch')
    for i, target in enumerate(target_list):
        p = f'manifest.targets[{i}]'
        if not isinstance(target, dict):
            err(p, 'must be an object'); continue
        pid = target.get('paragraph_id')
        if not _nonempty(pid) or pid in targets:
            err(p, 'paragraph_id must be nonempty and unique'); continue
        targets[pid] = target
        uid = target.get('unit_id')
        if uid not in units or target.get('source_id') != units[uid].get('source_id'):
            err(p, 'unit and source binding invalid')
        if not _nonempty(target.get('stage')):
            err(p, 'stage required')

    def anchors_check(anchors, p, reviewed, source):
        if not isinstance(anchors, list) or not anchors:
            err(p, 'at least one anchor required'); return
        for j, a in enumerate(anchors):
            ap = f'{p}[{j}]'
            if not isinstance(a, dict):
                err(ap, 'must be an object'); continue
            uid, quote = a.get('unit_id'), a.get('quote')
            if uid not in units:
                err(ap, 'unknown unit_id'); continue
            if uid not in reviewed:
                err(ap, 'unit was not reviewed')
            if units[uid].get('source_id') != source:
                err(ap, 'unit source differs from target source')
            if not _nonempty(quote) or not isinstance(units[uid].get('text'), str):
                err(ap, 'quote must be nonempty'); continue
            text = units[uid]['text']
            starts = []
            pos = text.find(quote)
            while pos >= 0:
                starts.append(pos)
                pos = text.find(quote, pos + 1)
            if not starts:
                err(ap, 'exact quote not found'); continue
            occurrence = a.get('occurrence')
            if occurrence is None and len(starts) == 1:
                continue
            if type(occurrence) is not int or occurrence < 0 or occurrence >= len(starts):
                err(ap, 'occurrence must be an in-bounds zero-based integer')
    annotations = packet.get('annotations')
    if not isinstance(annotations, list):
        return errors + ['packet.annotations: must be a list']
    seen_paragraphs, seen_target_ids = set(), set()
    for i, ann in enumerate(annotations):
        p = f'annotations[{i}]'
        if not isinstance(ann, dict):
            err(p, 'must be an object'); continue
        pid = ann.get('paragraph_id')
        if pid not in targets or pid in seen_paragraphs:
            err(p, 'paragraph_id must be unique and in manifest'); continue
        seen_paragraphs.add(pid)
        binding = targets[pid]
        if packet.get('stage') != binding.get('stage'):
            err(p, 'stage does not match manifest target')
        ctx = ann.get('context')
        if not isinstance(ctx, dict):
            err(p, 'context required'); continue
        if arm == 'revised':
            for key in ('family', 'form', 'section', 'audience', 'reader_task', 'neutral_contribution', 'context_reason', 'extraction_issues'):
                if key not in ctx:
                    err(p + '.context', f'{key} required')
            if not isinstance(ctx.get('extraction_issues'), list):
                err(p + '.context.extraction_issues', 'must be a list')
        sufficiency = ctx.get('context_sufficiency')
        if sufficiency not in ('sufficient', 'insufficient', 'uncertain', 'unknown_legacy'):
            err(p + '.context', 'invalid context_sufficiency')
        reviewed = ctx.get('reviewed_units')
        if not isinstance(reviewed, list) or not reviewed:
            err(p + '.context.reviewed_units', 'nonempty list required'); reviewed = []
        for uid in reviewed:
            if not isinstance(uid, str) or uid not in units:
                err(p + '.context.reviewed_units', 'unknown unit_id')
            elif units[uid].get('source_id') != binding.get('source_id'):
                err(p + '.context.reviewed_units', 'unit source differs from target source')
        if binding.get('unit_id') not in reviewed:
            err(p + '.context.reviewed_units', 'must include paragraph unit')
        roles = ann.get('roles')
        if not isinstance(roles, list):
            err(p + '.roles', 'must be a list'); continue
        decisions_by_function = {}
        derived_clear, derived_unresolved = set(), set()
        for j, role in enumerate(roles):
            rp = f'{p}.roles[{j}]'
            if not isinstance(role, dict):
                err(rp, 'must be an object'); continue
            fid, decision, status = role.get('function_id'), role.get('decision'), role.get('status')
            if isinstance(fid, str) and decision in ('present', 'rejected', 'unresolved'):
                decisions_by_function.setdefault(fid, set()).add(decision)
                if decision == 'present' and status == 'clear':
                    derived_clear.add(fid)
                if decision == 'unresolved':
                    derived_unresolved.add(fid)
            if fid not in FUNCTION_FIELDS:
                err(rp, 'unknown function_id')
            if decision not in ('present', 'rejected', 'unresolved'):
                err(rp, 'invalid decision')
            if status not in STATUSES:
                err(rp, 'invalid status')
            if decision in ('present', 'rejected') and status != 'clear' or decision == 'unresolved' and status not in STATUSES - {'clear'}:
                err(rp, 'decision and status inconsistent')
            if not _nonempty(role.get('reason')):
                err(rp, 'reason required')
            anchors_check(role.get('anchors'), rp + '.anchors', reviewed, binding.get('source_id'))
            role_anchors = role.get('anchors')
            if not isinstance(role_anchors, list) or not any(isinstance(a, dict) and a.get('unit_id') == binding.get('unit_id') for a in role_anchors):
                err(rp + '.anchors', 'at least one anchor must be in the paragraph unit')
            if arm != 'revised':
                # Optional original-arm targets are not required or interpreted,
                # but any supplied anchors must still resolve exactly.
                if 'targets' in role:
                    if not isinstance(role['targets'], list):
                        err(rp + '.targets', 'must be a list when supplied')
                    else:
                        for k, target in enumerate(role['targets']):
                            if not isinstance(target, dict):
                                err(f'{rp}.targets[{k}]', 'must be an object')
                            elif 'anchors' in target:
                                anchors_check(target['anchors'], f'{rp}.targets[{k}].anchors', reviewed, binding.get('source_id'))
                continue
            fields = role.get('role_fields')
            if not isinstance(fields, dict):
                err(rp, 'role_fields required'); fields = {}
            for field in FUNCTION_FIELDS.get(fid, ()):
                if field not in fields or fields[field] is None or fields[field] == '':
                    err(rp + '.role_fields', f'{field} required')
            alternatives = role.get('alternatives')
            if not isinstance(alternatives, list) or status == 'ambiguous' and not alternatives:
                err(rp + '.alternatives', 'list required; ambiguous status requires alternatives')
            assessment = role.get('evidence_assessment')
            if not isinstance(assessment, dict):
                err(rp, 'evidence_assessment required'); assessment = {}
            for key, allowed in ASSESSMENT_ENUMS.items():
                if assessment.get(key) not in allowed:
                    err(rp + '.evidence_assessment', f'invalid {key}')
            if assessment.get('basis_kind') == 'hypothetical' and assessment.get('empirical_evidence_status') == 'independently_checked':
                err(rp + '.evidence_assessment', 'hypothetical basis contradicts independently checked empirical evidence')
            if (assessment.get('role_adequacy') not in (None, 'not_assessed') or assessment.get('truth_status') not in (None, 'not_assessed') or assessment.get('empirical_evidence_status') == 'independently_checked') and not _nonempty(assessment.get('assessment_reason')):
                err(rp + '.evidence_assessment', 'assessment_reason required for assessed claims')
            rt = role.get('targets')
            if not isinstance(rt, list):
                err(rp, 'targets must be a list'); rt = []
            if fid in RELATIONS and not rt:
                if decision == 'present':
                    err(rp, 'present relation requires target')
                elif decision == 'rejected' and (sufficiency != 'sufficient' or not _nonempty(role.get('target_absence_reason'))):
                    err(rp, 'rejected relation without target requires sufficient context and target_absence_reason')
                elif decision == 'unresolved' and (status not in ('insufficient_context', 'extraction_uncertain') or not _nonempty(role.get('missing_target_reason'))):
                    err(rp, 'unresolved relation without target requires insufficient context or uncertain extraction and missing_target_reason')
            for k, target in enumerate(rt):
                tp = f'{rp}.targets[{k}]'
                if not isinstance(target, dict):
                    err(tp, 'must be an object'); continue
                tid = target.get('target_id')
                if not _nonempty(tid) or tid in seen_target_ids:
                    err(tp, 'target_id must be nonempty and unique')
                else:
                    seen_target_ids.add(tid)
                if target.get('kind') not in ('explicit_span', 'implicit_reconstruction'):
                    err(tp, 'invalid kind')
                if target.get('status') not in STATUSES:
                    err(tp, 'invalid status')
                if fid in RELATIONS and decision == 'present' and target.get('status') != 'clear':
                    err(tp, 'present relation requires clear targets')
                for key in ('paraphrase', 'reason'):
                    if not _nonempty(target.get(key)):
                        err(tp, f'{key} required')
                anchors_check(target.get('anchors'), tp + '.anchors', reviewed, binding.get('source_id'))
        for fid, decisions in decisions_by_function.items():
            if len(decisions) > 1:
                err(p + '.roles', f'conflicting decisions for {fid}')
        expected = {'clear_labels': sorted(derived_clear), 'unresolved_labels': sorted(derived_unresolved), 'candidate_union': sorted(derived_clear | derived_unresolved)}
        for key, value in expected.items():
            if key in ann and ann[key] != value:
                err(p + '.' + key, 'supplied summary differs from derived labels')
    expected_paragraphs = {pid for pid, target in targets.items() if target.get('stage') == packet.get('stage')}
    if seen_paragraphs != expected_paragraphs:
        err('packet.annotations', 'must cover exactly the manifest targets for packet stage; missing=' + repr(sorted(expected_paragraphs - seen_paragraphs)) + ', extra=' + repr(sorted(seen_paragraphs - expected_paragraphs)))
    return errors


def normalize(packet, manifest):
    """Validate and copy packet, resolving anchors and deriving label sets.

    Raises ValueError with all detected errors. Does not change coder judgments.
    """
    errors = validate(packet, manifest)
    if errors:
        raise ValueError('\n'.join(errors))
    result = deepcopy(packet)
    units = {u['unit_id']: u for u in manifest['units']}
    targets = {t['paragraph_id']: t for t in manifest['targets']}
    def resolve(anchor):
        unit = units[anchor['unit_id']]
        quote = anchor['quote']
        occurrence = anchor.get('occurrence', 0)
        start = -1
        for _ in range(occurrence + 1):
            start = unit['text'].find(quote, start + 1)
        anchor.update(start=start, end=start + len(quote), text_sha256=_digest(quote), source_id=unit['source_id'], unit_sha256=unit['sha256'])
    for ann in result['annotations']:
        binding = targets[ann['paragraph_id']]
        ann['source_binding'] = {key: binding[key] for key in ('unit_id', 'stage', 'source_id')}
        clear, unresolved = set(), set()
        for role in ann['roles']:
            if role['decision'] == 'present' and role['status'] == 'clear':
                clear.add(role['function_id'])
            if role['decision'] == 'unresolved':
                unresolved.add(role['function_id'])
            for a in role['anchors']:
                resolve(a)
            for target in role.get('targets', []):
                for a in target.get('anchors', []):
                    resolve(a)
        ann['clear_labels'] = sorted(clear)
        ann['unresolved_labels'] = sorted(unresolved)
        ann['candidate_union'] = sorted(clear | unresolved)
    return result


if __name__ == '__main__':
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description='Validate a calibration packet against a manifest; optionally print normalized JSON.')
    parser.add_argument('packet', help='packet JSON path')
    parser.add_argument('manifest', help='manifest JSON path')
    parser.add_argument('--normalize', action='store_true', help='print normalized packet JSON after validation')
    args = parser.parse_args()
    try:
        with open(args.packet, encoding='utf-8') as f:
            packet_data = json.load(f)
        with open(args.manifest, encoding='utf-8') as f:
            manifest_data = json.load(f)
        problems = validate(packet_data, manifest_data)
        if problems:
            print('\n'.join(problems), file=sys.stderr)
            sys.exit(1)
        if args.normalize:
            print(json.dumps(normalize(packet_data, manifest_data), ensure_ascii=False, indent=2))
        else:
            print('Valid: bounded structural checks passed.')
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
