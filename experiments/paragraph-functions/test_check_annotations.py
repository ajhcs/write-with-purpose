import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_annotations import CATALOG, InputError, check


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "examples/queue-explainer.txt"
ANNOTATIONS = HERE / "examples/queue-explainer.annotations.json"


class AnnotationChecks(unittest.TestCase):
    def setUp(self):
        self.source = SOURCE.read_bytes()
        self.manifest = json.loads(ANNOTATIONS.read_text(encoding="utf-8"))
        self.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def run_check(self):
        return check(self.source, self.manifest, self.catalog)

    def test_example_checks_mechanics_only(self):
        result = self.run_check()
        self.assertEqual(result["input_checks"], "passed")
        self.assertEqual(result["limit_status"], "met")
        self.assertEqual(result["semantic_assessment"], "not_performed")
        self.assertEqual(result["paragraphs"][0]["whitespace_tokens"], 26)
        self.assertLess(result["annotated_characters"], result["source_characters"])

    def test_stale_source_is_rejected(self):
        self.source += b"New text."
        with self.assertRaisesRegex(InputError, "hash mismatch"):
            self.run_check()

    def test_wrong_quote_and_bounds_are_rejected(self):
        for field, value in (("quote", "invented text"), ("start", -1), ("end", 999999), ("start", True)):
            with self.subTest(field=field, value=value):
                manifest = copy.deepcopy(self.manifest)
                manifest["paragraphs"][0][field] = value
                with self.assertRaises(InputError):
                    check(self.source, manifest, self.catalog)

    def test_unknown_function_is_rejected(self):
        self.manifest["paragraphs"][0]["observed_functions"] = ["conclude"]
        with self.assertRaisesRegex(InputError, "unknown label"):
            self.run_check()

    def test_semantically_wrong_registered_label_is_not_certified(self):
        self.manifest["paragraphs"][0]["observed_functions"] = ["instruct"]
        result = self.run_check()
        self.assertEqual(result["input_checks"], "passed")
        self.assertEqual(result["semantic_assessment"], "not_performed")
        self.assertEqual(result["observations"][0]["code"], "ROLE_LABEL_DIFFERENCE")

    def test_mixed_and_unresolved_roles_are_permitted(self):
        self.manifest["paragraphs"][0]["observed_functions"] = ["orient", "assert"]
        self.manifest["paragraphs"][1]["observed_functions"] = []
        self.manifest["paragraphs"][1]["annotation_status"] = "unresolved"
        self.assertEqual(self.run_check()["input_checks"], "passed")

    def test_minimum_and_zero_maximum_are_enforced(self):
        self.manifest["constraints"] = [
            {"paragraph": "p1", "unit": "whitespace_tokens", "min": 100, "source": "test contract"},
            {"paragraph": "p2", "unit": "whitespace_tokens", "max": 0, "source": "test contract"},
        ]
        result = self.run_check()
        self.assertEqual(result["limit_status"], "violated")
        self.assertEqual({v["code"] for v in result["violations"]},
                         {"BELOW_DECLARED_MINIMUM", "ABOVE_DECLARED_MAXIMUM"})

    def test_absent_limits_do_not_invent_defaults(self):
        self.manifest["constraints"] = []
        self.assertEqual(self.run_check()["limit_status"], "none_declared")

    def test_invalid_constraints_are_rejected(self):
        variants = [
            {"max": True}, {"max": -1}, {"max": 1.5}, {"max": "40"},
            {"min": 50, "max": 40}, {"max": None}, {"maximum": 40},
            {"unit": "sentences"}, {"source": ""}, {"paragraph": "missing"},
        ]
        for update in variants:
            with self.subTest(update=update):
                manifest = copy.deepcopy(self.manifest)
                manifest["constraints"][0].update(update)
                with self.assertRaises(InputError):
                    check(self.source, manifest, self.catalog)

    def test_duplicate_ids_are_rejected(self):
        for field in ("paragraphs", "sections"):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest[field].append(copy.deepcopy(manifest[field][0]))
                with self.assertRaisesRegex(InputError, "duplicate ID"):
                    check(self.source, manifest, self.catalog)

    def test_dangling_section_evidence_and_relation_references_are_rejected(self):
        variants = [copy.deepcopy(self.manifest) for _ in range(3)]
        variants[0]["paragraphs"][0]["section"] = "missing"
        variants[1]["paragraphs"][0]["evidence_refs"] = ["missing"]
        variants[2]["relations"][0]["to"] = "missing"
        for manifest in variants:
            with self.subTest(manifest=manifest):
                with self.assertRaisesRegex(InputError, "unknown"):
                    check(self.source, manifest, self.catalog)

    def test_overlapping_and_out_of_order_spans_are_rejected(self):
        self.manifest["paragraphs"][0], self.manifest["paragraphs"][1] = (
            self.manifest["paragraphs"][1], self.manifest["paragraphs"][0])
        with self.assertRaisesRegex(InputError, "overlap or are out of order"):
            self.run_check()

    def test_unicode_character_offsets_preserve_crlf(self):
        text = "Éclair 🧭.\r\n\r\nSecond paragraph.\r\n"
        source = text.encode("utf-8")
        manifest = copy.deepcopy(self.manifest)
        manifest["source_sha256"] = hashlib.sha256(source).hexdigest()
        manifest["paragraphs"] = []
        for i, quote in enumerate(("Éclair 🧭.", "Second paragraph."), 1):
            start = text.index(quote)
            manifest["paragraphs"].append({"id": f"p{i}", "section": "question",
                                          "start": start, "end": start + len(quote), "quote": quote,
                                          "planned_functions": [], "observed_functions": [],
                                          "annotation_status": "unresolved", "evidence_refs": []})
        manifest["relations"] = []
        manifest["constraints"] = []
        result = check(source, manifest, self.catalog)
        self.assertEqual([p["whitespace_tokens"] for p in result["paragraphs"]], [2, 2])

    def test_catalogue_version_mismatch_is_rejected(self):
        self.manifest["catalog_version"] = "unknown"
        with self.assertRaisesRegex(InputError, "version mismatch"):
            self.run_check()

    def test_cli_exit_codes_and_input_preservation(self):
        # Keep all temporary working data on the repository's /workspace volume.
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            source = Path(directory) / "source.txt"
            annotations = Path(directory) / "annotations.json"
            source.write_bytes(self.source)
            for expected in (0, 1, 2):
                manifest = copy.deepcopy(self.manifest)
                if expected == 1:
                    manifest["constraints"][0]["max"] = 0
                if expected == 2:
                    annotations.write_text("{bad json", encoding="utf-8")
                else:
                    annotations.write_text(json.dumps(manifest), encoding="utf-8")
                before = (source.read_bytes(), annotations.read_bytes())
                process = subprocess.run([sys.executable, str(HERE / "check_annotations.py"),
                                          str(source), str(annotations)], capture_output=True, text=True)
                self.assertEqual(process.returncode, expected, process.stderr)
                self.assertEqual(json.loads(process.stdout)["semantic_assessment"], "not_performed")
                self.assertEqual(before, (source.read_bytes(), annotations.read_bytes()))


if __name__ == "__main__":
    unittest.main()
