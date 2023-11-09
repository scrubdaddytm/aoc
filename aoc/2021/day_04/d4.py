from aoc.cli import file_input
from aoc.geometry import Point
from dataclasses import dataclass
from enum import Enum


class Color(str, Enum):
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


@dataclass
class Cell:
    value: int
    position: Point
    called: bool = False

    def __repr__(self):
        return str(self.value)

class Board:
    def __init__(self, raw_board: list[list[int]]):
        self.cells_by_number = dict()
        self.rows = []
        for y, raw_row in enumerate(raw_board):
            row = []
            for x, raw_cell in enumerate(raw_row):
                cell = Cell(value=raw_cell, position=Point(x, y))
                row.append(cell)
                self.cells_by_number[raw_cell] = cell
            self.rows.append(row)

    def __repr__(self):
        rep = ""
        for row in self.rows:
            rep += "\n"
            rep += " ".join(map(lambda x: f"{Color.GREEN if x.called else ''}{str(x):>2}{Color.END if x.called else ''}", row))
        return rep + "\n"

    def score(self) -> int:
        uncalled_sum = 0
        for row in self.rows:
            for cell in row:
                if not cell.called:
                    uncalled_sum += cell.value
        return uncalled_sum

    def bingo(self) -> bool:
        for i in range(5):
            row_bingo = True
            col_bingo = True
            for j in range(5):
                row_bingo = row_bingo and self.rows[i][j].called
                col_bingo = col_bingo and self.rows[j][i].called
                if not row_bingo and not col_bingo:
                    break
            if row_bingo or col_bingo:
                return True
        return False
        # well i didn't read that diagonals dont count before I wrote this monstrosity...
        # return (
        #     self.rows[0][0].called and self.rows[1][1].called and self.rows[2][2].called and self.rows[3][3].called and self.rows[4][4].called
        #     ) or (
        #     self.rows[0][4].called and self.rows[1][3].called and self.rows[2][2].called and self.rows[3][1].called and self.rows[4][0].called
        # )


def play_bingo(draws: list[int], boards: list[Board]) -> int:
    for draw in draws:
        for board in boards:
            cell = board.cells_by_number.get(draw)
            if cell:
                cell.called = True
            if board.bingo():
                print(boards)
                return draw * board.score()
    return -1


def main() -> None:
    draws = []
    boards = []
    with file_input() as file:
        draws = list(map(int, file.readline().strip().split(",")))
        while line := file.readline():
            raw_board = []
            for _ in range(5):
                raw_board.append(map(int, file.readline().strip().split()))
            boards.append(Board(raw_board))

    print(f"part 1: {play_bingo(draws, boards)}")

if __name__ == "__main__":
    main()
