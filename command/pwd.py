import os
from command.command_base import *


class Pwd(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        output_stream.write(os.getcwd())
        output_stream.write("\n")
        return CODE_OK
