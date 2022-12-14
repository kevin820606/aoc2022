from src.utils import print_ans, read_aoc, AOCFILE
from collections import UserList

LeftIsSmaller = bool
def pair_compare(left:list|int, right:list|int) -> LeftIsSmaller:

    if type(left) == type(right) == int:
        return left < right

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    return list_compare(left, right)

def list_compare(left_objs:list, right_objs:list) -> LeftIsSmaller:

    for left, right in zip(left_objs, right_objs):
        if left == right:
            continue
        return pair_compare(left, right)
    if len(left_objs) != len(right_objs):
        return len(left_objs) < len(right_objs)
    return False

class Packet(UserList):
    def __init__(self, ls):
        super().__init__(ls)
    def __gt__(self, other: list | UserList) -> bool:
        return pair_compare(left=other, right=self)
    def __lt__(self, other: list | UserList) -> bool:
        return pair_compare(left=self, right=other)

def parse_compare_pairs(aoc_file:AOCFILE) -> list[tuple[Packet, Packet]]:
    raw_lists = []
    compair_pairs = []
    for line in aoc_file:
        if line:
            raw_lists.append(eval(line))
    while raw_lists:
        compair_pairs.append((Packet(raw_lists.pop(0)), Packet(raw_lists.pop(0))))
    return compair_pairs

def is_all_int(lft_list:list, right_list:list) -> bool:
    return all(map(lambda x: type(x) == int, lft_list + right_list))




def Q1():
    aoc_13 = read_aoc(13, use_test_data=False)
    pairs = parse_compare_pairs(aoc_file=aoc_13)
    ans = 0
    for n, (left, right) in enumerate(pairs, 1):
        print(f"pair {n}, {left=}, {right=}, {list_compare(left, right)=}")
        ans += n if list_compare(left, right) else 0
    print_ans(1, ans)

def Q2():
    sorted_list = [[[2]], [[6]]]
    aoc_13 = read_aoc(13, use_test_data=False)
    pairs = parse_compare_pairs(aoc_file=aoc_13)
    while pairs:
        sorted_list.extend(pairs.pop(0))
    sorted_list.sort()
    print((sorted_list.index([[2]]) + 1) * (sorted_list.index([[6]]) + 1))



if __name__ == "__main__":
    Q2()
