import os
from command.command_base import *


class Cd(CommandBase):
    """
            A class that implements the 'ls' command.
    """

    def execute(
            self,
            args: List[str],
            input_stream: TextIO,
            output_stream: TextIO,
            error_stream: TextIO,
    ):
        """
        List  information  about  the  FILEs (the current directory by default).
        Args:
            args: A list of command arguments.
            input_stream: The input stream to read from.
            output_stream: The output stream to write to.
            error_stream: The error stream to write to.

        Returns:
            A status code representing the result of the command execution.
        """
        if len(args) == 0:
            os.chdir(os.path.expanduser("~"))
        elif len(args) > 1:
            error_stream.write(f"cd: too many arguments\n")
            return INTERNAL_COMMAND_ERROR
        elif not os.path.exists(args[0]):
            error_stream.write(f"cd: {args[0]}: No such file or directory\n")
            return INTERNAL_COMMAND_ERROR
        elif not os.path.isdir(args[0]):
            error_stream.write(f"cd: {args[0]}: Not a directory\n")
            return INTERNAL_COMMAND_ERROR
        else:
            os.chdir(args[0])

        return CODE_OK
