import io
from typing import List, TextIO
from abc import ABC, abstractmethod


CODE_OK = 0
CODE_EXIT = -1
INTERNAL_COMMAND_ERROR = -2


class CommandBase(ABC):
    @abstractmethod
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        pass
