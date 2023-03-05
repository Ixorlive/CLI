from command.parser import Parser
from executor.executor import Executor


class Interpreter:
    # TODO название parser все-таки слишком отсылает к синтаксическому
    #  анализу при этом нельзя сказать, что parser ничего
    #  не делает кроме синтаксического анализа. Возможно стоит вернуться
    #  к старому названию CommandReader?
    def __init__(self, parser: Parser, executor: Executor):
        self._parser = parser
        self._executor = executor

    def run(self):
        # TODO еще над этим циклом и как из него выходить
        # TODO возможно стоит читать строчку аргумент пока кавычки не закрыты?
        while True:
            print("$", end="")
            command_line = input()
            commands = self._parser.parse_program(command_line)
            self._executor.execute(commands)
            print()
