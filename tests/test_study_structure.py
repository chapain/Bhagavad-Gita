"""Prove the story-map checks reject the defects they are intended to catch."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'source'))
from check_study_structure import audit, load_book
from audit_titles import possessive_side


class StudyStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_book = load_book()

    def setUp(self):
        self.metadata, self.english, self.localized, self.built = copy.deepcopy(self.valid_book)

    def errors(self):
        return audit(self.metadata, self.english, self.localized, self.built)[0]

    def assert_rejected(self, message):
        self.assertTrue(any(message in error for error in self.errors()), self.errors())

    def replace_part(self, ch, ti, pi, **fields):
        part = list(self.english[ch][ti][2][pi])
        for key, value in fields.items():
            part[{'title': 0, 'desc': 1, 'start': 2, 'end': 3}[key]] = value
        self.english[ch][ti][2][pi] = tuple(part)

    def test_reviewed_book_passes(self):
        self.assertEqual(self.errors(), [])

    def test_missing_verse_is_rejected(self):
        self.english[1][0][2].pop(0)
        self.assert_rejected('verse map has a gap')

    def test_reordered_verses_are_rejected(self):
        parts = self.english[1][0][2]
        parts[0], parts[1] = parts[1], parts[0]
        self.assert_rejected('reordered verse')

    def test_localized_ranges_must_match(self):
        parts = self.localized['ne'][1][0][2]
        part = parts[0]
        parts[0] = (part[0], part[1], '1.02', '1.02')
        self.assert_rejected('ne verse ranges are misaligned')

    def test_pilot_map_cannot_be_silently_recropped(self):
        verse = self.english[1][0][2].pop()
        self.english[1][1][2].insert(0, verse)
        self.assert_rejected('chapter 1: the reviewed story map changed')

    def test_long_theme_requires_review(self):
        themes = self.english[3]
        merged = [part for theme in themes[:3] for part in theme[2]]
        self.english[3] = [('Unreviewed merged theme', 'Temporary test description.', merged)] + themes[3:]
        self.assert_rejected('more than six verses requires a reviewed exception')

    def test_a_pearl_cannot_cover_two_verses(self):
        self.replace_part(1, 0, 0, end='1.02')
        self.assert_rejected('a pearl must be exactly one verse')

    def test_empty_verse_description_is_rejected(self):
        self.replace_part(1, 0, 0, desc='')
        self.assert_rejected('missing English title or description')

    def test_duplicate_verse_titles_are_rejected(self):
        self.replace_part(1, 0, 1, title=self.english[1][0][2][0][0])
        self.assert_rejected('duplicate English verse title')

    def test_overlong_verse_title_is_rejected(self):
        self.replace_part(1, 0, 0, title='A' * 55)
        self.assert_rejected('verse title is too long')

    def test_unbuilt_editorial_change_is_rejected(self):
        self.built[1]['themes'][0]['parts'][0]['titles']['en'] = 'Stale generated title'
        self.assert_rejected('built en verse copy differs from source')

    def test_bhishma_and_bhima_possessives_are_independent(self):
        title = 'Bhīṣma guards our army; Bhīma guards theirs'.lower()
        self.assertEqual(possessive_side(title, 'Bhīṣma'), 'our')
        self.assertEqual(possessive_side(title, 'Bhīma'), 'their')

    def test_inverted_army_sides_remain_detectable(self):
        wrong = 'Bhīṣma guards their army; Bhīma guards ours'.lower()
        literal = 'Ours, guarded by Bhīṣma; theirs, guarded by Bhīma'.lower()
        for name in ('Bhīṣma', 'Bhīma'):
            self.assertNotEqual(possessive_side(wrong, name), possessive_side(literal, name))

    def test_four_instructions_recur_not_the_entire_verse(self):
        self.assertIn('same four instructions', self.english[9][-1][1])
        self.assertNotIn('repeats this verse', self.english[9][-1][1])
        self.assertIn('चार आदेश', self.localized['ne'][9][-1][1])
        self.assertIn('चार निर्देश', self.localized['hi'][9][-1][1])
        def lines(ch, ref):
            verse = next(v for t in self.built[ch]['themes'] for p in t['parts']
                         for v in p['sutras'] if v['n'] == ref)
            return [''.join(row['t'].split()) for row in verse['lines'] if row['k'] == 'l']
        a, b = lines(9, '9.34'), lines(18, '18.65')
        self.assertEqual(a[0], b[0])
        self.assertNotEqual(a[1], b[1])


if __name__ == '__main__':
    unittest.main()
