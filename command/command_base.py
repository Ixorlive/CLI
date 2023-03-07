import io
from typing import List
from abc import ABC, abstractmethod


class CommandBase(ABC):
    @abstractmethod
    def execute(
            self,
            args: List[str],
            input_stream: io.StringIO,
            output_stream: io.StringIO,
            error_stream: io.StringIO,
    ):
        pass
