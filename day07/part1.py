from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    parent_dir: dict[str, str | None] = {'/': None}
    cur_dir = ['/']
    file_size: dict[str, int] = defaultdict(lambda: 0)

    lines = s.splitlines()
    while lines:
        line = lines.pop(0)
        if line.startswith('$'):
            command = line[2:]
            if command.startswith('cd'):
                # cd
                go_into = command[3:]
                if go_into == '/':
                    cur_dir = ['/']
                if go_into == '..':
                    cur_dir.pop(-1)
                else:
                    cur_dir.append(go_into)
            else:
                # ls
                while lines and not lines[0].startswith('$'):
                    line = lines.pop(0)
                    if line.startswith('dir'):
                        _, name = line.split()
                        full_name = os.path.join(*cur_dir, name)
                        parent_dir[full_name] = os.path.join(*cur_dir)
                    else:
                        sz, name = line.split()
                        full_name = os.path.join(*cur_dir, name)
                        parent_dir[full_name] = os.path.join(*cur_dir)
                        file_size[full_name] = int(sz)

    dir_size: dict[str, int] = defaultdict(lambda: 0)

    for name, file_sz in file_size.items():
        parent = parent_dir[name]
        while parent is not None:
            dir_size[parent] += file_sz
            parent = parent_dir[parent]

    compute = sorted([(v, k) for k, v in dir_size.items()])
    d_sz = 0
    for v, _ in compute:
        if v <= 100000:
            d_sz += v

    return d_sz


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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
