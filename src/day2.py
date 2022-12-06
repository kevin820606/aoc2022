from src.utils import read_aoc


outcome_score = {"win": 6, "lose": 0, "draw": 3}
def Q1():
    aoc_2 = read_aoc(2)
    shape_score = {"X": 1, "Y": 2, "Z": 3}  # Rock  # Paper  # Scissor
    score = 0
    for pair in aoc_2:
        elf, me = pair.split(" ")
        match (elf, me):
            case ("A", "X") | ("B", "Y") | ("C", "Z"):
                score += outcome_score["draw"] + shape_score[me]
            case ("C", "X") | ("A", "Y") | ("B", "Z"):
                score += outcome_score["win"] + shape_score[me]
            case ("B", "X") | ("C", "Y") | ("A", "Z"):
                score += outcome_score["lose"] + shape_score[me]
    print(f"Q1: total score is {score= }")

def Q2():
    aoc_2 = read_aoc(2)
    score = 0
    elf_score = {"A":1, "B":2, "C":3}
    indicator = {"X": "lose", "Y": "draw", "Z": "win"}
    for pair in aoc_2:
        elf, indicate = pair.split(" ")
        outcome = outcome_score[indicator[indicate]]
        print(indicate, outcome)
        match indicate:
            case "Z":
                shape_score = 1 if elf_score[elf] + 1 == 4 else elf_score[elf] + 1
            case "Y":
                shape_score = elf_score[elf]
            case "X":
                shape_score = 3 if elf_score[elf] - 1 == 0 else elf_score[elf] - 1
        score += shape_score + outcome

    print(f"Q2: total score is {score= }")


if __name__ == "__main__":
    Q1()
    Q2()
