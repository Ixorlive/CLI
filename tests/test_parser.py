from typing import Tuple

import pytest

from command.command_factory import CommandFactory
from command.commands import *
from environment.context_provider import ContextProvider
from parsing.lexer import Lexer
from parsing.parser import Parser, ParsingError


@pytest.mark.parametrize(
    "input_string, expected_commands",
    [
        ("", []),
        ('echo "Hello World"', [(Echo, ["Hello World"])]),
        ("echo 123 | wc", [(Echo, ["123"]), (Wc, [])]),
        ("echo text.txt | cat -n", [(Echo, ["text.txt"]), (Cat, ["-n"])]),
        ("file=text", [(Assign, [])]),
        (
            "cat test | echo test | wc test test test | cat test",
            [
                (Cat, ["test"]),
                (Echo, ["test"]),
                (Wc, ["test", "test", "test"]),
                (Cat, ["test"]),
            ],
        ),
        (
            "pwd test 'test test test' | echo",
            [(Pwd, ["test", "test test test"]), (Echo, [])],
        ),
    ],
)
def test_parser(input_string: str, expected_commands: List[Tuple[Command, List[str]]]):
    lexer = Lexer(input_string)
    context_provider = ContextProvider()
    command_factory = CommandFactory(context_provider)
    commands = Parser(lexer, command_factory).parse_program()
    assert len(commands) == len(expected_commands)
    for actual_command, expected_command in zip(commands, expected_commands):
        assert isinstance(actual_command._base, expected_command[0])
        assert actual_command._args == expected_command[1]


@pytest.mark.parametrize(
    "input_string",
    ["echo 1+1 | cat hello - hello", "echo 123 < text.txt", "pwd >> echo 123"],
)
def test_parser_exception(input_string: str):
    with pytest.raises(ParsingError):
        lexer = Lexer(input_string)
        context_provider = ContextProvider()
        command_factory = CommandFactory(context_provider)
        Parser(lexer, command_factory).parse_program()
