import shlex
from typing import Iterable, List, NamedTuple


class Token(NamedTuple):
    """
    A token represents a single lexeme in the input line.

    types:
        INTEGER: integers numbers
        OPERATOR: bash operators, see list them in _is_operator()
        IDENTIFIER: any string
    """

    type: str
    value: str


class Lexer(Iterable):
    """
    The Lexer class tokenizes the input line into a sequence of tokens.
    """

    def __init__(self, input_line: str):
        self.tokens = self.tokenize(input_line)
        self.index = 0

    def tokenize(self, input_line: str) -> List[Token]:
        """
        Tokenize the input line and return the sequence of tokens.
        """
        lexer = shlex.shlex(input_line, posix=True)
        lexer.whitespace_split = True
        tokens = []
        # TODO ввод "adjas'" вылетает с ValueError: No closing quotation хотелось бы
        #  чтобы была ошибка лексера на это (либо можно читать stdin пока пользователь
        #  не закроет кавычку)
        for token in lexer:
            if token.isdigit():
                tokens.append(Token(type="INTEGER", value=token))
            elif self._is_operator(token):
                tokens.append(Token(type="OPERATOR", value=token))
            else:
                tokens.append(Token(type="IDENTIFIER", value=token))
        return tokens

    def __iter__(self) -> "Lexer":
        self.index = 0
        return self

    def __next__(self) -> Token:
        if self.index >= len(self.tokens):
            raise StopIteration
        self.index += 1
        return self.tokens[self.index - 1]

    def current_token(self) -> Token:
        return self.tokens[self.index]

    def _is_operator(self, token: str):
        shell_operators = [
            "|",
            "<",
            ">",
            "&&",
            "||",
            "+",
            "-",
            "*",
            "/",
            "**",
            "%",
            "//",
            "<",
            "<=",
            ">",
            ">=",
            "==",
            "!=",
            "&",
            "|",
            "^",
            "~",
            "<<",
            ">>",
        ]
        return token in shell_operators
