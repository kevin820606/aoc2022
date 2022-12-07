from src.utils import read_aoc, print_ans, AOCFILE


aoc_6 = next(read_aoc(6)) # Only one line

def question(question_n:int, information_len:int) -> None:
    find_len = information_len - 1
    check_str:str = aoc_6[:find_len]
    for loc, char in enumerate(aoc_6[find_len:], information_len):
        if len(set(check_str + char)) < information_len:
            check_str = check_str[1:] + char
            continue
        print_ans(question_n, loc)
        break



if __name__ == "__main__":
    question(1, 4)
    question(2, 14)
