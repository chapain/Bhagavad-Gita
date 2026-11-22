#!/usr/bin/env python3
"""Candidate screen for next-verse word-row vocabulary in ne/hi literal tails.

Not a semantic proof: matches depend on exact gloss spelling, splitting, and
frequency. Examine each candidate against both Sanskrit verses. --revision
uses the canonical JSON at a local git revision for a reproducible before scan.
"""
import argparse
import collections
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def tokens(text):
    return [word for word in re.split(r'[^\u0900-\u097f]+', text) if len(word) >= 4]


def chapter(number, revision):
    path = f'source/ch{number}.json'
    if revision:
        text = subprocess.check_output(
            ['git', 'show', f'{revision}:{path}'], cwd=ROOT, text=True)
    else:
        text = (ROOT / path).read_text()
    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', help='local git revision, rather than working tree')
    args = parser.parse_args()
    verses = []
    for number in range(1, 19):
        data = chapter(number, args.revision)
        verses.extend(v for t in data['themes'] for p in t['parts'] for v in p['sutras'])
    assert len(verses) == 700
    pairs = [(a, b) for a, b in zip(verses, verses[1:])
             if a['n'].split('.')[0] == b['n'].split('.')[0]]
    assert len(pairs) == 682
    print('700 verses; 682 within-chapter adjacent pairs; 18 chapter endings')
    for index, lang in ((3, 'ne'), (4, 'hi')):
        frequency = collections.Counter()
        for verse in verses:
            frequency.update({w for f in verse['flow'] for r in f['words']
                              for w in tokens(r[index])})
        candidates = []
        for current, following in pairs:
            tail = ' '.join(tokens(current['lits'][lang])[-14:])
            own = {w for f in current['flow'] for r in f['words'] for w in tokens(r[index])}
            next_only = {w for f in following['flow'] for r in f['words']
                         for w in tokens(r[index]) if frequency[w] <= 12 and w not in own}
            hits = sorted(w for w in next_only if w in tail)
            if hits:
                candidates.append((current, following, hits))
        print(f'\n{lang}: {len(candidates)} candidates')
        for current, following, hits in candidates:
            print(f"{current['n']} -> {following['n']} | {', '.join(hits)}")
            print(f"  literal: {current['lits'][lang]}")
            print(f"  next Sanskrit: {following['d']}")


if __name__ == '__main__':
    main()
