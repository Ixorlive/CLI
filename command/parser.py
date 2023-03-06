from typing import List

from command.command_factory import CommandFactory
from command.commands import Command, CommandBase
from command.lexer import Lexer
from environment.context_provider import ContextProvider


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.command_factory = CommandFactory()

    def parse_program(self, context_provider: ContextProvider) -> List[Command]:
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
                command = self._parse_command(token.value, context_provider)
            else:
                args.append(token.value)
        if command is not None:
            commands.append(Command(command, args))
        return commands

    def _parse_command(
        self, command_str: str, context_provider: ContextProvider
    ) -> CommandBase:
        if "=" in command_str:
            variable = command_str.split("=")
            return self.command_factory.create_command_base(
                command_name="=",
                var_name=variable[0],
                var_value=variable[1],
                context_provider=context_provider,
            )
        return self.command_factory.create_command_base(command_str)
