import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import List, TextIO

from environment.context_provider import ContextProvider
from executor import executor


class CommandBase(ABC):
    @abstractmethod
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        pass


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


class Cat(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        if len(args) == 0:
            error_stream.write("cat: file not specified\n")
            return executor.INTERNAL_COMMAND_ERROR
        filename = args[0]
        try:
            with open(filename, "r") as inf:
                shutil.copyfileobj(inf, output_stream)
        except FileNotFoundError:
            error_stream.write(f"cat: {filename}: file not found\n")
            return executor.INTERNAL_COMMAND_ERROR


class Echo(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        output_stream.write(" ".join(args) + "\n")
        return executor.CODE_OK


class Wc(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        pass


class Pwd(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        output_stream.write(os.getcwd())
        return executor.CODE_OK


class Exit(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        return executor.CODE_EXIT


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
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        name = args[0]
        value = args[1]
        self._context_provider.set_variable(name, value)
        return executor.CODE_OK


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
    ) -> int:
        # TODO чтение из input_stream пока не работает
        path_to_command = shutil.which(self._command_name)
        if path_to_command is None:
            error_stream.write(f"{self._command_name}: command not found\n")
            return executor.INTERNAL_COMMAND_ERROR
        completed_process = subprocess.run(
            [path_to_command] + args,
            capture_output=True,
        )
        output_stream.write(completed_process.stdout.decode())
        error_stream.write(completed_process.stderr.decode())
        return executor.CODE_OK
