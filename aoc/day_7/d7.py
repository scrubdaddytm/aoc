from dataclasses import dataclass
import queue
from enum import auto
from enum import Enum

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


def calculate_sizes(root_dir: File):
    if root_dir.filetype == FileType.FILE:
        return root_dir.size

    for file in root_dir.children.values():
        val = calculate_sizes(file)
        root_dir.size += val

    return root_dir.size


def find_dir_to_delete(root_dir: File) -> int:
    mem_needed = 30_000_000 - (70_000_000 - root_dir.size)
    print(f"{mem_needed=}")
    smollest = root_dir.size
    
    stack = []
    stack.append(root_dir)
    while len(stack):
        current_file = stack.pop()

        if current_file.size >= mem_needed:
            print(f"{smollest=} VS {current_file.size}")
            smollest = min(smollest, current_file.size)
        else:
            print(f"im too smol {current_file.name}: {current_file.size}")
        
        for next_file in current_file.children.values():
            stack.append(next_file)

    return smollest



def find_small_directories(root_dir: File) -> None:
    size_sum = 0

    stack = []
    stack.append(root_dir)
    while len(stack):
        current_file = stack.pop()

        if current_file.filetype == FileType.DIR:
            for next_file in reversed(current_file.children.values()):
                stack.append(next_file)
            if current_file.size <= 100_000:
                size_sum += current_file.size
    return size_sum


def traverse(root_dir: File, callback: callable) -> None:
    stack = []
    stack.append(root_dir)
    while len(stack):
        current_file = stack.pop()

        callback(current_file)

        for next_file in reversed(current_file.children.values()):
            stack.append(next_file)

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

    traverse(directory_root, lambda current_file : print(f"- {current_file.name} ({current_file.filetype.name}) {current_file.size if current_file.size > 0 else ''}"))
    print(f"-"*200)

    calculate_sizes(directory_root)

    traverse(directory_root, lambda current_file : print(f"- {current_file.name} ({current_file.filetype.name}) {current_file.size if current_file.size > 0 else ''}"))
    print(f"-"*200)

    size_total = find_small_directories(directory_root)

    print(f"{size_total=}")

    print(f"-"*200)
    print(f"{find_dir_to_delete(directory_root)}")

if __name__ == "__main__":
    main()