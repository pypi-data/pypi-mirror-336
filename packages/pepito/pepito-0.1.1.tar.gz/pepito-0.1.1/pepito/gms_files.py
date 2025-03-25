import hashlib
from enum import Enum
from pathlib import Path


class FileType(Enum):
    """
    The type of file, depending on the extension.
    """

    XSD = "xsd"
    XML = "xml"
    XSL = "xsl"
    ASN = "asn"
    MIB = "mib"
    JSON = "json"
    YAML = "yaml"
    YML = "yml"


class GmsFile:
    """
    A file in the GMS context.
    """

    def __init__(self, file_path: Path, verbose: int = 0):
        if file_path.is_dir():
            raise ValueError("The file con not be a directory")

        self.path: Path = file_path
        self.verbose = verbose

        # Bytes are used here because the development was made on Linux and the new
        # lines management was a nightmare with CRLF inputs from Windows, especially for
        # MD5 computation.
        # Feel free to transform all into str if needed
        self.content: bytes = file_path.read_bytes()

        # kept so that it can be found in content not updated content if needed
        self.original_header: bytes = self.get_header()
        # will be updated later
        self.updated_header: bytes = self.original_header

        self.history_lines: bytes = self.last_history_line()
        self.trailing_blank_lines: bytes = self.get_trailing_blank_lines()

        self.md5 = self.compute_md5()

    @property
    def name(self) -> str:
        """
        The name of the file.
        :return: the name of the file
        """
        return self.path.name

    def get_header(self) -> bytes:
        """
        Get the file header
        :return: the file header
        """
        # in case files are not ASN like, XML like, JSON like or YAML like,
        # there is no header
        # This method is overridden by subclasses
        return b""

    def last_history_line(self) -> bytes:
        """
        Get the last history line.
        Usually the history is written with the most recent change above others.
        The history section first line contains 'History'

        :return: the last history line
        """
        header_lines = self.original_header.splitlines()
        for i, line in enumerate(header_lines):
            if b"History" in line:
                return header_lines[i + 1]
        return b""

    def get_trailing_blank_lines(self) -> bytes:
        """
        Get the trailing blank lines. The last new line does not count.

        :return: the trailing blank lines
        """
        if self.verbose > 0:
            print(f"Removing trailing blank lines of file {self.path}")
        lines = self.content.splitlines(keepends=True)

        # iterate backwards on the lines
        i = -1
        for i in range(len(lines), 0, -1):
            # watch the previous line so that the last line return is kept
            # if that previous line is not a new line, the process is stopped
            if self.is_empty_line(lines[i - 1]):
                break
        return b"".join(lines[i:])

    @staticmethod
    def is_empty_line(line: bytes) -> bool:
        """
        Check if a line has content appart from the new line chars

        :param line: the line to check
        :return: True if the line is empty, False otherwise
        """
        # \n is used on linux (LF), \r\n on Windows (CRLF) and \r on Mac (CR)
        return line != b"\n" and line != b"\r\n" and line != b"\r"

    def get_content_for_checksum(self) -> bytes:
        """
        Get the file content for the checksum.
        The checksum is computed on the file content with the header and trailing blank
        lines removed

        :return: the file content for the checksum
        """
        content_without_header = self.content.replace(self.original_header, b"")
        return content_without_header.replace(self.trailing_blank_lines, b"")

    def compute_md5(self) -> str:
        """
        Compute the MD5 hash of the file without the header and trailing blank lines

        :return: the MD5 value
        """
        if self.verbose > 0:
            print(f"Computing MD5 sum of file {self.path.name}")
        content_for_checksum = self.get_content_for_checksum()
        return hashlib.md5(content_for_checksum).hexdigest()

    @staticmethod
    def from_file_path(file: Path, verbose: int = 0):
        """
        Instantiate the right GmsFile depending on the extension.

        :param file: the file path
        :param verbose: the verbosity level
        :return: the right instance of GmsFile
        """
        file_type = file.name.split(".")[-1]
        try:
            match FileType(file_type):
                case FileType.XSD | FileType.XML | FileType.XSL:
                    return XmlLikeGmsFile(file, verbose)
                case FileType.ASN | FileType.MIB:
                    return AsnLikeGmsFile(file, verbose)
                case FileType.JSON:
                    return JsonLikeGmsFile(file, verbose)
                case FileType.YAML | FileType.YML:
                    return YamlLikeGmsFile(file, verbose)
                case _:
                    return GmsFile(file, verbose)
        except ValueError:
            # Case where the file type is not in the predefined types
            return GmsFile(file, verbose)

    def write(self) -> None:
        """
        Write the content of the file on the disk.
        """
        self.path.write_bytes(self.content)

    def __eq__(self, other) -> bool:
        if not isinstance(other, GmsFile):
            return NotImplemented

        return self.path == other.path and self.content == other.content


