from pathlib import Path

import typer
from rich import print
from typer import Argument, Option
from typing_extensions import Annotated

from pepito import git_commands
from pepito.checkin_service import CheckInService
from pepito.diff_service import (
    run_diff_with_choice,
    run_diff_with_commit,
    run_diff_with_file,
)
from pepito.errors import PepitoException
from pepito.gms_files import GmsFile

app = typer.Typer(rich_markup_mode="rich")

state = {"verbose": 0}


@app.command()
def diff(
    file: Annotated[
        Path,
        Argument(
            help="Path of the current file to compare. Path can be absolute or relative"
        ),
    ],
    other: Annotated[
        Path,
        Option(
            "--other",
            "-o",
            help="Path of the other file to compare. Path can be absolute or relative",
        ),
    ] = None,
    commit: Annotated[
        str,
        Option("--commit", "-c", help="Commit sha1 for the revision to compare"),
    ] = "",
):
    """
    Make a diff between 2 files, which can be on the file system or on Git.
    Display it with clearcase format in RTF.
    """
    verbose = state.get("verbose", False)

    try:
        if other and not commit:
            print(f"Running diff between {file} and {other}")
            run_diff_with_file(file, other, verbose)

        elif commit and not other:
            print(
                f"Running diff of file {file} between current revision and revision "
                f"{commit}"
            )
            run_diff_with_commit(file, commit, verbose)

        elif not commit and not other:
            run_diff_with_choice(file, verbose)

        else:
            print(
                "It is not possible to run diff with --other and --commit activated at "
                "the same time."
            )
    except PepitoException as e:
        print(e)
        raise typer.Exit(e.error_code)
    except Exception as e:
        print(f"UnknownError: {e}")
        raise typer.Exit(10)


@app.command()
def checksum(
    file: Annotated[
        Path,
        Argument(
            help="Path of the file to compute the checksum on. Path can be absolute or "
            "relative"
        ),
    ],
):
    """
    Compute the checksum (currently only MD5 is supported) of a file
    """
    print(f"Running checksum for {file}")
    try:
        gms_file = GmsFile.from_file_path(file, verbose=state.get("verbose", False))
        print(gms_file.md5)
    except PepitoException as e:
        print(e)
        raise typer.Exit(e.error_code)
    except Exception as e:
        print(f"UnknownError: {e}")
        raise typer.Exit(10)


@app.command()
def check_in():
    check_in_service = CheckInService()
    print("Checking in before commit")
    cwd = Path.cwd()
    try:
        modified_files = git_commands.get_staged_files(cwd)
        for file in modified_files:
            if state.get("verbose") > 0:
                print(f"Checking {file}")
            foc = typer.prompt("FOC version", type=str, default="")
            version = typer.prompt("File version", type=str, default="")
            check_in_service.update_headers(file, foc, version)
            check_in_service.verify_headers(file)
    except PepitoException as e:
        print(e)
        raise typer.Exit(e.error_code)
    except Exception as e:
        print(f"UnknownError: {e}")
        raise typer.Exit(10)


@app.callback()
def verbosity(
    verbose: Annotated[
        int,
        Option(
            "--verbose",
            "-v",
            count=True,
            help="Add logs. The more verbose the more logs are displayed",
        ),
    ] = 0,
):
    state.update({"verbose": verbose})
