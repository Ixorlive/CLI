import io
import subprocess
from command.command_base import CommandBase
from typing import List


class External(CommandBase):
    def __init__(self, command_name: str):
        self._command_name = command_name

    def execute(
            self,
            args: List[str],
            input_stream: io.StringIO,
            output_stream: io.StringIO,
            error_stream: io.StringIO,
    ):
        # TODO: Возможно стоит добавить в начало ["cmd", "/c", ...] или ["bash", ...], ибо пока не работает
        completed_process = subprocess.run(
            [self._command_name] + args,
            input=input_stream.read(),
            capture_output=True,
        )
        output_stream.write(completed_process.stdout)
        error_stream.write(completed_process.stderr)
