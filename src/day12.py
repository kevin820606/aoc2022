from src.utils import print_ans, read_aoc, AOCFILE
from typing import TypedDict, NamedTuple

class Coordinate(NamedTuple):
    x: int
    y: int


class Node(TypedDict, total=False):
    name:str
    coord: Coordinate
    children: list[Coordinate]
    parents: set[Coordinate]
    height: int
    is_check: bool
    distance_from_start: int


def get_coords(
    aoc_file: AOCFILE, start_sign:list[str]
) -> tuple[dict[Coordinate, Node], list[Coordinate], Coordinate]:
    starts = []
    all_coord: dict[Coordinate, Node] = dict()

    for y, line in enumerate(aoc_file):
        for x, word in enumerate(line):
            height = ord(word) - 96
            coord = Coordinate(x, y)
            if word in start_sign:
                height = 1
                starts.append(coord)
            if word == "E":
                height = 27
                end = coord
            all_coord |= {
                coord: Node(
                    name = word,
                    coord=coord,
                    height=height,
                    children=[],
                    is_check=False,
                    parents=set(),
                    distance_from_start=1000000
                )
            }
    return (all_coord, starts, end)


class Map:
    def __init__(self, nodes: dict[Coordinate, Node], end):
        self.end = end
        self.nodes = nodes

    def get_four_directions(self, coord: Coordinate) -> list[Coordinate]:
        x, y = coord
        return [
            Coordinate(x=x + 1, y=y),
            Coordinate(x=x, y=y + 1),
            Coordinate(x=x - 1, y=y),
            Coordinate(x=x, y=y - 1),
        ]

    def get_node_chain(self) -> None:
        for node in self.nodes.keys():
            four_directions = self.get_four_directions(node)
            for dir in four_directions:
                if self.nodes.get(dir):
                    if self.nodes[dir]["height"] - self.nodes[node]["height"] < 2:
                        self.nodes[node]["children"].append(dir)

    def get_start_to_end(self, start:Coordinate) -> None:
        node = start
        children = self.nodes[node]["children"]
        layer = 1
        next_layer_nodes:list[Coordinate] = []
        self.checked_list = []

        while children:
            node = children.pop(0)
            self.checked_list.append(node)

            for child in self.nodes[node]["children"]:
                if child not in self.checked_list:
                    next_layer_nodes.append(child)

            if self.end in next_layer_nodes:
                self.min = layer
                break

            if not children:
                layer += 1
                children = list(set(next_layer_nodes))
                next_layer_nodes = []

def Q1():
    aoc_file = read_aoc(12)
    all_cord, starts, end = get_coords(aoc_file=aoc_file, start_sign=["S"])
    questionmap = Map(nodes=all_cord, end = end)
    questionmap.get_node_chain()
    for start in starts:
        print(start)
        questionmap.get_start_to_end(start=start)
        print_ans(1, questionmap.min)

def Q2():
    aoc_file = read_aoc(12)
    all_coord, starts, end = get_coords(aoc_file=aoc_file, start_sign=["S", "a"])
    questionmap = Map(nodes=all_coord, end = end)
    min = 1000000
    check_list = []
    questionmap.get_node_chain()
    while starts:
        start = starts.pop(0)
        if not check_list:
            questionmap.get_start_to_end(start=start)
            check_list.extend(questionmap.checked_list)
        if not start in check_list:
            continue
        if questionmap.min < min:
            min = questionmap.min
    print_ans(2, min)

if __name__ == "__main__":
    Q1()
    Q2()
