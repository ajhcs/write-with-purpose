#!/usr/bin/env python3
"""Read-only checks on supplied paragraph annotations; no function classifier."""

import argparse
import hashlib
import json
from pathlib import Path
import re


CATALOG = Path(__file__).resolve().parents[2] / "docs/writing-harness/paragraph-functions.json"


class InputError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InputError(message)


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}: expected nonempty text")
    return value


def records(value, label):
    require(isinstance(value, list), f"{label}: expected array")
    require(all(isinstance(item, dict) for item in value), f"{label}: expected objects")
    return value


def identifiers(items, label):
    result = set()
    for item in records(items, label):
        name = nonempty(item.get("id"), f"{label}.id")
        require(name not in result, f"{label}: duplicate ID {name}")
        result.add(name)
    return result


def labels(value, allowed, label):
    require(isinstance(value, list), f"{label}: expected array")
    require(all(isinstance(item, str) for item in value), f"{label}: expected strings")
    require(len(value) == len(set(value)), f"{label}: duplicate labels")
    require(set(value) <= allowed, f"{label}: unknown label or reference")
    return value


def check(source_bytes, manifest, catalog):
    """Return mechanical findings only. Raises InputError for unusable annotations."""
    require(isinstance(manifest, dict), "manifest: expected object")
    require(isinstance(catalog, dict), "catalogue: expected object")
    require(manifest.get("schema_version") == "0.1", "unsupported annotation schema")
    nonempty(catalog.get("version"), "catalogue version")
    require(manifest.get("catalog_version") == catalog["version"], "catalogue version mismatch")
    require(manifest.get("source_sha256") == hashlib.sha256(source_bytes).hexdigest(),
            "source hash mismatch: annotations are stale or refer to another source")
    text = source_bytes.decode("utf-8")  # No newline or Unicode normalization.
    function_ids = identifiers(catalog.get("functions"), "catalogue functions")
    relation_names = catalog.get("relations")
    require(isinstance(relation_names, list) and
            all(isinstance(name, str) and name for name in relation_names),
            "catalogue relations: expected names")
    require(len(relation_names) == len(set(relation_names)), "duplicate catalogue relation")

    document = manifest.get("document")
    require(isinstance(document, dict), "document: expected object")
    for field in ("family", "form", "audience"):
        nonempty(document.get(field), f"document.{field}")
    # Family/form membership and audience accuracy are not assessed here.
    sections = records(manifest.get("sections"), "sections")
    section_ids = identifiers(sections, "sections")
    for section in sections:
        nonempty(section.get("purpose"), "section purpose")
    evidence = records(manifest.get("evidence"), "evidence")
    evidence_ids = identifiers(evidence, "evidence")
    for item in evidence:
        nonempty(item.get("kind"), "evidence kind")
        nonempty(item.get("locator"), "evidence locator")

    paragraphs = records(manifest.get("paragraphs"), "paragraphs")
    require(bool(paragraphs), "at least one annotated paragraph is required")
    paragraph_ids = identifiers(paragraphs, "paragraphs")
    counts, annotations, observations = {}, [], []
    previous_end = 0
    annotated_characters = 0
    for paragraph in paragraphs:
        pid = paragraph["id"]
        section = nonempty(paragraph.get("section"), f"{pid}.section")
        require(section in section_ids, f"{pid}: unknown section")
        start, end = paragraph.get("start"), paragraph.get("end")
        require(type(start) is int and type(end) is int, f"{pid}: offsets must be integers")
        require(0 <= start < end <= len(text), f"{pid}: invalid span bounds")
        require(start >= previous_end, f"{pid}: spans overlap or are out of order")
        previous_end = end
        span = text[start:end]
        require(span == paragraph.get("quote"), f"{pid}: quoted span differs from source")
        require(bool(span.strip()), f"{pid}: empty paragraph")
        planned = labels(paragraph.get("planned_functions"), function_ids, f"{pid}.planned")
        observed = labels(paragraph.get("observed_functions"), function_ids, f"{pid}.observed")
        status = paragraph.get("annotation_status")
        require(status in ("proposed", "reviewed", "unresolved"), f"{pid}: invalid annotation status")
        require(bool(observed) or status == "unresolved", f"{pid}: empty observed labels need unresolved status")
        labels(paragraph.get("evidence_refs"), evidence_ids, f"{pid}.evidence_refs")
        count = len(re.findall(r"\S+", span))
        counts[pid] = count
        annotated_characters += end - start
        annotations.append({"paragraph": pid, "whitespace_tokens": count,
                            "planned": planned, "observed": observed,
                            "supplied_annotation_status": status})
        if set(planned) != set(observed):
            observations.append({"code": "ROLE_LABEL_DIFFERENCE", "paragraph": pid,
                                 "meaning": "Supplied labels differ; editorial review needed."})

    relations = records(manifest.get("relations"), "relations")
    for relation in relations:
        source = nonempty(relation.get("from"), "relation.from")
        target = nonempty(relation.get("to"), "relation.to")
        require(source in paragraph_ids and target in paragraph_ids, "relation: unknown paragraph")
        require(source != target, "relation: self-reference")
        require(relation.get("type") in relation_names, "relation: unknown type")

    violations, limit_results, constrained = [], [], set()
    constraints = records(manifest.get("constraints"), "constraints")
    for constraint in constraints:
        allowed = {"paragraph", "unit", "min", "max", "source"}
        require(set(constraint) <= allowed, "constraint: unknown field")
        pid = nonempty(constraint.get("paragraph"), "constraint.paragraph")
        require(pid in paragraph_ids, "constraint: unknown paragraph")
        require(pid not in constrained, "constraint: duplicate paragraph; combine its bounds")
        constrained.add(pid)
        require(constraint.get("unit") == "whitespace_tokens", "constraint: unsupported counting unit")
        nonempty(constraint.get("source"), "constraint source")
        lower, upper = constraint.get("min"), constraint.get("max")
        require(lower is not None or upper is not None, "constraint: no declared bound")
        for bound in (lower, upper):
            require(bound is None or (type(bound) is int and bound >= 0), "constraint: invalid bound")
        require(lower is None or upper is None or lower <= upper, "constraint: minimum exceeds maximum")
        count = counts[pid]
        if lower is not None and count < lower:
            violations.append({"code": "BELOW_DECLARED_MINIMUM", "paragraph": pid,
                               "actual": count, "limit": lower})
        if upper is not None and count > upper:
            violations.append({"code": "ABOVE_DECLARED_MAXIMUM", "paragraph": pid,
                               "actual": count, "limit": upper})
        limit_results.append({**constraint, "actual": count})

    return {"input_checks": "passed", "semantic_assessment": "not_performed",
            "scope": "supplied annotated spans only; source coverage is not required",
            "counting_policy": "Non-whitespace runs in raw UTF-8 text; no markup or sentence parsing.",
            "source_sha256": manifest["source_sha256"],
            "annotated_characters": annotated_characters,
            "source_characters": len(text), "paragraphs": annotations,
            "declared_limits": limit_results,
            "limit_status": "violated" if violations else "met" if constraints else "none_declared",
            "violations": violations, "observations": observations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("annotations", type=Path)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    args = parser.parse_args()
    try:
        result = check(args.source.read_bytes(),
                       json.loads(args.annotations.read_text(encoding="utf-8")),
                       json.loads(args.catalog.read_text(encoding="utf-8")))
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({"input_checks": "failed", "semantic_assessment": "not_performed",
                          "error": str(error)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
