from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    grid = []
    for line in lines:
        grid.append(list(line.strip()))

    R = len(grid)
    C = len(grid[0])

    ELOC = None
    bfs = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S' or grid[r][c] == 'a':
                grid[r][c] = 'a'
                bfs.append(((r, c), 0))
            elif grid[r][c] == 'E':
                ELOC = (r, c)
                grid[r][c] = 'z'

    min_count = 10 ** 9
    visited: dict[Any, Any] = defaultdict(lambda: False)
    while bfs:
        position, steps = bfs.pop(0)
        if visited[position] is True:
            continue

        if position != ELOC:
            visited[position] = True
        else:
            min_count = min([min_count, steps])
            continue

        assert position is not None

        a, b = position
        for x, y in support.adjacent_4(a, b):
            if (
                0 <= x < R and
                0 <= y < C and
                ord(grid[x][y]) - ord(grid[a][b]) <= 1
                and grid[x][y] != 'a'
            ):
                bfs.append(((x, y), steps + 1))

    return min_count


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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
