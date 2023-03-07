import sys
from typing import List

from command.commands import Command, CODE_OK, CODE_EXIT


class Executor:
    def execute(self, commands: List[Command]) -> int:
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
