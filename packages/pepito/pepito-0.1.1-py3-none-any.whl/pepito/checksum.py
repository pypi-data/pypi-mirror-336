import hashlib
import re
from enum import Enum
from pathlib import Path

from rich import print


class FileType(Enum):
    XSD = "xsd"
    XML = "xml"
    XSL = "xsl"
    ASN = "asn"
    MIB = "mib"
    JSON = "json"
    YAML = "yaml"
    YML = "yml"


class Checksum:
    def __init__(self, file: Path, verbose: int = 0):
        self.file = file
        # the file extension is the last part after the "." in the file name
        file_extension = self.file.name.split(".")[-1]
        self.file_type = FileType(file_extension)

        self.bytes: bytes = file.read_bytes()
        # the bytes on which the checksum will  be computed
        self.checksum_bytes = file.read_bytes()

        self.md5_value = None

        self.verbose = verbose

    def compute_md5(self) -> None:
        self.checksum_bytes = self.remove_headers()
        self.checksum_bytes = self.remove_last_blank_lines()

        if self.verbose > 0:
            print(f"Computing MD5 sum of file {self.file}")
        self.md5_value = hashlib.md5(self.checksum_bytes).hexdigest()

    def remove_headers(self) -> bytes:
        if self.verbose > 0:
            print(f"Removing headers of file {self.file}")

        match FileType(self.file_type):
            case FileType.XSD | FileType.XML | FileType.XSL:
                return self.remove_xml_like_headers()
            case FileType.ASN | FileType.MIB:
                return self.remove_asn_like_headers()
            case FileType.JSON:
                return self.remove_json_like_headers()
            case FileType.YAML | FileType.YML:
                return self.remove_yaml_like_headers()
            case _:
                return self.bytes

    def remove_xml_like_headers(self) -> bytes:
        def is_xml_comment_opening(line: bytes) -> bool:
            return line.startswith(b"<!--")

        def is_xml_comment_closing(line: bytes) -> bool:
            return (
                # Linux
                line.endswith(b"-->\n")
                # Windows
                or line.endswith(b"-->\r\n")
                # Mac
                or line.endswith(b"\r")
            )

        lines = self.checksum_bytes.splitlines(keepends=True)

        # the first comment might not be on the first line of the file
        start, end = None, None
        for i in range(len(lines)):
            if not start and is_xml_comment_opening(lines[i]):
                # the comment block starts with <!-- and is considered as the start if the
                # start was not already found
                start = i
            elif start and is_xml_comment_closing(lines[i]):
                # the comment block ends with --> and is considered as the end only if there
                # was as start before
                end = i
                break
            else:
                # nothing specific to do if the line is neither the start nor the end
                continue

        if start and end:
            return b"".join(lines[:start] + lines[end + 1 :])
        return b"".join(lines)

    def remove_asn_like_headers(self) -> bytes:
        def is_comment_line(line: bytes):
            return line.startswith(b"--")

        lines = self.checksum_bytes.splitlines(keepends=True)

        i = 0
        while is_comment_line(lines[i]):
            i += 1
        return b"".join(lines[i:])

    def remove_json_like_headers(self) -> bytes:
        def is_comment_line(line: bytes):
            return line.startswith(b'"__comment__":')

        lines = self.checksum_bytes.splitlines(keepends=True)

        # the first comment might not be on the first line of the file
        start, end = None, None
        for i in range(len(lines)):
            if not start and is_comment_line(lines[i]):
                # the comment block starts with <!-- and is considered as the start if the
                # start was not already found
                start = i
            elif start and not is_comment_line(lines[i]):
                # the comment block ends with --> and is considered as the end only if there
                # was as start before
                end = i
                break
            else:
                # nothing specific to do if the line is neither the start nor the end
                continue

        if start and end:
            return b"".join(lines[:start] + lines[end:])
        return b"".join(lines)

    def remove_yaml_like_headers(self) -> bytes:
        def is_comment_line(line: bytes) -> bool:
            return line.startswith(b"#")

        lines = self.checksum_bytes.splitlines(keepends=True)

        i = 0
        while is_comment_line(lines[i]):
            i += 1
        return b"".join(lines[i:])

    def remove_last_blank_lines(self) -> bytes:
        if self.verbose > 0:
            print(f"Removing trailing blank lines of file {self.file}")
        lines = self.checksum_bytes.splitlines(keepends=True)

        # iterate backwards on the lines
        for i in range(len(lines), 0, -1):
            # watch the previous line so that the last line return is kept
            # if that previous line is not a new line, the process is stopped
            if self.is_empty_line(lines[i - 1]):
                break
        return b"".join(lines[:i])

    @staticmethod
    def is_empty_line(line: bytes) -> bool:
        # \n is used on linux (LF), \r\n on Windows (CRLF) and \r on Mac (CR)
        return line != b"\n" and line != b"\r\n" and line != b"\r"

    def replace_md5_in_headers(self):
        if self.verbose > 0:
            print(f"Replacing MD5 value in the header of file {self.file}")
        replacing_bytes = b"$md5sum: " + str.encode(self.md5_value) + b" $"
        self.bytes = re.sub(rb"\$md5sum: \w* \$", replacing_bytes, self.bytes)
        self.write_file()

    def write_file(self):
        if self.verbose > 0:
            print(f"Writing file {self.file} with the new MD5 value in the header")
        self.file.write_bytes(self.bytes)
