from typing import List, TextIO

from command.command_base import CommandBase

# - Import your command here ------------
from command.assign import Assign
from command.cat import Cat
from command.echo import Echo
from command.exit import Exit
from command.external import External
from command.pwd import Pwd
from command.wc import Wc
from command.grep import Grep
from command.ls import Ls
from command.cd import Cd
# =======================================

CODE_OK = 0
CODE_EXIT = -1
INTERNAL_COMMAND_ERROR = -2


class Command:
    """
    A command object that holds a base command and a list of arguments to execute.
    """

    def __init__(self, base: CommandBase, args: List[str]):
        self._base = base
        self._args = args

    def execute(
        self,
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        """
        Execute the command with the given input stream, output stream, and error stream.

        Args:
            input_stream (TextIO): the input stream to use for the command
            output_stream (TextIO): the output stream to use for the command
            error_stream (TextIO): the error stream to use for the command

        Returns:
            int: the return code of the command execution
        """
        return self._base.execute(self._args, input_stream, output_stream, error_stream)
