from src.utils import print_ans, read_aoc, AOCFILE
from typing import TypedDict, NamedTuple
from enum import Enum, auto


class DIRECTION(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()

class VISIBLE(Enum):
    IS_VISIBLE = auto()
    HIGH_AS_NEAR = auto()
    NOT_VISIBLE = auto()

class TreeInfo(TypedDict):
    height: int
    is_visible: VISIBLE | None
    up_visible: VISIBLE | None
    down_visible: VISIBLE | None
    left_visible: VISIBLE | None
    right_visible: VISIBLE | None


class Location(NamedTuple):
    x: int
    y: int


ForestType = dict[Location, TreeInfo]


class ElvesForest:
    def __init__(self, aoc_file: AOCFILE):
        self.aoc_file = aoc_file
        self.max_x = 0
        self.max_y = 0
        self.forest: ForestType = dict()

    def parse_forest(self) -> None:
        for x, line in enumerate(self.aoc_file):
            for y, tree_height in enumerate(line):
                self.forest[Location(x, y)] = TreeInfo(
                    height=int(tree_height),
                    is_visible=None,
                    up_visible=None,
                    right_visible=None,
                    down_visible=None,
                    left_visible=None,
                )
        self.max_x = x
        self.max_y = y

    def mark_visible(
        self, loc: Location, visible_loc: str, compare_height=int, find_dir=DIRECTION
    ) -> VISIBLE:
        find_tree = self.forest.get(loc)

        if find_tree is None:
            return VISIBLE.IS_VISIBLE

        if find_tree[visible_loc] in [VISIBLE.IS_VISIBLE, VISIBLE.HIGH_AS_NEAR]:
            if compare_height > find_tree["height"]:
                return VISIBLE.IS_VISIBLE
            if compare_height == find_tree["height"]:
                return VISIBLE.HIGH_AS_NEAR
            return VISIBLE.NOT_VISIBLE

        if find_tree[visible_loc] == VISIBLE.NOT_VISIBLE:
            return VISIBLE.NOT_VISIBLE

        while find_tree[visible_loc] is None:
            self.check_visible(
                tree_loc=loc,
                find_direction=find_dir,
            )
        return self.mark_visible(loc, visible_loc, compare_height, find_dir)

    def check_visible(
        self, tree_loc: Location, find_direction: DIRECTION | None = None
    ) -> None:

        check_directions = (
            [DIRECTION.UP, DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.DOWN]
            if find_direction is None
            else [find_direction]
        )

        for direction in check_directions:
            match direction:
                case DIRECTION.UP:
                    self.forest[tree_loc]["up_visible"] = self.mark_visible(
                        loc=Location(tree_loc[0], tree_loc[1] - 1),
                        visible_loc="up_visible",
                        compare_height=self.forest[tree_loc]["height"],
                        find_dir=direction,
                    )

                case DIRECTION.LEFT:
                    self.forest[tree_loc]["left_visible"] = self.mark_visible(
                        loc=Location(tree_loc[0] - 1, tree_loc[1]),
                        visible_loc="left_visible",
                        compare_height=self.forest[tree_loc]["height"],
                        find_dir=direction,
                    )

                case DIRECTION.DOWN:
                    self.forest[tree_loc]["down_visible"] = self.mark_visible(
                        loc=Location(tree_loc[0], tree_loc[1] + 1),
                        visible_loc="down_visible",
                        compare_height=self.forest[tree_loc]["height"],
                        find_dir=direction,
                    )

                case DIRECTION.RIGHT:
                    self.forest[tree_loc]["right_visible"] = self.mark_visible(
                        loc=Location(tree_loc[0] + 1, tree_loc[1]),
                        visible_loc="right_visible",
                        compare_height=self.forest[tree_loc]["height"],
                        find_dir=direction,
                    )
        self.forest[tree_loc]["is_visible"] = any([self.forest[tree_loc]["down_visible"] == VISIBLE.IS_VISIBLE, self.forest[tree_loc]["left_visible"]== VISIBLE.IS_VISIBLE, self.forest[tree_loc]["right_visible"]== VISIBLE.IS_VISIBLE, self.forest[tree_loc]["up_visible"]== VISIBLE.IS_VISIBLE])

    @property
    def get_visible_tree(self) -> int:
        count = 0
        for info in self.forest.values():
            try:
                count += info["is_visible"]
            except:
                print(info)
        return count

    def find_all_visible(self) -> None:
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                find_loc = Location(x, y)
                self.check_visible(find_loc)


def Q1():
    QuestionEF = ElvesForest(aoc_file=read_aoc(8))
    QuestionEF.parse_forest()
    QuestionEF.find_all_visible()
    from pprint import pprint
    pprint(QuestionEF.get_visible_tree)


if __name__ == "__main__":
    Q1()
