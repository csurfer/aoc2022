from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s = s.strip()

    sm = 0
    lines = s.splitlines()
    for line in lines:
        a, b = line[:len(line) // 2], line[len(line) // 2:]
        common = set(a).intersection(set(b))
        for ch in common:
            if 'a' <= ch <= 'z':
                sm += ord(ch) - ord('a') + 1
            else:
                sm += ord(ch) - ord('A') + 27
    # TODO: implement solution here!
    return sm


INPUT_S = '''\

'''
EXPECTED = 1


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
