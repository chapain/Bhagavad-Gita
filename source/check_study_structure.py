#!/usr/bin/env python3
"""Lock the reviewed story maps and their one-verse, trilingual pearls.

Six verses is an editorial guideline, not a mechanical chopping rule. Longer
passages need an explicit reason below; a new exception must be reviewed.
This checker only reads source and built data, and never repairs either.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = ROOT / 'source' / 'study_map_contract.json'
CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
APPROVED_MAPS = {int(ch): ranges for ch, ranges in CONTRACT['approved_maps'].items()}
LONG_THEME_EXCEPTIONS = {rng: (entry['verses'], entry['reason'])
                         for rng, entry in CONTRACT['long_theme_exceptions'].items()}
REVIEWED_TOTAL = sum(len(ranges) for ranges in APPROVED_MAPS.values())


def literal_assignment(path, name):
    for node in ast.parse(Path(path).read_text(encoding='utf-8')).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f'{path}: missing {name}')


def load_book(root=ROOT):
    root = Path(root)
    metadata = literal_assignment(root / 'source/gita_data.py', 'CHAPTERS')
    english, localized, built = {}, {}, {}
    for ch in range(1, 19):
        suffix = '' if ch == 1 else str(ch)
        english[ch] = literal_assignment(root / 'source' / f'gita_data{suffix}.py', f'CH{ch}_THEMES')
        raw = (root / 'data' / f'ch{ch}.js').read_text(encoding='utf-8')
        built[ch] = json.loads(raw[raw.index('=') + 1:].rstrip().rstrip(';'))
    for lang in ('ne', 'hi'):
        localized[lang] = literal_assignment(root / 'source' / f'themes_{lang}.py', f'THEMES_{lang.upper()}')
    return metadata, english, localized, built


def audit(metadata, english, localized, built):
    errors, checks = [], 0
    titles, long_ranges = {}, set()

    def ok(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(label)

    ok(len(metadata) == 18 and [row[0] for row in metadata] == list(range(1, 19)),
       'chapter metadata must cover chapters 1–18 in order')
    ok(set(APPROVED_MAPS) == set(range(1, 19)), 'all 18 chapters require a reviewed map')
    ok(sum(len(ts) for ts in english.values()) == REVIEWED_TOTAL,
       f'the reviewed book has {REVIEWED_TOTAL} themes')
    for row in metadata:
        ch, count = row[0], row[3]
        themes = english[ch]
        payload = built[ch]
        ok(len(payload['themes']) == len(themes), f'chapter {ch}: built theme count differs from source')
        seen = [part[2] for _, _, parts in themes for part in parts]
        expected = [f'{ch}.{n:02d}' for n in range(1, count + 1)]
        ok(seen == expected, f'chapter {ch}: verse map has a gap, duplicate, or reordered verse')
        ranges = [f'{parts[0][2]}–{parts[-1][3]}' for _, _, parts in themes if parts]
        if ch in APPROVED_MAPS:
            ok(ranges == APPROVED_MAPS[ch], f'chapter {ch}: the reviewed story map changed')
        if ch == 2:
            ok(all(len(parts) <= 5 for _, _, parts in themes), 'chapter 2: each theme holds at most five verses')
        for lang in ('ne', 'hi'):
            ok(len(localized[lang].get(ch, [])) == len(themes), f'chapter {ch}: {lang} theme count differs')
        for ti, (title, desc, parts) in enumerate(themes):
            label = f'chapter {ch} theme {ti + 1}'
            ok(bool(parts), f'{label}: empty theme')
            if not parts:
                continue
            rng = f'{parts[0][2]}–{parts[-1][3]}'
            if len(parts) > 6:
                long_ranges.add(rng)
                exception = LONG_THEME_EXCEPTIONS.get(rng)
                ok(exception is not None and len(parts) == exception[0],
                   f'{rng}: more than six verses requires a reviewed exception')
            entries = {'en': (title, desc, parts)}
            for lang in ('ne', 'hi'):
                translations = localized[lang].get(ch, [])
                if ti < len(translations):
                    entries[lang] = translations[ti]
            generated = payload['themes'][ti] if ti < len(payload['themes']) else None
            for lang, (tt, td, ps) in entries.items():
                ok(bool(tt.strip()) and bool(td.strip()), f'{label}: missing {lang} title or description')
                ok([p[2:] for p in ps] == [p[2:] for p in parts], f'{label}: {lang} verse ranges are misaligned')
                if generated is not None:
                    ok(generated['titles'].get(lang) == tt and generated['descs'].get(lang) == td,
                       f'{label}: built {lang} teaching copy differs from source')
            if generated is not None:
                ok(generated['range'] == rng and len(generated['parts']) == len(parts),
                   f'{label}: built range or verse count differs from source')
            for pi, (pt, pd, start, end) in enumerate(parts):
                ok(start == end, f'{start}: a pearl must be exactly one verse')
                ok(bool(pt.strip()) and bool(pd.strip()), f'{start}: missing English title or description')
                ok(len(pt) <= 54, f'{start}: English verse title is too long for a card')
                ok(pt not in titles, f'{start}: duplicate English verse title with {titles.get(pt)}')
                titles[pt] = start
                generated_part = (generated['parts'][pi]
                                  if generated is not None and pi < len(generated['parts']) else None)
                if generated_part is not None:
                    ok([v['n'] for v in generated_part['sutras']] == [start]
                       and generated_part['range'] == f'{start}–{end}',
                       f'{start}: built verse ID or individual range changed')
                for lang, (_, _, ps) in entries.items():
                    if pi >= len(ps):
                        continue
                    lp = ps[pi]
                    ok(bool(lp[0].strip()) and bool(lp[1].strip()), f'{start}: missing {lang} verse copy')
                    if generated_part is not None:
                        ok(generated_part['titles'].get(lang) == lp[0]
                           and generated_part['descs'].get(lang) == lp[1],
                           f'{start}: built {lang} verse copy differs from source')
    ok(long_ranges == set(LONG_THEME_EXCEPTIONS), 'the reviewed longer passages changed')
    ok(len(titles) == 700, 'all 700 pearls must have distinct English titles')
    return errors, checks


def main():
    try:
        errors, checks = audit(*load_book())
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(f'study structure: FAILED — {exc}')
        return 1
    if errors:
        for error in errors:
            print('  ✗', error)
        print(f'study structure: {checks} checks, {len(errors)} failed')
        return 1
    print(f'study structure: {checks} checks passed — {REVIEWED_TOTAL} story themes, 700 pearls, three languages')
    if '--explain' in __import__('sys').argv:
        for rng, (count, reason) in LONG_THEME_EXCEPTIONS.items():
            print(f'  {rng} ({count} verses): {reason}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
