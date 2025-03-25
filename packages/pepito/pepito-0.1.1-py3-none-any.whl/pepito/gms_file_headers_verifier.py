import re

from pepito.gms_files import GmsFile

# matches a line similar to
# GMS-Version          : $gmsVersion: "invalid_gms_version.xsd"  foc_30 v6  08-Feb-2021  mihelio $
# and get the file name, the foc, the version, the date and the author
gms_version_regex = re.compile(
    rb".*\$gmsVersion:\s+\"(.+)\"\s+(.*)\s+(v\d+)\s+(\d{2}-[a-zA-Z]{3}-\d{4})\s+(\w+).*\$"
)

# matches a line similar to
# .*Copyright\s+: E[CU] Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
copyright_regex = re.compile(
    rb".*Copyright\s+: E[CU] Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed."
)

# matches a line similar to
# MD5 of Body          : $md5sum: 6660b3770a54862bd66725533c77e26e $
md5_regex = re.compile(rb".*\$md5sum:\s+(\w+)\s+\$")

# matches a line similar to
# Updated as per GAL-IRN-TAS-GMS-X-4578 IS=2 ID=6
modification_reason_regex = re.compile(
    rb"(GAL|G2GIOV)-(IRN|DCP|ACI)-TAS-(GMS|ETE|GMS-X|WP2X-X)-([0-9]{1,6})\s+IS=(\d{1,4}\s+ID=(\d{1,4}))"
)


class FileHeaderVerifier:
    """
    Service used to verify the file header is correct
    """

    def __init__(self, file: GmsFile):
        self.file: GmsFile = file

    def is_gms_version_ok(self) -> bool:
        """
        Check the gmsVersion

        :return: True if the gmsVersion is correct, False otherwise
        """
        for line in self.file.original_header.splitlines():
            matches = gms_version_regex.findall(line)
            if matches:
                filename, foc, version, date, author = matches[0]
                return self.is_filename_ok(filename.decode())
        return False

    def is_filename_ok(self, filename: str) -> bool:
        """
        Check the filename

        :param filename: the filename
        :return: True if the filename is correct, False otherwise
        """
        return filename == self.file.name

    def is_copyright_ok(self) -> bool:
        """
        Check the copyright

        :return: True if the copyright is correct, False otherwise
        """
        for line in self.file.original_header.splitlines():
            if copyright_regex.match(line):
                return True
        return False

    def is_md5_ok(self) -> bool:
        """
        Check the MD5

        :return: True if the MD5 is correct, False otherwise
        """
        for line in self.file.original_header.splitlines():
            matches = md5_regex.match(line)
            if matches:
                return matches.group(1).decode() == self.file.md5
        return False

    def is_modification_reason_ok(self) -> bool:
        """
        Check the modification reason

        :return: True if the modification reason is correct, False otherwise
        """
        return bool(modification_reason_regex.findall(self.file.last_history_line()))
