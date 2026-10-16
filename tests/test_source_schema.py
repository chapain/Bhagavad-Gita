"""Mutation tests for the strict canonical chapter JSON schema."""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source"))
from schema import validate_chapters  # noqa: E402


class CanonicalSourceSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = [
            json.loads((ROOT / "source" / f"ch{num}.json").read_text(encoding="utf-8"))
            for num in range(1, 19)
        ]

    def changed(self, edit, expected):
        data = copy.deepcopy(self.chapters)
        edit(data)
        errors = validate_chapters(data)
        self.assertTrue(errors, "the malformed records must be rejected")
        self.assertIn(expected, "\n".join(errors))

    def test_canonical_records_pass(self):
        self.assertEqual(validate_chapters(self.chapters), [])

    def test_root_must_be_an_array(self):
        self.assertIn("chapters: must be an array", "\n".join(validate_chapters({"num": 1})))

    def test_exactly_eighteen_chapters_are_required(self):
        self.assertIn("must contain exactly 18 records", "\n".join(
            validate_chapters(self.chapters[:-1])))

    def test_chapter_keys_are_exact(self):
        self.changed(lambda d: d[0].pop("themes"), "chapter 1: invalid keys (missing ['themes'])")
        self.changed(lambda d: d[0].__setitem__("legacy", 1), "unexpected ['legacy']")
        self.changed(lambda d: d[0]["themes"][0].__setitem__("legacy", 1),
                     "chapter 1 theme 1: invalid keys (unexpected ['legacy'])")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0].__setitem__("legacy", 1),
                     "chapter 1 theme 1 part 1: invalid keys (unexpected ['legacy'])")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0].__setitem__("legacy", 1),
                     "verse 1: invalid keys (unexpected ['legacy'])")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0]["flow"][1].__setitem__("legacy", 1),
                     "verse 1.flow 2: invalid keys (unexpected ['legacy'])")

    def test_boolean_is_not_a_chapter_number(self):
        self.changed(lambda d: d[0].__setitem__("num", True), "chapter 1.num: must be integer 1")
        self.changed(lambda d: d[0].__setitem__("verses", True),
                     "chapter 1.verses: must be a positive integer")

    def test_language_maps_require_three_nonempty_strings(self):
        self.changed(lambda d: d[0].__setitem__("names", {"en": "Gita"}),
                     "chapter 1.names: must contain exactly en/ne/hi")
        self.changed(lambda d: d[0].__setitem__("subs", None),
                     "chapter 1.subs: must be an object with en/ne/hi strings")
        self.changed(lambda d: d[0]["themes"][0]["titles"].__setitem__("hi", " "),
                     "chapter 1 theme 1.titles.hi: must be a non-empty string")

    def test_theme_and_part_collections_must_be_nonempty_arrays(self):
        self.changed(lambda d: d[0].__setitem__("themes", {}),
                     "chapter 1.themes: must be a non-empty array")
        self.changed(lambda d: d[0]["themes"][0].__setitem__("parts", []),
                     "chapter 1 theme 1.parts: must be a non-empty array")

    def test_ranges_must_be_padded_and_match_their_verses(self):
        self.changed(lambda d: d[0]["themes"][0].__setitem__("range", "1.1-1.3"),
                     "must be a padded range joined by an en dash")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0].__setitem__("range", "1.02–1.02"),
                     "must match contained verses 1.01–1.01")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0].__setitem__("n", "01.01"),
                     "must use canonical verse id 1.01")
        self.changed(lambda d: d[0]["themes"][0].__setitem__("range", "01.01–01.16"),
                     "must use unpadded chapter numbers and two-digit verses")

    def test_every_part_holds_one_verse_and_ids_stay_sequential(self):
        def add_second_verse(data):
            part = data[0]["themes"][0]["parts"][0]
            part["sutras"].append(copy.deepcopy(part["sutras"][0]))
        self.changed(add_second_verse, "must contain exactly one verse, got 2")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0].__setitem__("n", "1.02"),
                     "expected 1.01, got 1.02")

    def test_verse_translation_fields_are_language_maps(self):
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0].__setitem__("lits", []),
                     "must be an object with en/ne/hi strings")

    def test_flow_requires_four_padas_and_valid_five_field_words(self):
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0]["flow"].pop(),
                     "must contain exactly four pāda rows, got 3")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0]["flow"][1]["words"][0].pop(),
                     "must be a five-string [deva, iast, en, ne, hi] row")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0]["flow"][1]["words"][0].__setitem__(0, ""),
                     "flow 2.words 1.deva: must be a non-empty string")

    def test_flow_kind_and_syllable_count_are_typed(self):
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0]["flow"][1].__setitem__("k", "x"),
                     "must be 'p' (pāda) or 's' (speaker)")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0]["flow"][1].__setitem__("n", True),
                     "must be a positive integer")

        def add_second_speaker(data):
            flow = data[0]["themes"][0]["parts"][0]["sutras"][0]["flow"]
            speaker = next(item for item in flow if item["k"] == "s")
            flow.append(copy.deepcopy(speaker))
        self.changed(add_second_speaker, "may contain at most one speaker row")

    def test_bad_nested_types_return_errors_not_tracebacks(self):
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0].__setitem__("flow", 7),
                     "verse 1.flow: must be an array")
        self.changed(lambda d: d[0]["themes"][0]["parts"][0]["sutras"][0]["flow"].__setitem__(0, None),
                     "verse 1.flow 1: must be an object")


if __name__ == "__main__":
    unittest.main()
