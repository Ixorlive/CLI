from command.commands import Command
from typing import List
import sys


class Executor:
    def execute(self, commands: List[Command]):
        if len(commands) == 0:
            return
        commands[0].execute(
            input_stream=sys.stdin,
            output_stream=sys.stdout,
            error_stream=sys.stderr,
        )
