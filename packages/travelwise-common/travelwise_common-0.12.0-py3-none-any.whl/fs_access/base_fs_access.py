from abc import ABC, abstractmethod
from typing import IO, Optional


class BaseFSAccess(ABC):
    @abstractmethod
    def get_file_paths(
        self, directory: str, file_type: str, file_regex: Optional[str]
    ) -> list[str]:
        pass

    @abstractmethod
    def open(self, path: str, mode: str) -> IO:
        # open the given file, mode = "r"/"w"
        pass
