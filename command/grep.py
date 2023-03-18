import argparse
import re

from command.command_base import *


class Grep(CommandBase):
    """
    A class that implements grep command
    """

    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        """
        Print the current working directory path to the output stream.
        Args:
            args: A list of command line arguments, which are ignored.
            input_stream: A TextIO object representing the input stream, which is ignored.
            output_stream: A TextIO object representing the output stream to which the current
                working directory path is written.
            error_stream: A TextIO object representing the error stream, which is ignored.
        Returns:
            CODE_OK, indicating successful command execution.
        """
        parser = argparse.ArgumentParser(prog="grep", add_help=False)
        parser.add_argument("pattern", type=str, help="the pattern to find")
        parser.add_argument("file", metavar="FILE", help="the files to search")
        parser.add_argument(
            "-w",
            "--word-regexp",
            action="store_true",
            help="select  only  those lines containing matches that form whole words",
        )
        parser.add_argument(
            "-i", "--ignore-case", action="store_true", help="case-insensitive search"
        )
        parser.add_argument(
            "-A",
            default=0,
            type=int,
            help="Print as many lines as passed in this argument of trailing context after "
            "matching lines",
        )
        parsed_args = parser.parse_args(args)

        if parsed_args.A < 0:
            error_stream.write(
                f"grep: {parsed_args.A}: invalid context length argument"
            )
            return INTERNAL_COMMAND_ERROR

        flags = 0
        if parsed_args.ignore_case:
            flags |= re.IGNORECASE
        pattern = parsed_args.pattern
        if parsed_args.word_regexp:
            pattern = rf"\b{parsed_args.pattern}\b"

        with open(parsed_args.file, "r") as file:
            counter = 0
            for line in file.readlines():
                if counter > 0:
                    counter -= 1
                    output_stream.write(line)
                elif re.search(pattern, line, flags) is not None:
                    output_stream.write(line)
                    counter = parsed_args.A

        return CODE_OK
