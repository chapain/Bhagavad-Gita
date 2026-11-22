#!/usr/bin/env python3
"""Find possible adjacent-verse vocabulary in Nepali/Hindi paraphrase tails.

A lead is not an error: read both verses and their context. This frequency and
spelling limited screen cannot detect paraphrases using different words, and
misses e.g. 6.22's former 'end of sorrow' boundary leak. --revision reads a
local git revision instead of canonical files in the working tree.
"""
import argparse
import collections
from audit_literal_boundaries import chapter, tokens


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', help='local git revision to inspect')
    args = parser.parse_args()
    verses = [v for c in range(1, 19) for t in chapter(c, args.revision)['themes']
              for p in t['parts'] for v in p['sutras']]
    assert len(verses) == 700
    pairs = [(a, b) for a, b in zip(verses, verses[1:])
             if a['n'].split('.')[0] == b['n'].split('.')[0]]
    assert len(pairs) == 682
    print('700 verses; 682 within-chapter adjacent pairs; 18 chapter endings')
    for index, lang in ((3, 'ne'), (4, 'hi')):
        frequency = collections.Counter()
        for verse in verses:
            frequency.update({word for f in verse['flow'] for row in f['words']
                              for word in tokens(row[index])})
        candidates = []
        for current, following in pairs:
            tail = ' '.join(tokens(current['paras'][lang])[-14:])
            own = {word for f in current['flow'] for row in f['words']
                   for word in tokens(row[index])}
            next_only = {word for f in following['flow'] for row in f['words']
                         for word in tokens(row[index])
                         if frequency[word] <= 12 and word not in own}
            hits = sorted(word for word in next_only if word in tail)
            if hits:
                candidates.append((current, following, hits))
        print(f'\n{lang}: {len(candidates)} candidates')
        for current, following, hits in candidates:
            print(f"{current['n']} -> {following['n']} | {', '.join(hits)}")
            print(f"  paraphrase: {current['paras'][lang]}")
            print(f"  next Sanskrit: {following['d']}")


if __name__ == '__main__':
    main()
