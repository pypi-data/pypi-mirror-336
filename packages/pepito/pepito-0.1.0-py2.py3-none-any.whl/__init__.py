from pathlib import Path

import typer
from rich import print
from typer import Argument, Option
from typing_extensions import Annotated

from pepito.checksum.checksum_service import run_checksum
from pepito.diff.diff_service import run_diff_with_commit, run_diff_with_file

app = typer.Typer(rich_markup_mode="rich")

VERSION = "0.1.0"


@app.command()
def diff(
    file: Annotated[Path, Argument(help="Path of the current file to compare")],
    other: Annotated[
        Path, Option("--other", "-o", help="Path of the other file to compare")
    ] = None,
    commit: Annotated[
        str,
        Option("--commit", "-c", help="Commit sha1 for the revision to compare"),
    ] = "",
):
    """
    Make a diff between 2 files, which can be on the file system or on Git.
    Display it with clear case format in RTF.
    """
    if other and not commit:
        print(f"Running diff between {file} and {other}")
        run_diff_with_file(file, other)
    elif commit and not other:
        print(
            f"Running diff of file {file} between current revision and revision {commit}"
        )
        run_diff_with_commit(file, commit)
    else:
        print(
            "It is not possible to run diff with --other and --commit activated at the same time."
        )
        raise typer.Exit(1)


@app.command()
def checksum(
    file: Annotated[Path, Argument(help="Path of the file to compute the checksum on")]
):
    """
    Compute the checksum (currently only MD5 is supported) of a file
    """
    print(f"Running checksum for {file}")
    run_checksum(file)
