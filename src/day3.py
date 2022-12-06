from src.utils import read_aoc
from string import ascii_letters


char_int_map = {letter: number for letter, number in zip(ascii_letters, range(1, 53))}


def Q1():
    aoc_3 = read_aoc(3)
    priorities = 0
    for items in aoc_3:
        item_1, item_2 = set(items[:len(items)//2]), set(items[len(items)//2:])
        priorities += char_int_map[item_1.intersection(item_2).pop()]
    return priorities

def Q2():
    aoc_3 = read_aoc(3)
    priorities = 0
    while True:
        try:
            item_1 = set(next(aoc_3))
            item_2 = set(next(aoc_3))
            item_3 = set(next(aoc_3))
        except StopIteration:
            break
        priorities += char_int_map[set.intersection(item_1, item_2, item_3).pop()]
    print(f"Q2: {priorities= }")
if __name__ == "__main__":
    Q2()
