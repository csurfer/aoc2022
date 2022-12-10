from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    cycle_xval = {}
    cycle = 0
    xval = 1
    for line in lines:
        if line.startswith('addx'):
            _, v = line.split()
            val = int(v)
            cycle += 1
            cycle_xval[cycle] = xval
            cycle += 1
            cycle_xval[cycle] = xval
            xval += val
        else:
            cycle += 1
            cycle_xval[cycle] = xval

    cycle_pixel_map = {}
    for i in range(1, 41):
        cycle_pixel_map[i] = i - 1
    for i in range(41, 81):
        cycle_pixel_map[i] = i - 41
    for i in range(81, 121):
        cycle_pixel_map[i] = i - 81
    for i in range(121, 161):
        cycle_pixel_map[i] = i - 121
    for i in range(161, 201):
        cycle_pixel_map[i] = i - 161
    for i in range(201, 241):
        cycle_pixel_map[i] = i - 201

    pixels = []
    for key in sorted(cycle_xval.keys()):
        pixel = cycle_pixel_map[key]
        if pixel in {
            cycle_xval[key] - 1,
            cycle_xval[key],
            cycle_xval[key] + 1,
        }:
            pixels.append('#')
        else:
            pixels.append('.')

    for i in range(40, 280, 40):
        print(''.join(pixels[i-40:i]))

    return 0


INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = 13140


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
