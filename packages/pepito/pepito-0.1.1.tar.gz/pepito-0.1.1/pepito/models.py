from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CommitLog(BaseModel):
    hash: str
    author: str
    date: datetime
    message: str

    def __str__(self):
        return f"{self.date} - {self.author}: {self.message} ({self.hash})"


class Reference(BaseModel):
    name: str
    id: int
    status: Literal["Approved", "Open"]


class Application(BaseModel):
    status: Literal["In Ref.", "In Anal."]
    first_version: str
    last_version: str

    @classmethod
    def from_str(cls, string: str):
        """
        Create an application based on a formatted string
        :param string:
        :return:
        """
        if string.startswith("["):
            string = string[1:]
        if string.endswith("]"):
            string = string[:-1]
        status, versions = string.split(" - ")
        if " -> " in versions:
            first_version, last_version = versions.split(" -> ")
        else:
            first_version = last_version = versions
        return Application(
            status=status,
            first_version=first_version,
            last_version=last_version,
        )


class FileReference(BaseModel):
    name: str
    application: Application
    gmsVersion: list[str]
    tags: list[str]
    checksum: str
    reference: Reference | None = Field(default=None)
    applicability: list[str]
