import hashlib
import re
from enum import Enum
from pathlib import Path
from typing import Optional


class FileType(Enum):
    XSD = "xsd"
    ASN = "asn"
    MIB = "mib"


class Checksum:
    def __init__(
        self,
        file: Optional[Path] = None,
        text: Optional[str] = None,
        filetype: Optional[FileType] = None,
    ):
        if file:
            self.file = file
            self.text = file.read_text()
            self.type = FileType(file.name.split(".")[-1])
        else:
            self.text = text
            self.type = filetype
        self.updated_text = text

    def md5(self) -> str:
        text_without_headers = self.remove_headers(self.text)
        final_text = self.remove_last_blank_lines(text_without_headers)
        return hashlib.md5(final_text.encode("utf-8")).hexdigest()

    def remove_headers(self, text: str) -> str:
        if self.type is FileType.XSD:
            return self.remove_xsd_headers(text)
        else:
            return self.remove_asn_mib_headers(text)

    def remove_xsd_headers(self, text: str) -> str:
        lines = text.splitlines()

        start, end = None, None
        for i in range(len(lines)):
            if not start and lines[i].startswith("<!--"):
                # the comment block starts with <!-- and is considered as the start if the
                # start was not already found
                start = i
            elif start and lines[i].endswith("-->"):
                # the comment block ends with --> and is considered as the end only if there
                # was as start before
                end = i
                break
            else:
                # nothing specific to do if the line is neither the start nor the end
                continue

        if not start or not end:
            return text

        return "\n".join(lines[:start] + lines[end + 1 :])

    def remove_asn_mib_headers(self, text: str) -> str:
        lines = text.splitlines()

        i = 0
        while lines[i].startswith("--"):
            i += 1
        return "\n".join(lines[i + 1 :])

    def remove_last_blank_lines(self, text: str) -> str:
        lines = text.splitlines()

        for i in range(len(lines), 0, -1):
            if lines[i - 1] != "":
                break
        return "\n".join(lines[:i])

    def change_header(self):
        md5 = self.md5()
        self.updated_text = re.sub(r"\$md5sum: \w* \$", f"$md5sum: {md5} $", self.text)

    def write_file(self):
        self.file.write_text(self.updated_text)
