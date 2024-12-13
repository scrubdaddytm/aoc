from aoc.cli import file_input
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Label


class Solver:

    def solve_p1(self, data: list[str], data_visualizer: "DataVisualizer") -> int:
        data_visualizer.data = "running..."
        return -1

    def solve_p2(self, data: list[str], data_visualizer: "DataVisualizer") -> int:
        data_visualizer.data = "running..."
        return -12


class Loader:

    data = None

    def load_data(self) -> list[str]:
        data = []
        with file_input() as file:
            while line := file.readline().strip():
                data.append(line)

        self.data = data


class DataVisualizer(Label):
    data = reactive("Empty")

    def watch_data(self, data) -> None:
        self.update(f"{self.data}")


class Result(Label):
    result: int = reactive(0)
    part: int

    def watch_result(self, result) -> None:
        self.update(f"Part {self.part}: {self.result}")


class TextualAppTemplate(App):
    CSS = """
    .buttons {
        align: center bottom;
    }
    .data {
        align: center top;
    }
    """
    day = "1"

    def on_mount(self) -> None:
        self.title = f"Advent of Code -- Day {self.day}"
        self.theme = "dracula"
        self.auto_refresh = 1 / 30

        self.loader = Loader()
        self.loader.load_data()
        self.solver = Solver()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(classes="data"):
            yield DataVisualizer(id="data")
            p1_result = Result(id="p1_result")
            p1_result.part = 1
            yield p1_result
            p2_result = Result(id="p2_result")
            p2_result.part = 2
            yield p2_result
        with HorizontalGroup(classes="buttons"):
            yield Button("Run P1", id="p1_button")
            yield Button("Run P2", id="p2_button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        data_visualizer = self.get_widget_by_id("data")
        match event.button.id:
            case "p1_button":
                p1_widget = self.get_widget_by_id("p1_result")
                result = self.solver.solve_p1(
                    self.loader.data,
                    data_visualizer,
                )
                p1_widget.result = result
            case "p2_button":
                p2_widget = self.get_widget_by_id("p2_result")
                result = self.solver.solve_p2(
                    self.loader.data,
                    data_visualizer,
                )
                p2_widget.result = result


if __name__ == "__main__":
    app = TextualAppTemplate()
    app.run(inline=True)
