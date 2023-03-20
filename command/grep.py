import argparse
import re
import sys

from command.command_base import *


class GrepArgumentsParsingError(Exception):
    pass


class CustomArgumentParser(argparse.ArgumentParser):
    """
    A workaround, since ArgumentParser still calls sys.exit on all errors, even with the exit_on_error=False parameter
    """

    def error(self, message):
        self.print_usage(sys.stderr)
        raise GrepArgumentsParsingError(f"{self.prog}: error: {message}\n")


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
        Print lines matching a pattern.
        Args:
            args: A list of command line arguments, which are ignored.
            input_stream: A TextIO object representing the input stream, which is ignored.
            output_stream: A TextIO object representing the output stream to which the current
                working directory path is written.
            error_stream: A TextIO object representing the error stream, which is ignored.
        Returns:
            CODE_OK, indicating successful command execution.
        """
        parser = self._setup_parser()
        try:
            parsed_args = parser.parse_args(args)
        except GrepArgumentsParsingError as e:
            error_stream.write(str(e))
            return INTERNAL_COMMAND_ERROR

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

        if parsed_args.file is not None:
            try:
                with open(parsed_args.file, "r") as file:
                    self._print_lines_matching_pattern(
                        file, output_stream, error_stream, pattern, flags, parsed_args.A
                    )
            except FileNotFoundError:
                error_stream.write(
                    f"grep: {parsed_args.file}: no such file or directory\n"
                )
                return INTERNAL_COMMAND_ERROR
            except OSError:
                error_stream.write(f"grep: {parsed_args.file}: couldn't open file\n")
                return INTERNAL_COMMAND_ERROR
        else:
            self._print_lines_matching_pattern(
                input_stream, output_stream, error_stream, pattern, flags, parsed_args.A
            )

        return CODE_OK

    def _setup_parser(self) -> CustomArgumentParser:
        parser = CustomArgumentParser(prog="grep", add_help=False)
        parser.add_argument("pattern", type=str, help="the pattern to find")
        parser.add_argument(
            "file", metavar="FILE", nargs="?", const=None, help="the files to search"
        )
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
        return parser

    def _print_lines_matching_pattern(
        self,
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
        pattern: str,
        flags: int,
        num_of_context_lines: int,
    ) -> None:
        counter = 0
        for line in input_stream.readlines():
            if re.search(pattern, line, flags) is not None:
                output_stream.write(line)
                counter = num_of_context_lines
            elif counter > 0:
                counter -= 1
                output_stream.write(line)
