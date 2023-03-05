from command.commands import Command
import sys


class Executor:
    def execute(self, commands: list[Command]):
        if len(commands) == 0:
            return
        commands[0].execute(
            input_stream=sys.stdin,
            output_stream=sys.stdout,
            error_stream=sys.stderr,
        )
