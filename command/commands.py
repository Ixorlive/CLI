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

# =======================================


class Command:
    def __init__(self, base: CommandBase, args: List[str]):
        self._base = base
        self._args = args

    def execute(
        self,
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        return self._base.execute(self._args, input_stream, output_stream, error_stream)
