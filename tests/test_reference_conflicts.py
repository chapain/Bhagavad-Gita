"""Reviewed reference-conflict regressions, not an automated semantic oracle.

The offline snapshot preserves editorial decisions made against pinned online
sources. It is test-only context, never an alternative runtime content store.
See docs/padachheda-conflict-resolution.md for sources, variants and limits.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads((ROOT / 'tests/fixtures/reference_conflicts.json').read_text())


def edition():
    return {v['n']: v for c in range(1, 19)
            for t in json.loads((ROOT / f'source/ch{c}.json').read_text())['themes']
            for p in t['parts'] for v in p['sutras']}


class ReferenceConflictTests(unittest.TestCase):
    def test_eighteen_reviewed_verses_match_sourced_decisions(self):
        self.assertEqual(set(EXPECTED), {
            '1.08', '1.09', '1.13', '2.06', '2.09', '2.71', '3.30', '4.28',
            '6.09', '6.19', '6.29', '9.16', '9.34', '11.12', '11.44',
            '11.47', '12.13', '18.53'})
        current = edition()
        for number, expected in EXPECTED.items():
            with self.subTest(verse=number):
                v = current[number]
                actual = {'printed': [v['d'], v['t']],
                          'flow_text': [[f['d'], f['t']] for f in v['flow']],
                          'words': [f['words'] for f in v['flow']],
                          'lits': v['lits'], 'paras': v['paras']}
                self.assertEqual(actual, expected)

    def test_all_nirmama_occurrences_explain_non_possessiveness(self):
        found = []
        for number, v in edition().items():
            for f in v['flow']:
                for w in f['words']:
                    if w[1] == 'nirmamaḥ':
                        found.append(number)
                        self.assertEqual(w[3:], ['मेरोपनरहित', "'मेरा' भाव से रहित"])
        self.assertEqual(found, ['2.71', '3.30', '12.13', '18.53'])

    def test_retained_relative_indefinite_and_independent_evams(self):
        current = edition()
        self.assertEqual([w[1] for f in current['9.34']['flow'] for w in f['words']],
                         ['manmanāḥ', 'bhava', 'madbhaktaḥ', 'madyājī', 'mām',
                          'namaskuru', 'mām', 'eva', 'eṣyasi', 'yuktvā', 'evam',
                          'ātmānam', 'matparāyaṇaḥ'])
        rows = [w for f in current['12.19']['flow'] for w in f['words']]
        i = next(i for i, w in enumerate(rows) if w[1] == 'yena')
        self.assertEqual([w[1] for w in rows[i:i + 2]], ['yena', 'kenacit'])
        self.assertIn('content with anything', current['12.19']['lits']['en'])
        self.assertIn('जे पनि पाए', current['12.19']['lits']['ne'])
        self.assertIn('जो कुछ मिले', current['12.19']['lits']['hi'])


if __name__ == '__main__':
    unittest.main()
