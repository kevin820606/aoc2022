from __future__ import annotations
from src.utils import print_ans, read_aoc, AOCFILE
from enum import Enum
import itertools
from dataclasses import dataclass
import curses


class PointType(Enum):
    AIR = "."
    STONE = "#"
    SANDSOURCE = "+"
    SAND = "o"


@dataclass
class Block:
    coord: complex
    pttype: PointType
    stable: bool = False
    is_left: bool = True


def implant_missing_struct(
    start: complex, end: complex, pttype: PointType
) -> list[Block]:
    find = end - start
    if find.real != 0:
        increment = 1 if find.real > 0 else -1
        return [
            Block(coord=complex(start.real + i, start.imag), pttype=pttype)
            for i in range(0, int(find.real) + increment, increment)
        ]
    increment = 1 if find.imag > 0 else -1
    return [
        Block(coord=complex(start.real, start.imag + j), pttype=pttype)
        for j in range(0, int(find.imag) + increment, increment)
    ]


def format_structure(
    aoc_file: AOCFILE
) -> tuple[dict[complex, Block], tuple[int, int], tuple[int, int]]:
    max_x, max_y = 0, 0
    min_x, min_y = 10000, 10000

    complete_struct: dict[complex, Block] = {}
    for line in aoc_file:
        end_points: list[complex] = []
        for part in line.split("->"):
            x, y = map(int, part.strip().split(","))
            if x > max_x:
                max_x = x + 1
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y + 1
            if y < min_y:
                min_y = y
            end_points.append(complex(x, y))
        for start, end in itertools.pairwise(end_points):
            complete_struct |= {
                point.coord: point
                for point in implant_missing_struct(start, end, pttype=PointType.STONE)
            }

    for j in range(max_y):
        for i in range(490, max_x):
            point = complex(i, j)
            if point in complete_struct.keys():
                continue
            complete_struct |= {point: Block(coord=point, pttype=PointType.AIR)}
    return complete_struct, (min_x, max_x), (min_y, max_y)


class DrawBoard:
    def __init__(self, max_x: int, max_y: int, min_x: int, min_y: int) -> None:
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y


    def simple_draw(self, struct: dict[complex, Block]) -> None:
        for j in range(self.max_y):
            print("")
            print(f"{j:03d} ", end="")
            for i in range(self.min_x, self.max_x):
                point = struct.get(complex(i, j))
                point_str = point.pttype.value if struct.get(complex(i, j)) else "."
                print(point_str, end="")
        print("")

    def curses_draw(self, struct: dict[complex, Block]) -> None:
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        for j in range(self.max_y):
            for i in range(self.min_x, self.max_x):
                point = struct.get(complex(i, j))
                point_str = point.pttype.value if struct.get(complex(i, j)) else "."
                self.stdscr.addstr(
                    j,
                    i - self.min_x + 1,
                    point_str,
                )
        self.stdscr.refresh()
        curses.napms(100)


class SandFlow:
    def __init__(
        self, struct: dict[complex, Block], sand_source: complex, last_layer: int
    ):
        self.struct = struct
        self.last_layer = last_layer
        self.sand_source = sand_source
        self.struct[sand_source].pttype = PointType.SANDSOURCE

    def input_new_sand(self) -> complex:
        x = self.sand_source.real
        y = self.sand_source.imag
        starting_sand = complex(x, y)
        self.struct[starting_sand].pttype = PointType.SAND
        return starting_sand

    def _block_exchange(self, moving: complex, moved: complex) -> None:
        self.struct[moving].pttype, self.struct[moved].pttype = (
            self.struct[moved].pttype,
            self.struct[moving].pttype,
        )

    def get_stable(self, check_point: complex) -> bool:
        check_block = self.struct[check_point]
        # if check_block.stable:
        #     return True
        left_block, right_block = self.struct.get(check_point - 1), self.struct.get(check_point + 1)

        if (left_block is None and right_block.pttype != PointType.AIR) or (right_block is None and left_block.pttype != PointType.AIR):
            self.struct[check_point].stable = True
            return True

        if left_block.pttype != PointType.AIR and right_block.pttype != PointType.AIR:
            self.struct[check_point].stable = True
            return True
        return False

    def sand_physic(
        self, moving_sand: complex, next_point: complex
    ) -> tuple[complex, complex]:
        # Case Air
        if self.struct[next_point].pttype == PointType.AIR:
            self._block_exchange(moving=moving_sand, moved=next_point)
            moving_sand = next_point
            next_point = moving_sand + complex(0, 1)
            return moving_sand, next_point

        # Case Stable
        if self.get_stable(check_point = next_point):
            return moving_sand, complex(-1, -1)
        next_left, next_right = next_point - 1, next_point + 1

        if self.struct[next_left].pttype == PointType.AIR:
            self._block_exchange(moving=moving_sand, moved=next_left)
            moving_sand = next_left
            next_point = moving_sand + complex(0, 1)
            return moving_sand, next_point
        if self.struct[next_right].pttype == PointType.AIR:
            self._block_exchange(moving=moving_sand, moved=next_right)
            moving_sand = next_right
            next_point = moving_sand + complex(0, 1)
            return moving_sand, next_point
        return moving_sand, complex(-1, -1)

    def drop_down(self, moving_sand: complex) -> bool:
        next_point = moving_sand + complex(0, 1)
        can_move = True
        while can_move:
            moving_sand, next_point = self.sand_physic(
                moving_sand=moving_sand, next_point=next_point
            )
            if next_point == complex(-1, -1):
                can_move = False
            if next_point.imag == self.last_layer:
                return False
        return True

    def run(self, drawboard: DrawBoard) -> None:
        # drawboard.simple_draw(struct=self.struct)
        run_times = 0
        not_full = True
        while not_full:
            moving_sand = self.input_new_sand()
            not_full = self.drop_down(moving_sand=moving_sand)
            # drawboard.simple_draw(struct=self.struct)
            run_times += 1
            if self.struct[self.sand_source + complex(0, 1)].stable:
                break
        print(run_times)
        # drawboard.simple_draw(struct=self.struct)


def Q1():
    struct, (min_x, max_x), (min_y, max_y) = format_structure(
        aoc_file=read_aoc(14, use_test_data=True)
    )
    draw_board = DrawBoard(max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y)
    sand_flow = SandFlow(struct=struct, sand_source=complex(500, 0), last_layer=max_y)
    # print(sand_flow.struct)
    sand_flow.run(drawboard=draw_board)
    #curses.endwin()

def Q2():
    struct, (min_x, max_x), (min_y, max_y) = format_structure(
        aoc_file=read_aoc(14, use_test_data=False)
    )


    # add new border
    for j in range(max_y + 2):
        for i in range(min_x - 1000, max_x + 1000):
            if not struct.get(complex(i, j)):
                pttype = PointType.AIR if j != max_y + 1 else PointType.STONE
                struct |= {complex(i, j): Block(coord = complex(i, j), pttype=pttype)}
    max_y = max_y + 2
    min_x = min_x - 10
    max_x = max_x + 10

    draw_board = DrawBoard(max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y)
    sand_flow = SandFlow(struct=struct, sand_source=complex(500, 0), last_layer=max_y)
    sand_flow.run(drawboard=draw_board)
    # curses.endwin()

if __name__ == "__main__":
    # Q1()
    Q2()
