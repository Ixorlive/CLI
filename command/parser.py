from command.commands import Command
from command.lexer import Lexer


class Parser:
    def __init__(self, command_factory, lexer: Lexer):
        pass

    # TODO может parse_command
    def parse_program(self, command_line: str) -> list[Command]:
        pass
