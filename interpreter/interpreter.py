import sys

from command.command_factory import CommandFactory
from executor.executor import CODE_EXIT, Executor
from parsing.lexer import Lexer
from parsing.parser import Parser, ParsingError


class Interpreter:
    def __init__(self, executor: Executor, command_factory: CommandFactory):
        self._executor = executor
        self._command_factory = command_factory

    def run(self):
        while True:
            command_line = input("$ ")
            try:
                lexer = Lexer(command_line)
                commands = Parser(lexer, self._command_factory).parse_program()
                code_return = self._executor.execute(commands)
                if code_return == CODE_EXIT:
                    return
            except ParsingError as e:
                print(e, file=sys.stderr)
            except Exception as e:
                print("unexpected error", file=sys.stderr)
