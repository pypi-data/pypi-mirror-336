from abc import ABC

from pydantic import BaseModel, field_validator


class Line(ABC):
    """
    A line is one line of diff, that can be a header line or a body line.
    """

    def to_clearcase_format(self) -> str:
        """
        Format the line according to Clearcase style

        :return: the line with the clearcase format
        """
        pass


class Header(Line, BaseModel):
    """
    A Header line is composed of 4 information:
    * the line number on which the change is applied (line_nb_before)
    * the number of lines that change (lines_changed_before)
    * the line number the change will be once it is applied (line_nb_after)
    * the number of lines the change has (lines_changed_after)
    """

    line_nb_before: int
    line_nb_after: int
    lines_changed_before: int
    lines_changed_after: int


class InsertHeader(Header):
    """
    An insert header is used to indicate that the following lines will be inserted
    """

    def to_clearcase_format(self) -> str:
        end_line_after = self.line_nb_after + self.lines_changed_after - 1
        return (
            f"-----[after {self.line_nb_before} "
            f"inserted {self.line_nb_after}-{end_line_after}]-----"
        )


class DeleteHeader(Header):
    """
    A delete header is used to indicate that the following lines will be deleted
    """

    def to_clearcase_format(self) -> str:
        return f"-----[deleted {self.line_nb_before} after {self.line_nb_after}]-----"


class ChangeHeader(Header):
    """
    A change header is used to indicate that the following lines will be replaced
    """

    def to_clearcase_format(self) -> str:
        if self.lines_changed_before > 1:
            end_line_before = self.line_nb_before + self.lines_changed_before - 1
            before = f"{self.line_nb_before}-{end_line_before}"
        else:
            before = self.line_nb_before

        if self.lines_changed_after > 1:
            end_line_after = self.line_nb_after + self.lines_changed_after - 1
            after = f"{self.line_nb_after}-{end_line_after}"
        else:
            after = self.line_nb_after
        return f"-----[{before} changed to {after}]-----"

    @field_validator("lines_changed_before", "lines_changed_after", mode="after")
    @classmethod
    def is_minimum_1(cls, value: int) -> int:
        """
        Validate that lines_changed_before and lines_changed_after value is at least 1

        :param value: the field value
        :return: the corrected value
        """
        return max(1, value)


class BodyLine(Line, BaseModel):
    """
    A body line contains a statement which is inserted or deleted
    """

    statement: str


class InsertLine(BodyLine):
    """
    A line which is inserted
    """

    def to_clearcase_format(self) -> str:
        return f"> {self.statement}"


class DeleteLine(BodyLine):
    """
    A line which is deleted
    """

    def to_clearcase_format(self):
        return f"< {self.statement}"


class FileHeader(Line, BaseModel):
    """
    A diff between 2 files starts with a summary of the 2 files which are compared
    """

    file1: str
    file2: str

    def to_clearcase_format(self):
        return f"""********************************
<<< file 1: {self.file1}
>>> file 2: {self.file2}
********************************"""


class TransitionLine(Line):
    """
    A transition line might be required at the separation between inserted and deleted
    lines
    """

    def to_clearcase_format(self):
        return "---"
