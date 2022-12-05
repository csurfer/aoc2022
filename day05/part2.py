from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    stacks: list[list[str]] = [
        list('---NONSENSE---PLACEHOLDER---'),
        list('TDWZVP'),
        list('LSWVFJD'),
        list('ZMLSVTBH'),
        list('RSJ'),
        list('CZBGFMLW'),
        list('QWVHZRGB'),
        list('VJPCBDN'),
        list('PTBQ'),
        list('HGZRC'),
    ]
    lines = s.splitlines()
    # print(stacks)
    for line in lines:
        cnt, src, dst = (int(item) for item in line.split(','))
        items = []
        for _ in range(cnt):
            items.append(stacks[src].pop(-1))
        stacks[dst].extend(reversed(items))
        # print(cnt, src, dst, stacks)
    # TODO: implement solution here!
    return ''.join(stacks[i][-1] for i in range(1, 10))


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
