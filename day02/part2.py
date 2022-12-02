from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s = s.strip()

    p1 = {'A': 1, 'B': 2, 'C': 3}

    lines = s.splitlines()
    score = 0
    for line in lines:
        m, n = line.split()
        mint = p1[m]
        if n == 'X':
            # Lose
            if mint == 1:
                nint = 3
            elif mint == 2:
                nint = 1
            else:
                nint = 2
            score += (nint + 0)
        elif n == 'Y':
            # Draw
            score += (mint + 3)
        else:
            # Win
            if mint == 1:
                nint = 2
            elif mint == 2:
                nint = 3
            else:
                nint = 1
            score += (nint + 6)

    # TODO: implement solution here!

    return score


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
