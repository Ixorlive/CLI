from abc import ABC, abstractmethod
from typing import List, TextIO

CODE_OK = 0
CODE_EXIT = -1
INTERNAL_COMMAND_ERROR = -2


class CommandBase(ABC):
    """
    Abstract base class for defining command line commands.
    """

    @abstractmethod
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        pass
