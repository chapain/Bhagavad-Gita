#!/usr/bin/env python3
"""Reproduce bounded whole-book candidate screens for the 2026-11-22 review.

These are reading aids, not validators: exact row forms, English gloss wording,
polysemy and the last-pāda restriction all cause false negatives or positives.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def all_verses():
    result = []
    for n in range(1, 19):
        chapter = json.loads((ROOT / 'source' / f'ch{n}.json').read_text())
        result.extend(v for t in chapter['themes'] for p in t['parts'] for v in p['sutras'])
    assert len(result) == 700
    return result


def rows(v):
    return [r for f in v['flow'] for r in f['words']]


def main():
    verses = all_verses()
    tests = (
        ('Final pāda contains an English gloss starting "having "',
         lambda v: [r for f in [f for f in v['flow'] if f['k'] == 'p'][-1:]
                    for r in f['words'] if r[2].startswith('having ')]),
        ('Both सुख and भोग occur in row forms',
         lambda v: ([r for r in rows(v) if 'सुख' in r[0] or 'भोग' in r[0]]
                    if any('सुख' in r[0] for r in rows(v)) and
                       any('भोग' in r[0] for r in rows(v)) else [])),
        ('Row form starts नियत',
         lambda v: [r for r in rows(v) if r[0].startswith('नियत')]),
        ('Devanagari row gloss contains अयोग्य',
         lambda v: [r for r in rows(v) if 'अयोग्य' in r[3] or 'अयोग्य' in r[4]]),
        ('बहु-family rows whose English gloss is many / of many',
         lambda v: [r for r in rows(v) if r[0].startswith(('बहु', 'बहू', 'बहव'))
                    and r[2] in ('many', 'of many')]),
        ('संयमी and मुनि co-occur in row forms',
         lambda v: ([r for r in rows(v) if 'संयमी' in r[0] or 'मुनि' in r[0] or 'मुने' in r[0]]
                    if any('संयमी' in r[0] for r in rows(v)) and
                       any('मुनि' in r[0] or 'मुने' in r[0] for r in rows(v)) else [])),
        ('Exact द्वेष्टि row forms',
         lambda v: [r for r in rows(v) if r[0] == 'द्वेष्टि']),
        ('व्यवसाय-family row forms',
         lambda v: [r for r in rows(v) if 'व्यवसाय' in r[0]]),
        ('अव्यय and अविनाश co-occur in row forms',
         lambda v: ([r for r in rows(v) if 'अव्यय' in r[0] or 'अविनाश' in r[0]]
                    if any('अव्यय' in r[0] for r in rows(v)) and
                       any('अविनाश' in r[0] for r in rows(v)) else [])),
    )
    for label, find in tests:
        hits = [(v, find(v)) for v in verses]
        hits = [(v, rs) for v, rs in hits if rs]
        print(f'\n{label}: {len(hits)} verses')
        for v, rs in hits:
            print(f"{v['n']} | " + ' / '.join(' | '.join(r) for r in rs))
            for lang in ('en', 'ne', 'hi'):
                print(f"  {lang}: {v['lits'][lang]}")

    # Broad, noisy lead list for English introductory participles, including
    # false positives such as "King". It is not a dangling-modifier detector.
    pattern = re.compile(r'''(?:^|[;—])\s*[“"']?(?:having\s+)?([a-z]+ing)\b[^;.!?]{0,180},''', re.I)
    hits = [(v, m.group()) for v in verses for m in pattern.finditer(v['lits']['en'])]
    print(f'\nEnglish introductory -ing clauses: {len(hits)} candidate clauses')
    for v, _ in hits:
        print(f"{v['n']} | {v['lits']['en']}")


if __name__ == '__main__':
    main()
