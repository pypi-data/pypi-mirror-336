from pathlib import Path

import typer
from rich import print

from pepito.checksum.checksum import Checksum


def run_checksum(file: Path):
    try:
        checksum = Checksum(file)
        checksum.change_header()
        checksum.write_file()
    except FileNotFoundError:
        print(f"The file '{file}' was not found\n")
        typer.Exit(1)
