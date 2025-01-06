#!/usr/bin/env python

import argparse
import os
import pathlib
import shutil
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser()
    input_group = parser.add_argument_group("AOC Arguments")
    input_group.add_argument("-d", "--day", type=int, required=True)
    input_group.add_argument(
        "-y", "--year", type=str, default=str(datetime.today().year)
    )
    cli_args = parser.parse_args()

    day_str = f"day_{cli_args.day:02}"
    day_str_short = f"d{cli_args.day:02}"

    path_base = pathlib.Path(__file__).parent.resolve()

    template_path = path_base / "day_template.py"
    day_path = path_base / f"y_{cli_args.year}" / f"{day_str}"
    sample_path = day_path / "sample.in"
    input_path = day_path / f"{day_str_short}.in"
    solution_path = day_path / f"{day_str_short}.py"

    os.makedirs(day_path, exist_ok=True)
    if not solution_path.exists():
        shutil.copy(template_path, solution_path)
    sample_path.touch()
    input_path.touch()


if __name__ == "__main__":
    main()
