from command.command_base import *


class Echo(CommandBase):
    """
    A class representing the 'echo' command, which writes its arguments to standard output.
    """

    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        """
        Executes the 'echo' command by writing its arguments to standard output.

        Args:
            args: A list of strings representing any arguments passed to the command.
            input_stream: A file-like object representing the standard input stream.
            output_stream: A file-like object representing the standard output stream.
            error_stream: A file-like object representing the standard error stream.

        Returns:
            An integer code representing the status of the command after execution.
        """
        output_stream.write(" ".join(args) + "\n")
        return CODE_OK
