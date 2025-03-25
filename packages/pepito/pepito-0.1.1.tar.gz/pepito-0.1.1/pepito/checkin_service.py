from pepito.errors import InvalidHeader
from pepito.gms_file_headers_modifier import FileHeaderModifier
from pepito.gms_file_headers_verifier import FileHeaderVerifier
from pepito.gms_files import GmsFile


class CheckInService:
    """
    Service launched at check in.
    It can update the header and verify its integrity.
    """

    def __init__(self, verbose: int = 0) -> None:
        self.verbose: int = verbose

    @staticmethod
    def update_headers(file: GmsFile, foc: str, version: str):
        """
        Update the file checksum and th gmsVersion in the header.

        :param file: the file to update
        :param foc: the foc version
        :param version: the version
        """
        header_modifier = FileHeaderModifier(file)
        header_modifier.update_gms_version(foc, version)

        header_modifier.update_md5sum(file.md5)

        header_modifier.apply_modifications()

    @staticmethod
    def verify_headers(file: GmsFile):
        """
        Verify that the header is consistant

        :param file: the file to verify
        """
        header_verifier = FileHeaderVerifier(file)

        if not header_verifier.is_copyright_ok():
            raise InvalidHeader(f"The copyright in the header of {file} is invalid")

        if not header_verifier.is_filename_ok(file.name):
            raise InvalidHeader(f"The file name in the header of {file} is invalid")

        if not header_verifier.is_md5_ok():
            raise InvalidHeader(f"The md5 checksum in the header of {file} is invalid")

        if not header_verifier.is_modification_reason_ok():
            raise InvalidHeader(
                f"The modification reason in the header of {file} is invalid"
            )
