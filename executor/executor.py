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
        result = commands[0].execute(
            input_stream=sys.stdin,
            output_stream=sys.stdout,
            error_stream=sys.stderr,
        )
        # if result == CODE_EXIT:
        #     if len(commands) == 1:
        #         return CODE_EXIT
        #     else:
        #         return CODE_OK
        return result
