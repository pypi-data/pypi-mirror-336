from pathlib import Path

from pydantic import TypeAdapter

from pepito.models import FileReference


class ReferenceFile:
    """
    The reference file is a file at the git root directory that contains information on
     all the files inside the directory.
    """

    def __init__(self, reference_file: Path):
        self.reference_file = reference_file
        self.files_attributes: list[FileReference] = []

    def read(self) -> None:
        """
        Read the contents of the reference file
        """
        data = self.reference_file.read_text()
        files_adapter = TypeAdapter(list[FileReference])
        self.files_attributes = files_adapter.validate_json(data)

    def write(self) -> None:
        """
        Write the contents of the reference file on the disk
        """
        files_adapter = TypeAdapter(list[FileReference])
        self.reference_file.write_bytes(
            files_adapter.dump_json(self.files_attributes, by_alias=True, indent=2)
        )

    def add(self, file_attributes: FileReference) -> None:
        """
        Add a file attribute to the reference file

        :param file_attributes: the file attributes to add
        """
        self.files_attributes.append(file_attributes)

    def remove(self, file_attributes: FileReference) -> None:
        """
        Remove a file attribute from the reference file

        :param file_attributes: the file attributes to remove
        """
        for file_attr in self.files_attributes:
            if file_attr == file_attributes:
                self.files_attributes.remove(file_attr)
