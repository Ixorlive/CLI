import io
from command.command_base import CommandBase
from typing import List


class Pwd(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        pass
