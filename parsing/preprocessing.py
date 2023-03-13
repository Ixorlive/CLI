from environment.context_provider import ContextProvider
from typing import Tuple


class Preprocessor:

    def __init__(self, context_provider: ContextProvider):
        self.context = context_provider
        self._in_single_quotes = False
        self._in_double_quotes = False

    def preprocess(self, input_str: str) -> str:
        result = ""
        while 1:
            pos_variable = self._find_pos(input_str)
            if pos_variable > 0 and input_str[pos_variable - 1] == '\\':
                result += input_str[:pos_variable - 1] + "$"
                input_str = input_str[pos_variable + 1:]
            elif pos_variable != -1:
                result += input_str[:pos_variable]
                var_name = self._get_variable_name(input_str[pos_variable + 1:])
                if not var_name:
                    result += "$"
                else:
                    value = self.context.get_variable(var_name)
                    result += value if value else ""
                input_str = input_str[pos_variable + len(var_name) + 1:]
            else:
                result += input_str
                break
        return result

    def _find_pos(self, src_str: str) -> int:
        for pos, c in enumerate(src_str):
            self._in_single_quotes ^= (c == '\'' and not self._in_double_quotes)
            self._in_double_quotes ^= (c == '\"' and not self._in_single_quotes)
            if not self._in_single_quotes and c == '$':
                return pos
        return -1

    @staticmethod
    def _get_variable_name(src_str: str) -> str:
        variable_name = ""
        if src_str[0].isnumeric():
            return src_str[0]
        for c in src_str:
            if Preprocessor._is_valid(c):
                variable_name += c
            else:
                break
        return variable_name

    @staticmethod
    def _is_valid(c: str) -> bool:
        return c.isalpha() or c.isnumeric() or c == '_'


if __name__ == "__main__":
    context: ContextProvider = ContextProvider()
    context.set_variable("test", "hello")
    context.set_variable("test_t", "hello1")
    context.set_variable("test12_", "hello2")
    input_line = "echo \"$test's $test12_\""
    preprocessor = Preprocessor(context)
    print(preprocessor.preprocess(input_line))
