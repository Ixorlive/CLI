import os
import sys

from command.command_base import *
from command.commands import Command


class Executor:
    """
    Class responsible for executing a list of commands.
    """

    def execute(self, commands: List[Command]) -> int:
        """
        Executes a list of Command objects.

        Args:
        - commands (List[Command]): A list of Command objects to be executed.

        Returns:
        - int: The exit code of the last executed command.
        """
        if len(commands) == 0:
            return CODE_OK

        error_stream = sys.stderr
        input_stream = sys.stdin
        for command in commands[:-1]:
            next_input_fd, output_fd = os.pipe()
            output_stream = os.fdopen(output_fd, "w")
            command.execute(
                input_stream=input_stream,
                output_stream=output_stream,
                error_stream=error_stream,
            )
            output_stream.close()
            if input_stream is not sys.stdin:
                input_stream.close()
            input_stream = os.fdopen(next_input_fd, "r")

        result = commands[-1].execute(
            input_stream=input_stream,
            output_stream=sys.stdout,
            error_stream=error_stream,
        )

        if result == CODE_EXIT:
            if len(commands) == 1:
                return CODE_EXIT
            else:
                return CODE_OK
        return result
