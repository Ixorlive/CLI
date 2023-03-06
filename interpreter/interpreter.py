from command.parser import Parser
from command.lexer import Lexer
from executor.executor import Executor
from environment.context_provider import ContextProvider


class Interpreter:
    def __init__(self, executor: Executor, context_provider: ContextProvider):
        self._executor = executor
        # TODO отразить на схеме
        self._context_provider = context_provider

    def run(self):
        # TODO еще над этим циклом и как из него выходить
        # TODO возможно стоит читать строчку аргумент пока кавычки не закрыты?
        # TODO Перехват сигналов?
        while True:
            print("$ ", end="")
            command_line = input()
            # фаза 2: preprocessing
            lexer = Lexer(command_line)
            commands = Parser(lexer).parse_program()
            result = self._executor.execute(commands)
            if result:
                return
            print()
