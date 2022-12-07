from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s = s.strip()

    window = list(s[:4])
    if len(set(window)) == 4:
        return 4

    for i, ch in enumerate(s[4:], start=5):
        window.pop(0)
        window.append(ch)
        if len(set(window)) == 4:
            return i

    return 0


INPUT_S = '''\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''
EXPECTED = 7


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
