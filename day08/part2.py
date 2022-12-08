from __future__ import annotations

import argparse
import os.path
from functools import reduce

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    grid: list[list[int]] = []
    lines = s.splitlines()
    for line in lines:
        grid.append(list(map(int, line)))

    R = len(grid)
    C = len(grid[0])
    mx = 1
    for r in range(1, R - 1):
        for c in range(1, C - 1):
            score: list[int] = []

            ir = r - 1
            while ir > 0 and grid[ir][c] < grid[r][c]:
                ir -= 1
            score.append(abs(r - ir))

            ir = r + 1
            while ir < R - 1 and grid[ir][c] < grid[r][c]:
                ir += 1
            score.append(abs(r - ir))

            ic = c - 1
            while ic > 0 and grid[r][ic] < grid[r][c]:
                ic -= 1
            score.append(abs(c - ic))

            ic = c + 1
            while ic < C - 1 and grid[r][ic] < grid[r][c]:
                ic += 1
            score.append(abs(c - ic))

            # print(r, c, score)
            mx = max([mx, reduce(lambda x, y: x*y, score)])

    return mx


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
