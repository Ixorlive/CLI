from typing import List

from command.command_factory import CommandFactory
from command.commands import Command, CommandBase
from parsing.lexer import Lexer


class ParsingError(Exception):
    """An error raised when there is a problem parsing a command."""

    pass


class Parser:
    def __init__(self, lexer: Lexer, command_factory: CommandFactory):
        self.lexer = lexer
        self.command_factory = command_factory

    def parse_program(self) -> List[Command]:
        """
        Parse a program from the tokens produced by the lexer.

        Returns:
            List[Command]: The list of parsed commands.
        """
        commands: List[Command] = []
        args: List[str] = []
        command = None
        for token in self.lexer:
            if token.type == "OPERATOR":
                if token.value == "|":
                    commands.append(Command(command, args))
                    command = None
                    args = []
                else:
                    raise ParsingError("Unknown operator " + token.value)
            elif command is None:
                command = self._parse_command(token.value)
            else:
                args.append(token.value)
        if command is not None:
            commands.append(Command(command, args))
        return commands

    def _parse_command(self, command_str: str) -> CommandBase:
        if "=" in command_str:
            variable = command_str.split("=")
            return self.command_factory.create_command_base(
                command_name="=",
                var_name=variable[0],
                var_value=variable[1],
            )
        return self.command_factory.create_command_base(command_str)
