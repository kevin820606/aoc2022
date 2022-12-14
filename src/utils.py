#! /usr/bin/env python3
from typing import Generator, Any
from pprint import pprint as print


AOCFILE = Generator[str, None, None]

def read_aoc(day: int, strip:bool = True, use_test_data:bool = False) -> AOCFILE:
    suffix = "_test" if use_test_data else ""
    with open(f"data/data_{day}{suffix}.txt", mode = "r") as dayfile:
        for line in dayfile.readlines():
            if strip:
                yield line.strip()
            else:
                yield line

def print_ans(question_number:int, ans: Any) -> None:
    print(f"Q{question_number} ans is {ans}.")
