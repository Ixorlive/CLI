import io
import subprocess

from typing import List
from command.command_base import CommandBase
from command.wc import Wc
from command.echo import Echo
from command.pwd import Pwd
from command.cat import Cat
from command.assign import Assign
from command.external import External


class Command:
    def __init__(self, base: CommandBase, args: List[str]):
        self._base = base
        self._args = args

    def execute(
            self,
            input_stream: io.StringIO,
            output_stream: io.StringIO,
            error_stream: io.StringIO,
    ):
        self._base.execute(self._args, input_stream, output_stream, error_stream)





