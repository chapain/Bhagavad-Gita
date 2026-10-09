"""Regression tests for the lossless Sanskrit spelling checks."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))
import check_padas as validator  # noqa: E402


class StrictTextValidatorTests(unittest.TestCase):
    def test_devanagari_preserves_phonemic_diacritics(self):
        self.assertEqual(validator.deva_to_iast("अविनश्यन्तम्"), "avinaśyantam")
        self.assertNotEqual(
            validator.strict_key(validator.deva_to_iast("अविनश्यन्तम्")),
            validator.strict_key("avināśyantam"),
        )

    def test_explicit_anusvara_conventions_only(self):
        self.assertEqual(validator.strict_key("saṃgha"), validator.strict_key("saṅgha"))
        self.assertEqual(validator.strict_key("saṁnyāsī"), validator.strict_key("sannyāsī"))
        self.assertNotEqual(validator.strict_key("tāmasa"), validator.strict_key("tamasa"))
        self.assertNotEqual(validator.strict_key("karśayantaḥ"), validator.strict_key("karṣayantaḥ"))

    def test_known_word_boundary_convention_is_narrow(self):
        self.assertIn(("2.06", "यत् वा", "yad vā"), validator.WORD_SPELLING_CONVENTIONS)
        self.assertNotIn(("2.06", "यत् वा", "yat vā"), validator.WORD_SPELLING_CONVENTIONS)


if __name__ == "__main__":
    unittest.main()
