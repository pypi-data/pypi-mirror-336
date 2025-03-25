from pathlib import Path

from pepito.diff.diff_processor import DiffProcessor
from pepito.diff.rtf_writer import RtfWriter

rtf_writer = RtfWriter()


def run_diff_with_file(file: Path, other: Path):
    diff_processor = DiffProcessor(current_file=file, other_file=other)
    filename = f"diff-{other.name}-{file.name}.rtf"
    diff = diff_processor.to_clearcase_format()

    rtf_writer.write(diff, filename, other, file)
    rtf_writer.display(filename)


def run_diff_with_commit(file: Path, commit_sha1: str):
    diff_processor = DiffProcessor(current_file=file, commit=commit_sha1)
    filename = f"diff-{commit_sha1}-{file.name}.rtf"
    diff = diff_processor.to_clearcase_format()

    rtf_writer.write(diff, filename, file)
    rtf_writer.display(filename)
