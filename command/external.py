import os
import shutil
import subprocess
import sys

from command.command_base import *


class External(CommandBase):
    """
    A command that executes an external program.
    """

    def __init__(self, command_name: str):
        """
        Initializes an instance of the External command with the specified command name.
        Args:
            command_name: The name of the external command to execute.
        """
        self._command_name = command_name

    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        """
        Executes the external command with the specified arguments and input/output streams.
        Args:
            args: A list of command line arguments to pass to the external command.
            input_stream: A TextIO object representing the input stream for the command.
            output_stream: A TextIO object representing the output stream for the command.
            error_stream: A TextIO object representing the error stream for the command.
        Returns:
            An integer representing the return code of the external command.
        """
        path_to_command = shutil.which(self._command_name)
        if path_to_command is None:
            error_stream.write(f"{self._command_name}: command not found\n")
            return INTERNAL_COMMAND_ERROR
        if input_stream is sys.stdin:
            proc = subprocess.run(
                [path_to_command] + args,
                stdin=sys.stdin,
                stdout=output_stream,
                stderr=error_stream,
            )
        else:
            proc = subprocess.run(
                [path_to_command] + args,
                input=input_stream.read().encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output_stream.write(proc.stdout.decode())
            error_stream.write(proc.stderr.decode())
        return proc.returncode


def _communicate(src, dst):
    import sys

    sys.stdin = os.fdopen(src, "r")
    sys.stdout = os.fdopen(dst, "w")
    while True:
        try:
            command_input = input()
            print(command_input)
        except EOFError:
            return
