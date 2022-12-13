from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Monkey:
    def __init__(
        self,
        start_items,
        operation,
        condition,
        true_monkey,
        false_monkey,
    ):
        self.start_items = start_items
        self.operation = operation
        self.condition = condition
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

        self.counter = 0

    def increment(self, val):
        self.counter += val


monkeys = {
    0: Monkey(
        start_items=[52, 60, 85, 69, 75, 75],
        operation=lambda old: old * 17,
        condition=lambda val: val % 13 == 0,
        true_monkey=6,
        false_monkey=7,
    ),
    1: Monkey(
        start_items=[96, 82, 61, 99, 82, 84, 85],
        operation=lambda old: old + 8,
        condition=lambda val: val % 7 == 0,
        true_monkey=0,
        false_monkey=7,
    ),
    2: Monkey(
        start_items=[95, 79],
        operation=lambda old: old + 6,
        condition=lambda val: val % 19 == 0,
        true_monkey=5,
        false_monkey=3,
    ),
    3: Monkey(
        start_items=[88, 50, 82, 65, 77],
        operation=lambda old: old * 19,
        condition=lambda val: val % 2 == 0,
        true_monkey=4,
        false_monkey=1,
    ),
    4: Monkey(
        start_items=[66, 90, 59, 90, 87, 63, 53, 88],
        operation=lambda old: old + 7,
        condition=lambda val: val % 5 == 0,
        true_monkey=1,
        false_monkey=0,
    ),
    5: Monkey(
        start_items=[92, 75, 62],
        operation=lambda old: old * old,
        condition=lambda val: val % 3 == 0,
        true_monkey=3,
        false_monkey=4,
    ),
    6: Monkey(
        start_items=[94, 86, 76, 67],
        operation=lambda old: old + 1,
        condition=lambda val: val % 11 == 0,
        true_monkey=5,
        false_monkey=2,
    ),
    7: Monkey(
        start_items=[57],
        operation=lambda old: old + 2,
        condition=lambda val: val % 17 == 0,
        true_monkey=6,
        false_monkey=2,
    ),
}


def compute(s: str) -> int:
    _ = s.strip()

    for round in range(10_000):
        for key in range(8):
            my_monkey = monkeys[key]
            # Inspect + relief
            # LCM of conditions should be acceptable by all hence removable.
            my_monkey.start_items = [
                my_monkey.operation(
                    item,
                ) % 9699690 for item in my_monkey.start_items
            ]
            my_monkey.increment(len(my_monkey.start_items))
            # Test and throw
            while my_monkey.start_items:
                item = my_monkey.start_items.pop(0)
                if my_monkey.condition(item):
                    monkeys[my_monkey.true_monkey].start_items.append(item)
                else:
                    monkeys[my_monkey.false_monkey].start_items.append(item)

    counts = sorted([monkeys[key].counter for key in range(8)], reverse=True)
    return counts[0] * counts[1]


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
