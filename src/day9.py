from src.utils import print_ans, read_aoc, AOCFILE
from typing import NamedTuple
from enum import Enum
from dataclasses import dataclass, field

class Coordinate(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)


MoveInstruction = tuple[Direction, int]
MoveInstructions = list[MoveInstruction]


@dataclass
class Node:

    former_node: str
    position: Coordinate = Coordinate(0, 0)
    _path_history: list[Coordinate] = field(default_factory=list)

    def move(
        self,
        next_direction: Direction | None = None,
        next_position: Coordinate | None = None,
    ) -> None:

        if next_direction is None and next_position is None:
            raise NotImplementedError

        self._path_history.append(self.position)

        if next_position:
            self.position = next_position
            return

        now_x, now_y = self.position
        if next_direction is not None:
            self.position = Coordinate(
                now_x + next_direction.value[0], now_y + next_direction.value[1]
            )

    @property
    def get_full_path_history(self):
        full_hist = self._path_history + [self.position]
        return full_hist

    @property
    def last_position(self):
        return self._path_history[-1]


def draw_grid(width: int, height: int, points: list[Coordinate]) -> None:
    full_grid = [["."] * width] * height
    for point in points:
        x, y = point
        x += 11
        y += 6
        test = full_grid[height - y - 1]
        if test[x] == ".":
            full_grid[height - y - 1] = test[0:x] + ["#"] + test[x + 1 :]

    for line in full_grid:
        if line !=["."] * width:
            print(" ".join(line), end="\n")
    print("\n")


def get_move_instruction(aoc_file: AOCFILE) -> MoveInstructions:
    instruction: MoveInstructions = []
    for line in aoc_file:
        raw_move, distance = line.split(" ")
        match raw_move:
            case "R":
                move = Direction.RIGHT
            case "U":
                move = Direction.UP
            case "L":
                move = Direction.LEFT
            case "D":
                move = Direction.DOWN
        instruction.append((move, int(distance)))
    return instruction


class Rope:
    def __init__(self, rope_lens: int) -> None:
        node_names: list[str] = ["Head"] + list(map(str, range(1, rope_lens)))
        self.nodes: dict[str, Node] = {"Head": Node(former_node="Head")} | {
            node_names[i]: Node(former_node=node_names[i - 1])
            for i in range(1, rope_lens)
        }
        self.last_dir:Direction|None = None

    def is_needed_move(
        self, former_node_position: Coordinate, latter_node_position: Coordinate
    ) -> bool:
        latter_x, latter_y = latter_node_position
        latter_surround: list[Coordinate] = [
            Coordinate(x=latter_x + x_move, y=latter_y + y_move)
            for x_move in range(-1, 2)
            for y_move in range(-1, 2)
        ]
        return not former_node_position in latter_surround

    def rope_tension_move(
        self, former_node: str, latter_node: str, head_dir: Direction
    ) -> None:
        next_x, next_y = self.nodes[former_node].position
        my_x, my_y = self.nodes[latter_node].position

        if abs(next_x - my_x) + abs(next_y - my_y) > 2:
            new_x = 1 if next_x > my_x else -1
            new_y = 1 if next_y > my_y else -1
            self.nodes[latter_node].move(next_position=Coordinate(x = my_x + new_x, y = my_y + new_y))
            return
        new_x = (next_x - my_x) // 2 if next_x != my_x else 0
        new_y = (next_y - my_y) // 2 if next_y != my_y else 0
        self.nodes[latter_node].move(next_position=Coordinate(x = my_x + new_x, y = my_y + new_y))




    def follow_up(self, direction: Direction) -> None:
        for node_name, node in self.nodes.items():
            if node_name == "Head":
                self.nodes[node_name].move(next_direction=direction)
            else:
                former_node_position = self .nodes[node.former_node].position
                if self.is_needed_move(
                    former_node_position=former_node_position,
                    latter_node_position=node.position,
                ):
                    self.rope_tension_move(
                        former_node=node.former_node,
                        latter_node=node_name,
                        head_dir=direction,
                    )
                    # node.move(next_position=self.nodes[node.former_node].last_position)



class Movement:
    def __init__(self, moves_instructs: MoveInstructions, rope: Rope) -> None:
        self.rope: Rope = rope
        self.moves_instructs = moves_instructs

    def simulate(self) -> None:
        for instruct in self.moves_instructs:
            direction, times = instruct
            for _ in range(times):
                self.rope.follow_up(direction=direction)


def Question(num: int, rope_len: int) -> None:
    rope = Rope(rope_lens=rope_len)
    move_instructions = get_move_instruction(aoc_file=read_aoc(9))
    rope_movement = Movement(rope=rope, moves_instructs=move_instructions)
    rope_movement.simulate()
    end_node_name = list(rope_movement.rope.nodes)[-1]
    print(rope.nodes[end_node_name].get_full_path_history)
    print_ans(
        num, len(set(rope_movement.rope.nodes[end_node_name].get_full_path_history))
    )
    #draw_grid(width=26, height=30, points=rope_movement.rope.nodes[end_node_name].get_full_path_history)

if __name__ == "__main__":
    # Question(1, 2)
    Question(2, 10)
