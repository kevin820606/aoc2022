from src.utils import read_aoc

def main() -> None:
    data = read_aoc(1)
    elves = []
    calories = 0
    for datum in data:
        if datum == "\n":
            elves.append(calories)
            calories = 0
        else:
            calories += int(datum)
    elves.sort(reverse=True)
    print(f"Q1: the most calories is {elves[0]}")
    print(f"Q2: Top three elves calories is {sum(elves[0:3])}")

if __name__ == "__main__":
    main()
