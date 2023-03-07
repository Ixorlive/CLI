import os
import shutil
import subprocess
import multiprocessing
import io
from abc import ABC, abstractmethod
from typing import List

from environment.context_provider import ContextProvider

# internal result codes
CODE_OK = 0
CODE_EXIT = -1
INTERNAL_COMMAND_ERROR = -2


class CommandBase(ABC):
    @abstractmethod
    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        pass


class Command:
    def __init__(self, base: CommandBase, args: List[str]):
        self._base = base
        self._args = args

    def execute(
        self,
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        return self._base.execute(self._args, input_stream, output_stream, error_stream)


class Cat(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        if len(args) == 0:
            error_stream.write("cat: file not specified\n")
            return INTERNAL_COMMAND_ERROR
        filename = args[0]
        try:
            with open(filename, "r") as inf:
                shutil.copyfileobj(inf, output_stream)
        except FileNotFoundError:
            error_stream.write(f"cat: {filename}: file not found\n")
            return INTERNAL_COMMAND_ERROR


class Echo(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        output_stream.write(" ".join(args) + "\n")
        return CODE_OK


class Wc(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        pass


class Pwd(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        output_stream.write(os.getcwd())
        return CODE_OK


class Exit(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        return CODE_EXIT


class Assign(CommandBase):
    def __init__(
        self, var_name: str, var_value: str, context_provider: ContextProvider
    ):
        self._var_name = var_name
        self._var_value = var_value
        self._context_provider = context_provider

    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
    ) -> int:
        self._context_provider.set_variable(self._var_name, self._var_value)
        return CODE_OK


# TODO Что делать если запущен bash?
class External(CommandBase):
    def __init__(self, command_name: str):
        self._command_name = command_name

    def execute(
        self,
        args: List[str],
        input_stream: io.FileIO,
        output_stream: io.FileIO,
        error_stream: io.FileIO,
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
