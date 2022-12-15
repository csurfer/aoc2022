from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Sense:
    def __init__(self, sensor, beacon):
        self.sensor = sensor
        self.beacon = beacon
        self.safety_grid = self.md(
            self.sensor[0], self.sensor[1], self.beacon[0], self.beacon[1],
        )

    def md(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def impossible_in_row(self, y):
        width = self.safety_grid - abs(self.sensor[1] - y)
        if width < 0:
            return None
        if width == 0:
            return (self.sensor[0], self.sensor[0])
        return (self.sensor[0] - width, self.sensor[0] + width)


def compute(s: str) -> int:
    lines = s.splitlines()
    sensor_beacon = []
    minx, miny = 10 ** 9, 10 ** 9
    maxx, maxy = -10 ** 9, -10 ** 9
    for line in lines:
        sensor_str, beacon_str = line.split(':')
        sensor = tuple(map(int, sensor_str.split(',')))
        beacon = tuple(map(int, beacon_str.split(',')))

        minx = min([minx, sensor[0], beacon[0]])
        maxx = max([maxx, sensor[0], beacon[0]])
        miny = min([miny, sensor[1], beacon[1]])
        maxy = max([maxy, sensor[1], beacon[1]])

        sensor_beacon.append(Sense(sensor, beacon))

    y_required = 2_000_000

    max_width = [10 ** 9, -10 ** 9]
    for sense in sensor_beacon:
        width = sense.impossible_in_row(y_required)
        if width is not None:
            max_width[0] = min([max_width[0], width[0]])
            max_width[1] = max([max_width[1], width[1]])

    if max_width[1] - max_width[0] + 1 < 0:
        return 0

    overlapping_beacons = set()
    for sense in sensor_beacon:
        if (
            sense.beacon[1] == y_required
            and max_width[0] <= sense.beacon[0] <= max_width[1]
        ):
            overlapping_beacons.add(sense.beacon)

    return max_width[1] - max_width[0] + 1 - len(overlapping_beacons)


INPUT_S = '''\
2,18:-2,15
9,16:10,16
13,2:15,3
12,14:10,16
10,20:10,16
14,17:10,16
8,7:2,10
2,0:2,10
0,11:2,10
20,14:25,17
17,20:21,22
16,7:15,3
14,3:15,3
20,1:15,3
'''
EXPECTED = 26


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
