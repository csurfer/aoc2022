from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s = s.strip()
    lines = s.splitlines()
    cnt = 0
    for line in lines:
        parts = line.split(',')
        r1s, r1e = list(map(int, parts[0].split('-')))
        r2s, r2e = list(map(int, parts[1].split('-')))
        if r1s <= r2s <= r2e <= r1e or r2s <= r1s <= r1e <= r2e:
            cnt += 1
    # TODO: implement solution here!
    return cnt


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
