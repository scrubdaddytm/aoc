import asyncio
from collections import OrderedDict

from aoc.cli import file_input
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Label


class Data(Label):
    data = reactive("")

    def watch_data(self, data) -> None:
        self.update(data)


class Result(Label):
    result: int = reactive(0)
    part: int

    def __init__(self, part: int = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.part = part

    def watch_result(self, result) -> None:
        self.update(f"Part {self.part}: {self.result}")


class Day01App(App):
    CSS = """
    .buttons {
        align: center bottom;
    }
    .data {
        align: center top;
        width: 100%;
    }
    """
    day = "1"
    left_locs = []
    right_locs = []

    def on_mount(self) -> None:
        self.title = f"Advent of Code -- Day {self.day}"
        self.theme = "dracula"

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(classes="data"):
            yield Data(id="data")
            yield Result(id="p1_result", part=1)
            yield Result(id="p2_result", part=2)
        with HorizontalGroup(classes="buttons"):
            yield Button("Load Data", id="load_data")
            yield Button("Run P1", id="p1")
            yield Button("Run P2", id="p2")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "load_data":
                self.load_data()
            case "p1":
                if not self.right_locs:
                    self.load_data()
                await self.run_p1()
            case "p2":
                if not self.right_locs:
                    self.load_data()
                await self.run_p2()

    async def run_p1(self) -> None:
        p1_result = self.get_widget_by_id("p1_result")
        data_widget = self.get_widget_by_id("data")

        disp = ""
        diff = 0
        for left, right in zip(self.left_locs, self.right_locs):
            curr_diff = abs(left - right)
            disp += f"abs({left} - {right}) = {curr_diff}\n"
            diff += curr_diff
            data_widget.data = disp + f"    sum = {diff}"
            await asyncio.sleep(0.5)

        p1_result.result = diff

    async def run_p2(self) -> None:
        p2_result = self.get_widget_by_id("p2_result")
        data_widget = self.get_widget_by_id("data")

        disp = ""
        total = 0
        count = OrderedDict()
        for right in self.right_locs:
            if right in count:
                count[right] += 1
            else:
                count[right] = 1
            data_widget.data = str(count)
            await asyncio.sleep(0.1)

        disp += str(count) + "\n"
        for left in self.left_locs:
            prod = left * count.get(left, 0)
            disp += f"{left} * {right} = {prod}\n"
            total += prod
            data_widget.data = disp + f"    sum = {total}"
            await asyncio.sleep(0.5)

        p2_result.result = total

    def load_data(self) -> None:
        data_widget = self.get_widget_by_id("data")
        self.left_locs = []
        self.right_locs = []
        with file_input() as file:
            while line := file.readline().strip():
                left, right = map(int, line.split())
                self.left_locs.append(left)
                self.right_locs.append(right)

        data = ""
        for left, right in zip(self.left_locs, self.right_locs):
            data += f"{left}, {right}\n"
        data_widget.data = data[:-1]


if __name__ == "__main__":
    app = Day01App()
    app.run(inline=True)
