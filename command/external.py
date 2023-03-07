import multiprocessing
import subprocess
import shutil
import os
from command.command_base import *


class External(CommandBase):
    def __init__(self, command_name: str):
        self._command_name = command_name

    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        path_to_command = shutil.which(self._command_name)
        if path_to_command is None:
            error_stream.write(f"{self._command_name}: command not found\n")
            return INTERNAL_COMMAND_ERROR
        proc = subprocess.Popen(
            [path_to_command] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        reading_input = multiprocessing.Process(
            target=_communicate, args=(input_stream.fileno(), proc.stdin.fileno())
        )
        writing_output = multiprocessing.Process(
            target=_communicate, args=(proc.stdout.fileno(), output_stream.fileno())
        )
        errors_output = multiprocessing.Process(
            target=_communicate, args=(proc.stderr.fileno(), error_stream.fileno())
        )
        reading_input.start()
        writing_output.start()
        errors_output.start()

        try:
            proc.wait()
        finally:
            reading_input.kill()
            writing_output.kill()
            errors_output.kill()

        return proc.returncode


def _communicate(src, dst):
    import sys

    sys.stdin = os.fdopen(src, "r")
    sys.stdout = os.fdopen(dst, "w")
    while True:
        try:
            command_input = sys.stdin.read()
            print(command_input)
        except EOFError:
            return
