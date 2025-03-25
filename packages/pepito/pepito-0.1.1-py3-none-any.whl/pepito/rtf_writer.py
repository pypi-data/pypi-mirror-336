import platform
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from rich import print

AUTO_COLOR = "\\cf0"
RED = "\\cf1"
BLUE = "\\cf2"
BLACK = "\\cf4"

MODERN_COURIER_NEW = "\\f0"
DEFAULT_COURIER_NEW = "\\f1"
TIMES_NEW_ROMAN = "\\f2"
NORMAL_VIEW = "\\viewkind4"
NEW_PARAGRAPH = "\\par"
RESET_PARAGRAPH = "\\pard"
ONE_BYTE_UNICODE = "\\uc1"
BOLD = "\\b"
END_BOLD = "\\b0"
EOL = f"{NEW_PARAGRAPH}\n"
FRENCH = "\\lang1036"
ENGLISH_UK = "\\lang2057"

if platform.system() == "Windows":
    from pathlib import WindowsPath

    WORDPAD_EXE = WindowsPath("c:/", "Applications", "TextPad 4", "TextPad.exe")


class RtfWriter:
    """
    Produce a diff in the Clearcase format and print it as a RTF file.
    """

    def __init__(self, tmp_folder: Path = Path(tempfile.gettempdir())) -> None:
        self.tmp_folder = tmp_folder

    @staticmethod
    def get_file_header() -> str:
        """
        Create the file header

        :return: the header in RTF format
        """
        charset = "{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0 Courier New;}{\\f1\\fnil\\fcharset0 Courier New;}{\\f2\\fnil\\fcharset0 Times New Roman;}}"
        colors = "{\\colortbl ; \\red255\\green0\\blue0; \\red0\\green0\\blue255; \\red0\\green255\\blue0; \\red0\\green0\\blue0;}"
        generator = "{\\*\\generator clearcase2git 0.1;}\n"
        paperformat = "\\landscape\\paperw15840\\paperh12240\\margl720\\margr720\\margt720\\margb720\n"

        parts = [charset, colors, generator, paperformat]
        return "".join(parts)

    def get_diff_header(self, file1: Path, file2: Optional[Path] = None) -> str:
        """
        Create the diff between the 2 files

        :param file1: the first file to compare
        :param file2: the second file to compare
        :return: the diff in RTF format
        """
        if file2 is None or file1 == file2:
            filename = file1.name
            filename1 = ""
            filename2 = ""
        else:
            filename = file2.name
            filename1 = f": {file1.name}"
            filename2 = f": {file2.name}"

        attached_files = f"{NORMAL_VIEW}{ONE_BYTE_UNICODE}{RESET_PARAGRAPH}{RED}{ENGLISH_UK}{MODERN_COURIER_NEW}{self.font_size(20)} {BLUE}{MODERN_COURIER_NEW} Updated file, please refer to the attached files ({AUTO_COLOR}{BOLD} {filename}{BLUE}{MODERN_COURIER_NEW} ).{EOL} {EOL} {EOL}"
        checksum = f"{NORMAL_VIEW}{ONE_BYTE_UNICODE}{RESET_PARAGRAPH}{BLACK}{ENGLISH_UK}{BOLD}{TIMES_NEW_ROMAN}{self.font_size(24)} Note: {END_BOLD} The MD5 checksum of xsd/xml/MIB files is calculated without the header block.{EOL}{EOL}"
        wording_before = f"{NORMAL_VIEW}{ONE_BYTE_UNICODE}{RESET_PARAGRAPH}{RED}{ENGLISH_UK}{BOLD}{MODERN_COURIER_NEW}{self.font_size(24)} < {DEFAULT_COURIER_NEW} Wording before\\tab{AUTO_COLOR}{TIMES_NEW_ROMAN} ({RED} in Red{filename1}{AUTO_COLOR} ) {EOL}"
        transition_line_1 = f"{NORMAL_VIEW}{ONE_BYTE_UNICODE}{RESET_PARAGRAPH}{BLACK}{ENGLISH_UK}{BOLD}{MODERN_COURIER_NEW}{self.font_size(24)} ---{EOL}"
        wording_after = f"{NORMAL_VIEW}{ONE_BYTE_UNICODE}{RESET_PARAGRAPH}{BLUE}{ENGLISH_UK}{BOLD}{MODERN_COURIER_NEW}{self.font_size(24)} > {DEFAULT_COURIER_NEW} Wording after\\tab{AUTO_COLOR}{TIMES_NEW_ROMAN} ({BLUE} in Blue{filename2}{AUTO_COLOR} ) {EOL}"
        transition_line_2 = f"{NORMAL_VIEW}{ONE_BYTE_UNICODE}{RESET_PARAGRAPH}{BLACK}{ENGLISH_UK}{BOLD}{MODERN_COURIER_NEW}{self.font_size(16)} ------------------------------------------------------------------------{END_BOLD} {EOL}"
        header_end = f"{NORMAL_VIEW}{ONE_BYTE_UNICODE}{RESET_PARAGRAPH}{FRENCH}{self.font_size(16)}\n"

        parts = [
            attached_files,
            checksum,
            wording_before,
            transition_line_1,
            wording_after,
            transition_line_2,
            header_end,
        ]
        return "".join(parts)

    @staticmethod
    def get_diff_content(lines: str) -> str:
        """
        Get the diff between the 2 files contents

        :param lines: the lines to compare
        :return: the compared lines as RTF format
        """
        diff = ""
        for line in lines.split("\n"):
            if line.startswith("<"):
                diff += (
                    f"{RED}{MODERN_COURIER_NEW} {line}{BLACK}{MODERN_COURIER_NEW} {EOL}"
                )
            elif line.startswith(">"):
                diff += f"{BLUE}{MODERN_COURIER_NEW} {line}{BLACK}{MODERN_COURIER_NEW} {EOL}"
            else:
                diff += f"{line}{EOL}"
        return diff

    @staticmethod
    def get_diff_footer() -> str:
        """
        Get the RTF footer
        :return: the RTF footer
        """
        return "}\n"

    def write(self, diff: str, rtf_file: str, file1: Path, file2: Path = None) -> None:
        """
        Write the RTF file

        :param diff: the content diff
        :param rtf_file: the path to the RTF file to write in
        :param file1: the first file to compare
        :param file2: the second file to compare
        """
        self.tmp_folder.mkdir(parents=True, exist_ok=True)
        file_content = (
            self.get_file_header()
            + self.get_diff_header(file1, file2)
            + self.get_diff_content(diff)
            + self.get_diff_footer()
        )
        file = self.tmp_folder / rtf_file
        print(f"Writing to {file.absolute()}")
        file.write_text(file_content)

    @staticmethod
    def font_size(size: int) -> str:
        """
        Get the RTF font size

        :param size: the font size value
        :return: the RTF font size
        """
        return f"\\fs{size}"

    def display(self, rtf_file: str) -> None:
        """
        Display the file if on a Windows machine.
        As RTF is a proprietary format, it cannot be displayed on other machines

        :param rtf_file: the file to display
        """
        if platform.system() != "Windows":
            return
        file = self.tmp_folder / rtf_file

        wordpad = subprocess.Popen((WORDPAD_EXE, str(file)))
        wordpad.wait()

        user_quits_doc = subprocess.Popen(
            (
                "ping",
                "1.1.1.1",
                "-n",
                "1",
                "-w",
                "3000",
                ">",
                "nul",
            )
        )
        user_quits_doc.wait()

        file.unlink()
