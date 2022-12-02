from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s = s.strip()

    p1 = {'A': 1, 'B': 2, 'C': 3}
    p2 = {'X': 1, 'Y': 2, 'Z': 3}

    lines = s.splitlines()
    score = 0
    for line in lines:
        m, n = line.split()
        mint = p1[m]
        nint = p2[n]
        if nint == mint:
            # Draw
            score += (nint + 3)
        elif (mint, nint) in {(1, 2), (2, 3), (3, 1)}:
            # Win
            score += (nint + 6)
        else:
            score += nint
    # TODO: implement solution here!

    return score


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
