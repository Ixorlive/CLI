from command.command_base import *


class Exit(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        return CODE_EXIT
