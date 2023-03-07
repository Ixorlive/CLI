from command.lexer import Lexer
from command.parser import Parser
from command.command_factory import CommandFactory
from executor.executor import Executor


class Interpreter:
    def __init__(self, executor: Executor, command_factory: CommandFactory):
        self._executor = executor
        # TODO отразить на схеме
        self._command_factory = command_factory

    def run(self):
        # TODO еще над этим циклом и как из него выходить
        # TODO возможно стоит читать строчку аргумент пока кавычки не закрыты?
        while True:
            print("$ ", end="")
            command_line = input()
            # фаза 2: preprocessing
            lexer = Lexer(command_line)
            commands = Parser(lexer, self._command_factory).parse_program()
            result = self._executor.execute(commands)
            if result:
                return
            print()
