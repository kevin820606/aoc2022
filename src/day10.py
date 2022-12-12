from src.utils import print_ans, read_aoc, AOCFILE
from enum import StrEnum, auto

class CPUInstruct(StrEnum):
    NOOP = auto()
    ADDX = auto()

Instruction = tuple[CPUInstruct, int]

def get_instruct(aoc_file: AOCFILE) -> list[Instruction]:
    instr_list = []
    for line in aoc_file:
        instruct = line.split(" ")
        match instruct[0]:
            case CPUInstruct.NOOP:
                instr_list.append((CPUInstruct.NOOP, 0))
            case CPUInstruct.ADDX:
                instr_list.append((CPUInstruct.ADDX, int(instruct[1])))
    return instr_list

def compile_instruction(instructions: list[Instruction]) -> list[int]:
    cpu_num = 1
    command_process = [0] # start from initial position 0
    for instruct, add_num in instructions:
        match instruct:
            case CPUInstruct.NOOP:
                command_process.append(cpu_num)
            case CPUInstruct.ADDX:
                command_process.append(cpu_num)
                cpu_num += add_num
                command_process.append(cpu_num)
    return command_process

def Q1():
    instructions = get_instruct(read_aoc(10))
    compile_instruct = compile_instruction(instructions=instructions)
    request_cycle_number = [20, 60, 100, 140, 180, 220]
    [print(f"cycle = {n}, number = {cycle}") for n, cycle in enumerate(compile_instruct)]
    print(1, sum([cycle * compile_instruct[cycle - 1] for cycle in request_cycle_number]))


def Q2():
    instructions = get_instruct(read_aoc(10))
    init = 0
    crt = ""
    cycle = 0
    sprite = "." * 40
    compare_sprite = sprite[0:init] + "###" + sprite[init+3:]
    for instruct, number in instructions:
        match instruct:
            case CPUInstruct.ADDX:
                index = cycle % 40
                crt += "#" if compare_sprite[index] == "#" else "."
                cycle += 1
                index = cycle % 40
                crt += "#" if compare_sprite[index] == "#" else "."
                cycle += 1
                init += number
                compare_sprite = sprite[0:init] + "###" + sprite[init+3:]
            case CPUInstruct.NOOP:
                index = cycle % 40
                crt += "#" if compare_sprite[index] == "#" else "."
                cycle += 1
    for i in range(0, 240, 40):
        print(f"{crt[i:i+39]}")

if __name__ == "__main__":
    # Q1()
    Q2()
