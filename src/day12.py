from src.utils import print_ans, read_aoc, AOCFILE
from typing import TypedDict, NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int


class Node(TypedDict, total=False):
    coord: Coordinate
    children: list[Coordinate]
    parents: set[Coordinate]
    height: int
    is_check: bool
    distance_from_start: int


def get_coords(
    aoc_file: AOCFILE,
) -> tuple[dict[Coordinate, Node], Coordinate, Coordinate]:
    all_coord: dict[Coordinate, Node] = dict()
    for y, line in enumerate(aoc_file):
        for x, word in enumerate(line):
            height = ord(word) - 96
            coord = Coordinate(x, y)
            if word == "S":
                height = 1
                start = coord
            if word == "E":
                height = 27
                end = coord
            all_coord |= {
                coord: Node(
                    coord=coord,
                    height=height,
                    children=[],
                    is_check=False
                )
            }
    return (all_coord, start, end)


class Map:
    def __init__(self, nodes: dict[Coordinate, Node]):
        self.nodes = nodes

    def get_four_directions(self, coord: Coordinate) -> list[Coordinate]:
        x, y = coord
        return [
            Coordinate(x=x + 1, y=y),
            Coordinate(x=x - 1, y=y),
            Coordinate(x=x, y=y + 1),
            Coordinate(x=x, y=y - 1)
        ]

    def get_node_chain(self) -> None:
        for node in self.nodes.keys():
            four_directions = self.get_four_directions(node)
            for dir in four_directions:
                if self.nodes.get(dir):
                    if self.nodes[dir]["height"] - self.nodes[node]["height"] in [0, 1]:
                        self.nodes[node]["children"].append(dir)
                        # self.nodes[dir]["parents"].add(node)

    def get_minimal_distance_from_start(self, start: Coordinate) -> None:
        self.nodes[start]["distance_from_start"] = 0
        check_list = [start]
        while check_list:
            coord = check_list.pop(0)
            children = self.nodes[coord]["children"]
            for child in children:
                if (not coord in self.nodes[child]["parents"]):
                    continue
                self.nodes[child]["parents"].remove(coord)
                if (
                    self.nodes[child]["distance_from_start"]
                    >= self.nodes[coord]["distance_from_start"] + 1
                ):
                    self.nodes[child]["distance_from_start"] = (
                        self.nodes[coord]["distance_from_start"] + 1
                    )
                check_list.append(child)

    def get_start_to_end(self, start:Coordinate, end:Coordinate) -> None:
        node = start
        children = self.nodes[node]["children"]
        layer = 1
        next_children:list[Coordinate] = []
        while children:
            child = children.pop(0)

            next_children.extend(self.nodes[child]["children"])

            if end in next_children:
                print(layer + 1)
                break

            if not children:
                layer += 1
                children = list(set(next_children))
                next_children = []
                if layer > 900:
                    print(children)
                print(layer)

def Q1():
    aoc_file = read_aoc(12)
    all_cord, start, end = get_coords(aoc_file=aoc_file)
    questionmap = Map(nodes=all_cord)
    questionmap.get_node_chain()
    questionmap.get_start_to_end(start=start, end=end)


if __name__ == "__main__":
    Q1()
