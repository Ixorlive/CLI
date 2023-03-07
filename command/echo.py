import io
from command.command_base import CommandBase
from typing import List


class Echo(CommandBase):
    def execute(
            self,
            args: List[str],
            input_stream: io.StringIO,
            output_stream: io.StringIO,
            error_stream: io.StringIO,
    ):
        # TODO обработка ошибок?
        output_stream.write(" ".join(args))