import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List

from rich import print

from pepito.errors import CommitNotFound, GitError, NoDiffFound, NotAFile
from pepito.gms_files import GmsFile
from pepito.models import CommitLog


def diff_from_filesystem(file_v1: Path, file_v2: Path, verbose: int = 0) -> str:
    """
    Make a diff between 2 files from the file system.
    Display only the changed and not the lines before or after

    :param file_v1: the first file to compare
    :param file_v2: the second file to compare
    :param verbose: the verbosity level
    :return: the diff lines from git
    """
    if verbose:
        print(f"Getting git diff between file {file_v1} and file {file_v2}")

    check_file_is_valid(file_v1)
    check_file_is_valid(file_v2)

    # base command
    command = ["git", "diff"]
    # makes git display only changed lines
    command.append("--unified=0")
    # indicate that the comparison is between files from the filesystem and not from Git
    command.append("--no-index")
    # add the 2 files to compare
    command.append(str(file_v1.absolute()))
    command.append(str(file_v2.absolute()))

    if verbose:
        print(f'Git command run: "{" ".join(command)}"')

    # run the command
    result = subprocess.run(command, capture_output=True)

    if result.returncode < 0:
        error = result.stderr.decode()
        raise GitError(error)

    # retrieve the output
    response = result.stdout.decode()

    if verbose == 2:
        print("Response:\n", response)

    if not response:
        raise NoDiffFound(f"There is no diff between file {file_v2} and file {file_v1}")

    return response


def check_file_is_valid(file: Path) -> None:
    """
    Check if the provided file is valid

    :param file: the file to check
    :raise: FileNotFoundError if the file does not exist
    :raise: NotAFile if the file is a directory
    """
    if not file.exists():
        raise FileNotFoundError(f"The file {file} does not exist")
    if file.is_dir():
        raise NotAFile(
            f"The file {file} is a directory and the diff can only be performed on a "
            f"file"
        )


def diff_from_git_history(
    current_file: Path, commit_sha1: str, verbose: int = 0
) -> str:
    """
    Make a diff of a single file between the current Git revision and another revision.
    Display only the changed and not the lines before or after

    :param current_file: the file to compare
    :param commit_sha1: the git revision to campare
    :param verbose: the verbosity level
    :return: the diff lines from git
    """
    if verbose:
        print(
            f"Getting git diff for file {current_file} between current revision and "
            f"commit {commit_sha1}"
        )
    check_file_is_valid(current_file)

    # base command
    command = ["git", "diff"]
    # makes git display only changed lines
    command.append("--unified=0")
    # add the sha1 of the revision to compare
    command.append(commit_sha1)
    # add the files to compare
    command.append(str(current_file.absolute()))

    # get the local root directory of the file
    git_root = get_git_root_directory(current_file)

    # run the command
    if verbose:
        print(f'Git command run: "{" ".join(command)}" in directory "{git_root}"')
    # cwd (current working directory) ensures that the command is launched in the
    # right git directory
    result = subprocess.run(command, capture_output=True, cwd=git_root)

    if result.returncode != 0:
        error = result.stderr.decode()
        if "unknown revision or path not in the working tree" in error:
            raise CommitNotFound(
                f"The commit {commit_sha1} was not found in the working tree"
            )

        raise GitError(error)

    # retrieve the output
    response = result.stdout.decode()

    if verbose == 2:
        print("Response:\n", response)

    if not response:
        raise NoDiffFound(
            f"There is no diff between file {current_file} in current revision and in "
            f"commit {commit_sha1} "
        )

    return response


def get_git_root_directory(path: Path, verbose: int = 0) -> Path:
    """
    Get the git root directory of a file or directory.
    The git root directory is where the '.git' folder is located.

    :param path: the path to check
    :param verbose: the verbosity level
    :return: the path to the git root
    """
    if verbose:
        print(f"Getting Git root directory for path {path}")
    command = ["git", "rev-parse", "--show-toplevel"]

    cwd = path.parent if path.is_file() else path
    if verbose:
        print(f'Git command run: "{" ".join(command)}" in directory "{cwd}"')
    result = subprocess.run(command, capture_output=True, cwd=cwd)
    response = result.stdout.decode().strip()
    if verbose == 2:
        print("Response:\n", response)
        print(f"Git root directory of path {path} is {Path(response)}")
    return Path(response)


def get_commits_for_file(file: Path, verbose: int = 0) -> List[CommitLog]:
    """
    Get all the commits for the given file.

    :param file: the file to get the commits from
    :param verbose: the verbosity level
    :return: list of all commits that touched the given file
    """
    if verbose:
        print(f"Getting all the commits for the file {file}")
    command = ["git", "log"]

    # put all information on one line
    command.append("--oneline")
    # set date format
    command.append("--date=iso8601")
    # set log format (%h for the hash, %x09 for tab, %an for author name, %ad for
    # author date and %s for the message
    command.append('--pretty=format:"%h%x09%an%x09%ad%x09%s"')
    # display it in reverse order
    command.append("--reverse")
    # add the file on which the log should be performed
    command.append(str(file))

    git_root = get_git_root_directory(file)

    if verbose:
        print(f'Git command run: "{" ".join(command)}" in directory "{git_root}"')
    result = subprocess.run(command, capture_output=True, cwd=git_root)
    response = result.stdout.decode().strip()

    if verbose == 2:
        print("Response:\n", response)

    commits = []
    # try to match something like:
    # 5ecdd33 Stanislas Jouffroy      2025-03-11 07:21:27 +0100       modified file for test purpose #9
    regex = re.compile(
        r"(\w+)\s+(.*)\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ([+-]\d{4})\s+(.*)"
    )
    for line in response.splitlines():
        # on some systems the line ca start with " for no known reasons
        line.removeprefix('"')

        hash_, author, date, timezone, message = regex.findall(line)[0]
        iso_date = f"{date}{timezone[:3]}:{timezone[3:]}"

        commits.append(
            CommitLog(
                hash=hash_,
                author=author.strip(),
                date=datetime.fromisoformat(iso_date),
                message=message,
            )
        )
    return commits


def get_user_name() -> str:
    """
    Get the git username
    :return: the git username
    """
    command = ["git", "config", "user.name"]
    result = subprocess.run(command, capture_output=True)
    return result.stdout.decode().strip()


def get_staged_files(git_path: Path, verbose: int = 0) -> list[GmsFile]:
    """
    Get all files that are staged in Git

    :param git_path: the git root directory
    :param verbose: the verbosity level
    :return: the list of all GMS files that are staged
    """
    command = ["git", "diff", "--name-only", "--cached"]
    response = subprocess.run(command, capture_output=True, cwd=git_path)
    files = response.stdout.decode()

    result = []
    for file in files.splitlines():
        file_path = git_path / file
        result.append(GmsFile.from_file_path(file_path, verbose))
    return result
