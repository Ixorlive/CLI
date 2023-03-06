import io
import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import List, TextIO

from environment.context_provider import ContextProvider


class CommandBase(ABC):
    @abstractmethod
    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        pass


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


class Cat(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        if len(args) == 0:
            error_stream.write("cat: file not specified")
            return
        filename = args[0]
        try:
            with open(filename, "r") as inf:
                shutil.copyfileobj(inf, output_stream)
        except FileNotFoundError:
            error_stream.write(f"cat: {filename}: file not found")


class Echo(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        output_stream.write(" ".join(args))


class Wc(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        pass


class Pwd(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        output_stream.write(os.getcwd())


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
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        name = args[0]
        value = args[1]
        self._context_provider.set_variable(name, value)


# TODO Что делать если запущен bash?
class External(CommandBase):
    def __init__(self, command_name: str):
        self._command_name = command_name

    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ):
        path_to_command = shutil.which(self._command_name)
        if path_to_command is None:
            error_stream.write(f"{self._command_name}: command not found")
            return
        completed_process = subprocess.run(
            [path_to_command] + args,
            input=input_stream.read(),
            capture_output=True,
        )
        output_stream.write(completed_process.stdout)
        error_stream.write(completed_process.stderr)
