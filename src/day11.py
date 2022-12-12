from src.utils import print_ans, read_aoc, AOCFILE
from dataclasses import dataclass
from typing import Callable
from functools import reduce

SendingItems = list[tuple[str, int]]


def operation_parser(operation_str:str) -> Callable[[int], int]:
    new = operation_str.split("=")[1].strip()
    if new == "old * old":
        def new_func(old:int) -> int:
            return old * old
        return new_func
    new = new.replace("old ", "")
    operator, number  = new.split(" ")
    match operator:
        case "+":
            def new_func(old:int) -> int:
                return old + int(number)
        case "*":
            def new_func(old:int) -> int:
                return old * int(number)

    return new_func

@dataclass
class Monkey:
    name: str
    hold_items: list
    operation: Callable[[int], int]
    test_number:int
    test_true: str
    test_false:str
    inspected_times:int

    def __repr__(self) -> str:
        return f"Monkey {self.name} has {self.hold_items}"

    def recieve_item(self, item:int) -> None:
        self.hold_items.append(item)

    def is_divisible(self, item:int) -> bool:
        return item % self.test_number == 0

    def send_item_target(self, worry_level:int) -> str:
        if self.is_divisible(worry_level):
            return self.test_true
        return self.test_false

    def inspect_item(self, worry_devider:int) -> SendingItems:
        give_out_item:SendingItems = []
        while self.hold_items:
            inspecting = self.hold_items.pop(0)
            worry_level = self.operation(inspecting)
            reduce_number = worry_level // worry_devider if worry_devider == 3 else worry_level % worry_devider
            send_target = self.send_item_target(worry_level=reduce_number)
            give_out_item.append((send_target, reduce_number))
            self.inspected_times += 1
        return give_out_item

Monkeys = dict[str, Monkey]



def get_monkeys(aoc_file:AOCFILE) -> Monkeys:
    monkeys:Monkeys = dict()
    monkey_name = ""
    for line in aoc_file:
        data = line.split(":")
        if "Monkey" in data[0]:
            _, monkey_name = data[0].split(" ")
        if "items" in data[0]:
            start_item = list(map(int, data[1].strip().split(", ")))
        if "Operation" in data[0]:
            operation = operation_parser(data[1].strip())
        if "Test" in data[0]:
            test_number = int(data[1].replace(" divisible by ", ""))
        if "true" in data[0]:
            test_true = data[1].replace(" throw to monkey ","")
        if "false" in data[0]:
            test_false = data[1].replace(" throw to monkey ","")
            monkeys |= {monkey_name:Monkey(name=monkey_name, hold_items=start_item,operation=operation,test_number=test_number, test_true=test_true, test_false=test_false, inspected_times=0)}
    return monkeys


class MonkeyFactory:
    def __init__(self, monkeys:Monkeys, worry_divider:int) -> None:
        # https://github.com/kresimir-lukin/AdventOfCode2022/blob/main/day11.py
        # reduce whole number under least commmon multiple
        self.worry_divider = reduce(lambda x, y: x * y,[m.test_number for m in monkeys.values()], 1)
        if worry_divider == 3:
            self.worry_divider = worry_divider
        self.monkeys = monkeys

    def monkey_work(self) -> None:
        send_away_items:SendingItems = []
        for monkey in self.monkeys.values():
            send_away_items = monkey.inspect_item(worry_devider=self.worry_divider)
            for target, item in send_away_items:
                self.monkeys[target].recieve_item(item=item)

    def go_round(self, round_times:int) -> None:
        for _ in range(round_times):
            self.monkey_work()


def Q1():
    aoc_11 = read_aoc(11)
    work_monkeys = get_monkeys(aoc_file=aoc_11)
    monkey_factory = MonkeyFactory(monkeys=work_monkeys, worry_divider=3)
    monkey_factory.go_round(20)
    monkey_business = [m.inspected_times for m in monkey_factory.monkeys.values()]
    monkey_business.sort()
    print_ans(1, monkey_business[-1] * monkey_business[-2])

def Q2():
    aoc_11 = read_aoc(11)
    work_monkeys = get_monkeys(aoc_file=aoc_11)
    monkey_factory = MonkeyFactory(monkeys=work_monkeys, worry_divider=0)
    monkey_factory.go_round(10000)
    monkey_business = [m.inspected_times for m in monkey_factory.monkeys.values()]
    monkey_business.sort()
    # print(monkey_business)
    print_ans(2, monkey_business[-1] * monkey_business[-2])


if __name__ == "__main__":
    Q1()
    Q2()
