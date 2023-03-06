from typing import Tuple

import pytest

from command.commands import *
from command.lexer import Lexer
from command.parser import Parser, ParsingError
from environment.context_provider import ContextProvider


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
    commands = Parser(lexer).parse_program(ContextProvider())
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
        Parser(lexer).parse_program(ContextProvider())
