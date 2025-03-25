from pathlib import Path

import typer

from pepito import git_commands
from pepito.diff_processor import DiffProcessor
from pepito.errors import InvalidChoice
from pepito.rtf_writer import RtfWriter

rtf_writer = RtfWriter()


def run_diff_with_file(file: Path, other: Path, verbose: int = 0) -> None:
    """
    Run a diff between 2 files on the filesystem.

    :param file: the file to compare
    :param other: the other file 2 compare
    :param verbose: the verbosity level
    """
    diff_processor = DiffProcessor(current_file=file, other_file=other, verbose=verbose)
    filename = f"diff-{other.name}-{file.name}.rtf"
    diff = diff_processor.to_clearcase_format()

    rtf_writer.write(diff, filename, other, file)
    rtf_writer.display(filename)


def run_diff_with_commit(file: Path, commit_sha1: str, verbose: int = 0) -> None:
    """
    Run a diff between 2 versions in git of the same file.

    :param file: the file to compare
    :param commit_sha1: the revision sha1
    :param verbose: the verbosity level
    """
    diff_processor = DiffProcessor(
        current_file=file, commit=commit_sha1, verbose=verbose
    )
    filename = f"diff-{commit_sha1}-{file.name}.rtf"
    diff = diff_processor.to_clearcase_format()

    rtf_writer.write(diff, filename, file)
    rtf_writer.display(filename)


def run_diff_with_choice(file: Path, verbose: int = 0) -> None:
    """
    Run the diff interactively.
    The user can choose either a file or a revision to compare to a file.

    :param file: the file to compare.
    :param verbose: the verbosity level
    """
    last_commits = git_commands.get_commits_for_file(file, verbose=verbose)

    question = ["Choose a revision or a custom file to compare your file with:"]
    n = 1
    for n, commit in enumerate(last_commits):
        question.append(f"{n+1}. {commit}")
    question.append(f"{n+2}. Choose a file")
    question.append("Choose a number")

    choice = int(typer.prompt("\n".join(question), type=int)) - 1

    if choice and choice == len(last_commits):
        other = typer.prompt(
            "Give the path to the file to compare", prompt_suffix="\n", type=Path
        )
        run_diff_with_file(file, other, verbose=verbose)

    elif 0 <= choice < len(last_commits):
        run_diff_with_commit(file, last_commits[choice].hash, verbose=verbose)

    else:
        raise InvalidChoice("This choice is not available")
