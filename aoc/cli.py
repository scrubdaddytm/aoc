import argparse
from contextlib import contextmanager


@contextmanager
def file_input(*args, **kwds):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=argparse.FileType('r'))
    cli_args = parser.parse_args()
    yield cli_args.filename