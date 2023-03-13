import sys

from command.command_factory import CommandFactory
from executor.executor import CODE_EXIT, Executor
from parsing.lexer import Lexer
from parsing.parser import Parser, ParsingError
from parsing.preprocessing import Preprocessor


class Interpreter:
    """
    A command-line interpreter that reads commands from the user, parses them,
    creates the corresponding command objects, and executes them using an
    Executor instance.
    """

    def __init__(
        self,
        executor: Executor,
        command_factory: CommandFactory,
        preprocessor: Preprocessor,
    ):
        self._executor = executor
        self._command_factory = command_factory
        self._preprocessor = preprocessor

    def run(self):
        """
        Runs the interpreter in a loop, reading commands from the user, parsing
        them, creating the corresponding command objects, and executing them
        using the executor. If an error occurs during parsing or execution, an
        error message is printed to the error stream.
        """
        while True:
            command_line = input("$ ")
            try:
                command_line = self._preprocessor.preprocess(command_line)
                lexer = Lexer(command_line)
                commands = Parser(lexer, self._command_factory).parse_program()
                code_return = self._executor.execute(commands)
                if code_return == CODE_EXIT:
                    return
            except ParsingError as e:
                print(e, file=sys.stderr)
            except Exception as e:
                print("unexpected error", file=sys.stderr)
