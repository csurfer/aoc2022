from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move(r, c, grid, R, C):
    # Down
    if r + 1 < R and grid[r + 1][c] == '.':
        return r + 1, c
    # Diagonal Left
    if r + 1 < R and c - 1 >= 0 and grid[r + 1][c - 1] == '.':
        return r + 1, c - 1
    # Diagonal Right
    if r + 1 < R and c + 1 < C and grid[r + 1][c + 1] == '.':
        return r + 1, c + 1

    # Stop clause
    if r + 1 < R and c - 1 >= 0 and c + 1 < C:
        return r, c

    # Abyss
    return R, C


def compute(s: str) -> int:
    lines = s.splitlines()
    formations = []
    C, R = 0, 0
    for line in lines:
        coords = line.split(' -> ')
        rock_formation = []
        for coord in coords:
            a, b = coord.split(',')
            x, y = int(a), int(b)
            C = max([x, C])
            R = max([y, R])
            rock_formation.append((x, y))
        formations.append(rock_formation)

    C += 200
    R += 3
    grid = [['.' for c in range(C)] for r in range(R)]

    for rocks in formations:
        stc, str = rocks[0]
        grid[str][stc] = '#'
        for enc, enr in rocks[1:]:
            while str != enr or stc != enc:
                grid[str][stc] = '#'
                if str > enr:
                    str -= 1
                elif str < enr:
                    str += 1
                if stc > enc:
                    stc -= 1
                elif stc < enc:
                    stc += 1
            grid[enr][enc] = '#'
            stc, str = enc, enr

    # Sand drop
    sand_count = 0
    while True:
        # New sand unit
        r, c = 0, 500
        while True:
            newr, newc = move(r, c, grid, R, C)
            if (newr, newc) == (R, C):
                # Abyss
                return sand_count
            elif (newr, newc) != (r, c):
                # Flowing
                r, c = newr, newc
            elif (newr, newc) == (r, c):
                grid[r][c] = 'O'
                sand_count += 1
                break


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 24


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
