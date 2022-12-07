from src.utils import print_ans, read_aoc, AOCFILE
from typing import TypedDict
from enum import Enum, auto, StrEnum

class INPUTTYPE(Enum):
    ACTION = auto()
    FILEINFO = auto()

class FILETYPE(StrEnum):
    FILE = auto()
    DIRECTORY = auto()


class Node(TypedDict, total=False):
    parent: str
    name: str
    children: list[str]
    filetype: FILETYPE
    size: int
    layer: int

FileTree = dict[str, Node]


def get_tree_name(parent_name:str, file_name:str):
    if file_name == "/":
        return "/"
    return f"{parent_name}/{file_name}" if parent_name != "/" else f"/{file_name}"


class FileSystem:

    def __init__(self, inputs: AOCFILE) -> None:
        self.tree: FileTree = dict()
        self.inputs: AOCFILE = inputs
        self.pwd: str = ""
        self.tree["/"] = Node(parent="", name = "/", filetype=FILETYPE.DIRECTORY, layer=0, children=[], size = -1)
        self.max_layer: int = 0
        self.layer_dict: dict[int, set[str]] = {0: {"/"}}

    @staticmethod
    def get_input_type(command: str) -> INPUTTYPE:
        if command[0] == "$":
            return INPUTTYPE.ACTION
        return INPUTTYPE.FILEINFO

    @staticmethod
    def calculate_file_size(node_name: str, tree: FileTree) -> int:

        assert node_name in tree.keys()

        if tree[node_name]["size"] > 0 or tree[node_name]["filetype"] == FILETYPE.FILE:
            return tree[node_name]["size"]

        size = 0
        if tree[node_name]["filetype"] == FILETYPE.DIRECTORY:
            for child_name in tree[node_name]["children"]:
                size += FileSystem.calculate_file_size(node_name = child_name, tree = tree)

        return size

    def parse_action(self, command:str) -> None:
        command = command.replace("$ ", "")

        if "cd" in command:
            dir_name = command.replace("cd ", "")
            if dir_name == "..":
                self.pwd = self.tree[self.pwd]["parent"]
            else:
                self.pwd = get_tree_name(self.pwd, dir_name)

        if "ls" in command:
            pass

    def parse_ls_file(self, command:str) -> None:
        indicator, file_name = command.split(" ")
        child_layer = self.tree[self.pwd]["layer"] + 1

        tree_file_name = get_tree_name(self.pwd, file_name)

        if indicator == "dir":
            self.tree[tree_file_name] = self.tree.get(file_name, Node(
                parent = self.pwd, name = file_name, size = 0, filetype= FILETYPE.DIRECTORY, layer = child_layer, children=[]))
        else:
            self.tree[tree_file_name] = self.tree.get(file_name, Node(
                parent = self.pwd, name = file_name, size = int(indicator), filetype= FILETYPE.FILE, layer = child_layer))


        if not tree_file_name in self.tree[self.pwd]["children"]:
            self.tree[self.pwd]["children"].append(tree_file_name)

        if child_layer > self.max_layer:
            self.max_layer = child_layer
            self.layer_dict.setdefault(self.max_layer, set())
        self.layer_dict[child_layer].add(tree_file_name)

    def check_directory_size(self):
        not_finished = True
        now_layer = self.max_layer
        while not_finished:
            if now_layer == 0:
                not_finished = False
            for tree_file_name in self.layer_dict[now_layer]:
                self.tree[tree_file_name]["size"] = FileSystem.calculate_file_size(node_name=tree_file_name, tree=self.tree)
            now_layer -= 1

    def read_input(self) -> None:
        for command in self.inputs:
            file_type = FileSystem.get_input_type(command=command)
            if file_type == INPUTTYPE.ACTION:
                self.parse_action(command=command)
            if file_type == INPUTTYPE.FILEINFO:
                self.parse_ls_file(command=command)

    def get_directory_size(self, node_name) -> int:
        assert node_name in self.tree.keys()
        return self.tree[node_name]["size"]
    def get_all_directory_size(self) -> list[int]:
        return [node["size"] for node in self.tree.values() if node["filetype"] == FILETYPE.DIRECTORY]

aoc_7 = read_aoc(7)
QuestionFS = FileSystem(inputs=aoc_7)
QuestionFS.read_input()
QuestionFS.check_directory_size()

def Q1():
    bigger_dir = []
    for node in QuestionFS.tree.values():
        if node["filetype"] == FILETYPE.DIRECTORY and node["size"] < 100_000:
            bigger_dir.append(node["size"])
    print_ans(1, sum(bigger_dir))

def Q2():
    require_space = 30_000_000
    total_space = 70_000_000
    occupied_space = QuestionFS.get_directory_size("/")
    free = total_space - occupied_space
    all_dir_size = [size for size in QuestionFS.get_all_directory_size() if size > require_space - free]
    all_dir_size.sort()
    print_ans(2, all_dir_size[0])


if __name__ == "__main__":
    #Q1()
    Q2()

