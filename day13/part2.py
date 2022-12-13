from __future__ import annotations

import argparse
import os.path
from random import randint

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compare_ints(left, right):
    if left < right:
        return True
    elif left > right:
        return False
    else:
        # No decision
        return None


def compare_lists(left, right):
    idx = 0
    while True:
        if idx >= len(left) and idx >= len(right):
            # Both ran out of items.
            # No decision
            return None
        elif idx >= len(left) and idx < len(right):
            # Left ran out first
            return True
        elif idx < len(left) and idx >= len(right):
            # Right ran out first
            return False
        else:
            # Neither ran out yet.
            ret_val = compare(left[idx], right[idx])
            if ret_val is not None:
                return ret_val
        idx += 1


def compare(left, right):
    if type(left) == int and type(right) == int:
        ret_val = compare_ints(left, right)
        if ret_val is not None:
            return ret_val
    elif type(left) == list and type(right) == list:
        ret_val = compare_lists(left, right)
        if ret_val is not None:
            return ret_val
    elif type(left) == int and type(right) == list:
        ret_val = compare_lists(list([left]), right)
        if ret_val is not None:
            return ret_val
    elif type(left) == list and type(right) == int:
        ret_val = compare_lists(left, list([right]))
        if ret_val is not None:
            return ret_val

    return None


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = randint(0, len(arr) - 1)
    true_list = []
    false_list = []
    for i in range(len(arr)):
        if i == pivot:
            continue
        if compare(arr[i], arr[pivot]):
            true_list.append(arr[i])
        else:
            false_list.append(arr[i])

    return merge_sort(true_list) + [arr[pivot]] + merge_sort(false_list)


def compute(s: str) -> int:
    lines = s.splitlines()
    DIV_PACKET_1 = [[2]]
    DIV_PACKET_2 = [[6]]
    non_empty_lines = [DIV_PACKET_1, DIV_PACKET_2]
    for line in lines:
        if line != '':
            non_empty_lines.append(eval(line))

    sorted_array = merge_sort(non_empty_lines)

    mul = 1
    for i, item in enumerate(sorted_array):
        if item == DIV_PACKET_1 or item == DIV_PACKET_2:
            mul *= i + 1
    return mul


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


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
