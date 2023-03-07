import io
from command.command_base import CommandBase
from typing import List


class Cat(CommandBase):
    def execute(
            self,
            args: List[str],
            input_stream: io.StringIO,
            output_stream: io.StringIO,
            error_stream: io.StringIO,
    ):
        if not args:
            output_stream.write(input_stream.read())
            return

        for arg in args:
            try:
                with open(arg, "r") as file:
                    output_stream.write(file.read())
            except FileNotFoundError:
                error_stream.write(f"cat: {arg}: No such file or directory\n")
