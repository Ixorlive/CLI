import shutil

from command.command_base import *


class Cat(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        if not args:
            output_stream.write(input_stream.read())
            return CODE_OK

        for arg in args:
            try:
                with open(arg, "r") as file:
                    shutil.copyfileobj(file, output_stream)
            except FileNotFoundError:
                error_stream.write(f"cat: {arg}: No such file or directory\n")
                return INTERNAL_COMMAND_ERROR
        return CODE_OK
