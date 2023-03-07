from command.command_base import *


class Echo(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        output_stream.write(" ".join(args) + "\n")
        return CODE_OK