class XmlLikeGmsFile(GmsFile):
    """
    Files are considered as XML like files when they have the same type of headers.
    Each header line of XML like file start with `"__comment__":`.
    The header starts at after the first line of the XML file.

    As of today `.xml`, `.xsd` and `.xsl` files are XML like files
    """

    def get_header(self) -> bytes:
        lines = self.content.splitlines(keepends=True)

        # the first comment might not be on the first line of the file
        start, end = None, None
        for i in range(len(lines)):
            if not start and self.is_comment_opening(lines[i]):
                # the comment block starts with <!-- and is considered as the start if
                # the start was not already found
                start = i
            elif start and self.is_xml_comment_closing(lines[i]):
                # the comment block ends with --> and is considered as the end only if
                # there was as start before
                end = i
                break
            else:
                # nothing specific to do if the line is neither the start nor the end
                continue

        if start and end:
            return b"".join(lines[start : end + 1])
        return b""

    @staticmethod
    def is_comment_opening(line: bytes) -> bool:
        """
        Check if the line is the first line of a comment.
        A comment block starts with '<!--'

        :param line: the line to test
        :return: True if the line is an opening comment, False otherwise
        """
        return line.startswith(b"<!--")

    @staticmethod
    def is_xml_comment_closing(line: bytes) -> bool:
        """
        Check if the line is the last line of a comment.
        A comment block ends with '-->'

        :param line: the line to test
        :return: True if the line is a closing comment, False otherwise
        """
        return (
            # Linux
            line.endswith(b"-->\n")
            # Windows
            or line.endswith(b"-->\r\n")
            # Mac
            or line.endswith(b"\r")
        )


class AsnLikeGmsFile(GmsFile):
    """
    Files are considered as ASN like files when they have the same type of headers.
    Each header line of ASN like file start with `--`.
    The header starts at the very first line of the ASN file.

    As of today `.asn` and `.mib` files are ASN like files
    """

    def get_header(self) -> bytes:
        lines = self.content.splitlines(keepends=True)

        i = 0
        while self.is_comment_line(lines[i]):
            i += 1
        return b"".join(lines[:i])

    @staticmethod
    def is_comment_line(line: bytes):
        """
        Check if the line is a comment.
        A comment line starts with '--'

        :param line: the line to check
        :return: True if the line is a comment, False otherwise
        """
        return line.startswith(b"--")


class JsonLikeGmsFile(GmsFile):
    """
    Files are considered as JSON like files when they have the same type of headers.
    Each header line of JSON like file start with `"__comment__":`.
    The header starts at after the first line of the JSON file.

    As of today `.json` files are JSON like files
    """

    def get_header(self) -> bytes:
        lines = self.content.splitlines(keepends=True)

        # the first comment might not be on the first line of the file
        start, end = None, None
        for i in range(len(lines)):
            if not start and self.is_comment_line(lines[i]):
                # the comment block starts with <!-- and is considered as the start if
                # the start was not already found
                start = i
            elif start and not self.is_comment_line(lines[i]):
                # the comment block ends with --> and is considered as the end only if
                # there was as start before
                end = i
                break
            else:
                # nothing specific to do if the line is neither the start nor the end
                continue

        if start and end:
            return b"".join(lines[start:end])
        return b""

    @staticmethod
    def is_comment_line(line: bytes):
        """
        Check if the line is a comment line.
        A comment line starts with '"__comment__":'

        :param line: the line to check
        :return: True if the line is a comment line, False otherwise
        """
        return line.startswith(b'"__comment__":')


class YamlLikeGmsFile(GmsFile):
    """
    Files are considered as YAML like files when they have the same type of headers.
    Each header line of YAML like file start with `#`.
    The header starts at the very first line of the YAML file.

    As of today `.yaml` and `.yml` files are YAML like files
    """

    def get_header(self) -> bytes:

        lines = self.content.splitlines(keepends=True)

        i = 0
        while self.is_comment_line(lines[i]):
            i += 1
        return b"".join(lines[:i])

    @staticmethod
    def is_comment_line(line: bytes):
        """
        Check if the line is a comment line.
        A comment line starts with '#'

        :param line: the line to check
        :return: True if the line is a comment line, False otherwise
        """
        return line.startswith(b"#")
