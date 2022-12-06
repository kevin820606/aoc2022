from src.utils import read_aoc, print_ans, AOCFILE
from typing import NamedTuple
import re


class Instruction(NamedTuple):
    move_times: int
    start_stack: int
    end_stack: int


STORAGE = dict[int, list]


def crate_parser(aoc: AOCFILE) -> STORAGE:
    raw_lines: list[str] = []
    for line in aoc:
        if re.search('\d', line):
            lines_index = map(int, re.findall('\d', line))
            storage: STORAGE = {num: list() for num in range(1, max(lines_index)+ 1)}
            break

        raw_lines.append(line.replace("\n", " "))
    stacks = raw_lines[::-1]
    for layer in stacks:
        each_line: list[str] = re.findall(pattern="(\[\D\]|\s{3})\s", string=layer)
        for lane_number, raw_item in enumerate(each_line, 1):
            if not raw_item.strip():
                continue
            storage[lane_number].append(raw_item)

    return storage


def action_parser(aoc: AOCFILE) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in aoc:
        if not line.strip():
            continue
        instructions.append(Instruction(*list(map(int, re.findall("\d+", line)))))
    return instructions

def get_last_cargo(crates: STORAGE) -> str:
    final_string:str = ""
    for last_item in crates.values():
        try:
            final_string += last_item.pop()
        except IndexError:
            final_string += ""
    final_string = re.sub("\[|\]", "", final_string)
    return final_string

aoc_5 = read_aoc(5, strip=False)
crates = crate_parser(aoc=aoc_5)
instructions = action_parser(aoc=aoc_5)

def Q1() -> None:
    aoc_5 = read_aoc(5, strip=False)
    crates = crate_parser(aoc=aoc_5)
    instructions = action_parser(aoc=aoc_5)
    for move, start, end in instructions:
        for _ in range(move):
            crates[end].append(crates[start].pop())
    final_string = get_last_cargo(crates=crates)
    print_ans(1, final_string)



def Q2() -> None:
    for move, start, end in instructions:
        crates[end] = crates[end] + crates[start][-move:]
        crates[start] = crates[start][:-move]

    final_string = get_last_cargo(crates=crates)
    print_ans(2, final_string)


if __name__ == "__main__":
    Q1()
    Q2()
