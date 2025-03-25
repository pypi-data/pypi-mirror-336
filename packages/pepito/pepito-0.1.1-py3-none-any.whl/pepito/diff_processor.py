import re
from pathlib import Path
from typing import List, Optional

from pepito import git_commands
from pepito.diff_lines import (
    ChangeHeader,
    DeleteHeader,
    DeleteLine,
    FileHeader,
    InsertHeader,
    InsertLine,
    Line,
    TransitionLine,
    Header,
)
from pepito.errors import GitError


class DiffProcessor:
    """
    Handle the diff between 2 files. The 2 files can be on the file system or the same
    file at 2 different git revisions.
    """

    def __init__(
        self,
        current_file: Path,
        other_file: Optional[Path] = None,
        commit: Optional[str] = None,
        verbose: int = 0,
    ) -> None:
        self.current_file: Path = current_file
        self.old_file: Path = other_file
        self.commit: str = commit
        self.verbose: int = verbose
        self.lines: List[Line] = []

    def to_clearcase_format(self) -> str:
        """
        Output the diff to the Clearcase format

        :return: the diff as displayed in Clearcase
        """
        if self.old_file:
            git_diff = git_commands.diff_from_filesystem(
                file_v1=self.old_file, file_v2=self.current_file, verbose=self.verbose
            )
        elif self.commit:
            git_diff = git_commands.diff_from_git_history(
                current_file=self.current_file,
                commit_sha1=self.commit,
                verbose=self.verbose,
            )
        else:
            raise ValueError("Missing a file or a git version to compare")

        git_lines = git_diff.splitlines()
        for git_line in git_lines:
            self.add_line_processor(git_line)
            self.add_transition_line_if_necessary()

        return "\n".join(line.to_clearcase_format() for line in self.lines)

    def add_line_processor(self, line: str) -> None:
        """
        Determine the type of line and append the right line processor ot the lines list

        :param line: the line in git format
        """
        if line.startswith("diff"):
            regex = re.compile(r"diff --git [1,c](.+) [2,w](.+)")
            file1, file2 = regex.findall(line)[0]
            self.lines.append(FileHeader(file1=file1, file2=file2))

        elif line.startswith("@"):
            self.lines.append(self.get_header(line))

        elif (
            line.startswith("--- 1")
            or line.startswith("+++ 2")
            or line.startswith("index")
            or line.startswith("new file mode")
        ):
            # lines to be ignored
            pass

        elif line.startswith("+"):
            data = line.replace("+", "", 1)
            self.lines.append(InsertLine(statement=data))

        elif line.startswith("-"):
            data = line.replace("-", "", 1)
            self.lines.append(DeleteLine(statement=data))

        else:
            raise GitError(
                f"Error while converting the line '{line}' to ClearCase format"
            )

    def get_header(self, line: str) -> Header:
        """
        Determine the header type and instantiate it

        :param line: the input line
        :return: the right header type instance
        """
        regex = re.compile(r"@+ -(\d+)(,(\d+))? \+(\d+)(,(\d+))? @+")
        (
            line_nb_before,
            _,
            change_size_before,
            line_nb_after,
            _,
            change_size_after,
        ) = regex.findall(line)[0]

        # convert strings to integers
        line_nb_before = int(line_nb_before)
        line_nb_after = int(line_nb_after)
        change_size_before = int(change_size_before or "-1")
        change_size_after = int(change_size_after or "-1")

        if self.is_delete(change_size_after):
            return DeleteHeader(
                line_nb_before=line_nb_before,
                line_nb_after=line_nb_after,
                lines_changed_before=change_size_before,
                lines_changed_after=change_size_after,
            )
        elif self.is_insert(change_size_before):
            return InsertHeader(
                line_nb_before=line_nb_before,
                line_nb_after=line_nb_after,
                lines_changed_before=change_size_before,
                lines_changed_after=change_size_after,
            )
        elif self.is_change(change_size_before, change_size_after):
            return ChangeHeader(
                line_nb_before=line_nb_before,
                line_nb_after=line_nb_after,
                lines_changed_before=change_size_before,
                lines_changed_after=change_size_after,
            )
        else:
            raise GitError(
                f"Error while converting the line '{line}' to ClearCase format"
            )

    @staticmethod
    def is_delete(change_size_after: int) -> bool:
        """
        check if the line is deleted line.

        :param change_size_after: the number of line which will be inserted
        :return: True if the line is deleted, False otherwise
        """
        return change_size_after == 0

    @staticmethod
    def is_insert(change_size_before: int) -> bool:
        """
        check if the line is inserted line.

        :param change_size_before: the number of line which will be deleted
        :return: True if the line is inserted, False otherwise
        """
        return change_size_before == 0

    @staticmethod
    def is_change(change_size_before: int, change_size_after: int) -> bool:
        """
        check if the line is changed line.

        :param change_size_before: the number of line which will be deleted
        :param change_size_after: the number of line which will be inserted
        :return:
        """
        return (
            (change_size_before < change_size_after)
            or (change_size_before == change_size_after)
            or (change_size_before > 0 and change_size_after == -1)
        )

    def add_transition_line_if_necessary(self) -> None:
        """
        Add a transition line between deleted and inserted lines.
        This occurs when there is at least one deleted line and one inserted line.

        :return: a transition line
        """
        if (
            len(self.lines) > 2
            and type(self.lines[-2]) is DeleteLine
            and type(self.lines[-1]) is InsertLine
        ):
            self.lines.insert(-1, TransitionLine())
