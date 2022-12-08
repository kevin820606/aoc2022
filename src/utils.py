#! /usr/bin/env python3
from typing import Generator, Any
from pprint import pprint as print


AOCFILE = Generator[str, None, None]

def read_aoc(day: int, strip:bool = True) -> AOCFILE:
    with open(f"data/data_{day}.txt", mode = "r") as dayfile:
        for line in dayfile.readlines():
            if strip:
                yield line.strip()
            else:
                yield line

def print_ans(question_number:int, ans: Any) -> None:
    print(f"Q{question_number} ans is {ans}.")
