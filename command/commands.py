import io
import subprocess

from abc import ABC, abstractmethod

from typing import List


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
        pass


class Echo(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        # TODO обработка ошибок?
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
        pass


class Assign(CommandBase):
    def __init__(self, var_name: str, var_value: str):
        self.var_name = var_name
        self.var_value = var_value

    def execute(
        self,
        args: List[str],
        input_stream: io.StringIO,
        output_stream: io.StringIO,
        error_stream: io.StringIO,
    ):
        pass


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
        completed_process = subprocess.run(
            [self._command_name] + args,
            input=input_stream.read(),
            capture_output=True,
        )
        output_stream.write(completed_process.stdout)
        error_stream.write(completed_process.stderr)
