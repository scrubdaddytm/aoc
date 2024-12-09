import argparse
import pathlib
import sys
from contextlib import contextmanager


@contextmanager
def file_input(*args, **kwds):
    parser = argparse.ArgumentParser()
    file_input_group = parser.add_argument_group("file input group")
    file_input_group.add_argument("-i", "--input-file", type=str, default="")
    file_input_group.add_argument("-s", "--use-sample", action="store_true")
    cli_args = parser.parse_args()

    input_file = cli_args.input_file
    if input_file == "":
        day_program = pathlib.Path(sys.argv[0])
        input_filename = (
            "sample.in" if cli_args.use_sample else f"{day_program.stem}.in"
        )
        input_file = day_program.parent / input_filename
        if not input_file.exists():
            raise ValueError(f"no input file present: {input_filename}")
    else:
        input_file = pathlib.Path(input_file)

    yield input_file.open()


def check_debug(*args, **kwds) -> bool:
    parser = argparse.ArgumentParser()
    debugging_input_group = parser.add_argument_group("debugging flags")
    debugging_input_group.add_argument("-d", "--debug", action="store_true")
    cli_args = parser.parse_args()

    return cli_args.debug
