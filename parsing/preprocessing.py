from environment.context_provider import ContextProvider


class Preprocessor:
    """
    The Preprocessor class takes a ContextProvider object as input and provides methods for preprocessing input strings,
    replacing variables with their values.
    """

    def __init__(self, context_provider: ContextProvider):
        self.context = context_provider
        self._in_single_quotes = False
        self._in_double_quotes = False

    def preprocess(self, input_str: str) -> str:
        """

        Replaces occurrences of variables in the input string with their values, based on the provided ContextProvider.
        Variables are denoted by the '$' symbol.
        If the variable is inside single quotes, no substitution is done.
        If there is a '\' character before the '$' symbol, it is skipped and the '$' symbol is added to the output.
        If the variable is inside a substitution (${var_name}) - no supported case =( :TODO add support
        If there are no valid characters for the variable name after the '$' symbol, no substitution is done.
        If the ContextProvider returns None for a variable, it is replaced with an empty string.
        If the variable name starts with a number, the '$' symbol
            and the number are replaced with an empty string (as in bash).
        In all other cases, the variable is substituted with its value, e.g. '$var_name' -> 'value'.
        """
        result = ""
        while 1:
            pos_variable = self._find_pos(input_str)
            if pos_variable > 0 and input_str[pos_variable - 1] == "\\":
                result += input_str[: pos_variable - 1] + "$"
                input_str = input_str[pos_variable + 1 :]
            elif pos_variable != -1:
                result += input_str[:pos_variable]
                var_name = self._get_variable_name(input_str[pos_variable + 1 :])
                if not var_name:
                    result += "$"
                else:
                    value = self.context.get_variable(var_name)
                    result += value if value else ""
                input_str = input_str[pos_variable + len(var_name) + 1 :]
            else:
                result += input_str
                break
        if self._in_single_quotes or self._in_double_quotes:
            # error will be in lexer, idk what to do
            self._in_single_quotes = self._in_double_quotes = False
        return result

    def _find_pos(self, src_str: str) -> int:
        """
        Finds the position '$' character that is not inside a single-quoted
        """
        for pos, c in enumerate(src_str):
            self._in_single_quotes ^= c == "'" and not self._in_double_quotes
            self._in_double_quotes ^= c == '"' and not self._in_single_quotes
            if not self._in_single_quotes and c == "$":
                return pos
        return -1

    @staticmethod
    def _get_variable_name(src_str: str) -> str:
        """
        Gets the variable name following a '$' character in a string.
        """
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
        return c.isalpha() or c.isnumeric() or c == "_"
