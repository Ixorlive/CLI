import shutil

from command.command_base import *


class Cat(CommandBase):
    """
    A command that concatenates and displays the contents of files.

    If no arguments are provided, it reads from the standard input and writes to the standard output.
    If file arguments are provided, it reads each file and writes their contents to the standard output.

    If a file is not found, it writes an error message to the error stream and returns an error code.
    """

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
            except OSError:
                error_stream.write(f"cat: {arg}: Couldn't open file\n")
                return INTERNAL_COMMAND_ERROR
        return CODE_OK
