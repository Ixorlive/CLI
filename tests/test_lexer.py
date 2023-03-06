from typing import List, Tuple
import pytest

from command.lexer import Lexer, Token


@pytest.mark.parametrize("input_string, expected_tokens", [
    ("", []),
    ("echo \"Hello World\"", [
        Token("IDENTIFIER", "echo"),
        Token("IDENTIFIER", "Hello World")
    ]),
    ("echo 'Hello World'", [
        Token("IDENTIFIER", "echo"),
        Token("IDENTIFIER", "Hello World")
    ]),
    ("echo 'Hello World'", [
        Token("IDENTIFIER", "echo"),
        Token("IDENTIFIER", "Hello World")
    ]),
    ("asdasd fasndf asdpfmasodfasdfas    dadf  asdf asdf a", [
        Token("IDENTIFIER", "asdasd"),
        Token("IDENTIFIER", "fasndf"),
        Token("IDENTIFIER", "asdpfmasodfasdfas"),
        Token("IDENTIFIER", "dadf"),
        Token("IDENTIFIER", "asdf"),
        Token("IDENTIFIER", "asdf"),
        Token("IDENTIFIER", "a"),
    ]),
    ("cat file.txt | grep 'error' > output.txt", [
        Token("IDENTIFIER", "cat"),
        Token("IDENTIFIER", "file.txt"),
        Token("OPERATOR", "|"),
        Token("IDENTIFIER", "grep"),
        Token("IDENTIFIER", "error"),
        Token("OPERATOR", ">"),
        Token("IDENTIFIER", "output.txt"),
    ]),
    # examples
    ("FILE=example.txt", [
        Token("IDENTIFIER", "FILE=example.txt")
    ]),
    ("cat example.txt", [
        Token("IDENTIFIER", "cat"),
        Token("IDENTIFIER", "example.txt")
    ]),
    ("cat example.txt | wc", [
        Token("IDENTIFIER", "cat"),
        Token("IDENTIFIER", "example.txt"),
        Token("OPERATOR", "|"),
        Token("IDENTIFIER", "wc")
    ]),
    ("y=it", [
        Token("IDENTIFIER", "y=it")
    ])
])
def test_lexer(input_string: str, expected_tokens: List[Token]):
    lexer = Lexer(input_string)
    actual_tokens = list(lexer)
    assert actual_tokens == expected_tokens
