from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_touching(H, T):
    return T == H or T in set(support.adjacent_8(H[0], H[1]))


def move_tail(H, T):
    # In same column
    if H[0] == T[0]:
        new_T = tuple([T[0], T[1] + 1])
        if is_touching(H, new_T):
            return new_T
        new_T = tuple([T[0], T[1] - 1])
        if is_touching(H, new_T):
            return new_T

    # In same row
    if H[1] == T[1]:
        new_T = tuple([T[0] + 1, T[1]])
        if is_touching(H, new_T):
            return new_T
        new_T = tuple([T[0] - 1, T[1]])
        if is_touching(H, new_T):
            return new_T

    # Neither
    new_T = tuple([T[0] + 1, T[1] + 1])
    if is_touching(H, new_T):
        return new_T
    new_T = tuple([T[0] - 1, T[1] + 1])
    if is_touching(H, new_T):
        return new_T
    new_T = tuple([T[0] + 1, T[1] - 1])
    if is_touching(H, new_T):
        return new_T
    new_T = tuple([T[0] - 1, T[1] - 1])
    if is_touching(H, new_T):
        return new_T


def eval_for_knots(number_of_knots: int, lines) -> int:
    T_FOOTPRINT = set()
    knots = [(0, 0) for _ in range(number_of_knots)]

    for line in lines:
        direction, steps = line.split()
        steps = int(steps)
        while steps:
            steps -= 1
            match direction:
                case 'U':
                    knots[0] = (knots[0][0], knots[0][1] + 1)
                case 'D':
                    knots[0] = (knots[0][0], knots[0][1] - 1)
                case 'R':
                    knots[0] = (knots[0][0] + 1, knots[0][1])
                case 'L':
                    knots[0] = (knots[0][0] - 1, knots[0][1])

            for i in range(1, number_of_knots):
                if not is_touching(knots[i - 1], knots[i]):
                    knots[i] = move_tail(knots[i - 1], knots[i])

            T_FOOTPRINT.add(knots[-1])

    return len(T_FOOTPRINT)


def compute(s: str) -> int:
    lines = s.splitlines()
    return eval_for_knots(2, lines)


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
