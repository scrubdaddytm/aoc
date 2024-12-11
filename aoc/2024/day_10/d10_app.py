import time
from collections import defaultdict, deque

from aoc.cli import file_input
from aoc.geometry import CARDINAL_DIRECTIONS, Point
from aoc.print_tools import make_grid
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, Header, Static


def find_trails(
    topo_map: dict[Point, int],
    trailheads: set[Point],
) -> dict[Point, set[Point]]:
    access = defaultdict(set)

    for trailhead in trailheads:
        seen = set()
        q = deque()
        q.append(trailhead)

        while q:
            p = q.popleft()
            if p in seen:
                continue
            seen.add(p)
            p_val = topo_map[p]

            for d in CARDINAL_DIRECTIONS:
                next_cell = d(p)
                if next_cell not in topo_map:
                    continue

                next_val = topo_map[next_cell]
                if next_val == p_val + 1:
                    if next_val == 9:
                        access[trailhead].add(next_cell)
                    if next_cell not in seen:
                        q.append(next_cell)

    return access


class MyApp(App):

    topo_map = {}
    trailheads = set()
    ends = set()

    BINDINGS = [Binding("ctrl+c", "quit", "Quit", show=False, priority=True)]

    def on_mount(self) -> None:
        self.title = "Advent of Code -- Day 10"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Load Data", id="data")
        yield Static(id="graph")
        yield Button("Run P1", id="p1")
        yield Static(id="p1_result")
        yield Button("Run P2", id="p2")
        yield Static(id="p2_result")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "data":
                self.get_widget_by_id("graph").update("LOADING DATA")
                self.load_data()
            case "p1":
                if not self.topo_map:
                    self.load_data()
                p1_access = find_trails(self.topo_map, self.trailheads)
                p1 = sum(len(p1_access[trailhead])
                         for trailhead in self.trailheads)
                self.get_widget_by_id("p1_result").update(f"Part 1: {p1}")
            case "p2":
                if not self.topo_map:
                    self.load_data()
                self.access = defaultdict(int)
                p2_access = await self.distinct_trails(
                    self.topo_map,
                    self.ends,
                    self.access,
                )
                p2 = sum(p2_access[trailhead] for trailhead in self.trailheads)

                grid = make_grid(self.access, min_x=0, min_y=0)
                self.get_widget_by_id("p2_result").update(
                    f"{grid}\nPart 2: {p2}")

    async def distinct_trails(
        self,
        topo_map: dict[Point, int],
        ends: set[Point],
        access: dict[Point, int],
    ) -> dict[Point, int]:
        seen = set()
        q = deque()
        for end in ends:
            q.append(end)
            access[end] = 1

        while q:
            p = q.popleft()
            if p in seen:
                continue
            seen.add(p)
            p_val = topo_map[p]

            grid = make_grid(self.access, min_x=0, min_y=0)
            self.get_widget_by_id("p2_result").update(grid)
            self.refresh()

            for d in CARDINAL_DIRECTIONS:
                next_cell = d(p)
                if next_cell not in topo_map:
                    continue

                next_val = topo_map[next_cell]
                if next_val == p_val - 1:
                    access[next_cell] += access[p]
                    if next_cell not in seen:
                        q.append(next_cell)

        return access

    def load_data(self) -> None:
        self.topo_map = defaultdict(int)
        with file_input() as file:
            i = 0
            while line := file.readline().strip():
                for j, c in enumerate(line):
                    if c == ".":
                        continue
                    c_int = int(c)
                    p = Point(j, i)
                    self.topo_map[p] = c_int
                    if c_int == 0:
                        self.trailheads.add(p)
                    elif c_int == 9:
                        self.ends.add(p)
                i += 1
        grid = make_grid(self.topo_map, min_x=0, min_y=0)
        self.get_widget_by_id("graph").update(
            f"{grid}\nTrailheads: {self.trailheads}\nPeaks: {self.ends}"
        )


if __name__ == "__main__":
    app = MyApp()
    app.run(inline=True)
