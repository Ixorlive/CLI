from command.lexer import Lexer
from command.parser import Parser, ParsingError
from command.command_factory import CommandFactory
from executor import executor


class Interpreter:
    def __init__(self, executor: executor.Executor, command_factory: CommandFactory):
        self._executor = executor
        self._command_factory = command_factory

    def run(self):
        # TODO возможно стоит читать строчку аргумент пока кавычки не закрыты?
        while True:
            print("$ ", end="")
            command_line = input()
            # фаза 2: preprocessing
            try:
                lexer = Lexer(command_line)
                commands = Parser(lexer, self._command_factory).parse_program()
                result = self._executor.execute(commands)
                if result == executor.CODE_EXIT:
                    return
            except ParsingError as e:
                print(e)
            except Exception as e:
                print()
