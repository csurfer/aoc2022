from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_visible(grid: list[list[int]], r: int, c: int, R: int, C: int) -> bool:
    if r == 0 or r == R - 1 or c == 0 or c == C - 1:
        return True

    return (
        all(grid[ir][c] < grid[r][c] for ir in range(0, r)) or
        all(grid[ir][c] < grid[r][c] for ir in range(r + 1, R)) or
        all(grid[r][ic] < grid[r][c] for ic in range(0, c)) or
        all(grid[r][ic] < grid[r][c] for ic in range(c + 1, C))
    )


def compute(s: str) -> int:
    grid: list[list[int]] = []
    lines = s.splitlines()
    for line in lines:
        grid.append(list(map(int, line)))

    R = len(grid)
    C = len(grid[0])
    cnt = 0
    for r in range(R):
        for c in range(C):
            if is_visible(grid, r, c, R, C):
                cnt += 1
    return cnt


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
