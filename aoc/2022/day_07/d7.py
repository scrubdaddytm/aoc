from dataclasses import dataclass
from enum import auto
from enum import Enum
from typing import Any

from aoc.cli import file_input


class FileType(Enum):
    FILE = auto()
    DIR = auto()


@dataclass()
class File:
    parent: "File"
    filetype: FileType
    name: str
    size: int
    children: dict[str, "File"]

    def __repr__(self) -> str:
        return str({
            "parent": self.parent.name if self.parent else None,
            "type": self.filetype.name,
            "name": self.name,
            "size": self.size,
            "children": self.children.keys(),
        })


class Callback:
    def callback(self, current_file: File, depth: int) -> None:
        pass

    def result(self) -> Any:
        pass


class PrintDirStructure(Callback):
    def callback(self, current_file: File, depth: int) -> None:
        print(f"{' '*depth}- {current_file.name} ({current_file.filetype.name}) {current_file.size if current_file.size > 0 else ''}")


class FindSmolDirs(Callback):
    callback_size_total = 0

    def callback(self, current_file: File, depth: int) -> None:
        if current_file.filetype == FileType.DIR and current_file.size <= 100_000:
            self.callback_size_total += current_file.size

    def result(self) -> int:
        return self.callback_size_total


class FindDirToDelete(Callback):
    smollest = 70_000_000

    def __init__(self, root_dir_size: int) -> None:
        self.mem_needed = 30_000_000 - (70_000_000 - root_dir_size)

    def callback(self, current_file: File, depth: int) -> None:
        if current_file.size >= self.mem_needed:
            self.smollest = min(self.smollest, current_file.size)

    def result(self) -> int:
        return self.smollest


def calculate_sizes(root_dir: File) -> int:
    if root_dir.filetype == FileType.FILE:
        return root_dir.size

    for file in root_dir.children.values():
        val = calculate_sizes(file)
        root_dir.size += val

    return root_dir.size


def traverse_preorder(root_dir: File, callback: Callback) -> Any:
    stack = []
    stack.append((root_dir, 0))
    while len(stack):
        current_file, depth = stack.pop()

        callback.callback(current_file, depth)

        for next_file in reversed(current_file.children.values()):
            stack.append((next_file, depth+1))

    return callback.result()

def parse_terminal_output(terminal_output: list[str]) -> File:
    root = File(None, FileType.DIR, "/", 0, {})
    current_dir = root
    for line in terminal_output[1:]:
        match (cmd := line.split()):
            case ["$", "ls"]:
                pass
            case ["$", "cd", "/"]:
                current_dir = root
            case ["$", "cd", ".."]:
                current_dir = current_dir.parent
            case ["$", "cd", _]:
                current_dir = current_dir.children[cmd[2]]
            case ["dir", _]:
                current_dir.children[cmd[1]] = File(current_dir, FileType.DIR, cmd[1], 0, {})
            case _:
                current_dir.children[cmd[1]] = File(current_dir, FileType.FILE, cmd[1], int(cmd[0]), {})

    return root


def main() -> None:
    terminal_output = []
    with file_input() as file:
        while line := file.readline().strip():
            terminal_output.append(line)

    directory_root = parse_terminal_output(terminal_output)

    calculate_sizes(directory_root)

    traverse_preorder(directory_root, PrintDirStructure())
    print(f"smol dir sum = {traverse_preorder(directory_root, FindSmolDirs())}")
    print(f"dir size to delete = {traverse_preorder(directory_root, FindDirToDelete(directory_root.size))}")

if __name__ == "__main__":
    main()
