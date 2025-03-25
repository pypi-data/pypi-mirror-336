import re
from datetime import datetime

from pepito import git_commands
from pepito.gms_files import GmsFile

# matches a line similar to
# GMS-Version          : $gmsVersion: "file.xsd"  foc_30 v6  08-Feb-2021  mihelio $
gms_version_regex = re.compile(
    rb".*\$gmsVersion:\s+\".+\"\s+.*\s+v\d+\s+\d{2}-[a-zA-Z]{3}-\d{4}\s+\w+.*\$"
)
# matches a line similar to
# MD5 of Body          : $md5sum: 6660b3770a54862bd66725533c77e26e $
md5_regex = re.compile(rb".*\$md5sum:\s+\w+\s+\$")


class FileHeaderModifier:
    """
    Service used to modify the header of a file
    """

    def __init__(self, file: GmsFile):
        self.file = file

    def update_gms_version(self, foc: str, version: str) -> None:
        """
        Update the gmsVersion in the file header

        :param foc: the foc version
        :param version: the version
        """
        name = self.file.name
        author = git_commands.get_user_name()
        # the format %d-%b-%Y represents the date as 13-Mar-2025
        date = datetime.today().strftime("%d-%b-%Y")

        new_gms_version = (
            f'$gmsVersion: "{name}"  {foc} {version}  {date}  {author} $'.encode()
        )
        self.file.updated_header = gms_version_regex.sub(
            new_gms_version, self.file.updated_header
        )

    def update_md5sum(self, md5: str) -> None:
        """
        Update the checksum in the file header
        :param md5: the MD5 value
        """
        new_checksum = f"$md5sum: {md5} $".encode()
        self.file.updated_header = md5_regex.sub(new_checksum, self.file.updated_header)

    def apply_modifications(self) -> None:
        """
        Write the modifications to the disk.
        """
        self.file.content = self.file.content.replace(
            self.file.original_header, self.file.updated_header
        )
        self.file.write()
