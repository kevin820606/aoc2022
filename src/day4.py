from src.utils import read_aoc, print_ans

def parse_charge_line(charge_line: str) -> set[int]:
    start, end = map(int, charge_line.split('-'))
    return set(range(start, end+1))

def Q1() -> None:
    aoc_4 = read_aoc(4)
    overlaps_groups = 0
    for elves in aoc_4:
        elf_1, elf_2 = map(parse_charge_line, elves.split(','))
        overlaps_groups += elf_1 <= elf_2 or elf_1 >= elf_2
    print_ans(1, overlaps_groups)

def Q2() -> None:
    aoc_4 = read_aoc(4)
    joint_groups = 0
    for elves in aoc_4:
        elf_1, elf_2 = map(parse_charge_line, elves.split(','))
        joint_groups += not elf_1.isdisjoint(elf_2)
    print_ans(2, joint_groups)

if __name__ == "__main__":
    Q1()
    Q2()
