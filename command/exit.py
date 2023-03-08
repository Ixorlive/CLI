from command.command_base import *


class Exit(CommandBase):
    """
    A command that immediately exits the shell.
    """

    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        """
        Execute the exit command.

        Args:
            args: A list of strings representing any arguments passed to the command.
            input_stream: A file-like object representing the standard input stream.
            output_stream: A file-like object representing the standard output stream.
            error_stream: A file-like object representing the standard error stream.

        Returns:
            The exit code for the command. In this case, CODE_EXIT.
        """
        return CODE_EXIT
