import glob
import os
import re
from contextlib import contextmanager
from typing import IO, Optional

from fs_access.base_fs_access import BaseFSAccess


class LocalFSAccess(BaseFSAccess):
    def get_file_paths(
        self, directory: str, file_type: str, file_regex: Optional[str] = None
    ) -> list[str]:
        file_paths = glob.glob(
            os.path.join(directory, "**", f"*.{file_type.lower()}"),
            recursive=True,
        )

        if file_regex:
            pattern = re.compile(file_regex)
            file_paths = [
                path for path in file_paths if pattern.search(os.path.basename(path))
            ]

        return file_paths

    @contextmanager
    def open(self, path: str, mode: str = "r") -> IO:
        with open(path, mode) as f:
            yield f
