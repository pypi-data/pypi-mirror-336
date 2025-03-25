from pathlib import Path

from pepito.checksum import Checksum


def run_checksum(file: Path, verbose: int = 0):
    checksum = Checksum(file, verbose)
    checksum.compute_md5()
    checksum.replace_md5_in_headers()
