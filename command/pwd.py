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
        """
        Print the current working directory path to the output stream.
        Args:
            args: A list of command line arguments, which are ignored.
            input_stream: A TextIO object representing the input stream, which is ignored.
            output_stream: A TextIO object representing the output stream to which the current
                working directory path is written.
            error_stream: A TextIO object representing the error stream, which is ignored.
        Returns:
            CODE_OK, indicating successful command execution.
        """
        output_stream.write(os.getcwd())
        output_stream.write("\n")
        return CODE_OK
